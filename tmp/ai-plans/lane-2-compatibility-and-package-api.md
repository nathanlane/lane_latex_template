---
topic: lane-2-compatibility-and-package-api
created: 2026-07-01
status: Draft
---

# Lane 2 Compatibility And Package API

## Task

Repair package/API compatibility so documented usage paths behave consistently for
standalone package loading, module composition, and optional module contracts, while
keeping all typography and visual defaults unchanged.

## Constraints

- Preserve visual output defaults: do not change margins, fonts, colors, spacing,
  numbering schemes, or float-placement defaults in this lane.
- Treat `docs/superpowers/plans/2026-07-01-deep-review-roadmap.md` as the
  master roadmap and `docs/technical/DEEP_REVIEW_FINDINGS_2026-07-01.md` as the
  canonical findings source.
- Lane 1 is complete and merged; avoid re-opening build-hygiene drift unless a
  compatibility fix changes command contracts.
- Every material LaTeX code fix must include a `%% FIX:` comment with a concise
  rationale.
- Update `CHANGELOG.md` and relevant README/docs sections after any material
  change.
- No silent public-contract changes: if optional module behavior is narrowed, the
  docs must reflect it in the same commit.
- Do not implement typography work; defer content layout changes to Lane 4.

## Worktree Context

- Mode: branch in checkout.
- Repository path: `/Users/nathanlane/code/lane_latex_template`.
- Branch: `main`.
- Worktree path: `/Users/nathanlane/code/lane_latex_template`.
- External-output collision risk: low. This lane may run `latexmk` and shell harnesses
  that write local generated artifacts; no Overleaf, network, or external cache writes
  are planned.

## Files In Scope

- `paper/preamble-natbib.tex`
  - Repair pathing or usage problems that currently break natbib entry points.
- `paper/lltpaperstyle.sty`
  - Resolve module ownership and preloading behavior that affects API
    compatibility.
- `paper/modules/lltfontfallbacks.sty`
  - Validate standalone-loading behavior and compatibility expectations.
- `paper/modules/lltfontfeatures.sty`
  - Validate standalone-loading behavior and compatibility expectations.
- `paper/modules/lltpaperstyleminimal.sty`
  - Confirm real `minimal` contract and avoid regressions in reduced module sets.
- `paper/modules/lltparagraphs.sty`
  - Confirm load-order interactions when used standalone or with preloaded modules.
- `paper/modules/lltmicrotype.sty`
  - Read-only by default unless an API contract for module loading explicitly
    requires a minimal compatibility adjustment.
- `paper/modules/README.md`
  - Align standalone and preload claims with observed behavior.
- `paper/llt.dtx`
- `paper/llt.ins`
  - Verify .dtx/.ins extraction path and generated package outputs.
- `main.tex`
  - Keep as a controlled integration test for API loading paths and preload
    contract changes.
- `tests/run-tests.sh`
  - Include compatibility-focused probes for standalone and preload paths.
- `tests/test-bibliography.sh`
  - Include manual `biblatex` loading checks if they remain part of API contract.
- `tests/test_regression_harness.py`
  - Ensure command probes map to the compatibility checks and fail only on true
    compatibility regressions.
- `README.md`
  - Reflect supported package/API entry points and any narrowed module promises.
- `CHANGELOG.md`
  - Record material compatibility behavior changes.

## Footprint Budget

- Net-new durable files: 0.
  - Prefer edits to existing packaging/docs/tests. New helpers should only be added
    with a plan delta.
- Net-new abstractions: 0.
  - Keep scope to contract-preserving compatibility fixes.
- Expected changed-file budget: 8-16 tracked files.
  - Focus on `paper/` package files, `main.tex`, harnesses, tests, and
    compatibility-facing docs/changelog.

## Assumptions

- Lane 1 decisions about warning policy are stable and accepted.
- Manual `biblatex` loading and module preloading are active user-facing compatibility
  surfaces and should be kept explicit in docs.
- Any `.dtx`/`.ins` output mismatch must be reconciled before asserting release-like
  distribution claims.
- Standalone module compatibility can be validated from local tooling without external
  package publication or network dependencies.

## Implementation Plan

1. Rebaseline compatibility evidence and keep a clean working index:
   - `git status --porcelain=v1`
   - `make lint`
   - `latexmk -pdf -interaction=nonstopmode main.tex`
   - `pytest -q`
   - `tests/run-tests.sh`
   - Capture baseline `rg` checks for package entry points and module loads.
2. Repair broken preamble API paths:
   - Validate `paper/preamble-natbib.tex` import path and document the resulting
     behavior.
   - Confirm no stale references remain in active docs and integration points.
3. Resolve DTX/INS extraction contract:
   - Inspect `paper/llt.dtx` and `paper/llt.ins` generation paths and outputs.
   - Decide whether generated artifacts are authoritative for compatibility promises;
     if not, mark them as non-authoritative in docs in the same scope.
4. Validate standalone module behavior:
   - Probe `lltfontfallbacks`, `lltfontfeatures`, and `lltpaperstyleminimal`
     loading paths as standalone/optional modules.
   - Ensure failures are reported with actionable contract wording rather than
     silent fallback.
5. Reconcile module preload collisions:
   - Verify `lltparagraphs` preload interactions and ordering against
     `lltpaperstyle`.
   - Remove ambiguous or conflicting preload semantics where safe, without changing
     typography output defaults.
6. Validate `biblatex` compatibility:
   - Audit manual `biblatex` loading calls in build/docs paths and ensure they do not
     add warnings in supported usage.
   - Keep non-visual compatibility fixes in place with clear scope notes.
7. Update module ownership and documentation:
   - Align `paper/modules/README.md` and `README.md` with the actual supported
     optional module and minimal options.
8. Capture final compatibility results and commit plan-visible notes about any
   remaining intentional limitations in compatibility claims.

## Risks

- DTX/INS and standalone-module claims may require broader packaging decisions that
  exceed this lane and could defer parts of the API to a future packaging pass.
- Resolving module preload compatibility without visual deltas may require API
  contract changes that affect documented "out-of-the-box" expectations.
- Some compatibility paths may be accepted as best-effort if no stable external
  packaging distribution contract is present; those exceptions must be documented.
- If `paper/modules/lltpaperstyleminimal.sty` is narrower than current docs claim,
  docs changes could be larger than code changes.
- Tests currently assert shell return codes and PDF text; a regression in API surface
  may require adding compatibility probes and could increase verification scope.

## Test Plan

### Planned Verification

Run from `/Users/nathanlane/code/lane_latex_template`:

```bash
make lint
latexmk -pdf -interaction=nonstopmode main.tex
pytest -q
tests/run-tests.sh
git status --short
```

Add focused compatibility checks for:

- natbib preamble path resolution
- `.dtx` / `.ins` generation path and outputs
- `lltfontfallbacks`, `lltfontfeatures`, `lltpaperstyleminimal` standalone load
- module preload order (`lltparagraphs` + `lltpaperstyle`)
- manual `biblatex` loading path under supported scenarios
- minimal option behavior
