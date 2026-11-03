# -*- coding: utf-8 -*-
"""Posts: load content/posts/*.json, validate, tiny Markdown -> HTML."""
import os, re, json, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, 'content', 'posts')
SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
SCHEMA_HELP = 'see README.md "Posts" for the JSON schema'

def validate(p, tool_slugs=()):
    err = []
    for k in ('slug', 'title', 'description', 'date', 'sources'):
        if not p.get(k): err.append(f'missing "{k}"')
    if not (p.get('body_md') or p.get('body_html')): err.append('need "body_md" or "body_html"')
    if p.get('slug') and (not SLUG_RE.match(p['slug']) or len(p['slug']) > 80): err.append('slug must be lowercase a-z, 0-9 and hyphens (max 80)')
    if p.get('date'):
        try: datetime.datetime.fromisoformat(str(p['date']).replace('Z', '+00:00'))
        except Exception: err.append('date must be ISO, e.g. 2026-11-03 or 2026-11-03T09:00:00+06:00')
    if p.get('description') and len(p['description']) > 300: err.append('description max 300 chars')
    s = p.get('sources')
    if s is not None:
        if not isinstance(s, list) or not s: err.append('sources must be a non-empty list')
        else:
            for i, x in enumerate(s):
                if not isinstance(x, dict) or not x.get('title') or not re.match(r'^https?://', x.get('url', '')): err.append(f'sources[{i}] needs title and http(s) url')
    for t in p.get('related_tools', []) or []:
        if tool_slugs and t not in tool_slugs: err.append(f'related_tools: unknown tool "{t}"')
    if p.get('tags') is not None and not isinstance(p['tags'], list): err.append('tags must be a list')
    return err

def load_all(tool_slugs=()):
    out = []
    if not os.path.isdir(POSTS_DIR): return out
    for f in sorted(os.listdir(POSTS_DIR)):
        if not f.endswith('.json'): continue
        p = json.load(open(os.path.join(POSTS_DIR, f), encoding='utf-8'))
        e = validate(p, tool_slugs)
        if e: raise SystemExit(f'{f}: ' + '; '.join(e))
        if p.get('draft'): continue
        out.append(p)
    return sorted(out, key=lambda p: str(p['date']), reverse=True)

def _inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\*)', r'<i>\1</i>', s)
    def link(m):
        t, u = m.group(1), m.group(2).replace('"', '%22')
        ext = u.startswith('http') and 'dfaster.com' not in u
        return f'<a href="{u}"' + (' target="_blank" rel="noopener"' if ext else '') + f'>{t}</a>'
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, s)
    return s

def md(src):
    """Subset: #/##/### headings, paragraphs, - / * lists, 1. lists, > quote/note, ``` code, --- rule, | tables |, **b**, *i*, `code`, [t](url)."""
    lines = src.replace('\r', '').split('\n'); out = []; i = 0
    while i < len(lines):
        l = lines[i]
        if not l.strip(): i += 1; continue
        if l.startswith('```'):
            j = i + 1; buf = []
            while j < len(lines) and not lines[j].startswith('```'): buf.append(lines[j]); j += 1
            out.append('<pre><code>' + html.escape('\n'.join(buf)) + '</code></pre>'); i = j + 1; continue
        m = re.match(r'^(#{1,4})\s+(.*)', l)
        if m:
            lv = min(len(m.group(1)) + 1, 4); out.append(f'<h{lv}>{_inline(m.group(2))}</h{lv}>'); i += 1; continue
        if re.match(r'^-{3,}\s*$', l): out.append('<hr>'); i += 1; continue
        if l.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].startswith('>'): buf.append(lines[i][1:].strip()); i += 1
            out.append('<div class="note">' + _inline(' '.join(buf)) + '</div>'); continue
        if l.lstrip().startswith('|'):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                r = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.match(r'^:?-+:?$', c) for c in r): rows.append(r)
                i += 1
            h = '<div class="tbl"><table><thead><tr>' + ''.join(f'<th>{_inline(c)}</th>' for c in rows[0]) + '</tr></thead><tbody>'
            h += ''.join('<tr>' + ''.join(f'<td>{_inline(c)}</td>' for c in r) + '</tr>' for r in rows[1:]) + '</tbody></table></div>'
            out.append(h); continue
        if re.match(r'^\s*([-*]|\d+[.)])\s+', l):
            ordered = bool(re.match(r'^\s*\d+[.)]\s+', l)); tag = 'ol' if ordered else 'ul'; items = []
            while i < len(lines) and re.match(r'^\s*([-*]|\d+[.)])\s+', lines[i]):
                items.append(re.sub(r'^\s*([-*]|\d+[.)])\s+', '', lines[i])); i += 1
                while i < len(lines) and lines[i].startswith('   ') and lines[i].strip(): items[-1] += ' ' + lines[i].strip(); i += 1
            out.append(f'<{tag}>' + ''.join(f'<li>{_inline(x)}</li>' for x in items) + f'</{tag}>'); continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,4}\s|```|>|\s*([-*]|\d+[.)])\s+|\s*\|)', lines[i]):
            buf.append(lines[i].strip()); i += 1
        out.append('<p>' + _inline(' '.join(buf)) + '</p>')
    return '\n'.join(out)
