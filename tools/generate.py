#!/usr/bin/env python3
"""Optional page generator for the CarClean site.

The site is plain static HTML and needs no build step. This script only exists to
make rebranding fast: change the constants and copy below, run
`python3 tools/generate.py`, and all pages are rewritten with a consistent
header, footer, schema and contact details. If you edit the HTML by hand
instead, do not run this script afterwards (it overwrites the pages).
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://carcleanmiddengroningen.nl"
NAME = "CarClean Midden-Groningen"
PHONE = "0598 744 299"
TEL = "+31598744299"
EMAIL = "info@carcleanmiddengroningen.nl"
WA = "https://wa.me/31598744299?text=Hoi%20CarClean%2C%20ik%20wil%20graag%20een%20afspraak%20maken."
MAPS = "https://www.google.com/maps/search/?api=1&query=CarClean+Midden-Groningen+Hoogezand"
TOWNS = ["Hoogezand", "Sappemeer", "Foxhol", "Kropswolde", "Slochteren", "Zuidbroek", "Muntendam",
         "Veendam", "Scheemda", "Winschoten", "Delfzijl", "Stadskanaal", "Groningen", "Zuidlaren", "Assen", "Emmen"]


def eur(n):
    """Dutch price format: 1089 -> 1.089, 14.95 -> 14,95, 544.5 -> 544,50."""
    whole, cents = f"{n:,.2f}".split(".")
    whole = whole.replace(",", ".")
    return whole if cents == "00" else f"{whole},{cents}"


def i(name, cls=""):
    c = f' class="i {cls}"' if cls else ' class="i"'
    return f'<svg{c} aria-hidden="true" focusable="false"><use href="#i-{name}"></use></svg>'


ARROW = i("arrow", "icon-arrow")
AC = ' aria-current="page"'


def pic(name, widths, alt, sizes, cls="", eager=False, w=None, h=None):
    srcset = ", ".join(f"/img/p/{name}-{x}.webp {x}w" for x in widths)
    mid = widths[1] if len(widths) > 1 else widths[0]
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    dims = f' width="{w}" height="{h}"' if w else ""
    return (f'<img{c} src="/img/p/{name}-{mid}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{alt}"{dims} {load}>')


# Image intrinsic sizes (at the 560w variant ratio)
DIM = {"lambo": (1356, 1695), "bmw": (1400, 1050), "gklasse": (1200, 1600), "mercedes": (1024, 793),
       "porsche-wide": (1080, 864), "lexus-wide": (1080, 864), "gklasse-wide": (1080, 864)}
W = {"lambo": [560, 900, 1356], "bmw": [480, 900, 1400],
     "porsche-wide": [480, 800, 1080], "lexus-wide": [480, 800, 1080], "gklasse-wide": [480, 800, 1080], "gklasse": [560, 900, 1200],
     "mercedes": [480, 1024]}


def P(name, alt, sizes, cls="", eager=False):
    w, h = DIM[name]
    return pic(name, W[name], alt, sizes, cls, eager, w, h)


NAV = [("/", "Home"), ("/diensten/", "Diensten & prijzen"), ("/over-ons/", "Over ons"), ("/contact/", "Contact")]

BUSINESS = {
    "@type": "AutoWash",
    "@id": SITE + "/#business",
    "name": NAME,
    "alternateName": ["CarClean Hoogezand", "CarClean Groningen"],
    "description": "Autopoetsbedrijf voor auto poetsen, detailing, ceramische coating en reconditionering in Hoogezand en heel Midden-Groningen. Voor particulieren, dealers, leasemaatschappijen en wagenparken.",
    "slogan": "Dé nummer 1 in het reconditioneren van voertuigen",
    "url": SITE + "/",
    "logo": SITE + "/img/Carclean.png",
    "image": [SITE + "/img/og-image.jpg", SITE + "/img/p/lambo-1356.webp"],
    "telephone": TEL,
    "email": EMAIL,
    "priceRange": "€10 - €1089",
    "currenciesAccepted": "EUR",
    "paymentAccepted": "Pin, contant, factuur",
    "address": {"@type": "PostalAddress", "addressLocality": "Hoogezand", "addressRegion": "Groningen", "addressCountry": "NL"},
    "geo": {"@type": "GeoCoordinates", "latitude": 53.1617, "longitude": 6.7614},
    "hasMap": MAPS,
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "08:00", "closes": "17:00"}],
    "areaServed": [{"@type": "City", "name": t} for t in TOWNS],
    "parentOrganization": {"@type": "Organization", "name": "BeBlitz High-End Car Detailing", "url": "https://www.beblitz.nl"},
    "contactPoint": [{"@type": "ContactPoint", "telephone": TEL, "contactType": "customer service",
                      "areaServed": "NL", "availableLanguage": ["nl", "en"]}],
    "makesOffer": [
        {"@type": "Offer", "name": n, "price": p, "priceCurrency": "EUR",
         "priceSpecification": {"@type": "PriceSpecification", "price": p, "priceCurrency": "EUR", "minPrice": p, "valueAddedTaxIncluded": False},
         "itemOffered": {"@type": "Service", "name": n, "areaServed": "Midden-Groningen"}}
        for n, p in [("Basic Wash handwas", 14.95), ("Complete Beurt binnen en buiten", 29.95),
                     ("Premium Detail", 79.95), ("Detailing interieur", 453), ("Detailing exterieur met waxcoating", 665),
                     ("Ceramische coating", 1089), ("Wasstraat Brons", 10.00), ("Wasstraat Diamant", 19.50)]
    ],
}


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def breadcrumb(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "name": name, "item": SITE + url} for n, (url, name) in enumerate(items)]}


def head(title, desc, path, extra_ld=None, preload_hero=False, noindex=False):
    url = SITE + path
    ld = [BUSINESS] if path == "/" else [{"@type": "AutoWash", "@id": SITE + "/#business", "name": NAME, "url": SITE + "/", "telephone": TEL}]
    ld.append({"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME, "inLanguage": "nl-NL",
               "publisher": {"@id": SITE + "/#business"}} if path == "/" else
              {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
               "inLanguage": "nl-NL", "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#business"}})
    if extra_ld:
        ld.extend(extra_ld)
    graph = {"@context": "https://schema.org", "@graph": ld}
    hero_preload = ('<link rel="preload" as="image" href="/img/p/lambo-900.webp" '
                    'imagesrcset="/img/p/lambo-560.webp 560w, /img/p/lambo-900.webp 900w, /img/p/lambo-1356.webp 1356w" '
                    'imagesizes="(min-width: 960px) 40vw, 100vw" fetchpriority="high">\n') if preload_hero else ""
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    canon = "" if noindex else f'<link rel="canonical" href="{url}">\n'
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
{canon}<meta name="theme-color" content="#07090c">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Logo van CarClean Midden-Groningen naast een gepoetste zwarte sportwagen in de studio">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
{hero_preload}<link rel="stylesheet" href="/css/style.css">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<script src="/js/main.js" defer></script>
{jsonld(graph)}
</head>
"""


def header(active):
    links = "\n".join(
        f'        <li><a href="{u}"{AC if u == active else ""}>{t}</a></li>' for u, t in NAV)
    mlinks = "\n".join(
        f'      <li><a href="{u}"{AC if u == active else ""}>{t} {ARROW}</a></li>' for u, t in NAV)
    return f"""<body>
<a class="skip-link" href="#main">Naar de inhoud</a>
<header class="header" data-header>
  <div class="container header__inner">
    <a class="brand" href="/">
      <img src="/img/logo-mark.webp" alt="" width="148" height="96">
      <span class="brand__text"><span class="brand__name">CarClean</span><span class="brand__sub">Midden-Groningen</span></span>
    </a>
    <nav class="nav" aria-label="Hoofdmenu">
      <ul>
{links}
      </ul>
    </nav>
    <div class="header__actions">
      <a class="btn btn--ghost btn--sm header__phone" href="tel:{TEL}">{i("phone")} {PHONE}</a>
      <a class="btn btn--primary btn--sm" href="/afspraak/">Plan je beurt</a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" data-menu-toggle>
        <span></span><span class="visually-hidden">Menu</span>
      </button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" data-menu>
  <nav aria-label="Mobiel menu">
    <ul>
{mlinks}
      <li><a href="/afspraak/"{AC if active == "/afspraak/" else ""}>Afspraak maken {ARROW}</a></li>
    </ul>
  </nav>
  <div class="btn-row">
    <a class="btn btn--primary btn--block" href="tel:{TEL}">{i("phone")} Bel {PHONE}</a>
    <a class="btn btn--ghost btn--block" href="{WA}" target="_blank" rel="noopener">{i("whatsapp")} WhatsApp ons</a>
  </div>
  <div class="mobile-menu__meta">
    <span class="open-status" data-open-status><span class="dot"></span><span data-open-text>Ma–vr 08:00–17:00</span></span>
    <span>Hoogezand · heel Midden-Groningen · 24/7 voor zakelijke klanten</span>
  </div>
</div>
<main id="main">
"""


def footer():
    return f"""</main>
<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="brand" href="/">
          <img src="/img/logo-mark.webp" alt="" width="148" height="96" loading="lazy">
          <span class="brand__text"><span class="brand__name">CarClean</span><span class="brand__sub">Midden-Groningen</span></span>
        </a>
        <p>Het autopoetsbedrijf van Groningen. Dochter van <a class="link" href="https://www.beblitz.nl" target="_blank" rel="noopener">BeBlitz High-End Car Detailing</a>. 24/7 bereikbaar voor zakelijke klanten, met eigen transport, leenauto's en poetsen op locatie.</p>
        <p class="open-status mt-5" data-open-status><span class="dot"></span><span data-open-text>Ma–vr 08:00–17:00</span></p>
      </div>
      <div>
        <h2>Diensten</h2>
        <ul>
          <li><a href="/diensten/#particulier">Handwas &amp; poetsen</a></li>
          <li><a href="/diensten/#detailing">Auto detailing</a></li>
          <li><a href="/diensten/#coating">Ceramische coating</a></li>
          <li><a href="/diensten/#wasstraat">Wasstraat</a></li>
          <li><a href="/diensten/#zakelijk">Dealers &amp; wagenparken</a></li>
          <li><a href="/diensten/#haal-en-breng">Haal &amp; breng</a></li>
        </ul>
      </div>
      <div>
        <h2>CarClean</h2>
        <ul>
          <li><a href="/over-ons/">Over ons</a></li>
          <li><a href="/afspraak/">Afspraak maken</a></li>
          <li><a href="/contact/">Contact &amp; route</a></li>
          <li><a href="/diensten/#calculator">Prijscalculator</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="tel:{TEL}">{PHONE}</a></li>
          <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL.replace("@", "@<wbr>")}</a></li>
          <li><a href="{MAPS}" target="_blank" rel="noopener">Hoogezand, Groningen</a></li>
        </ul>
      </div>
    </div>
    <p class="footer__big" aria-hidden="true">CARCLEAN</p>
    <div class="footer__bottom">
      <span>© <span data-year>2026</span> {NAME}. Alle rechten voorbehouden.</span>
      <span>Auto poetsen in Hoogezand, Sappemeer, Veendam, Groningen &amp; omgeving</span>
    </div>
  </div>
</footer>
<nav class="actionbar" aria-label="Snel contact">
  <a href="tel:{TEL}">{i("phone")} Bel</a>
  <a href="{WA}" target="_blank" rel="noopener">{i("whatsapp")} WhatsApp</a>
  <a class="is-primary" href="/afspraak/">{i("calendar")} Plan je beurt</a>
</nav>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Stuur ons een WhatsApp-bericht">{i("whatsapp")}</a>
</body>
</html>
"""


def page_hero(crumbs, eyebrow, h1, lead, extra=""):
    bc = "".join(
        f'<li><a href="{u}">{n}</a></li>' if k < len(crumbs) - 1 else f'<li aria-current="page">{n}</li>'
        for k, (u, n) in enumerate(crumbs))
    return f"""<section class="page-hero">
  <div class="hero__bg" aria-hidden="true"></div>
  <div class="container page-hero__inner">
    <nav class="breadcrumbs" aria-label="Kruimelpad"><ol>{bc}</ol></nav>
    <span class="eyebrow">{eyebrow}</span>
    <h1><span class="sheen">{h1}</span></h1>
    <p class="lead">{lead}</p>
    {extra}
  </div>
</section>
"""


def cta_band(title="Klaar voor showroomglans?", text="Plan online in een minuut, of bel en je staat er vandaag nog in."):
    return f"""<section class="section section--tight">
  <div class="container">
    <div class="cta-band reveal">
      <div class="cta-band__inner">
        <div class="stack">
          <span class="eyebrow">Plan je beurt</span>
          <h2>{title}</h2>
          <p class="lead">{text}</p>
        </div>
        <div class="btn-row">
          <a class="btn btn--primary btn--lg" href="/afspraak/">Afspraak maken {ARROW}</a>
          <a class="btn btn--ghost btn--lg" href="tel:{TEL}">{i("phone")} {PHONE}</a>
        </div>
      </div>
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------- map
COORDS = {"Hoogezand": (53.1617, 6.7614), "Sappemeer": (53.163, 6.795), "Foxhol": (53.170, 6.716),
          "Groningen": (53.219, 6.567), "Veendam": (53.106, 6.879), "Zuidbroek": (53.165, 6.861),
          "Slochteren": (53.207, 6.805), "Scheemda": (53.173, 6.966), "Winschoten": (53.144, 7.034),
          "Delfzijl": (53.330, 6.919), "Stadskanaal": (52.990, 6.950), "Zuidlaren": (53.093, 6.682),
          "Assen": (52.993, 6.562), "Emmen": (52.785, 6.897)}


def xy(name):
    lat, lon = COORDS[name]
    return round(280 + (lon - 6.7614) * 480), round(275 + (53.1617 - lat) * 790)


def service_map():
    roads = [["Groningen", "Foxhol", "Hoogezand", "Sappemeer", "Zuidbroek", "Scheemda", "Winschoten"],
             ["Zuidbroek", "Veendam", "Stadskanaal", "Emmen"], ["Groningen", "Zuidlaren", "Assen"],
             ["Groningen", "Slochteren", "Delfzijl"], ["Hoogezand", "Zuidlaren"]]
    rd = "".join('<polyline class="road" points="' + " ".join(f"{xy(t)[0]},{xy(t)[1]}" for t in r) + '"/>' for r in roads)
    hx, hy = xy("Hoogezand")
    rings = "".join(f'<circle class="ring{" ring--1" if n == 0 else ""}" cx="{hx}" cy="{hy}" r="{r}"/>' for n, r in enumerate([90, 180, 270]))
    LBL = {"Groningen": ("end", -12, 6), "Slochteren": ("middle", 0, -14), "Delfzijl": ("start", 12, 6),
           "Zuidbroek": ("middle", -4, -14), "Scheemda": ("start", 10, -12), "Winschoten": ("start", 12, 16),
           "Veendam": ("start", 12, 7), "Stadskanaal": ("start", 12, 7), "Zuidlaren": ("end", -12, 7),
           "Assen": ("end", -12, 7), "Emmen": ("start", 12, 7)}
    towns = ""
    for t, (anchor, dx, dy) in LBL.items():
        x, y = xy(t)
        towns += f'<g class="town"><circle cx="{x}" cy="{y}" r="5"/><text x="{x + dx}" y="{y + dy}" text-anchor="{anchor}">{t}</text></g>'
    hq = (f'<circle class="pulse" cx="{hx}" cy="{hy}" r="10"/>'
          f'<g class="town town--hq"><circle cx="{hx}" cy="{hy}" r="9"/><text x="{hx - 18}" y="{hy + 8}" text-anchor="end">Hoogezand</text></g>')
    return f"""<div class="map reveal">
  <svg viewBox="60 105 515 500" role="img" aria-labelledby="map-title">
    <title id="map-title">Kaart van het werkgebied: vanuit Hoogezand rijden we naar o.a. Groningen, Veendam, Winschoten, Delfzijl, Stadskanaal, Assen en Emmen</title>
    {rings}{rd}{towns}{hq}
  </svg>
  <div class="map__cta">
    <span class="chip">{i("truck")} Haal &amp; breng in de hele regio</span>
    <a class="btn btn--primary btn--sm" href="{MAPS}" target="_blank" rel="noopener">{i("pin")} Open in Google Maps</a>
  </div>
</div>"""


def area_section(heading_tag="h2"):
    chips = "".join(f'<li class="chip">{t}</li>' for t in TOWNS)
    return f"""<section class="section surface-dark-2" aria-labelledby="regio-title">
  <div class="container area">
    <div class="stack reveal">
      <span class="eyebrow">Werkgebied</span>
      <{heading_tag} id="regio-title" class="h2">Vanuit Hoogezand. Voor heel Groningen &amp; Drenthe.</{heading_tag}>
      <p class="lead">Je komt naar ons toe, wij komen naar jou, of we halen je auto op met de trailer. Midden-Groningen is onze thuisbasis, en we rijden net zo makkelijk naar de stad, de Veenkoloniën of Drenthe.</p>
      <ul class="towns" role="list">{chips}</ul>
      <p class="muted mt-4">Woon je net buiten deze lijst? <a class="link" href="/contact/">Vraag het gewoon</a>: we zeggen zelden nee.</p>
    </div>
    {service_map()}
  </div>
</section>
"""


def stars():
    return '<div class="review__stars" role="img" aria-label="5 van 5 sterren">' + i("star") * 5 + "</div>"


# Reviews: PLACEHOLDERS copied from the previous site; replace with real Google reviews before launch.
REVIEWS = [
    ("Mijn auto ziet er weer als nieuw uit. Snel geholpen, vriendelijk contact en een uitstekend resultaat. Zeker voor herhaling vatbaar!", "R. de Vries", "Particulier · Hoogezand", "RV"),
    ("Als dealer hebben wij regelmatig voertuigen klaar nodig. CarClean levert altijd op tijd en de kwaliteit is consistent goed. Een betrouwbare partner.", "J. Postma", "Autodealer · Sappemeer", "JP"),
    ("Via de haal &amp; breng service geen enkel gedoe. Auto werd opgehaald en schoon teruggebracht terwijl ik gewoon aan het werk was. Aanrader!", "M. Bakker", "Particulier · Veendam", "MB"),
]


def reviews_section():
    cards = ""
    for n, (q, who, meta, ini) in enumerate(REVIEWS):
        cards += f"""<figure class="card review reveal" data-delay="{n * 90}">
        {stars()}
        <blockquote><p>“{q}”</p></blockquote>
        <figcaption><span class="avatar" aria-hidden="true">{ini}</span><div><strong>{who}</strong><span>{meta}</span></div></figcaption>
      </figure>"""
    return f"""<section class="section surface-light" aria-labelledby="reviews-title">
  <!-- PLACEHOLDER-REVIEWS: vervang door echte Google-reviews (naam + plaats, met toestemming) vóór livegang. -->
  <div class="container">
    <div class="section-head section-head--split">
      <div class="stack reveal"><span class="eyebrow">Klanten aan het woord</span><h2 id="reviews-title">Wat klanten zeggen.</h2></div>
      <p class="lead reveal">Particulieren en dealers kiezen ons om dezelfde reden: het resultaat klopt, elke keer, zonder dat ze erachteraan hoeven te zitten.</p>
    </div>
    <div class="reviews">{cards}</div>
  </div>
</section>
"""


def gallery(tag="h2"):
    W2 = "(min-width: 800px) 50vw, 100vw"
    T = "(min-width: 800px) 25vw, 50vw"
    items = [("bmw", "Glascoating op een BMW i8, vleugeldeuren open", "Glascoating · BMW i8", W2),
             ("lambo", "Zwarte Lamborghini in de detailingstudio na een complete exterieurbehandeling", "Exterieur detailing", T),
             ("lexus-wide", "Gereinigd en gevoed leren interieur van een Lexus LC", "Interieur detailing · Lexus", T),
             ("porsche-wide", "Gepoetste Porsche 911 Cabriolet op de oprit", "Polish &amp; finish · Porsche 911", T),
             ("gklasse-wide", "Mercedes G-Klasse showroomklaar onder studiolicht", "Showroomklaar voor dealer", "(min-width: 800px) 50vw, 50vw"),
             ("mercedes", "Mercedes-AMG S-Klasse Cabriolet na een premium handwas", "Premium handwas · AMG", "(min-width: 800px) 50vw, 50vw")]
    figs = "".join(f'<figure class="reveal" data-delay="{n * 60}">{P(k, alt, sz)}<figcaption>{cap}</figcaption></figure>'
                   for n, (k, alt, cap, sz) in enumerate(items))
    return f"""<section class="section" aria-labelledby="werk-title">
  <div class="container">
    <div class="section-head section-head--split">
      <div class="stack reveal"><span class="eyebrow">Ons werk</span><{tag} id="werk-title" class="h2">Resultaat dat voor zich spreekt.</{tag}></div>
      <p class="lead reveal">Een greep uit recente klussen: van een glascoating op een i8 tot een dealer-G-Klasse die dezelfde middag de showroom in ging.</p>
    </div>
    <div class="bento">{figs}</div>
  </div>
</section>
"""


def _sprite():
    """Inline the icon sprite so icons also work when a page is opened straight from disk."""
    import re
    svg = open(os.path.join(ROOT, "img", "icons.svg"), encoding="utf-8").read()
    body = re.sub(r"<!--.*?-->", "", svg.split(">", 1)[1].rsplit("</svg>", 1)[0], flags=re.S)
    body = body.replace('<symbol id="', '<symbol id="i-')
    return '<svg xmlns="http://www.w3.org/2000/svg" class="sprite" width="0" height="0" aria-hidden="true" focusable="false">' + " ".join(body.split()) + "</svg>"


SPRITE = None


def relativize(html, depth):
    """Turn root paths (/css/...) into relative ones (../css/...) so pages work from disk too.
    Absolute URLs (https://...), canonical/og tags and the Netlify form action stay untouched."""
    import re
    p = "../" * depth
    home = p or "./"
    html = re.sub(r'(href|src)="/(?=["#?])', lambda m: f'{m.group(1)}="{home}', html)
    html = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{p}', html)
    html = re.sub(r'((?:image)?srcset)="([^"]*)"', lambda m: m.group(1) + '="' + re.sub(r'(^|,\s*)/', lambda n: n.group(1) + p, m.group(2)) + '"', html)
    return html


def write(path, html):
    global SPRITE
    if SPRITE is None:
        SPRITE = _sprite()
    html = html.replace("<body>\n", "<body>\n" + SPRITE + "\n", 1)
    if path != "404.html":  # Netlify serves 404.html at any depth, so it keeps root paths
        html = relativize(html, path.count("/"))
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path, len(html))


# ================================================================ HOME
def home():
    tiles = [
        ("porsche-wide", "01", "Handwas &amp; poetsen", "Met de hand gewassen, binnen gezogen, ruiten streeploos. Voor elke week of elk seizoen.", "14,95", "/diensten/#particulier", "Gepoetste zwarte Porsche 911 Cabriolet"),
        ("lexus-wide", "02", "Auto detailing", "Dieptereiniging van interieur en lak. Vlekken, geurtjes en swirls verdwijnen echt.", "453", "/diensten/#detailing", "Cognac leren interieur van een Lexus na interieur detailing"),
        ("bmw", "03", "Ceramische coating", "Twee lagen keramische bescherming: jarenlang diepe glans, water parelt er gewoon af.", "1.089", "/diensten/#coating", "BMW i8 met verse ceramische coating"),
        ("gklasse-wide", "04", "Dealers &amp; wagenparken", "Recon, showroomklaar en foto-klaar. Snelle doorloop, vaste tarieven, 24/7 bereikbaar.", None, "/diensten/#zakelijk", "Mercedes G-Klasse showroomklaar gemaakt voor een dealer"),
    ]
    tile_html = ""
    for n, (img, num, t, p, price, href, alt) in enumerate(tiles):
        pr = (f'<p class="price"><span class="price__from">v.a.</span><span class="price__amount">€{price}</span></p>'
              if price else '<p class="price"><span class="price__amount">Op offerte</span></p>')
        tile_html += f"""<a class="tile reveal" data-delay="{n * 80}" href="{href}">
        <div class="tile__img">{P(img, alt, "(min-width: 1100px) 700px, (min-width: 700px) 50vw, 100vw")}</div>
        <div class="tile__top"><span class="tile__num">{num}</span><span class="tile__go">{i("arrow")}</span></div>
        <h3>{t}</h3>
        <p>{p}</p>
        {pr}
      </a>"""
    features = [
        ("repeat", "24/7 bereikbaar", "Brandschade, incident in de parkeergarage of spoed vanuit de zaak? We sturen direct transport en lossen het waar mogelijk dezelfde dag op."),
        ("zap", "Snelle doorloop", "Geen wachtrijen. Doorstroom is jouw grootste asset, dus jouw voertuigen staan snel weer glanzend in de showroom."),
        ("camera", "AI-fotostudio", "Eigen fotoruimte met AI-achtergronden: direct showroomklare beelden voor je website, marketplace en advertenties."),
        ("wrench", "Partnernetwerk", "Spot-repair, deukherstel, restyling en APK via vaste partners. Eén aanspreekpunt, volledig ontzorgd."),
        ("key", "Transport &amp; leenauto's", "We komen met de trailer of leveren een leenauto. Jouw klant blijft mobiel, jouw planning blijft staan."),
        ("pin", "Poetsen op locatie", "Liever op je eigen terrein? We komen ter plekke, in heel Midden-Groningen, Assen, Emmen en Zuidlaren."),
    ]
    feat = "".join(f'<div class="feature reveal" data-delay="{(n % 3) * 80}"><div class="card__icon">{i(ic)}</div><h3>{t}</h3><p>{p}</p></div>'
                   for n, (ic, t, p) in enumerate(features))
    faqs = [
        ("Wat kost auto poetsen in Hoogezand?", "Een handwas begint bij €14,95 en een complete beurt binnen en buiten bij €29,95. Voor een volledige detailing betaal je vanaf €453 (interieur), een ceramische coating vanaf €1.089. Met de <a class=\"link\" href=\"/diensten/#calculator\">prijscalculator</a> zie je direct wat jouw combinatie kost."),
        ("Hoe snel kan ik terecht?", "Meestal binnen een paar werkdagen, vaak sneller. Zakelijke klanten met spoed helpen we 24/7. Vraag online een afspraak aan en we bevestigen binnen een uur op werkdagen."),
        ("Halen jullie mijn auto op?", "Ja. Met onze haal &amp; breng service halen we je auto met de trailer op, thuis of op je werk, en brengen we hem schoon terug. Dat kan in heel Midden-Groningen en omgeving."),
        ("Werken jullie ook voor dealers en leasemaatschappijen?", "Dat is onze specialiteit. We reconditioneren inruilauto's, maken voertuigen showroom- en foto-klaar en onderhouden wagenparken tegen vaste contracttarieven."),
        ("Wat is het verschil tussen wax en een ceramische coating?", "Wax geeft mooie glans maar slijt binnen weken tot maanden. Een ceramische coating hecht zich aan de lak en beschermt jaren tegen vuil, UV en vogelpoep. Wassen gaat daarna een stuk makkelijker."),
    ]
    faq = "".join(f"<details><summary>{q}</summary><div class=\"faq__body\"><p>{a}</p></div></details>" for q, a in faqs)
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q.replace("&amp;", "&"),
              "acceptedAnswer": {"@type": "Answer", "text": a.replace("&amp;", "&")}} for q, a in faqs]}
    h = head("Auto poetsen &amp; detailing Hoogezand | CarClean Midden-Groningen",
             "Auto poetsen, detailing en ceramische coating in Hoogezand en Midden-Groningen. Handwas v.a. €14,95, haal &amp; breng en 24/7 service voor dealers.",
             "/", extra_ld=[faq_ld], preload_hero=True)

    body = f"""
<section class="hero" aria-labelledby="hero-title">
  <div class="hero__bg" aria-hidden="true"></div>
  <div class="container hero__grid">
    <div class="hero__content">
      <h1 id="hero-title"><span class="kicker">Auto poetsen &amp; detailing in Hoogezand</span><span class="sheen">Showroomglans. Zonder&nbsp;wachtrij.</span></h1>
      <p class="hero__lead">Van een snelle handwas tot een ceramische coating die jaren meegaat. Voor particulieren, dealers en wagenparken in heel Midden-Groningen. Wij halen op, poetsen en brengen terug.</p>
      <div class="btn-row">
        <a class="btn btn--primary btn--lg" href="/afspraak/">Plan je beurt {ARROW}</a>
        <a class="btn btn--ghost btn--lg" href="/diensten/">Bekijk prijzen</a>
      </div>
      <div class="hero__proof">
        <div class="proof"><strong data-count="500" data-suffix="+">500+</strong><span>voertuigen gereinigd</span></div>
        <div class="proof"><strong>24/7</strong><span>voor zakelijke klanten</span></div>
        <div class="proof"><strong>€14,95</strong><span>handwas vanaf</span></div>
      </div>
    </div>
    <div class="hero__visual">
      <div class="hero__frame">
        {P("lambo", "Zwarte Lamborghini Aventador met geopende deuren in de detailingstudio, de lak spiegelt het studiolicht", "(min-width: 960px) 40vw, 100vw", eager=True)}
      </div>
      <div class="float-card float-card--b" aria-hidden="true">
        <span class="row open-status" data-open-status><span class="dot"></span><strong data-open-text>Ma–vr 08:00–17:00</strong></span>
        <span class="muted">Bevestiging binnen 1 uur</span>
      </div>
      <div class="float-card float-card--a" aria-hidden="true">
        <span class="row">{i("shield", "")}<strong>Ceramische coating</strong></span>
        <span class="muted">2 lagen · jarenlang glans</span>
      </div>
    </div>
  </div>
</section>

<section class="trust" aria-label="Keurmerken en moederbedrijf">
  <div class="container trust__inner">
    <span class="trust__label">Vertrouwd door</span>
    <a class="trust__logo" href="https://www.bovag.nl" target="_blank" rel="noopener"><img src="/img/bovag-logo.webp" alt="BOVAG" width="60" height="96" loading="lazy"></a>
    <a class="trust__logo" href="https://www.rdw.nl" target="_blank" rel="noopener"><img src="/img/rdw-logo.webp" alt="RDW" width="130" height="96" loading="lazy"></a>
    <a class="trust__logo" href="https://www.beblitz.nl" target="_blank" rel="noopener"><span><strong>Dochter van BeBlitz</strong>High-End Car Detailing</span></a>
  </div>
</section>

<section class="section" aria-labelledby="diensten-title">
  <div class="container">
    <div class="section-head section-head--split">
      <div class="stack reveal"><span class="eyebrow">Diensten</span><h2 id="diensten-title">Eén adres voor elke graad van schoon.</h2></div>
      <p class="lead reveal">Vaste prijzen, geen verrassingen. Kies wat je auto nodig heeft, of laat ons meekijken en eerlijk adviseren.</p>
    </div>
    <div class="tiles">{tile_html}</div>
    <div class="also reveal">
      <span>Ook voor:</span>
      <a class="chip" href="/diensten/#wasstraat">{i("droplet")} Wasstraat v.a. €10</a>
      <a class="chip" href="/diensten/#haal-en-breng">{i("truck")} Haal &amp; breng</a>
      <a class="chip" href="/diensten/#groot-materieel">{i("truck")} Vrachtwagens</a>
      <a class="chip" href="/diensten/#groot-materieel">{i("anchor")} Boten</a>
      <a class="chip" href="/diensten/#groot-materieel">{i("leaf")} Agrarisch</a>
    </div>
  </div>
</section>

<section class="section surface-dark-2" aria-labelledby="verschil-title">
  <div class="container polish">
    <div class="stack reveal">
      <span class="eyebrow">Zie het verschil</span>
      <h2 id="verschil-title">Sleep. Poets. Glans.</h2>
      <p class="lead">Wegverkeer, pekel en zon maken lak dof, grauw en vlekkerig. Wij halen de diepte en kleur terug, en met een coating blijft dat zo.</p>
      <ul class="checks">
        <li>Meerfasen handwas, nooit borstels op je lak</li>
        <li>Machinaal polijsten haalt swirls en krassen weg</li>
        <li>Wax of ceramische coating voor blijvende bescherming</li>
      </ul>
      <a class="arrow-link mt-4" href="/diensten/#detailing">Bekijk detailing {ARROW}</a>
    </div>
    <div class="reveal">
      <div class="compare" data-compare>
        <img src="/img/p/mercedes-1024.webp" alt="" width="1024" height="793" loading="lazy" decoding="async">
        <img class="compare__before compare__before--sim" src="/img/p/mercedes-1024.webp" alt="" width="1024" height="793" loading="lazy" decoding="async">
        <div class="compare__grime" aria-hidden="true"></div>
        <span class="compare__tag compare__tag--l" aria-hidden="true">Voor</span>
        <span class="compare__tag compare__tag--r" aria-hidden="true">Na</span>
        <input class="compare__range" type="range" min="0" max="100" value="50" aria-label="Vergelijk voor en na: verschuif om het verschil te zien" data-compare-range>
        <div class="compare__handle" aria-hidden="true"><span class="compare__knob">{i("swap")}</span></div>
      </div>
      <p class="compare__note">Mercedes-AMG S-Klasse. Voor-weergave is een illustratie van doffe, vervuilde lak.</p>
    </div>
  </div>
</section>

<section class="section b2b" aria-labelledby="b2b-title">
  <div class="container">
    <div class="section-head section-head--split">
      <div class="stack reveal"><span class="eyebrow">Voor zakelijke klanten</span><h2 id="b2b-title">Jouw showroom vol. Wij regelen de rest.</h2></div>
      <div class="stack reveal">
        <p class="lead">Autobedrijven willen snel, makkelijk en ontzorgd worden. Daarom bouwen we aan een 24-uursbedrijf: transparant, realistisch geprijsd en altijd op tijd.</p>
        <div class="btn-row"><a class="btn btn--primary" href="/contact/?onderwerp=zakelijk">Zakelijke offerte {ARROW}</a><a class="btn btn--ghost" href="tel:{TEL}">{i("phone")} {PHONE}</a></div>
      </div>
    </div>
    <div class="feature-list">{feat}</div>
  </div>
</section>

<section class="section surface-light" aria-labelledby="hb-title">
  <div class="container">
    <div class="section-head section-head--split">
      <div class="stack reveal"><span class="eyebrow">Haal &amp; breng</span><h2 id="hb-title">Jij werkt door. Wij halen je auto op.</h2></div>
      <p class="lead reveal">Geen tijd om langs te komen? We laden je auto op onze eigen trailer, thuis of op het werk, en zetten hem stralend terug.</p>
    </div>
    <ol class="steps" role="list">
      <li class="step reveal"><h3>Plan online of bel</h3><p>Kies je behandeling en een moment dat jou uitkomt. Binnen een uur hoor je van ons.</p></li>
      <li class="step reveal" data-delay="90"><h3>Wij halen op</h3><p>Op het afgesproken tijdstip staat onze trailer voor de deur. Sleutel afgeven, klaar.</p></li>
      <li class="step reveal" data-delay="180"><h3>Schoon terug</h3><p>Na de behandeling brengen we je auto terug, spic en span. Jij hoeft er niets voor te doen.</p></li>
    </ol>
    <div class="btn-row mt-7 reveal"><a class="btn btn--dark btn--lg" href="/afspraak/?dienst=haalbreng">Haal &amp; breng aanvragen {ARROW}</a></div>
  </div>
</section>

{gallery()}

{reviews_section()}

<section class="section" aria-labelledby="over-title">
  <div class="container split">
    <div class="split__media reveal">
      {P("gklasse", "Mercedes G-Klasse in de studio van CarClean en BeBlitz", "(min-width: 960px) 45vw, 100vw")}
      <div class="stamp" aria-hidden="true"><span><strong>BeBlitz</strong>familie</span></div>
    </div>
    <div class="stack reveal">
      <span class="eyebrow">Over CarClean</span>
      <h2 id="over-title">High-end vakmanschap, voor elke auto.</h2>
      <p class="lead">CarClean is de jongste loot van BeBlitz High-End Car Detailing. Dezelfde kennis waarmee we Lamborghini's en Porsches behandelen, zetten we nu in voor jouw dagelijkse auto, je leasebak en de voorraad van je showroom.</p>
      <div class="stats mt-6">
        <div class="stat"><strong data-count="500" data-suffix="+">500+</strong><span>voertuigen gereinigd</span></div>
        <div class="stat"><strong data-count="12" data-suffix="+">12+</strong><span>gemeenten bediend</span></div>
        <div class="stat"><strong>24/7</strong><span>zakelijke service</span></div>
        <div class="stat"><strong data-count="100" data-suffix="%">100%</strong><span>tevredenheidsgarantie</span></div>
      </div>
      <a class="arrow-link mt-5" href="/over-ons/">Lees ons verhaal {ARROW}</a>
    </div>
  </div>
</section>

{area_section()}

<section class="section surface-light" aria-labelledby="faq-title">
  <div class="container split">
    <div class="stack reveal">
      <span class="eyebrow">Veelgestelde vragen</span>
      <h2 id="faq-title">Goed om te weten.</h2>
      <p class="lead">Staat je vraag er niet bij? App of bel ons, je krijgt een eerlijk antwoord van iemand die er verstand van heeft.</p>
      <div class="btn-row"><a class="btn btn--dark" href="{WA}" target="_blank" rel="noopener">{i("whatsapp")} Stel je vraag via WhatsApp</a></div>
    </div>
    <div class="faq reveal">{faq}</div>
  </div>
</section>

{cta_band()}
"""
    write("index.html", h + header("/") + body + footer())


# ================================================================ DIENSTEN
def plan(title, price, desc, items, href, cta="Plan deze beurt", featured=False, unit="", metal=None, frm=True):
    badge = '<span class="badge">Meest gekozen</span>' if featured else ""
    m = f'<span class="metal metal--{metal}" aria-hidden="true"></span>' if metal else ""
    lis = "".join(f"<li>{x}</li>" for x in items)
    f = '<span class="price__from">v.a.</span>' if frm else ""
    u = f'<span class="price__unit">{unit}</span>' if unit else ""
    btn = "btn--primary" if featured else "btn--dark"
    return f"""<article class="card plan{" plan--featured" if featured else ""} reveal">
        {badge}{m}
        <h3>{title}</h3>
        <p class="price">{f}<span class="price__amount">€{price}</span>{u}</p>
        <p class="muted">{desc}</p>
        <ul class="checks">{lis}</ul>
        <a class="btn {btn} btn--block" href="{href}">{cta} {ARROW}</a>
      </article>"""


def service(id_, eyebrow, h2, lead, benefits, content, cta=None):
    ben = "".join(f"<li>{b}</li>" for b in benefits)
    c = cta or ""
    return f"""<section class="service" id="{id_}" aria-labelledby="{id_}-title">
    <div class="service__intro reveal">
      <span class="eyebrow">{eyebrow}</span>
      <h2 id="{id_}-title">{h2}</h2>
      <p class="lead">{lead}</p>
      <ul class="checks">{ben}</ul>
      {c}
    </div>
    <div class="stack">{content}</div>
  </section>"""


def diensten():
    offer_ld = {"@type": "OfferCatalog", "name": "Diensten en prijzen CarClean Midden-Groningen", "url": SITE + "/diensten/",
                "itemListElement": [{"@type": "Offer", "price": p, "priceCurrency": "EUR",
                                     "itemOffered": {"@type": "Service", "name": n, "provider": {"@id": SITE + "/#business"}, "areaServed": "Midden-Groningen"}}
                                    for n, p in [("Basic Wash", 14.95), ("Complete Beurt", 29.95), ("Premium Detail", 79.95),
                                                 ("Detailing interieur", 453), ("Detailing exterieur", 665), ("Ceramische coating", 1089),
                                                 ("Koplamp polijsten", 60.50), ("Velgen coating", 121), ("Ozonbehandeling", 121),
                                                 ("Remklauwen spuiten", 544.50), ("Wasstraat Brons", 10), ("Wasstraat Zilver", 13.50),
                                                 ("Wasstraat Goud", 16.50), ("Wasstraat Diamant", 19.50)]]}
    h = head("Auto detailing, coating &amp; prijzen Hoogezand | CarClean",
             "Prijzen voor auto poetsen, detailing en ceramische coating in Hoogezand. Handwas v.a. €14,95, detailing v.a. €453, coating v.a. €1.089. Bereken je prijs.",
             "/diensten/", extra_ld=[offer_ld, breadcrumb([("/", "Home"), ("/diensten/", "Diensten & prijzen")])])

    sub = [("particulier", "Handwas"), ("detailing", "Detailing"), ("coating", "Coating"), ("extras", "Extra's"),
           ("wasstraat", "Wasstraat"), ("haal-en-breng", "Haal &amp; breng"), ("zakelijk", "Zakelijk"),
           ("groot-materieel", "Groot materieel"), ("calculator", "Prijscalculator")]
    subnav = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in sub)

    s_part = service("particulier", "Particulieren", "Handwas &amp; poetsen.",
        "Van een snelle wasbeurt tussendoor tot een beurt waarna je auto ruikt en voelt als nieuw. Alles met de hand, nooit met borstels.",
        ["Klaar terwijl jij een kop koffie drinkt", "Veilig voor lak en coating", "Ook voor SUV, MPV en bestelwagen (prijs op aanvraag)"],
        '<div class="plans plans--3">'
        + plan("Basic Wash", "14,95", "Snel en effectief, perfect voor regelmatig onderhoud.", ["Exterieur handwas", "Ramen buiten", "Velgen spoelen", "Afdrogen met microvezel"], "/afspraak/?dienst=basic")
        + plan("Complete Beurt", "29,95", "Binnen én buiten: de keuze van de meeste klanten.", ["Alles van Basic Wash", "Interieur stofzuigen", "Dashboard &amp; panelen", "Matten reinigen", "Ramen binnen &amp; buiten"], "/afspraak/?dienst=complete", featured=True)
        + plan("Premium Detail", "79,95", "Alsof hij net van de dealer komt.", ["Alles van Complete Beurt", "Leer &amp; kunststof behandeling", "Spray-wax bescherming", "Motorruimte spoelen", "Geurneutralisatie"], "/afspraak/?dienst=premium")
        + '</div><p class="fineprint reveal">Prijzen excl. btw, voor een gemiddelde personenauto. SUV, MPV of bestelwagen? Bel <a class="link" href="tel:' + TEL + '">' + PHONE + '</a>.</p>')

    s_det = service("detailing", "Detailing", "Auto detailing, tot in elke naad.",
        "Detailing gaat verder dan schoon. We reinigen, corrigeren en beschermen. Zo krijgt je auto zijn oorspronkelijke kleur, diepte en geur terug, en stijgt de inruilwaarde.",
        ["Vlekken, kringen en geurtjes echt weg", "Swirls en lichte krassen weggepolijst", "Hogere restwaarde bij verkoop of inruil"],
        '<div class="plans plans--2">'
        + plan("Detailing interieur", "453", "Grondige dieptereiniging van het complete interieur.", ["Stofzuigen &amp; dieptereinigen", "Vlekken uit bekleding", "Dashboard &amp; panelen behandeld", "Bacterie- &amp; geurneutralisatie"], "/afspraak/?dienst=interieur")
        + plan("Detailing exterieur", "665", "Excellente exterieurbehandeling met waxcoating voor maximale glans.", ["Meerfasen wasbehandeling", "Machinaal polijsten (per laag)", "Waxcoating", "Velgen &amp; ruiten gereinigd"], "/afspraak/?dienst=exterieur", featured=True, frm=False)
        + '</div>')

    s_coat = service("coating", "Lakbescherming", "Ceramische coating.",
        "Een keramische laag die zich aan je lak hecht. Je auto blijft jaren dieper glanzen, vuil hecht minder en wassen gaat in de helft van de tijd.",
        ["Jarenlange bescherming tegen UV, pekel en vogelpoep", "Hydrofoob: water en vuil parelen eraf", "Inclusief polijsten vooraf"],
        f"""<div class="split">
        <div class="split__media reveal">{P("bmw", "BMW i8 met ceramische coating, de lak weerspiegelt de omgeving", "(min-width: 960px) 30vw, 100vw")}</div>
        {plan("2-laags ceramische coating", "1.089", "Professionele keramische lakbescherming voor wie het maximale wil.", ["Lakcorrectie &amp; polijsten inbegrepen", "2 lagen keramische coating", "Hydrofobe werking", "Jaren bescherming en glans"], "/afspraak/?dienst=coating", cta="Vraag een coating aan", featured=True)}
      </div>""")

    extras = [("Koplampen polijsten", "Helder en scherp: veiliger en mooier.", "60,50", "per stuk"),
              ("Velgen coating", "Bescherming en glans, met of zonder polijsten.", "121", "per velg"),
              ("Ozonbehandeling", "24-uurs ozon: rook- en dierengeur volledig weg.", "121", "vaste prijs"),
              ("Remklauwen spuiten", "In elke kleur, met of zonder logo. Coating optioneel.", "544,50", "per set")]
    ex = "".join(f'<div class="extra reveal"><div><h3>{t}</h3><p>{p}</p></div><p class="amount">v.a. €{a}<small>{u}</small></p></div>' for t, p, a, u in extras)
    s_ext = service("extras", "Extra behandelingen", "De finishing touch.",
        "Los te boeken of te combineren met elke beurt. Meer weten over PPF, wrapping of spuitwerk? Via BeBlitz en ons partnernetwerk regelen we het.",
        ["Te combineren met elke beurt", "Advies op maat, gratis"],
        f'<div class="extras">{ex}</div><p class="fineprint reveal">Prijzen excl. btw.</p>',
        f'<a class="btn btn--dark" href="/afspraak/?dienst=anders">Vraag advies {ARROW}</a>')

    s_was = service("wasstraat", "Wasstraat · in samenwerking met BeBlitz", "Wasstraat-pakketten.",
        "Modern, snel en grondig: ideaal voor regulier onderhoud tussen je poetsbeurten door. Betalen met pin.",
        ["Doorrijden en direct resultaat", "Schonere velgen met intensieve foam"],
        '<div class="plans plans--4">'
        + plan("Brons", "10,00", "De essentials, snel en doeltreffend.", ["Auto wassen", "Drogen"], "/afspraak/?dienst=brons", cta="Boeken", metal="bronze", frm=False)
        + plan("Zilver", "13,50", "Meer aandacht voor een betere reiniging.", ["Intensieve foam", "Auto wassen", "Velgen reinigen", "Drogen"], "/afspraak/?dienst=zilver", cta="Boeken", metal="silver", frm=False)
        + plan("Goud", "16,50", "De complete wasbeurt voor vlekkeloze glans.", ["Handmatige voorwas", "Intensieve foam", "Auto wassen", "Velgen reinigen", "Drogen"], "/afspraak/?dienst=goud", cta="Boeken", metal="gold", featured=True, frm=False)
        + plan("Diamant", "19,50", "De ultieme wasstraatbeurt.", ["Alles van Goud", "Lakverzegeling met wax", "Handmatig nadrogen"], "/afspraak/?dienst=diamant", cta="Boeken", metal="diamond", frm=False)
        + '</div>')

    s_hb = service("haal-en-breng", "Extra service", "Haal &amp; breng, met eigen trailer.",
        "Geen tijd of geen vervoer? We laden je voertuig op onze trailer, reinigen het professioneel en brengen het schoon terug. In heel Midden-Groningen en omgeving.",
        ["Thuis of op je werk opgehaald", "Op een moment dat jou past", "Ook voor niet-rijdende voertuigen"],
        f"""<div class="grid grid--2">
        <div class="card reveal"><div class="card__icon">{i("home")}</div><h3>Aan huis</h3><p>We rijden naar je thuisadres, laden de auto op de trailer en brengen hem schoon terug. Jij hoeft niets te doen.</p></div>
        <div class="card reveal" data-delay="80"><div class="card__icon">{i("building")}</div><h3>Op het werk</h3><p>Laat je auto ophalen terwijl jij gewoon werkt. Schoon terug voordat je naar huis gaat.</p></div>
      </div>
      <div class="btn-row reveal"><a class="btn btn--dark" href="/afspraak/?dienst=haalbreng">Haal &amp; breng aanvragen {ARROW}</a><a class="btn btn--ghost" href="tel:{TEL}">{i("phone")} Bel ons</a></div>""")

    biz = [("car", "Inruilklaar pakket", "Basisreiniging binnen en buiten voor inruilauto's. Snel en efficiënt, met scherpe stuksprijzen bij volume."),
           ("sparkle", "Showroompakket", "Volledige detail voor een showroomklare presentatie: polijsten, bescherming, ruiten, tot in de puntjes."),
           ("camera", "Foto-klaar &amp; AI-studio", "Eigen fotoruimte met AI-achtergronden. Direct bruikbare beelden voor je website en marketplaces."),
           ("calendar", "Maandcontract", "Vaste prijs per maand voor een afgesproken aantal beurten. Zorgeloos en goed te begroten."),
           ("repeat", "24/7 spoedservice", "Brand- of parkeergarageschade? We sturen direct transport en lossen het waar mogelijk dezelfde dag op."),
           ("users", "Bedrijfstarief", "Hoe meer voertuigen, hoe scherper de prijs. Korting vanaf 3 voertuigen per beurt.")]
    bz = "".join(f'<div class="card card--hover reveal" data-delay="{(n % 2) * 80}"><div class="card__icon">{i(ic)}</div><h3>{t}</h3><p>{p}</p></div>' for n, (ic, t, p) in enumerate(biz))
    s_biz = service("zakelijk", "Dealers · lease · wagenparken", "Showroomklaar. Elke keer.",
        "Jij verkoopt, wij zorgen voor de presentatie. Vaste prijsafspraken, snelle doorlooptijd en één aanspreekpunt, ook voor spot-repair, deukherstel en APK via onze partners.",
        ["Vaste contracttarieven", "Eigen transport &amp; leenauto's", "24/7 bereikbaar"],
        f'<div class="grid grid--2">{bz}</div>',
        f'<a class="btn btn--dark" href="/contact/?onderwerp=zakelijk">Vraag een zakelijke offerte {ARROW}</a>')

    big = [("truck", "Vrachtwagens &amp; bestelwagens", "Cabine, opbouw en chassis grondig gewassen, en het interieur opgefrist. Volledig op maat."),
           ("anchor", "Boten", "Aanslag, algen en zout weg, binnen en buiten, met optionele beschermende coating. Klaar voor het seizoen."),
           ("leaf", "Agrarisch materieel", "Tractoren, combines, aanhangers en machines. Bij ons of op locatie, grondig en snel.")]
    bg = "".join(f'<div class="card reveal" data-delay="{n * 80}"><div class="card__icon">{i(ic)}</div><h3>{t}</h3><p>{p}</p><a class="arrow-link mt-4" href="/contact/?onderwerp=groot">Prijs opvragen {ARROW}</a></div>' for n, (ic, t, p) in enumerate(big))
    s_big = service("groot-materieel", "Groot materieel", "Vrachtwagens, boten &amp; agrarisch.",
        "Van bestelbus tot combine: we hebben de middelen en de ervaring voor elk formaat. Altijd een prijs op maat.",
        ["Op locatie of bij ons", "Flexibel in te plannen, ook buiten het seizoen"],
        f'<div class="grid">{bg}</div>')

    pk = [("basic", "Basic Wash", 14.95), ("complete", "Complete Beurt", 29.95), ("premium", "Premium Detail", 79.95),
          ("interieur", "Detailing interieur", 453), ("exterieur", "Detailing exterieur", 665), ("coating", "Ceramische coating", 1089)]
    pk_html = "".join(f'<label class="choice"><input type="radio" name="pakket" value="{k}" data-price="{p}" data-label="{l}"{" checked" if k == "complete" else ""}><span>{l} <small>€{eur(p)}</small></span></label>' for k, l, p in pk)
    ex_opts = [("koplampen", "Koplampen polijsten (2×)", 121), ("velgen", "Velgen coating (4×)", 484), ("ozon", "Ozonbehandeling", 121),
               ("remklauwen", "Remklauwen spuiten", 544.5), ("haalbreng", "Haal &amp; breng", 0)]
    ex_html = "".join(f'<label class="choice"><input type="checkbox" name="extra" value="{k}" data-price="{p}" data-label="{l}"><span>{l} <small>{"in overleg" if not p else "+€" + eur(p)}</small></span></label>' for k, l, p in ex_opts)
    calc = f"""<section class="section surface-light surface-light--2" id="calculator" aria-labelledby="calc-title">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Prijscalculator</span><h2 id="calc-title">Stel je beurt samen.</h2><p class="lead">Kies een behandeling en extra's. Je ziet direct de vanaf-prijs, en met één klik staat alles klaar in het afspraakformulier.</p></div>
    <form class="calc reveal" data-calc aria-describedby="calc-note">
      <div class="calc__options">
        <fieldset class="choices"><legend>1. Behandeling</legend>{pk_html}</fieldset>
        <fieldset class="choices"><legend>2. Extra's <span class="optional">(optioneel)</span></legend>{ex_html}</fieldset>
      </div>
      <div class="calc__total" aria-live="polite">
        <span class="eyebrow">Jouw indicatie</span>
        <p><span class="price__from">vanaf</span><br><span class="calc__sum" data-calc-sum>€29,95</span></p>
        <ul class="calc__lines" data-calc-lines><li><span>Complete Beurt</span><span>€29,95</span></li></ul>
        <a class="btn btn--primary btn--block" href="/afspraak/?dienst=complete" data-calc-link>Vraag deze beurt aan {ARROW}</a>
        <p class="calc__note" id="calc-note">Indicatie excl. btw voor een gemiddelde personenauto. De definitieve prijs hoor je vooraf, nooit achteraf.</p>
      </div>
    </form>
  </div>
</section>"""

    faqs = [("Zijn de prijzen inclusief btw?", "De genoemde prijzen zijn exclusief btw. Bij je afspraakbevestiging krijg je altijd de totaalprijs vooraf."),
            ("Wat als mijn auto extra vies is?", "Bij extreme vervuiling (veel dierenhaar, schimmel, zand) overleggen we vooraf over eventuele meerkosten. Geen verrassingen achteraf."),
            ("Hoe lang duurt een behandeling?", "Een handwas is binnen het uur klaar. Een complete detailing duurt een dag, een ceramische coating één tot twee dagen inclusief uitharden."),
            ("Kan ik betalen met pin?", "Ja, je kunt pinnen. Zakelijke klanten ontvangen een factuur.")]
    faq = "".join(f"<details><summary>{q}</summary><div class=\"faq__body\"><p>{a}</p></div></details>" for q, a in faqs)

    body = page_hero([("/", "Home"), ("/diensten/", "Diensten &amp; prijzen")], "Transparante tarieven",
                     "Diensten &amp; prijzen", "Auto poetsen, detailing en ceramische coating in Hoogezand en omgeving. Vaste prijzen, geen kleine lettertjes. Voor particulieren én zakelijk.",
                     f'<div class="btn-row"><a class="btn btn--primary" href="#calculator">Bereken je prijs {ARROW}</a><a class="btn btn--ghost" href="/afspraak/">Direct afspraak maken</a></div>')
    body += f"""<nav class="subnav" aria-label="Diensten op deze pagina"><div class="container"><ul data-subnav>{subnav}</ul></div></nav>
<div class="surface-light"><div class="container">
  {s_part}
  {s_det}
  {s_coat}
  {s_ext}
  {s_was}
  {s_hb}
  {s_biz}
  {s_big}
</div></div>
{calc}
<section class="section surface-light" aria-labelledby="pfaq-title">
  <div class="container split">
    <div class="stack reveal"><span class="eyebrow">Over prijzen</span><h2 id="pfaq-title">Eerlijk is eerlijk.</h2><p class="lead">De prijs die je vooraf hoort, is de prijs die je betaalt.</p></div>
    <div class="faq reveal">{faq}</div>
  </div>
</section>
{cta_band("Weet je wat je auto nodig heeft?", "Plan direct, of laat ons gratis meekijken en adviseren.")}
"""
    write("diensten/index.html", h + header("/diensten/") + body + footer())


# ================================================================ OVER ONS
def over():
    h = head("Over CarClean | autopoetsbedrijf Midden-Groningen",
             "CarClean Midden-Groningen is de dochter van BeBlitz High-End Car Detailing. Ons verhaal, onze werkwijze en waarom Groningen voor ons kiest.",
             "/over-ons/", extra_ld=[breadcrumb([("/", "Home"), ("/over-ons/", "Over ons")])])
    values = [("Ontzorgen", "Jij hoeft nergens aan te denken. We halen op, plannen mee, regelen partners en melden ons als het klaar is."),
              ("Snelheid", "Geen wachtrijen. Een auto die stilstaat kost geld, zeker in een showroom. Dus werken we snel, zonder haast te maken met kwaliteit."),
              ("Vakmanschap", "High-end kennis van BeBlitz, toegepast op elke auto. Professionele middelen, de juiste technieken, oog voor detail."),
              ("Eerlijk", "Realistische prijzen, vooraf bekend. Niet tevreden? Dan lossen we het op. Dat is geen actie, dat is de standaard.")]
    vals = "".join(f'<div class="value reveal"><h3>{t}</h3><p>{p}</p></div>' for t, p in values)
    team = [("sparkle", "De detailers", "Getraind in de studio van BeBlitz. Van handwas tot lakcorrectie en coating: ze weten precies wat je lak nodig heeft."),
            ("users", "Planning &amp; zakelijk", "Jouw vaste aanspreekpunt voor afspraken, contracten en spoed. Bereikbaar per telefoon en WhatsApp, 24/7 voor B2B."),
            ("truck", "Transport", "Rijden met de trailer door heel Groningen en Drenthe, en zorgen dat je auto veilig heen en terug gaat.")]
    # TEAM: vervang .member__photo inhoud door <img> met echte teamfoto's zodra beschikbaar.
    tm = "".join(f'<article class="card member reveal" data-delay="{n * 80}"><div class="member__photo">{i(ic)}</div><div class="member__body"><h3>{t}</h3><p>{p}</p></div></article>' for n, (ic, t, p) in enumerate(team))
    body = page_hero([("/", "Home"), ("/over-ons/", "Over ons")], "Ons verhaal",
                     "High-end roots. Groningse nuchterheid.",
                     "CarClean Midden-Groningen is het autopoetsbedrijf voor heel Groningen en Drenthe, en de jongste loot van BeBlitz High-End Car Detailing.")
    body += f"""
<section class="section surface-light" aria-labelledby="wie-title">
  <div class="container split">
    <div class="split__media reveal">
      {P("lambo", "Zwarte Lamborghini in de detailingstudio van BeBlitz", "(min-width: 960px) 45vw, 100vw")}
      <div class="stamp" aria-hidden="true"><span><strong>24/7</strong>voor B2B</span></div>
    </div>
    <div class="stack prose reveal">
      <span class="eyebrow">Wie wij zijn</span>
      <h2 id="wie-title">Reconditioneren is ons vak. Ontzorgen onze standaard.</h2>
      <p class="lead">Bij BeBlitz behandelen we al jaren supercars en klassiekers. Met CarClean brengen we dat niveau naar iedereen: de particulier in Hoogezand, de dealer in Veendam en het wagenpark in Groningen.</p>
      <p>We bouwen aan een 24-uursbedrijf: snelle, vakkundige doorloop, geen lange wachtrijen, eigen transport, leenauto's en poetsen op locatie. Voor zakelijke klanten zijn we altijd bereikbaar, ook bij brandschade of een incident in de parkeergarage.</p>
      <p>Via ons partnernetwerk regelen we ook spot-repair, deukherstel, restyling en APK. Eén aanspreekpunt, volledig ontzorgd. Realistisch in prijs, transparant in kwaliteit.</p>
      <div class="btn-row mt-5"><a class="btn btn--dark" href="/afspraak/">Maak een afspraak {ARROW}</a><a class="btn btn--ghost" href="/contact/?onderwerp=zakelijk">Zakelijke offerte</a></div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container">
    <div class="stats reveal">
      <div class="stat"><strong data-count="500" data-suffix="+">500+</strong><span>voertuigen gereinigd</span></div>
      <div class="stat"><strong data-count="12" data-suffix="+">12+</strong><span>gemeenten bediend</span></div>
      <div class="stat"><strong>24/7</strong><span>bereikbaar voor zakelijk</span></div>
      <div class="stat"><strong data-count="100" data-suffix="%">100%</strong><span>tevredenheidsgarantie</span></div>
    </div>
  </div>
</section>

<section class="section surface-light" aria-labelledby="waarden-title">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Waar we voor staan</span><h2 id="waarden-title">Vier beloftes. Geen uitzonderingen.</h2></div>
    <div class="values">{vals}</div>
  </div>
</section>

<section class="section" aria-labelledby="team-title">
  <div class="container">
    <div class="section-head section-head--split">
      <div class="stack reveal"><span class="eyebrow">Het team</span><h2 id="team-title">De mensen achter de glans.</h2></div>
      <p class="lead reveal">Geen callcenter, geen doorverbinden. Je spreekt direct met de mensen die aan je auto werken.</p>
    </div>
    <div class="team">{tm}</div>
  </div>
</section>

<section class="section surface-light" aria-labelledby="werkwijze-title">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Werkwijze</span><h2 id="werkwijze-title">Van aanvraag tot glans.</h2></div>
    <ol class="steps" role="list">
      <li class="step reveal"><h3>Aanvraag &amp; advies</h3><p>Online, via WhatsApp of telefonisch. We adviseren eerlijk wat je auto echt nodig heeft, en je weet vooraf wat het kost.</p></li>
      <li class="step reveal" data-delay="90"><h3>Behandeling</h3><p>Ophalen of langskomen. Daarna gaan onze detailers aan de slag met professionele middelen en de wasstraat van BeBlitz.</p></li>
      <li class="step reveal" data-delay="180"><h3>Oplevering</h3><p>We lopen het resultaat samen met je na. Niet tevreden? Dan lossen we het op. Dat is onze belofte.</p></li>
    </ol>
  </div>
</section>

{gallery()}
{area_section()}
{cta_band("Nieuwsgierig geworden?", "Kom langs, bel of plan direct je eerste beurt.")}
"""
    write("over-ons/index.html", h + header("/over-ons/") + body + footer())


# ================================================================ AFSPRAAK
SERVICE_OPTIONS = [
    ("Handwas &amp; poetsen", [("basic", "Basic Wash (v.a. €14,95)"), ("complete", "Complete Beurt (v.a. €29,95)"), ("premium", "Premium Detail (v.a. €79,95)")]),
    ("Detailing &amp; coating", [("interieur", "Detailing interieur (v.a. €453)"), ("exterieur", "Detailing exterieur + wax (€665)"), ("coating", "Ceramische coating (v.a. €1.089)")]),
    ("Extra's", [("koplampen", "Koplampen polijsten"), ("velgen", "Velgen coating"), ("ozon", "Ozonbehandeling"), ("remklauwen", "Remklauwen spuiten")]),
    ("Wasstraat", [("brons", "Wasstraat Brons (€10)"), ("zilver", "Wasstraat Zilver (€13,50)"), ("goud", "Wasstraat Goud (€16,50)"), ("diamant", "Wasstraat Diamant (€19,50)")]),
    ("Zakelijk &amp; overig", [("haalbreng", "Haal &amp; breng"), ("dealer", "Dealer / showroompakket"), ("wagenpark", "Wagenpark / contract"),
                               ("groot", "Vrachtwagen, boot of agrarisch"), ("anders", "Weet ik nog niet, graag advies")]),
]


def err(id_, msg):
    return f'<p class="field__error" id="{id_}-err">{msg}</p>'


def afspraak():
    h = head("Afspraak auto poetsen Hoogezand, plan online | CarClean",
             "Plan je afspraak voor auto poetsen, detailing of coating in Hoogezand. Vijf velden, binnen een uur bevestiging op werkdagen. Haal &amp; breng mogelijk.",
             "/afspraak/", extra_ld=[breadcrumb([("/", "Home"), ("/afspraak/", "Afspraak maken")])])
    opts = "".join(f'<optgroup label="{g}">' + "".join(f'<option value="{l.replace("&amp;", "&")}" data-id="{k}">{l}</option>' for k, l in items) + "</optgroup>" for g, items in SERVICE_OPTIONS)
    body = page_hero([("/", "Home"), ("/afspraak/", "Afspraak maken")], "In 60 seconden geregeld",
                     "Plan je beurt.", "Vijf velden, meer niet. Binnen een uur (op werkdagen) bellen of appen we je om het moment te bevestigen.")
    body += f"""
<section class="section surface-light">
  <div class="container form-layout">
    <aside class="form-layout__aside stack reveal" aria-labelledby="hoe-title">
      <h2 id="hoe-title" class="h3">Zo werkt het</h2>
      <ol class="mini-steps" role="list">
        <li><span class="n">1</span><div><strong>Vul het formulier in</strong><p>Kies je behandeling en een voorkeursdag.</p></div></li>
        <li><span class="n">2</span><div><strong>Wij bevestigen</strong><p>Binnen 1 uur op werkdagen, telefonisch of via WhatsApp.</p></div></li>
        <li><span class="n">3</span><div><strong>Jouw auto glanst</strong><p>Breng hem langs of laat hem ophalen met de trailer.</p></div></li>
      </ol>
      <div class="card mt-6">
        <h3>Liever direct contact?</h3>
        <p class="mt-4">Ma–vr 08:00–17:00. Zakelijk 24/7.</p>
        <div class="btn-row mt-5">
          <a class="btn btn--dark btn--sm" href="tel:{TEL}">{i("phone")} {PHONE}</a>
          <a class="btn btn--ghost btn--sm" href="{WA}" target="_blank" rel="noopener">{i("whatsapp")} WhatsApp</a>
        </div>
      </div>
    </aside>

    <div class="form-card reveal">
      <h2>Jouw aanvraag</h2>
      <p class="muted">Velden met <span class="req" aria-hidden="true">*</span><span class="visually-hidden">een sterretje</span> zijn verplicht.</p>
      <form class="form mt-6" name="afspraak" method="POST" action="/bedankt/" data-netlify="true" netlify-honeypot="bot-field" data-validate data-form-type="afspraak" id="booking">
        <input type="hidden" name="form-name" value="afspraak">
        <input type="hidden" name="samenstelling" value="" data-samenstelling>
        <p class="hp-field" aria-hidden="true"><label>Niet invullen <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>

        <div class="summary-chip" data-summary role="status">{i("check")}<span data-summary-text></span></div>

        <div class="field">
          <label for="naam">Naam <span class="req" aria-hidden="true">*</span></label>
          <input class="input" id="naam" name="naam" type="text" autocomplete="name" required aria-describedby="naam-err" placeholder="Voor- en achternaam">
          {err("naam", "Vul je naam in, dan weten we wie we moeten bellen.")}
        </div>
        <div class="form-row form-row--2">
          <div class="field">
            <label for="telefoon">Telefoon <span class="req" aria-hidden="true">*</span></label>
            <input class="input" id="telefoon" name="telefoon" type="tel" inputmode="tel" autocomplete="tel" required pattern="[\\s\\(\\)+\\-]*(?:\\d[\\s\\(\\)+\\-]*){{10,}}" aria-describedby="telefoon-err" placeholder="06 12345678">
            {err("telefoon", "Vul een geldig telefoonnummer in (minimaal 10 cijfers).")}
          </div>
          <div class="field">
            <label for="email">E-mail <span class="req" aria-hidden="true">*</span></label>
            <input class="input" id="email" name="email" type="email" autocomplete="email" required aria-describedby="email-err" placeholder="naam@voorbeeld.nl">
            {err("email", "Vul een geldig e-mailadres in, zoals naam@voorbeeld.nl.")}
          </div>
        </div>
        <div class="form-row form-row--2">
          <div class="field">
            <label for="dienst">Behandeling <span class="req" aria-hidden="true">*</span></label>
            <select class="input" id="dienst" name="dienst" required aria-describedby="dienst-err">
              <option value="">Kies een behandeling</option>
              {opts}
            </select>
            {err("dienst", "Kies een behandeling, of kies ‘graag advies’.")}
          </div>
          <div class="field">
            <label for="datum">Voorkeursdatum <span class="optional">(optioneel)</span></label>
            <input class="input" id="datum" name="datum" type="date" aria-describedby="datum-hint datum-err" data-date-min>
            <p class="field__hint" id="datum-hint" data-date-hint>We zijn open ma–vr. Zakelijk ook in het weekend.</p>
            {err("datum", "Kies een datum vanaf vandaag.")}
          </div>
        </div>

        <button class="btn btn--primary btn--lg btn--block" type="submit">Afspraak aanvragen {ARROW}</button>
        <p class="form-note">{i("lock")}<span>Je gegevens gebruiken we alleen om je afspraak in te plannen. Geen nieuwsbrief, geen gedoe.</span></p>
      </form>
    </div>
  </div>
</section>
"""
    write("afspraak/index.html", h + header("/afspraak/") + body + footer())


# ================================================================ CONTACT
def contact():
    cp_ld = {"@type": "ContactPage", "@id": SITE + "/contact/#contactpage", "url": SITE + "/contact/", "name": "Contact CarClean Midden-Groningen", "about": {"@id": SITE + "/#business"}}
    h = head("Contact | auto schoonmaken Hoogezand &amp; Groningen | CarClean",
             "Neem contact op met CarClean Midden-Groningen in Hoogezand. Bel 0598 744 299, app ons of stuur een bericht. Ma–vr 08:00–17:00, zakelijk 24/7 bereikbaar.",
             "/contact/", extra_ld=[cp_ld, breadcrumb([("/", "Home"), ("/contact/", "Contact")])])
    days = [("1", "Maandag", "08:00 – 17:00"), ("2", "Dinsdag", "08:00 – 17:00"), ("3", "Woensdag", "08:00 – 17:00"),
            ("4", "Donderdag", "08:00 – 17:00"), ("5", "Vrijdag", "08:00 – 17:00"), ("6", "Zaterdag", "Gesloten*"), ("0", "Zondag", "Gesloten*")]
    rows = "".join(f'<tr data-day="{d}"><th scope="row">{n}</th><td>{t}</td></tr>' for d, n, t in days)
    body = page_hero([("/", "Home"), ("/contact/", "Contact")], "Direct contact",
                     "Even sparren? Bel, app of mail.", "Je krijgt meteen iemand aan de lijn die verstand heeft van je auto. Berichten beantwoorden we doorgaans binnen een uur.")
    body += f"""
<section class="section surface-light">
  <div class="container form-layout">
    <div class="stack reveal">
      <h2 class="h3">Snelste route</h2>
      <div class="contact-cards">
        <a class="contact-card" href="tel:{TEL}"><span class="card__icon">{i("phone")}</span><div><strong>{PHONE}</strong><span>Bellen, ma–vr 08:00–17:00</span></div>{i("arrow", "arrow")}</a>
        <a class="contact-card" href="{WA}" target="_blank" rel="noopener"><span class="card__icon">{i("whatsapp")}</span><div><strong>WhatsApp</strong><span>Stuur een foto, krijg advies</span></div>{i("arrow", "arrow")}</a>
        <a class="contact-card" href="mailto:{EMAIL}"><span class="card__icon">{i("mail")}</span><div><strong>E-mail</strong><span>{EMAIL}</span></div>{i("arrow", "arrow")}</a>
        <a class="contact-card" href="{MAPS}" target="_blank" rel="noopener"><span class="card__icon">{i("pin")}</span><div><strong>Hoogezand</strong><span>Route via Google Maps</span></div>{i("arrow", "arrow")}</a>
      </div>
      <div class="card mt-6">
        <h3 class="open-status" data-open-status><span class="dot"></span><span data-open-text>Openingstijden</span></h3>
        <table class="hours mt-4" data-hours><caption class="visually-hidden">Openingstijden</caption><tbody>{rows}</tbody></table>
        <p class="fineprint mt-4">* Zakelijke klanten zijn 24/7 bereikbaar voor spoed.</p>
      </div>
    </div>

    <div class="form-card reveal">
      <h2>Stuur ons een bericht</h2>
      <p class="muted">Vraag, offerte of samenwerking? We reageren snel.</p>
      <form class="form mt-6" name="contact" method="POST" action="/bedankt/" data-netlify="true" netlify-honeypot="bot-field" data-validate data-form-type="contact">
        <input type="hidden" name="form-name" value="contact">
        <p class="hp-field" aria-hidden="true"><label>Niet invullen <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
        <div class="field">
          <label for="c-naam">Naam <span class="req" aria-hidden="true">*</span></label>
          <input class="input" id="c-naam" name="naam" type="text" autocomplete="name" required aria-describedby="c-naam-err">
          {err("c-naam", "Vul je naam in.")}
        </div>
        <div class="form-row form-row--2">
          <div class="field">
            <label for="c-email">E-mail <span class="req" aria-hidden="true">*</span></label>
            <input class="input" id="c-email" name="email" type="email" autocomplete="email" required aria-describedby="c-email-err">
            {err("c-email", "Vul een geldig e-mailadres in.")}
          </div>
          <div class="field">
            <label for="c-tel">Telefoon <span class="optional">(optioneel)</span></label>
            <input class="input" id="c-tel" name="telefoon" type="tel" inputmode="tel" autocomplete="tel">
          </div>
        </div>
        <div class="field">
          <label for="c-onderwerp">Onderwerp</label>
          <select class="input" id="c-onderwerp" name="onderwerp" data-prefill="onderwerp">
            <option value="Algemene vraag" data-id="algemeen">Algemene vraag</option>
            <option value="Offerte particulier" data-id="offerte">Offerte particulier</option>
            <option value="Zakelijk: dealer, lease of wagenpark" data-id="zakelijk">Zakelijk: dealer, lease of wagenpark</option>
            <option value="Vrachtwagen, boot of agrarisch" data-id="groot">Vrachtwagen, boot of agrarisch</option>
          </select>
        </div>
        <div class="field">
          <label for="c-bericht">Bericht <span class="req" aria-hidden="true">*</span></label>
          <textarea class="input" id="c-bericht" name="bericht" required aria-describedby="c-bericht-err" placeholder="Waar kunnen we je mee helpen?"></textarea>
          {err("c-bericht", "Schrijf kort waar we je mee kunnen helpen.")}
        </div>
        <button class="btn btn--primary btn--lg btn--block" type="submit">Verstuur bericht {ARROW}</button>
        <p class="form-note">{i("lock")}<span>We gebruiken je gegevens alleen om je vraag te beantwoorden.</span></p>
      </form>
    </div>
  </div>
</section>
{area_section()}
"""
    write("contact/index.html", h + header("/contact/") + body + footer())


# ================================================================ BEDANKT & 404
def bedankt():
    h = head("Bedankt, we hebben je aanvraag | CarClean Midden-Groningen",
             "Je aanvraag is verstuurd. We nemen binnen een uur op werkdagen contact met je op.", "/bedankt/", noindex=True)
    body = f"""
<section class="page-hero">
  <div class="hero__bg" aria-hidden="true"></div>
  <div class="container thanks">
    <div class="thanks__mark"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>
    <span class="eyebrow">Verstuurd</span>
    <h1><span class="sheen">Top<span data-thanks-name></span>, we hebben het!</span></h1>
    <p class="lead" data-thanks-lead>Je bericht is goed aangekomen. Dit gebeurt er nu:</p>
    <ol class="timeline" role="list">
      <li><span class="when">Binnen 1 uur</span><div><strong>We nemen contact op</strong><p>Op werkdagen bellen of appen we je om alles door te nemen en een moment te bevestigen.</p></div></li>
      <li><span class="when">Vooraf</span><div><strong>Je weet wat het kost</strong><p>Je krijgt de prijs vooraf, inclusief eventuele haal &amp; breng. Geen verrassingen.</p></div></li>
      <li><span class="when">Op de dag</span><div><strong>Glans</strong><p>Breng je auto langs of wij halen hem op. Daarna: showroomglans.</p></div></li>
    </ol>
    <div class="btn-row btn-row--center">
      <a class="btn btn--primary" href="{WA}" target="_blank" rel="noopener">{i("whatsapp")} Haast? App ons</a>
      <a class="btn btn--ghost" href="/">Terug naar home</a>
    </div>
  </div>
</section>
"""
    write("bedankt/index.html", h + header("") + body + footer())


def notfound():
    h = head("Pagina niet gevonden | CarClean Midden-Groningen", "Deze pagina bestaat niet (meer).", "/404", noindex=True)
    body = f"""
<section class="page-hero">
  <div class="hero__bg" aria-hidden="true"></div>
  <div class="container thanks">
    <span class="eyebrow">Fout 404</span>
    <h1><span class="sheen">Deze pagina is weggepoetst.</span></h1>
    <p class="lead">De pagina die je zoekt bestaat niet (meer). Geen zorgen, je auto kan nog steeds glanzen.</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--primary" href="/">Naar home {ARROW}</a>
      <a class="btn btn--ghost" href="/diensten/">Diensten &amp; prijzen</a>
    </div>
  </div>
</section>
"""
    write("404.html", h + header("") + body + footer())


home(); diensten(); over(); afspraak(); contact(); bedankt(); notfound()
