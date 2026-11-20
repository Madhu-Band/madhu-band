#!/usr/bin/env python3
"""Generate the Madhu site's HTML pages from tools/content/*.json.
Run from anywhere:  python3 tools/build.py
"""
import json, html, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "tools" / "content"
site = json.loads((CONTENT / "site.json").read_text(encoding="utf-8"))
shows = json.loads((CONTENT / "shows.json").read_text(encoding="utf-8"))

esc = lambda s: html.escape(str(s), quote=True)
NAME = site["name"]
URL = site["url"].rstrip("/")
YEAR = datetime.date.today().year
NAV = [("index.html", "Home"), ("about.html", "About"), ("music.html", "Music"),
       ("shows.html", "Shows"), ("epk.html", "EPK"), ("contact.html", "Contact")]

def page(filename, title, description, body, current, scripts=False):
    nav = "".join(
        f'<a href="{href}"' + (' aria-current="page"' if href == current else "") + f">{label}</a>"
        for href, label in NAV)
    path = "" if filename == "index.html" else filename
    full_title = NAME if filename == "index.html" else f"{title} | {NAME}"
    shows_json = json.dumps(shows).replace("</", "<\\/")
    extra = (f'<script id="shows-data" type="application/json">{shows_json}</script>\n'
             '<script src="js/site.js" defer></script>\n') if scripts else ""
    email = site.get("email", "").strip()
    footer_contact = (f'<a href="mailto:{esc(email)}">{esc(email)}</a>' if email
                      else '<a href="contact.html">Contact</a>')
    social = [(k, v) for k, v in site.get("social", {}).items() if v.strip()]
    if site.get("youtube_channel", "").strip():
        social.append(("YouTube", site["youtube_channel"]))
    social_html = "".join(f'<li><a href="{esc(v)}" rel="noopener">{esc(k)}</a></li>' for k, v in social)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{URL}/{path}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(NAME)}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{URL}/{path}">
<meta property="og:image" content="{URL}/img/group-og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="index.html"><img src="img/logo-cream.png" width="164" height="34" alt="{esc(NAME)} — home"></a>
<nav class="nav" aria-label="Main">{nav}</nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap">
<div>&copy; {YEAR} {esc(NAME)} &middot; Texas Hill Country &middot; {footer_contact}</div>
{('<ul>' + social_html + '</ul>') if social_html else ''}
</div></footer>
{extra}</body>
</html>
"""

def paras(items):
    return "\n".join(f"<p>{esc(p)}</p>" for p in items)

def video_block(v, heading=True):
    vid = esc(v["id"])
    h = f'<h3>{esc(v["title"])}</h3>' if heading else ""
    return f"""<div class="video-block">{h}
<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{esc(v['title'])}" loading="lazy"
 allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" referrerpolicy="origin" allowfullscreen></iframe></div>
<p><a href="https://www.youtube.com/watch?v={vid}" rel="noopener">Watch on YouTube</a></p></div>"""

pron = esc(site["pronunciation"]); meaning = esc(site["meaning"])
email = site.get("email", "").strip()
contact_line = (f'<a class="btn" href="mailto:{esc(email)}">Email {esc(email)}</a>' if email
                else '<p class="empty">Booking details are coming soon.</p>')
members = site["members"]
first_video = site["videos"][0]

# ---- Home
home = f"""<section class="hero" style="padding:0">
<img src="img/group-hero.jpg" width="2000" height="1125" alt="Madhu: Shoni Dawn, Mark MacDonald and Christopher Slone standing together among Hill Country trees">
<div class="overlay"><div class="wrap">
<h1><img src="img/logo-cream.png" width="520" height="108" alt="{esc(NAME)}"></h1>
<p class="pron">{esc(NAME)} (<strong>{pron}</strong>) means “{meaning}.”</p>
</div></div>
</section>
<div class="band"><div class="wrap"><p>{esc(site['tagline'])}</p></div></div>
<section><div class="wrap cols two">
<div><h2>The band</h2><p class="lead">{esc(site['short_bio'])}</p>
<div class="btn-row"><a class="btn" href="about.html">Meet the band</a><a class="btn ghost" href="epk.html">Press kit</a></div></div>
<div><h2>Watch</h2>{video_block(first_video, heading=False)}</div>
</div></section>
<section class="alt"><div class="wrap">
<h2>Upcoming shows</h2>
<div data-shows data-limit="3"><noscript><p>Please enable JavaScript to see upcoming shows, or <a href="contact.html">get in touch</a>.</p></noscript></div>
<div class="btn-row"><a class="btn ghost" href="shows.html">All shows</a></div>
</div></section>"""

# ---- About
mem_html = "".join(
    f'<article class="member{" full" if i == 0 else ""}"><h3>{esc(m["name"])}</h3><p class="role">{esc(m["role"])}</p>{paras(m["bio"])}</article>'
    for i, m in enumerate(members))
about = f"""<div class="page-title"><div class="wrap"><h1>About</h1></div></div>
<section><div class="wrap">
<p class="lead">{esc(site['bio'][0])}</p>
<p>Pronounced <strong>{pron}</strong>.</p>
</div></section>
<section class="alt"><div class="wrap"><h2>The players</h2>
<div class="cols two">{mem_html}</div></div></section>"""

# ---- Music
vids = "\n".join(video_block(v) for v in site["videos"])
music = f"""<div class="page-title"><div class="wrap"><h1>Music &amp; Video</h1></div></div>
<section><div class="wrap" style="max-width:860px">{vids}
<p>More recordings and videos are on the way.</p></div></section>"""

# ---- Shows
showspg = f"""<div class="page-title"><div class="wrap"><h1>Shows</h1></div></div>
<section><div class="wrap">
<div data-shows><noscript><p>Please enable JavaScript to see upcoming shows, or <a href="contact.html">get in touch</a>.</p></noscript></div>
<p style="margin-top:2rem">Want {esc(NAME)} at your venue, festival or private event? <a href="contact.html">Get in touch</a>.</p>
</div></section>"""

# ---- EPK
roster = "; ".join(f'{m["name"]} ({m["role"].lower()})' for m in members)
epk = f"""<div class="page-title"><div class="wrap"><h1>Press kit</h1></div></div>
<section><div class="wrap cols two">
<div><h2>At a glance</h2>
<dl class="facts">
<dt>Band</dt><dd>{esc(NAME)} ({pron}) — “{meaning}”</dd>
<dt>Based in</dt><dd>Texas Hill Country, near Austin</dd>
<dt>Sound</dt><dd>Country blues and Americana with an Eastern influence</dd>
<dt>Lineup</dt><dd>{esc(roster)}</dd>
<dt>Repertoire</dt><dd>Original material plus classic covers</dd>
</dl></div>
<div><h2>Short bio</h2><blockquote class="copy">{esc(site['short_bio'])}</blockquote>
<p><a href="about.html">Full bios</a></p></div>
</div></section>
<section class="alt"><div class="wrap"><h2>Photos &amp; logos</h2>
<div class="downloads">
<div class="dl"><img src="img/group-hero.jpg" width="500" height="281" alt="Group photo, wide crop" loading="lazy"><a href="img/group-hero.jpg" download>Group photo, wide (2000 px)</a><small>Web and print layouts</small></div>
<div class="dl"><img src="img/group-full.jpg" width="500" height="333" alt="Group photo, full frame" loading="lazy"><a href="img/group-full.jpg" download>Group photo, full frame</a><small>Largest available size</small></div>
<div class="dl"><div class="logo-tile"><img src="img/logo-dark.png" width="400" height="83" alt="{esc(NAME)} logo, dark"></div><a href="img/logo-dark.png" download>Logo, dark (transparent PNG)</a><small>For light backgrounds</small></div>
<div class="dl"><div class="logo-tile dark"><img src="img/logo-cream.png" width="400" height="83" alt="{esc(NAME)} logo, light"></div><a href="img/logo-cream.png" download>Logo, light (transparent PNG)</a><small>For dark backgrounds</small></div>
</div></div></section>
<section><div class="wrap" style="max-width:860px"><h2>Video</h2>{video_block(first_video)}</div></section>
<section class="dark"><div class="wrap"><h2 style="color:var(--cream)">Booking &amp; press</h2>
<div class="btn-row" style="margin-top:0">{contact_line}</div></div></section>"""

# ---- Contact
contact = f"""<div class="page-title"><div class="wrap"><h1>Contact</h1></div></div>
<section><div class="wrap" style="max-width:760px">
<p class="lead">Booking, press and general inquiries for {esc(NAME)}.</p>
{contact_line}
<p style="margin-top:2rem">Based in the Texas Hill Country near Austin.</p>
</div></section>"""

pages = [
    ("index.html", "Home", site["short_bio"], home, True),
    ("about.html", "About", "Meet Madhu: Mark MacDonald, Christopher Slone and Shoni Dawn — country blues and Americana from the Texas Hill Country.", about, False),
    ("music.html", "Music & Video", "Watch and listen to Madhu, a Texas Hill Country band blending Eastern influence with country blues and Americana.", music, False),
    ("shows.html", "Shows", "Upcoming Madhu shows in Austin and the Texas Hill Country.", showspg, True),
    ("epk.html", "Press kit", "Madhu press kit: bio, photos, logos and booking information.", epk, False),
    ("contact.html", "Contact", "Contact Madhu for booking, press and general inquiries.", contact, False),
]
for fn, title, desc, body, scripts in pages:
    (ROOT / fn).write_text(page(fn, title, desc, body, fn, scripts), encoding="utf-8")
    print("wrote", fn)

# 404 + sitemap
(ROOT / "404.html").write_text(page("404.html", "Page not found", "Page not found.",
    '<div class="page-title"><div class="wrap"><h1>Page not found</h1></div></div><section><div class="wrap"><p>That page is not here. <a href="index.html">Back to the home page</a>.</p></div></section>',
    ""), encoding="utf-8")
sm = "".join(f"<url><loc>{URL}/{'' if fn=='index.html' else fn}</loc></url>" for fn, *_ in pages)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>', encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {URL}/sitemap.xml\n", encoding="utf-8")
