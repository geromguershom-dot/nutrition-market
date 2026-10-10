#!/usr/bin/env python3
"""Génère les pages statiques de Nutrition & Market.

Usage :  python3 build.py
Les pages HTML sont écrites à la racine du dossier (prêtes pour Vercel / GitHub Pages).
Pour modifier le contenu, éditez les listes ci-dessous (produits, annonces, articles…),
puis relancez la commande.
"""
import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent

# ----------------------------------------------------------------------------
# Informations de l'entreprise
# ----------------------------------------------------------------------------
SITE = "Nutrition & Market"
TAGLINE = "Santé • Nutrition • Agriculture"
BASELINE = ("Votre partenaire pour une vie saine, une agriculture productive "
            "et une nutrition cellulaire optimale.")
WA_NUMBER = "237682091580"
PHONE = "+237 6 82 09 15 80"
PHONE_HREF = "+237682091580"
EMAIL = "geromguershom@gmail.com"
CITY = "Yaoundé, Cameroun"
HOURS = "Lun - Sam : 8h00 - 18h00"
YEAR = 2026

# ----------------------------------------------------------------------------
# Contenu
# ----------------------------------------------------------------------------
PRODUCTS = [
    dict(id="aloe-vera-gel", name="Forever Aloe Vera Gel", price=15000, img="aloe-vera", new=True),
    dict(id="bee-pollen", name="Forever Bee Pollen", price=12000, img="bee-pollen", new=False),
    dict(id="arctic-sea", name="Forever Arctic Sea", price=18000, img="arctic-sea", new=False),
    dict(id="immublend", name="Forever ImmuBlend", price=20000, img="immunoblend", new=False),
    dict(id="protein", name="Forever Protein", price=25000, img="protein", new=True),
]

FORMATIONS = [
    dict(title="Nutrition Cellulaire", level="Débutant", modules=12, img="formation-nutrition"),
    dict(title="Santé & Bien-être", level="Intermédiaire", modules=15, img="formation-wellness"),
    dict(title="Agriculture Durable", level="Professionnel", modules=18, img="formation-agriculture"),
]

# "end" : date ISO après laquelle l'annonce est affichée comme terminée (ou None)
ANNONCES = [
    dict(title="Promotion spéciale Aloe Vera Gel", text="-20% jusqu'au 30 Juin 2025",
         date="20 Mai 2025", end="2025-06-30", kind="Promotion", ended="Promotion terminée",
         img="aloe-vera"),
    dict(title="Nouvel arrivage de produits", text="Découvrez nos nouveaux produits",
         date="18 Mai 2025", end=None, kind="Actualité", ended="",
         img="annonce-products"),
    dict(title="Séminaire Nutrition & Santé", text="Rejoignez-nous ce 15 Juin à Yaoundé",
         date="15 Mai 2025", end="2025-06-15", kind="Événement", ended="Événement passé",
         img="annonce-seminar"),
]

# "youtube" : identifiant d'une vidéo YouTube (ex. "dQw4w9WgXcQ"). None = « bientôt disponible ».
VIDEOS = [
    dict(title="Comment utiliser l'Aloe Vera", cat="Conseils d'utilisation",
         img="conseil-aloe", youtube=None),
    dict(title="Boostez votre immunité", cat="Santé cellulaire",
         img="conseil-immunity", youtube=None),
    dict(title="Astuces pour une agriculture productive", cat="Agriculture",
         img="conseil-agriculture", youtube=None),
]

HEALTH_NOTE = ("Les besoins varient d'une personne à l'autre (âge, climat, activité, état de santé). "
               "En cas de doute ou de pathologie, demandez conseil à un professionnel de santé.")

ARTICLES = [
    dict(
        slug="bien-s-hydrater-au-quotidien", cat="Santé", img="social-tips",
        title="Bien s'hydrater au quotidien", date="10 Octobre 2026", minutes=3,
        excerpt="Quelques repères simples pour boire suffisamment, même quand il fait chaud et que la journée est chargée.",
        body=[
            ("p", "L'eau participe à presque toutes les fonctions du corps : digestion, régulation de la température, transport des nutriments. Pourtant, on oublie facilement de boire quand on est occupé, surtout sous la chaleur."),
            ("h2", "Des repères simples"),
            ("ul", [
                "Buvez régulièrement tout au long de la journée plutôt qu'une grande quantité d'un coup.",
                "Gardez une bouteille d'eau à portée de main : au travail, dans le taxi, au marché.",
                "Une urine claire ou jaune pâle est généralement bon signe ; une urine très foncée invite à boire davantage.",
                "Augmentez vos apports quand il fait très chaud, quand vous transpirez beaucoup ou après un effort.",
            ]),
            ("h2", "Et à manger aussi"),
            ("p", "Beaucoup de fruits et de légumes contiennent énormément d'eau : pastèque, ananas, concombre, tomate, papaye. Ils complètent utilement l'eau que vous buvez."),
            ("h2", "À limiter"),
            ("p", "Les boissons très sucrées apportent beaucoup de calories sans bien rassasier. Gardez-les pour les occasions et préférez l'eau, éventuellement parfumée avec quelques tranches de citron ou de concombre."),
            ("note", HEALTH_NOTE),
        ]),
    dict(
        slug="assiette-equilibree-produits-locaux", cat="Nutrition", img="social-smoothie",
        title="Composer une assiette équilibrée avec des produits locaux",
        date="10 Octobre 2026", minutes=4,
        excerpt="Féculents, légumes, protéines, fruits : comment équilibrer vos repas avec ce que l'on trouve au marché.",
        body=[
            ("p", "Manger équilibré ne demande pas de produits chers ou importés. Les marchés camerounais regorgent d'aliments variés et de saison."),
            ("h2", "Le principe de l'assiette"),
            ("ul", [
                "Environ la moitié de l'assiette en légumes et en fruits : feuilles de manioc, épinards, gombo, tomates, carottes, mangue, papaye.",
                "Un quart en féculents : plantain, manioc, igname, macabo, riz ou maïs.",
                "Un quart en protéines : poisson, œufs, haricots, arachides, poulet.",
            ]),
            ("h2", "Quelques habitudes utiles"),
            ("ul", [
                "Variez les couleurs : plus l'assiette est colorée, plus elle est variée.",
                "Préférez les cuissons à l'eau, à la vapeur ou au four aux fritures répétées.",
                "Allez-y doucement sur le sel et les cubes d'assaisonnement.",
                "Gardez les fruits entiers plutôt qu'en jus : ils rassasient mieux.",
            ]),
            ("p", "Il n'existe pas d'assiette parfaite : l'important est la régularité. Changer une habitude à la fois est plus durable qu'une transformation radicale."),
            ("note", HEALTH_NOTE),
        ]),
    dict(
        slug="bases-du-potager-sol-vivant", cat="Agriculture", img="conseil-agriculture",
        title="Les bases d'un sol vivant au potager", date="10 Octobre 2026", minutes=3,
        excerpt="Compost, paillage, rotation des cultures : trois gestes simples pour un sol plus fertile et des récoltes plus régulières.",
        body=[
            ("p", "Un sol riche en matière organique retient mieux l'eau, nourrit les plantes et demande moins d'intrants. Trois gestes suffisent pour commencer."),
            ("h2", "1. Le compost"),
            ("p", "Rassemblez épluchures, feuilles, restes de cultures et fumier bien décomposé. Au bout de quelques mois, ce mélange devient un amendement noir et friable qui améliore la structure du sol. Évitez d'y mettre de la viande, du poisson ou de l'huile."),
            ("h2", "2. Le paillage"),
            ("p", "Couvrir le sol de paille, de feuilles sèches ou de résidus de culture limite l'évaporation, freine les mauvaises herbes et protège le sol des fortes pluies."),
            ("h2", "3. La rotation des cultures"),
            ("p", "Ne cultivez pas la même famille de plantes au même endroit chaque saison. Alterner légumes-feuilles, légumes-racines et légumineuses (haricots, arachides) réduit les maladies et équilibre les besoins du sol."),
            ("h2", "Un dernier réflexe"),
            ("p", "Arrosez tôt le matin ou en fin de journée pour limiter les pertes d'eau, et observez vos plantes : feuilles jaunies, croissance lente ou taches sont des signaux à ne pas ignorer."),
        ]),
]

TIPS = [
    ("fa-tint", "Hydratation", "Buvez régulièrement dans la journée, davantage quand il fait chaud ou après un effort."),
    ("fa-apple-alt", "Assiette variée", "Légumes, féculents et protéines à chaque repas, avec des produits de saison."),
    ("fa-walking", "Mouvement", "Marchez, dansez, bougez : une demi-heure par jour est un bon objectif pour beaucoup d'adultes."),
    ("fa-moon", "Sommeil", "Couchez-vous à heures régulières : un sommeil suffisant soutient l'énergie et l'humeur."),
    ("fa-calendar-check", "Régularité", "De petits changements durables valent mieux qu'un grand changement abandonné."),
    ("fa-tags", "Lire les étiquettes", "Vérifiez la composition, la date de péremption et le mode d'emploi de chaque produit."),
]

UNIVERS = [
    ("fa-seedling", "Agriculture", "Des solutions efficaces pour des cultures saines et productives."),
    ("fa-heartbeat", "Santé Cellulaire", "Renforcez vos cellules, votre énergie et votre immunité."),
    ("fa-apple-alt", "Nutrition Cellulaire", "Nourrissez votre corps à la source pour une vie plus saine."),
]

ENGAGEMENTS = [
    ("fa-truck", "Livraison rapide", "Partout au Cameroun"),
    ("fa-hand-holding-usd", "Paiement à la livraison", "Paiement sécurisé"),
    ("fa-certificate", "Produits authentiques", "Qualité garantie"),
    ("fa-headset", "Service client à l'écoute", "Nous sommes là pour vous"),
]

FAQ = [
    ("Livrez-vous partout au Cameroun ?", "Oui, nous assurons une livraison rapide partout au Cameroun."),
    ("Comment puis-je payer ?", "Le paiement se fait à la livraison."),
    ("Comment passer commande ?", "Ajoutez vos produits au panier puis envoyez la commande par WhatsApp, ou écrivez-nous directement via le formulaire de contact."),
    ("Quels sont vos horaires ?", "Nous sommes joignables du lundi au samedi, de 8h00 à 18h00."),
]

NAV = [
    ("accueil", "Accueil", "index.html"),
    ("boutique", "Boutique", "boutique.html"),
    ("conseils", "Conseils", "conseils.html"),
    ("formations", "Formations", "formations.html"),
    ("annonces", "Annonces", "annonces.html"),
    ("blog", "Blog", "blog.html"),
    ("videos", "Vidéos", "videos.html"),
    ("apropos", "À propos", "a-propos.html"),
    ("contact", "Contact", "contact.html"),
]


# ----------------------------------------------------------------------------
# Utilitaires
# ----------------------------------------------------------------------------
def esc(s):
    return html.escape(str(s), quote=True)


def fcfa(n):
    return f"{n:,}".replace(",", "\u00a0") + "\u00a0FCFA"


def wa_link(msg):
    return f"https://wa.me/{WA_NUMBER}?text={quote(msg)}"


def article_href(a):
    return f"article-{a['slug']}.html"


PETAL = "M0,-3 C13,-9 13,-27 0,-32 C-13,-27 -13,-9 0,-3Z"
LOGO_SVG = """<svg viewBox="-34 -34 68 68" width="{s}" height="{s}" aria-hidden="true">
<path d="{p}" fill="{c1}"/>
<path transform="rotate(90)" d="{p}" fill="{c2}"/>
<path transform="rotate(180)" d="{p}" fill="{c1}"/>
<path transform="rotate(270)" d="{p}" fill="{c2}"/>
<circle r="5" fill="#e8a838"/></svg>"""


def logo(light=False, size=45):
    svg = LOGO_SVG.format(s=size, p=PETAL,
                          c1="#ffffff" if light else "#2d5016",
                          c2="#a8d86a" if light else "#4a7c23")
    tagline = "" if light else f'<span class="logo-tagline">{esc(TAGLINE)}</span>'
    return f"""<a href="index.html" class="logo" aria-label="{esc(SITE)} – accueil">
<div class="logo-icon">{svg}</div>
<div class="logo-text"><span class="logo-name">NUTRITION</span><span class="logo-amp">&amp; MARKET</span>{tagline}</div></a>"""


# ----------------------------------------------------------------------------
# Composants
# ----------------------------------------------------------------------------
def product_card(p):
    badge = '<div class="product-badge badge-new">Nouveau</div>' if p["new"] else ""
    msg = f"Bonjour {SITE}, je souhaite commander : {p['name']} ({fcfa(p['price'])})."
    return f"""<div class="product-card reveal" data-id="{p['id']}" data-new="{int(p['new'])}" data-price="{p['price']}">
{badge}
<div class="product-img"><img src="images/{p['img']}.webp" alt="{esc(p['name'])}" loading="lazy" width="400" height="400"></div>
<div class="product-info">
<h3>{esc(p['name'])}</h3>
<p class="product-price">{fcfa(p['price'])}</p>
<div class="product-actions">
<a href="{wa_link(msg)}" class="btn-details" target="_blank" rel="noopener">Commander <i class="fab fa-whatsapp"></i></a>
<button class="btn-cart" type="button" data-add="{p['id']}" aria-label="Ajouter {esc(p['name'])} au panier" title="Ajouter au panier"><i class="fas fa-shopping-cart"></i></button>
</div></div></div>"""


def formation_card(f, with_cta=False):
    cta = ""
    if with_cta:
        msg = f"Bonjour {SITE}, je souhaite des informations sur la formation « {f['title']} »."
        cta = f'<a href="{wa_link(msg)}" class="btn btn-primary formation-cta" target="_blank" rel="noopener"><i class="fab fa-whatsapp"></i> Demander le programme</a>'
    return f"""<div class="formation-card reveal">
<div class="formation-img"><img src="images/{f['img']}.webp" alt="{esc(f['title'])}" loading="lazy"></div>
<div class="formation-info">
<h3>{esc(f['title'])}</h3>
<p class="formation-level">{esc(f['level'])}</p>
<div class="formation-meta"><i class="fas fa-book"></i> {f['modules']} modules</div>
{cta}
</div></div>"""


def annonce_card(a):
    end = f' data-end="{a["end"]}" data-ended-label="{esc(a["ended"])}"' if a["end"] else ""
    return f"""<div class="annonce-card reveal"{end}>
<div class="annonce-img"><img src="images/{a['img']}.webp" alt="{esc(a['title'])}" loading="lazy"></div>
<div class="annonce-info">
<span class="tag">{esc(a['kind'])}</span><span class="tag tag-ended" hidden></span>
<h4>{esc(a['title'])}</h4>
<p>{esc(a['text'])}</p>
<span class="annonce-date">{esc(a['date'])}</span>
</div></div>"""


def article_card(a):
    return f"""<article class="blog-card reveal">
<a href="{article_href(a)}"><img src="images/{a['img']}.webp" alt="{esc(a['title'])}" loading="lazy"></a>
<div class="blog-card-body">
<span class="tag">{esc(a['cat'])}</span>
<h3><a href="{article_href(a)}">{esc(a['title'])}</a></h3>
<p>{esc(a['excerpt'])}</p>
<div class="blog-meta"><span>{esc(a['date'])}</span><span>{a['minutes']} min de lecture</span></div>
</div></article>"""


def video_card(v):
    if v["youtube"]:
        media = (f'<div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/{v["youtube"]}" '
                 f'title="{esc(v["title"])}" loading="lazy" allowfullscreen></iframe></div>')
    else:
        media = (f'<div class="video-thumb"><img src="images/{v["img"]}.webp" alt="{esc(v["title"])}" loading="lazy">'
                 '<div class="play-btn"><i class="fas fa-play"></i></div>'
                 '<span class="soon-badge">Bientôt disponible</span></div>')
    return f"""<div class="conseil-video-card reveal">{media}
<p>{esc(v['title'])}</p><small>{esc(v['cat'])}</small></div>"""


def page_hero(title, subtitle, crumbs=None):
    trail = f'<a href="index.html">Accueil</a>'
    for label, href in (crumbs or []):
        trail += f' <i class="fas fa-chevron-right"></i> <a href="{href}">{esc(label)}</a>'
    trail += f' <i class="fas fa-chevron-right"></i> <span>{esc(title)}</span>'
    return f"""<section class="page-hero"><div class="container">
<nav class="breadcrumb" aria-label="Fil d'Ariane">{trail}</nav>
<h1>{esc(title)}</h1><p>{esc(subtitle)}</p></div></section>"""


def whatsapp_cta(text, label="Nous écrire sur WhatsApp", msg="Bonjour, j'aimerais un conseil personnalisé."):
    return f"""<div class="cta-band"><div><h3>{esc(text)}</h3></div>
<a href="{wa_link(msg)}" class="btn btn-whatsapp" target="_blank" rel="noopener"><i class="fab fa-whatsapp"></i> {esc(label)}</a></div>"""


# ----------------------------------------------------------------------------
# Gabarit commun
# ----------------------------------------------------------------------------
def layout(key, title, description, body):
    nav_items = []
    for k, label, href in NAV:
        active = ' class="active" aria-current="page"' if k == key else ""
        if k == "boutique":
            nav_items.append(f"""<li class="dropdown"><a href="{href}"{active}>{label} <i class="fas fa-chevron-down"></i></a>
<ul class="dropdown-menu"><li><a href="boutique.html">Tous les produits</a></li>
<li><a href="boutique.html?filtre=nouveau">Nouveautés</a></li></ul></li>""")
        else:
            nav_items.append(f'<li><a href="{href}"{active}>{label}</a></li>')
    nav = "\n".join(nav_items)

    footer_links = "\n".join(f'<li><a href="{h}">{l}</a></li>' for _, l, h in NAV)
    products_json = json.dumps({p["id"]: {"name": p["name"], "price": p["price"]} for p in PRODUCTS},
                               ensure_ascii=False)
    full_title = SITE if key == "accueil" else f"{title} – {SITE}"
    float_link = wa_link("Bonjour, j'aimerais un conseil personnalisé.")
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:image" content="images/hero.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="icon" href="images/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>

<div class="top-bar"><div class="container">
<span>{esc(BASELINE)}</span>
<div class="top-bar-right">
<div class="social-links">
<a href="#" title="Facebook" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
<a href="#" title="Instagram" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
<a href="#" title="TikTok" aria-label="TikTok"><i class="fab fa-tiktok"></i></a>
<a href="#" title="YouTube" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
</div>
<a href="tel:{PHONE_HREF}" class="phone-link"><i class="fas fa-phone"></i> {PHONE}</a>
</div></div></div>

<header class="header" id="header"><div class="container"><div class="header-content">
{logo()}
<nav class="main-nav" id="mainNav" aria-label="Navigation principale"><ul>
{nav}
</ul></nav>
<div class="header-actions">
<button class="btn-commander" id="cartOpen" type="button" aria-label="Ouvrir le panier"><i class="fas fa-shopping-cart"></i> Panier <span class="cart-count" id="cartCount">0</span></button>
<button class="mobile-toggle" id="mobileToggle" type="button" aria-label="Ouvrir le menu" aria-expanded="false"><i class="fas fa-bars"></i><span class="toggle-fallback">Menu</span></button>
</div>
</div></div></header>

<main>
{body}
</main>

<section class="trust-bar"><div class="container"><div class="trust-grid">
{''.join(f'<div class="trust-item"><i class="fas {i}"></i><div><strong>{esc(t)}</strong><span>{esc(s)}</span></div></div>' for i, t, s in ENGAGEMENTS)}
</div></div></section>

<a href="{float_link}" class="whatsapp-float" target="_blank" rel="noopener" aria-label="Contacter par WhatsApp">
<div class="whatsapp-tooltip">Besoin d'un conseil personnalisé ?<br>Contactez-nous sur WhatsApp</div>
<i class="fab fa-whatsapp"></i></a>

<footer class="footer"><div class="container">
<div class="footer-grid">
<div class="footer-brand">
{logo(light=True, size=40)}
<p>{esc(BASELINE)}</p>
<div class="footer-social">
<a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
<a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
<a href="#" aria-label="TikTok"><i class="fab fa-tiktok"></i></a>
<a href="#" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
</div></div>
<div class="footer-newsletter">
<h3>Newsletter</h3>
<p>Inscrivez-vous pour recevoir nos conseils santé, nos offres et nos nouveautés.</p>
<form class="newsletter-form" id="newsletterForm">
<input type="email" placeholder="Votre email" aria-label="Votre email" required>
<button type="submit" aria-label="S'inscrire"><i class="fas fa-paper-plane"></i></button>
</form>
<p class="form-feedback" id="newsletterFeedback" role="status" hidden></p>
</div>
<div class="footer-links"><h3>Liens rapides</h3><ul>
{footer_links}
</ul></div>
<div class="footer-contact"><h3>Contact</h3><ul>
<li><i class="fas fa-phone"></i> <a href="tel:{PHONE_HREF}">{PHONE}</a></li>
<li><i class="fas fa-envelope"></i> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><i class="fas fa-map-marker-alt"></i> {esc(CITY)}</li>
<li><i class="fas fa-clock"></i> {esc(HOURS)}</li>
</ul></div>
</div>
<div class="footer-bottom"><p>&copy; {YEAR} {esc(SITE)} — site de démonstration.</p></div>
</div></footer>

<div class="cart-overlay" id="cartOverlay"></div>
<aside class="cart-drawer" id="cartDrawer" aria-label="Panier" aria-hidden="true">
<div class="cart-head"><h2>Votre panier</h2><button type="button" id="cartClose" aria-label="Fermer le panier"><i class="fas fa-times"></i><span class="toggle-fallback">Fermer</span></button></div>
<div class="cart-body" id="cartBody"></div>
<div class="cart-foot">
<div class="cart-total"><span>Total</span><strong id="cartTotal">0&nbsp;FCFA</strong></div>
<a href="#" class="btn btn-whatsapp cart-order" id="cartOrder" target="_blank" rel="noopener"><i class="fab fa-whatsapp"></i> Commander sur WhatsApp</a>
<p class="cart-note">Paiement à la livraison. Votre commande est envoyée par WhatsApp : nous vous confirmons le prix final et la livraison.</p>
</div>
</aside>

<script>window.NM = {{ products: {products_json}, whatsapp: "{WA_NUMBER}", shop: {json.dumps(SITE, ensure_ascii=False)} }};</script>
<script src="script.js"></script>
</body>
</html>
"""


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
def page_index():
    univers = "".join(f"""<a href="a-propos.html#univers" class="univers-card">
<div class="univers-icon"><i class="fas {i}"></i></div>
<div class="univers-info"><h4>{esc(t)}</h4><p>{esc(d)}</p></div>
<i class="fas fa-arrow-right univers-arrow"></i></a>""" for i, t, d in UNIVERS)

    quick = [("fa-store", "Boutique", "Nos produits", "boutique.html"),
             ("fa-lightbulb", "Conseils", "Utilisation & bienfaits", "conseils.html"),
             ("fa-graduation-cap", "Formations", "Apprenez & évoluez", "formations.html"),
             ("fa-bullhorn", "Annonces", "Promotions & actualités", "annonces.html"),
             ("fa-newspaper", "Blog", "Articles & astuces", "blog.html"),
             ("fa-video", "Vidéos", "Conseils en vidéos", "videos.html")]
    quick_html = "".join(f"""<a href="{h}" class="quick-nav-item reveal"><i class="fas {i}"></i><span>{esc(t)}</span><small>{esc(s)}</small></a>"""
                         for i, t, s, h in quick)

    body = f"""
<section class="hero" id="accueil"><div class="container"><div class="hero-grid">
<div class="hero-content">
<h1>Prenez soin de vos cellules,<br><span class="text-highlight">nourrissez votre avenir.</span></h1>
<p class="hero-subtitle">Des produits naturels de qualité pour votre santé, votre bien-être et une agriculture durable.</p>
<div class="hero-features">
<div class="hero-feature"><i class="fas fa-leaf"></i><span>Produits naturels</span></div>
<div class="hero-feature"><i class="fas fa-check-circle"></i><span>Qualité garantie</span></div>
<div class="hero-feature"><i class="fas fa-truck"></i><span>Livraison rapide</span></div>
<div class="hero-feature"><i class="fas fa-shield-alt"></i><span>Paiement à la livraison</span></div>
</div>
<div class="hero-buttons">
<a href="boutique.html" class="btn btn-primary">Découvrir nos produits <i class="fas fa-arrow-right"></i></a>
<a href="contact.html" class="btn btn-secondary"><i class="fab fa-whatsapp"></i> Nous contacter</a>
</div></div>
<div class="hero-visual">
<div class="hero-image-wrapper"><img src="images/hero.webp" alt="Produits nutritionnels naturels" class="hero-main-img" width="1200" height="800"></div>
<div class="univers-cards"><h3 class="univers-title">Nos 3 Univers</h3>{univers}</div>
</div></div></div></section>

<section class="quick-nav"><div class="container"><div class="quick-nav-grid">{quick_html}</div></div></section>

<section class="products"><div class="container">
<div class="section-header"><h2>Nos produits phares</h2>
<a href="boutique.html" class="btn-link">Voir tous les produits <i class="fas fa-arrow-right"></i></a></div>
<div class="products-grid">{''.join(product_card(p) for p in PRODUCTS)}</div>
</div></section>

<section class="conseils"><div class="container"><div class="conseils-grid">
<div class="conseils-content">
<h2>Des conseils personnalisés<br>pour chaque produit</h2>
<p>Découvrez nos conseils d'utilisation, explications détaillées, modes d'emploi et recommandations pour tirer le meilleur de chaque produit.</p>
<a href="conseils.html" class="btn btn-primary">Explorer nos conseils <i class="fas fa-arrow-right"></i></a>
</div>
<div class="conseils-videos">{''.join(video_card(v) for v in VIDEOS)}</div>
</div></div></section>

<section class="formations"><div class="container"><div class="formations-grid">
<div class="formations-content">
<h2>Nos formations</h2>
<p>Développez vos connaissances en nutrition cellulaire, santé et agriculture grâce à nos formations pratiques.</p>
<a href="formations.html" class="btn btn-primary">Voir toutes les formations <i class="fas fa-arrow-right"></i></a>
</div>
<div class="formations-cards">{''.join(formation_card(f) for f in FORMATIONS)}</div>
</div></div></section>

<section class="annonces"><div class="container">
<div class="section-header"><h2>Annonces &amp; Actualités</h2></div>
<div class="annonces-grid">{''.join(annonce_card(a) for a in ANNONCES)}</div>
<div class="section-footer"><a href="annonces.html" class="btn-link">Voir toutes les annonces <i class="fas fa-arrow-right"></i></a></div>
</div></section>

<section class="page-section blog-preview"><div class="container">
<div class="section-header"><h2>Derniers articles</h2>
<a href="blog.html" class="btn-link">Voir le blog <i class="fas fa-arrow-right"></i></a></div>
<div class="blog-grid">{''.join(article_card(a) for a in ARTICLES)}</div>
</div></section>
"""
    return layout("accueil", SITE, BASELINE + " Produits naturels de qualité au Cameroun.", body)


def page_boutique():
    body = page_hero("Boutique", "Des produits naturels de qualité, livrés partout au Cameroun. Paiement à la livraison.") + f"""
<section class="page-section"><div class="container">
<div class="filters-bar">
<div class="filters" role="group" aria-label="Filtrer les produits">
<button class="filter-btn active" type="button" data-filter="all">Tous</button>
<button class="filter-btn" type="button" data-filter="new">Nouveautés</button>
</div>
<label class="sort-label">Trier par
<select class="sort-select" id="sortSelect">
<option value="default">Sélection</option>
<option value="asc">Prix croissant</option>
<option value="desc">Prix décroissant</option>
</select></label>
</div>
<div class="products-grid is-catalog" id="catalog">{''.join(product_card(p) for p in PRODUCTS)}</div>
<p class="empty-state" id="catalogEmpty" hidden>Aucun produit ne correspond à ce filtre.</p>
{whatsapp_cta("Une question sur un produit ?", msg="Bonjour, j'ai une question sur un de vos produits.")}
</div></section>"""
    return layout("boutique", "Boutique", "Découvrez les produits Nutrition & Market : santé cellulaire, nutrition, bien-être. Livraison partout au Cameroun.", body)


def page_conseils():
    tips = "".join(f"""<div class="tip-card reveal"><div class="tip-icon"><i class="fas {i}"></i></div>
<h3>{esc(t)}</h3><p>{esc(d)}</p></div>""" for i, t, d in TIPS)
    body = page_hero("Conseils", "Des repères simples pour une vie plus saine, au quotidien.") + f"""
<section class="page-section"><div class="container">
<div class="tips-grid">{tips}</div>
<p class="legal-note"><i class="fas fa-info-circle"></i> {esc(HEALTH_NOTE)}</p>
</div></section>
<section class="page-section alt"><div class="container">
<div class="section-header"><h2>Conseils en vidéo</h2><a href="videos.html" class="btn-link">Toutes les vidéos <i class="fas fa-arrow-right"></i></a></div>
<div class="video-grid">{''.join(video_card(v) for v in VIDEOS)}</div>
</div></section>
<section class="page-section"><div class="container">
<div class="section-header"><h2>À lire sur le blog</h2><a href="blog.html" class="btn-link">Tous les articles <i class="fas fa-arrow-right"></i></a></div>
<div class="blog-grid">{''.join(article_card(a) for a in ARTICLES)}</div>
{whatsapp_cta("Besoin d'un conseil personnalisé pour un produit ?")}
</div></section>"""
    return layout("conseils", "Conseils", "Conseils santé, nutrition et agriculture : repères simples pour une vie plus saine au quotidien.", body)


def page_formations():
    body = page_hero("Formations", "Développez vos connaissances en nutrition cellulaire, santé et agriculture grâce à des formations pratiques.") + f"""
<section class="page-section"><div class="container">
<div class="formations-page-grid">{''.join(formation_card(f, with_cta=True) for f in FORMATIONS)}</div>
{whatsapp_cta("Une question sur nos formations ?", msg="Bonjour, j'ai une question sur vos formations.")}
</div></section>"""
    return layout("formations", "Formations", "Formations en nutrition cellulaire, santé & bien-être et agriculture durable, du niveau débutant au niveau professionnel.", body)


def page_annonces():
    body = page_hero("Annonces & Actualités", "Promotions, nouveaux arrivages et événements : restez informé.") + f"""
<section class="page-section"><div class="container">
<div class="annonces-grid">{''.join(annonce_card(a) for a in ANNONCES)}</div>
<p class="legal-note"><i class="fas fa-bell"></i> Pour ne rien manquer, inscrivez-vous à la newsletter en bas de page ou suivez-nous sur WhatsApp.</p>
</div></section>"""
    return layout("annonces", "Annonces", "Promotions, nouveautés et événements Nutrition & Market.", body)


def page_blog():
    body = page_hero("Blog", "Articles et astuces sur la nutrition, la santé et l'agriculture.") + f"""
<section class="page-section"><div class="container">
<div class="blog-grid">{''.join(article_card(a) for a in ARTICLES)}</div>
</div></section>"""
    return layout("blog", "Blog", "Articles et astuces sur la nutrition, la santé et l'agriculture.", body)


def page_article(a):
    parts = []
    for kind, content in a["body"]:
        if kind == "p":
            parts.append(f"<p>{esc(content)}</p>")
        elif kind == "h2":
            parts.append(f"<h2>{esc(content)}</h2>")
        elif kind == "ul":
            parts.append("<ul>" + "".join(f"<li>{esc(i)}</li>" for i in content) + "</ul>")
        elif kind == "note":
            parts.append(f'<p class="legal-note"><i class="fas fa-info-circle"></i> {esc(content)}</p>')
    others = [x for x in ARTICLES if x["slug"] != a["slug"]]
    body = page_hero(a["title"], a["excerpt"], crumbs=[("Blog", "blog.html")]) + f"""
<section class="page-section"><div class="container">
<article class="article">
<div class="article-meta"><span class="tag">{esc(a['cat'])}</span><span>{esc(a['date'])}</span><span>{a['minutes']} min de lecture</span></div>
<img class="article-img" src="images/{a['img']}.webp" alt="{esc(a['title'])}" width="1200" height="675">
{''.join(parts)}
</article>
</div></section>
<section class="page-section alt"><div class="container">
<div class="section-header"><h2>À lire aussi</h2></div>
<div class="blog-grid">{''.join(article_card(x) for x in others)}</div>
</div></section>"""
    return layout("blog", a["title"], a["excerpt"], body)


def page_videos():
    body = page_hero("Vidéos", "Nos conseils en vidéo : utilisation des produits, santé cellulaire et agriculture.") + f"""
<section class="page-section"><div class="container">
<div class="video-grid">{''.join(video_card(v) for v in VIDEOS)}</div>
{whatsapp_cta("Une vidéo à nous suggérer ?", label="Proposer un sujet", msg="Bonjour, j'aimerais voir une vidéo sur le sujet suivant : ")}
</div></section>"""
    return layout("videos", "Vidéos", "Conseils en vidéo : utilisation des produits, santé cellulaire, agriculture.", body)


def page_apropos():
    univers = "".join(f"""<div class="tip-card reveal"><div class="tip-icon"><i class="fas {i}"></i></div>
<h3>{esc(t)}</h3><p>{esc(d)}</p></div>""" for i, t, d in UNIVERS)
    eng = "".join(f"""<div class="tip-card reveal"><div class="tip-icon"><i class="fas {i}"></i></div>
<h3>{esc(t)}</h3><p>{esc(s)}</p></div>""" for i, t, s in ENGAGEMENTS)
    body = page_hero("À propos", "Votre partenaire pour une vie saine, une agriculture productive et une nutrition cellulaire optimale.") + f"""
<section class="page-section"><div class="container">
<div class="about-intro">
<h2>Notre mission</h2>
<p>{esc(SITE)} accompagne les Camerounais vers une meilleure santé grâce à des produits naturels de qualité, à des conseils clairs et à des formations pratiques. Nous réunissons trois univers : l'agriculture, la santé cellulaire et la nutrition cellulaire.</p>
</div>
</div></section>
<section class="page-section alt" id="univers"><div class="container">
<div class="section-header"><h2>Nos 3 univers</h2></div>
<div class="tips-grid three">{univers}</div>
</div></section>
<section class="page-section"><div class="container">
<div class="section-header"><h2>Nos engagements</h2></div>
<div class="tips-grid four">{eng}</div>
</div></section>
<section class="page-section alt"><div class="container">
<div class="section-header"><h2>Nous trouver</h2></div>
<ul class="info-list">
<li><i class="fas fa-map-marker-alt"></i> {esc(CITY)}</li>
<li><i class="fas fa-clock"></i> {esc(HOURS)}</li>
<li><i class="fas fa-phone"></i> <a href="tel:{PHONE_HREF}">{PHONE}</a></li>
<li><i class="fas fa-envelope"></i> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
</ul>
{whatsapp_cta("Parlons de vos besoins", label="Nous contacter")}
</div></section>"""
    return layout("apropos", "À propos", "Nutrition & Market : produits naturels, conseils et formations en nutrition, santé cellulaire et agriculture, à Yaoundé.", body)


def page_contact():
    contact_wa = wa_link("Bonjour, j'ai une question.")
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(r)}</p></details>" for q, r in FAQ)
    body = page_hero("Contact", "Une question, une commande, un conseil ? Écrivez-nous, nous répondons rapidement.") + f"""
<section class="page-section"><div class="container"><div class="contact-grid">
<div class="contact-info">
<h2>Nos coordonnées</h2>
<ul class="info-list">
<li><i class="fas fa-phone"></i> <a href="tel:{PHONE_HREF}">{PHONE}</a></li>
<li><i class="fab fa-whatsapp"></i> <a href="{contact_wa}" target="_blank" rel="noopener">WhatsApp</a></li>
<li><i class="fas fa-envelope"></i> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><i class="fas fa-map-marker-alt"></i> {esc(CITY)}</li>
<li><i class="fas fa-clock"></i> {esc(HOURS)}</li>
</ul>
<h2 class="faq-title">Questions fréquentes</h2>
<div class="faq">{faq}</div>
</div>
<form class="contact-form" id="contactForm" novalidate>
<h2>Envoyez-nous un message</h2>
<div class="form-group"><label for="cf-name">Nom</label><input id="cf-name" name="name" type="text" required autocomplete="name"></div>
<div class="form-group"><label for="cf-phone">Téléphone</label><input id="cf-phone" name="phone" type="tel" autocomplete="tel" placeholder="+237 ..."></div>
<div class="form-group"><label for="cf-subject">Sujet</label>
<select id="cf-subject" name="subject">
<option>Commande</option><option>Conseil personnalisé</option><option>Formation</option><option>Autre</option></select></div>
<div class="form-group"><label for="cf-message">Message</label><textarea id="cf-message" name="message" rows="5" required></textarea></div>
<button type="submit" class="btn btn-whatsapp"><i class="fab fa-whatsapp"></i> Envoyer sur WhatsApp</button>
<p class="form-feedback" id="contactFeedback" role="status" hidden></p>
<p class="cart-note">Votre message s'ouvre dans WhatsApp, prêt à être envoyé à notre équipe.</p>
</form>
</div></div></section>"""
    return layout("contact", "Contact", "Contactez Nutrition & Market à Yaoundé : commande, conseil personnalisé, formation.", body)


# ----------------------------------------------------------------------------
def main():
    pages = {
        "index.html": page_index(),
        "boutique.html": page_boutique(),
        "conseils.html": page_conseils(),
        "formations.html": page_formations(),
        "annonces.html": page_annonces(),
        "blog.html": page_blog(),
        "videos.html": page_videos(),
        "a-propos.html": page_apropos(),
        "contact.html": page_contact(),
    }
    for a in ARTICLES:
        pages[article_href(a)] = page_article(a)
    for name, content in pages.items():
        (ROOT / name).write_text(content, encoding="utf-8")
    print(f"{len(pages)} pages générées :")
    for name in pages:
        print("  -", name)


if __name__ == "__main__":
    main()
