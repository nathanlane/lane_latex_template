---
topic: lane-3-repo-professionalism-and-docs
created: 2026-07-03
status: Reviewed
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
    repository-identity defect and must not be edited in this lane. No in-scope
    file is a TeX/package input `\input` by `main.tex`, so `main.pdf` cannot
    change; the plan verifies this **structurally** (the changed set contains no
    `.tex`/`.sty`/`.cls`/`.bib`) plus a successful local rebuild — it does not
    diff the untracked/gitignored PDF (see F3 resolution).
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
- `AGENTS.md` — correct the `pytest -q` "layout hashes" claim (`:19`); remove the
  active Overleaf support/DoD claims (`:4`, `:10`, `:36-37`, `:85`) per the
  Overleaf gate (F1).
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
   drop the Overleaf-named fallback (remove it, or genericize to "an online
   LaTeX service" with **no** "Overleaf" mention) so no active doc names Overleaf.
   In `AGENTS.md`, strike the Overleaf clauses (F1): the Mission line (`:4`),
   "both platforms" (`:10`), the DoD Overleaf-render and Overleaf-build-number
   lines (`:36-37`), and the Quick-Start "Recompile on Overleaf" clause (`:85`).

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
- **Accidental visual/behavior change.** Mitigation: no in-scope file is a TeX
  input; verification asserts the changed set contains no `.tex`/`.sty`/`.cls`/
  `.bib` (F3), the `latexmk` rebuild stays green, and `make lint` / `pytest -q`
  pass. (`main.pdf` is gitignored/untracked, so git cannot diff it — hence the
  structural input check rather than a PDF diff.)
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
# Identity / broken load paths cleared from ACTIVE files (historical audit &
# optimization docs are out of scope and expected to still match):
rg -n "paper/paperstyle|paperstyle-overleaf|preamble-overleaf|East Asian Miracle Paper|EastAsia_Paper" \
   INSTALL.md TROUBLESHOOTING.md AGENTS.md Makefile \
   docs/README.md docs/guides docs/technical/TESTING.md docs/PACKAGE_ROADMAP.md \
   paper/STYLE_GUIDE.md paper/CUSTOM_COMMANDS.md
# No Overleaf references remain in active public docs (F1 gate):
rg -n -i "overleaf" README.md INSTALL.md TROUBLESHOOTING.md AGENTS.md \
   docs/README.md docs/technical/TESTING.md || echo "OK: active docs are Overleaf-free"
# Testing-doc + stale-index claims cleared — ACTIVE files ONLY (F2). The
# historical evidence docs (docs/technical/DEEP_REVIEW_FINDINGS_2026-07-01.md and
# docs/superpowers/plans/2026-07-01-deep-review-roadmap.md) intentionally retain
# these strings and are out of scope, so they are NOT scanned:
rg -n "format-python|layout hash|FINAL_COMPILATION_STATUS|docs/audits|docs/plans|OVERLEAF_WARNING_SUPPRESSION" \
   AGENTS.md README.md docs/README.md docs/technical/TESTING.md Makefile
# docs/README.md points only at existing files (no dangling links):
#   scripted check that each linked path resolves.
# Root license detected:
ls LICENSE
# No TeX/package inputs touched, so main.pdf cannot change (F3). A printed path
# below means an unexpected TeX input changed; no match prints OK:
git diff --name-only main -- . | rg '\.(tex|sty|cls|bib)$' && echo "UNEXPECTED: TeX input changed" || echo "OK: no TeX/package inputs changed"
# (the latexmk run above already confirms the local rebuild still succeeds.)
git status --short
```

Expected: `make lint` exit 0; `pytest -q` all pass; `tests/run-tests.sh` all
pass; the active-file greps return no matches and the Overleaf check prints
`OK` (historical/evidence docs untouched); `docs/README.md` links all resolve;
root `LICENSE` present; the changed set contains no `.tex`/`.sty`/`.cls`/`.bib`
(so `main.pdf` cannot change) and the `latexmk` rebuild succeeds.

### Execution Results

Implemented in commit `fa15e86` (`docs: professionalize lane template
documentation`).

Commands run from the repo root:

```bash
make lint
# exit 0

latexmk -pdf -interaction=nonstopmode main.tex
# exit 0; main.pdf was already up to date

pytest -q
# exit 0; 18 passed in 68.08s

tests/run-tests.sh
# exit 0; Passed: 115, Failed: 0; all compatibility probes passed

git diff --check
# exit 0

rg -n "paper/paperstyle|paperstyle-overleaf|preamble-overleaf|East Asian Miracle Paper|EastAsia_Paper" \
   INSTALL.md TROUBLESHOOTING.md AGENTS.md Makefile \
   docs/README.md docs/guides docs/technical/TESTING.md docs/PACKAGE_ROADMAP.md \
   paper/STYLE_GUIDE.md paper/CUSTOM_COMMANDS.md
# exit 1; no matches

rg -n -i "overleaf" README.md INSTALL.md TROUBLESHOOTING.md AGENTS.md \
   docs/README.md docs/technical/TESTING.md
# exit 1; no matches

rg -n "format-python|layout hash|FINAL_COMPILATION_STATUS|docs/audits|docs/plans|OVERLEAF_WARNING_SUPPRESSION" \
   AGENTS.md README.md docs/README.md docs/technical/TESTING.md Makefile
# exit 1; no matches

python3 -c '...docs/README.md link resolver...'
# exit 0; OK

ls LICENSE
# exit 0; LICENSE

git diff --name-only main -- . | rg '\.(tex|sty|cls|bib)$'
# exit 1; no TeX/package inputs changed
```

Before this final plan-only status commit, `git status --porcelain=v1` showed
only `tmp/ai-plans/lane-3-repo-professionalism-and-docs.md` modified.

### Verifier Validation

- Method: reran-planned-verification
- Evidence: Independently re-ran the planned set — `make lint`=0, `pytest -q` 18 passed, `tests/run-tests.sh` 115/0; active-doc identity/Overleaf/`format-python`/layout-hash greps all clean; every `llt*` package named in edited docs (lltpaperstyle, lltpaperstyleminimal, lltdimensions, lltmicrotype, llthochuli, lltfontfallbacks) resolves to a real `.sty`; `docs/README.md` all 23 links resolve; no `.tex`/`.sty`/`.cls`/`.bib` in the changed set (so `main.pdf` cannot move). Both Plan-Delta deviations independently confirmed justified and non-blocking; no scope-gate/hook exists in this repo to trip on the unlisted `licenses/` path.

## Reviewer Findings

### 2026-07-03

- [routing hint: accepted-current] `AGENTS.md` is in scope, but the plan only
  changes its `pytest -q` description while leaving active Overleaf support and
  Definition-of-Done claims at `AGENTS.md:4`, `AGENTS.md:36-37`, and
  `AGENTS.md:85`. That conflicts with the resolved user gate to remove Overleaf
  claims from public/active docs unless there is exact log evidence. Either add
  those `AGENTS.md` lines to the Lane 3 scope and verification, or explicitly
  waive `AGENTS.md` as non-public agent policy and explain why it may keep the
  stronger Overleaf contract.
- [routing hint: accepted-current] The second planned cleanup grep scans all of
  `docs`, but live historical/review evidence under
  `docs/technical/DEEP_REVIEW_FINDINGS_2026-07-01.md` and
  `docs/superpowers/plans/2026-07-01-deep-review-roadmap.md` intentionally
  contains `layout hash`, `format-python`, `FINAL_COMPILATION_STATUS`,
  `docs/audits`, and/or `docs/plans`. Since the plan explicitly leaves
  historical audit/roadmap material untouched, that grep will fail a correct
  implementation. Narrow it to active docs or exclude the historical evidence
  files.
- [routing hint: accepted-current] The plan says `main.pdf` must remain
  content-stable, but `main.pdf` is ignored and untracked in this checkout, so
  `git status --short` cannot detect PDF churn. The planned `pdfinfo` page count
  plus spot-check text is weaker than the zero rendered-output claim. Either
  record and compare a pre/post text or raster artifact for `main.pdf`, or narrow
  the verification claim to "no TeX/package inputs changed; local rebuild still
  succeeds."

### 2026-07-04 (review-diff-vs-plan verifier pass)

No material findings — the implementation matches the frozen plan; status
advanced to `Reviewed`. Independent verification plus per-file diff review
confirmed:

- All eight finding groups (A–H) implemented. Every active-doc identity,
  Overleaf, broken-path, and testing-claim target is cleared, while the
  historical audit/optimization docs are left untouched and the
  `The East Asian Miracle` *citation example* (`BIBLIOGRAPHY_GUIDE.md:62`) is
  preserved per plan intent.
- No new broken paths introduced: every `llt*` package named in the edited docs
  resolves to a real `.sty` file.
- Constraints honored: no `.tex`/`.sty`/`.cls`/`.bib` changed, so `main.pdf`
  cannot move; `make lint` / `pytest -q` / `tests/run-tests.sh` all green.

Two deviations were found and independently judged **non-blocking / accepted**
(both already recorded under Plan Deltas 2026-07-04):

- `license/ → licenses/` directory rename — necessary to avoid a root-`LICENSE`
  case-fold collision on a case-insensitive filesystem; documented in
  `CHANGELOG.md`. The only referrer to the old path is a frozen, out-of-scope
  historical evidence doc (`DEEP_REVIEW_FINDINGS_2026-07-01.md`), so nothing
  functional dangles, and no scope-gate/hook exists in this repo to enforce the
  Files-In-Scope allowlist.
- Full LPPL text sourced from the TeX Live canonical copy rather than the short
  `license/LICENSE.txt` notice — same root-`LICENSE` outcome with better
  provenance.

## Resolutions

### 2026-07-04

All three challenge findings verified against the live tree and routed
`accepted-current` (folded into this plan pre-implementation; no
re-implementation loop needed since nothing is implemented yet).

- **F1 (AGENTS.md carries active Overleaf claims) → accepted-current.**
  `AGENTS.md` is a tracked, publicly visible policy doc, so the resolved
  "remove Overleaf claims entirely from active/public docs" gate applies to it.
  Confirmed the claims at `AGENTS.md:4` (Mission), `:10` ("both platforms"),
  `:36-37` (DoD Overleaf render + Overleaf build numbers), and `:85`
  (Quick-Start "Recompile on Overleaf"). **Change:** expanded Files In Scope and
  Implementation step 2 to strike those clauses; added an active-docs
  Overleaf-free grep to Planned Verification. Also tightened `INSTALL.md:347`
  to drop the Overleaf *name* (not just soften the claim) so the check is crisp.

- **F2 (cleanup grep over-scans historical docs) → accepted-current.** Verified
  9 intentional matches for the cleanup strings in the out-of-scope evidence
  files (`docs/technical/DEEP_REVIEW_FINDINGS_2026-07-01.md`,
  `docs/superpowers/plans/2026-07-01-deep-review-roadmap.md`), so the original
  broad `docs` scan would false-fail a correct implementation. **Change:**
  narrowed that grep to the active files Lane 3 actually edits
  (`AGENTS.md README.md docs/README.md docs/technical/TESTING.md Makefile`) and
  documented why the historical evidence docs are excluded.

- **F3 (main.pdf stability claim unverifiable) → accepted-current.** Confirmed
  `main.pdf` is gitignored and untracked, so `git status` cannot detect PDF
  churn and a `pdfinfo` page count is a weak proxy for "zero rendered-output
  change." Since **no in-scope file is a TeX/package input**, narrowed the claim
  to "no `.tex`/`.sty`/`.cls`/`.bib` changed; local rebuild still succeeds,"
  verified structurally via `git diff --name-only main` plus the existing
  `latexmk` run. **Change:** updated the Constraints wording, the
  Accidental-visual-change risk mitigation, and the Test Plan.

## Plan Deltas

### 2026-07-04

- The frozen plan said to copy full LPPL text from `license/LICENSE.txt`, but
  that file is only a short LPPL notice. Implemented the same root `LICENSE`
  outcome using the canonical local TeX Live copy at
  `/usr/local/texlive/2025/texmf-dist/doc/latex/base/lppl.txt`. Because the
  checkout is on a case-insensitive filesystem, the existing `license/`
  directory collided with a root `LICENSE` file, so the short notice moved from
  `license/LICENSE.txt` to `licenses/LICENSE.txt`.
- The frozen verification grep for broken load paths included `README.md`, while
  Implementation step 1 explicitly preserved the README migration note
  containing the legacy `paper/paperstyle` token. Planned verification should
  exclude `README.md` from that specific broken-path grep and rely on the
  migration-note exception documented in step 1.
