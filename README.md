# United Citizen Law — Website

The public marketing website for **United Citizen Law** (uclaw.net), a Sacramento personal-injury firm. Multilingual, conversion-optimized, WCAG-AA, and built for maximum SEO/AEO. Static HTML — no build step. Built by **Apex Growth Corp**.

## Pages

| URL | File | What it is |
|---|---|---|
| `/` | `index.html` | Homepage — founder-story hero, case-review wizard, 5-language switching, clickable team bios |
| `/car-accident-lawyer-sacramento.html` | practice page | Car accidents |
| `/truck-accident-lawyer-sacramento.html` | practice page | Truck accidents |
| `/motorcycle-accident-lawyer-sacramento.html` | practice page | Motorcycle accidents |
| `/rideshare-accident-lawyer-sacramento.html` | practice page | Uber / Lyft accidents |
| `/pedestrian-accident-lawyer-sacramento.html` | practice page | Pedestrian accidents |
| `/dog-bite-lawyer-sacramento.html` | practice page | Dog bites |
| `/slip-and-fall-lawyer-sacramento.html` | practice page | Slip & fall / premises |
| `/wrongful-death-lawyer-sacramento.html` | practice page | Wrongful death |
| `/team.html` | team page | Full 9-person team with bios, languages, direct extensions |

Each page carries a single `<h1>`, LegalService + Service + FAQPage + BreadcrumbList schema, a canonical that matches its served URL, and a free-consultation CTA.

## Deploy (Vercel)

This is a **static site with no build command**.

1. Import this repo into Vercel.
2. Framework preset: **Other**. Build command: *(none)*. Output directory: *(leave blank / root)*.
3. Deploy. `index.html` serves at `/`; every other page resolves by its `.html` path.

`vercel.json` adds security headers (HSTS, nosniff, frame-options, referrer-policy) and long-cache immutable headers for `/team/` images. `robots.txt` welcomes AI answer engines (GPTBot, PerplexityBot, ClaudeBot, Google-Extended) and points to `sitemap.xml`.

## Before going live on uclaw.net

- In `index.html`, set `FORM_ENDPOINT` (Formspree or the CRM webhook) and flip `PREVIEW_MODE = false`.
- Verify the Google review count and map pin before shipping the schema.
- Dari / Urdu / Arabic copy is a conversion layer — have a native speaker review before production.

## Regenerate practice + team pages

The 8 practice pages and `team.html` are generated:

```bash
python3 _generate.py
```

Edit copy, team members, or schema in `_generate.py`, then re-run. `index.html` is hand-authored and not generated.

---

*Attorney advertising. Past results do not guarantee future outcomes.*
