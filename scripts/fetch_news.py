#!/usr/bin/env python3
"""Fetch English Bangladesh news RSS, translate NEW items to Bangla (cached by link), write news.json.
Runs in GitHub Actions (.github/workflows/news.yml). Stdlib only."""
import json, os, re, time, html, urllib.request, urllib.parse, email.utils, datetime, xml.etree.ElementTree as ET
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'news.json')
FEEDS = [  # edit this list to change sources
    ('The Business Standard', 'https://www.tbsnews.net/top-news/rss.xml'),
    ('Prothom Alo English', 'https://en.prothomalo.com/feed/'),
]
MAX_ITEMS, MAX_AGE_DAYS, MAX_NEW_TRANSLATIONS, DELAY = 60, 7, 80, 1.5
UA = {'User-Agent': 'Mozilla/5.0 (dFaster Tools news bot; +https://dfaster.com/tools/news/)'}

def get(url, timeout=25):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()

def clean(s, n=None):
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))
    s = re.sub(r'\s+', ' ', s).strip()
    if n and len(s) > n:
        s = s[:n].rsplit(' ', 1)[0] + '…'
    return s

def parse(name, data):
    root = ET.fromstring(data); out = []
    for it in root.iter('item'):
        g = lambda tag: (it.findtext(tag) or '')
        title, link = clean(g('title')), g('link').strip()
        if not title or not link: continue
        desc = g('description') or g('{http://purl.org/rss/1.0/modules/content/}encoded')
        try: dt = email.utils.parsedate_to_datetime(g('pubDate').strip())
        except Exception: dt = None
        if dt and dt.tzinfo is None: dt = dt.replace(tzinfo=datetime.timezone.utc)
        out.append(dict(title=title, snippet=clean(desc, 240), link=link, source=name,
                        published=dt.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') if dt else ''))
    return out

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
    items = []
    for name, url in FEEDS:
        try:
            got = parse(name, get(url)); print(name, len(got)); items += got
        except Exception as ex: print('feed fail', name, ex)
    if not items:
        print('no items fetched; keeping existing news.json'); return
    cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=MAX_AGE_DAYS)).strftime('%Y-%m-%dT%H:%M:%SZ')
    seen, fresh = set(), []
    for it in sorted(items, key=lambda x: x['published'], reverse=True):
        if it['link'] in seen or (it['published'] and it['published'] < cutoff): continue
        seen.add(it['link']); fresh.append(it)
    fresh = fresh[:MAX_ITEMS]
    reused, need = 0, []
    for it in fresh:
        o = old.get(it['link'])
        if o and o.get('title') == it['title'] and o.get('title_bn'):   # cache hit by link
            it['title_bn'], it['snippet_bn'] = o['title_bn'], o.get('snippet_bn', ''); reused += 1
        else:
            it['title_bn'], it['snippet_bn'] = '', ''; need.append(it)
    need = need[:MAX_NEW_TRANSLATIONS]
    done = 0
    if need:
        # snippets/titles never contain newlines (clean() collapses whitespace), so newline batching is safe
        tr = translate_many([x['title'] for x in need] + [x['snippet'] for x in need])
        for k, it in enumerate(need):
            tb, sb = tr[k], tr[len(need) + k]
            if tb:  # on failure title_bn stays '' -> page shows the original; retried next run
                it['title_bn'], it['snippet_bn'] = tb, (sb or ''); done += 1
    data = dict(updated=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                sources=[dict(name=n, url=u) for n, u in FEEDS], items=fresh)
    json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'items {len(fresh)}  translated-new {done}  cached {reused}  untranslated {sum(1 for i in fresh if not i["title_bn"])}')

if __name__ == '__main__':
    main()
