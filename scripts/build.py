#!/usr/bin/env python3
"""Χτίζει τις σελίδες του site (EN στη ρίζα, EL στο /el/) από ένα κοινό template.
Χρήση: python3 scripts/build.py   — αλλάζεις κείμενα εδώ, όχι στα .html."""
import json, os, html, re, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://pangeo57-debug.github.io/pg-ai-solutions"
V = "20"
GA4_ID = os.environ.get("PG_GA4_ID") or os.environ.get("GA4_MEASUREMENT_ID") or ""
TODAY = datetime.date.today().isoformat()
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
  en=dict(kind="Finance app", name="Cash Flow", status="Private app · demo on request",
   desc="A personal finance app: income and expenses in two taps, clear statistics, and data that stays on the phone, even offline.",
   stats=[], pts=["Income and expenses in two taps, by category","Recurring payments, monthly goals and budgets","Statistics and smart insights","Works offline; data stays on the device, with a JSON backup","Optional sync through Supabase"],
   tags=["React","TypeScript","PWA"]),
  el=dict(kind="Εφαρμογή οικονομικών", name="Cash Flow", status="Ιδιωτική εφαρμογή · demo κατόπιν αιτήματος",
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
 dict(id="pgai", img="pgai", live="https://pangeo57-debug.github.io/pg-ai-solutions/",
  en=dict(kind="Website + brand", name="PG AI Solutions", status="Live",
   desc="Our own studio site and identity: a bilingual, multi-page website with a live route-optimization hero, built and branded in-house.",
   stats=[], pts=["Brand identity: PG route monogram, palette and typography","Bilingual (Greek / English), multi-page, SEO-ready","Animated hero that runs a real route optimization","Self-hosted fonts, no trackers, fast on mobile"],
   tags=["Branding","HTML · CSS · JS","SEO","GitHub Pages"]),
  el=dict(kind="Ιστοσελίδα + brand", name="PG AI Solutions", status="Live",
   desc="Το δικό μας site και η ταυτότητα του studio: δίγλωσση, πολυσέλιδη ιστοσελίδα με hero που τρέχει πραγματική βελτιστοποίηση διαδρομής.",
   stats=[], pts=["Ταυτότητα: μονόγραμμα PG σαν διαδρομή, παλέτα και τυπογραφία","Δίγλωσσο (ελληνικά / αγγλικά), πολυσέλιδο, έτοιμο για SEO","Hero που τρέχει πραγματική βελτιστοποίηση διαδρομής","Γραμματοσειρές στον δικό μας server, χωρίς trackers, γρήγορο στο κινητό"],
   tags=["Branding","HTML · CSS · JS","SEO","GitHub Pages"])),
]

T = {
 "en": dict(
  lang="en", locale="en_GB", theme="Switch light / dark theme", other="el", other_label="ΕΛ",
  nav=dict(index="Home", services="Services", work="Work", studio="Studio", contact="Contact"),
  titles=dict(index="Web Design & App Development in Patras, Greece | PG AI Solutions", services="Websites, Business Apps & Optimization Software | PG AI Solutions", work="Our Work: Websites, Apps & Route Optimization | PG AI Solutions", studio="Software Studio in Patras, Greece | PG AI Solutions", privacy="Privacy Policy | PG AI Solutions", terms="Terms of Use | PG AI Solutions"),
  descs=dict(index="Software studio in Patras, Greece. We design and build websites, business apps and optimization software for small businesses. Reply within one working day.", services="Website design with SEO, booking and ordering apps, and scheduling and route optimization software, built around how your business actually works.", work="Websites and apps we have built: RoutePal route optimization, the Surplo B2B marketplace, Cash Flow, Cooking Made with Love and MathDecoded.", studio="PG AI Solutions is a software studio in Patras, Greece. We model the problem before writing code. How we work, in four steps.", privacy="How the PG AI Solutions website handles personal data: what we collect, why, who receives it, how long we keep it and your rights.", terms="Terms of use for the PG AI Solutions website."),
  crumb="Home", og_alt="PG AI Solutions: websites, apps and optimization software from Patras, Greece",
  faq_head=("Questions", "Common <em>questions.</em>", "Short answers to what businesses ask us first."),
  faq=[("How much does a website or an app cost?","The price comes from what the project needs, not the other way around. After a first conversation we send a written proposal with clear scope, timeline and cost, so there are no surprises later."),
       ("How quickly do you reply?","Within one working day, with clear next steps and, when it fits, a proposal."),
       ("Do you work with businesses outside Patras?","Yes. We are based in Patras, Greece, and work with both local and remote clients, in Greek and English."),
       ("Who owns the website, the domain and the data?","You do. The domain and the accounts are yours, and your data stays yours, with export and backup."),
       ("Can the app be installed on a phone?","Yes. Our apps install on the phone like a native app (PWA) and work offline where it matters."),
       ("Do you handle SEO, hosting and maintenance?","Yes. Websites include a technical SEO audit, Google Business Profile, structured data and Search Console, plus hosting, backups, updates and monthly reporting.")],
  skip="Skip to content",
  hero=dict(tag="Websites, apps & software · Patras", h1=[("From chaos,",0),("the optimal",1),("solution.",1)], sub="We build websites, apps and optimization software for small businesses, with AI and algorithms in our work from day one.", cta="Start a conversation", link="View our work", aria="Animation: a real route optimizer arranges scattered stops into the PG monogram, then into the shortest route of a working day", hud=("stops","iterations","route"), proof=[("3","services"),("1","working day to reply"),("584","automated quality checks"),("4","languages in our apps")]),
  ask=dict(eyebrow="Tell us what you need", h="One sentence. <em>A clear plan.</em>", lead="Write it the way you would say it to a colleague. Within one working day you have a reply with the next steps.", note="Example plan for a project like this", q="I need a booking app that also builds the week's schedule by itself", chips=["Booking app","Bilingual website","Shift scheduling","Delivery routes"], plan=[("Week 1","we learn how you work today"),("Weeks 2–4","we build the app and the automatic schedule"),("Week 5","testing with your own data, then handover")], cta="Describe your project"),
  svc_head=("What we do", "Three services. <em>One standard of work.</em>", "Every project is designed for your business from scratch, with no off-the-shelf templates."),
  svcs=[("Website design & development","Websites built for your business, fast on a phone and set up properly for Google. Hosting and maintenance included."),("Business app development","Apps for bookings, orders and the daily work of the office, which also open on a phone."),("Optimization software","Appointment schedules, shifts and delivery routes that plan themselves, using algorithms measured on known benchmark problems.")],
  work_head=("Selected work", "Work we have <em>delivered.</em>", "Apps and websites we designed and built. Some are live, others are in development."),
  all_work="View more work",
  proc_head=("How we work", "Four steps, <em>each one checked.</em>", "Before we move to the next step, we check that the previous one solves your real problem."),
  steps=[("Understand","We learn who will use it, what limits you have and what the real goal is, before any design or code."),("Design","We design the data, the logic and the screens together, so no expensive changes are needed later."),("Build","We deliver in small pieces and test with real scenarios, not only the ideal case."),("Launch & improve","We put it live, watch how it is used and keep improving it. The work does not stop at handover.")],
  services_intro=("Services","What we <em>build.</em>","We take on a few projects at a time, so each one has our attention from the first conversation to launch and after."),
  svc_detail=[
   ("Website design & development","Websites built for your business and set up properly for Google, with hosting and maintenance included.",["Designed for your business, no off-the-shelf templates","Fast on every device, built to bring you enquiries","SEO: technical audit, Google Business Profile, structured data, Search Console","Branding: logo, palette and typography when you need them","Hosting, backups, updates and monthly reporting","Greek and English when you need both; you own the domain and accounts"]),
   ("Business app development","Apps built around the way your business works, from bookings to the tools your team uses every day.",["Booking systems, quoting, ordering and internal tools","Installs on the phone like an app (PWA)","Works offline where it matters","Your data stays yours, with export and backup","Built to grow with the business"]),
   ("Optimization software","Software that plans appointments, shifts and routes for you, using proven algorithms measured against known benchmarks.",["Route and appointment planning with real travel times","Scheduling with constraints and time windows","Dashboards that show you what to decide, not just numbers","Measured against known benchmarks, not guesses","Clear explanations of why the result is good"])],
  work_intro=("Work","What we have <em>built.</em>","Every project started from a real problem a business had. See what we delivered and how it works."),
  live="Visit live site",
  studio_intro=("Studio","First we understand, <em>then we write code.</em>","PG AI Solutions is a software studio based in Patras, Greece. We build websites, apps and optimization software that fit the way each business really works."),
  spec=[("Based in","Patras, Greece"),("What we build","Websites, apps, optimization software"),("Languages","Greek & English"),("Clients","In Patras and remote"),("Approach","Understand first, then build")],
  contact=dict(eyebrow="Contact", h="Tell us about <em>your project.</em>", lead="Write to us with what you want to achieve. We reply within one working day with the next steps and, when it fits, a proposal.", phone="Phone", email="Email", where="Studio", where_v="Patras, Greece", reply="Reply", reply_v="Within one working day",
    consent='By sending this form you agree to our <a href="privacy.html">privacy policy</a>.', who1="New project", who2="Partnership", subj1="New project inquiry · PG AI Solutions", subj2="Collaboration inquiry · PG AI Solutions",
    name="Name", mail="Email", msg="Message", ph_msg="What do you need, in a few words?", send="Send message",
    t=dict(sending="Sending…", sent="Sent ✓", send="Send message", thanks="Thank you. We will reply to your email soon.", fail="The message could not be sent. Please email pangeo57@yahoo.gr or call +30 697 191 9078.")),
  band=("A few projects at a time","We work with <em>a few clients</em> at once.","That way every project has our attention from the first meeting to delivery. Tell us about yours.","Book a meeting"),
  start_head=("How we start", "From first call <em>to proposal.</em>", "First we understand your business. The price comes from what the project needs, not the other way around."),
  start=[("Conversation","A call or a meeting to understand what you want to achieve and who will use it."),("Proposal","A written proposal with what the project includes, the timeline and the cost. No surprises later."),("Delivery","Design and build in stages, with a working version in your hands early.")],
  budget=dict(label="Budget", opts=["Not sure yet","€2,000 – €5,000","€5,000 – €15,000","€15,000+"]),
  privacy="Privacy policy", privacy_href="privacy.html",
 ),
 "el": dict(
  lang="el", locale="el_GR", theme="Εναλλαγή ανοιχτού / σκούρου θέματος", other="en", other_label="EN",
  nav=dict(index="Αρχική", services="Υπηρεσίες", work="Έργα", studio="Studio", contact="Επικοινωνία"),
  titles=dict(index="Κατασκευή Ιστοσελίδων & Εφαρμογών στην Πάτρα | PG AI Solutions", services="Κατασκευή Ιστοσελίδων, Εφαρμογές & Λογισμικό | PG AI Solutions", work="Έργα: Ιστοσελίδες & Εφαρμογές που Φτιάξαμε | PG AI Solutions", studio="Studio Ανάπτυξης Λογισμικού στην Πάτρα | PG AI Solutions", privacy="Πολιτική Απορρήτου | PG AI Solutions", terms="Όροι Χρήσης | PG AI Solutions"),
  descs=dict(index="Studio λογισμικού στην Πάτρα. Κατασκευή ιστοσελίδων, ανάπτυξη εφαρμογών και λογισμικό βελτιστοποίησης για μικρές επιχειρήσεις. Απάντηση σε μία εργάσιμη.", services="Κατασκευή ιστοσελίδων με SEO, εφαρμογές κρατήσεων και παραγγελιών, λογισμικό για πρόγραμμα και δρομολόγια, φτιαγμένα γύρω από την επιχείρησή σας.", work="Ιστοσελίδες και εφαρμογές που φτιάξαμε: RoutePal για βελτιστοποίηση διαδρομών, η αγορά B2B Surplo, Cash Flow, Cooking Made with Love και MathDecoded.", studio="Η PG AI Solutions είναι studio ανάπτυξης λογισμικού στην Πάτρα. Μοντελοποιούμε το πρόβλημα πριν γράψουμε κώδικα. Πώς δουλεύουμε, σε τέσσερα βήματα.", privacy="Πώς ο ιστότοπος της PG AI Solutions διαχειρίζεται προσωπικά δεδομένα: τι συλλέγουμε, γιατί, ποιος τα λαμβάνει, για πόσο τα κρατάμε και τα δικαιώματά σας.", terms="Όροι χρήσης του ιστότοπου της PG AI Solutions."),
  crumb="Αρχική", og_alt="PG AI Solutions: ιστοσελίδες, εφαρμογές και λογισμικό βελτιστοποίησης από την Πάτρα",
  faq_head=("Ερωτήσεις", "Συχνές <em>ερωτήσεις.</em>", "Σύντομες απαντήσεις σε όσα μας ρωτούν πρώτα οι επιχειρήσεις."),
  faq=[("Πόσο κοστίζει η κατασκευή ιστοσελίδας ή εφαρμογής;","Η τιμή βγαίνει από το τι χρειάζεται το έργο, όχι το αντίστροφο. Μετά την πρώτη κουβέντα στέλνουμε γραπτή πρόταση με το τι περιλαμβάνει, το χρονοδιάγραμμα και το κόστος, χωρίς εκπλήξεις αργότερα."),
       ("Σε πόσο χρόνο απαντάτε;","Μέσα σε μία εργάσιμη, με σαφή επόμενα βήματα και, όπου ταιριάζει, πρόταση συνεργασίας."),
       ("Δουλεύετε με επιχειρήσεις εκτός Πάτρας;","Ναι. Η έδρα μας είναι στην Πάτρα και δουλεύουμε με τοπικούς και απομακρυσμένους πελάτες, στα ελληνικά και στα αγγλικά."),
       ("Σε ποιον ανήκουν η ιστοσελίδα, το domain και τα δεδομένα;","Σε εσάς. Το domain και οι λογαριασμοί είναι δικά σας, και τα δεδομένα μένουν δικά σας, με εξαγωγή και αντίγραφο."),
       ("Μπορεί η εφαρμογή να εγκατασταθεί στο κινητό;","Ναι. Οι εφαρμογές μας εγκαθίστανται στο κινητό σαν εφαρμογή (PWA) και λειτουργούν offline όπου χρειάζεται."),
       ("Αναλαμβάνετε SEO, φιλοξενία και συντήρηση;","Ναι. Οι ιστοσελίδες περιλαμβάνουν τεχνικό έλεγχο SEO, Google Business Profile, δομημένα δεδομένα και Search Console, μαζί με φιλοξενία, αντίγραφα, ενημερώσεις και μηνιαία αναφορά.")],
  skip="Μετάβαση στο περιεχόμενο",
  hero=dict(tag="Ιστοσελίδες, εφαρμογές & λογισμικό · Πάτρα", h1=[("Από το χάος,",0),("η βέλτιστη",1),("λύση.",1)], sub="Φτιάχνουμε ιστοσελίδες, εφαρμογές και λογισμικό βελτιστοποίησης για μικρές επιχειρήσεις, με AI και αλγορίθμους στη δουλειά μας από την πρώτη μέρα.", cta="Ξεκινήστε μια συζήτηση", link="Δείτε τα έργα μας", aria="Κινούμενη εικόνα: ένας πραγματικός αλγόριθμος βελτιστοποίησης τακτοποιεί σκόρπιες στάσεις στο μονόγραμμα PG και μετά στη συντομότερη διαδρομή μιας εργάσιμης μέρας", hud=("στάσεις","επαναλήψεις","διαδρομή"), proof=[("3","υπηρεσίες"),("1","εργάσιμη για να απαντήσουμε"),("584","αυτόματοι έλεγχοι ποιότητας"),("4","γλώσσες στις εφαρμογές μας")]),
  ask=dict(eyebrow="Πείτε μας τι χρειάζεστε", h="Μια πρόταση. <em>Ένα καθαρό πλάνο.</em>", lead="Γράψτε το όπως θα το λέγατε σε έναν συνεργάτη. Μέσα σε μία εργάσιμη έχετε απάντηση με τα επόμενα βήματα.", note="Ενδεικτικό πλάνο για ένα τέτοιο έργο", q="Θέλω εφαρμογή για ραντεβού που βγάζει μόνη της το πρόγραμμα της εβδομάδας", chips=["Εφαρμογή κρατήσεων","Δίγλωσση ιστοσελίδα","Πρόγραμμα βαρδιών","Δρομολόγια"], plan=[("Εβδ. 1","μαθαίνουμε πώς δουλεύετε σήμερα"),("Εβδ. 2–4","φτιάχνουμε την εφαρμογή και το αυτόματο πρόγραμμα"),("Εβδ. 5","δοκιμή με τα δικά σας δεδομένα και παράδοση")], cta="Περιγράψτε το έργο σας"),
  svc_head=("Τι κάνουμε", "Τρεις υπηρεσίες. <em>Ένα επίπεδο δουλειάς.</em>", "Κάθε έργο σχεδιάζεται για τη δική σας επιχείρηση από την αρχή, χωρίς έτοιμα templates."),
  svcs=[("Κατασκευή ιστοσελίδων","Ιστοσελίδες φτιαγμένες για την επιχείρησή σας, γρήγορες στο κινητό και στημένες σωστά για το Google. Με φιλοξενία και συντήρηση."),("Ανάπτυξη εφαρμογών","Εφαρμογές για κρατήσεις, παραγγελίες και την καθημερινή δουλειά του γραφείου, που ανοίγουν και στο κινητό."),("Λογισμικό βελτιστοποίησης","Πρόγραμμα ραντεβού, βάρδιες και δρομολόγια που βγαίνουν αυτόματα, με αλγορίθμους μετρημένους σε γνωστά προβλήματα.")],
  work_head=("Επιλεγμένα έργα", "Δουλειές που <em>έχουμε παραδώσει.</em>", "Εφαρμογές και ιστοσελίδες που σχεδιάσαμε και φτιάξαμε. Άλλες είναι σε λειτουργία, άλλες σε ανάπτυξη."),
  all_work="Δείτε περισσότερα",
  proc_head=("Πώς δουλεύουμε", "Τέσσερα βήματα, <em>με έλεγχο σε καθένα.</em>", "Πριν προχωρήσουμε στο επόμενο βήμα, ελέγχουμε ότι το προηγούμενο λύνει το πραγματικό σας πρόβλημα."),
  steps=[("Κατανόηση","Μαθαίνουμε ποιοι θα το χρησιμοποιούν, τι περιορισμούς έχετε και ποιος είναι ο πραγματικός στόχος, πριν από σχέδιο ή κώδικα."),("Σχεδιασμός","Σχεδιάζουμε μαζί τα δεδομένα, τη λογική και τις οθόνες, ώστε να μη χρειαστούν ακριβές αλλαγές αργότερα."),("Υλοποίηση","Παραδίδουμε σε μικρά κομμάτια και δοκιμάζουμε με πραγματικά σενάρια, όχι μόνο με την ιδανική περίπτωση."),("Παράδοση & βελτίωση","Το βγάζουμε στον αέρα, βλέπουμε πώς χρησιμοποιείται και το βελτιώνουμε. Η δουλειά δεν σταματά στην παράδοση.")],
  services_intro=("Υπηρεσίες","Τι <em>φτιάχνουμε.</em>","Αναλαμβάνουμε λίγα έργα κάθε φορά, ώστε το καθένα να έχει την προσοχή μας από την πρώτη κουβέντα μέχρι την παράδοση και μετά."),
  svc_detail=[
   ("Κατασκευή ιστοσελίδων","Ιστοσελίδες φτιαγμένες για την επιχείρησή σας και στημένες σωστά για το Google, με φιλοξενία και συντήρηση.",["Σχεδιασμένες για το brand σας, χωρίς έτοιμα templates","Γρήγορες σε κάθε συσκευή, φτιαγμένες να φέρνουν επαφές","SEO: τεχνικός έλεγχος, Google Business Profile, δομημένα δεδομένα, Search Console","Branding: λογότυπο, παλέτα και τυπογραφία όταν χρειάζονται","Φιλοξενία, αντίγραφα, ενημερώσεις και μηνιαία αναφορά","Ελληνικά και αγγλικά όταν χρειάζονται· το domain και οι λογαριασμοί είναι δικά σας"]),
   ("Ανάπτυξη εφαρμογών","Εφαρμογές φτιαγμένες γύρω από τον τρόπο που δουλεύει η επιχείρησή σας, από κρατήσεις μέχρι τα εργαλεία που χρησιμοποιεί κάθε μέρα η ομάδα σας.",["Συστήματα κρατήσεων, προσφορές, παραγγελίες και εσωτερικά εργαλεία","Εγκαθίστανται στο κινητό σαν εφαρμογή (PWA)","Λειτουργούν offline όπου χρειάζεται","Τα δεδομένα μένουν δικά σας, με εξαγωγή και αντίγραφο","Φτιαγμένες για να μεγαλώνουν μαζί με την επιχείρηση"]),
   ("Λογισμικό βελτιστοποίησης","Λογισμικό που βγάζει για εσάς το πρόγραμμα ραντεβού, τις βάρδιες και τα δρομολόγια, με δοκιμασμένους αλγορίθμους μετρημένους σε γνωστά προβλήματα.",["Σχεδιασμός διαδρομών και ραντεβού με πραγματικούς χρόνους δρόμου","Προγραμματισμός με περιορισμούς και χρονικά παράθυρα","Dashboards που σας δείχνουν τι να αποφασίσετε, όχι μόνο αριθμούς","Μετρημένα απέναντι σε γνωστά benchmarks, όχι στο περίπου","Καθαρή εξήγηση για το γιατί το αποτέλεσμα είναι καλό"])],
  work_intro=("Έργα","Τι έχουμε <em>φτιάξει.</em>","Κάθε έργο ξεκίνησε από ένα πραγματικό πρόβλημα μιας επιχείρησης. Δείτε τι παραδώσαμε και πώς δουλεύει."),
  live="Δείτε το live",
  studio_intro=("Studio","Πρώτα καταλαβαίνουμε, <em>μετά γράφουμε κώδικα.</em>","Η PG AI Solutions είναι studio λογισμικού με έδρα την Πάτρα. Φτιάχνουμε ιστοσελίδες, εφαρμογές και λογισμικό βελτιστοποίησης που ταιριάζουν στον τρόπο που δουλεύει πραγματικά κάθε επιχείρηση."),
  spec=[("Έδρα","Πάτρα, Ελλάδα"),("Τι φτιάχνουμε","Ιστοσελίδες, εφαρμογές, λογισμικό βελτιστοποίησης"),("Γλώσσες","Ελληνικά & αγγλικά"),("Πελάτες","Στην Πάτρα και εξ αποστάσεως"),("Προσέγγιση","Πρώτα κατανόηση, μετά υλοποίηση")],
  contact=dict(eyebrow="Επικοινωνία", h="Πείτε μας για <em>το έργο σας.</em>", lead="Γράψτε μας τι θέλετε να πετύχετε. Απαντάμε μέσα σε μία εργάσιμη με τα επόμενα βήματα και, όταν ταιριάζει, με πρόταση συνεργασίας.", phone="Τηλέφωνο", email="Email", where="Studio", where_v="Πάτρα, Ελλάδα", reply="Απάντηση", reply_v="Μέσα σε μία εργάσιμη",
    consent='Με την αποστολή συμφωνείτε με την <a href="privacy.html">πολιτική απορρήτου</a>.', who1="Νέο έργο", who2="Συνεργασία", subj1="Νέο αίτημα έργου · PG AI Solutions", subj2="Πρόταση συνεργασίας · PG AI Solutions",
    name="Όνομα", mail="Email", msg="Μήνυμα", ph_msg="Τι χρειάζεστε, με λίγα λόγια;", send="Αποστολή μηνύματος",
    t=dict(sending="Αποστολή…", sent="Εστάλη ✓", send="Αποστολή μηνύματος", thanks="Ευχαριστούμε. Θα σας απαντήσουμε σύντομα στο email σας.", fail="Το μήνυμα δεν στάλθηκε. Γράψτε μας στο pangeo57@yahoo.gr ή καλέστε στο +30 697 191 9078.")),
  band=("Λίγα έργα κάθε φορά","Δουλεύουμε με <em>λίγους πελάτες</em> ταυτόχρονα.","Έτσι κάθε έργο έχει την προσοχή μας από την πρώτη συνάντηση μέχρι την παράδοση. Πείτε μας για το δικό σας.","Κλείστε μια συνάντηση"),
  start_head=("Πώς ξεκινάμε", "Από την πρώτη κουβέντα <em>στην πρόταση.</em>", "Πρώτα καταλαβαίνουμε την επιχείρησή σας. Η τιμή βγαίνει από το τι χρειάζεται το έργο, όχι το αντίστροφο."),
  start=[("Γνωριμία","Μια κουβέντα, από κοντά ή online, για να καταλάβουμε τι θέλετε να πετύχετε και ποιοι θα το χρησιμοποιούν."),("Πρόταση","Γραπτή πρόταση με το τι περιλαμβάνει το έργο, το χρονοδιάγραμμα και το κόστος. Χωρίς εκπλήξεις αργότερα."),("Υλοποίηση","Σχεδιασμός και ανάπτυξη σε στάδια, με μια έκδοση που δουλεύει στα χέρια σας από νωρίς.")],
  budget=dict(label="Προϋπολογισμός", opts=["Δεν ξέρω ακόμα","2.000 – 5.000 €","5.000 – 15.000 €","15.000 € +"]),
  privacy="Πολιτική απορρήτου", privacy_href="privacy.html",
 ),
}

def fn(p): return "./" if p == "index" else f"{p}.html"
def url(lang, p):
    pre = BASE + ("/el/" if lang == "el" else "/")
    return pre if p == "index" else pre + f"{p}.html"

def plain(x): return html.unescape(re.sub(r"<[^>]+>", "", x))

def schema(L, p):
    """One JSON-LD graph per page: the business, the site, the page, breadcrumbs, and page-specific items."""
    t = T[L]; org = BASE + "/#org"; site = BASE + "/#site"; page = url(L, p)
    g = [{"@type":"ProfessionalService","@id":org,"name":"PG AI Solutions","url":BASE+"/","logo":BASE+"/assets/logo-512.png","image":BASE+"/assets/og-image.png",
          "description":T[L]["descs"]["index"],"telephone":"+306971919078","email":"pangeo57@yahoo.gr",
          "address":{"@type":"PostalAddress","addressLocality":"Patras" if L=="en" else "Πάτρα","addressRegion":"Achaea" if L=="en" else "Αχαΐα","addressCountry":"GR"},
          "areaServed":[{"@type":"City","name":"Patras" if L=="en" else "Πάτρα"},{"@type":"Country","name":"Greece" if L=="en" else "Ελλάδα"}],
          "knowsLanguage":["el","en"],
          "contactPoint":{"@type":"ContactPoint","contactType":"sales","telephone":"+306971919078","email":"pangeo57@yahoo.gr","availableLanguage":["Greek","English"]},
          "hasOfferCatalog":{"@type":"OfferCatalog","name":t["nav"]["services"],"itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":a,"description":b,"url":url(L,"services")+f"#s{i+1}"}} for i,(a,b,_) in enumerate(t["svc_detail"])]}},
         {"@type":"WebSite","@id":site,"url":BASE+"/","name":"PG AI Solutions","publisher":{"@id":org},"inLanguage":["en","el"]},
         {"@type":"WebPage","@id":page+"#page","url":page,"name":t["titles"][p],"description":t["descs"][p],"inLanguage":t["lang"],"isPartOf":{"@id":site},"about":{"@id":org}}]
    if p != "index":
        g.append({"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":t["crumb"],"item":url(L,"index")},{"@type":"ListItem","position":2,"name":t["titles"][p].split(" | ")[0],"item":page}]})
    if p == "services":
        for i,(a,b,lst) in enumerate(t["svc_detail"]):
            g.append({"@type":"Service","@id":page+f"#s{i+1}","name":a,"description":b,"serviceType":a,"provider":{"@id":org},"areaServed":{"@type":"Country","name":"Greece" if L=="en" else "Ελλάδα"},"url":page+f"#s{i+1}"})
        g.append({"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in t["faq"]]})
    if p == "work":
        items = []
        for i,pj in enumerate(PROJECTS):
            d = pj[L]; it = {"@type":"CreativeWork","name":d["name"],"description":d["desc"],"genre":d["kind"],"image":f'{BASE}/assets/work/{pj["img"]}.webp',"creator":{"@id":org},"keywords":", ".join(d["tags"])}
            if pj["live"]: it["url"] = pj["live"]
            items.append({"@type":"ListItem","position":i+1,"item":it})
        g.append({"@type":"ItemList","name":plain(t["work_intro"][1]),"itemListElement":items})
    return {"@context":"https://schema.org","@graph":g}

def head(L, p, pre):
    t = T[L]; title = t["titles"][p]; desc = t["descs"][p]
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{url(l,p)}">\n' for l in ("en","el")) + f'<link rel="alternate" hreflang="x-default" href="{url("en",p)}">\n'
    ld = '<script type="application/ld+json">' + json.dumps(schema(L, p), ensure_ascii=False) + '</script>\n'
    analytics = f'<script>window.PG_ANALYTICS={{"id":{json.dumps(GA4_ID)}}};</script>\n' if GA4_ID else '<script>window.PG_ANALYTICS={"id":""};</script>\n'
    other = "el" if L == "en" else "en"
    return f'''<!DOCTYPE html>
<html lang="{t["lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#06080F" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url(L,p)}">
{alts}<meta property="og:type" content="website">
<meta property="og:site_name" content="PG AI Solutions">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url(L,p)}">
<meta property="og:image" content="{BASE}/assets/og-image.png?v={V}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{t["og_alt"]}">
<meta property="og:locale" content="{t["locale"]}">
<meta property="og:locale:alternate" content="{T[other]["locale"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/assets/og-image.png?v={V}">
{ld}{analytics}<link rel="icon" type="image/svg+xml" href="{pre}logo/pg-icon.svg">
<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="preload" href="{pre}assets/fonts/manrope-{"greek" if L=="el" else "latin"}-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/site.css?v={V}">
<script>(function(d){{d.classList.add('js');try{{var t=localStorage.getItem('pg-theme');if(t)d.setAttribute('data-theme',t)}}catch(e){{}}}})(document.documentElement)</script>
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
<nav class="nav" aria-label="Main">{links}<a href="#contact" class="hide-s">{n["contact"]}</a><button class="theme" type="button" aria-label="{t["theme"]}" title="{t["theme"]}"><span aria-hidden="true"></span></button><a class="lang" href="{other}" hreflang="{t["other"]}" lang="{t["other"]}">{t["other_label"]}</a></nav>
</div></header>
'''

def sec_head(h, tag="h2"):
    e, title, lead = h
    return f'<div class="sec-head"><span class="eyebrow">{e}</span><{tag} class="h2">{title}</{tag}><p class="lead">{lead}</p></div>'

def intro(h, L=None, p=None):
    e, title, lead = h
    crumb = ""
    if L and p and p != "index":
        parent = plain(titles_for_breadcrumb(L, p))
        crumb = f'<nav class="breadcrumb" aria-label="{"Breadcrumb" if L == "en" else "Διαδρομή"}"><ol><li><a href="{url(L, "index")}">{T[L]["crumb"]}</a></li><li aria-current="page">{html.escape(parent)}</li></ol></nav>'
    return f'<section class="intro"><div class="wrap">{crumb}<span class="eyebrow">{e}</span><h1 class="h1">{title}</h1><p class="lead">{lead}</p></div></section>'

def titles_for_breadcrumb(L, p):
    return T[L]["titles"][p].split(" | ")[0]

def strip(L, pre):
    out = []
    for pj in PROJECTS:
        d = pj[L]
        out.append(f'<a class="wcard" href="work.html#{pj["id"]}"><span class="shot"><img src="{pre}assets/work/{pj["img"]}.webp?v={V}" width="480" height="1038" alt="" loading="lazy" decoding="async"></span><small>{d["kind"]}</small><b>{d["name"]}</b></a>')
    return '<div class="strip">' + "".join(out) + "</div>"

def steps(L):
    return '<div class="steps">' + "".join(f'<div class="step"><span class="n">0{i+1}</span><h3 class="h3">{a}</h3><p>{b}</p></div>' for i,(a,b) in enumerate(T[L]["steps"])) + "</div>"

def page_index(L, pre):
    t = T[L]; h = t["hero"]
    more = "Περισσότερα" if L=="el" else "Learn more"
    rows = "".join(f'<a class="scard rv" href="services.html#s{i+1}"><span class="sn">0{i+1}</span><svg class="smark" viewBox="0 0 48 16" aria-hidden="true"><path d="M2 12 L14 4 L26 10 L40 3" fill="none" stroke="url(#sg)" stroke-width="1.5"/><rect x="0" y="10" width="4" height="4" fill="#0593C6"/><rect x="38" y="1" width="4" height="4" fill="#D83995"/></svg><h3 class="h3">{a}</h3><p>{b}</p><span class="smore">{more} <i aria-hidden="true">→</i></span></a>' for i,(a,b) in enumerate(t["svcs"]))
    proof = "".join(f'<div class="rv"><b>{a}</b><span>{b}</span></div>' for a,b in h["proof"])
    k = 0; lines = []
    for txt, acc in h["h1"]:
        ws = []
        for w in txt.split():
            ws.append(f'<span class="wd{" g" if acc else ""}" style="--d:{200+70*k}ms">{w}</span>'); k += 1
        lines.append(" ".join(ws))
    h1 = lines[0] + "<br>" + " ".join(lines[1:])
    a = t["ask"]
    chips = "".join(f"<span>{c}</span>" for c in a["chips"])
    plan = f'<small>{a["note"]}</small>' + "".join(f"<div><b>{x}</b> · {y}</div>" for x, y in a["plan"])
    return f'''<section class="hero" aria-labelledby="hero-h"><canvas role="img" aria-label="{h["aria"]}"></canvas>
<div class="wrap"><div class="hero-txt"><span class="eyebrow live fade" style="--d:100ms">{h["tag"]}</span><h1 class="h1" id="hero-h">{h1}</h1><p class="lead fade" style="--d:700ms">{h["sub"]}</p>
<div class="hero-act fade" style="--d:850ms"><a class="btn" href="#contact">{h["cta"]} <i aria-hidden="true">→</i></a><a class="txtlink" href="work.html">{h["link"]}</a></div>
<div class="hud fade" style="--d:1100ms" aria-hidden="true"><div><span>{h["hud"][0]}</span><b data-n>0</b></div><div><span>{h["hud"][1]}</span><b data-it>0</b></div><div><span>{h["hud"][2]}</span><b data-km>…</b></div><i class="bar"><i data-bar></i></i></div></div>
<div class="phones fade" style="--d:1300ms" aria-hidden="true"><figure class="phone p1"><img src="{pre}assets/work/routepal.webp?v={V}" width="480" height="1038" alt=""></figure><figure class="phone p2"><img src="{pre}assets/work/cashflow.webp?v={V}" width="480" height="1038" alt=""></figure></div></div>
</section>
<div class="proof"><div class="wrap">{proof}</div></div>
<section class="sec ask"><div class="wrap"><div class="sec-head"><span class="eyebrow">{a["eyebrow"]}</span><h2 class="h2">{a["h"]}</h2><p class="lead">{a["lead"]}</p></div>
<div class="prompt" data-q="{html.escape(a["q"], quote=True)}"><p class="pin" aria-label="{html.escape(a["q"], quote=True)}"></p><div class="chips">{chips}</div><div class="plan">{plan}</div><a class="btn" href="#contact">{a["cta"]} <i aria-hidden="true">→</i></a></div></div></section>
<section class="sec"><svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="#3FB4E0"/><stop offset="1" stop-color="#F06BB4"/></linearGradient></defs></svg><div class="wrap">{sec_head(t["svc_head"])}<div class="sgrid">{rows}</div></div></section>
<section class="sec alt"><div class="wrap">{sec_head(t["work_head"])}{strip(L, pre)}<p style="margin-top:32px"><a class="btn line" href="work.html">{t["all_work"]} <i aria-hidden="true">→</i></a></p></div></section>
<section class="sec"><div class="wrap">{sec_head(t["proc_head"])}{steps(L)}</div></section>
<section class="cta-band"><div class="wrap"><div><span class="eyebrow">{t["band"][0]}</span><h2 class="h2">{t["band"][1]}</h2><p class="lead">{t["band"][2]}</p></div><a class="btn" href="#contact">{t["band"][3]} <i aria-hidden="true">→</i></a></div></section>
'''

def start_sec(L, cls="sec"):
    t = T[L]
    st = '<div class="steps steps3">' + "".join(f'<div class="step"><span class="n">0{i+1}</span><h3 class="h3">{a}</h3><p>{b}</p></div>' for i,(a,b) in enumerate(t["start"])) + "</div>"
    return f'<section class="{cls}"><div class="wrap">{sec_head(t["start_head"])}{st}</div></section>'

def faq_sec(L):
    t = T[L]
    items = "".join(f'<details class="qa"><summary><h3 class="h3">{q}</h3><i aria-hidden="true"></i></summary><p>{a}</p></details>' for q,a in t["faq"])
    return f'<section class="sec alt" id="faq"><div class="wrap">{sec_head(t["faq_head"])}<div class="faq">{items}</div></div></section>'

def page_services(L, pre):
    t = T[L]; out = []
    for i,(a,b,lst) in enumerate(t["svc_detail"]):
        li = "".join(f"<li>{x}</li>" for x in lst)
        out.append(f'<div class="svc" id="s{i+1}"><span class="n">0{i+1}</span><div class="body"><h2 class="h2">{a}</h2><p class="lead">{b}</p></div><ul class="plist">{li}</ul></div>')
    return intro(t["services_intro"], L, "services") + f'<section class="sec" style="padding-top:0"><div class="wrap">{"".join(out)}</div></section><section class="sec alt"><div class="wrap">{sec_head(t["proc_head"])}{steps(L)}</div></section>' + start_sec(L) + faq_sec(L)

def page_work(L, pre):
    t = T[L]; out = []
    for pj in PROJECTS:
        d = pj[L]
        live = f'<p><a class="btn line" href="{pj["live"]}" target="_blank" rel="noopener">{t["live"]} <i aria-hidden="true">↗</i></a></p>' if pj["live"] else ""
        st = ('<div class="stats">' + "".join(f'<div><b>{a}</b><span>{b}</span></div>' for a,b in d["stats"]) + '</div>') if d["stats"] else ""
        li = "".join(f"<li>{x}</li>" for x in d["pts"]); tg = "".join(f"<span>{x}</span>" for x in d["tags"])
        cls = "status live" if d["status"] == "Live" else "status"
        out.append(f'''<article class="proj" id="{pj["id"]}"><div class="pshot"><img src="{pre}assets/work/{pj["img"]}.webp?v={V}" width="480" height="1038" alt="{d["name"]}: {d["kind"].lower()}{" — screenshot" if L=="en" else " — στιγμιότυπο"}" loading="lazy" decoding="async"></div>
<div class="pbody"><span class="eyebrow">{d["kind"]}</span><h2 class="h2">{d["name"]}</h2><span class="{cls}">{d["status"]}</span><p class="lead">{d["desc"]}</p>{st}<ul class="plist">{li}</ul><div class="tags">{tg}</div>{live}</div></article>''')
    return intro(t["work_intro"], L, "work") + f'<section><div class="wrap">{"".join(out)}</div></section>'

def page_studio(L, pre):
    t = T[L]
    spec = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a,b in t["spec"])
    return intro(t["studio_intro"], L, "studio") + f'<section class="sec"><div class="wrap"><dl class="spec">{spec}</dl></div></section><section class="sec alt"><div class="wrap">{sec_head(t["proc_head"])}{steps(L)}</div></section>'

def contact(L):
    c = T[L]["contact"]
    tj = html.escape(json.dumps(c["t"], ensure_ascii=False), quote=True)
    return f'''<section class="contact" id="contact" aria-labelledby="c-h"><div class="wrap">
<div class="cinfo"><span class="eyebrow">{c["eyebrow"]}</span><h2 class="h2" id="c-h">{c["h"]}</h2><p class="lead">{c["lead"]}</p>
<dl><div><dt>{c["phone"]}</dt><dd><a href="tel:+306971919078">+30 697 191 9078</a></dd></div><div><dt>{c["email"]}</dt><dd><a href="mailto:pangeo57@yahoo.gr">pangeo57@yahoo.gr</a></dd></div><div><dt>{c["where"]}</dt><dd>{c["where_v"]}</dd></div><div><dt>{c["reply"]}</dt><dd>{c["reply_v"]}</dd></div></dl></div>
<form class="cf" action="https://formspree.io/f/xyeyvzga" method="POST" data-t="{tj}">
<input type="hidden" name="_subject" value="{c["subj1"]}"><input type="hidden" name="Πηγή" value="PG AI Solutions site">
<input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
<fieldset class="who"><legend class="hp">{c["who1"]} / {c["who2"]}</legend><label><input type="radio" name="Interest" value="Project" data-subj="{c["subj1"]}" checked><span>{c["who1"]}</span></label><label><input type="radio" name="Interest" value="Collaboration" data-subj="{c["subj2"]}"><span>{c["who2"]}</span></label></fieldset>
<div class="f2"><div class="fld"><label for="f-name">{c["name"]}</label><input id="f-name" name="Name" autocomplete="name" required></div><div class="fld"><label for="f-mail">{c["mail"]}</label><input id="f-mail" type="email" name="Email" autocomplete="email" required></div></div>
<div class="fld"><label for="f-budget">{T[L]["budget"]["label"]}</label><select id="f-budget" name="Budget">{"".join(f'<option>{o}</option>' for o in T[L]["budget"]["opts"])}</select></div>
<div class="fld"><label for="f-msg">{c["msg"]}</label><textarea id="f-msg" name="Message" placeholder="{c["ph_msg"]}" required></textarea></div>
<p class="fnote">{c["consent"]}</p>
<button class="btn" type="submit"><span>{c["send"]}</span> <i aria-hidden="true">→</i></button><p class="note" role="status" aria-live="polite"></p>
</form></div></section>
'''

def footer(L, pre):
    t = T[L]; n = t["nav"]
    links = "".join(f'<a href="{fn(k)}">{n[k]}</a>' for k in PAGES[1:])
    return f'''<footer class="ft"><div class="wrap"><span>© 2026 PG AI Solutions · {T[L]["contact"]["where_v"]}</span><nav aria-label="Footer">{links}<a href="{t["privacy_href"]}">{t["privacy"]}</a><a href="terms.html">{"Terms of use" if L=="en" else "Όροι χρήσης"}</a></nav></div></footer>
<script src="{pre}assets/site.js?v={V}" defer></script>
</body>
</html>
'''

def page_privacy(L, pre):
    body = open(os.path.join(ROOT, f"scripts/content/privacy.{L}.html"), encoding="utf-8").read()
    h = ("Privacy","Privacy <em>policy.</em>","What this website collects, why, and your rights.") if L=="en" else ("Απόρρητο","Πολιτική <em>απορρήτου.</em>","Τι συλλέγει αυτός ο ιστότοπος, γιατί, και ποια είναι τα δικαιώματά σας.")
    return intro(h, L, "privacy") + f'<section class="sec" style="padding-top:clamp(48px,6vw,80px)"><div class="wrap"><article class="prose">{body}</article></div></section>'

def page_terms(L, pre):
    body = open(os.path.join(ROOT, f"scripts/content/terms.{L}.html"), encoding="utf-8").read()
    h = ("Terms","Terms <em>of use.</em>","The rules for using this website.") if L=="en" else ("Όροι","Όροι <em>χρήσης.</em>","Οι κανόνες χρήσης αυτού του ιστότοπου.")
    return intro(h, L, "terms") + f'<section class="sec" style="padding-top:clamp(48px,6vw,80px)"><div class="wrap"><article class="prose">{body}</article></div></section>'

BUILD = dict(index=page_index, services=page_services, work=page_work, studio=page_studio, privacy=page_privacy, terms=page_terms)
for L in ("en", "el"):
    pre = "../" if L == "el" else ""
    for p in PAGES + ["privacy", "terms"]:
        body = head(L, p, pre) + header(L, p, pre) + '<main id="main">\n' + BUILD[p](L, pre) + '\n</main>\n' + (contact(L) if p not in ("privacy", "terms") else "") + footer(L, pre)
        path = os.path.join(ROOT, "el" if L == "el" else "", "index.html" if p == "index" else f"{p}.html")
        open(path, "w", encoding="utf-8").write(body)
        print("wrote", os.path.relpath(path, ROOT))

# 404 (served from any path, so every link is absolute)
nf = head("en", "index", BASE + "/").replace(T["en"]["titles"]["index"], "Page not found | PG AI Solutions").replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
nf += f'''<main id="main"><section class="intro" style="border:0"><div class="wrap"><span class="eyebrow">404</span><h1 class="h1">Page <em>not found.</em></h1><p class="lead">This page does not exist or has moved. Η σελίδα δεν υπάρχει ή έχει μετακινηθεί.</p><div class="hero-act"><a class="btn" href="{BASE}/">Home <i aria-hidden="true">→</i></a><a class="btn line" href="{BASE}/el/" lang="el">Αρχική <i aria-hidden="true">→</i></a></div></div></section></main>
</body>
</html>
'''
open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(nf)
print("wrote 404.html")

# sitemap
urls = []
for p in PAGES + ["privacy", "terms"]:
    for L in ("en","el"):
        loc = url(L,p)
        alt = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{url(l,p)}"/>' for l in ("en","el")) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{url("en",p)}"/>'
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>{alt}\n  </url>")
open(os.path.join(ROOT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
print("wrote sitemap.xml")
