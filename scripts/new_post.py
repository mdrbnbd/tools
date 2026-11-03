#!/usr/bin/env python3
"""Add or update a post, then rebuild the site.

  python3 scripts/new_post.py POST.json            # validate, save to content/posts/<slug>.json, rebuild
  python3 scripts/new_post.py POST.json --publish  # same + git pull --rebase, commit, push (retries)
  python3 scripts/new_post.py --check POST.json    # validate only
  cat POST.json | python3 scripts/new_post.py -    # read from stdin

Exit codes: 0 ok, 2 invalid JSON/schema, 3 slug exists (use --force to overwrite), 4 git error.
Schema: README.md -> "Posts".
"""
import sys, os, json, subprocess, datetime, argparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import posts as P
from tools_def import TOOLS

def git(*a, check=True):
    r = subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True)
    if check and r.returncode: print('git', ' '.join(a), 'failed:\n', r.stdout, r.stderr, file=sys.stderr); sys.exit(4)
    return r

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('file'); ap.add_argument('--publish', action='store_true'); ap.add_argument('--force', action='store_true')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    try:
        raw = sys.stdin.read() if a.file == '-' else open(a.file, encoding='utf-8').read()
        p = json.loads(raw)
    except Exception as ex:
        print('invalid JSON:', ex, file=sys.stderr); sys.exit(2)
    p.setdefault('author', 'Robin'); p.setdefault('lang', 'bn'); p.setdefault('tags', [])
    err = P.validate(p, {t['slug'] for t in TOOLS})
    if err:
        print('schema errors:\n - ' + '\n - '.join(err), file=sys.stderr); sys.exit(2)
    if a.check: print('ok:', p['slug']); return
    if a.publish: git('pull', '--rebase', '-q', 'origin', 'main')
    os.makedirs(P.POSTS_DIR, exist_ok=True)
    dest = os.path.join(P.POSTS_DIR, p['slug'] + '.json')
    existed = os.path.exists(dest)
    if existed and not a.force:
        print(f'slug "{p["slug"]}" already exists ({dest}); use --force to overwrite', file=sys.stderr); sys.exit(3)
    if existed and not p.get('updated'): p['updated'] = datetime.date.today().isoformat()
    json.dump(p, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'src', 'build.py')], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode: print(r.stderr, file=sys.stderr); sys.exit(r.returncode)
    url = f'https://dfaster.com/tools/posts/{p["slug"]}/'
    if a.publish:
        git('add', '-A')
        if git('diff', '--cached', '--quiet', check=False).returncode == 0: print('nothing to commit'); print(url); return
        git('commit', '-q', '-m', f'post: {p["slug"]}')
        for i in range(3):
            if git('push', '-q', 'origin', 'HEAD:main', check=False).returncode == 0: break
            git('pull', '--rebase', '-X', 'theirs', '-q', 'origin', 'main', check=False)   # news bot may have pushed meanwhile
        else:
            print('push failed after 3 tries', file=sys.stderr); sys.exit(4)
        print('pushed', git('rev-parse', '--short', 'HEAD').stdout.strip())
    print(url)

if __name__ == '__main__':
    main()
