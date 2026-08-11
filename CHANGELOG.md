# Changelog

All notable changes to the Lane LaTeX Template are documented here.

## 2026-08-11

- **Breaking rename:** `\sectionbreak` → `\sectionsep` and `\paragraphbreak` →
  `\paragraphsep`. titlesec executes any defined `\<level>break` macro as a
  hook during heading construction; `\paragraphbreak` made run-in `\paragraph`
  fail with "perhaps a missing `\item`", and `\sectionbreak` silently injected
  `\vspace{2\gridunit}` (26.4pt) before every `\section` in place of the
  intended `\@secpenalty`. After the rename, section spacing matches the
  declared `\titlespacing` values — rendered output loses the accidental
  26.4pt per-section gap and regains break-before-section penalties.
- Removed `\SetTracking`/`\lsstyle` from the `\titleformat` blocks for
  `\section` and `\subsection`: `\SetTracking` is global and the package's own
  microtype `series=b` rule annulled the declared +80/+60 heading tracking, so
  the lines were dead code that also churned the tracking list document-wide
  (122 override messages per build).
- Fixed run-in `\paragraph` emitting zero space before the following text
  ("RobustnessEstimates"): dropped the `[~]` after-code and set the
  `\titlespacing` after-value to `0.75em` (same fix applied to `\paragraphsc`).
- Filed the adopter defect report under `notes/`.
- **Behavior change:** the `\le`/`\ge`/`\epsilon`/`\phi`/`\vec` redefinitions
  moved behind a new `mathredefs` package option, default off. A typography
  package must not change what a manuscript's mathematics says; documents
  relying on the variants should pass
  `\usepackage[mathredefs]{lltpaperstyle}`.
- Fixed `\SetTracking` leaking its tracking amount into PDF bookmarks
  ("1 60Identification Strategy"): the `\pdfstringdefDisableCommands`
  substitution now discards both arguments.
- Corrected the `\hfuzz=0.2pt` comment: it is *looser* than LaTeX's 0.1pt
  default, not "tighter" (value unchanged).
- Split the qpl protrusion lists by encoding: TS1-only symbols
  (`\textdagger`, `\textdaggerdbl`, `\textparagraph`,
  `\textasteriskcentered`, `\texteuro`) moved to a TS1 list, OT1 dropped
  (all twelve symbol keys fail microtype's OT1 slot lookup), brace keys
  re-spelled `\textbraceleft`/`\textbraceright` in the T1 list, and a
  mistyped `\ ` (control space) backslash key spelled `\textbackslash`.
  "Unknown slot number" microtype messages per build: 231 → 0. Intended
  rendering delta: title-page footnote marks (`*`, †, ‡) now actually
  protrude (~1pt left shift); everything else unchanged (39 pages).
- Recorded the baseline-grid decision in
  `docs/typography/BASELINE-GRID-DECISION.md`: re-document the true measured
  values (10.95pt body, 16.32pt baseline) and treat `\gridunit` as a spacing
  quantum, not the document baseline; making the 13.2pt grid real was rejected
  because it requires removing `\linespread` and would shrink documents ~19%.
  Research brief: `notes/baseline-grid-decision-brief.md`.

## 2026-07-04

- Removed active documentation claims about unverified external build support,
  keeping the public setup guidance tied to locally verified `latexmk`, `chktex`,
  pytest, and shell-harness checks.
- Replaced stale `paper/paperstyle` examples in installation and troubleshooting
  docs with current `lltpaperstyle` package names while preserving the README
  migration note for older documents.
- Reworked active repository-identity text, testing guidance, docs index,
  supported-version policy, and release/version wording around the Lane LaTeX
  Template.
- Added a root `LICENSE` containing the LPPL v1.3c text, renamed the legacy
  short-notice directory to `licenses/` to avoid a case-folding collision, and
  archived the duplicate troubleshooting guide under `docs/archive/`.

## 2026-07-02

- Added compatibility fixes for natbib entry-point and standalone module contracts:
  `paper/preamble-natbib.tex` now loads `lltpaperstyle` in `natbib` mode and
  uses conditional citation aliases to avoid duplicate command-definition errors;
  the legacy DOI prefix customization is guarded for TeX Live variants without
  `\doiprefix`.
- Reworked `lltpaperstyle` package loading so `inputenc` is loaded lazily before
  bibliography setup and never after manually loaded `biblatex`; documented that
  `nobiblatex` leaves both bibliography and encoding setup to the caller unless a
  modern LaTeX UTF-8 default is sufficient.
- Added explicit standalone dependency declarations for `lltlists` (`graphicx`,
  `etoolbox`) and `lltmathgridlocked` (`etoolbox`) so hooks and marker
  rendering work when loaded outside `lltpaperstyle`.
- Added paragraph preload ownership shims in `lltpaperstyle`/`lltparagraphs` so
  the supported optional-module-before-main-package order remains stable, and
  documented that loading `lltparagraphs` after `lltpaperstyle` is unsupported
  unless the reverse order is fully guarded.
- Repaired standalone module/package surfaces for `lltfontfallbacks` local
  font-availability conditionals, `lltfontfeatures` dash/text-symbol aliases,
  and `lltpaperstyleminimal`'s package-hook dependency on `etoolbox`.
- Marked `.dtx/.ins` usage as non-authoritative in `paper/README-DTX.md` and
  updated compatibility wording in `paper/modules/README.md` and `README.md` for
  the separate `lltpaperstyleminimal` package surface.
- Extended test harnesses with compatibility probes for standalone/preload contract
  paths, including `lltfontfeatures`, and fixed root-level auxiliary artifact
  cleanup for temporary compatibility probes.
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
