# Deep Review Master Roadmap Plan

> **For agentic workers:** This is a staged roadmap, not an implementation plan.
> Use it to decide which lane plan to open next and which decisions must be
> resolved before writing that lane plan.

**Goal:** Convert the 2026-07-01 deep review findings into serialized, testable
lane plans without mixing build hygiene, package API repairs, documentation
cleanup, and visual-output changes.

**Architecture:** This roadmap is the master coordination layer. It does not
prescribe line-level patches. Each lane below should get its own implementation
plan only when that lane is ready to start, because earlier lanes may change the
evidence surface for later lanes.

**Tech Stack:** LaTeX2e/pdfTeX, `latexmk`, Biber/biblatex/natbib, shell test
harnesses, pytest, Poppler tools (`pdftotext`, `pdfinfo`, `pdftoppm`), and the
Lane LaTeX Template package files under `paper/`.

**Supersession:** This file supersedes the earlier 2026-07-01 deep-review
roadmap draft at this same path. It is now the canonical master roadmap for the
July 2026 deep-review remediation work. The older May 2026 plans in
`docs/superpowers/plans/` remain historical implementation plans for already
identified May findings; they are not active master roadmaps.

**Current decision record:**

- Accepted: Use four staged lane plans rather than one umbrella plan.
- Accepted: Create this tracked roadmap before opening the first detailed lane
  plan.
- Accepted: Use a hybrid serialized workflow: roadmap first, then plan and
  complete each lane in order.
- Accepted: Treat `docs/technical/DEEP_REVIEW_FINDINGS_2026-07-01.md` as the
  canonical findings source for lane scoping.
- Accepted: Typography-affecting fixes require rendered before/after evidence
  and explicit approval before layout hashes or visual baselines are refreshed.
- Accepted: The May 2026 plans may be consulted for historical context, but new
  remediation work should start from this roadmap and then open a fresh lane
  plan.

---

## Source Findings

Use the following as the evidence packet when drafting lane plans:

- `docs/technical/DEEP_REVIEW_FINDINGS_2026-07-01.md`
- The earlier-run comparison findings captured in the current conversation:
  warning-clean build status, `tests/check-spacing-integrity.sh main.pdf`
  failure, indentation contract inversion, concrete module-preload failure, and
  caption/grid documentation drift.
- Live local verification before each lane begins; do not rely on stale logs
  when a command is cheap to rerun.

## Lane Order

### Lane 1: Build Hygiene And Test Surface

**Purpose:** Make the local verification surface trustworthy before touching
compatibility, docs, or visual contracts.

**Scope candidates:**

- Biber warnings in `main.blg`, especially invalid ISBNs for
  `brown2018flexible` and `bringhurst2012elements`.
- Current `main.log` warning surface, including `\showhyphens`, overfull boxes,
  underfull boxes, overfull vbox evidence, and `microtype` unknown-slot records.
- Tracked test-log churn from `pytest -q`.
- `tests/check-spacing-integrity.sh main.pdf` failing density/page-efficiency
  heuristics.
- Clarify whether the repository requires warning-clean logs or only green exit
  codes.

**Non-goals:**

- No margin, font, color, grid, caption, heading, paragraph, or float-placement
  design changes.
- No bibliography-system redesign except minimal metadata fixes needed to remove
  Biber warnings.
- No Overleaf claim cleanup except where needed to describe local build/test
  gates accurately.

**Decision gates before drafting Lane 1:**

- Decide whether Lane 1 must reach zero warnings in `main.log` and `main.blg`,
  or whether some warnings may be documented as accepted.
- Decide whether overfull verbatim examples should be rewritten, resized, or
  documented as intentional demonstration artifacts.
- Decide whether `tests/check-spacing-integrity.sh main.pdf` is a hard gate, an
  advisory heuristic, or obsolete.
- Decide whether test harness logs should become entirely transient, move to a
  temp directory, or remain committed golden logs.

**Likely verification:**

```bash
make lint
latexmk -pdf -interaction=nonstopmode main.tex
latexmk -pdf -interaction=nonstopmode -g main.tex
pytest -q
git status --short
rg -n "Warning|Error|Undefined|Overfull|Underfull|WARN -" main.log main.blg
rg -c "Unknown slot number" main.log
tests/check-spacing-integrity.sh main.pdf
```

### Lane 2: Compatibility And Package API

**Purpose:** Repair advertised compatibility paths after the build/test surface
is reliable.

**Scope candidates:**

- Broken `paper/preamble-natbib.tex` path.
- Stale `.dtx` / `.ins` extraction path that emits an obsolete package stub.
- Optional font modules that fail standalone, including `lltfontfallbacks` and
  `lltfontfeatures`.
- General standalone-module claims in `paper/modules/README.md`.
- Module-preload collisions such as `lltparagraphs` before `lltpaperstyle`.
- Manual `biblatex` loading path that currently permits package warnings.
- Ambiguous module ownership between `lltpaperstyle.sty` and module files.
- Clarify the real `minimal` option contract.

**Non-goals:**

- No default visual-output changes unless a compatibility fix cannot work
  without them and the change is explicitly approved.
- No broad package modularization beyond the smallest contract-preserving fix.

**Decision gates before drafting Lane 2:**

- Decide whether `.dtx` / `.ins` should be made authoritative now or clearly
  marked non-authoritative until a release-packaging pass.
- Decide whether standalone module support is a public contract or should be
  narrowed in documentation.
- Decide whether `minimal` should mean genuinely essential-only or simply
  "reduced typography modules."
- Decide whether module preloading is a supported extension mechanism or an
  internal implementation detail.

**Likely verification:**

```bash
make lint
latexmk -pdf -interaction=nonstopmode main.tex
pytest -q
tests/run-tests.sh
git status --short
```

Add focused temp-dir or pytest probes for natbib preamble, DTX extraction,
standalone optional modules, module-preload cases, manual `biblatex` warnings,
and `lltpaperstyleminimal.sty`.

### Lane 3: Repository Professionalism And Documentation

**Purpose:** Make the repository present as a reusable Lane LaTeX Template
rather than a mixed historical project fork.

**Scope candidates:**

- Stale `paper/paperstyle` paths in active onboarding docs.
- Unsupported Overleaf "works automatically" claims.
- East Asian Miracle identity in active files.
- Broken `docs/README.md` index entries.
- Duplicate troubleshooting surfaces.
- Release, license, CTAN, and versioning signals.
- Testing documentation claims that do not match the actual pytest and shell
  harness behavior.
- Documentation split between active user docs, maintainer docs, historical
  audits, and archived implementation notes.

**Non-goals:**

- No package behavior changes.
- No typography changes.
- No claim of Overleaf verification unless exact Overleaf log/build evidence is
  supplied.
- No attempt to make CTAN/release promises until Lane 2 resolves whether the
  DTX/INS path is authoritative.

**Decision gates before drafting Lane 3:**

- Decide whether active docs should say "Overleaf pending verification" or wait
  for current Overleaf evidence before closing the lane.
- Decide whether historical EastAsia material should be archived, renamed, or
  deleted.
- Decide whether CTAN material is an active release target or a future-only
  archive.
- Decide whether `docs/README.md` should be regenerated mechanically from
  tracked files or maintained manually with a short curated index.

**Likely verification:**

```bash
make lint
latexmk -pdf -interaction=nonstopmode main.tex
pytest -q
rg -n "paper/paperstyle|paperstyle-overleaf|preamble-overleaf|East Asian Miracle|EastAsia|Overleaf.*works automatically" README.md INSTALL.md TROUBLESHOOTING.md docs paper Makefile
rg -n "format-python|layout hash|FINAL_COMPILATION_STATUS|docs/audits|docs/plans" AGENTS.md README.md docs tests Makefile
```

### Lane 4: Typography Contracts

**Purpose:** Resolve mismatches between documented typographic intent,
implementation, fixtures, and rendered output.

**Scope candidates:**

- Run-in `\paragraph` collision producing `Quick ReferenceFor` in `main.pdf`.
- `\nq` nested quote macro duplicating its first argument.
- First-paragraph indentation after headings, lists, quotes, and displays.
- The apparent inversion between the first-paragraph indentation comments and
  `\@afterindentfalse` aliasing.
- Caption width, font size, and hanging-indent contract drift.
- Table and figure note environments versus bare note commands.
- Baseline-grid spacing documentation versus effective settings.
- Dash glyph rendering in the API examples.
- `microtype` unknown-slot records insofar as they affect optical margin
  behavior after Lane 1 decides warning policy.
- Color, list-metric, footnote, and accessibility documentation drift.

**Non-goals:**

- No silent visual changes.
- No layout hash refresh without a before/after rendered-page review.
- No margin, font, color, spacing, numbering, or float-placement default changes
  unless explicitly approved as part of this lane.

**Decision gates before drafting Lane 4:**

- Decide whether the current rendered output or the documented typography
  contract is authoritative for each mismatch.
- Decide which pages/fixtures form the visual approval baseline.
- Decide whether visual approval is manual rendered-page inspection, raster
  hash comparison, or both.
- Decide whether content-correctness fixes with visual effects, such as `\nq`,
  can proceed under the smallest-change rule before broader typography work.

**Likely verification:**

```bash
make lint
latexmk -pdf -interaction=nonstopmode main.tex
pytest -q
pdftotext -f 2 -l 2 -layout main.pdf -
pdftotext -f 37 -l 37 -layout main.pdf -
pdftoppm -png -r 144 main.pdf /private/tmp/llt-main
```

Add targeted fixture renders for headings, lists, captions, notes, math,
footnotes, quotes, dashes, and appendices before accepting any visual change.

---

## Cross-Lane Rules

- Every material LaTeX code fix must include a `%% FIX:` comment with a concise
  rationale.
- Update `CHANGELOG.md` and relevant README sections after material changes.
- Keep commits path-scoped to the active lane.
- Preserve unrelated dirty state if it appears during implementation.
- If a lane changes the evidence surface for a later lane, refresh the later
  lane's assumptions before drafting it.
- Do not use Overleaf language stronger than the evidence available in the
  current checkout or supplied compile log.
- Do not stage or revert unrelated dirty files. If generated logs are dirty,
  document whether they are lane evidence or cleanup targets.
- Run the lane's targeted verification before updating docs to claim success.

## Roadmap Close Criteria

- Lane 1 is complete when the local build/test surface is explicit, repeatable,
  and leaves no unintended tracked-file churn or explicitly documents accepted
  churn.
- Lane 2 is complete when public compatibility and package API paths either
  compile or are honestly documented as unsupported.
- Lane 3 is complete when active documentation, repository identity, and release
  claims are coherent.
- Lane 4 is complete when typography contracts match implementation and rendered
  output, with visual changes explicitly approved.

## Next Question Queue

Use the `grill-me` pattern before drafting each lane plan. Ask one decision at a
time, starting with the first unresolved gate for the active lane.

Initial Lane 1 question:

> Should the build hygiene plan require zero warnings in `main.log` and
> `main.blg`, or should it permit explicitly documented accepted warnings?

Follow-up Lane 1 question:

> Should `tests/check-spacing-integrity.sh main.pdf` become a hard gate for the
> main template PDF, remain an advisory diagnostic, or be rewritten before it is
> used for pass/fail decisions?
