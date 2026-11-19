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
