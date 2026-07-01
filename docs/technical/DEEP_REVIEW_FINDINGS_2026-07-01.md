# Deep Review Findings - 2026-07-01

## Scope

This note consolidates three independent read-only reviews of the Lane LaTeX
Template:

1. Maintainability and LaTeX/code best practices.
2. Repository professionalism and documentation.
3. Typography.

The reviews were performed by three separate explorer agents and then
cross-checked against the live checkout.

## Baseline Verification

Shared baseline commands:

```bash
make lint
latexmk -pdf -interaction=nonstopmode main.tex
pytest -q
rg -n "Warning|Error|Undefined|Overfull|Underfull|WARN -" main.log main.blg
```

Observed status:

- `make lint` passed.
- `latexmk -pdf -interaction=nonstopmode main.tex` passed and reported
  `main.pdf` was already up to date.
- `pytest -q` passed with 17 tests.
- `main.blg` still contains two invalid ISBN warnings.
- `main.log` still contains one `\showhyphens` warning, overfull/underfull box
  records, and 241 `microtype` "Unknown slot number" records.
- Running `pytest -q` dirtied tracked log artifacts under
  `tests/compilation/logs/`, which is itself repository hygiene evidence.

## Part 1: Maintainability And LaTeX Best Practices

### P1 - `preamble-natbib.tex` Contradicts The Package Contract

Evidence:

- `paper/preamble-natbib.tex:42` loads `lltpaperstyle` without the `natbib`
  option.
- `paper/lltpaperstyle.sty:172` then follows the default bibliography path and
  loads `biblatex`.
- `paper/preamble-natbib.tex:50` loads `natbib` afterward.
- `paper/preamble-natbib.tex:91` defines `\citeauthor` and `\citeyear` with
  `\newcommand`, even though natbib already provides those commands.

Impact:

The documented natbib preamble can load incompatible bibliography systems and is
not a reliable public entry point.

Smallest next fix:

Load natbib before `lltpaperstyle`, then load
`\usepackage[natbib]{lltpaperstyle}` so the package detects natbib and skips
biblatex. Remove the redundant citation command aliases.

### P2 - Advertised Standalone Modules Are Not Standalone-Safe

Evidence:

- `paper/modules/README.md:3` says each module can be used independently.
- `paper/modules/lltlists.sty:398` uses `\AtBeginEnvironment` without requiring
  `etoolbox`.
- `paper/modules/lltmathgridlocked.sty:50` uses `\AtEndEnvironment` similarly.
- `paper/modules/lltfontfeatures.sty:120` uses `\addfontfeatures` while claiming
  pdfLaTeX Type 1 support.
- `paper/modules/lltfontfeatures.sty:154` defines `\textendash` and
  `\textemdash` with `\newcommand`.

Impact:

Users following module documentation can hit undefined control sequences or
command-already-defined failures before the main package is involved.

Smallest next fix:

Either document modules as internal-only, or add standalone smoke fixtures and
declare each module's dependencies locally.

### P2 - The DTX/INS Release Path Is Stale

Evidence:

- `paper/README-DTX.md:14` tells maintainers to run `latex lltpaperstyle.ins`.
- `paper/lltpaperstyle.ins:38` generates `lltpaperstyle.sty` from the DTX file.
- `paper/lltpaperstyle.dtx:179` is still v1.6.
- `paper/lltpaperstyle.dtx:241` says the rest of the implementation is omitted.
- `paper/lltpaperstyle.sty:68` is the live v1.7 package.

Impact:

A maintainer following the documented CTAN/docstrip workflow could overwrite the
current package with an older partial implementation.

Smallest next fix:

Mark the DTX path as non-authoritative until rebuilt, or regenerate the DTX from
the live source and add a check that docstrip output matches the shipped `.sty`.

### P2 - Module Ownership Is Still Ambiguous

Evidence:

- `paper/lltpaperstyle.sty` loads modules but later defines overlapping
  heading, paragraph, quote, list, and spacing behavior.
- Examples include overlap between `paper/lltpaperstyle.sty:944`,
  `paper/modules/lltheadings.sty:183`, and
  `paper/modules/lltparagraphs.sty:222`.

Impact:

Full-package behavior and standalone-module behavior can diverge silently, and
user overrides may be undone by later main-package definitions.

Smallest next fix:

Pick one owner per feature. Keep orchestration in `lltpaperstyle.sty`; move
implementation to modules, or make main-package compatibility shims use
`\providecommand` only.

### P2 - Manual `biblatex` Contract Allows Warnings

Evidence:

- `README.md:205` recommends loading `biblatex` before `lltpaperstyle`.
- `tests/fixtures/biblatex-manual-contract.tex:2` follows that pattern.
- `paper/lltpaperstyle.sty:149` loads `inputenc` later.
- `tests/compilation/logs/biblatex-manual-contract_pass3.log:140` contains
  `Package biblatex Warning: Load 'inputenc' before biblatex`.
- The bibliography test checks unresolved citations/references, not package
  warnings.

Impact:

A documented supported path can pass pytest while violating the project's
warning-clean build expectation.

Smallest next fix:

Document `inputenc` before manual `biblatex` for legacy pdfTeX, or stop
package-level `inputenc` loading on modern LaTeX. Then assert the fixture log has
no `biblatex Warning`.

### P3 - Default Pytest Gate Is Narrower Than Documented

Evidence:

- `AGENTS.md:19` says `pytest -q` diff-checks layout hashes.
- `tests/test_regression_harness.py` compiles a small subset and uses text
  assertions.
- `tests/README.md:38` says visual checks are manual.

Impact:

Visual or fixture-wide regressions can slip through the required pytest gate.

Smallest next fix:

Add a parametrized pytest smoke over the supported fixture set, then add stable
layout/text/hash assertions for public contracts that must not move.

## Part 2: Repository Professionalism And Documentation

### P1 - Active Onboarding Docs Contain Broken Paths

Evidence:

- `INSTALL.md:244`, `INSTALL.md:268`, and `INSTALL.md:331` still instruct users
  to load `paper/paperstyle`.
- `TROUBLESHOOTING.md:341`, `TROUBLESHOOTING.md:349`, and
  `TROUBLESHOOTING.md:460` reference absent files or packages:
  `preamble-overleaf.tex`, `paperstyle-overleaf`, and `paperstyle-minimal`.

Impact:

New users can hit dead instructions during first-run setup and support flows.

Smallest next fix:

Replace active examples with `\usepackage{lltpaperstyle}` and current options,
or explicitly mark legacy paths unsupported.

### P1 - Overleaf Support Claims Exceed Evidence

Evidence:

- `README.md:23`, `README.md:96`, and `README.md:165` say Overleaf works
  automatically.
- `README.md:76` says the exact Overleaf build identifier is unavailable.
- `TROUBLESHOOTING.md:334` says Overleaf is under investigation.

Impact:

Public compatibility claims are internally contradictory.

Smallest next fix:

Change public Overleaf language to "pending verification" unless a current
Overleaf compile log and build identifier are supplied.

### P1 - Active Repo Identity Still Reads Like An Old Paper Fork

Evidence:

- `Makefile:1` and `Makefile:280` say "East Asian Miracle Paper".
- `docs/guides/BIBLIOGRAPHY_GUIDE.md:3`,
  `docs/guides/LATEX_STYLE_STANDARDS.md:1`, and
  `docs/TROUBLESHOOTING.md:3` repeat East Asia paper framing.

Impact:

The project does not consistently present as a reusable Lane LaTeX Template.

Smallest next fix:

Rename active user-facing identity strings to "Lane LaTeX Template" and move
paper-specific examples to samples or archive.

### P2 - Documentation Index Is Stale

Evidence:

- `docs/README.md:7` lists `docs/audits/`.
- `docs/README.md:24` lists `docs/plans/`.
- `docs/README.md:67` links `technical/FINAL_COMPILATION_STATUS.md`.
- Those paths were not present in `rg --files`.

Impact:

The documentation hub cannot be trusted as a navigation surface.

Smallest next fix:

Regenerate `docs/README.md` from tracked files and separate active, internal,
and archived docs.

### P2 - Testing Documentation Misstates The Actual Workflow

Evidence:

- `AGENTS.md:19` says `pytest -q` diff-checks layout hashes.
- `tests/test_regression_harness.py:32` shows PDF text assertions and no hash
  checks.
- `docs/technical/TESTING.md:397` documents `make format-python`, but
  `Makefile:146` exposes `format`.

Impact:

Maintainers may run nonexistent or misunderstood gates.

Smallest next fix:

Create one canonical testing table covering `make lint`, `make build`,
`pytest -q`, `tests/run-tests.sh`, Poppler, and generated artifact paths.

### P2 - Version And Release Signals Conflict

Evidence:

- `README.md:616` says current release is `v0.1.0-beta`.
- `paper/lltpaperstyle.sty:68` advertises package v1.7.
- `docs/style/CHANGELOG.md:43` contains placeholder GitHub release links.

Impact:

Users cannot tell what version is supported or released.

Smallest next fix:

Choose one canonical root changelog/version source and archive or merge
`docs/style/CHANGELOG.md`.

### P2 - License And Security Polish Is Incomplete For GitHub Reuse

Evidence:

- `license/LICENSE.txt:1` is a short LPPL notice, not a root `LICENSE`.
- `SECURITY.md:32` says only "latest version" is supported.

Impact:

GitHub license detection and downstream reuse are weaker than they need to be.

Smallest next fix:

Add a root `LICENSE` with the full LPPL v1.3c text or standard notice, and make
supported versions explicit.

### P3 - Troubleshooting Is Duplicated And Divergent

Evidence:

- Both top-level `TROUBLESHOOTING.md` and `docs/TROUBLESHOOTING.md` exist.
- One contains obsolete Overleaf paths; the other uses East Asia framing.

Impact:

Users get inconsistent advice.

Smallest next fix:

Keep one canonical troubleshooting document and archive the other.

## Part 3: Typography

### P1 - Run-In `\paragraph` Collides With Body Text

Evidence:

- `main.tex:24` uses `\paragraph{Quick Reference}` followed by body text.
- `paper/modules/lltheadings.sty:130` defines run-in paragraph formatting.
- `pdftotext -f 2 -l 2 -layout main.pdf -` extracts
  `Quick ReferenceFor`.

Impact:

This is a real heading/body separation defect in the public template.

Smallest next fix:

Add a minimal paragraph fixture, then adjust only paragraph separator behavior.
Do not change heading size, spacing, font, or hierarchy.

### P1 - Nested Quote Macro Emits Incorrect Content

Evidence:

- `paper/lltpaperstyle.sty:425` defines
  `\newcommand{\nq}[2]{\kern0.02em``#1 \sq{#2} #1''\kern0.02em}`.
- `appendices/api_examples.tex:157` demonstrates
  `\nq{She said}{Hello there}`.
- `pdftotext -f 37 -l 37 -layout main.pdf -` extracts
  `She said 'Hello there'She said`.

Impact:

The typography API changes author text, not just styling.

Smallest next fix:

Correct `\nq` with fixture-backed coverage. The visual change should be limited
to removing the duplicated words.

### P2 - Dash Commands Need Controlled Glyph Verification

Evidence:

- `paper/lltpaperstyle.sty:339` defines `\emdash` using `---`.
- `appendices/api_examples.tex:92` demonstrates dash usage.
- The typography review reported double-hyphen-like output in the API demo.

Impact:

The special-character typography contract may be visually undermined.

Smallest next fix:

Create a controlled dash glyph fixture/raster check, then decide whether to use
explicit text dash commands. Preserve the current dash spacing policy unless a
visual change is approved.

### P2 - Documented Grid Contract Conflicts With Implementation

Evidence:

- `paper/STYLE_GUIDE.md:20` and `paper/README.md:1059` mention `12.65pt`.
- `paper/modules/lltdimensions.sty:22` implements `13.2pt`.
- `docs/GRID_SYSTEM_REFERENCE.md:52` says display math uses one grid unit.
- `paper/lltpaperstyle.sty:2557` uses `19.8pt` display skips.

Impact:

Future reviewers cannot tell whether grid deviations are bugs, historical notes,
or intended behavior.

Smallest next fix:

Reconcile docs to the live implementation or mark older audit material as
historical.

### P2 - Microtype Configuration Is Noisy And Partly Invalid

Evidence:

- `paper/modules/lltmicrotype.sty:293` configures mathematical/special-symbol
  protrusion.
- `main.log` contains 241 `Package microtype Info: Unknown slot number of
  character` records.

Impact:

Optical margin behavior is hard to trust despite documentation claiming full
microtype implementation.

Smallest next fix:

Restrict custom protrusion to encoding-valid glyphs or guard it by encoding,
then verify with an optical-margin fixture.

### P3 - Typography Regression Coverage Is Mostly Semantic Or Manual

Evidence:

- `tests/test_regression_harness.py` compiles a small subset and uses text
  assertions.
- `tests/README.md:36` describes visual checks as manual.

Impact:

Headings, captions, lists, floats, footnotes, and grid rhythm can drift without
an automated signal.

Smallest next fix:

Add temp-dir raster/hash checks for selected typography pages before approving
future visual changes.

## Visual Verification Plan

Before any typography fix that can affect output:

- Inspect existing `main.pdf` pages 2, 17-20, 23-25, 28, 35, and 37-38.
- Render these fixtures in `/private/tmp`, not the checkout:
  `heading-optimization-test.tex`, `list-optimization-test.tex`,
  `caption-test.tex`, `quote-test.tex`, `footnote-test.tex`,
  `crossref-test.tex`, `optical-margin-test.tex`, `hyphenation-test.tex`, and
  `float-test.tex`.
- Use `pdftoppm -png -r 144` or 300 dpi and compare page hashes plus cropped
  regions around headings, captions, footnotes, dash examples, and quote
  examples.
- Pair raster checks with `pdffonts`, `pdfinfo`, `pdftotext -layout`, and a log
  scan for `Overfull`, `Underfull`, `Unknown slot`, and warnings.

## Recommended Lane Order

1. Build hygiene and warning policy.
2. Package/API compatibility and maintainability.
3. Repository professionalism and documentation consolidation.
4. Typography contract fixes with rendered before/after evidence.
