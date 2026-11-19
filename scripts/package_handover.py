#!/usr/bin/env python3
"""Build, validate and package the client handover without exposing secrets."""
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist"
ZIP = OUT / "pg-ai-solutions-client-handover.zip"

INCLUDE_DIRS = ("assets", "el", "logo")
INCLUDE_FILES = (
    "404.html", "_headers", "index.html", "privacy.html", "robots.txt",
    "services.html", "sitemap.xml", "studio.html", "terms.html", "work.html",
    "README.md", "HANDOVER.md",
)
INCLUDE_SCRIPTS = ("build.py", "set-domain.sh", "validate_seo.py", "package_handover.py")


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


run("python3", "scripts/build.py")
run("python3", "scripts/validate_seo.py")

OUT.mkdir(parents=True, exist_ok=True)
if ZIP.exists():
    ZIP.unlink()

handover = OUT / "CLIENT-HANDOVER.md"
handover.write_text(
    """# PG AI Solutions — Client Handover\n\n"""
    "## Live review\n\n"
    "https://pangeo57-debug.github.io/pg-ai-solutions/\n\n"
    "## Included\n\n"
    "- Bilingual generated website\n"
    "- Build and SEO validation scripts\n"
    "- Deployment, privacy, handover and domain instructions\n"
    "- Sitemap, robots.txt, security headers and responsive assets\n\n"
    "## Before launch\n\n"
    "1. Register or transfer the approved custom domain.\n"
    "2. Configure DNS and production hosting.\n"
    "3. Activate an official company email and Formspree account.\n"
    "4. Configure Turnstile, Cloudflare WAF/IP limits and GA4 only if approved.\n"
    "5. Complete legal entity details and verify Search Console.\n",
    encoding="utf-8",
)

with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as archive:
    archive.write(handover, "CLIENT-HANDOVER.md")
    for name in INCLUDE_FILES:
        path = ROOT / name
        if path.exists():
            archive.write(path, name)
    for name in INCLUDE_DIRS:
        path = ROOT / name
        if path.exists():
            for file in path.rglob("*"):
                if file.is_file():
                    archive.write(file, file.relative_to(ROOT).as_posix())
    scripts_dir = ROOT / "scripts"
    for name in INCLUDE_SCRIPTS:
        path = scripts_dir / name
        if path.exists():
            archive.write(path, f"scripts/{name}")

handover.unlink()
print(ZIP)
