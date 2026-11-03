# Local review and hosting preparation — 3 November 2026

This is an unpublished implementation. Do not push a source branch onto an existing Pages deployment branch: the three older company repositories currently publish automatically. No production DNS, account, credential or hosting configuration was changed.

## Build and content editing

```sh
python3 scripts/build.py
python3 scripts/check.py
```

`dist` is always the local **noindex** review artifact. `SITE_MODE=production BUILD_DIR=dist-production` explicitly creates indexable production HTML and one canonical CNAME. A project-path preview uses `BASE_PATH=/review BUILD_DIR=dist-subpath`; it remains noindex. Source checkout files are not a deployment artifact. Publish only the reviewed build directory after approval. Plain text `/app-ads.txt` must remain at the domain root, even when a project-path preview is used. Crawler permissions remain wildcard Allow; no training-crawler decision or search-console submission was made.

Edit the generated static HTML for pages/guides, landing.css for styling, and site.config.json for explicit canonical routes. scripts/build.py is the dependency-free supported build; the old Gulp/npm theme toolchain is retired. The tooling one-time content importer is not the normal build. Legacy legal/campaign/game routes and Unity runtime files are retained.

## Host and routing

The matching company GitHub repository has Pages enabled and currently publishes from its existing branch. Preserve that hosting; do not migrate accounts. This isolated branch includes the pre-existing unpublished draft in a separate baseline commit. The remote production tip observed on 3 November is an ancestor of this draft (verified locally). Recheck the remote tip before any approved release; no remote branch was changed. CNAME now contains one canonical host rather than two.

The inactive workflow example builds and uploads a review artifact only; it cannot deploy. Do not activate it without choosing the repository and branch. GitHub Pages supports static files and directory redirects but cannot apply arbitrary HTTP headers or consume `.redirects.json` / Nginx rules. Static aliases are usable fallbacks, not HTTP301 promises. The optional Nginx example is a configuration reference for an existing approved server, not authorization to purchase or configure a server.

## Exact preservation and validation

evidence/preserved-files.json freezes legal/contact source and seller bytes plus legacy runtime builds. The original company seller list uses CRLF; preserve exact bytes rather than substituting another publisher list.

Validate root and project-path builds. Check store destinations, native crawlable content, one main H1, internal links and anchors, metadata/canonicals, sitemap, noindex on preview, seller hashes, protected source legal/runtime files, 320/390px and desktop rendering. A store link is an official destination, not a promise about every region/device, ad policy or platform feature. Upcoming Minesweeper capabilities are labeled Coming soon separately from public iOS2.1. Existing analytics must be verified before being restored; no tracking scope was added.

## Approval, cutover and rollback gates

1. Review content, platform claims and research wording. Research goals are not clinical results or an institutional endorsement.
2. Confirm exact repository, Pages entitlement/source, canonical hostname, deployment branch, HTTPS/certificate behavior, and write access. Reconcile current remote changes before any approved push; local draft baselines are not assumed to be the current production tip.
3. Save a full export/backup of current hosting, route inventory, analytics configuration, seller file, DNS and HTTPS settings. Public crawling cannot prove hidden-route parity.
4. Build an immutable production artifact and record checksums. Test on an expressly approved preview host first, including true404s, legacy aliases, mobile downloads, analytics and byte-exact root text/plain seller delivery. Do not index a preview.
5. Approve the exact publication and any DNS change separately. Retain the old host and original deployment/DNS configuration through verification. No console enrollment or IndexNow submission is included.
6. After approved cutover verify apex/www, representative deep URLs, privacy/history/terms, app-ads.txt200 text/plain, robots/sitemap/canonicals, store downloads, browser animation and analytics. If these fail, restore the recorded old host/DNS and known-good deployment; keep the new artifact for diagnosis. DNS rollback is subject to propagation/TTL, so do not delete the old host.

No rankings, AI citations, traffic improvement or Core Web Vitals field pass is asserted by local validation. The useful content and download paths establish a foundation for conversion; real traffic and conversion need measurement after approved publication.
