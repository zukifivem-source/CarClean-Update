# Hulply — website (hulply.nl)

Statische website, zonder build-stap. Alles wat online moet staat in `public/`.

```
public/            ← dit is de website (uploaden / koppelen aan hosting)
  index.html         homepage met scroll-film
  algemene-voorwaarden.html, privacy.html, cookies.html, disclaimer.html, 404.html
  styles.css, main.js
  assets/            logo, favicon, fonts (lokaal, geen Google), film + posters, og.jpg
  _headers           beveiligingsheaders (Cloudflare Pages / Netlify)
tools/             ← bronbestanden, niet online zetten
  *.body.html        teksten van de juridische pagina's
  build_legal.py     zet de juridische pagina's om naar public/ (python3 tools/build_legal.py)
  og.html, icon.html bron van de deelafbeelding en het app-icoon
```

## Vóór livegang invullen (verplicht)

Zoek in `public/` en `tools/` naar deze plaatshouders en vervang ze overal:

| Plaatshouder | Wat |
|---|---|
| `[RECHTSVORM + VOLLEDIGE NAAM]` | bv. "Hulply V.O.F." of de namen bij een eenmanszaak, precies zoals bij de KVK |
| `[ADRES]` | vestigingsadres zoals ingeschreven bij de KVK |
| `[KVK-NUMMER]` | KVK-nummer |
| `[BTW-ID]` | btw-identificatienummer (niet het omzetbelastingnummer) |
| `[TELEFOONNUMMER]` | telefoonnummer (ook in `href="tel:..."`) |

Controleer ook:
- `info@hulply.nl`: bestaat dit mailadres? Het contactformulier stuurt daarheen.
- Algemene voorwaarden art. 10: aansprakelijkheid is gemaximeerd op € 10.000 per gebeurtenis / € 25.000 per jaar. Pas aan naar wens of naar je verzekering.
- Na het aanpassen van teksten in `tools/*.body.html`: `python3 tools/build_legal.py`.

> Deze juridische teksten zijn een zorgvuldige basis, maar geen juridisch advies. Laat ze bij voorkeur één keer nalezen door een jurist, zeker als jullie een beroepsaansprakelijkheidsverzekering afsluiten. Stuur de algemene voorwaarden altijd mee met je offertes (als pdf) en verwijs ernaar in de offerte, anders kun je er later lastiger een beroep op doen.

## Online zetten op hulply.nl (Cloudflare Pages, gratis)

1. Maak een account op cloudflare.com → **Workers & Pages** → **Create** → **Pages**.
2. Koppel de GitHub-repository, of kies **Upload assets** en sleep de map `public/` erin.
   - Bij koppelen: *Build command* leeg laten, *Build output directory* = `hulply/public`.
3. Ga naar **Custom domains** → voeg `hulply.nl` en `www.hulply.nl` toe en volg de DNS-stappen
   (nameservers naar Cloudflare verhuizen, of een CNAME bij je huidige domeinregistrar).

Netlify of Vercel werken ook: publiceer de map `public/`.

## Contactformulier

Het formulier opent nu het e-mailprogramma van de bezoeker met een ingevuld bericht (er worden geen gegevens op de website opgeslagen).
Wil je dat aanvragen direct binnenkomen zonder mailprogramma, koppel dan later een formulierdienst (bv. Formspree of Cloudflare Pages Functions) en werk de privacyverklaring bij.
