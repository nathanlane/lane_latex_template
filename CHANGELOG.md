# Changelog

All notable changes to the Lane LaTeX Template are documented here.

## 2026-07-02

- Added compatibility fixes for natbib entry-point and standalone module contracts:
  `paper/preamble-natbib.tex` now loads `lltpaperstyle` in `natbib` mode and
  uses conditional citation aliases to avoid duplicate command-definition errors.
- Added explicit standalone dependency declarations for `lltlists` (`graphicx`,
  `etoolbox`) and `lltmathgridlocked` (`etoolbox`) so hooks and marker
  rendering work when loaded outside `lltpaperstyle`.
- Marked `.dtx/.ins` usage as non-authoritative in `paper/README-DTX.md` and
  updated compatibility wording in `paper/modules/README.md` and `README.md` for
  the separate `lltpaperstyleminimal` package surface.
- Extended test harnesses with compatibility probes for standalone/preload contract
  paths, including `lltfontfeatures`, and fixed harness artifact handling for
  temporary compatibility probes.
- Added manual biblatex-warning enforcement in `tests/test-bibliography.sh`.
- Added regression assertion that `tests/run-tests.sh` executes compatibility
  probes in the pytest harness.
- Hardened compatibility-probe control flow in `tests/run-tests.sh` so all probes
  execute and report cumulative failures before failing the lane harness.
- Removed the stale `lltpaperstyleminimal` option claim from `README.md` package
  options and aligned standalone-module documentation language in
  `paper/modules/README.md` with validated dependency requirements.

## 2026-07-01

- Added a consolidated deep review findings note covering maintainability,
  repository documentation/professionalism, and typography.
- Added a master roadmap plan for turning the deep review findings into
  serialized build, package API, documentation, and typography lane plans.
- Added lane-1 build hygiene fixes: removed malformed ISBN metadata warnings
  from `references.bib`, made `tests/compilation/logs/*.log` transient in
  `.gitignore`, and documented the verification artifact contract.
- Classified `main.log`/`main.blg` warning policy and spacing-integrity check as
  advisory in this lane; updated verification guidance in `README.md`,
  `tests/README.md`, and `docs/technical/TESTING.md`.
- Made `tests/check-spacing-integrity.sh` self-describe as an advisory diagnostic
  that always exits 0 except on genuine tooling errors, matching the documented
  non-gating role (previously it exited 1 on heuristic spacing flags).
- Corrected the `tlmgr install` list in `README.md` to match the fonts actually
  loaded (`tgpagella`, `inconsolata`, `newpx`/newpxmath, `mathalfa`, `booktabs`);
  removed the spurious sans-serif math entry (`newpxsf`, no such package; the
  template loads no sans math).

## 2026-05-28

- Added a LaTeX package code review report focused on maintainability, option contracts, and package API risks.
- Added a checkpointed implementation plan for resolving the LaTeX package maintainability findings.
- Added reviewer findings for the LaTeX maintainability implementation plan.
- Updated the maintainability implementation plan to resolve reviewer findings before implementation.
- Added option-contract regression coverage for `nocolor`, `minimal,nocolor`, `draft`, `natbib`, `nobiblatex`, normal `\ref`, and subsection float-barrier modes.
- Made `nocolor` option-aware by loading semantic colors consistently and mapping template colors to black/grayscale values.
- Implemented native `natbib` mode, preserved `nobiblatex`, and removed the runtime warning wrapper around LaTeX's standard `\ref`.
- Made subsection float barriers an explicit package option with `nosubsectionbarriers` support.
- Consolidated active `microtype` loading and tuning into `lltmicrotype` while preserving default raster output.
- Resolved follow-up P1/P2 review findings for public text-symbol commands and active microtype ownership in `lltmicrotype`.
- Restored legacy emphasis, small-caps, dash, ellipsis, note, divider, and symbol command compatibility covered by existing fixtures.
- Fixed quote/list environment closure, nested `readableitem` labels, dagger recursion, and floatless caption warnings surfaced by the fixture harness.
- Updated LaTeX fixtures to use current package names and a two-pass compile harness for stable hyperref/rerun checks.
- Clarified the canonical bibliography loading contract and documented the manual `nobiblatex` override path.
- Added regression coverage for manually loaded biblatex with `lltpaperstyle[nobiblatex]`.
- Fixed the bibliography test harness package search path for direct fixture runs.
- Documented the Poppler `pdftotext` dependency used by PDF text regression assertions.
- Made the compatibility regression test skip PDF text assertions clearly when `pdftotext` is unavailable.

## 2026-05-27

- Restored optional footnote mark support and appendix section compatibility for starred and short-title forms.
- Added a focused regression fixture for footnote and appendix compatibility backports.
- Restored the repository infrastructure contract so the AGENTS.md lint, build, and regression gates are runnable from the root.
- Resolved the active merge marker in `main.tex` without changing the intended LaTeX layout.
- Updated active build and test references from the removed package name to `lltpaperstyle`.
- Added pytest coverage for build-target drift, executable shell harnesses, root changelog presence, active package references, and the minimal LaTeX regression harness.
