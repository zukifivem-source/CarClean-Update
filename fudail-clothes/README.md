# Fudail Clothes – website

Static site (HTML, CSS, vanilla JS). No build step. Hosted on Netlify.

## Deploy on Netlify
1. New site from this repo.
2. Base directory: `fudail-clothes` · Publish directory: `fudail-clothes` · Build command: empty.
3. Forms: Netlify detects the `reserveren` and `contact` forms automatically. Set e-mail notifications under *Site configuration → Forms → Form notifications*.
4. Connect the domain and update `https://www.fudailclothes.nl` everywhere (canonical tags, `og:url`, `sitemap.xml`, `robots.txt`, JSON-LD) if the domain differs.

## Before going live (replace placeholders)
- Address, phone, WhatsApp number, e-mail, KvK number (footer, contact page, JSON-LD on `index.html` and `contact.html`)
- Opening hours (contact page, footer, JSON-LD)
- Map coordinates (contact page iframe + Google Maps link + JSON-LD `geo`)
- Reviews on the homepage (marked `VOORBEELD-REVIEWS`), use real Google reviews
- Team names and photos, product photos (the garment silhouettes are placeholders)
- Instagram and TikTok links
- Prices ("vanaf" prices on home and collecties)

## Rebrand for another client
- Colors, type scale, spacing and radii: the tokens in `:root` at the top of `css/styles.css`
- Font: `fonts/archivo-var.woff2` (self-hosted, SIL Open Font License); swap the `@font-face` to change it
- Logo: the `.wordmark` text in each page header/footer and `img/favicon.svg`
- Share image: `img/og-image.png` (1200×630)
