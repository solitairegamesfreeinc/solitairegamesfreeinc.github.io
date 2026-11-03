# Solitaire Games Free website

Static app discovery pages, gameplay guides and preserved legal/game routes for https://solitairegamesfreeinc.com. The supported build uses Python standard library; no npm install or retired Gulp theme is needed.

```sh
python3 scripts/build.py
python3 scripts/check.py
```

The default dist artifact is noindex for review. If the existing local preview is stopped, run `python3 scripts/serve_preview.py --root dist --port 8764` and open http://127.0.0.1:8764/ on that same Mac. It binds loopback only.

Edit the static game/guide HTML and landing.css. See docs/SELF-HOSTING.md for production build, exact publisher files, GitHub Pages artifact publishing, approval and rollback; docs/SECURITY-REMEDIATION.md explains dependency retirement and legal-content preservation. Publishing onto the existing production branch can deploy automatically, so do not push a review build there.
