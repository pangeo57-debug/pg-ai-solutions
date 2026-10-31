# PG AI Solutions — Οδηγός παράδοσης

## Τι περιέχει
- Πολυσέλιδο site: `index`, `services`, `work`, `studio` (EN στη ρίζα, ΕΛ στο `el/`), `privacy.html`, `el/privacy.html`, `404.html`
- Κοινά αρχεία: `assets/site.css`, `assets/site.js`, `logo/pg-mark.svg` (έμβλημα PG), `logo/pg-icon.svg` (favicon)
- `robots.txt`, `sitemap.xml`, `assets/` (γραμματοσειρές OFL, εικόνες έργων και κοινοποίησης)
- Δεν φορτώνεται τίποτα από τρίτους στη φόρτωση σελίδας (χωρίς cookies/analytics). Μόνο η αποστολή φόρμας πηγαίνει στο formsubmit.co.

## Αλλαγή κειμένων
Όλα τα κείμενα (και στις δύο γλώσσες) και τα έργα είναι στο `scripts/build.py`. Αλλάζεις εκεί και τρέχεις `python3 scripts/build.py`· ξαναγράφει όλες τις σελίδες και το `sitemap.xml`. Μην αλλάζεις τα .html με το χέρι.

## Domain (ΠΡΟΣΟΧΗ: τα robots/sitemap δουλεύουν σωστά μόνο σε domain root)
1. Αγορά domain (π.χ. .gr). 2. `scripts/set-domain.sh https://www.to-domain.gr` 3. Αρχείο `CNAME` με το domain στη ρίζα και ρύθμιση DNS όπως ζητά το hosting.

## Hosting
GitHub Pages: Settings → Pages → Deploy from branch `main` / root. Εναλλακτικά Netlify/Cloudflare Pages (drag & drop του φακέλου).

## Φόρμα επικοινωνίας
Την πρώτη φορά το formsubmit.co στέλνει email ενεργοποίησης στο pangeo57@yahoo.gr — στείλε ένα δοκιμαστικό μήνυμα και επιβεβαίωσε (έλεγξε και τα spam).

## Google
1. Search Console → προσθήκη ιδιοκτησίας (domain) → επαλήθευση DNS.
2. Sitemaps → υποβολή `sitemap.xml`. 3. «Έλεγχος URL» → «Αίτημα indexing» για `/` και `/el/`.
4. Δημιουργία Google Business Profile (Πάτρα) — σημαντικό για τοπική αναζήτηση.
Ρεαλιστικά: ευρετηρίαση σε μέρες–εβδομάδες· καλή θέση σε ανταγωνιστικές αναζητήσεις θέλει χρόνο, περιεχόμενο και σύνδεσμοι.

## Πολιτική απορρήτου — να επιβεβαιωθούν από τον ιδιοκτήτη
- Πλήρη νομικά στοιχεία υπευθύνου (επωνυμία/όνομα, ΑΦΜ, διεύθυνση).
- Χρόνος διατήρησης (προτείνεται 12 μήνες αν δεν υπάρξει συνεργασία).
- Αν προστεθούν analytics/cookies, χρειάζεται ενημέρωση και banner συναίνεσης.
Δεν αποτελεί νομική συμβουλή· προτείνεται έλεγχος από νομικό.

## Ιδιοκτησία
Domain, hosting και λογαριασμός Search Console να είναι στο όνομα του πελάτη.
