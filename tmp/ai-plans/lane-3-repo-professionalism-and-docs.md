---
topic: lane-3-repo-professionalism-and-docs
created: 2026-07-03
status: Draft
---

# Lane 3: Repository Professionalism And Documentation

## Task

- Summary: Make the repository present as a reusable *Lane LaTeX Template*
  rather than a mixed historical paper fork, by repairing documentation-only
  professionalism defects surfaced in the 2026-07-01 deep review (Part 2). This
  is the third lane of the deep-review roadmap
  (`docs/superpowers/plans/2026-07-01-deep-review-roadmap.md:155`), run after
  Lane 1 (build hygiene) and Lane 2 (compatibility/API), both merged to `main`.
- Requested outcome: Active onboarding docs, repository identity, doc index,
  testing docs, and version/license/release signals are internally coherent and
  match the actual tracked files and workflow — with **zero package-behavior,
  typography, or rendered-output changes**.

## Constraints

- Repo constraints:
  - Cross-lane rules (roadmap:256-269): every material fix documents its
    rationale; update `CHANGELOG.md` and relevant README sections after
    material changes; keep commits path-scoped to this lane; preserve unrelated
    dirty state; do not use Overleaf language stronger than the evidence.
  - Lane 3 non-goals (roadmap:174-180): **no package behavior changes, no
    typography changes**, no Overleaf verification claims without exact Overleaf
    log evidence, no CTAN/release promises (Lane 2 left the `.dtx`/`.ins`
    packaging path **non-authoritative** — see
    `tmp/ai-plans/lane-2-compatibility-and-package-api.md` lines 81/119/261).
  - `main.tex` and the rendered `main.pdf` are **out of scope**. The demo paper
    is sample content; its academic subject (the East Asian Miracle) is not a
    repository-identity defect and must not be edited in this lane. `main.pdf`
    must remain content-stable.
- User constraints (decision gates resolved 2026-07-03 via grill-me):
  - **Overleaf** → *Remove the claims entirely* from public docs (not merely
    "pending verification").
  - **Identity** → *Rename active user-facing files* to "Lane LaTeX Template";
    *leave historical audit/optimization docs untouched* with their original
    wording.
  - **Release signals** → *Reconcile version numbers to one honest source and
    add a root `LICENSE`; defer CTAN/release* (no release promises this lane).
  - **Docs index** → *Curated manual rewrite* of `docs/README.md` matching the
    actual tracked files (not mechanical regeneration).

## Worktree Context

- Mode: branch in checkout (default)
- Path: /Users/nathanlane/code/lane_latex_template
- Branch: codex/lane-3-repo-professionalism-and-docs
- Detached: no
- Plan path: tmp/ai-plans/lane-3-repo-professionalism-and-docs.md
- External output collision risk: none
- Waiver: n/a

## Files In Scope

Active edits (documentation / metadata only):

- `README.md` — remove Overleaf claims; reconcile version/release signals.
- `INSTALL.md` — replace `paper/paperstyle` load examples with `lltpaperstyle`;
  neutralize the generic Overleaf fallback line so it makes no support claim.
- `TROUBLESHOOTING.md` — replace `paper/paperstyle` examples; delete the
  "Overleaf-Specific Issues" section (this also removes the dead
  `preamble-overleaf.tex` / `paperstyle-overleaf` / `paperstyle-minimal`
  references).
- `AGENTS.md` — correct the `pytest -q` "layout hashes" claim.
- `Makefile` — rename the two identity strings in the header comment and the
  help `@echo` (comment/echo text only; no recipe or target logic).
- `SECURITY.md` — make supported versions explicit.
- `LICENSE` — **net-new** root license file (full LPPL v1.3c text, sourced from
  `license/LICENSE.txt`) for GitHub license detection.
- `docs/README.md` — curated manual rewrite matching actual tracked docs.
- `docs/guides/LATEX_STYLE_STANDARDS.md` — rename active identity strings.
- `docs/guides/BIBLIOGRAPHY_GUIDE.md` — rename the identity framing sentence
  only (keep the legitimate "The East Asian Miracle" *citation example*).
- `docs/technical/TESTING.md` — fix `make format-python` → `make format`;
  reconcile the pytest/testing description; host the canonical testing table.
- `docs/PACKAGE_ROADMAP.md` — rename the `EastAsia_Paper` title.
- `docs/style/CHANGELOG.md` — replace placeholder GitHub release links.
- `paper/STYLE_GUIDE.md` — reword the `\articletitle{...}` demo example to a
  neutral placeholder (doc example only; not compiled into `main.pdf`).
- `paper/CUSTOM_COMMANDS.md` — reword the `\articletitle{...}` demo example.
- `docs/TROUBLESHOOTING.md` — archive to `docs/archive/TROUBLESHOOTING-legacy.md`
  (resolves the duplicate/divergent troubleshooting surface; root
  `TROUBLESHOOTING.md` becomes canonical).
- `CHANGELOG.md` — record the Lane 3 doc changes (cross-lane rule).

Inspect-only (verification, not edited):

- `paper/lltpaperstyle.sty` (version `v1.7` reference), `license/LICENSE.txt`
  (LPPL source text), `main.tex`, `main.pdf`, `tests/`.

Explicitly **out of scope / left untouched** (historical audit & optimization
records, per the "keep history" decision):

- `docs/technical/COMPLEXITY_AUDIT_REPORT.md`,
  `docs/LOCAL_FORK_TEMPLATE_AUDIT_2026-05-27.md`,
  `docs/typography/BLOCKQUOTE_LIST_OPTIMIZATION.md`,
  `docs/development/grid/GRID-IMPROVEMENTS-SUMMARY.md`, and the other
  `docs/*_AUDIT_REPORT.md` / `docs/**/*OPTIMIZATION*.md` historical notes.

## Footprint Budget

- Net-new files (target 0): **1** — root `LICENSE`.
- Net-new abstractions (scripts/macros/targets) (target 0): **0**.
- Plan weight justified? yes
- Justification: the root `LICENSE` is an explicit user-approved addition for
  GitHub license detection and downstream reuse (deep-review finding P2). One
  file is archived via `git mv` (a rename, not a net-new file).

## Assumptions

- The two version numbers are *different namespaces*: `v0.1.0-beta` is the
  template-repository release; `\ProvidesPackage{lltpaperstyle}[... v1.7 ...]`
  is the internal style-package version. Reconciliation = make them
  non-contradictory and single-sourced/explained, not force them equal.
- `license/LICENSE.txt` is LPPL v1.3c and is a valid source for the root
  `LICENSE` text; GitHub detects a root file named `LICENSE`.
- Editing markdown/comment text in the listed docs does not alter `main.pdf`
  because none of these files are `\input` into `main.tex`.
- Root `TROUBLESHOOTING.md` is the canonical location; `docs/TROUBLESHOOTING.md`
  is the divergent duplicate to archive.

## Implementation Plan

Execute in this order; keep each change minimal and rationale-commented where a
material claim changes.

1. **Broken load paths (Group A).** In `INSTALL.md` (`:244`, `:268`, `:331`) and
   `TROUBLESHOOTING.md` (`:37`, `:48`, `:89`, `:317`), replace
   `\usepackage{paper/paperstyle}` / `[compat]{paper/paperstyle}` examples with
   the current `\usepackage{lltpaperstyle}` (and correct option names). Leave
   `README.md:678` intact — it is a documented rename migration note.

2. **Remove Overleaf claims (Group B).** In `README.md` remove/neutralize the
   Overleaf support statements at `:23`, `:98`, `:170`, `:543`, and the Overleaf
   evidence-caveat block at `:73-76`. In `TROUBLESHOOTING.md` delete the
   "Overleaf-Specific Issues" section (TOC entry `:13`, mention `:35`, body
   `:323-384`) — this also removes the dead `preamble-overleaf.tex`,
   `paperstyle-overleaf`, `paperstyle-minimal` references. In `INSTALL.md:347`
   reword the generic "consider Overleaf" fallback so it asserts no verified
   compatibility (or drop it).

3. **Repo identity, active files only (Group C).** Rename "East Asian Miracle
   Paper" / "EastAsia_Paper" identity strings to "Lane LaTeX Template" in:
   `Makefile:1` and `Makefile:280` (comment + `@echo` text only),
   `docs/guides/LATEX_STYLE_STANDARDS.md:1` and `:230`,
   `docs/guides/BIBLIOGRAPHY_GUIDE.md:3` (framing sentence; keep the `:62`
   citation example), `docs/technical/TESTING.md:3`, `docs/PACKAGE_ROADMAP.md:1`,
   and the `\articletitle{...}` demo examples in `paper/STYLE_GUIDE.md:86` and
   `paper/CUSTOM_COMMANDS.md:78`. Do **not** touch historical audit/optimization
   docs or `main.tex`.

4. **Curated docs index rewrite (Group D).** Rewrite `docs/README.md` to match
   the real tree (`git ls-files docs/`): remove the nonexistent `audits/`
   section, the `plans/` entries and `FINAL_COMPILATION_STATUS.md` links
   (`:53`, `:69`), and the stale `OVERLEAF_WARNING_SUPPRESSION_GUIDE.md` entry
   (`:22`). Group surviving docs as active / internal / archived across the real
   directories: `ai-workflow, archive, development, guides, style, superpowers,
   technical, tmp, typography`.

5. **Testing docs accuracy (Group E).** Fix `AGENTS.md:19` to describe the real
   gate (compiles a fixture subset; PDF-text assertions; no layout-hash diff).
   In `docs/technical/TESTING.md` change `make format-python` → `make format`
   (`:423`, `:697`) and add one canonical testing table covering `make lint`,
   `make build`, `pytest -q`, `tests/run-tests.sh`, and generated-artifact
   paths.

6. **Version / release / license (Groups F, G).** In `README.md` make the
   version signals non-contradictory and single-sourced (keep `v0.1.0-beta` as
   the repository release; add a one-line note that bundled `lltpaperstyle.sty`
   carries its own package version, currently v1.7; correct the stale release
   date if needed). Replace the placeholder GitHub release links in
   `docs/style/CHANGELOG.md:43`. Add a root `LICENSE` (full LPPL v1.3c from
   `license/LICENSE.txt`). Make `SECURITY.md:32` supported-versions explicit.
   Add **no** CTAN/release promises.

7. **Duplicate troubleshooting (Group H).** `git mv docs/TROUBLESHOOTING.md
   docs/archive/TROUBLESHOOTING-legacy.md` and add a one-line archived-note
   header; keep the (now Overleaf-cleaned, path-corrected) root
   `TROUBLESHOOTING.md` as canonical. Check for and fix inbound links to the
   moved file.

8. **Changelog.** Record the Lane 3 documentation changes in `CHANGELOG.md`.

## Risks

- **Over-deletion of useful content.** Removing the Overleaf section could drop
  genuinely useful non-Overleaf tips. Mitigation: only the Overleaf-specific
  subsection is removed; general tips stay in root `TROUBLESHOOTING.md`.
- **Broken inbound links** after archiving `docs/TROUBLESHOOTING.md` or rewriting
  `docs/README.md`. Mitigation: `rg` for referrers before/after; the
  verification step greps for dangling links.
- **Version confusion.** Conflating repo-release vs package version. Mitigation:
  the reconciliation explains the two namespaces rather than forcing equality.
- **Accidental visual/behavior change.** Mitigation: `main.tex` excluded;
  rebuild `main.pdf` and confirm it is content-stable (page count + text
  unchanged); `make lint` and `pytest -q` stay green.
- **Makefile fragility.** Only comment/`@echo` text changes — no recipe lines,
  preserving tab structure.

## Test Plan

### Planned Verification

Run from the repo root after implementation:

```bash
make lint
latexmk -pdf -interaction=nonstopmode main.tex
pytest -q
tests/run-tests.sh
# Identity/paths/Overleaf claims fully cleared from ACTIVE files
# (historical audit/optimization docs are expected to still match and are out of scope):
rg -n "paper/paperstyle|paperstyle-overleaf|preamble-overleaf|Overleaf.*[Ww]orks automatically|East Asian Miracle Paper|EastAsia_Paper" \
   README.md INSTALL.md TROUBLESHOOTING.md AGENTS.md Makefile \
   docs/README.md docs/guides docs/technical/TESTING.md docs/PACKAGE_ROADMAP.md \
   paper/STYLE_GUIDE.md paper/CUSTOM_COMMANDS.md
# Testing-doc + stale-index claims cleared:
rg -n "format-python|layout hash|FINAL_COMPILATION_STATUS|docs/audits|docs/plans|OVERLEAF_WARNING_SUPPRESSION" \
   AGENTS.md README.md docs Makefile
# docs/README.md points only at existing files (no dangling links):
#   manual/scripted check that each linked path resolves.
# Root license detected:
ls LICENSE
# main.pdf content-stable (page count unchanged, spot-check text):
pdfinfo main.pdf | rg "Pages"
git status --short
```

Expected: `make lint` exit 0; `pytest -q` all pass; `tests/run-tests.sh` all
pass; the active-file greps return no matches (historical docs untouched);
`docs/README.md` links all resolve; root `LICENSE` present; `main.pdf` page
count matches pre-change.

### Execution Results

- Pending.

### Verifier Validation

- Method: pending
- Evidence: pending

## Reviewer Findings

- None yet.

## Resolutions

- None yet.

## Plan Deltas

- None yet.
