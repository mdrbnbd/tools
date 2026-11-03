# -*- coding: utf-8 -*-
"""dFaster Tools static site generator. Run: python3 src/build.py  (from repo root)"""
import os, html, json, datetime, re
from tools_def import CATS, TOOLS, SITES
from tutorials_def import GUIDES, ARTICLES
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://dfaster.com/tools/'
ADS = 'ca-pub-6277863204170835'
VERSION = 'v1-' + datetime.date.today().isoformat()
PAGES = []
LOGO = '<svg viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c5cff"/><stop offset="1" stop-color="#00c2a6"/></linearGradient></defs><rect width="64" height="64" rx="16" fill="url(#lg)"/><path d="M18 18h12a14 14 0 0 1 0 28H18z" fill="none" stroke="#fff" stroke-width="6"/><path d="M38 26h10M38 34h8" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>'
CATMAP = {c[0]: c for c in CATS}
TOOLMAP = {t['slug']: t for t in TOOLS}
e = html.escape

def page(path, title, desc, body, crumbs=None, scripts=(), og_type='website', extra_head=''):
    depth = path.count('/')
    pre = '../' * depth
    url = BASE + path
    t_full = title if 'dFaster Tools' in title else f'{title} | dFaster Tools'
    cr = ''
    if crumbs:
        cr = '<nav class="crumbs" aria-label="breadcrumb">' + ' › '.join(f'<a href="{pre}{h}">{e(n)}</a>' if h is not None else e(n) for n, h in crumbs) + '</nav>'
    sc = ''.join(f'<script src="{pre}{s}"></script>' for s in scripts)
    out = f'''<!doctype html>
<html lang="bn"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(t_full)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="dFaster Tools"><meta property="og:locale" content="bn_BD">
<meta property="og:title" content="{e(t_full)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}icons/og.png">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(t_full)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}icons/og.png">
<meta name="theme-color" content="#7c5cff"><meta name="dft-root" content="{pre}">
<link rel="manifest" href="{pre}manifest.json"><link rel="icon" href="{pre}icons/icon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{pre}icons/icon-192.png">
<link rel="preload" href="{pre}assets/fonts/hind-bengali-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/fonts/fonts.css"><link rel="stylesheet" href="{pre}css/style.css">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADS}" crossorigin="anonymous"></script>
{extra_head}</head><body>
<a class="skip" href="#main">মূল অংশে যান</a>
<header class="top"><div class="wrap"><a class="brand" href="{pre}" aria-label="dFaster Tools হোম">{LOGO}<span>dFaster <b>Tools</b></span></a>
<a class="hdr-link" href="{pre}#all" data-en="Tools">টুলস</a><a class="hdr-link" href="{pre}news/" data-en="News">খবর</a><a class="hdr-link" href="{pre}tutorials/" data-en="Tutorials">টিউটোরিয়াল</a><button class="lang-btn" id="langBtn" type="button" aria-label="Language">EN</button></div></header>
<div class="wrap"><div class="ad-slot" data-slot="top"></div></div>
<main id="main" class="wrap">{cr}{body}</main>
<div class="wrap"><div class="ad-slot" data-slot="bottom"></div></div>
<footer class="foot"><div class="wrap"><nav><a href="{pre}" data-en="Home">হোম</a><a href="{pre}tutorials/" data-en="Tutorials">টিউটোরিয়াল</a><a href="{pre}news/" data-en="News">খবর</a><a href="{pre}about/" data-en="About">আমাদের সম্পর্কে</a><a href="{pre}privacy/" data-en="Privacy Policy">গোপনীয়তা নীতি</a><a href="{pre}contact/" data-en="Contact">যোগাযোগ</a><a href="https://dfaster.com/">dfaster.com</a></nav>
<div>© <span data-year></span> dFaster Tools · <span class="made"><a href="https://wa.me/8801766119905" target="_blank" rel="noopener">Made by Robin</a></span></div></div></footer>
<script src="{pre}js/ads-config.js"></script><script src="{pre}js/common.js"></script>{sc}
</body></html>
'''
    fp = os.path.join(ROOT, path, 'index.html') if (path == '' or path.endswith('/')) else os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(out)
    if not path.endswith('.html') or path == '404.html':
        if path != '404.html': PAGES.append(path)

def card(href, icon, title, desc, en=None, den=None, extra='', cls='card'):
    a = f' data-en="{e(en)}"' if en else ''
    b = f' data-en="{e(den)}"' if den else ''
    return f'<a class="{cls}" href="{href}"{extra}><div class="ic">{icon}</div><h3{a}>{e(title)}</h3><p{b}>{e(desc)}</p></a>'

# ---------- home ----------
def home():
    chips = '<button class="chip on" data-cat="all" data-en="All">সব</button>' + ''.join(f'<button class="chip" data-cat="{c[0]}" data-en="{e(c[2])}">{c[3]} {e(c[1])}</button>' for c in CATS)
    secs = ''
    for c in CATS:
        if c[0] == 'tutorial':
            items = [card(f'tutorials/{a["slug"]}/', a['icon'], a['title'], a['desc'], extra=f' data-k="{e(a["title"]+" "+a["desc"])}"', cls='card tut') for a in ARTICLES]
            items += [card(f'tutorials/{t["slug"]}/', '📘', t['bn'] + ' — ব্যবহারের নিয়ম', 'ধাপে ধাপে গাইড ও টিপস', en=t['en'] + ' — How to use', den='Step-by-step guide', extra=f' data-k="{e(t["bn"]+" "+t["en"]+" টিউটোরিয়াল গাইড")}"', cls='card tut') for t in TOOLS]
        else:
            items = [card(f'{t["slug"]}/', t['icon'], t['bn'], t['desc'], t['en'], t['den'], extra=f' data-k="{e(t["bn"]+" "+t["en"]+" "+t["desc"]+" "+t["kw"])}"') for t in TOOLS if t['cat'] == c[0]]
        secs += f'<section class="cat" data-cat="{c[0]}" id="cat-{c[0]}"><h2 class="cat-title">{c[3]} <span data-en="{e(c[2])}">{e(c[1])}</span></h2><div class="grid">{"".join(items)}</div></section>'
        if c[0] == 'text':
            secs += '<div class="ad-slot" data-slot="middle"></div>'
    sites = ''.join(card(u, i, n, d, extra=' target="_blank" rel="noopener"') for i, n, d, u in SITES)
    body = f'''<section class="hero"><h1 data-en="Free Bangla tools for everyday life">প্রতিদিনের কাজের ফ্রি বাংলা টুলস</h1>
<p data-en="Electricity bill, tax, zakat, photo resize, Bijoy-Unicode, prayer times and more — fast, free and works offline.">বিদ্যুৎ বিল, আয়কর, জাকাত, ছবি রিসাইজ, বিজয়-ইউনিকোড, নামাজের সময়সহ {str(len(TOOLS)).translate(str.maketrans('0123456789','০১২৩৪৫৬৭৮৯'))}টি টুল — দ্রুত, ফ্রি, অফলাইনেও চলে।</p>
<div class="search"><input id="q" type="search" placeholder="টুল খুঁজুন… যেমন বিল, জমি, ছবি" data-en-ph="Search tools… e.g. bill, land, photo" aria-label="টুল খুঁজুন"></div></section>
<a class="news-promo" href="news/">📰 <span data-en="Latest news (English sources, shown in Bangla)">আজকের খবর — বাংলায় পড়ুন</span> →</a>
<div class="chips" id="chips" role="tablist">{chips}</div><div id="all">{secs}</div><p class="empty" id="empty" data-en="No tool found.">কোনো টুল পাওয়া যায়নি।</p>
<section class="sites" style="margin-top:1.6rem"><h2 class="cat-title">🌐 <span data-en="Our other sites">আমাদের অন্যান্য সাইট</span></h2><div class="grid">{sites}</div></section>
<script>document.addEventListener('DOMContentLoaded',function(){{var D=DFT,cat='all';function f(){{var q=D.toEn(D.$('#q').value.trim().toLowerCase()),n=0;D.$$('.cat').forEach(function(s){{var vis=0;D.$$('.card',s).forEach(function(c){{var ok=(!q||D.toEn((c.dataset.k||c.textContent).toLowerCase()).indexOf(q)>=0);c.hidden=!ok;if(ok)vis++}});s.hidden=!(vis&&(cat==='all'||s.dataset.cat===cat));if(!s.hidden)n+=vis}});D.$('#empty').style.display=n?'none':'block'}}
D.$$('#chips .chip').forEach(function(b){{b.addEventListener('click',function(){{cat=b.dataset.cat;D.$$('#chips .chip').forEach(function(x){{x.classList.toggle('on',x===b)}});f()}})}});D.$('#q').addEventListener('input',f);var h=location.hash.match(/^#cat-(\\w+)/);if(h){{var b=D.$('#chips [data-cat="'+h[1]+'"]');if(b)b.click()}}}});</script>'''
    page('', 'dFaster Tools — প্রতিদিনের কাজের ফ্রি বাংলা অনলাইন টুলস', 'বিদ্যুৎ বিল, আয়কর, জাকাত, বয়স, বিকাশ চার্জ, জমির মাপ, ছবি রিসাইজ, বিজয়-ইউনিকোড, টাইপিং টেস্ট, মোবাইল প্যাকেজ, GPA ও নামাজের সময় — সব ফ্রি বাংলা টুল এক জায়গায়।', body)

def tool_pages():
    for t in TOOLS:
        c = CATMAP[t['cat']]
        others = [x for x in TOOLS if x['slug'] != t['slug'] and x['cat'] == t['cat']][:3] or [x for x in TOOLS if x['slug'] != t['slug']][:3]
        rel = ''.join(card(f'../{x["slug"]}/', x['icon'], x['bn'], x['desc'], x['en'], x['den']) for x in others)
        body = f'''<h1>{t["icon"]} <span data-en="{e(t["en"])}">{e(t["bn"])}</span></h1><p class="muted" data-en="{e(t["den"])}">{e(t["desc"])}</p>
{t["body"]}
<a class="tut-link" href="../tutorials/{t["slug"]}/">📘 <span data-en="How to use this tool (tutorial)">কীভাবে ব্যবহার করবেন — ধাপে ধাপে টিউটোরিয়াল</span> →</a>
<div class="ad-slot" data-slot="middle"></div>
<h2 data-en="Related tools">আরও টুল</h2><div class="grid">{rel}</div>'''
        page(f'{t["slug"]}/', f'{t["bn"]} — {t["en"]}', t['desc'], body, crumbs=[('হোম', ''), (c[1], f'#cat-{c[0]}'), (t['bn'], None)], scripts=t['js'])

def tutorials():
    cards = ''.join(card(f'{a["slug"]}/', a['icon'], a['title'], a['desc'], cls='card tut') for a in ARTICLES)
    tcards = ''.join(card(f'{t["slug"]}/', t['icon'], t['bn'] + ' — ব্যবহারের নিয়ম', t['desc'], cls='card tut') for t in TOOLS)
    page('tutorials/', 'টিউটোরিয়াল — বাংলায় ধাপে ধাপে গাইড', 'ছবি রিসাইজ, বিজয় থেকে ইউনিকোড, বিদ্যুৎ বিল কমানো, আয়কর হিসাবসহ প্রতিটি টুলের বাংলা গাইড।',
         f'<h1>📘 <span data-en="Tutorials">টিউটোরিয়াল</span></h1><p class="muted">প্রতিটি টুল কীভাবে ব্যবহার করবেন, সাথে কাজের টিপস — সহজ বাংলায়।</p><h2>গুরুত্বপূর্ণ গাইড</h2><div class="grid">{cards}</div><h2 style="margin-top:1.2rem">টুল ব্যবহারের নিয়ম</h2><div class="grid">{tcards}</div>',
         crumbs=[('হোম', ''), ('টিউটোরিয়াল', None)])
    for t in TOOLS:
        g = GUIDES[t['slug']]
        steps = ''.join(f'<li>{s}</li>' for s in g['steps']); tips = ''.join(f'<li>{s}</li>' for s in g['tips'])
        body = f'''<article class="prose"><h1>{t["icon"]} {e(t["bn"])} — কীভাবে ব্যবহার করবেন</h1><p>{g["intro"]}</p>
<p><a class="btn" href="../../{t["slug"]}/">টুলটি খুলুন →</a></p><h2>ধাপে ধাপে</h2><ol>{steps}</ol><div class="ad-slot" data-slot="middle"></div><h2>দরকারি টিপস</h2><ul>{tips}</ul>
<h2>প্রায়ই জিজ্ঞাসিত প্রশ্ন</h2><p><b>টুলটি কি ফ্রি?</b> হ্যাঁ, সম্পূর্ণ ফ্রি, কোনো রেজিস্ট্রেশন লাগে না।</p><p><b>আমার তথ্য কি কোথাও যায়?</b> না, সব হিসাব আপনার ব্রাউজারেই হয়। বিস্তারিত <a href="../../privacy/">গোপনীয়তা নীতিতে</a>।</p></article>'''
        page(f'tutorials/{t["slug"]}/', f'{t["bn"]} ব্যবহারের নিয়ম — বাংলা টিউটোরিয়াল', f'{t["bn"]} কীভাবে ব্যবহার করবেন: ধাপে ধাপে বাংলা গাইড ও টিপস।', body,
             crumbs=[('হোম', ''), ('টিউটোরিয়াল', 'tutorials/'), (t['bn'], None)], og_type='article')
    for a in ARTICLES:
        t = TOOLMAP[a['tool']]
        body = f'<article class="prose"><h1>{a["icon"]} {e(a["title"])}</h1>{a["html"]}<p style="margin-top:1rem"><a class="btn" href="../../{t["slug"]}/">{t["icon"]} {e(t["bn"])} খুলুন →</a></p></article>'
        page(f'tutorials/{a["slug"]}/', a['title'], a['desc'], body, crumbs=[('হোম', ''), ('টিউটোরিয়াল', 'tutorials/'), (a['title'][:40] + '…', None)], og_type='article')

def static_pages():
    page('about/', 'আমাদের সম্পর্কে', 'dFaster Tools কী, কারা বানিয়েছে এবং কেন।', '''<article class="prose"><h1>আমাদের সম্পর্কে</h1>
<p><b>dFaster Tools</b> বাংলাদেশের মানুষের প্রতিদিনের ছোট ছোট হিসাব আর কাজ সহজ করার জন্য বানানো ফ্রি অনলাইন টুলের সংগ্রহ। বিদ্যুৎ বিল, আয়কর, জাকাত, জমির মাপ, চাকরির আবেদনের ছবি, বিজয়-ইউনিকোড, নামাজের সময় — সবকিছু এক জায়গায়, সহজ বাংলায়।</p>
<h2>আমাদের নীতি</h2><ul><li><b>ফ্রি ও রেজিস্ট্রেশন ছাড়া:</b> কোনো একাউন্ট লাগে না।</li><li><b>গোপনীয়তা:</b> সব হিসাব আপনার ব্রাউজারেই হয়; ছবি বা তথ্য আমাদের কাছে আসে না।</li><li><b>স্বচ্ছ উৎস:</b> রেট বা হার যেখানে আছে, সেখানে উৎস ও তারিখ লেখা থাকে।</li><li><b>দ্রুত ও অফলাইন:</b> একবার খুললে ইন্টারনেট ছাড়াও বেশিরভাগ টুল চলে।</li></ul>
<h2>কে বানিয়েছে</h2><p>সাইটটি তৈরি ও পরিচালনা করেন ওয়েব ডেভেলপার <a href="https://dfaster.com/">Robin (dfaster.com)</a>। কোনো ভুল চোখে পড়লে বা নতুন টুলের আইডিয়া থাকলে <a href="../contact/">যোগাযোগ করুন</a>।</p>
<div class="note">এখানকার হিসাব সাধারণ ধারণার জন্য। আইনি, কর বা ধর্মীয় বিষয়ে চূড়ান্ত সিদ্ধান্তের আগে সংশ্লিষ্ট বিশেষজ্ঞের পরামর্শ নিন।</div></article>''', crumbs=[('হোম', ''), ('আমাদের সম্পর্কে', None)])
    page('privacy/', 'গোপনীয়তা নীতি (Privacy Policy)', 'dFaster Tools কী তথ্য সংগ্রহ করে, কুকি ও Google AdSense বিজ্ঞাপন সম্পর্কে তথ্য।', f'''<article class="prose"><h1>গোপনীয়তা নীতি</h1><p class="muted">সর্বশেষ হালনাগাদ: {datetime.date.today().strftime('%d-%m-%Y')}</p>
<p>dFaster Tools (dfaster.com/tools) আপনার গোপনীয়তাকে গুরুত্ব দেয়। এই নীতিতে বলা আছে সাইট ব্যবহারের সময় কী তথ্য কোথায় যায়।</p>
<h2>আপনার দেওয়া তথ্য</h2><p>ক্যালকুলেটরে দেওয়া সংখ্যা, টেক্সট বা ছবি আপনার ডিভাইসের ব্রাউজারেই প্রক্রিয়া হয়। এগুলো আমাদের কোনো সার্ভারে পাঠানো বা সংরক্ষণ করা হয় না। কিছু পছন্দ (যেমন ভাষা বা জেলা) আপনার ব্রাউজারের localStorage-এ রাখা হয়, যা আপনি ব্রাউজারের সেটিংস থেকে মুছতে পারেন।</p>
<h2>হোস্টিং</h2><p>সাইটটি GitHub Pages-এ হোস্ট করা। নিরাপত্তা ও পরিচালনার জন্য GitHub সার্ভার লগে IP ঠিকানার মতো প্রযুক্তিগত তথ্য রাখতে পারে (<a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub Privacy Statement</a>)।</p>
<h2>কুকি ও বিজ্ঞাপন (Google AdSense)</h2><ul><li>এই সাইটে Google AdSense-এর মাধ্যমে বিজ্ঞাপন দেখানো হয়।</li><li>Google সহ তৃতীয় পক্ষের বিক্রেতারা কুকি ব্যবহার করে আপনার এই সাইট ও অন্যান্য সাইটে আগের ভিজিটের ভিত্তিতে বিজ্ঞাপন দেখায়।</li><li>Google-এর বিজ্ঞাপন কুকি ব্যবহারের ফলে Google ও তার অংশীদাররা আপনার এই সাইট এবং/অথবা ইন্টারনেটের অন্যান্য সাইটের ভিজিটের ভিত্তিতে বিজ্ঞাপন দেখাতে পারে।</li><li>আপনি <a href="https://www.google.com/settings/ads" rel="noopener">Google Ads Settings</a> থেকে ব্যক্তিগতকৃত বিজ্ঞাপন বন্ধ করতে পারেন, অথবা <a href="https://www.aboutads.info/choices/" rel="noopener">www.aboutads.info</a> থেকে তৃতীয় পক্ষের কুকি বন্ধ করতে পারেন।</li><li>বিস্তারিত: <a href="https://policies.google.com/technologies/ads" rel="noopener">Google কীভাবে বিজ্ঞাপনে কুকি ব্যবহার করে</a>।</li></ul>
<h2>শিশুদের গোপনীয়তা</h2><p>আমরা জেনেশুনে ১৩ বছরের কম বয়সী কারও ব্যক্তিগত তথ্য সংগ্রহ করি না।</p>
<h2>বাইরের লিংক</h2><p>সাইটে অন্য ওয়েবসাইটের লিংক থাকতে পারে; সেসব সাইটের গোপনীয়তা নীতির জন্য আমরা দায়ী নই।</p>
<h2>যোগাযোগ</h2><p>এই নীতি নিয়ে প্রশ্ন থাকলে <a href="../contact/">যোগাযোগ পাতায়</a> জানান।</p>
<h2 lang="en">English summary</h2><p lang="en">We do not collect personal data; all calculations run in your browser. We use Google AdSense, which uses cookies to serve ads based on your prior visits to this and other websites. You can opt out of personalised advertising at Google Ads Settings.</p></article>''', crumbs=[('হোম', ''), ('গোপনীয়তা নীতি', None)])
    page('contact/', 'যোগাযোগ', 'dFaster Tools-এর সাথে যোগাযোগ — WhatsApp।', '''<article class="prose"><h1>যোগাযোগ</h1>
<p>ভুল রিপোর্ট, নতুন টুলের অনুরোধ, রেট হালনাগাদ বা ব্যবসায়িক প্রস্তাব — যেকোনো বিষয়ে লিখুন।</p>
<p><a class="btn" href="https://wa.me/8801766119905" target="_blank" rel="noopener">💬 WhatsApp-এ মেসেজ দিন</a></p>
<p>ওয়েবসাইট: <a href="https://dfaster.com/">dfaster.com</a></p>
<div class="note">কোনো রেট বা হার পুরোনো মনে হলে উৎসের লিংকসহ জানালে দ্রুত ঠিক করে দেওয়া হবে।</div></article>''', crumbs=[('হোম', ''), ('যোগাযোগ', None)])

def news():
    body = """<h1>📰 <span data-en="Latest news">আজকের খবর</span></h1>
<p class="muted" data-en="Headlines from English-language Bangladeshi news sites, updated every 2 hours. In Bangla mode they are shown machine-translated.">ইংরেজি ভাষার বাংলাদেশি সংবাদমাধ্যমের শিরোনাম, প্রতি ২ ঘণ্টায় হালনাগাদ। বাংলা মোডে স্বয়ংক্রিয় অনুবাদে দেখানো হয় — পুরো খবর পড়তে শিরোনামে চাপুন।</p>
<div class="news-ctl" id="newsCtl"><span class="small muted">অনুবাদে ভুল থাকতে পারে।</span><button type="button" class="btn sm ghost" id="origAll" aria-pressed="false">মূল ইংরেজি দেখুন</button></div>
<div id="newsList"><p class="muted">লোড হচ্ছে…</p></div><p class="small muted" id="newsSrc"></p>"""
    page('news/', 'আজকের খবর — বাংলায়', 'বাংলাদেশের ইংরেজি সংবাদমাধ্যমের সর্বশেষ শিরোনাম বাংলায় পড়ুন, মূল ইংরেজিও দেখা যায়। প্রতি ২ ঘণ্টায় হালনাগাদ।', body,
         crumbs=[('হোম', ''), ('খবর', None)], scripts=['js/tools/news.js'])

def extras():
    # 404 (GitHub Pages uses repo-level 404 only for the user site; keep for local + /tools/ deep links)
    page('404.html', 'পাতা পাওয়া যায়নি', 'পাতা পাওয়া যায়নি।', '<h1>পাতা পাওয়া যায়নি</h1><p><a href="https://dfaster.com/tools/">সব টুল দেখুন →</a></p>')
    today = datetime.date.today().isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{p}</loc><lastmod>{today}</lastmod></url>\n' for p in PAGES) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(sm)
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
    man = dict(name='dFaster Tools — বাংলা টুলস', short_name='dFaster Tools', description='প্রতিদিনের কাজের ফ্রি বাংলা টুলস', lang='bn', start_url='./', scope='./', display='standalone',
               background_color='#f6f7fb', theme_color='#7c5cff', icons=[dict(src='icons/icon-192.png', sizes='192x192', type='image/png'), dict(src='icons/icon-512.png', sizes='512x512', type='image/png'), dict(src='icons/icon-maskable-512.png', sizes='512x512', type='image/png', purpose='maskable')])
    json.dump(man, open(os.path.join(ROOT, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
    assets = set()
    for dp, dn, fn in os.walk(ROOT):
        if any(x in dp for x in ('/.git', '/src', '/scripts')): continue
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), ROOT)
            if rel.endswith(('.html', '.js', '.css', '.woff2', '.png', '.svg', '.json')) and rel not in ('sw.js',) and 'LICENSE' not in rel and rel != 'icons/og.png':
                assets.add(rel.replace('index.html', '') if rel.endswith('index.html') else rel)
    pre = sorted(assets)
    sw = f'''/* dFaster Tools service worker — auto-generated by src/build.py */
const VERSION='{VERSION}';const CACHE='dft-'+VERSION;
const PRECACHE={json.dumps(['./' if p == '' else p for p in pre], ensure_ascii=False)};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(PRECACHE)).then(()=>self.skipWaiting()))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith('dft-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener('fetch',e=>{{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==location.origin)return;
 if(e.request.mode==='navigate'){{e.respondWith(fetch(e.request).then(r=>{{const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));return r}}).catch(()=>caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||caches.match('./'))));return}}
 if(u.pathname.endsWith('/news.json')){{e.respondWith(fetch(e.request).then(r=>{{const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));return r}}).catch(()=>caches.match(e.request,{{ignoreSearch:true}})));return}}
 e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||fetch(e.request).then(n=>{{const c=n.clone();caches.open(CACHE).then(x=>x.put(e.request,c));return n}})))}});
'''
    open(os.path.join(ROOT, 'sw.js'), 'w').write(sw)
    print('pages', len(PAGES), 'precache', len(pre))

home(); news(); tool_pages(); tutorials(); static_pages(); extras()
