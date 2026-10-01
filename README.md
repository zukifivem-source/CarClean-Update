# CarClean Midden-Groningen: website

Static website for an auto-detailing business in Hoogezand. Plain HTML, one CSS file and one small
JS file. No framework, no build step, deploys as-is on Netlify.

**Lighthouse (mobile, local test):** Performance 98–100 · Accessibility 100 · Best practices 100 · SEO 100

## Structure

```
/                     index.html               Home
/diensten/            diensten/index.html      Services, prices, price calculator
/over-ons/            over-ons/index.html      Story, values, team, process
/afspraak/            afspraak/index.html      Booking form (5 fields)
/contact/             contact/index.html       Contact form, click-to-call, WhatsApp, hours, map
/bedankt/             bedankt/index.html       Thank-you page (both forms land here)
404.html                                       Custom 404
css/style.css         The whole design system (tokens → components → sections)
js/main.js            Menu, reveal, open-now status, slider, calculator, form validation
img/icons.svg         SVG icon sprite
img/p/                Responsive WebP photos (480–1400px)
fonts/                Archivo variable font (self-hosted, OFL licence)
netlify.toml          Redirects from the old .html URLs, security headers, caching
tools/generate.py     Optional: regenerates every page from one place (see Rebranding)
```

## Deploying on Netlify

1. Connect the repo in Netlify. Leave the build command empty and set the publish directory to `.`
   (this is already in `netlify.toml`).
2. **Forms:** under *Forms*, enable form detection. The `afspraak` and `contact` forms appear after
   the first deploy. Then set up an email notification (Forms → Settings → Form notifications) to
   the client's address.
3. Spam protection is a honeypot field (`bot-field`). Netlify's spam filter (Akismet) also runs
   automatically.
4. Domain: point `carcleanmiddengroningen.nl` at Netlify and enable HTTPS.
5. After going live, submit `sitemap.xml` in Google Search Console and finish the
   Google Business Profile (same name, phone number and opening hours as on the site).

## Rebranding for a new client

1. **Colours, fonts, radius:** only section 1 of `css/style.css` (`:root` tokens). `--brand`,
   `--brand-2`, `--brand-ink` and `--brand-deep` set the whole palette. Check WCAG contrast
   for `--brand-ink` on `--brand` and `--brand-deep` on `--paper`.
2. **Font:** add the new font under a **new file name** (fonts are cached for a year) and
   update the `@font-face` block and the `<link rel="preload">` in every `<head>`. `--wide` and `--narrow`
   need a variable font with a `wdth` axis; set both to `100%` otherwise.
3. **Business data and copy:** the quickest route is `tools/generate.py`. Change the constants at
   the top (`NAME`, `PHONE`, `TEL`, `EMAIL`, `WA`, `MAPS`, `SITE`, `TOWNS`, `COORDS`, `BUSINESS`),
   adjust the copy in the page functions, then run `python3 tools/generate.py`. Header, footer,
   JSON-LD, Open Graph tags and the service-area map are then consistent everywhere.
   Without the script: find and replace in all `*.html` files.
4. **Photos:** create WebP variants from the originals (the CarClean originals are in git history,
   commit `eab5809`, and aren't deployed), for example:
   `convert photo.jpg -strip -resize 900x -quality 70 img/p/name-900.webp` (widths 480/560, 900, 1200+).
5. **Logo/favicon:** `img/logo-mark.webp`, `favicon.ico`, `img/favicon-32.png`,
   `img/apple-touch-icon.png`, `img/og-image.jpg` (1200×630).
6. Update `sitemap.xml`, `robots.txt` and the redirects in `netlify.toml`.

## Developing locally

```
python3 -m http.server 8080      # then open http://localhost:8080
```
Forms only work on Netlify (locally a POST returns a 501).
