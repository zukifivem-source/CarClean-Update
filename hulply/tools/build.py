"""Bouwt alle pagina's van hulply.nl met dezelfde header en footer.

Gebruik (vanuit de map hulply/):  python3 tools/build.py
Bronnen staan in tools/pages/*.html en beginnen met regels als:
  <!-- title: ... -->      paginatitel
  <!-- desc: ... -->       meta-omschrijving
  <!-- nav: diensten -->   actief menu-item (home, diensten, werkwijze, over, vragen, contact, legal)
  <!-- layout: legal -->   optioneel: juridische pagina (kop + leesbreedte + tabjes)
"""
import pathlib, re

TOOLS = pathlib.Path(__file__).resolve().parent
PUBLIC = TOOLS.parent / "public"
SITE = "https://hulply.nl/"

MARK = ('<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#16181D"/>'
        '<path d="M11 39c6.5 0 10.5-3.8 10.5-9.4 0-4.6-3.6-7.6-7.2-6.1-3.8 1.6-2.4 8.5 3.1 10.4 5.2 1.8 11.4.4 16-2.4 '
        '4.6-2.8 8.6-4.3 19.6-4.3" fill="none" stroke="#F6F4EF" stroke-width="4.2" stroke-linecap="round" '
        'stroke-linejoin="round"/><circle cx="53" cy="27.2" r="3.6" fill="#C9521D"/></svg>')
MARK_DARK = MARK.replace('fill="#16181D"', 'fill="#F6F4EF"', 1).replace('stroke="#F6F4EF"', 'stroke="#16181D"')

NAV = [("diensten", "diensten.html", "Diensten"), ("werkwijze", "werkwijze.html", "Werkwijze"),
       ("over", "over-ons.html", "Over ons"), ("vragen", "veelgestelde-vragen.html", "Vragen")]
LEGAL = [("algemene-voorwaarden.html", "Algemene voorwaarden"), ("privacy.html", "Privacyverklaring"),
         ("cookies.html", "Cookieverklaring"), ("disclaimer.html", "Disclaimer")]
CUR = ' aria-current="page"'
ARROW = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>')

PAGE = """<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  {canonical}
  <meta name="theme-color" content="#F6F4EF">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="nl_NL">
  <meta property="og:site_name" content="Hulply">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{site}assets/og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preload" href="assets/fonts/newsreader-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="styles.css">
  <script src="main.js" defer></script>
</head>
<body>
  <a class="skip" href="#main">Naar de inhoud</a>
  <header class="header">
    <div class="wrap">
      <a class="brand" href="index.html" aria-label="Hulply, naar de homepage">{mark}hulply</a>
      <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span></button>
      <nav class="nav" id="menu" aria-label="Hoofdmenu">
{nav}
        <a class="btn btn-primary" href="contact.html"{contact_current}>Plan een kennismaking</a>
      </nav>
    </div>
  </header>
  <main id="main">
{main}
  </main>
  <footer class="footer">
    <div class="wrap">
      <div class="foot-grid">
        <div>
          <a class="brand" href="index.html" aria-label="Hulply">{mark_dark}hulply</a>
          <p>Procesoptimalisatie en automatisering voor het mkb. Minder handwerk, meer ruimte voor wat telt.</p>
        </div>
        <div>
          <h4>Hulply</h4>
          <ul>
            <li><a href="diensten.html">Diensten</a></li>
            <li><a href="werkwijze.html">Werkwijze</a></li>
            <li><a href="over-ons.html">Over ons</a></li>
            <li><a href="veelgestelde-vragen.html">Veelgestelde vragen</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4>Juridisch</h4>
          <ul>
{legal_links}
          </ul>
        </div>
        <div>
          <h4>Contact</h4>
          <ul>
            <li><a href="mailto:info@hulply.nl">info@hulply.nl</a></li>
            <li><a href="tel:[TELEFOONNUMMER]">[TELEFOONNUMMER]</a></li>
            <li>[ADRES]</li>
          </ul>
        </div>
      </div>
      <div class="foot-bottom">
        <span>© 2026 Hulply. Alle rechten voorbehouden.</span>
        <span>[RECHTSVORM + VOLLEDIGE NAAM] · KvK [KVK-NUMMER] · btw-id [BTW-ID]</span>
      </div>
    </div>
  </footer>
</body>
</html>
"""

LEGAL_WRAP = """    <section class="page-hero">
      <div class="wrap">
        <p class="crumbs"><a href="index.html">Home</a> / Juridisch</p>
        <h1 class="display">{title}</h1>
        <nav class="legal-nav" aria-label="Juridische documenten">
{tabs}
        </nav>
      </div>
    </section>
    <section class="section tight">
      <div class="wrap">
        <div class="legal">
          <p class="meta">Versie 1.0 · laatst bijgewerkt op 28 september 2026</p>
{body}
        </div>
      </div>
    </section>"""


def indent(text, n):
    return "\n".join((" " * n + l) if l.strip() else "" for l in text.strip("\n").splitlines())


def build():
    for src in sorted((TOOLS / "pages").glob("*.html")):
        raw = src.read_text(encoding="utf-8")
        meta = dict(re.findall(r"^<!--\s*(\w+):\s*(.*?)\s*-->$", raw, re.M))
        body = re.sub(r"^<!--\s*\w+:.*?-->\n", "", raw, flags=re.M)
        name = src.name
        active = meta.get("nav", "")
        if meta.get("layout") == "legal":
            tabs = "\n".join(
                f'          <a href="{h}"{CUR if h == name else ""}>{t}</a>' for h, t in LEGAL)
            main = LEGAL_WRAP.format(title=meta["title"], tabs=tabs, body=indent(body, 10))
        else:
            main = indent(body, 4)
        nav = "\n".join(
            f'        <a href="{h}"{CUR if k == active else ""}>{t}</a>' for k, h, t in NAV)
        legal_links = "\n".join(f'            <li><a href="{h}">{t}</a></li>' for h, t in LEGAL)
        url = SITE if name == "index.html" else SITE + name
        title = meta["title"] if name == "index.html" else f'{meta["title"]} | Hulply'
        canonical = ('<meta name="robots" content="noindex">' if name == "404.html"
                     else f'<link rel="canonical" href="{url}">')
        html = PAGE.format(title=title, og_title=meta.get("og", meta["title"]), desc=meta["desc"], url=url,
                           site=SITE, canonical=canonical, mark=MARK, mark_dark=MARK_DARK, nav=nav,
                           contact_current=' aria-current="page"' if active == "contact" else "",
                           main=main.replace("{{ARROW}}", ARROW), legal_links=legal_links)
        (PUBLIC / name).write_text(html, encoding="utf-8")
        print("geschreven:", name)


if __name__ == "__main__":
    build()
