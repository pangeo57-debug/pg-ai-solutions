#!/usr/bin/env python3
"""Χτίζει τις σελίδες του site (EN στη ρίζα, EL στο /el/) από ένα κοινό template.
Χρήση: python3 scripts/build.py   — αλλάζεις κείμενα εδώ, όχι στα .html."""
import json, os, html, re, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://pangeo57-debug.github.io/pg-ai-solutions"
V = "20"
GA4_ID = os.environ.get("PG_GA4_ID") or os.environ.get("GA4_MEASUREMENT_ID") or ""
TURNSTILE_SITE_KEY = os.environ.get("PG_TURNSTILE_SITE_KEY") or ""
TODAY = datetime.date.today().isoformat()
LOGO = open(os.path.join(ROOT, "logo/pg-mark.svg"), encoding="utf-8").read().replace(' role="img" aria-label="PG"', ' aria-hidden="true"').replace('id="pgr"', 'id="pgr-h"').replace("url(#pgr)", "url(#pgr-h)")
PAGES = ["index", "services", "work", "studio"]

PROJECTS = [
 dict(id="routepal", img="routepal", live="https://pangeo57-debug.github.io/routiq/routiq.html",
  en=dict(kind="Route optimization", name="Routepal", status="Live",
   desc="A complete weekly planning app for appointments and visits, with the schedule arranged around people, locations and availability.",
   stats=[],
   pts=["A clear daily and weekly plan","Maps and navigation for each stop","Appointments organised by group or paired visit","Easy PDF handover and phone use"],
   tags=["Planning","Appointments","Mobile"]),
  el=dict(kind="Βελτιστοποίηση διαδρομών", name="Routepal", status="Live",
   desc="Μία πλήρης εφαρμογή εβδομαδιαίου προγραμματισμού για ραντεβού και επισκέψεις, με πρόγραμμα οργανωμένο γύρω από ανθρώπους, τοποθεσίες και διαθεσιμότητα.",
   stats=[],
   pts=["Καθαρό ημερήσιο και εβδομαδιαίο πρόγραμμα","Χάρτης και πλοήγηση για κάθε στάση","Ομαδοποίηση και συνδυασμός ραντεβού","Εύκολη εξαγωγή PDF και χρήση στο κινητό"],
   tags=["Προγραμματισμός","Ραντεβού","Κινητό"])),
 dict(id="cashflow", img="cashflow", live=None,
  en=dict(kind="Finance app", name="Cash Flow", status="Private app · demo on request",
   desc="A personal finance app: income and expenses in two taps, clear statistics, and data that stays on the phone, even offline.",
   stats=[], pts=["Income and expenses in a few taps","Recurring payments and monthly budgets","Clear personal statistics","Works on the phone, even offline","Private data with an easy backup"],
   tags=["Personal finance","Mobile","Privacy"]),
  el=dict(kind="Εφαρμογή οικονομικών", name="Cash Flow", status="Ιδιωτική εφαρμογή · demo κατόπιν αιτήματος",
   desc="Εφαρμογή προσωπικών οικονομικών: έσοδα και έξοδα με δύο πατήματα, καθαρά στατιστικά και δεδομένα που μένουν στο κινητό, ακόμα και offline.",
   stats=[], pts=["Έσοδα και έξοδα σε λίγα πατήματα","Επαναλαμβανόμενες πληρωμές και μηνιαίοι στόχοι","Καθαρά προσωπικά στατιστικά","Λειτουργεί στο κινητό, ακόμα και χωρίς internet","Ιδιωτικά δεδομένα με εύκολο αντίγραφο"],
   tags=["Προσωπικά οικονομικά","Κινητό","Ιδιωτικότητα"])),
]

T = {
 "en": dict(
  lang="en", locale="en_GB", theme="Switch light / dark theme", other="el", other_label="ΕΛ",
  nav=dict(index="Home", services="Services", work="Work", studio="Studio", contact="Contact"),
  titles=dict(index="Web Design & Apps in Patras, Greece | PG AI Solutions", services="Websites, Apps & Optimization Software | PG AI Solutions", work="Our Work: Websites, Apps & Optimization | PG AI Solutions", studio="Software Studio in Patras, Greece | PG AI Solutions", privacy="Privacy Policy | PG AI Solutions", terms="Terms of Use | PG AI Solutions"),
  descs=dict(index="Custom websites and mini apps for small businesses in Patras and remotely across Greece. Clear scope, clean design and a working result.", services="Professional websites and e-shops, AI business automations and custom web applications. Clear scope and direct handover.", work="Selected work from PG AI Solutions: Routepal route optimization and Cash Flow personal finance.", studio="PG AI Solutions is a small software studio in Patras, Greece. We build websites and custom business tools.", privacy="How the PG AI Solutions website handles personal data: what we collect, why, who receives it, how long we keep it and your rights.", terms="Terms of use for the PG AI Solutions website: content, accuracy of information, links to other sites and governing law."),
  crumb="Home", og_alt="PG AI Solutions: websites, apps and optimization software from Patras, Greece",
  faq_head=("Questions", "Common <em>questions.</em>", "Short answers to what businesses ask us first."),
  faq=[("How much does a website or an app cost?","The price comes from what the project needs, not the other way around. After a first conversation we send a written proposal with clear scope, timeline and cost, so there are no surprises later."),
       ("How quickly do you reply?","Within one working day, with clear next steps and, when it fits, a proposal."),
       ("Do you work with businesses outside Patras?","Yes. We are based in Patras, Greece, and work with both local and remote clients, in Greek and English."),
       ("Who owns the website, the domain and the data?","You do. The domain and the accounts are yours, and your data stays yours, with export and backup."),
       ("Can the app be used on a phone?","Yes. Custom apps can be designed for a clean phone and desktop experience."),
       ("Do you handle launch and maintenance?","Yes. We include the agreed launch, handover and follow-up support.")],
  skip="Skip to content",
  hero=dict(tag="Custom websites & mini apps · Patras", h1=[("Websites and apps",0),("built around your business.",1)], sub="Simple, premium websites and focused mini apps for small businesses. Built clearly, handover cleanly, and used by real people.", cta="Discuss a project", link="See selected work", aria="Animation: a real route optimizer arranges scattered stops into the PG monogram, then into the shortest route of a working day", proof=[("1","clear scope"),("1","working day to reply"),("Custom","built for your workflow"),("EN / EL","bilingual delivery")]),
  ask=dict(eyebrow="Tell us what you need", h="One sentence. <em>A clear plan.</em>", lead="Write it the way you would say it to a colleague. Within one working day you have a reply with the next steps.", note="Example plan for a project like this", q="I need a booking app that also builds the week's schedule by itself", chips=["Booking app","Bilingual website","Shift scheduling","Delivery routes"], plan=[("Week 1","we learn how you work today"),("Weeks 2–4","we build the app and the automatic schedule"),("Week 5","testing with your own data, then handover")], cta="Describe your project"),
  svc_head=("What we do", "Three clear <em>services.</em>", "Choose the practical result your business needs."),
  svcs=[("Professional websites & e-shops","Modern, fast websites and online stores built to present your offer clearly and generate sales."),("AI automation & digital assistants","Automations for bookings, requests and orders, plus AI assistants trained around your business."),("Custom web apps & optimization","Focused tools for routing, planning and management, built around your real workflow.")],
  work_head=("Selected work", "A small selection. <em>Built properly.</em>", "Two examples of custom software, with the detail kept where it matters."),
  all_work="View more work",
  proc_head=("How we work", "Four steps, <em>each one checked.</em>", "Before we move to the next step, we check that the previous one solves your real problem."),
  steps=[("Understand","We learn who will use it, what limits you have and what the real goal is, before any design or code."),("Design","We design the data, the logic and the screens together, so no expensive changes are needed later."),("Build","We deliver in small pieces and test with real scenarios, not only the ideal case."),("Launch & improve","We put it live, watch how it is used and keep improving it. The work does not stop at handover.")],
  services_intro=("Services","What we <em>build.</em>","We take on a few projects at a time, so each one has our attention from the first conversation to launch and after."),
  svc_detail=[
   ("Professional websites & e-shops","Fast, modern websites and online stores that turn visitors into enquiries and customers.",["A focused website or e-shop built for your offer","Clear product, service and contact pages","Mobile-first responsive design","SEO-ready structure and analytics setup","Launch support and practical maintenance"]),
   ("AI automation & digital assistants","AI and simple automations that reduce repetitive work and keep requests moving.",["Booking and appointment automation","Order and enquiry management","AI assistants for common customer questions","Connections to your existing tools","Clear handover and staff guidance"]),
   ("Custom web apps & optimization","Custom tools for field work, planning and team management.",["Route and schedule planning","Customer or booking management","Operational dashboards","Tools tailored to your daily workflow","Maintenance and future improvements"])],
  work_intro=("Work","What we have <em>built.</em>","Every project started from a real problem a business had. See what we delivered and how it works."),
  live="Visit live site",
  studio_intro=("Studio","First we understand, <em>then we build.</em>","PG AI Solutions is a small studio based in Patras, Greece. We build premium websites and focused mini apps that fit the way each business really works."),
  spec=[("Based in","Patras, Greece"),("What we build","Premium websites and focused mini apps"),("Languages","Greek & English"),("Clients","Local and remote"),("Approach","Understand first, then build")],
  contact=dict(eyebrow="Contact", h="Tell us about <em>your project.</em>", lead="Write to us with what you want to achieve. We reply within one working day with the next steps and, when it fits, a proposal.", phone="Phone", email="Email", where="Studio", where_v="Patras, Greece", reply="Reply", reply_v="Within one working day",
    consent='By sending this form you agree to our <a href="privacy.html">privacy policy</a>.', who1="New project", who2="Partnership", subj1="New project inquiry · PG AI Solutions", subj2="Collaboration inquiry · PG AI Solutions",
    name="Name", mail="Email", msg="Message", ph_msg="What do you need, in a few words?", send="Send message",
    t=dict(sending="Sending…", sent="Sent ✓", send="Send message", thanks="Thank you. We will reply to you soon.", fail="The message could not be sent. Please use the form again or call +30 697 191 9078.")),
  band=("A few projects at a time","We work with <em>a few clients</em> at once.","That way every project has our attention from the first meeting to delivery. Tell us about yours.","Book a meeting"),
  start_head=("How we start", "From first call <em>to proposal.</em>", "First we understand your business. The price comes from what the project needs, not the other way around."),
  start=[("Conversation","A call or a meeting to understand what you want to achieve and who will use it."),("Proposal","A written proposal with what the project includes, the timeline and the cost. No surprises later."),("Delivery","Design and build in stages, with a working version in your hands early.")],
  packages=dict(head=("Ways to start","Choose the smallest useful <em>scope.</em>","A starting point, shaped into a clear written proposal."), items=[("1","Professional website or e-shop","Essential pages, mobile-first design, SEO setup and launch.","Request a quote"),("2","AI automation","One focused workflow, AI assistant or request-management process.","Discuss your workflow"),("3","Custom web solution","A tailored application with integrations, reporting or optimization.","Book a free assessment")]),
  budget=dict(label="Budget", opts=["Not sure yet","€2,000 – €5,000","€5,000 – €15,000","€15,000+"]),
  privacy="Privacy policy", privacy_href="privacy.html",
 ),
 "el": dict(
  lang="el", locale="el_GR", theme="Εναλλαγή ανοιχτού / σκούρου θέματος", other="en", other_label="EN",
  nav=dict(index="Αρχική", services="Υπηρεσίες", work="Έργα", studio="Studio", contact="Επικοινωνία"),
  titles=dict(index="Κατασκευή Ιστοσελίδων & Εφαρμογών, Πάτρα | PG AI Solutions", services="Ιστοσελίδες, Εφαρμογές & Λογισμικό | PG AI Solutions", work="Έργα: Ιστοσελίδες & Εφαρμογές | PG AI Solutions", studio="Studio Ανάπτυξης Λογισμικού στην Πάτρα | PG AI Solutions", privacy="Πολιτική Απορρήτου | PG AI Solutions", terms="Όροι Χρήσης | PG AI Solutions"),
  descs=dict(index="Επαγγελματικές ιστοσελίδες και custom αυτοματισμοί για μικρές επιχειρήσεις στην Πάτρα και εξ αποστάσεως. Καθαρό πλάνο και λειτουργικό αποτέλεσμα.", services="Επαγγελματικές ιστοσελίδες και e-shops, AI αυτοματισμοί και custom web εφαρμογές. Καθαρό πεδίο και σαφή παράδοση.", work="Επιλεγμένα έργα της PG AI Solutions: Routepal για βελτιστοποίηση διαδρομών και Cash Flow.", studio="Η PG AI Solutions είναι μικρό studio στην Πάτρα. Φτιάχνουμε επαγγελματικές ιστοσελίδες και custom εργαλεία για επιχειρήσεις.", privacy="Πώς ο ιστότοπος της PG AI Solutions διαχειρίζεται προσωπικά δεδομένα: τι συλλέγουμε, γιατί, ποιος τα λαμβάνει, για πόσο τα κρατάμε και τα δικαιώματά σας.", terms="Όροι χρήσης του ιστότοπου της PG AI Solutions: περιεχόμενο, ακρίβεια πληροφοριών, σύνδεσμοι προς άλλους ιστότοπους και εφαρμοστέο δίκαιο."),
  crumb="Αρχική", og_alt="PG AI Solutions: ιστοσελίδες, εφαρμογές και λογισμικό βελτιστοποίησης από την Πάτρα",
  faq_head=("Ερωτήσεις", "Συχνές <em>ερωτήσεις.</em>", "Σύντομες απαντήσεις σε όσα μας ρωτούν πρώτα οι επιχειρήσεις."),
  faq=[("Πόσο κοστίζει η κατασκευή ιστοσελίδας ή εφαρμογής;","Η τιμή βγαίνει από το τι χρειάζεται το έργο, όχι το αντίστροφο. Μετά την πρώτη κουβέντα στέλνουμε γραπτή πρόταση με το τι περιλαμβάνει, το χρονοδιάγραμμα και το κόστος, χωρίς εκπλήξεις αργότερα."),
       ("Σε πόσο χρόνο απαντάτε;","Μέσα σε μία εργάσιμη, με σαφή επόμενα βήματα και, όπου ταιριάζει, πρόταση συνεργασίας."),
       ("Δουλεύετε με επιχειρήσεις εκτός Πάτρας;","Ναι. Η έδρα μας είναι στην Πάτρα και δουλεύουμε με τοπικούς και απομακρυσμένους πελάτες, στα ελληνικά και στα αγγλικά."),
       ("Σε ποιον ανήκουν η ιστοσελίδα, το domain και τα δεδομένα;","Σε εσάς. Το domain και οι λογαριασμοί είναι δικά σας, και τα δεδομένα μένουν δικά σας, με εξαγωγή και αντίγραφο."),
       ("Μπορεί η εφαρμογή να χρησιμοποιηθεί στο κινητό;","Ναι. Οι custom εφαρμογές μπορούν να σχεδιαστούν καθαρά για κινητό και υπολογιστή."),
       ("Αναλαμβάνετε δημοσίευση και συντήρηση;","Ναι. Περιλαμβάνουμε την συμφωνημένη δημοσίευση, παράδοση και μετέπειτα υποστήριξη.")],
  skip="Μετάβαση στο περιεχόμενο",
  hero=dict(tag="Custom ιστοσελίδες & mini εφαρμογές · Πάτρα", h1=[("Ιστοσελίδες και εφαρμογές",0),("φτιαγμένες για την επιχείρησή σας.",1)], sub="Απλές, premium ιστοσελίδες και στοχευμένες mini εφαρμογές για μικρές επιχειρήσεις. Καθαρή υλοποίηση και σαφής παράδοση.", cta="Συζητήστε το έργο σας", link="Δείτε επιλεγμένα έργα", aria="Κινούμενη εικόνα: ένας πραγματικός αλγόριθμος βελτιστοποίησης τακτοποιεί σκόρπιες στάσεις στο μονόγραμμα PG και μετά στη συντομότερη διαδρομή μιας εργάσιμης μέρας", proof=[("1","καθαρό πεδίο"),("1","εργάσιμη για απάντηση"),("Custom","για τη δική σας ροή"),("EL / EN","δίγλωσση παράδοση")]),
  ask=dict(eyebrow="Πείτε μας τι χρειάζεστε", h="Μια πρόταση. <em>Ένα καθαρό πλάνο.</em>", lead="Γράψτε το όπως θα το λέγατε σε έναν συνεργάτη. Μέσα σε μία εργάσιμη έχετε απάντηση με τα επόμενα βήματα.", note="Ενδεικτικό πλάνο για ένα τέτοιο έργο", q="Θέλω εφαρμογή για ραντεβού που βγάζει μόνη της το πρόγραμμα της εβδομάδας", chips=["Εφαρμογή κρατήσεων","Δίγλωσση ιστοσελίδα","Πρόγραμμα βαρδιών","Δρομολόγια"], plan=[("Εβδ. 1","μαθαίνουμε πώς δουλεύετε σήμερα"),("Εβδ. 2–4","φτιάχνουμε την εφαρμογή και το αυτόματο πρόγραμμα"),("Εβδ. 5","δοκιμή με τα δικά σας δεδομένα και παράδοση")], cta="Περιγράψτε το έργο σας"),
  svc_head=("Τι κάνουμε", "Τρεις σαφείς <em>υπηρεσίες.</em>", "Επιλέγουμε το πρακτικό αποτέλεσμα που χρειάζεται η επιχείρησή σας."),
  svcs=[("Επαγγελματικές ιστοσελίδες & e-shop","Modern, γρήγορες ιστοσελίδες και ηλεκτρονικά καταστήματα που παρουσιάζουν καθαρά την προσφορά και διευκολύνουν τις πωλήσεις."),("AI αυτοματισμοί & ψηφιακοί βοηθοί","Αυτοματισμοί για κρατήσεις, αιτήματα και παραγγελίες, με AI βοηθούς προσαρμοσμένους στην επιχείρησή σας."),("Custom web εφαρμογές & βελτιστοποίηση","Εξειδικευμένα εργαλεία για δρομολόγηση, προγραμματισμό και διαχείριση, χτισμένα γύρω από τη δική σας δουλειά.")],
  work_head=("Επιλεγμένα έργα", "Μικρή επιλογή. <em>Σωστή υλοποίηση.</em>", "Δύο παραδείγματα custom λογισμικού, με τη λεπτομέρεια εκεί που πραγματικά χρειάζεται."),
  all_work="Δείτε περισσότερα",
  proc_head=("Πώς δουλεύουμε", "Τέσσερα βήματα, <em>με έλεγχο σε καθένα.</em>", "Πριν προχωρήσουμε στο επόμενο βήμα, ελέγχουμε ότι το προηγούμενο λύνει το πραγματικό σας πρόβλημα."),
  steps=[("Κατανόηση","Μαθαίνουμε ποιοι θα το χρησιμοποιούν, τι περιορισμούς έχετε και ποιος είναι ο πραγματικός στόχος, πριν από σχέδιο ή κώδικα."),("Σχεδιασμός","Σχεδιάζουμε μαζί τα δεδομένα, τη λογική και τις οθόνες, ώστε να μη χρειαστούν ακριβές αλλαγές αργότερα."),("Υλοποίηση","Παραδίδουμε σε μικρά κομμάτια και δοκιμάζουμε με πραγματικά σενάρια, όχι μόνο με την ιδανική περίπτωση."),("Παράδοση & βελτίωση","Το βγάζουμε στον αέρα, βλέπουμε πώς χρησιμοποιείται και το βελτιώνουμε. Η δουλειά δεν σταματά στην παράδοση.")],
  services_intro=("Υπηρεσίες","Τι <em>φτιάχνουμε.</em>","Αναλαμβάνουμε λίγα έργα κάθε φορά, ώστε το καθένα να έχει την προσοχή μας από την πρώτη κουβέντα μέχρι την παράδοση και μετά."),
  svc_detail=[
   ("Επαγγελματικές ιστοσελίδες & e-shops","Γρήγορες, modern ιστοσελίδες και ηλεκτρονικά καταστήματα που παρουσιάζουν καθαρά την προσφορά και διευκολύνουν την αγορά.",["Website ή e-shop χτισμένο γύρω από την επιχείρησή σας","Καθαρά σελίδες προϊόντων, υπηρεσιών και επικοινωνίας","Responsive σχεδιασμό για κάθε συσκευή","SEO-ready δομή και analytics setup","Δημοσίευση και πρακτική συντήρηση"]),
   ("AI αυτοματισμοί & ψηφιακοί βοηθοί","Εργαλεία που μειώνουν την επαναλαμβανόμενη δουλειά και κρατούν τα αιτήματα σε ροή.",["Αυτοματοποίηση κρατήσεων και ραντεβού","Διαχείριση παραγγελιών και αιτημάτων","AI βοηθοί για συχνές ερωτήσεις πελατών","Σύνδεση με τα εργαλεία που ήδη χρησιμοποιείτε","Σαφής παράδοση και καθοδήγηση προσωπικού"]),
   ("Custom web εφαρμογές & λύσεις βελτιστοποίησης","Εξειδικευμένα εργαλεία για πεδία δουλειάς, προγραμματισμό και διαχείριση.",["Δρομολόγηση και προγράμματα","Διαχείριση πελατών ή κρατήσεων","Πίνακες για καθημερινές λειτουργίες","Εργαλεία φτιαγμένα γύρω από τη δική σας δουλειά","Συντήρηση και μελλοντικές βελτιώσεις"])],
  work_intro=("Έργα","Τι έχουμε <em>φτιάξει.</em>","Κάθε έργο ξεκίνησε από ένα πραγματικό πρόβλημα μιας επιχείρησης. Δείτε τι παραδώσαμε και πώς δουλεύει."),
  live="Δείτε το live",
  studio_intro=("Studio","Πρώτα καταλαβαίνουμε, <em>μετά υλοποιούμε.</em>","Η PG AI Solutions είναι μικρό studio με έδρα την Πάτρα. Φτιάχνουμε premium ιστοσελίδες και στοχευμένες mini εφαρμογές που ταιριάζουν στον τρόπο που δουλεύει πραγματικά κάθε επιχείρηση."),
  spec=[("Έδρα","Πάτρα, Ελλάδα"),("Τι φτιάχνουμε","Ιστοσελίδες, εφαρμογές, λογισμικό βελτιστοποίησης"),("Γλώσσες","Ελληνικά & αγγλικά"),("Πελάτες","Στην Πάτρα και εξ αποστάσεως"),("Προσέγγιση","Πρώτα κατανόηση, μετά υλοποίηση")],
  contact=dict(eyebrow="Επικοινωνία", h="Πείτε μας για <em>το έργο σας.</em>", lead="Γράψτε μας τι θέλετε να πετύχετε. Απαντάμε μέσα σε μία εργάσιμη με τα επόμενα βήματα και, όταν ταιριάζει, με πρόταση συνεργασίας.", phone="Τηλέφωνο", email="Email", where="Studio", where_v="Πάτρα, Ελλάδα", reply="Απάντηση", reply_v="Μέσα σε μία εργάσιμη",
    consent='Με την αποστολή συμφωνείτε με την <a href="privacy.html">πολιτική απορρήτου</a>.', who1="Νέο έργο", who2="Συνεργασία", subj1="Νέο αίτημα έργου · PG AI Solutions", subj2="Πρόταση συνεργασίας · PG AI Solutions",
    name="Όνομα", mail="Email", msg="Μήνυμα", ph_msg="Τι χρειάζεστε, με λίγα λόγια;", send="Αποστολή μηνύματος",
    t=dict(sending="Αποστολή…", sent="Εστάλη ✓", send="Αποστολή μηνύματος", thanks="Ευχαριστούμε. Θα σας απαντήσουμε σύντομα.", fail="Το μήνυμα δεν στάλθηκε. Δοκιμάστε ξανά τη φόρμα ή καλέστε στο +30 697 191 9078.")),
  band=("Λίγα έργα κάθε φορά","Δουλεύουμε με <em>λίγους πελάτες</em> ταυτόχρονα.","Έτσι κάθε έργο έχει την προσοχή μας από την πρώτη συνάντηση μέχρι την παράδοση. Πείτε μας για το δικό σας.","Κλείστε μια συνάντηση"),
  start_head=("Πώς ξεκινάμε", "Από την πρώτη κουβέντα <em>στην πρόταση.</em>", "Πρώτα καταλαβαίνουμε την επιχείρησή σας. Η τιμή βγαίνει από το τι χρειάζεται το έργο, όχι το αντίστροφο."),
  start=[("Γνωριμία","Μια κουβέντα, από κοντά ή online, για να καταλάβουμε τι θέλετε να πετύχετε και ποιοι θα το χρησιμοποιούν."),("Πρόταση","Γραπτή πρόταση με το τι περιλαμβάνει το έργο, το χρονοδιάγραμμα και το κόστος. Χωρίς εκπλήξεις αργότερα."),("Υλοποίηση","Σχεδιασμός και ανάπτυξη σε στάδια, με μια έκδοση που δουλεύει στα χέρια σας από νωρίς.")],
  packages=dict(head=("Τρόποι να ξεκινήσετε","Επιλέξτε το μικρότερο χρήσιμο <em>πεδίο.</em>","Ένα σημείο εκκίνησης που γίνεται σαφή γραπτή πρόταση."), items=[("1","Επαγγελματική ιστοσελίδα ή e-shop","Βασικές σελίδες, mobile-first σχεδιασμός, SEO setup και δημοσίευση.","Ζητήστε προσφορά"),("2","AI αυτοματισμός","Μία στοχευμένη ροή εργασίας, AI βοηθός ή διαχείριση αιτημάτων.","Συζητήστε τη ροή σας"),("3","Custom web λύση","Εξειδικευμένη εφαρμογή με integrations, αναφορές ή βελτιστοποίηση.","Κλείστε δωρεάν αξιολόγηση")]),
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
          "description":T[L]["descs"]["index"],"telephone":"+306971919078",
          "address":{"@type":"PostalAddress","addressLocality":"Patras" if L=="en" else "Πάτρα","addressRegion":"Achaea" if L=="en" else "Αχαΐα","addressCountry":"GR"},
          "areaServed":[{"@type":"City","name":"Patras" if L=="en" else "Πάτρα"},{"@type":"Country","name":"Greece" if L=="en" else "Ελλάδα"}],
          "knowsLanguage":["el","en"],
          "contactPoint":{"@type":"ContactPoint","contactType":"sales","telephone":"+306971919078","availableLanguage":["Greek","English"]},
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
    protection = f'<script>window.PG_TURNSTILE_SITE_KEY={json.dumps(TURNSTILE_SITE_KEY)};</script>\n'
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
{ld}{analytics}{protection}<link rel="icon" type="image/svg+xml" href="{pre}logo/pg-icon.svg">
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
<nav class="nav" aria-label="Main">{links}<a href="{"./" if p in ("privacy","terms") else ""}#contact" class="hide-s">{n["contact"]}</a><button class="theme" type="button" aria-label="{t["theme"]}" title="{t["theme"]}"><span aria-hidden="true"></span></button><a class="lang" href="{other}" hreflang="{t["other"]}" lang="{t["other"]}">{t["other_label"]}</a></nav>
</div></header>
'''

def sec_head(h, tag="h2"):
    e, title, lead = h
    return f'<div class="sec-head"><span class="eyebrow">{e}</span><{tag} class="h2">{title}</{tag}><p class="lead">{lead}</p></div>'

def intro(h, L=None, p=None):
    e, title, lead = h
    crumb = ""
    if L and p and p != "index":
        parent = plain(T[L]["titles"][p].split(" | ")[0])
        crumb = f'<nav class="breadcrumb" aria-label="{"Breadcrumb" if L == "en" else "Διαδρομή"}"><ol><li><a href="{url(L, "index")}">{T[L]["crumb"]}</a></li><li aria-current="page">{html.escape(parent)}</li></ol></nav>'
    return f'<section class="intro"><div class="wrap">{crumb}<span class="eyebrow">{e}</span><h1 class="h1">{title}</h1><p class="lead">{lead}</p></div></section>'

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
<div class="wrap"><div class="hero-txt"><span class="eyebrow live fade" style="--d:100ms">{h["tag"]}</span><h1 class="h1" id="hero-h">{h1}</h1></div>
<div class="stage"></div>
<div class="hero-txt hero-sub"><p class="lead fade" style="--d:850ms">{h["sub"]}</p>
<div class="hero-act fade" style="--d:1000ms"><a class="btn" href="#contact">{h["cta"]} <i aria-hidden="true">→</i></a><a class="txtlink" href="work.html">{h["link"]}</a></div></div>
<div class="phones fade" style="--d:1300ms" aria-hidden="true"><figure class="phone p1"><img src="{pre}assets/work/routepal.webp?v={V}" width="480" height="1038" alt=""></figure><figure class="phone p2"><img src="{pre}assets/work/cashflow.webp?v={V}" width="480" height="1038" alt=""></figure></div></div>
</section>
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

def packages_sec(L):
    t = T[L]["packages"]
    items = "".join(f'<div class="step"><span class="n">{n}</span><h3 class="h3">{name}</h3><p>{desc}</p><p><a class="txtlink" href="#contact">{cta} <i aria-hidden="true">→</i></a></p></div>' for n,name,desc,cta in t["items"])
    return f'<section class="sec alt"><div class="wrap">{sec_head(t["head"])}<div class="steps steps3">{items}</div></div></section>'

def page_services(L, pre):
    t = T[L]; out = []
    for i,(a,b,lst) in enumerate(t["svc_detail"]):
        li = "".join(f"<li>{x}</li>" for x in lst)
        out.append(f'<div class="svc" id="s{i+1}"><span class="n">0{i+1}</span><div class="body"><h2 class="h2">{a}</h2><p class="lead">{b}</p></div><ul class="plist">{li}</ul></div>')
    return intro(t["services_intro"], L, "services") + f'<section class="sec" style="padding-top:0"><div class="wrap">{"".join(out)}</div></section><section class="sec alt"><div class="wrap">{sec_head(t["proc_head"])}{steps(L)}</div></section>' + packages_sec(L) + start_sec(L) + faq_sec(L)

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
<dl><div><dt>{c["phone"]}</dt><dd><a href="tel:+306971919078">+30 697 191 9078</a></dd></div><div><dt>{c["where"]}</dt><dd>{c["where_v"]}</dd></div><div><dt>{c["reply"]}</dt><dd>{c["reply_v"]}</dd></div></dl></div>
<form class="cf" action="https://formspree.io/f/xyeyvzga" method="POST" data-t="{tj}">
<input type="hidden" name="_subject" value="{c["subj1"]}"><input type="hidden" name="Πηγή" value="PG AI Solutions site">
<input type="hidden" name="_form_started" value="">
<input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
<fieldset class="who"><legend class="hp">{c["who1"]} / {c["who2"]}</legend><label><input type="radio" name="Interest" value="Project" data-subj="{c["subj1"]}" checked><span>{c["who1"]}</span></label><label><input type="radio" name="Interest" value="Collaboration" data-subj="{c["subj2"]}"><span>{c["who2"]}</span></label></fieldset>
<div class="f2"><div class="fld"><label for="f-name">{c["name"]}</label><input id="f-name" name="Name" autocomplete="name" maxlength="80" required></div><div class="fld"><label for="f-mail">{c["mail"]}</label><input id="f-mail" type="email" name="Email" autocomplete="email" maxlength="254" required></div></div>
<div class="fld"><label for="f-budget">{T[L]["budget"]["label"]}</label><select id="f-budget" name="Budget">{"".join(f'<option>{o}</option>' for o in T[L]["budget"]["opts"])}</select></div>
<div class="fld"><label for="f-msg">{c["msg"]}</label><textarea id="f-msg" name="Message" placeholder="{c["ph_msg"]}" minlength="10" maxlength="3000" required></textarea></div>
<p class="fnote">{c["consent"]}</p>
<button class="btn" type="submit"><span>{c["send"]}</span> <i aria-hidden="true">→</i></button><p class="note" role="status" aria-live="polite"></p>
</form></div></section>
'''

def footer(L, pre):
    t = T[L]; n = t["nav"]
    links = "".join(f'<a href="{fn(k)}">{n[k]}</a>' for k in PAGES[1:])
    legal = ("Legal details: Business name — Pending / VAT: — / GEMI: — / Headquarters: Patras, Greece" if L=="en" else "Νομικά στοιχεία: Επωνυμία — σε προσδιορισμό / ΑΦΜ: — / ΓΕΜΗ: — / Έδρα: Πάτρα, Ελλάδα")
    return f'''<footer class="ft"><div class="wrap"><div><span>© 2026 PG AI Solutions · {T[L]["contact"]["where_v"]}</span><small>{legal}</small></div><nav aria-label="Footer">{links}<a href="{t["privacy_href"]}">{t["privacy"]}</a><a href="terms.html">{"Terms of use" if L=="en" else "Όροι χρήσης"}</a></nav></div></footer>
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
nf = re.sub(r'<link rel="(?:canonical|alternate)"[^>]*>\n?', '', nf)
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
