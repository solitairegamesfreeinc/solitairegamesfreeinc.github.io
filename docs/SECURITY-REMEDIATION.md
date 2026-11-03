# Local security remediation — 3 November 2026

The modern pages build with Python standard library and need no npm dependencies. The old New Age/Gulp3/node-sass/browser-sync tree and unused jQuery/BootstrapJavaScript were retired, rather than upgraded into an unused build. npm manifest/lockfile now have zero dependencies. The former full/minified/slim vendor copies and obsolete theme scripts are removed. Bootstrap CSS and icon assets remain only as static legacy styling references; no Bootstrap or jQuery executable is shipped. Unity game build bytes remain frozen and are not represented as an audited engine release.

Legacy legal/support pages now use an accessible native wrapper and small local CSS, with the entire original content fragment unchanged. evidence/legal-content-preserved.json records prior source digests and exact fragments; check.py verifies them in source and output. Policy text, ratings/reviews, game features and ad sellers are not edited.

No Dependabot alert was dismissed, no security setting changed and no remote branch was updated. GitHub's counts remain open until reviewed commits reach the default branch and GitHub rescans. A zero npm audit is a dependency-graph result, not proof a whole website is vulnerability-free. Host security headers and account controls remain deployment concerns.
