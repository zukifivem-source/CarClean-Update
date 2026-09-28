"""Genereert de juridische pagina's met dezelfde header en footer als de homepage.
Gebruik: python3 tools/build_legal.py  (vanuit de map hulply/)"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent / "public"
SRC = pathlib.Path(__file__).resolve().parent
MARK = '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="16" fill="#FF8A3D"/><path d="M10 40c7 0 11-4 11-10s-4-9-8-7-3 9 3 11 12 1 17-2 9-5 21-5" fill="none" stroke="#0E1116" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

PAGE = """<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title} | Hulply</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://hulply.nl/{slug}">
  <meta name="theme-color" content="#0E1116">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="styles.css">
  <script src="main.js" defer></script>
</head>
<body>
  <a class="skip" href="#main">Naar de inhoud</a>
  <header class="header scrolled">
    <div class="wrap">
      <a class="brand" href="/" aria-label="Hulply, naar de homepage">{mark}hulply</a>
      <nav class="nav" aria-label="Hoofdmenu">
        <a href="/#diensten">Diensten</a>
        <a href="/#werkwijze">Werkwijze</a>
        <a class="btn btn-primary" href="/#contact">Gratis procesScan</a>
      </nav>
    </div>
  </header>
  <main id="main" class="legal">
    <div class="wrap">
      <h1>{title}</h1>
      <p class="meta">Versie 1.0 · laatst bijgewerkt op 28 september 2026</p>
{body}
    </div>
  </main>
  <footer>
    <div class="wrap">
      <div class="foot">
        <a class="brand" href="/" aria-label="Hulply">{mark}hulply</a>
        <nav aria-label="Juridisch">
          <a href="algemene-voorwaarden.html">Algemene voorwaarden</a>
          <a href="privacy.html">Privacyverklaring</a>
          <a href="cookies.html">Cookieverklaring</a>
          <a href="disclaimer.html">Disclaimer</a>
        </nav>
      </div>
      <p class="legal-line">© 2026 Hulply · Alle rechten voorbehouden<br>[RECHTSVORM + VOLLEDIGE NAAM] · [ADRES] · KvK [KVK-NUMMER] · btw-id [BTW-ID] · <a href="tel:[TELEFOONNUMMER]">[TELEFOONNUMMER]</a> · <a href="mailto:info@hulply.nl">info@hulply.nl</a></p>
    </div>
  </footer>
</body>
</html>
"""

for src in sorted(SRC.glob("*.body.html")):
    raw = src.read_text(encoding="utf-8")
    meta = dict(re.findall(r"^<!--\s*(\w+):\s*(.*?)\s*-->$", raw, re.M))
    body = re.sub(r"^<!--.*?-->\n", "", raw, flags=re.M)
    slug = src.name.replace(".body.html", ".html")
    html = PAGE.format(title=meta["title"], desc=meta["desc"], slug=slug, mark=MARK,
                       body="\n".join("      " + l if l else l for l in body.strip().splitlines()))
    (ROOT / slug).write_text(html, encoding="utf-8")
    print("geschreven:", slug)
