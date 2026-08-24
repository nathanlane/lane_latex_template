# Changelog

All notable changes to the Lane LaTeX Template are documented here.

## Unreleased

Corrected package paths in the adopter-facing docs that #47 left stale:

- `README.md`'s directory diagram still showed `lanepaper/preamble.tex` and a
  `lanepaper/modules/` subdirectory. Neither exists: `preamble.tex` lives with
  the document in `demo/`, and #47 flattened the modules into `lanepaper/`.
- `README.md`'s first-document instructions told adopters to
  `\input{demo/preamble.tex}` — a path inside this repository, not theirs.
  Replaced with the two lines that file actually contains.
- `README.md`'s version history and `CONTRIBUTING.md`'s namespace section both
  cited `paper/lanepaper.sty`, a path removed by #47.

The stale-name guard in `tests/test_infrastructure.py` scans `.tex`, `.sty`,
`.sh` and `.py` only, so none of these were caught automatically.

Added LPPL 1.3c headers to all 16 package files (issue #53):

- Every file in `lanepaper/` now carries the license, the `maintained`
  maintenance status, and the Current Maintainer. Previously 0 of 16 did, which
  is a CTAN review blocker: `LICENSE` at the repository root is not sufficient.
- The header text comes from `licenses/LICENSE.txt`, which already named
  Nathan Lane as copyright holder and Current Maintainer. Two things changed
  there: the year is now 2025-2026, and "This work consists of the file .sty
  files and content of this repo" became "the files in `lanepaper/`". After
  #47 that line matters — it defines the licensed Work, and `demo/`, `docs/`
  and `tests/` are not part of what ships.
- `tests/test_infrastructure.py` asserts every `lanepaper/*.sty` carries the
  header, so a new module cannot skip it. Confirmed the guard fails when a
  header is removed.
- Fixed the banner comment in all 16 files: each named a pre-2025 filename
  (`PAPERSTYLE.STY`, `COLORS.STY`, `MICROTYPE-CONFIG.STY`). These are
  uppercase, so the #46 rename sweep did not reach them.
- Replaced three `% Author: Academic Paper Template Project` placeholders,
  which contradicted the project's own license file.

Headers are comments: `main.pdf` is unchanged, byte for byte, against the
pre-rename baseline. `pytest -q` 32 passed; `tests/run-tests.sh` 115 passed.

Moved to the package-first layout (branch `refactor/rename-lanepaper-46`,
issue #47, ADR-0001):

- `lanepaper/` holds the 16 `.sty` files and nothing else, flattened — the
  `modules/` subdirectory is gone, so `TEXINPUTS` is one entry instead of two
  and the directory is exactly what `l3build install` installs and what a
  `git subtree` pull carries.
- `demo/` holds the CI fixture document: `main.tex`, `preamble.tex`,
  `preamble-natbib.tex`, `titlepage.tex`, `appendices/`, `figures/`, and
  `references.bib`. It is not a starting point for papers.
- `paper/` no longer exists. Its eleven Markdown files moved to
  `docs/package/`, except `MIGRATION.md` and `MODULARIZATION_ACTION_PLAN.md`
  which are historical and moved to `docs/archive/`. `paper/modules/README.md`
  became `docs/package/modules.md` to avoid colliding with `paper/README.md`.
- `TEXINPUTS` now covers `./lanepaper:./demo` and `BIBINPUTS` covers `.:./demo`,
  so `main` and `references.bib` still resolve from the repository root and
  `main.pdf` is still written there. CI needed no path changes as a result,
  including the `upload-artifact` path and the `safe.directory` step.
- `.gitignore`'s figure negation is now `!demo/figures/*.pdf`; verified that a
  PDF there is tracked while other PDFs stay ignored.
- Fixed 16 test fixtures and development documents that loaded
  `\input{paper/preamble.tex}` by path, plus the `prelude-natbib-preamble`
  compatibility probe in `tests/run-tests.sh`.
- Regenerated `docs/PACKAGE_NAMING_CONVENTION.md` from the actual file list and
  repaired five documentation links that the move had broken or silently
  repointed.

Verified by 150dpi raster comparison against the pre-rename baseline. Four of
40 pages differ, each for a stated reason: the title page's `\today` line
(the baseline was built two days earlier), two pages where the demo prints its
own `\usepackage` line, and one where it cites the style guide's new path.
`pytest -q` 31 passed; `tests/run-tests.sh` 115 passed, 0 failed;
`make lint`, `make build`, and the style validator all clean.

Renamed the package to `lanepaper` and unified the internal prefix to `\lnp@`
(branch `refactor/rename-lanepaper-46`, issue #46, ADR-0001):

- `\usepackage{lltpaperstyle}` is now `\usepackage{lanepaper}`. The 16 `.sty`
  files were renamed: `paper/lanepaper.sty` is the package, `lnpminimal` and
  `lnpgridoverlay` are the other entry points, and the 13 modules are `lnp` +
  role. The short prefix follows CTAN practice — `biblatex` ships `blx-*.sty`
  with `\blx@` macros; compare `\MT@`, `\Hy@`, `\Gm@`, `\ttl@`.
- Five competing internal prefixes collapsed into `\lnp@`: `\paper@` (105),
  `\ifllt@` (32), `\llt@` (27), `\paperstyle@` (6), `\lltpaperstyle@` (4) and
  `\lltfontfeatures@` (5). LaTeX kernel macros (`\p@`, `\f@`, `\z@`,
  `\tagform@`, `\maketag@`, `\g@`) are untouched — verified by count.
- The undecorated `\paperstyle*` family (24 macros) went the same way. The 22
  internal ones are now `\lnp@*`; the two entry points a user actually types
  are `\lanepaperdiagnostics` and `\lanepaperinfo`. `\lanepaperinfo` is
  defined but never called anywhere — left in place, worth revisiting.
- Removed 137 `\makeatletter`/`\makeatother` lines from the package files.
  `@` is a letter inside a `.sty` by construction, so each `\makeatother` was
  revoking that for the rest of the file; the old macro names had no `@` so
  nothing noticed. With `\lnp@` names this broke the build outright at 39
  sites. `lnplists.sty` also had one unbalanced `\makeatletter`.
- `tests/test_infrastructure.py` now guards both generations of retired names —
  the pre-2025 `paper/paperstyle` layout and the `llt*` / prefix names — and
  builds its pattern by concatenation so it cannot match its own source.
- `docs/PACKAGE_NAMING_CONVENTION.md` was regenerated from the actual file
  list; it had carried four modules that never existed
  (`lltcompilationfixessimple`, `lltmicrotypeconfig`,
  `lltmathematicsgridlocked`, `llthochulirefinements`) since July 2025.
  `NAMESPACE_CONVENTIONS.md` records why `\lnp@` was chosen over `\lane@`.
- Archival documents keep the old names on purpose: the ADRs, `CONTEXT.md`'s
  glossary, dated reviews and audits under `docs/`, `docs/archive/`,
  `paper/MIGRATION.md`, and this file's history.

Verified by per-page raster comparison at 150dpi against the pre-rename build.
`main.pdf`: 38 of 40 pages byte-identical; pages 4 and 39 differ only where the
demo prints `\usepackage{lltpaperstyle}` in its own code listing, which the
rename is supposed to change. `tests/fixtures/opening-test.tex`, the only
document exercising `\firstlinesc`, is identical on all 5 pages. `pytest -q`
31 passed; `tests/run-tests.sh` 115 passed, 0 failed.

Deleted the stale `.dtx`/`.ins` scaffold (branch `chore/delete-dtx-scaffold-49`,
issue #49):

- Removed `paper/lltpaperstyle.dtx`, `paper/lltpaperstyle.ins`, and
  `paper/README-DTX.md`. The `.ins` declared
  `\generate{\file{lltpaperstyle.sty}{\from{lltpaperstyle.dtx}{package}}}`, but the
  `.dtx` was a 252-line v1.6 scaffold from 2025-07-09 against a shipping `.sty`
  of 3206 lines at v2.0, and it ended with "the rest of the implementation would
  continue here". Running the documented docstrip workflow would have replaced
  the package with a stub.
- Nothing built from them: no reference in `Makefile`, `.latexmkrc`,
  `compile.sh`, the shell harnesses, the pytest suite, or CI.
- CTAN accepts plain `.sty` plus README and documentation; per ADR-0002 the
  release path is `l3build ctan`, not docstrip.
- Surviving `.dtx` mentions are deliberate: LPPL boilerplate in `LICENSE`,
  history in this file, and the dated review records under `docs/`. The
  contradictions in `docs/PACKAGE_ROADMAP.md` belong to issue #52.

Stopped the microtype tracking-list churn (branch `fix/tracking-lists-39`, issue #39):

- `main.log` tracking-override messages: 40 -> 0. Every per-invocation
  `\SetTracking` in an executable macro body is now `\textls`, which states the
  amount at the point of use instead of declaring a global list. The nine
  package-load declarations in `lltmicrotype.sty` are intentional and unchanged.
- The original plan for this issue — declaring named lists at load and selecting
  them per macro — is not possible: microtype provides `name` and `load` for
  declaring and inheriting lists, but no point-of-use selection.
- Most per-site amounts turned out to be inert, clobbered by `\SetTracking`'s
  global scope, and were dropped. Four contexts where the amount really did
  apply keep it explicitly: `\firstlinesc` and `lltparagraphs`' opening (exact
  11pt matches no named-size list), and the three OT1 sites in
  `lltfontfeatures.sty` (every tracking list declares `T1` only).
- Fixed a tracking leak in `\articletitlefootnote`: `\lsstyle` ran unscoped and
  bled past the title into its `\footnote`. It is now `{\lsstyle #1}\footnote{#2}`.
  This is the one intended rendering change.

Verified by per-page raster comparison at 150dpi rather than text extraction,
which cannot see reflow: 39 of 40 pages of `main.pdf` are byte-identical, and
page 1 differs only in the title and thanks-footnote bands. Because `main.tex`
does not exercise `\firstlinesc`, `tests/fixtures/opening-test.tex` was rendered
and compared as well — all 5 pages identical.

Documentation pass over the entry docs (branch `docs/entry-docs-pass`, issue #41):

- Cut `paper/README.md` from 1115 to roughly 690 lines, mostly duplication with
  `README.md` and `API_REFERENCE.md`.
- Corrected the documented font stack. `paper/README.md` claimed
  `newtxmath[libertine]`, `scaled=0.93`, and Bembo; the packages actually loaded
  are tgpagella, zi4 at `scaled=0.96`, newpxmath, and mathalfa
  (`paper/modules/lltfonts.sty`).
- Corrected microtype values (`1050/15/15`, not `1100/10/10`), the `\linespread`
  figure (1.20), the citation style (`authoryear`, not Chicago), and the
  bold-small-caps documentation, which described scaling and a `\balancedbsc`
  command that do not exist.
- Corrected two module classifications that contradicted the loader:
  `lltmicrotype` is always loaded, `lltmathgridlocked` never is.
- Removed a dead `examples/` reference from `INSTALL.md` and a
  `docs/typography/` path that resolved relative to `paper/`.
- Restored documentation for `\smartitalic`, `\smartbold`,
  `\thirdgridparagraphs`, `\refinedbullet`, and `\refineddash`, which an
  earlier draft of this pass had deleted while they remained implemented, and
  marked `\compactpar` and `\loosepars` deprecated to match the code.
- Narrowed claims to what is actually verified: tested TeX Live versions are
  named individually, MiKTeX is marked unverified, and quantum spacing is
  described as covering most rather than all vertical space, since
  `paper/modules/lltheadings.sty` uses 18pt and 6pt.

Cleanup nits (branch `chore/cleanup-nits-32`, issue #32):

- Retargeted `AGENTS.md` §7's dead `CLAUDE.md` reference to `paper/STYLE_GUIDE.md`
  and `docs/typography/`. No `CLAUDE.md` has ever existed in this repository.
- Fixed the BSD-grep `invalid character range` warning emitted by
  `src/sh/validate_latex_style.sh` on every file (43 per run). The math-operator
  bracket expressions used `[=+\-*/]`; BSD grep reads `\` literally inside a
  bracket expression, so this parsed as the reversed range `\`(0x5C)→`*`(0x2A).
- Rewrote that check to exempt subscript and superscript spans before testing
  for unspaced operators. Repairing the bracket expression alone made the check
  fire on `\sum_{i=1}^n` in `main.tex` and `tests/fixtures/full-features.tex`;
  indices are conventionally unspaced, so those were false positives the broken
  expression had been masking. The exemption is deliberately narrow — exempting
  every brace group would hide real defects such as `$\sqrt{x+y}$` and `${x=y}$`
  — and it tracks brace depth, since indices nest (`x_{\mathrm{i=1}}`).
- Spaced the operator in `\frac{1}{n-1}` at `main.tex:309`, the one genuine hit
  the repaired check found. TeX ignores whitespace in math mode; the rendered
  PDF text is unchanged (verified by `pdftotext` comparison — the PDF's bytes
  differ only through its embedded build timestamp).
- Added regression coverage for the check in `tests/test_infrastructure.py`, in
  all four directions: unspaced operators flag, operators inside brace groups
  still flag, and neither flat nor nested unspaced indices do. The check previously had no
  behavioural test, which is how one that silently malfunctioned went unnoticed.
- Added `poppler-utils` to the CI workflow's apt step. The PDF-text regression
  assertions in `tests/test_regression_harness.py` were skipping silently in CI
  for want of `pdftotext`, so footnote-mark and appendix-title leakage was
  caught only on machines with Poppler installed.

## v2.1.0 — 2026-08-19

Release polish pass (branch `chore/release-polish`):

- Removed byline and IPG attribution from README.md and `pdfauthor` metadata in main.tex.
- Updated tagline: "A living LaTeX template… Actively used and revised."
- Removed "production-grade" phrasing from README.md, main.tex (prose and `\subsection{Production-Grade Features}` heading), paper/README.md, and Makefile comment.
- Rewrote stub bullet in README.md features list with accurate, opt-in-aware claims about `llthochuli` optical refinements.
- Deleted research-repo scaffolding: `.env.example`, `data/raw/.gitkeep`, `data/processed/.gitkeep`; removed dead `cp .env.example .env` instructions from README.md and SECURITY.md; removed `touch .gitkeep` from `make setup` target.
- Updated Version History in README.md to `v2.1.0`.
- Fixed stale module filenames in paper/README.md module tree.

Added GitHub Actions CI workflow (branch `ci/build-and-test`, merged 2026-08-19): build, lint, and test gates now run on push and pull request.

## 2026-08-18

Pre-release hygiene batch (branch `chore/pre-release-hygiene`):

- Fixed `tests/fixtures/opening-test.tex`: added `\clearpage` before the
  `\section{Conservative Drop Cap Guidelines}` so the `\academicdropcap{W}{…}`
  call no longer falls at the bottom of page 3 where lettrine emits
  `*** ATTENTION REQUIRED ***`. Suite now reports 0 failures.
- Fixed `.gitignore`: `!figures/*.pdf` carried a trailing inline comment
  (`# …`), which git does not parse — the negation was silently inert. Moved
  the comment to its own preceding line; `git check-ignore -v figures/test.pdf`
  now returns the negation rule. Dropped `!tests/visual/output/*.pdf` entirely:
  those PDFs are regenerated on every `tests/run-tests.sh` run and should stay
  ignored.
- Removed 21 tracked internal-workspace files (`archive/**`, `tmp/ai-plans/**`,
  `docs/superpowers/plans/**`, `docs/tmp/plans/**`, `docs/ai-workflow/**`,
  `notes/**`). History retains the full content. Fixed all dead links in
  surviving tracked files that pointed into these paths (README.md,
  docs/README.md, docs/typography/BASELINE-GRID.md,
  docs/typography/BASELINE-GRID-DECISION.md, CHANGELOG.md).
- README.md: removed dead link to `CLAUDE.md` (gitignored, absent for
  cloners) and dead link to deleted plan doc; retargeted Contributing
  section to new `CONTRIBUTING.md`.
- Version reconciliation: bumped `\ProvidesPackage` in `lltcolors.sty`,
  `lltfonts.sty`, and `llthochuli.sty` from `v1.0 [2025/07/0x]` to
  `v1.1 [2026/08/12]` to align with the 2026-08-12 release date shared by
  all other modules; `lltpaperstyle.sty` (`v2.0`) and `lltmicrotype.sty`
  (`v1.2`) are unchanged.
- Added `CONTRIBUTING.md`: build (`make`), test suites (`bash tests/run-tests.sh`,
  `python3 -m pytest -q`, `make test`), `llt` namespace convention, and
  module doc locations.

## v2.0.0 — 2026-08-12

Release cut after the adopter defect report (see git history:
`notes/ADOPTER-DEFECT-REPORT-2026-08-11.md`). Two breaking changes:
`\sectionbreak` → `\sectionsep` and `\paragraphbreak` → `\paragraphsep`
(no aliases — the old names collide with titlesec's `\<level>break` hook and
must not be defined), and the `\le`/`\ge`/`\epsilon`/`\phi`/`\vec`
redefinitions moved behind the new `mathredefs` option (default off).
Migration: `paper/MIGRATION.md`.

All 2026-08-12 entries below constitute the release.

## 2026-08-12

- Fixed the three pre-existing overfull hboxes in the `main.tex` demo prose
  (8.2pt section heading, 16.8pt and 49.5pt `verbatim` examples) by
  rewording/reformatting demo content only — no template tolerance touched.
  `main.log` now reports zero overfull hboxes.

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
- Filed the adopter defect report (see git history: `notes/ADOPTER-DEFECT-REPORT-2026-08-11.md`).
- Harness hardening: `make lint` now covers `paper/` and `appendices/` (was
  root-only) and probes `-n48` support so ChkTeX 1.7.6 (TeX Live 2022) no
  longer fails the gate; committed the missing `src/sh/check-packages.sh`
  and made `make check-deps` fail loudly instead of echoing a fake-healthy
  fallback; fixed `src/sh/validate_latex_style.sh` (errexit killed it on the
  first diagnostic, paths escaped the repo root, and it checked another
  project's files); rewrote the TESTING.md log-analysis section that
  documented a never-committed `context/tools/log-parsing/` toolchain;
  added `tests/test_measured_values.py` — compile-time assertions on the
  measured `\baselineskip` (16.32pt), `\jot` (9.9pt), `\footnotesep` (inert
  floor), canonical penalties, and the `\DeclareMathSizes` firing — the
  regression net the defect report called for. Gates verified on both
  TeX Live 2022 and 2026; TROUBLESHOOTING documents the stale-aux failure
  when switching TeX Live versions.
- Deleted silently overridden duplicate assignments: `\spaceskip`/`\xspaceskip`
  (0.35em/0.5em declared early, 0.33em/0.48em in force), `\brokenpenalty`
  (5000 → 2000 in force), `\postdisplaypenalty` (10000 → 2000 in force), and
  the duplicate `\raggedbottom`, `\parindent`, and `\arraystretch`/`\tabcolsep`
  defaults. The in-force values were kept, so rendering is unchanged
  (verified: measured values byte-identical before/after). Widow/orphan
  penalties now have one canonical home in `lltpaperstyle.sty` (10000/10000/
  10000); the `lltheadings` and `lltcompilationfixes` restatements are gone,
  and the gridlocked modules' softer penalties (5000) are documented as an
  intentional grid-mode variant regime.
- Footnote machinery: marker box widened 7pt → 11.5pt (body and title-page
  blocks). Measured at the marker's spec, Pagella's tabular old-style digits
  are 3.6pt each: two-digit markers (7.2pt) already overflowed the 7pt box
  (hidden by `\hfuzz`) and three-digit markers (10.8pt) overprinted note
  text; wrapped-line indent matches the wider box. Rendered delta: footnote
  text shifts right 4.5pt (single-digit gap 3.4pt → 7.9pt, two-digit gap
  → 4.3pt). Dropped footmisc's inert `hang,flushmargin` options
  (Lane's own `\@makefntext` replaced their implementation) and the inert
  `\footnotemargin` settings; documented `\PassOptionsToPackage` before
  `\usepackage{lltpaperstyle}` as the supported way to pass footmisc options
  such as `bottom` without an option clash. Corrected the `\footnote`
  redefinition comment (the `\nobreak` acts on footnote text, not the mark).
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
  Research brief archived in git history as `notes/baseline-grid-decision-brief.md`.
- Re-documented the grid-derived constants to match the measured build
  (decision (b) follow-through; rendering unchanged except where noted):
  every "13.2pt baseline/leading" claim in code comments and docs now states
  the true values (10.95pt body, 16.32pt baseline, 13.2pt spacing quantum);
  the `[grid]` overlay's base lines step at the real `\baselineskip` instead
  of confirming the false premise; `\DeclareMathSizes` is keyed to 10.95pt so
  it actually fires (scriptscript 6.1pt → 6pt, the declared value);
  `\jot` (ships as 9.9pt), `\footnotesep` (inert floor, not inter-note
  space), `\extrarowheight`/table-row (~21.8pt rows), footnote leading (12pt
  actual), and the `\spaceskip` body-size freeze comments now describe what
  the build does. Review sweep also corrected: float-skip values in
  BASELINE-GRID.md (now the measured 13.2/13.2/9.9pt), table-row arithmetic
  (~21.8pt standard), remaining false claims in STYLE_GUIDE,
  CUSTOM_COMMANDS, modules docs, and the `main.tex` demo prose (main.pdf
  demo text now states 10.95pt/16.32pt; 40 pages).

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
