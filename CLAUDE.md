# Notities voor Claude: websites bouwen voor klanten

De eigenaar van deze repo bouwt websites voor lokale ondernemers en verkoopt ze. Communicatie in het Nederlands; antwoord in het Nederlands.

## Wat er in deze repo staat
- **Root (`index.html`, `diensten.html`, …):** de CarClean-site (autopoetsbedrijf). Niet aanpassen tenzij daarom gevraagd wordt.
- **`fudail-clothes/`:** voorbeeldklant Fudail Clothes (kledingwinkel, Groningen). Zelfstandige site met eigen `netlify.toml` en `README.md`.
- **`.claude/skills/`:** geïnstalleerde skills (frontend-design, ui-ux-pro-max, ui-design-system, mobile-design, seo-optimizer, code-reviewer, senior-backend, senior-fullstack, react-best-practices).
- **Nieuwe klant:** zet de site in een eigen map, bijvoorbeeld `bakkerij-jansen/`, en laat bestaande sites met rust.

## Belangrijkste regel: elke klant krijgt een eigen stijl
Kopieer **niet** de stijl van Fudail Clothes (hang-tags, dennengroen met roze, Archivo) of van CarClean. Bedenk per bedrijf een nieuwe visuele identiteit vanuit hun eigen wereld: materialen, gereedschap, taal en klanten van die branche. Een bakker, een kapper en een loodgieter moeten er totaal verschillend uitzien.

- Begin met **2 stijlrichtingen** (palet, lettertypes, sfeer, één opvallend element). Kies er één en leg uit waarom.
- Zoek een **opvallend element dat uit de branche komt**, zoals de hang-tags bij Fudail. Bedenk telkens iets nieuws.
- Vermijd standaard AI-looks: crème met terracotta, zwart met neongroen, krantenlayout, identieke afgeronde kaartjes, labels in hoofdletters boven elke kop, en pijltjes (→) achter knoppen.
- Voeg minstens één **creatief én nuttig interactief onderdeel** toe dat bij het bedrijf past. Bij Fudail waren dat een outfitbouwer, een aftelklok naar de drop en een klikbaar kledingrek. Voorbeelden van andere ideeën: een prijscalculator, een "kies je behandeling"-tool, een beschikbaarheidskiezer, een voor-na-slider.

## Lessen uit eerdere builds (wél altijd toepassen)
- **Geen uitgerekte of samengeperste letters.** Gebruik bij variabele fonts geen extreme `wdth`-waarden (de eigenaar vond dat lelijk). Haal impact uit gewicht, grootte en layout.
- **De site moet werken door op `index.html` te dubbelklikken.** Gebruik dus relatieve links (`collecties.html`, `css/styles.css`) en geen `/collecties`. Uitzondering: `404.html` houdt absolute paden, omdat Netlify die pagina op elke diepte toont.
- **Host fonts zelf.** Download ze via npm `@fontsource-variable/<font>` en zet ze in `fonts/`. Dat is sneller en vermijdt het AVG/GDPR-probleem van Google Fonts.
- **Stack:** gewone HTML, CSS en vanilla JS, zonder build-stap, gehost op Netlify. Formulieren via Netlify Forms (`data-netlify="true"` plus een honeypot). Bedankpagina op `noindex`, en blokkeer die pagina **niet** in `robots.txt`.
- **Kleuren als tokens in `:root`** in één CSS-bestand, zodat je de site voor een volgende klant makkelijk kunt omzetten.
- **Mobiel eerst:** vaste actiebalk onderaan (Bel / WhatsApp / hoofdactie), tikvlakken van minimaal 44px, hover-effecten binnen `@media (hover: hover)`, en `prefers-reduced-motion` respecteren.
- **SEO:** unieke title (max. 60 tekens) en meta description (max. 160) per pagina, gericht op "[dienst] [stad]". Verder één H1 per pagina, LocalBusiness-schema (of een subtype zoals ClothingStore) in JSON-LD, Open Graph met een PNG-afbeelding van 1200×630, `sitemap.xml` en canonical-tags.
- **Verzin geen echte gegevens.** Gebruik duidelijke placeholders (Voorbeeldstraat 12, 050 123 45 67) en markeer voorbeeldreviews in de HTML met `VOORBEELD`. Zet nooit een nep-AggregateRating in het schema.
- **Lever altijd een checklist mee** van wat de klant nog moet aanleveren: adres, telefoon, foto's, echte reviews, prijzen.

## Controleren voor oplevering
- Maak screenshots met Playwright (Chromium staat in `/opt/pw-browsers`). Test op 390px en 1440px, en ook via `file://`.
- Lighthouse: `CHROME_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome npx lighthouse@12 <url>`. Doel: 90+ in alle categorieën. Fudail haalde 98–100.
- Controleer contrast (WCAG AA), dat er geen horizontale scroll is, één H1 per pagina, labels bij alle formuliervelden en geen dode links.

## Bekende problemen in deze omgeving
- `npx claude-code-templates` kan geen skills installeren, omdat `api.github.com` geblokkeerd is. Gebruik in plaats daarvan een sparse `git clone` van `davila7/claude-code-templates`.
- Het script van `ui-ux-pro-max/scripts/search.py` crasht op Python 3.11 (f-string-fout). Pas de regels uit de skill dan handmatig toe.
- `code-reviewer/scripts/code_quality_checker.py` is een stub die altijd "0 findings" meldt. Doe de review dus zelf.
- `mobile-design/scripts/mobile_audit.py` is gemaakt voor React Native/Flutter en zegt weinig over websites.
- Google Fonts en de OpenStreetMap-kaart laden niet in de sandbox (certificaat- of 429-fout). Dat is geen fout in de site.
- Laat geen `__pycache__` achter na het draaien van skill-scripts.

## Goed startpunt voor een nieuwe klant
De eigenaar gebruikt een vaste prompt met de secties: bedrijf, pagina's, design, mobiel, SEO, techniek en oplevering. Vertaal "Book now" en "Services" naar wat bij de branche past. Bij Fudail werd dat "Reserveer & pas in de winkel" en "Collecties".
