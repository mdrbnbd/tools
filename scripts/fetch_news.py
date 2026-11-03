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

def translate(text):
    """Free keyless Google endpoint. Returns None on failure (caller falls back to the original)."""
    if not text: return ''
    if os.environ.get('NO_TRANSLATE'): return None
    url = 'https://translate.googleapis.com/translate_a/single?' + urllib.parse.urlencode(dict(client='gtx', sl='en', tl='bn', dt='t', q=text))
    for attempt in range(3):
        try:
            j = json.loads(get(url, 20).decode('utf-8'))
            res = ''.join(seg[0] for seg in j[0] if seg and seg[0])
            return res.strip() or None
        except Exception as ex:
            print('  translate fail', attempt + 1, type(ex).__name__, str(ex)[:80])
            time.sleep(DELAY * (attempt + 2) * 2)
    return None

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
    budget, done, reused = MAX_NEW_TRANSLATIONS, 0, 0
    for it in fresh:
        o = old.get(it['link'])
        if o and o.get('title') == it['title'] and o.get('title_bn'):   # cache hit by link
            it['title_bn'], it['snippet_bn'] = o['title_bn'], o.get('snippet_bn', ''); reused += 1; continue
        it['title_bn'], it['snippet_bn'] = '', ''
        if budget <= 0: continue
        tb = translate(it['title']); time.sleep(DELAY); budget -= 1
        sb = translate(it['snippet']) if (tb and it['snippet']) else ''
        if it['snippet']: time.sleep(DELAY); budget -= 1
        if tb:
            it['title_bn'], it['snippet_bn'] = tb, (sb or ''); done += 1
        # on failure title_bn stays '' → page shows the original; retried next run
    data = dict(updated=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                sources=[dict(name=n, url=u) for n, u in FEEDS], items=fresh)
    json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'items {len(fresh)}  translated-new {done}  cached {reused}  untranslated {sum(1 for i in fresh if not i["title_bn"])}')

if __name__ == '__main__':
    main()
