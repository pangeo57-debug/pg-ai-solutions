# pg-ai-solutions
website for website making 

## Build and analytics

Build every generated page and the sitemap with:

```sh
python3 scripts/build.py
```

Analytics is optional and privacy-conscious. To enable GA4, set a Google Analytics 4 measurement ID when building:

```sh
PG_GA4_ID=G-XXXXXXXXXX python3 scripts/build.py
```

`GA4_MEASUREMENT_ID` is also accepted. No ID is configured by default, so no analytics script is loaded. If an ID is supplied, GA4 is loaded only after the visitor accepts the on-page analytics consent banner. IP anonymization is enabled and analytics events cover CTA, phone, email, project/service navigation, and form success/failure.

## Form protection

Set an optional Cloudflare Turnstile site key when building:

```sh
PG_TURNSTILE_SITE_KEY=0x... python3 scripts/build.py
```

The form also has a 45-second local cooldown, honeypot field, input limits and submission timeout protection. These are user-experience limits, not a substitute for server-side protection. Configure Cloudflare WAF rate limiting or the provider's server-side submission limits for real IP-based abuse protection.

## Automated handover

Every push to `main` and every pull request runs the build, SEO validator and client ZIP packaging workflow.

Create the package locally:

```sh
python3 scripts/package_handover.py
```

The resulting file is `dist/pg-ai-solutions-client-handover.zip`.
