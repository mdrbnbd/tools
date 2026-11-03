# dFaster Tools — https://dfaster.com/tools/

Bangla-first, mobile-first static tool site (PWA, works offline). No backend. Served by GitHub Pages from this repo (`mdrbnbd/tools`) under the user site's custom domain `dfaster.com`. No CNAME file here.

## Build
Pages are generated: edit `src/tools_def.py` (tool pages), `src/tutorials_def.py` (guides/articles), then run

```
python3 src/build.py
```

It writes every `*/index.html`, `sitemap.xml`, `robots.txt`, `manifest.json` and `sw.js` (bump happens automatically by date).

## Editable data (check these regularly)
| File | What | Status |
|---|---|---|
| `data/rates.js` → `electricity` | BERC slab rates (June 2026 order), VAT, demand charge/kW, meter rent | slabs from news reports; **demand charge 42 Tk/kW & meter rent need verifying** with your utility |
| `data/rates.js` → `tax` | FY 2026-27 slabs, thresholds, rebate, minimum tax | from PwC / Daily Star; verify against NBR |
| `data/rates.js` → `zakat` | gold/silver price per vori (BAJUS) | **changes often — update the date & price** |
| `data/rates.js` → `mfs` | bKash / Nagad cash-out & send-money charges | bKash from bkash.com; **Nagad from third-party source** |
| `data/packages.js` | GP / Robi / Banglalink / Teletalk internet packs | GP & Teletalk from official sites; **Robi & BL unverified** — users are told to check the operator app |
| `data/districts.js` | 64 districts lat/lon for prayer times | nuhil/bangladesh-geocode |

## News page (`/news/`)
`.github/workflows/news.yml` runs `scripts/fetch_news.py` every 2 hours (and on manual dispatch). It fetches English RSS feeds (list `FEEDS` in the script — currently The Business Standard top news and Prothom Alo English), translates **only new items** to Bangla (cache by link) with free keyless endpoints tried in order: `translate.googleapis.com/translate_a/single?client=gtx` (batched POST), then `clients5.google.com` dict-chrome-ex, then MyMemory — batched, 1.5 s+ back-off, a provider is skipped after 2 failures, and commits `news.json` with `title_bn` / `snippet_bn` next to the originals. If translation fails the Bangla fields stay empty, the page shows the original, and the item is retried on the next run.

## AdSense
- Publisher `ca-pub-6277863204170835`; the `adsbygoogle.js` tag is in every page `<head>` (Auto ads).
- Manual units: put slot ids in `js/ads-config.js` → `SLOTS`. Empty = hidden.
- `ads.txt` lives at the root of `mdrbnbd/mdrbnbd.github.io` (served at https://dfaster.com/ads.txt).

## Credits
Prayer times: [adhan-js](https://github.com/batoulapps/adhan-js) (MIT). Bijoy converter: unicode2ascii (MIT). Font: Hind Siliguri (OFL).

Made by Robin — https://wa.me/8801766119905
