---
topic: lane-1-build-hygiene-test-surface
created: 2026-07-01
status: Implemented
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
- Preserve unrelated user-authored dirty state. The currently dirty
  `tests/compilation/logs/` files are generated artifacts and are part of the
  Lane 1 problem surface; implementation must snapshot them before changing
  anything, then either make them transient or document an explicit retained
  contract.
- Treat raw TeX logs as transient unless implementation proves a real golden-log
  consumer exists. Do not create a new golden-log contract in this lane.
- Treat `tests/check-spacing-integrity.sh main.pdf` as an advisory diagnostic at
  plan start. It must not be used as a hard green gate unless Lane 1 rewrites or
  reclassifies it with documented pass/fail semantics.
- Do not make any Overleaf verification claim unless a current Overleaf compile
  log/build identifier is supplied.
- Do not implement Lane 2 package compatibility fixes or Lane 4 typography
  behavior fixes here.

## Worktree Context

- Mode: branch in checkout.
- Repository path: `/Users/nathanlane/code/lane_latex_template`.
- Branch: `codex/lane-1-build-hygiene-plan`.
- Draft plan birth commit: `0bc9b37` (`docs(plan): open
  lane-1-build-hygiene-test-surface (Draft)`).
- Upstream: branch was created from `main`; local branch has no upstream
  configured. A remote branch name exists but was not populated by local `git
  push` because local GitHub credentials are invalid.
- Current generated-artifact dirt to snapshot before implementation:
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
- `tests/test_regression_harness.py`
  - Contract owner for the pytest calls that trigger the shell harnesses; include
    at least read-only, and edit if output paths or assertions must change.
- `.gitignore`
  - Candidate update to remove the current `tests/compilation/logs/*.log`
    re-inclusion if generated logs become transient artifacts.
- `pytest.ini`
  - Read-only by default; document the `-p no:capture` environment workaround if
    local green status does not imply CI-equivalent coverage.
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
- Generated files that may be read and may be removed from tracking if Lane 1
  confirms they are transient:
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
- Expected changed-file budget: 4-9 tracked files plus possible deletion of
  obsolete tracked logs.
  - Likely files are `references.bib`, shell test harnesses, `.gitignore`, test
    docs, README, and changelog. A narrower diff is preferred.

## Assumptions

- Do not assume baseline commands exit 0; implementation step 1 must verify and
  record the current command outcomes before making changes.
- `latexmk -pdf -interaction=nonstopmode -g main.tex` should be used in this
  lane to force a fresh local build when checking warning state.
- The current invalid ISBN warnings in `main.blg` are metadata issues, not
  typography or package API issues.
- `tests/check-spacing-integrity.sh main.pdf` currently fails density/page
  efficiency heuristics; until reclassified, it is diagnostic evidence rather
  than a hard pass/fail gate.
- The current `microtype` unknown-slot records are build-surface noise; whether
  they require a code fix or accepted-warning documentation must be decided
  before implementation.
- If fixing an overfull/underfull box requires changing demo prose or verbatim
  examples, that is in scope only if it does not change template design defaults.
- The three dirty tracked log files are generated artifacts. Current pytest tests
  assert shell return codes and PDF text, not log-file contents.

## Implementation Plan

1. Reproduce the baseline from a clean staged index and capture the pre-change
   porcelain snapshot:
   - `git status --porcelain=v1`
   - `make lint`
   - `latexmk -pdf -interaction=nonstopmode -g main.tex`
   - `pytest -q`
   - `tests/check-spacing-integrity.sh main.pdf || true`
   - `rg -n "Warning|Error|Undefined|Overfull|Underfull|WARN -" main.log main.blg`
   - `rg -c "Unknown slot number" main.log`
   - `git status --short`
2. Apply the Lane 1 warning policy:
   - remove machine-actionable metadata/build warnings when the fix is
     non-visual and authoritative,
   - keep required commands exit-0,
   - document accepted content-level box warnings with exact regexes and
     rationale when fixing them would change typography or demo design,
   - defer visual-output or optical-margin fixes to Lane 4.
3. Fix invalid Biber ISBN warnings in `references.bib` if authoritative metadata
   confirms the current ISBN values are malformed or wrong. Offline-safe options
   are ISBN-13 check-digit validation to prove malformation, or removing the
   `isbn` field rather than asserting an unverified replacement value.
4. Triage the `\showhyphens`, overfull, underfull, and overfull-vbox records:
   - fix content/demo examples only when there is no design change,
   - otherwise document accepted warnings with line references and rationale.
5. Triage `microtype` unknown-slot records:
   - identify whether they are caused by invalid protrusion entries,
   - defer optical-margin changes to Lane 4 unless a no-output-change fix is
     proven,
   - document any accepted warning state explicitly.
6. Fix test-log churn by making raw harness logs transient:
   - confirm no pytest or shell assertion reads
     `tests/compilation/logs/*.log` as golden data,
   - remove the `.gitignore` re-include for `tests/compilation/logs/*.log`,
   - redirect harness logs to ignored output or leave them in the same path only
     after it is ignored,
   - remove obsolete tracked log copies with `git rm --cached` or `git rm` as
     appropriate,
   - update `tests/test_regression_harness.py` if path or assertion behavior
     changes.
7. Decide the role of `tests/check-spacing-integrity.sh main.pdf`:
   - default for this plan is advisory diagnostic,
   - promote to hard gate only after the heuristic is rewritten or calibrated for
     the template PDF,
   - otherwise document it as non-gating evidence and keep final verification
     explicit about the expected non-zero status.
   Update docs and script messaging to match the decision.
8. Update `README.md`, `tests/README.md`, `docs/technical/TESTING.md`, and
   `CHANGELOG.md` only as needed to reflect the final local verification
   contract.
9. Run the full Lane 1 verification suite and compare final
   `git status --porcelain=v1` against the pre-change snapshot. Success means no
   new unexpected generated-artifact churn beyond planned source/doc changes and
   any deliberate tracked-log removals.
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
- Removing tracked logs changes the evidence surface for Lane 2 fixtures
  (`biblatex-manual-contract*` and `compatibility-backports`). Record this as a
  Lane 2 assumption refresh after Lane 1 closes.
- Generated LaTeX artifacts can obscure source diffs. Keep commits path-limited
  and do not stage generated logs unless the plan explicitly keeps golden logs.
- `microtype` unknown-slot fixes may affect optical margin behavior. Defer to
  Lane 4 unless a no-output-change proof is available.
- `pytest.ini` disables capture with `-p no:capture` for a local
  conda/readline issue, so a local green pytest run is not necessarily identical
  to a CI run with normal capture enabled.

## Test Plan

### Planned Verification

Run from `/Users/nathanlane/code/lane_latex_template`:

```bash
make lint
latexmk -pdf -interaction=nonstopmode main.tex
latexmk -pdf -interaction=nonstopmode -g main.tex
pytest -q
tests/check-spacing-integrity.sh main.pdf || true
rg -n "Warning|Error|Undefined|Overfull|Underfull|WARN -" main.log main.blg
rg -c "Unknown slot number" main.log
git status --porcelain=v1
```

Expected final signals:

- Required lint/build/test commands exit 0.
- Warning policy is explicit and documented.
- `pytest -q` does not leave unintended tracked-file churn.
- `tests/check-spacing-integrity.sh main.pdf` has a documented diagnostic or
  gating role and expected pass/fail behavior.
- Any remaining warning output is either eliminated or documented as accepted
  with exact evidence.
- Final porcelain status contains no unexpected generated artifacts beyond the
  source/doc changes and any deliberate tracked-log removals.

### Execution Results

- Baseline pre-change porcelain (snapshot):  
  ` M tests/compilation/logs/biblatex-manual-contract_pass1.log`  
  ` M tests/compilation/logs/biblatex-manual-contract_pass2.log`  
  ` M tests/compilation/logs/compatibility-backports.log`
- Final checks executed and green:
  - `make lint` (0)
  - `latexmk -pdf -interaction=nonstopmode main.tex` (0)
  - `latexmk -pdf -interaction=nonstopmode -g main.tex` (0)
  - `pytest -q` (17 passed)
  - `tests/check-spacing-integrity.sh main.pdf || true` (non-zero as expected for lane policy)
  - `rg -n "Warning|Error|Undefined|Overfull|Underfull|WARN -" main.log main.blg` (shows accepted template-content warnings only)
  - `rg -c "Unknown slot number" main.log` (241; accepted and deferred)
- Final porcelain status is limited to:
  - edited source/docs:
    `.gitignore`, `references.bib`, `CHANGELOG.md`, `README.md`,
    `tests/README.md`, `docs/technical/TESTING.md`
  - deleted transient fixtures: all `tests/compilation/logs/*.log`
- Warning policy now classifies `showhyphens`, remaining overfull/underfull
  warnings, and microtype unknown-slot reports as accepted in this lane unless a
  no-output-change fix is proven.
- `tests/check-spacing-integrity.sh` is explicitly advisory.

### Verifier Validation

- Method: command suite and artifact-state comparison against baseline.
- Evidence:
  - `make lint`, `latexmk -pdf -interaction=nonstopmode main.tex`,
    `latexmk -pdf -interaction=nonstopmode -g main.tex`, and `pytest -q` all
    exit 0.
  - Baseline-status comparison captured in `Execution Results` shows expected log churn was converted to tracked deletions under the transient-log contract.

## External Agent Challenge Findings

Source: external challenge/red-team agent, 2026-07-01. Grounded against the
working tree, `git log`, `.gitignore`, `pytest.ini`, and
`tests/test_regression_harness.py`. Ordered by severity. These are findings to
resolve before implementation, not accepted decisions.

### High severity

1. The tracked golden logs serve no verification purpose. Only
   `tests/test_regression_harness.py` consumes the harness output, and it
   asserts solely on `returncode == 0` (lines 19, 30, 59) and on `pdftotext`
   output of the PDF (lines 43-48). It never opens `compatibility-backports.log`,
   `*_pass1.log`, or `*_pass2.log`. Those files are redirected stdout
   (`tests/test-bibliography.sh:35,69`) that happens to be committed. Step 6's
   golden-vs-transient branch is therefore over-weighted: nothing compares
   against these logs, so there is no golden contract to preserve. The
   defensible answer is transient (gitignore or redirect).
2. The Constraints/Assumptions framing of the dirty logs is factually wrong.
   Lines 30-32 ("evidence from the previous `pytest -q` run … must not be
   silently reverted") and line 123 conflict with `git log`, which shows
   `a5dd714 Refresh compatibility backport log` — these are deliberately
   re-committed artifacts, neither incidental run evidence nor user-authored
   source. The "preserve as evidence" constraint freezes the exact problem the
   lane exists to fix.
3. The `.gitignore` policy is already half-migrated toward transient. Line 10
   ignores `*.log`; line 125 force-re-includes `!tests/compilation/logs/*.log`;
   lines 138-139 then re-ignore `minimal-root.log` and `minimal.log`. The plan
   treats `.gitignore` as a blank candidate (line 73) and never reconciles with
   this inconsistent per-file carve-out. The migration direction is already set;
   the lane should finish it, not re-open it.
4. "Golden + deterministic" (step 6c) is effectively infeasible for raw pdflatex
   logs. The working-tree diff shows `compatibility-backports.log` changing from
   a committed absolute path (`/Users/nathanlane/.../fixtures/…`) to `./tests/
   fixtures/…`, plus 79-column line-wrap differences. Raw TeX logs embed absolute
   paths, the TeX Live banner, and column-wrapped paths; byte-stable regeneration
   needs a normalization/scrub pass, which would be a net-new durable file and
   violate the Footprint Budget (line 97).

### Medium severity

5. The success criterion is unfalsifiable as written. Steps 1 and 9 both run
   `pytest -q`, which rewrites the three preserved logs, while line 31 forbids
   reverting them. There is no mechanism to distinguish preserved pre-existing
   dirt from new churn. Capture a `git status --porcelain` snapshot at step 1 and
   define success as "no new entries beyond that snapshot."
6. The churn fix targets the shell writers (`tests/run-tests.sh`,
   `tests/test-bibliography.sh`) but omits the contract owner,
   `tests/test_regression_harness.py`, from scope. It should be in scope at least
   read-only, since it is the file that would break if a redirect path changed.
7. `tests/check-spacing-integrity.sh main.pdf` is a circular gate. It currently
   fails, yet it stays in the required verification block (line 198) while step 7
   pre-declares it may be obsolete. Its role must be decided before certifying a
   green surface, or it must be explicitly demoted to non-gating.

### Low severity

8. The ISBN fix bans guessing (step 3, Risks) but supplies no offline mechanism.
   Name an offline-safe path: local ISBN-13 check-digit validation to prove
   malformation, or removal of the `isbn` field (clears the warning without
   asserting a false value).
9. Cross-lane collision not flagged. The three preserved logs are Lane 2 fixtures
   (`biblatex-manual-contract*`, `compatibility-backports`). Redirecting or
   ignoring them changes Lane 2's evidence surface; the roadmap's Cross-Lane
   Rules require flagging this.
10. Stale baseline: the plan cites `e0512f0` (line 43) but HEAD is already
    `0bc9b37` (this plan's own commit).
11. `pytest.ini:4` carries `-p no:capture` with a comment about a conda/readline
    capture segfault — an environment-specific workaround meaning local green does
    not guarantee CI green. Worth noting in a "trustworthy surface" lane.
12. Assumption line 109 ("commands currently exit 0") should be a verified
    precondition captured as step 1's first output, not an assumption.

### Recommended plan changes

- State plainly that no test reads these logs, make all
  `tests/compilation/logs/*.log` transient (finishing lines 138-139), delete the
  tracked copies, and drop step 6's golden branch and the "preserve as evidence"
  constraint.
- Snapshot `git status --porcelain` at step 1; success = no new porcelain entries
  after the final verification run.
- Resolve the `check-spacing-integrity.sh` classification before declaring the
  surface green, or remove it from the required block.
- Add `test_regression_harness.py` to scope; name the offline ISBN method; flag
  the Lane 2 evidence-surface collision.

## Resolutions

- Finding 1: `accepted-current`. The plan now treats raw harness logs as
  transient unless implementation proves a real golden-log consumer exists, and
  step 6 directs implementation to remove the tracked-log contract.
- Finding 2: `accepted-current`. The generated-log files are no longer described
  as evidence that must be preserved; they are now identified as generated
  artifacts to snapshot and resolve.
- Finding 3: `accepted-current`. `.gitignore` is now in scope specifically to
  remove or reconcile the `tests/compilation/logs/*.log` re-inclusion.
- Finding 4: `accepted-current`. The golden-log branch was removed from step 6;
  deterministic raw TeX log normalization is out of scope for this lane.
- Finding 5: `accepted-current`. Step 1 and the final verification now require
  pre/post `git status --porcelain=v1` comparison so success is falsifiable.
- Finding 6: `accepted-current`. `tests/test_regression_harness.py` is now in
  scope as the pytest contract owner for shell-harness behavior.
- Finding 7: `accepted-current`. `tests/check-spacing-integrity.sh main.pdf` is
  now advisory at plan start and appears in planned verification as
  `tests/check-spacing-integrity.sh main.pdf || true`.
- Finding 8: `accepted-current`. The ISBN step now names offline-safe routes:
  local check-digit validation or removing malformed `isbn` fields rather than
  guessing replacements.
- Finding 9: `accepted-current`. The Risks section now flags that tracked-log
  removal changes the Lane 2 fixture evidence surface and must refresh Lane 2
  assumptions.
- Finding 10: `accepted-current`. Worktree Context now records `0bc9b37` as the
  Draft plan birth commit instead of the earlier roadmap commit.
- Finding 11: `accepted-current`. `pytest.ini` is now in scope as read-only by
  default, and the Risks section records the `-p no:capture` local/CI parity
  concern.
- Finding 12: `accepted-current`. Baseline command success is no longer an
  assumption; implementation step 1 must verify and record current command
  outcomes.

## Plan Deltas

- 2026-07-01: Froze the plan after resolving externally appended material
  challenge findings.
- 2026-07-01: Changed the log-handling strategy from "preserve generated-log
  dirt as evidence" to "snapshot, then make raw TeX logs transient unless a real
  golden-log consumer is proven."
- 2026-07-01: Demoted `tests/check-spacing-integrity.sh main.pdf` from required
  green gate to advisory diagnostic until Lane 1 documents or rewrites its
  pass/fail semantics.
- 2026-07-01: Added `tests/test_regression_harness.py` and `pytest.ini` to scope
  for harness-contract and local/CI parity review.
- 2026-07-01: Added explicit offline-safe ISBN handling, cross-lane Lane 2
  collision risk, and pre/post porcelain status comparison.
- 2026-07-01: Completed log hygiene by removing all tracked
  `tests/compilation/logs/*.log` artifacts from git and documenting transient log
  handling; this changes expected final status to include staged deletions.
