#!/usr/bin/env python3
"""Χτίζει τις σελίδες του site (EN στη ρίζα, EL στο /el/) από ένα κοινό template.
Χρήση: python3 scripts/build.py   — αλλάζεις κείμενα εδώ, όχι στα .html."""
import json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://pangeo57-debug.github.io/pg-ai-solutions"
V = "3"
LOGO = open(os.path.join(ROOT, "logo/pg-mark.svg"), encoding="utf-8").read().replace(' role="img" aria-label="PG"', ' aria-hidden="true"').replace('id="pgr"', 'id="pgr-h"').replace("url(#pgr)", "url(#pgr-h)")
PAGES = ["index", "services", "work", "studio"]

PROJECTS = [
 dict(id="routepal", img="routepal", live="https://pangeo57-debug.github.io/routiq/routiq.html",
  en=dict(kind="Route optimization", name="RoutePal", status="Live",
   desc="Plans a whole week of appointments and visits: who, when and in what order, using real travel times. Underneath runs a multi-phase optimization engine for routing with time windows (VRPTW).",
   stats=[("9","optimization phases"),("175","automated tests"),("4","languages")],
   pts=["Weekly or single-day plans, built from each client's available slots and split shifts","Multi-phase engine: constraint backtracking, simulated annealing and large neighbourhood search (LNS)","Real distances and drive times (OSRM/HERE), with rush-hour traffic per appointment","Benchmarked on Solomon VRPTW instances against best published and exact (Held-Karp) optima","Group and paired visits, map with navigation, PDF export, installs on the phone"],
   tags=["VRPTW","Simulated annealing","LNS","PWA"]),
  el=dict(kind="Βελτιστοποίηση διαδρομών", name="RoutePal", status="Live",
   desc="Οργανώνει μια ολόκληρη εβδομάδα ραντεβού και επισκέψεων: ποιος, πότε, με ποια σειρά, με πραγματικούς χρόνους δρόμου. Από κάτω τρέχει μηχανή βελτιστοποίησης πολλών φάσεων για δρομολόγηση με χρονικά παράθυρα (VRPTW).",
   stats=[("9","φάσεις βελτιστοποίησης"),("175","αυτόματα τεστ"),("4","γλώσσες")],
   pts=["Εβδομαδιαίο πρόγραμμα ή μία μέρα, με βάση τα διαθέσιμα διαστήματα κάθε πελάτη και σπαστά ωράρια","Μηχανή πολλών φάσεων: backtracking αναζήτηση περιορισμών, simulated annealing και large neighborhood search (LNS)","Πραγματικές αποστάσεις και χρόνοι δρόμου (OSRM/HERE), με κίνηση ώρας αιχμής ανά ραντεβού","Μετρημένο στα VRPTW προβλήματα του Solomon απέναντι στις καλύτερες δημοσιευμένες λύσεις και σε ακριβή βέλτιστα (Held-Karp)","Ομαδικά ραντεβού και ζευγάρια, χάρτης με πλοήγηση, εξαγωγή PDF, εγκατάσταση στο κινητό"],
   tags=["VRPTW","Simulated annealing","LNS","PWA"])),
 dict(id="surplo", img="surplo", live=None,
  en=dict(kind="B2B marketplace", name="Surplo", status="In development · demo on request",
   desc="A marketplace where small businesses sell surplus and unsold stock to other businesses, with payment held in escrow until the goods arrive.",
   stats=[], pts=["Standing buy requests: the buyer says what they need, a seller fills it in one click","Offers and counter-offers, then escrow payment (card, Apple/Google Pay, PayPal, SEPA)","The seller is paid only when the buyer confirms delivery; disputes go to an admin","Business verification, reviews and an order flow with full history","Web app plus a native iOS app (Capacitor)"],
   tags=["Next.js","Stripe Connect","Postgres","iOS"]),
  el=dict(kind="Αγορά B2B", name="Surplo", status="Σε ανάπτυξη · demo κατόπιν αιτήματος",
   desc="Αγορά όπου μικρές επιχειρήσεις πουλάνε πλεονάζον και αδιάθετο απόθεμα σε άλλες επιχειρήσεις, με την πληρωμή σε escrow μέχρι να φτάσει το εμπόρευμα.",
   stats=[], pts=["Μόνιμα αιτήματα αγοράς: ο αγοραστής δηλώνει τι θέλει, ο πωλητής το καλύπτει με ένα κλικ","Προσφορές και αντιπροσφορές, μετά πληρωμή σε escrow (κάρτα, Apple/Google Pay, PayPal, SEPA)","Ο πωλητής πληρώνεται μόνο όταν ο αγοραστής επιβεβαιώσει την παραλαβή· οι διαφορές πάνε σε διαχειριστή","Επαλήθευση επιχειρήσεων, αξιολογήσεις και ροή παραγγελιών με πλήρες ιστορικό","Web εφαρμογή και native εφαρμογή iOS (Capacitor)"],
   tags=["Next.js","Stripe Connect","Postgres","iOS"])),
 dict(id="cashflow", img="cashflow", live=None,
  en=dict(kind="Mini app", name="Cash Flow", status="Private app · demo on request",
   desc="A personal finance app: income and expenses in two taps, clear statistics, and data that stays on the phone, even offline.",
   stats=[], pts=["Income and expenses in two taps, by category","Recurring payments, monthly goals and budgets","Statistics and smart insights","Works offline; data stays on the device, with a JSON backup","Optional sync through Supabase"],
   tags=["React","TypeScript","PWA"]),
  el=dict(kind="Mini app", name="Cash Flow", status="Ιδιωτική εφαρμογή · demo κατόπιν αιτήματος",
   desc="Εφαρμογή προσωπικών οικονομικών: έσοδα και έξοδα με δύο πατήματα, καθαρά στατιστικά και δεδομένα που μένουν στο κινητό, ακόμα και offline.",
   stats=[], pts=["Έσοδα και έξοδα με δύο πατήματα, ανά κατηγορία","Επαναλαμβανόμενες πληρωμές, μηνιαίοι στόχοι και budgets","Στατιστικά και έξυπνες παρατηρήσεις","Λειτουργεί offline· τα δεδομένα μένουν στη συσκευή, με αντίγραφο JSON","Προαιρετικός συγχρονισμός μέσω Supabase"],
   tags=["React","TypeScript","PWA"])),
 dict(id="cooking", img="cooking", live="https://cookingmadewithlove.netlify.app/",
  en=dict(kind="Website", name="Cooking Made with Love", status="Live",
   desc="A website for a home bakery that sells handmade bread and pastries at a farmers' market in Michigan.",
   stats=[], pts=["Product catalogue: breads, sweets and pastries","Market location with a Google Maps link","Share image for social media","Deploys automatically on every change (Netlify)"],
   tags=["HTML · CSS · JS","SEO","Netlify"]),
  el=dict(kind="Ιστοσελίδα", name="Cooking Made with Love", status="Live",
   desc="Ιστοσελίδα για οικιακό φούρνο που πουλάει χειροποίητο ψωμί και γλυκά σε λαϊκή αγορά στο Michigan.",
   stats=[], pts=["Κατάλογος προϊόντων: ψωμιά, γλυκά και αρτοσκευάσματα","Τοποθεσία της αγοράς με σύνδεσμο στο Google Maps","Εικόνα προεπισκόπησης για κοινοποίηση στα social","Ανεβαίνει αυτόματα σε κάθε αλλαγή (Netlify)"],
   tags=["HTML · CSS · JS","SEO","Netlify"])),
 dict(id="mathdecoded", img="mathdecoded", live="https://pangeo57-debug.github.io/mathdecoded/",
  en=dict(kind="Website + app", name="MathDecoded", status="Live",
   desc="A site for private maths tutoring (SAT and Greek national exams) with exercises, puzzles and quizzes, installable on the phone.",
   stats=[], pts=["Exercises, puzzles and quizzes that keep progress","Installs on the phone like an app (PWA)","Identity built on the existing Instagram","Privacy policy and terms of use pages"],
   tags=["PWA","HTML · CSS · JS","GitHub Pages"]),
  el=dict(kind="Ιστοσελίδα + εφαρμογή", name="MathDecoded", status="Live",
   desc="Σελίδα για ιδιαίτερα μαθήματα μαθηματικών (SAT και Πανελλήνιες) με ασκήσεις, γρίφους και quiz, που εγκαθίσταται στο κινητό.",
   stats=[], pts=["Ασκήσεις, γρίφοι και quiz που κρατούν την πρόοδο","Εγκαθίσταται στο κινητό σαν εφαρμογή (PWA)","Ταυτότητα βασισμένη στο υπάρχον Instagram","Σελίδες πολιτικής απορρήτου και όρων χρήσης"],
   tags=["PWA","HTML · CSS · JS","GitHub Pages"])),
]

T = {
 "en": dict(
  lang="en", locale="en_GB", other="el", other_label="ΕΛ",
  nav=dict(index="Home", services="Services", work="Work", studio="Studio", contact="Contact"),
  titles=dict(index="Websites, Mini Apps & Optimization Software in Patras | PG AI Solutions", services="Services | PG AI Solutions", work="Work | PG AI Solutions", studio="Studio & Process | PG AI Solutions"),
  descs=dict(index="Custom websites, mini apps and optimization software from a small studio in Patras, Greece.", services="Websites, custom mini apps and optimization software, built around how your business actually works.", work="RoutePal, Surplo, Cash Flow, Cooking Made with Love and MathDecoded: what we built and why.", studio="A studio in Patras that models the problem before writing code. How we work, in four steps."),
  skip="Skip to content",
  hero=dict(tag="Software studio · Patras", h1="It starts<br>as <em>code.</em>", sub="Websites, mini apps and optimization software for businesses that want tools built around how they actually work.", cta="Start a project", link="See our work", km="km", saved="shorter", aria="Animated example: code runs and draws the shortest route between stops"),
  svc_head=("What we do", "Three things, <em>done properly.</em>", "From a fast website to software that solves a hard scheduling problem."),
  svcs=[("Websites","Fast, custom websites that present the business properly and are easy to find on Google."),("Custom mini apps","Small, focused apps built around how one person or a team actually works."),("Software & optimization","Scheduling, routing and decision tools, built on the right algorithms.")],
  work_head=("Selected work", "Five projects. <em>One method.</em>", "Apps and websites in production and in development."),
  all_work="All projects",
  proc_head=("How we work", "A process built like <em>an optimization loop.</em>", "Each stage feeds the next and is checked against the real problem before we move on."),
  steps=[("Discover","Map the users, constraints, data and the actual goal, before any design or code."),("Architect","Design the data model, algorithm and interface together, so the build doesn't fight itself later."),("Build","Deliver in focused iterations, tested on real scenarios, not just the happy path."),("Launch & tune","Ship, watch real usage and keep improving. Software should get better after handover.")],
  services_intro=("Services","What we <em>build.</em>","Three kinds of work, one approach: understand the problem first, then build exactly what fits."),
  svc_detail=[
   ("Websites","Fast, custom websites that present the business properly and are easy to find on Google.",["Designed for your business, no templates","Fast on mobile, with clean SEO and structured data","Greek and English when you need both","Contact forms that land in your inbox","You own the domain, hosting and accounts"]),
   ("Custom mini apps","Small, focused apps built around how one person or a team actually works.",["Bookings, price calculators, menus, internal tools","Installs on the phone like an app (PWA)","Works offline where it matters","Data stays yours, with export and backup","Built to grow when the business does"]),
   ("Software & optimization","Scheduling, routing and decision tools, built on the right algorithms.",["Route and appointment planning with real travel times","Scheduling with constraints and time windows","Dashboards that turn numbers into decisions","Measured against known benchmarks, not guesses","Clear explanations of why the result is good"])],
  work_intro=("Work","Things we <em>built.</em>","Each project started as a real problem. Here is what it does and how."),
  live="Visit live site",
  studio_intro=("Studio","Software built to be <em>understood.</em>","PG AI Solutions is a studio in Patras, Greece. We model the problem properly before writing code, and build websites, apps and software that fit how our clients really work."),
  spec=[("Based in","Patras, Greece"),("Focus","Web development & applied optimization"),("Areas","Web · Dashboards · Optimization"),("Clients","Local & remote"),("Approach","Model first, then build")],
  contact=dict(eyebrow="Contact", h="Have something that needs <em>building?</em>", lead="Tell us the problem, not just the feature list. We'll find the right way to solve it.", phone="Phone", email="Email", where="Studio", where_v="Patras, Greece", reply="Reply", reply_v="Usually within one working day",
    who1="I have a project", who2="Let's collaborate", subj1="New project inquiry · PG AI Solutions", subj2="Collaboration inquiry · PG AI Solutions",
    name="Name", mail="Email", msg="Message", ph_msg="What are you trying to solve?", send="Send message",
    t=dict(sending="Sending…", sent="Sent ✓", send="Send message", thanks="Thank you. We will reply to your email soon.", fail="That did not go through. Please write to pangeo57@yahoo.gr.")),
  privacy="Privacy policy", privacy_href="privacy.html",
 ),
 "el": dict(
  lang="el", locale="el_GR", other="en", other_label="EN",
  nav=dict(index="Αρχική", services="Υπηρεσίες", work="Έργα", studio="Studio", contact="Επικοινωνία"),
  titles=dict(index="Ιστοσελίδες, Mini Apps & Λογισμικό Βελτιστοποίησης στην Πάτρα | PG AI Solutions", services="Υπηρεσίες | PG AI Solutions", work="Έργα | PG AI Solutions", studio="Studio & Διαδικασία | PG AI Solutions"),
  descs=dict(index="Custom ιστοσελίδες, mini apps και λογισμικό βελτιστοποίησης από ένα μικρό studio στην Πάτρα.", services="Ιστοσελίδες, custom mini apps και λογισμικό βελτιστοποίησης, φτιαγμένα γύρω από τον τρόπο που δουλεύει η επιχείρησή σας.", work="RoutePal, Surplo, Cash Flow, Cooking Made with Love και MathDecoded: τι φτιάξαμε και γιατί.", studio="Studio στην Πάτρα που μοντελοποιεί το πρόβλημα πριν γράψει κώδικα. Πώς δουλεύουμε, σε τέσσερα βήματα."),
  skip="Μετάβαση στο περιεχόμενο",
  hero=dict(tag="Studio λογισμικού · Πάτρα", h1="Ξεκινά<br>σαν <em>κώδικας.</em>", sub="Ιστοσελίδες, mini apps και λογισμικό βελτιστοποίησης για επιχειρήσεις που θέλουν εργαλεία φτιαγμένα για τον τρόπο που δουλεύουν.", cta="Ξεκινάμε", link="Δες τα έργα", km="km", saved="συντομότερη", aria="Κινούμενο παράδειγμα: ο κώδικας τρέχει και σχεδιάζει τη συντομότερη διαδρομή ανάμεσα σε στάσεις"),
  svc_head=("Τι κάνουμε", "Τρία πράγματα, <em>σωστά.</em>", "Από μια γρήγορη ιστοσελίδα μέχρι λογισμικό που λύνει ένα δύσκολο πρόβλημα προγραμματισμού."),
  svcs=[("Ιστοσελίδες","Γρήγορες, custom ιστοσελίδες που παρουσιάζουν σωστά την επιχείρηση και βρίσκονται εύκολα στο Google."),("Custom mini apps","Μικρές, στοχευμένες εφαρμογές φτιαγμένες γύρω από τον τρόπο που δουλεύει ένας άνθρωπος ή μια ομάδα."),("Λογισμικό & βελτιστοποίηση","Εργαλεία προγραμματισμού, δρομολόγησης και αποφάσεων, χτισμένα σε σωστούς αλγορίθμους.")],
  work_head=("Επιλεγμένα έργα", "Πέντε έργα. <em>Μία μέθοδος.</em>", "Εφαρμογές και ιστοσελίδες σε λειτουργία και σε ανάπτυξη."),
  all_work="Όλα τα έργα",
  proc_head=("Πώς δουλεύουμε", "Μια διαδικασία σαν <em>βρόχος βελτιστοποίησης.</em>", "Κάθε στάδιο τροφοδοτεί το επόμενο και ελέγχεται απέναντι στο πραγματικό πρόβλημα πριν προχωρήσουμε."),
  steps=[("Ανακάλυψη","Χαρτογραφούμε τους χρήστες, τους περιορισμούς, τα δεδομένα και τον πραγματικό στόχο, πριν από σχεδιασμό ή κώδικα."),("Αρχιτεκτονική","Σχεδιάζουμε μαζί το μοντέλο δεδομένων, τον αλγόριθμο και τη διεπαφή, ώστε η υλοποίηση να μην παλεύει με τον εαυτό της αργότερα."),("Υλοποίηση","Παραδίδουμε σε εστιασμένες επαναλήψεις, δοκιμάζοντας σε πραγματικά σενάρια, όχι μόνο στην ιδανική περίπτωση."),("Έναρξη & βελτίωση","Δημοσιεύουμε, παρακολουθούμε την πραγματική χρήση και βελτιώνουμε. Το λογισμικό πρέπει να βελτιώνεται και μετά την παράδοση.")],
  services_intro=("Υπηρεσίες","Τι <em>φτιάχνουμε.</em>","Τρία είδη δουλειάς, μία προσέγγιση: πρώτα καταλαβαίνουμε το πρόβλημα, μετά χτίζουμε ακριβώς αυτό που ταιριάζει."),
  svc_detail=[
   ("Ιστοσελίδες","Γρήγορες, custom ιστοσελίδες που παρουσιάζουν σωστά την επιχείρηση και βρίσκονται εύκολα στο Google.",["Σχεδιασμένες για την επιχείρησή σας, χωρίς έτοιμα templates","Γρήγορες στο κινητό, με σωστό SEO και δομημένα δεδομένα","Ελληνικά και αγγλικά όταν χρειάζονται και τα δύο","Φόρμες επικοινωνίας που φτάνουν στο email σας","Το domain, το hosting και οι λογαριασμοί είναι δικά σας"]),
   ("Custom mini apps","Μικρές, στοχευμένες εφαρμογές φτιαγμένες γύρω από τον τρόπο που δουλεύει ένας άνθρωπος ή μια ομάδα.",["Κρατήσεις, κοστολόγηση, μενού, εσωτερικά εργαλεία","Εγκαθίστανται στο κινητό σαν εφαρμογή (PWA)","Λειτουργούν offline όπου χρειάζεται","Τα δεδομένα μένουν δικά σας, με εξαγωγή και αντίγραφο","Φτιαγμένες για να μεγαλώνουν μαζί με την επιχείρηση"]),
   ("Λογισμικό & βελτιστοποίηση","Εργαλεία προγραμματισμού, δρομολόγησης και αποφάσεων, χτισμένα σε σωστούς αλγορίθμους.",["Σχεδιασμός διαδρομών και ραντεβού με πραγματικούς χρόνους δρόμου","Προγραμματισμός με περιορισμούς και χρονικά παράθυρα","Dashboards που κάνουν τους αριθμούς αποφάσεις","Μετρημένα απέναντι σε γνωστά benchmarks, όχι στο περίπου","Καθαρή εξήγηση για το γιατί το αποτέλεσμα είναι καλό"])],
  work_intro=("Έργα","Τι <em>φτιάξαμε.</em>","Κάθε έργο ξεκίνησε από ένα πραγματικό πρόβλημα. Εδώ είναι τι κάνει και πώς."),
  live="Δείτε το live",
  studio_intro=("Studio","Λογισμικό φτιαγμένο για να <em>γίνεται κατανοητό.</em>","Η PG AI Solutions είναι studio με έδρα την Πάτρα. Μοντελοποιούμε σωστά το πρόβλημα πριν γράψουμε κώδικα και φτιάχνουμε ιστοσελίδες, εφαρμογές και λογισμικό που ταιριάζουν στον τρόπο που δουλεύουν πραγματικά οι πελάτες μας."),
  spec=[("Έδρα","Πάτρα, Ελλάδα"),("Εστίαση","Ανάπτυξη web & εφαρμοσμένη βελτιστοποίηση"),("Τομείς","Web · Dashboards · Βελτιστοποίηση"),("Πελάτες","Τοπικοί & απομακρυσμένοι"),("Προσέγγιση","Πρώτα μοντελοποίηση, μετά υλοποίηση")],
  contact=dict(eyebrow="Επικοινωνία", h="Έχετε κάτι που θέλει <em>να χτιστεί;</em>", lead="Πείτε μας το πρόβλημα, όχι μόνο τη λίστα με τις λειτουργίες. Θα βρούμε τον σωστό τρόπο να το λύσουμε.", phone="Τηλέφωνο", email="Email", where="Studio", where_v="Πάτρα, Ελλάδα", reply="Απάντηση", reply_v="Συνήθως μέσα σε μία εργάσιμη",
    who1="Έχω ένα έργο", who2="Θέλω να συνεργαστούμε", subj1="Νέο αίτημα έργου · PG AI Solutions", subj2="Πρόταση συνεργασίας · PG AI Solutions",
    name="Όνομα", mail="Email", msg="Μήνυμα", ph_msg="Τι θέλετε να λύσουμε;", send="Αποστολή μηνύματος",
    t=dict(sending="Αποστολή…", sent="Εστάλη ✓", send="Αποστολή μηνύματος", thanks="Ευχαριστούμε. Θα σας απαντήσουμε σύντομα στο email σας.", fail="Η αποστολή δεν ολοκληρώθηκε. Γράψτε μας στο pangeo57@yahoo.gr.")),
  privacy="Πολιτική απορρήτου", privacy_href="privacy.html",
 ),
}

def fn(p): return "./" if p == "index" else f"{p}.html"
def url(lang, p):
    pre = BASE + ("/el/" if lang == "el" else "/")
    return pre if p == "index" else pre + f"{p}.html"

def head(L, p, pre):
    t = T[L]; title = t["titles"][p]; desc = t["descs"][p]
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{url(l,p)}">\n' for l in ("en","el")) + f'<link rel="alternate" hreflang="x-default" href="{url("en",p)}">\n'
    ld = ""
    if p == "index":
        ld = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"ProfessionalService","name":"PG AI Solutions","url":url(L,"index"),"logo":BASE+"/assets/logo-512.png","image":BASE+"/assets/og-image.png","telephone":"+306971919078","email":"pangeo57@yahoo.gr","address":{"@type":"PostalAddress","addressLocality":"Patras","addressCountry":"GR"},"areaServed":"GR"}, ensure_ascii=False) + '</script>\n'
    return f'''<!DOCTYPE html>
<html lang="{t["lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#ffffff">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url(L,p)}">
{alts}<meta property="og:type" content="website">
<meta property="og:site_name" content="PG AI Solutions">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url(L,p)}">
<meta property="og:image" content="{BASE}/assets/og-image.png">
<meta property="og:locale" content="{t["locale"]}">
<meta name="twitter:card" content="summary_large_image">
{ld}<link rel="icon" type="image/svg+xml" href="{pre}logo/pg-icon.svg">
<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="preload" href="{pre}assets/fonts/notodisplay-{"greek" if L=="el" else "latin"}-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/site.css?v={V}">
</head>
<body>
<a class="skip" href="#main">{t["skip"]}</a>
'''

def header(L, p, pre):
    t = T[L]; n = t["nav"]
    other_pre = "../" if L == "el" else "el/"
    other = other_pre + ("" if p == "index" else f"{p}.html")
    links = "".join(f'<a href="{fn(k)}"{" aria-current=\"page\"" if k==p else ""}{" class=\"hide-s\"" if k=="index" else ""}>{n[k]}</a>' for k in PAGES)
    return f'''<header class="hd"><div class="wrap">
<a class="logo" href="./" aria-label="PG AI Solutions">{LOGO}<span><b>PG AI</b> Solutions</span></a>
<nav class="nav" aria-label="Main">{links}<a href="#contact" class="hide-s">{n["contact"]}</a><a class="lang" href="{other}" hreflang="{t["other"]}" lang="{t["other"]}">{t["other_label"]}</a></nav>
</div></header>
'''

def sec_head(h, tag="h2"):
    e, title, lead = h
    return f'<div class="sec-head"><span class="eyebrow">{e}</span><{tag} class="h2">{title}</{tag}><p class="lead">{lead}</p></div>'

def intro(h):
    e, title, lead = h
    return f'<section class="intro"><div class="wrap"><span class="eyebrow">{e}</span><h1 class="h1">{title}</h1><p class="lead">{lead}</p></div></section>'

def strip(L, pre):
    out = []
    for pj in PROJECTS:
        d = pj[L]
        out.append(f'<a class="wcard" href="work.html#{pj["id"]}"><span class="shot"><img src="{pre}assets/work/{pj["img"]}.webp" width="480" height="1038" alt="" loading="lazy" decoding="async"></span><small>{d["kind"]}</small><b>{d["name"]}</b></a>')
    return '<div class="strip">' + "".join(out) + "</div>"

def steps(L):
    return '<div class="steps">' + "".join(f'<div class="step"><span class="n">0{i+1}</span><h3 class="h3">{a}</h3><p>{b}</p></div>' for i,(a,b) in enumerate(T[L]["steps"])) + "</div>"

def page_index(L, pre):
    t = T[L]; h = t["hero"]
    rows = "".join(f'<a class="row" href="services.html#s{i+1}"><span class="n">0{i+1}</span><h3 class="h3">{a}</h3><p>{b}</p><span class="go" aria-hidden="true">→</span></a>' for i,(a,b) in enumerate(t["svcs"]))
    return f'''<section class="hero" aria-labelledby="hero-h"><canvas role="img" aria-label="{h["aria"]}"></canvas>
<div class="wrap"><pre aria-hidden="true"></pre><div class="hero-txt"><span class="eyebrow">{h["tag"]}</span><h1 class="h1" id="hero-h">{h["h1"]}</h1><p class="lead">{h["sub"]}</p>
<div class="hero-act"><a class="txtlink" href="work.html">{h["link"]}</a><a class="btn line" href="#contact">{h["cta"]} <i aria-hidden="true">→</i></a></div>
<div class="meta" aria-hidden="true"><span><b data-km>0.0</b> {h["km"]}</span><span><b data-gain>…</b> {h["saved"]}</span></div></div></div></section>
<section class="sec"><div class="wrap">{sec_head(t["svc_head"])}<div class="rows">{rows}</div></div></section>
<section class="sec alt"><div class="wrap">{sec_head(t["work_head"])}{strip(L, pre)}<p style="margin-top:32px"><a class="btn line" href="work.html">{t["all_work"]} <i aria-hidden="true">→</i></a></p></div></section>
<section class="sec"><div class="wrap">{sec_head(t["proc_head"])}{steps(L)}</div></section>
'''

def page_services(L, pre):
    t = T[L]; out = []
    for i,(a,b,lst) in enumerate(t["svc_detail"]):
        li = "".join(f"<li>{x}</li>" for x in lst)
        out.append(f'<div class="svc" id="s{i+1}"><span class="n">0{i+1}</span><div class="body"><h2 class="h2">{a}</h2><p class="lead">{b}</p></div><ul class="plist">{li}</ul></div>')
    return intro(t["services_intro"]) + f'<section class="sec" style="padding-top:0"><div class="wrap">{"".join(out)}</div></section><section class="sec alt"><div class="wrap">{sec_head(t["proc_head"])}{steps(L)}</div></section>'

def page_work(L, pre):
    t = T[L]; out = []
    for pj in PROJECTS:
        d = pj[L]
        live = f'<p><a class="btn line" href="{pj["live"]}" target="_blank" rel="noopener">{t["live"]} <i aria-hidden="true">↗</i></a></p>' if pj["live"] else ""
        st = ('<div class="stats">' + "".join(f'<div><b>{a}</b><span>{b}</span></div>' for a,b in d["stats"]) + '</div>') if d["stats"] else ""
        li = "".join(f"<li>{x}</li>" for x in d["pts"]); tg = "".join(f"<span>{x}</span>" for x in d["tags"])
        cls = "status live" if d["status"] == "Live" else "status"
        out.append(f'''<article class="proj" id="{pj["id"]}"><div class="pshot"><img src="{pre}assets/work/{pj["img"]}.webp" width="480" height="1038" alt="{d["name"]}" loading="lazy" decoding="async"></div>
<div class="pbody"><span class="eyebrow">{d["kind"]}</span><h2 class="h2">{d["name"]}</h2><span class="{cls}">{d["status"]}</span><p class="lead">{d["desc"]}</p>{st}<ul class="plist">{li}</ul><div class="tags">{tg}</div>{live}</div></article>''')
    return intro(t["work_intro"]) + f'<section><div class="wrap">{"".join(out)}</div></section>'

def page_studio(L, pre):
    t = T[L]
    spec = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a,b in t["spec"])
    return intro(t["studio_intro"]) + f'<section class="sec"><div class="wrap"><dl class="spec">{spec}</dl></div></section><section class="sec alt"><div class="wrap">{sec_head(t["proc_head"])}{steps(L)}</div></section>'

def contact(L):
    c = T[L]["contact"]
    tj = html.escape(json.dumps(c["t"], ensure_ascii=False), quote=True)
    return f'''<section class="contact" id="contact" aria-labelledby="c-h"><div class="wrap">
<div class="cinfo"><span class="eyebrow">{c["eyebrow"]}</span><h2 class="h2" id="c-h">{c["h"]}</h2><p class="lead">{c["lead"]}</p>
<dl><div><dt>{c["phone"]}</dt><dd><a href="tel:+306971919078">+30 697 191 9078</a></dd></div><div><dt>{c["email"]}</dt><dd><a href="mailto:pangeo57@yahoo.gr">pangeo57@yahoo.gr</a></dd></div><div><dt>{c["where"]}</dt><dd>{c["where_v"]}</dd></div><div><dt>{c["reply"]}</dt><dd>{c["reply_v"]}</dd></div></dl></div>
<form class="cf" action="https://formsubmit.co/pangeo57@yahoo.gr" method="POST" data-t="{tj}">
<input type="hidden" name="_subject" value="{c["subj1"]}"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">
<input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<fieldset class="who"><legend class="hp">{c["who1"]} / {c["who2"]}</legend><label><input type="radio" name="Interest" value="Project" data-subj="{c["subj1"]}" checked><span>{c["who1"]}</span></label><label><input type="radio" name="Interest" value="Collaboration" data-subj="{c["subj2"]}"><span>{c["who2"]}</span></label></fieldset>
<div class="f2"><div class="fld"><label for="f-name">{c["name"]}</label><input id="f-name" name="Name" autocomplete="name" required></div><div class="fld"><label for="f-mail">{c["mail"]}</label><input id="f-mail" type="email" name="Email" autocomplete="email" required></div></div>
<div class="fld"><label for="f-msg">{c["msg"]}</label><textarea id="f-msg" name="Message" placeholder="{c["ph_msg"]}" required></textarea></div>
<button class="btn" type="submit"><span>{c["send"]}</span> <i aria-hidden="true">→</i></button><p class="note" role="status" aria-live="polite"></p>
</form></div></section>
'''

def footer(L, pre):
    t = T[L]; n = t["nav"]
    links = "".join(f'<a href="{fn(k)}">{n[k]}</a>' for k in PAGES[1:])
    return f'''<footer class="ft"><div class="wrap"><span>© 2026 PG AI Solutions · {T[L]["contact"]["where_v"]}</span><nav aria-label="Footer">{links}<a href="{t["privacy_href"]}">{t["privacy"]}</a></nav></div></footer>
<script src="{pre}assets/site.js?v={V}" defer></script>
</body>
</html>
'''

BUILD = dict(index=page_index, services=page_services, work=page_work, studio=page_studio)
for L in ("en", "el"):
    pre = "../" if L == "el" else ""
    for p in PAGES:
        body = head(L, p, pre) + header(L, p, pre) + '<main id="main">\n' + BUILD[p](L, pre) + '\n</main>\n' + contact(L) + footer(L, pre)
        path = os.path.join(ROOT, "el" if L == "el" else "", "index.html" if p == "index" else f"{p}.html")
        open(path, "w", encoding="utf-8").write(body)
        print("wrote", os.path.relpath(path, ROOT))

# sitemap
urls = []
for p in PAGES + ["privacy"]:
    for L in ("en","el"):
        loc = url(L,p) if p != "privacy" else BASE + ("/el/" if L=="el" else "/") + "privacy.html"
        alt = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{(url(l,p) if p!="privacy" else BASE+("/el/" if l=="el" else "/")+"privacy.html")}"/>' for l in ("en","el"))
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-10-31</lastmod>{alt}\n  </url>")
open(os.path.join(ROOT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
print("wrote sitemap.xml")
