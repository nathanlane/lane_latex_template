---
topic: lane-1-build-hygiene-test-surface
created: 2026-07-01
status: Draft
---

# Lane 1 Build Hygiene Test Surface

## Task

Create a trustworthy local verification surface for the Lane LaTeX Template
before package API, documentation, or typography fixes proceed. This lane should
make the build warning policy explicit, remove or classify current warning
noise, and ensure required test commands do not leave unintended tracked-file
churn.

## Constraints

- Preserve visual design: do not change margins, fonts, colors, spacing,
  numbering schemes, or figure/float placement defaults in this lane.
- Treat `docs/superpowers/plans/2026-07-01-deep-review-roadmap.md` as the
  master roadmap and `docs/technical/DEEP_REVIEW_FINDINGS_2026-07-01.md` as the
  findings source.
- Keep this lane limited to build hygiene, generated-artifact behavior, warning
  policy, and metadata/content fixes needed to make the local gates meaningful.
- Every material LaTeX code fix must include a `%% FIX:` comment with a concise
  rationale.
- Update `CHANGELOG.md` and relevant README/testing docs after any material
  change.
- Preserve unrelated dirty state. The generated log files currently dirty in
  `tests/compilation/logs/` are evidence from the previous `pytest -q` run and
  must not be silently reverted inside this plan.
- Do not make any Overleaf verification claim unless a current Overleaf compile
  log/build identifier is supplied.
- Do not implement Lane 2 package compatibility fixes or Lane 4 typography
  behavior fixes here.

## Worktree Context

- Mode: branch in checkout.
- Repository path: `/Users/nathanlane/code/lane_latex_template`.
- Branch: `codex/lane-1-build-hygiene-plan`.
- Baseline commit for this plan: `e0512f0` (`docs(plan): add deep review
  roadmap`).
- Upstream: branch was created from `main`; no branch upstream is configured yet.
- Current dirty files to preserve outside the plan commit:
  - `tests/compilation/logs/biblatex-manual-contract_pass1.log`
  - `tests/compilation/logs/biblatex-manual-contract_pass2.log`
  - `tests/compilation/logs/compatibility-backports.log`
- External-output collision risk: low. This lane may run LaTeX/PDF tooling and
  shell tests that write repo-local generated artifacts. No Dropbox, Overleaf,
  network, or external-cache writes are planned.

## Files In Scope

- `references.bib`
  - Candidate metadata fixes for invalid ISBN warnings.
- `main.tex`
  - Candidate content-only changes for warning-clean build output, if they do
    not change the template design contract.
- `paper/lltpaperstyle.sty`
  - Read-only by default in this lane; only touch if a warning-policy fix is
    strictly non-visual and clearly belongs to build hygiene.
- `paper/modules/lltmicrotype.sty`
  - Read-only by default in this lane; classify `Unknown slot number` records
    here, but defer visual/optical changes to Lane 4 unless a no-output-change
    fix is proven.
- `tests/run-tests.sh`
  - Candidate fix for generated log output location and tracked-log churn.
- `tests/test-bibliography.sh`
  - Candidate fix for generated bibliography log output location and tracked-log
    churn.
- `.gitignore`
  - Candidate update if generated logs should become transient artifacts.
- `tests/check-spacing-integrity.sh`
  - Candidate policy/documentation update if the script remains advisory or is
    rewritten as a real gate.
- `tests/README.md`
  - Document the actual regression/test artifact contract.
- `docs/technical/TESTING.md`
  - Document warning policy, generated-artifact behavior, and spacing-integrity
    status if this remains an active technical doc.
- `README.md`
  - Align the public verification commands and warning/test expectations if they
    are currently user-facing.
- `CHANGELOG.md`
  - Record material workflow/test/build hygiene changes.
- Generated files that may be read but should not be committed unless the lane
  explicitly decides to keep golden logs:
  - `main.log`
  - `main.blg`
  - `main.pdf`
  - `tests/compilation/logs/*.log`

## Footprint Budget

- Net-new durable files: 0.
  - This lane should prefer modifying existing build/test/docs files. If a new
    helper is needed, add a Plan Delta before implementation.
- Net-new abstractions: 0.
  - Avoid introducing new build frameworks or test abstractions; make the
    existing commands trustworthy.
- Expected changed-file budget: 4-8 tracked files.
  - Likely files are `references.bib`, shell test harnesses, `.gitignore`, test
    docs, README, and changelog. A narrower diff is preferred.

## Assumptions

- `make lint`, `latexmk -pdf -interaction=nonstopmode main.tex`, and
  `pytest -q` currently exit 0.
- `latexmk -pdf -interaction=nonstopmode -g main.tex` should be used in this
  lane to force a fresh local build when checking warning state.
- The current invalid ISBN warnings in `main.blg` are metadata issues, not
  typography or package API issues.
- `tests/check-spacing-integrity.sh main.pdf` currently fails density/page
  efficiency heuristics; this may indicate either a real spacing issue or a
  heuristic that is inappropriate for the demo/template PDF.
- The current `microtype` unknown-slot records are build-surface noise; whether
  they require a code fix or accepted-warning documentation must be decided
  before implementation.
- If fixing an overfull/underfull box requires changing demo prose or verbatim
  examples, that is in scope only if it does not change template design defaults.
- The three dirty tracked log files are not user-authored source edits.

## Implementation Plan

1. Reproduce the baseline from a clean staged index while preserving the current
   generated-log dirt:
   - `make lint`
   - `latexmk -pdf -interaction=nonstopmode -g main.tex`
   - `pytest -q`
   - `tests/check-spacing-integrity.sh main.pdf`
   - `rg -n "Warning|Error|Undefined|Overfull|Underfull|WARN -" main.log main.blg`
   - `rg -c "Unknown slot number" main.log`
   - `git status --short`
2. Decide and record the warning policy for Lane 1:
   - zero warnings required,
   - accepted warnings documented with exact regexes and rationale, or
   - split policy where `main.blg` and package warnings must be clean but
     selected content-level box warnings may be accepted.
3. Fix invalid Biber ISBN warnings in `references.bib` if authoritative metadata
   confirms the current ISBN values are malformed or wrong.
4. Triage the `\showhyphens`, overfull, underfull, and overfull-vbox records:
   - fix content/demo examples only when there is no design change,
   - otherwise document accepted warnings with line references and rationale.
5. Triage `microtype` unknown-slot records:
   - identify whether they are caused by invalid protrusion entries,
   - defer optical-margin changes to Lane 4 unless a no-output-change fix is
     proven,
   - document any accepted warning state explicitly.
6. Fix test-log churn:
   - determine whether committed logs are intended golden artifacts,
   - if not, redirect harness log output to a temp/generated directory and update
     `.gitignore`,
   - if yes, make regeneration deterministic and document how maintainers should
     update the golden logs.
7. Decide the role of `tests/check-spacing-integrity.sh main.pdf`:
   - hard gate,
   - advisory diagnostic,
   - or obsolete script requiring rewrite before use.
   Update docs and script messaging to match the decision.
8. Update `README.md`, `tests/README.md`, `docs/technical/TESTING.md`, and
   `CHANGELOG.md` only as needed to reflect the final local verification
   contract.
9. Run the full Lane 1 verification suite and inspect `git status --short`.
10. Leave a short implementation note in this plan's execution results during
    the implementation step, including any warnings that remain accepted and any
    deferred Lane 2 or Lane 4 follow-ups.

## Risks

- A strict zero-warning policy may force typography or demo-content changes that
  exceed Lane 1. If so, classify those warnings and route the visual behavior to
  Lane 4 instead of silently changing output.
- The spacing-integrity script may be measuring document density rather than a
  real spacing bug. Treat failure as evidence to classify, not automatic proof
  of a layout defect.
- Redirecting test logs may require updating tests that currently expect
  committed log paths. Keep this local to the shell harnesses and pytest tests.
- Fixing ISBN metadata should use authoritative bibliographic data. Do not guess
  ISBNs.
- Generated LaTeX artifacts can obscure source diffs. Keep commits path-limited
  and do not stage generated logs unless the plan explicitly keeps golden logs.
- `microtype` unknown-slot fixes may affect optical margin behavior. Defer to
  Lane 4 unless a no-output-change proof is available.

## Test Plan

### Planned Verification

Run from `/Users/nathanlane/code/lane_latex_template`:

```bash
make lint
latexmk -pdf -interaction=nonstopmode main.tex
latexmk -pdf -interaction=nonstopmode -g main.tex
pytest -q
tests/check-spacing-integrity.sh main.pdf
rg -n "Warning|Error|Undefined|Overfull|Underfull|WARN -" main.log main.blg
rg -c "Unknown slot number" main.log
git status --short
```

Expected final signals:

- Required lint/build/test commands exit 0.
- Warning policy is explicit and documented.
- `pytest -q` does not leave unintended tracked-file churn, or any intended
  golden-log churn is documented and deterministic.
- `tests/check-spacing-integrity.sh main.pdf` has a documented role and expected
  pass/fail behavior.
- Any remaining warning output is either eliminated or documented as accepted
  with exact evidence.

### Execution Results

- Pending.

### Verifier Validation

- Method: pending.
- Evidence: pending.
