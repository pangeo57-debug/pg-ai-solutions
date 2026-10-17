#!/usr/bin/env bash
# Χρήση: scripts/set-domain.sh https://www.to-domain-sou.gr
# Αλλάζει το βασικό URL σε όλα τα αρχεία (canonical, hreflang, sitemap, OG, JSON-LD).
set -euo pipefail
NEW="${1:?Δώσε το νέο URL, π.χ. https://www.example.gr}"; NEW="${NEW%/}"
OLD="https://pangeo57-debug.github.io/pg-ai-solutions"
cd "$(dirname "$0")/.."
grep -rl --include='*.html' --include='*.xml' --include='*.txt' --include='*.md' "$OLD" . | grep -v '^./.git/' | xargs -r sed -i "s|$OLD|$NEW|g"
echo "OK: $OLD -> $NEW"
