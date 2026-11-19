#!/usr/bin/env python3
"""Validate generated HTML, sitemap, JSON-LD, links and analytics hooks."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://pangeo57-debug.github.io/pg-ai-solutions"
PAGES = [
    "", "services.html", "work.html", "studio.html",
    "privacy.html", "terms.html", "el/",
    "el/services.html", "el/work.html", "el/studio.html",
    "el/privacy.html", "el/terms.html",
]


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.h1 = 0
        self.in_h1 = False
        self.tags = {}
        self.links = []
        self.images = []
        self.jsonld = []
        self.in_jsonld = False
        self.jsonld_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1 += 1
            self.in_h1 = True
        if tag in ("meta", "link", "img", "a", "script"):
            self.tags.setdefault(tag, []).append(attrs)
        if tag == "img":
            self.images.append(attrs)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_jsonld = True
            self.jsonld_text = []

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "h1":
            self.in_h1 = False
        if tag == "script" and self.in_jsonld:
            self.in_jsonld = False
            self.jsonld.append("".join(self.jsonld_text))

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_jsonld:
            self.jsonld_text.append(data)


def file_for(url_path):
    if url_path in ("", "/"):
        return ROOT / "index.html"
    path = url_path.strip("/")
    candidate = ROOT / path
    if candidate.is_dir():
        return candidate / "index.html"
    if candidate.suffix == "":
        candidate = candidate.with_suffix(".html")
    return candidate


errors = []
titles = {}
for page in PAGES:
    if page == "":
        rel = "index.html"
    elif page == "el/":
        rel = "el/index.html"
    else:
        rel = page
    path = ROOT / rel
    if not path.exists():
        errors.append(f"{page}: missing generated file")
        continue
    parser = AuditParser()
    parser.feed(path.read_text(encoding="utf-8"))

    if parser.h1 != 1:
        errors.append(f"{page}: expected one H1, found {parser.h1}")
    if not parser.title.strip():
        errors.append(f"{page}: missing title")
    elif parser.title.strip() in titles:
        errors.append(f"{page}: duplicate title {parser.title.strip()}")
    titles[parser.title.strip()] = page

    metas = {x.get("name"): x.get("content") for x in parser.tags.get("meta", []) if x.get("name")}
    if not metas.get("description"):
        errors.append(f"{page}: missing meta description")
    links = {x.get("rel"): x.get("href") for x in parser.tags.get("link", []) if x.get("rel")}
    canonical = next((x.get("href") for x in parser.tags.get("link", []) if x.get("rel") == "canonical"), None)
    if page == "":
        canonical_expected = BASE + "/"
    elif page == "el/":
        canonical_expected = BASE + "/el/"
    else:
        canonical_expected = BASE + "/" + page
    if canonical != canonical_expected:
        errors.append(f"{page}: canonical {canonical!r} != {canonical_expected}")

    og = {x.get("property"): x.get("content") for x in parser.tags.get("meta", []) if x.get("property")}
    for key in ("og:title", "og:description", "og:url", "og:image", "twitter:title", "twitter:description", "twitter:image"):
        if not og.get(key) and not (key.startswith("twitter") and metas.get(key)):
            if not (key.startswith("twitter") and next((x.get("content") for x in parser.tags.get("meta", []) if x.get("name") == key), None)):
                errors.append(f"{page}: missing {key}")

    for raw in parser.jsonld:
        try:
            json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{page}: invalid JSON-LD: {exc}")

    for attrs in parser.images:
        if attrs.get("alt") is None:
            errors.append(f"{page}: img missing alt attribute: {attrs.get('src')}")

    for href in parser.links:
        if href.startswith(("http://", "https://", "tel:", "mailto:", "#")):
            continue
        clean = href.split("#", 1)[0].split("?", 1)[0]
        target = (path.parent / clean).resolve() if clean else path.resolve()
        if clean.startswith("../"):
            target = (path.parent / clean).resolve()
        if not target.exists():
            errors.append(f"{page}: broken internal link {href}")

sitemap = ROOT / "sitemap.xml"
if not sitemap.exists():
    errors.append("missing sitemap.xml")
else:
    try:
        root = ET.parse(sitemap).getroot()
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [node.text for node in root.findall(".//sm:loc", ns)]
        for page in PAGES:
            if page in ("", "el/"):
                expected = BASE + "/" if page == "" else BASE + "/el/"
            else:
                expected = BASE + "/" + page
            if expected not in locs:
                errors.append(f"sitemap: missing {expected}")
    except ET.ParseError as exc:
        errors.append(f"sitemap: invalid XML: {exc}")

robots = (ROOT / "robots.txt").read_text(encoding="utf-8") if (ROOT / "robots.txt").exists() else ""
if "Sitemap:" not in robots or BASE + "/sitemap.xml" not in robots:
    errors.append("robots.txt: missing absolute sitemap URL")

for hook in ("cta_click", "form_submit_success", "form_submit_failure", "phone_click", "email_click", "service_link_click", "project_link_click", "navigation_click"):
    if hook not in (ROOT / "assets/site.js").read_text(encoding="utf-8"):
        errors.append(f"analytics: missing hook {hook}")

js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
build = (ROOT / "scripts/build.py").read_text(encoding="utf-8")
if "PG_GA4_ID" not in build or "GA4_MEASUREMENT_ID" not in build:
    errors.append("analytics: build configuration missing")
if "PG_ANALYTICS" not in build:
    errors.append("analytics: page configuration missing")

for secret_name in ("API_KEY", "CLIENT_SECRET", "PRIVATE_KEY", "PASSWORD", "ACCESS_TOKEN"):
    if re.search(r"\b" + secret_name + r"\b\s*[:=]\s*[\"'][^\"']+[\"']", build + "\n" + js):
        errors.append(f"security: possible exposed secret {secret_name}")
if "PG_TURNSTILE_SITE_KEY" not in build:
    errors.append("security: Turnstile build configuration missing")
if "submitKey='pg-form-submit-until'" not in js:
    errors.append("security: form submission cooldown missing")

if errors:
    print("\n".join("ERROR " + error for error in errors))
    sys.exit(1)
print(f"SEO validation passed: {len(PAGES)} pages, sitemap, robots, JSON-LD, links and analytics hooks")
