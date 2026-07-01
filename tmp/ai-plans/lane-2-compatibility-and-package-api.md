---
topic: lane-2-compatibility-and-package-api
created: 2026-07-01
status: Frozen
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
- Branch: `codex/lane-2-compatibility-and-package-api` (create or switch from
  `main` before implementation).
- Worktree path: `/Users/nathanlane/code/lane_latex_template`.
- Detached: no.
- Plan path: `tmp/ai-plans/lane-2-compatibility-and-package-api.md`.
- External-output collision risk: low. This lane may run `latexmk` and shell harnesses
  that write local generated artifacts; no Overleaf, network, or external cache writes
  are planned.
- Waiver: none; implementation must not proceed directly on `main`.

## Files In Scope

- `paper/preamble-natbib.tex`
  - Repair load-order, package-option, and duplicate-alias problems that currently
    break natbib entry points.
- `paper/lltpaperstyle.sty`
  - Resolve module ownership and preloading behavior that affects API
    compatibility.
- `paper/lltpaperstyleminimal.sty`
  - Validate the separate minimal package load as distinct from the main-package
    `minimal` option.
- `paper/modules/lltfontfallbacks.sty`
  - Validate standalone-loading behavior and compatibility expectations.
- `paper/modules/lltfontfeatures.sty`
  - Validate standalone-loading behavior and compatibility expectations.
- `paper/modules/lltlists.sty`
  - Add local standalone dependency declarations if needed for environment hooks.
- `paper/modules/lltmathgridlocked.sty`
  - Add local standalone dependency declarations if needed for environment hooks.
- `paper/modules/lltparagraphs.sty`
  - Confirm load-order interactions when used standalone or with preloaded modules.
- `paper/modules/lltmicrotype.sty`
  - Read-only by default unless an API contract for module loading explicitly
    requires a minimal compatibility adjustment.
- `paper/modules/README.md`
  - Align standalone and preload claims with observed behavior.
- `paper/lltpaperstyle.dtx`
- `paper/lltpaperstyle.ins`
  - Verify .dtx/.ins extraction path and generated package outputs.
- `paper/README-DTX.md`
  - Mark the docstrip path non-authoritative until a release-packaging pass rebuilds
    it from the live package source.
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
- Expected changed-file budget: 10-18 tracked files.
  - Focus on `paper/` package files, `main.tex`, harnesses, tests, and
    compatibility-facing docs/changelog.
  - New compatibility probes should run from temp dirs or existing harness files;
    durable fixture files require a new plan delta.

## Assumptions

- Lane 1 decisions about warning policy are stable and accepted.
- Manual `biblatex` loading and module preloading are active user-facing compatibility
  surfaces and should be kept explicit in docs.
- `.dtx`/`.ins` outputs are non-authoritative for this lane; mark that clearly
  rather than asserting release-like distribution readiness.
- Standalone module support remains a public contract for modules documented as
  standalone; this lane fixes the in-scope dependency gaps rather than narrowing
  the claim by default.
- The main package `minimal` option means reduced typography modules, while
  `paper/lltpaperstyleminimal.sty` is a distinct package surface that must be
  validated separately.
- Module preloading is a supported extension mechanism only for documented
  load-order cases; unsupported orders must be rejected or documented explicitly.
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
2. Repair broken natbib preamble API behavior:
   - Load `lltpaperstyle` with the intended natbib option/order and remove duplicate
     citation aliases that redefine existing natbib commands.
   - Confirm no stale references remain in active docs and integration points.
3. Resolve DTX/INS extraction contract:
   - Inspect `paper/lltpaperstyle.dtx` and `paper/lltpaperstyle.ins` generation
     paths and outputs.
   - Mark the generated artifacts and maintainer instructions as non-authoritative
     until a future release-packaging pass rebuilds them from the live package
     source.
4. Validate standalone module behavior:
   - Probe `lltfontfallbacks`, `lltfontfeatures`, `lltlists`,
     `lltmathgridlocked`, and the separate `lltpaperstyleminimal` package load.
   - Add local dependency declarations such as `etoolbox` where an in-scope module
     uses environment hooks standalone.
   - Ensure failures are reported with actionable contract wording rather than
     silent fallback.
5. Reconcile module preload collisions:
   - Verify `lltparagraphs` preload interactions and ordering against
     `lltpaperstyle`.
   - Keep documented preloading supported while rejecting or documenting unsupported
     load orders, without changing typography output defaults.
6. Validate `biblatex` compatibility:
   - Assert the existing manual `biblatex` contract fixture emits no
     `biblatex Warning` under supported usage.
   - Keep non-visual compatibility fixes in place with clear scope notes.
7. Update module ownership and documentation:
   - Align `paper/modules/README.md` and `README.md` with the actual supported
     optional module and minimal options.
8. Capture final compatibility results and commit plan-visible notes about any
   remaining intentional limitations in compatibility claims.

## Risks

- DTX/INS rebuild work exceeds this lane; docs must prevent maintainers from treating
  the stale docstrip path as authoritative.
- Resolving module preload compatibility without visual deltas may require API
  contract changes that affect documented "out-of-the-box" expectations.
- Some compatibility paths may be accepted as best-effort if no stable external
  packaging distribution contract is present; those exceptions must be documented.
- If `paper/lltpaperstyleminimal.sty` is narrower than current docs claim,
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

Add focused compatibility checks from temp dirs or existing harness files for:

- natbib preamble load order, option selection, and duplicate citation aliases
- `.dtx` / `.ins` non-authoritative docs and extraction-path behavior
- `lltfontfallbacks`, `lltfontfeatures`, `lltlists`, `lltmathgridlocked`, and
  separate-package `lltpaperstyleminimal` standalone loads
- module preload order (`lltparagraphs` + `lltpaperstyle`)
- manual `biblatex` loading path under supported scenarios, including absence of
  `biblatex Warning` in the existing manual-contract fixture
- main-package `minimal` option behavior, distinct from separate
  `lltpaperstyleminimal` package behavior

### Execution Results

- Pending.

### Verifier Validation

- Method: pending
- Evidence: No review has run yet.

## Reviewer Findings

### 2026-07-01 challenge-plan (Critic)

1. **Files In Scope names three paths that do not exist in the checkout.**
   Evidence: `paper/llt.dtx` and `paper/llt.ins` are absent; the actual files are
   `paper/lltpaperstyle.dtx` and `paper/lltpaperstyle.ins` (see
   `paper/README-DTX.md:14` and the canonical findings' DTX section).
   `paper/modules/lltpaperstyleminimal.sty` is absent; the actual file is
   `paper/lltpaperstyleminimal.sty` (sibling of `paper/lltpaperstyle.sty`, not a
   module). Impact: the implementer is misdirected, and under the plan-template
   scope-token grammar the real files would fall outside the declared scope
   allowlist. Routing hint: accepted-current — correct the three tokens before
   freeze.

2. **Worktree Context is effectively main-checkout implementation without a
   waiver.** Evidence: `Mode: branch in checkout` but `Branch: main` and the
   worktree is the primary checkout; no `Waiver:` line; template fields
   `Detached:` and `Plan path:` are also missing. Lane 1 shipped via a task
   branch and PR (merge `5278ded`). Impact: substantive multi-file
   implementation would land directly on `main`, which the workflow flags as
   requiring an explicit waiver. Routing hint: accepted-current — either name a
   lane branch for implementation or record an explicit waiver.

3. **Roadmap Lane-2 decision gates are embedded as implementation steps instead
   of being decided.** Evidence: the master roadmap
   (`docs/superpowers/plans/2026-07-01-deep-review-roadmap.md`, § Lane 2
   "Decision gates before drafting Lane 2") requires four decisions before the
   lane plan is drafted: (a) DTX/INS authoritative vs non-authoritative,
   (b) standalone-module support as public contract vs narrowed docs,
   (c) what `minimal` means, (d) module preloading supported vs internal.
   The plan's Assumptions take partial positions on (a) and (d) only; steps 3–5
   carry "decide whether…" language into implementation. Impact: public-contract
   decisions get made mid-implementation, which the plan's own "no silent
   public-contract changes" constraint is meant to prevent. Routing hint:
   accepted-current — record one-line decisions for all four gates (in
   Assumptions via delta, or in Resolutions) before freeze, or explicitly waive
   with rationale.

4. **Standalone-module validation omits the modules the canonical findings
   actually name as broken.** Evidence:
   `DEEP_REVIEW_FINDINGS_2026-07-01.md` P2 cites `paper/modules/lltlists.sty:398`
   (`\AtBeginEnvironment` with no `\RequirePackage{etoolbox}` — confirmed live)
   and `paper/modules/lltmathgridlocked.sty:50` (`\AtEndEnvironment`, same gap),
   while `paper/modules/README.md:3` and `:53` claim every module works
   standalone. Plan step 4 and the test plan probe only `lltfontfallbacks`,
   `lltfontfeatures`, and `lltpaperstyleminimal`; `lltlists.sty` and
   `lltmathgridlocked.sty` are not in Files In Scope. Impact: step 7 cannot
   honestly align the README's standalone claims without deciding the status of
   the unprobed modules. Routing hint: accepted-current — either (i) narrow the
   README claim to the validated subset (docs-only, already in scope) or
   (ii) add the two module files plus one-line `etoolbox` requires to scope via
   plan delta. Pick one; do not do both by default.

5. **The `minimal` contract conflates a package option with a separate
   package.** Evidence: `README.md:308` documents
   `\usepackage[minimal]{lltpaperstyle}` (an option of the main package), while
   `lltpaperstyleminimal.sty` is a distinct sibling package at `paper/`. The
   plan's step 4 and test-plan bullets treat "lltpaperstyleminimal standalone
   load" and "minimal option behavior" as one mislocated item. Impact: the lane
   could validate one surface and claim both. Routing hint: accepted-current —
   name both surfaces explicitly (option behavior; separate-package load) and
   tie the resolution to gate (c) in finding 3.

6. **Footprint budget (net-new durable files: 0) is in tension with the test
   plan's new probes.** Evidence: the test plan adds ~6 focused compatibility
   checks; standalone-load probes normally need fixture `.tex` files (compare
   `tests/fixtures/biblatex-manual-contract.tex`). The roadmap suggests
   "temp-dir or pytest probes". Impact: the implementer must either violate the
   budget or improvise. Routing hint: accepted-current — one line stating probes
   run from temp dirs / existing harness files, or pre-authorize a small fixture
   count via plan delta.

7. **The plan omits the template's lifecycle sections.** Evidence: no
   `## Resolutions`, `## Plan Deltas`, or `Test Plan → Execution Results` /
   `Verifier Validation` blocks (this `Reviewer Findings` section was added by
   the Critic). Impact: downstream skills (`resolve-plan-findings`,
   `implement-from-plan`, `review-diff-vs-plan`) have no home for their required
   writes. Routing hint: accepted-current — mechanical: append the missing stub
   sections.

8. **Size and wording (advisory).** The plan is proportionate overall: eight
   steps map one-to-one onto roadmap Lane-2 scope candidates, with zero net-new
   abstractions. Two trims worth considering: (i) step 6's `biblatex` audit may
   reduce to asserting no `biblatex Warning` in the existing
   `biblatex-manual-contract` fixture log, since Lane 1 already settled warning
   policy; (ii) step 2's "pathing" framing does not match the canonical defect —
   `paper/preamble-natbib.tex:42` loads `lltpaperstyle` without the `natbib`
   option, `:50` loads natbib after biblatex is already selected, and `:93-94`
   redefine `\citeauthor`/`\citeyear` with `\newcommand` — the fix is load
   order/option plus removing duplicate aliases, not a path repair. Routing
   hint: optional; accept as wording tightening or reject with one line.

No other material findings; Constraints, Risks, and the verification command
set are consistent with the roadmap and Lane 1 outcomes.

## Resolutions

1. `accepted-current` — Corrected the three bad scope tokens to
   `paper/lltpaperstyle.dtx`, `paper/lltpaperstyle.ins`, and
   `paper/lltpaperstyleminimal.sty` before freeze.
2. `accepted-current` — Updated `Worktree Context` with the intended
   implementation branch `codex/lane-2-compatibility-and-package-api`,
   `Detached: no`, the canonical plan path, and an explicit no-waiver rule
   against implementing directly on `main`.
3. `accepted-current` — Recorded the four Lane-2 gate decisions before freeze:
   `.dtx`/`.ins` is non-authoritative for this lane; standalone support remains
   public for documented standalone modules; `minimal` means reduced typography
   modules while `lltpaperstyleminimal` is a separate package surface; documented
   module preloading remains supported, with unsupported load orders rejected or
   documented explicitly.
4. `accepted-current` — Chose the code-fix route for the named standalone module
   gaps by adding `paper/modules/lltlists.sty` and
   `paper/modules/lltmathgridlocked.sty` to scope for local dependency
   declarations such as `etoolbox`; the plan does not narrow the README claim by
   default.
5. `accepted-current` — Split the main-package `minimal` option from the separate
   `paper/lltpaperstyleminimal.sty` package throughout scope, assumptions, and
   verification bullets.
6. `accepted-current` — Kept the zero-new-durable-files budget by requiring new
   probes to use temp dirs or existing harness files unless a later plan delta
   explicitly authorizes fixtures.
7. `accepted-current` — Added the missing lifecycle sections and stubs:
   `Execution Results`, `Verifier Validation`, `Resolutions`, and `Plan Deltas`.
8. `accepted-current` — Accepted the advisory wording tightening: step 2 now names
   natbib load-order/option/alias defects, and step 6 narrows `biblatex`
   verification to the existing manual-contract fixture warning check.

## Plan Deltas

- Status advanced from `Needs Resolution` to `Frozen` after all critic findings
  were routed.
- Worktree baseline changed from direct `main` implementation to the branch
  `codex/lane-2-compatibility-and-package-api` with no direct-main waiver.
- Scope tokens were corrected for DTX/INS and the separate minimal package, and
  scope was expanded to `paper/README-DTX.md`, `paper/modules/lltlists.sty`, and
  `paper/modules/lltmathgridlocked.sty`.
- Assumptions now record the four Lane-2 public-contract decisions before
  implementation.
- Implementation and verification wording now distinguish natbib load-order/API
  defects, DTX non-authoritative documentation, standalone module dependency
  fixes, module preload support, manual `biblatex` warning checks, the main
  `minimal` option, and the separate `lltpaperstyleminimal` package.
- Lifecycle stubs were added for downstream `implement-from-plan` and
  `review-diff-vs-plan` writes.
