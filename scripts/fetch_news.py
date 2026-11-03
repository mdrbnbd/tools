#!/usr/bin/env python3
"""Fetch TECH news RSS (English + Bangla), keep the last 24 h, translate only NEW English items to Bangla
(cached by link, capped per run), write news.json. Runs in GitHub Actions every 20 min (.github/workflows/news.yml).
Stdlib only."""
import json, os, re, time, html, urllib.request, urllib.parse, email.utils, datetime, xml.etree.ElementTree as ET
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'news.json')
GN = 'https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?'
# name, url, lang, max items per run, optional link filter (regex) — edit this list to change sources
FEEDS = [
    dict(name='The Verge', url='https://www.theverge.com/rss/index.xml', lang='en', per=15),
    dict(name='TechCrunch', url='https://techcrunch.com/feed/', lang='en', per=20),
    dict(name='Ars Technica', url='https://feeds.arstechnica.com/arstechnica/index', lang='en', per=20),
    dict(name='Engadget', url='https://www.engadget.com/rss.xml', lang='en', per=20),
    dict(name='Wired', url='https://www.wired.com/feed/rss', lang='en', per=15),
    dict(name='Google News Technology (BD, English)', url=GN + 'hl=en-BD&gl=BD&ceid=BD:en', lang='en', per=30, gn=True),
    dict(name='The Business Standard Tech', url='https://www.tbsnews.net/tech/rss.xml', lang='en', per=15),
    dict(name='The Daily Star Tech & Startup', url='https://www.thedailystar.net/tech-startup/rss.xml', lang='en', per=10),
    dict(name='Google News প্রযুক্তি (বাংলা)', url=GN + 'hl=bn&gl=BD&ceid=BD:bn', lang='bn', per=30, gn=True),
    dict(name='টেকশহর', url='https://techshohor.com/feed/', lang='bn', per=15),
    dict(name='প্রথম আলো প্রযুক্তি', url='https://www.prothomalo.com/feed/', lang='bn', per=10, link_re=r'prothomalo\.com/technology/'),
]
# bdnews24 Bangla has no working RSS (returns HTML) — not included.
SKIP_TITLE = re.compile(r'promo code|coupon|discount code|best .* deals? (this|of the) week', re.I)
MAX_ITEMS, WINDOW_H, MIN_ITEMS, FALLBACK_H = 160, 24, 20, 72
MAX_NEW_TRANSLATIONS, DELAY = 50, 1.5   # per run; the rest stay English until the next run
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36 dFasterToolsNews/1.0'}
ATOM = '{http://www.w3.org/2005/Atom}'

def get(url, timeout=25):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()

def clean(s, n=None):
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))
    s = re.sub(r'\s+', ' ', s).strip()
    if n and len(s) > n:
        s = s[:n].rsplit(' ', 1)[0] + '…'
    return s

def iso(dt):
    return dt.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def pdate(s):
    s = (s or '').strip()
    if not s: return None
    try:
        dt = email.utils.parsedate_to_datetime(s)
    except Exception:
        try: dt = datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))
        except Exception: return None
    return dt if dt.tzinfo else dt.replace(tzinfo=datetime.timezone.utc)

def parse(f, data):
    root = ET.fromstring(data); out = []
    entries = list(root.iter('item')) or list(root.iter(ATOM + 'entry'))
    for it in entries:
        def g(*tags):
            for t in tags:
                el = it.find(t)
                if el is not None:
                    txt = ''.join(el.itertext()).strip()   # itertext: Daily Star nests <a> inside <title>
                    if txt: return txt
            return ''
        title = clean(g('title', ATOM + 'title'))
        link = g('link').strip()
        if not link:
            el = it.find(ATOM + 'link'); link = el.get('href', '') if el is not None else ''
        if not title or not link: continue
        if f.get('link_re') and not re.search(f['link_re'], link): continue
        if SKIP_TITLE.search(title): continue
        source = f['name']
        desc = g('description', ATOM + 'summary', '{http://purl.org/rss/1.0/modules/content/}encoded')
        if f.get('gn'):
            src = it.findtext('source') or ''
            if src and title.endswith(' - ' + src): title = title[: -len(src) - 3].strip()
            source = src or source
            desc = ''   # Google News description only repeats the headline
        dt = pdate(g('pubDate', ATOM + 'published', ATOM + 'updated'))
        snip = clean(desc, 240)
        if snip.lower().startswith(title.lower()[:40]): snip = ''
        out.append(dict(title=title, snippet=snip, link=link, source=source, feed=f['name'], lang=f['lang'],
                        published=iso(dt) if dt else ''))
        if len(out) >= f.get('per', 20): break
    return out

def tkey(t):
    return re.sub(r'[\W_]+', '', t.lower())[:70]

# ---------- translation (free, keyless; tried in order, batched to stay gentle) ----------
def _gtx(texts):
    """translate.googleapis.com gtx endpoint; texts joined by newlines in one POST."""
    body = urllib.parse.urlencode(dict(q='\n'.join(texts))).encode()
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=bn&dt=t'
    req = urllib.request.Request(url, data=body, headers=dict(UA, **{'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}))
    j = json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8'))
    out = ''.join(seg[0] for seg in j[0] if seg and seg[0]).split('\n')
    if len(out) != len(texts): raise ValueError('segment mismatch %d/%d' % (len(out), len(texts)))
    return [x.strip() for x in out]

def _dict_chrome(texts):
    """clients5.google.com dict-chrome-ex endpoint; accepts many q= params, returns a list."""
    url = 'https://clients5.google.com/translate_a/t?' + urllib.parse.urlencode([('client', 'dict-chrome-ex'), ('sl', 'en'), ('tl', 'bn')] + [('q', t) for t in texts])
    j = json.loads(get(url, 30).decode('utf-8'))
    out = [(x[0] if isinstance(x, list) else x) for x in j]
    if len(out) != len(texts): raise ValueError('count mismatch')
    return [str(x).strip() for x in out]

def _mymemory(texts):
    out = []
    for t in texts:
        j = json.loads(get('https://api.mymemory.translated.net/get?' + urllib.parse.urlencode({'q': t[:480], 'langpair': 'en|bn'}), 30).decode('utf-8'))
        r = (j.get('responseData') or {}).get('translatedText') or ''
        if j.get('responseStatus') not in (200, '200') or not r or 'MYMEMORY WARNING' in r: raise ValueError('mymemory: %s' % j.get('responseDetails'))
        out.append(html.unescape(r).strip()); time.sleep(DELAY)
    return out

PROVIDERS = [('gtx', _gtx, 25), ('dict-chrome-ex', _dict_chrome, 10), ('mymemory', _mymemory, 10)]
_dead = set()

def translate_many(texts):
    """Returns list (same length) of Bangla strings, or None entries where every provider failed."""
    res = [None] * len(texts)
    todo = [i for i, t in enumerate(texts) if t]
    for i, t in enumerate(texts):
        if not t: res[i] = ''
    if os.environ.get('NO_TRANSLATE'): return res
    for name, fn, batch in PROVIDERS:
        if not todo: break
        if name in _dead: continue
        fails = 0; left = []
        for k in range(0, len(todo), batch):
            chunk = todo[k:k + batch]
            if fails >= 2: left += chunk; continue
            try:
                out = fn([texts[i] for i in chunk])
                for i, o in zip(chunk, out): res[i] = o or None
                left += [i for i in chunk if not res[i]]
                print(f'  {name}: translated {len(chunk)}'); fails = 0
            except Exception as ex:
                fails += 1; left += chunk
                print(f'  {name} fail:', type(ex).__name__, str(ex)[:100])
            time.sleep(DELAY * (1 + 2 * fails))
        if fails >= 2: _dead.add(name)
        todo = left
    return res

def main():
    old = {}
    if os.path.exists(OUT):
        try:
            for it in json.load(open(OUT, encoding='utf-8')).get('items', []): old[it['link']] = it
        except Exception as ex: print('old news.json unreadable', ex)
    items, status = [], []
    for f in FEEDS:
        try:
            got = parse(f, get(f['url'])); items += got; status.append(dict(name=f['name'], url=f['url'], lang=f['lang'], ok=True, n=len(got)))
            print(f"{f['name']}: {len(got)}")
        except Exception as ex:
            status.append(dict(name=f['name'], url=f['url'], lang=f['lang'], ok=False, n=0)); print('feed fail', f['name'], type(ex).__name__, str(ex)[:80])
    if not items:
        print('no items fetched; keeping existing news.json'); return
    now = datetime.datetime.now(datetime.timezone.utc)
    cut, cut2 = iso(now - datetime.timedelta(hours=WINDOW_H)), iso(now - datetime.timedelta(hours=FALLBACK_H))
    future = iso(now + datetime.timedelta(hours=2))
    seen_l, seen_t, pool = set(), set(), []
    for it in sorted(items, key=lambda x: x['published'], reverse=True):
        k = tkey(it['title'])
        if not it['published'] or it['published'] > future: continue
        if it['link'] in seen_l or k in seen_t: continue
        seen_l.add(it['link']); seen_t.add(k); pool.append(it)
    fresh = [x for x in pool if x['published'] >= cut]
    if len(fresh) < MIN_ITEMS:   # quiet period: top up with the newest from the last 72 h
        fresh = [x for x in pool if x['published'] >= cut2][:MIN_ITEMS]
    fresh = fresh[:MAX_ITEMS]
    reused, need = 0, []
    for it in fresh:
        if it['lang'] == 'bn':
            it['title_bn'], it['snippet_bn'] = it['title'], it['snippet']; continue
        o = old.get(it['link'])
        if o and o.get('title') == it['title'] and o.get('title_bn'):   # cache hit by link
            it['title_bn'], it['snippet_bn'] = o['title_bn'], o.get('snippet_bn', ''); reused += 1
        else:
            it['title_bn'], it['snippet_bn'] = '', ''; need.append(it)
    later = max(0, len(need) - MAX_NEW_TRANSLATIONS)
    need = need[:MAX_NEW_TRANSLATIONS]   # newest first; the rest stay English until the next run
    done = 0
    if need:
        # titles/snippets never contain newlines (clean() collapses whitespace), so newline batching is safe
        texts = [x['title'] for x in need] + [x['snippet'] for x in need]
        tr = translate_many(texts)
        for k, it in enumerate(need):
            tb, sb = tr[k], tr[len(need) + k]
            if tb:  # on failure title_bn stays '' -> page shows the original; retried next run
                it['title_bn'], it['snippet_bn'] = tb, (sb or ''); done += 1
    data = dict(updated=iso(now), window_hours=WINDOW_H, sources=status, items=fresh)
    json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'items {len(fresh)}  bn-native {sum(1 for i in fresh if i["lang"]=="bn")}  translated-new {done}  cached {reused}  '
          f'deferred {later}  untranslated {sum(1 for i in fresh if not i["title_bn"])}  newest {fresh[0]["published"] if fresh else "-"}')

if __name__ == '__main__':
    main()
