---
topic: lane-2-compatibility-and-package-api
created: 2026-07-01
status: Reviewed
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
    break natbib entry points, including the TeX Live 2025 `doi.sty`
    `\doiprefix` contract.
- `paper/lltpaperstyle.sty`
  - Resolve module ownership, preloading behavior, and package loading order that
    affects API compatibility.
- `paper/lltpaperstyleminimal.sty`
  - Validate the separate minimal package load as distinct from the main-package
    `minimal` option, including standalone dependencies for package hooks.
- `paper/modules/lltfontfallbacks.sty`
  - Validate standalone-loading behavior and compatibility expectations, including
    local conditionals needed outside the main package.
- `paper/modules/lltfontfeatures.sty`
  - Validate standalone-loading behavior and compatibility expectations, including
    idempotent text-symbol fallbacks.
- `paper/modules/lltlists.sty`
  - Add local standalone dependency declarations if needed for environment hooks.
- `paper/modules/lltmathgridlocked.sty`
  - Add local standalone dependency declarations if needed for environment hooks.
- `paper/modules/lltparagraphs.sty`
  - Confirm and repair load-order interactions when used standalone or with
    preloaded modules.
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
- `tests/fixtures/biblatex-manual-contract.tex`
  - Keep the documented manual-`biblatex` regression fixture aligned with the
    warning-free supported loading order.
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
   - Confirm the branch diff does not ship the out-of-scope `.claude/commands/`
     metadata; remove or move it off the lane branch before PR if still present.
   - `make lint`
   - `latexmk -pdf -interaction=nonstopmode main.tex`
   - `pytest -q`
   - `tests/run-tests.sh`
   - Capture baseline `rg` checks for package entry points and module loads.
2. Repair broken natbib preamble API behavior:
   - Load `lltpaperstyle` with the intended natbib option/order and remove duplicate
     citation aliases that redefine existing natbib commands.
   - Guard or remove the `\doiprefix` customization so TeX Live 2025 `doi.sty`
     compiles the documented natbib entry point.
   - Clean up any remaining no-op or self-referential citation aliases and comments
     that no longer describe natbib behavior.
   - Correct stale inline comments that still describe `\cite` as parenthetical
     after natbib has supplied its own command behavior.
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
   - Repair the currently failing standalone surfaces: `lltfontfallbacks`
     undefined conditionals, `lltfontfeatures` repeated text-symbol definitions,
     and `lltpaperstyleminimal` missing package-hook dependencies.
   - Add local dependency declarations such as `etoolbox` where an in-scope module
     uses environment hooks standalone.
   - Ensure failures are reported with actionable contract wording rather than
     silent fallback.
5. Reconcile module preload collisions:
   - Verify `lltparagraphs` preload interactions and ordering against
     `lltpaperstyle`.
   - Repair the `\noindentpar` collision for the documented preload path or document
     that exact load order as unsupported in the same commit.
   - Document the supported optional-module composition order explicitly: optional
     paragraph modules must be loaded before `lltpaperstyle`, and loading
     `lltparagraphs` after `lltpaperstyle` is unsupported unless fully guarded.
   - Keep documented preloading supported while rejecting or documenting unsupported
     load orders, without changing typography output defaults.
6. Validate `biblatex` compatibility:
   - Fix the supported manual-`biblatex` loading path or update the documented
     pattern before enforcing the no-warning gate.
   - Assert the existing manual `biblatex` contract fixture emits no
     `biblatex Warning` under supported usage.
   - Keep non-visual compatibility fixes in place with clear scope notes.
7. Update module ownership and documentation:
   - Align `paper/modules/README.md` and `README.md` with the actual supported
     optional module and minimal options.
   - Remove any README wording that describes `lltpaperstyleminimal` as a
     `lltpaperstyle` option; keep it documented only as a separate package surface.
   - Replace blanket standalone-module claims with wording that matches the repaired
     probes and table-listed support.
   - Extend `CHANGELOG.md` so every material package-side fix from the
     compatibility rework is recorded, including lazy `inputenc`, natbib
     `\doiprefix`, paragraph preload shims, fallback/font-feature repairs, and
     `lltpaperstyleminimal`'s hook dependency.
   - Note the `nobiblatex`/manual-biblatex loading contract clearly enough that the
     warning-free path is reproducible.
8. Harden the compatibility probe harness:
   - Add the missing main-package `minimal` option probe alongside the separate
     `lltpaperstyleminimal` package probe.
   - Let compatibility probes continue after individual failures and report the full
     failure set before exiting nonzero.
   - Clean compatibility-probe auxiliary files from the repo root as well as the
     temporary source directory, because `pdflatex` runs from `PROJECT_ROOT`.
9. Capture final compatibility results and commit plan-visible notes about any
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
- The active branch contains an out-of-scope metadata commit; it must be removed,
  moved, or explicitly blocked before the lane PR so the compatibility branch does
  not silently ship unrelated files.

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
- natbib `doi.sty` compatibility, including absence of the `\doiprefix` undefined
  error under TeX Live 2025
- `.dtx` / `.ins` non-authoritative docs and extraction-path behavior
- `lltfontfallbacks`, `lltfontfeatures`, `lltlists`, `lltmathgridlocked`, and
  separate-package `lltpaperstyleminimal` standalone loads
- module preload order (`lltparagraphs` + `lltpaperstyle`)
- manual `biblatex` loading path under supported scenarios, including absence of
  `biblatex Warning` in the existing manual-contract fixture
- main-package `minimal` option behavior, distinct from separate
  `lltpaperstyleminimal` package behavior
- compatibility-probe harness behavior that reports all probe failures before
  exiting nonzero

### Execution Results

- Compatibility surface fixes were completed against the lane scope:
  - `paper/preamble-natbib.tex`, `paper/lltpaperstyle.sty`,
    `paper/lltpaperstyleminimal.sty`, and module files in
    `paper/modules/{lltfontfallbacks,lltfontfeatures,lltparagraphs}.sty`
    were updated to repair API contracts without visual changes.
  - `paper/lltpaperstyle.dtx` and `paper/README-DTX.md` were marked as
    non-authoritative for release packaging behavior during this lane.
  - `paper/modules/README.md` and `README.md` now reflect the separate
    minimal package surface and validated dependency requirements for standalone
    modules.
  - `tests/run-tests.sh` now evaluates all compatibility probes and returns a
    cumulative failure count instead of stopping at first failure.
  - `tests/fixtures/biblatex-manual-contract.tex` now follows the documented
    warning-free manual-`biblatex` loading order.
  - `CHANGELOG.md` records all material compatibility/API fixes.
- `make lint` passed.
- `latexmk -pdf -interaction=nonstopmode main.tex` passed and produced
  `main.pdf` (41 pages).
- `pytest -q` passed: `18 passed in 68.28s`.
- `tests/run-tests.sh` passed: `Passed: 115`, `Failed: 0`, and all compatibility
  probes passed.
- `git status --short` before the final plan commit showed only the plan file
  modified.
- Post-review W1-W4 pass completed on 2026-07-03 in implementation commit
  `7dfaed4`:
  - `README.md` now documents the supported optional-module order for
    `lltparagraphs`: load optional modules before `lltpaperstyle`; reverse order
    remains unsupported unless fully guarded.
  - `CHANGELOG.md` now records the package-side fixes from `aa7a5b7`, including
    lazy `inputenc` loading, the natbib `\doiprefix` guard, paragraph preload
    shims, `lltfontfallbacks`, `lltfontfeatures`, and `lltpaperstyleminimal`.
  - `tests/run-tests.sh` now cleans root-path fallback `.aux`, `.log`, `.out`,
    `.bcf`, and `.run.xml` files for temporary compatibility probes.
  - `paper/preamble-natbib.tex` no longer describes the fallback `\cite` alias
    as parenthetical, and `README.md` documents the manual-`biblatex` /
    `nobiblatex` encoding-loading contract.
- Post-review verification rerun from the repo root on 2026-07-03:
  - `make lint` passed.
  - `latexmk -pdf -interaction=nonstopmode main.tex` passed with `main.pdf`
    already up to date.
  - `pytest -q` passed: `18 passed in 59.19s`.
  - `tests/run-tests.sh` passed: `Passed: 115`, `Failed: 0`, and all
    compatibility probes passed.
  - `git status --short` was clean after implementation commit `7dfaed4`.
  - Root-level compatibility-probe artifact check returned no matching
    `prelude-*`, `main-package-minimal-option.*`, `standalone-*`, or
    `preload-lltparagraphs-into-paperstyle.*` files.

### Verifier Validation

- Method: reran-planned-verification
- Evidence: Independently reran all planned commands on 2026-07-02: `make lint`
  passes; forced `latexmk -g` rebuild produces `main.pdf` (41 pages, matching
  the owner record); `pytest -q` 18 passed; `tests/run-tests.sh` Passed 115 /
  Failed 0 with all nine compatibility probes green; `git status --short`
  clean. Probe-level failures found in the first review pass no longer
  reproduce.
- Evidence: Reran the planned post-review command set on 2026-07-03 after W1-W4:
  `make lint` passed; `latexmk -pdf -interaction=nonstopmode main.tex` passed;
  `pytest -q` passed with 18 tests; `tests/run-tests.sh` passed with Passed 115 /
  Failed 0 and all compatibility probes green; `git status --short` was clean
  after committing the implementation; a root-level compatibility-probe artifact
  check found no leftover temp probe files.
- Evidence: Pass-3 verifier independently reran the full planned command set on
  2026-07-03: `make lint` passed; a forced `latexmk -g -pdf` rebuild produced
  `main.pdf` (41 pages, exit 0, no errors); `pytest -q` 18 passed;
  `tests/run-tests.sh` Passed 115 / Failed 0 with all eight compatibility
  probes green; `git status --short` clean; no `prelude-*`, `standalone-*`,
  `preload-*`, or `main-package-minimal-option.*` artifacts in the repo root
  after the suite run.

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

### 2026-07-02 review-diff-vs-plan (Verifier)

Reviewed diff `main...codex/lane-2-compatibility-and-package-api`
(implementation commit `df7e41c`, plus `bfa5988`). Scope gate script
`scripts/check_workflow_gates.py` does not exist in this repo; a manual
file-list-vs-scope-token check was performed instead.

V1. **The implement step never completed its lifecycle contract.** Evidence:
    frontmatter arrived at review as `status: Implementing` and
    `Execution Results` still reads "Pending."; no `Implemented`/`Blocked`
    status commit exists after `df7e41c`. Impact: the owner recorded no
    verification, and rerunning it (V2) shows the gates are red — the honest
    implement-step outcome was `Blocked` or continued work, not a silent
    handoff. Routing hint: accepted-current — return to `Frozen` and
    re-implement.

V2. **Planned verification fails when rerun.** Evidence: `pytest -q` → 4
    failed / 14 passed; `tests/run-tests.sh` exits 1. Three pytest failures
    cascade from the natbib probe (V3); the fourth is the manual-biblatex
    warning gate (V4). `make lint`, `latexmk -pdf ... main.tex`, and
    `git status --short` (clean tree) pass. Impact: the lane's own test plan
    rejects the implementation as shipped. Routing hint: accepted-current.

V3. **The natbib entry point still fails to compile.** Evidence:
    `paper/preamble-natbib.tex:80` runs `\renewcommand{\doiprefix}` but the
    TeX Live 2025 `doi.sty` no longer defines `\doiprefix` →
    `! LaTeX Error: Command \doiprefix undefined` in the probe log. The
    load-order/option/alias repairs in `df7e41c` are correct as far as they
    go (natbib loads once with `authoryear,round,semicolon,sort&compress`),
    but the lane's central P1 repair is incomplete: the documented entry
    point still cannot compile. Routing hint: accepted-current — guard or
    drop the `\doiprefix` customization.

V4. **The biblatex warning gate was added without the underlying fix.**
    Evidence: `tests/test-bibliography.sh` now hard-fails on
    `Package biblatex Warning`, but `paper/lltpaperstyle.sty:150/235/315`
    still load `inputenc` after a manually loaded `biblatex`, so the
    documented supported path emits `Load 'inputenc' before biblatex` and
    the gate is permanently red. The canonical finding's fix order was:
    change the loading/documentation first, then assert. Routing hint:
    accepted-current — fix ordering (or the documented pattern) in the same
    change that keeps the assertion.

V5. **Four of seven compatibility probes fail; the in-scope contracts they
    encode were never repaired.** Evidence (probe reruns, TeX Live 2025):
    `standalone-lltfontfeatures` → `\textendash already defined`
    (`paper/modules/lltfontfeatures.sty:154-155`, also self-referential
    definitions; in scope, untouched); `standalone-lltfontfallbacks` →
    `\inconsolataloadedtrue` undefined standalone
    (`paper/modules/lltfontfallbacks.sty:15`, no local `\newif`);
    `standalone-lltpaperstyleminimal` → `\AtEndPreamble` undefined
    (`paper/lltpaperstyleminimal.sty:79`, no `etoolbox` require — the exact
    defect class fixed in lltlists/lltmathgridlocked);
    `preload-lltparagraphs-into-paperstyle` → `\noindentpar already defined`
    (`paper/modules/lltparagraphs.sty:41` vs `paper/lltpaperstyle.sty:730`,
    both `\newcommand`; step 5 produced no code or doc change). Impact:
    steps 4-5 added probes encoding contracts that do not hold. Routing
    hint: accepted-current — fix each surface or explicitly document it as
    unsupported in the same commit, per the plan's no-silent-narrowing
    constraint.

V6. **README.md documents `lltpaperstyleminimal` as a package option.**
    Evidence: new "Available options" bullet
    "`lltpaperstyleminimal` – Load the standalone minimal package variant";
    `paper/lltpaperstyle.sty:134-144` declares no such option and has no
    `\DeclareOption*`, so `\usepackage[lltpaperstyleminimal]{lltpaperstyle}`
    errors with an unknown-option failure. This reintroduces in docs the
    option-vs-package conflation that Resolution 5 removed from the plan.
    Routing hint: accepted-current — delete the bullet; the correct
    clarifying Note below it already exists.

V7. **`paper/modules/README.md` still overclaims standalone support.**
    Evidence: line 3 ("can be used independently") and the Design
    Principles line ("Each module can function standalone") were left as
    blanket claims while the new inserted paragraph narrows support to
    table-listed modules — and per V5 even two table-listed modules fail
    standalone. Impact: step 7 ("align claims with observed behavior") is
    not met. Routing hint: accepted-current — align wording with whatever
    V5 resolution makes true.

V8. **One planned probe is missing.** Evidence: the test-plan bullet
    "main-package `minimal` option behavior, distinct from separate
    `lltpaperstyleminimal` package behavior" has no corresponding probe in
    `tests/run-tests.sh`. Routing hint: accepted-current — add the option
    probe alongside the existing package probe.

V9. **Out-of-scope commit on the lane branch breaks the footprint budget.**
    Evidence: `bfa5988` adds six net-new files under `.claude/commands/`,
    none in `Files In Scope`, against a net-new-durable-files budget of 0
    with no plan delta; the roadmap's cross-lane rule requires commits
    path-scoped to the active lane. Routing hint: deferred-backlog or
    user-accepted delta — either drop/move the commit off the lane branch
    or record an explicit justification; it should not ship silently inside
    the lane PR.

V10. **Advisory (minor, non-blocking).** (i) `run_compatibility_probes`
    lacks the `|| true` continuation the fixture loop uses, so the first
    probe failure aborts `tests/run-tests.sh` before remaining probes and
    the summary run. (ii) `\providecommand{\cite}{\citep}` at
    `paper/preamble-natbib.tex:62` is a no-op once natbib is loaded, so the
    adjacent "Default to parenthetical" comment no longer describes the
    behavior (natbib's `\cite` is textual in authoryear mode); either
    restore `\renewcommand` after load or fix the comment. (iii) The kept
    self-referential aliases (`\providecommand{\citeauthor}[1]{\citeauthor{#1}}`)
    are latent infinite recursion if natbib were ever absent; the canonical
    finding recommended deleting them. Routing hint: fold into the V3/V5
    re-implementation.

### 2026-07-02 review-diff-vs-plan (Verifier, pass 2)

Reviewed diff `main...codex/lane-2-compatibility-and-package-api` after the
rework commits (`6e11333`, `aa7a5b7`, `307f52f`). Manual scope check: all 18
changed files are in `Files In Scope`; the out-of-scope `.claude/commands/`
files were removed from the branch diff (V9 resolved). Prior findings V1-V9
and V10(i)/(iii) are verified fixed: the `\doiprefix` guard, lazy `inputenc`
loading, symmetric `\providecommand`/environment guards, the
`\ifinconsolataloaded` typo repair, `lltpaperstyleminimal`'s `etoolbox`
require, the removed README option bullet, the reworded standalone claims,
the added `minimal`-option probe, and cumulative probe failure reporting all
check out in code and under rerun (nine probes green, suite 115/0, pytest
18/18).

W1. **The reverse composition order still hard-fails and remains
    undocumented.** Evidence: a probe compiling `\usepackage{lltpaperstyle}`
    followed by `\usepackage{lltparagraphs}` fails with
    `! LaTeX Error: Command \dialogue already defined`;
    `paper/modules/lltparagraphs.sty` still defines `\dialogue`,
    `\quoteattribution` (:136), `\academicdropcap` (:208), and the
    `epigraph` (:62) / `emphasisquote` (:144) environments unguarded, while
    `README.md:351` advertises `lltparagraphs` as an optional module without
    stating any load order. Impact: the Task names "module composition" and
    the Assumptions require unsupported orders to be "rejected or documented
    explicitly"; a reader following the README's Modular Architecture
    section would naturally load the module after the package and hit a raw
    duplicate-definition error. Smallest fix is one documented sentence
    ("load optional modules before `lltpaperstyle`; loading them after is
    unsupported") or module-side guards mirroring the package's. Routing
    hint: accepted-current (docs-only acceptable).

W2. **CHANGELOG does not record the second commit's package-side fixes,
    contradicting Execution Results.** Evidence: the 2026-07-02 section
    covers the first-pass changes plus two harness/docs bullets, but omits
    `aa7a5b7`'s material fixes: the `\doiprefix` guard, the
    `inputenc` lazy-loading rework in `paper/lltpaperstyle.sty`, the
    preload ownership shims in `lltpaperstyle`/`lltparagraphs`, the
    `lltfontfallbacks` conditional repair, the `lltfontfeatures` dash-alias
    repair, and `lltpaperstyleminimal`'s new `etoolbox` dependency.
    The Constraints require CHANGELOG updates for material changes, and
    `Execution Results` states "CHANGELOG.md records all material
    compatibility/API fixes", which is currently inaccurate. Routing hint:
    accepted-current — extend the 2026-07-02 section.

W3. **Compatibility probes litter auxiliary files into the repo root.**
    Evidence: after `tests/run-tests.sh`, the checkout root contains
    `prelude-natbib-preamble.aux/.log/.out`, `standalone-*.aux/.log`, and
    `main-package-minimal-option.aux/.bcf/.log/.out/.run.xml`. The probe
    sources live in the temp dir, so `test_latex_file`'s cleanup paths
    (`${tex_file%.tex}.aux` etc.) never match the files pdflatex writes
    into `PROJECT_ROOT`; the PDF got a root-path fallback in `aa7a5b7` but
    the auxiliary cleanup did not. The files are gitignored (tree stays
    clean), but the lane's own CHANGELOG claims "fixed harness artifact
    handling for temporary compatibility probes". Routing hint:
    accepted-current — extend the cleanup to the same root-path fallback.

W4. **Advisory (minor, non-blocking).** (i) The inline comment
    "% Default to parenthetical" at the `\providecommand{\cite}{\citep}`
    line still misdescribes natbib's actual `\cite` behavior even though
    the `%% FIX:` note above it is now accurate; V10(ii) is otherwise
    stale. (ii) Under the `nobiblatex` option with no manually loaded
    `biblatex`, `inputenc` is now never loaded (the maybe-load call sits
    only in the biblatex/natbib branch and minimal mode); harmless on
    LaTeX ≥ 2018 where UTF-8 is the default, but it is a silent behavior
    change for that path worth one CHANGELOG/docs line alongside W2.
    Routing hint: fold into the W1-W3 fix commit.

### 2026-07-03 review-diff-vs-plan (Verifier, pass 3)

Reviewed diff `main...codex/lane-2-compatibility-and-package-api` after the
W1-W4 followup commits (`7dfaed4`, `12721df`). Manual scope check: all 18
changed files are modifications inside `Files In Scope`, with zero net-new
files (footprint budget of 0 held; probes run from a `mktemp -d` dir) and no
`.claude/commands/` content on the branch (V9 stays resolved).

Prior findings W1-W4 are verified fixed in code, docs, and under rerun:

- W1: `README.md` (Modular Architecture) now states "Load optional modules
  such as `lltparagraphs` before `lltpaperstyle`. Loading `lltparagraphs`
  after `lltpaperstyle` is unsupported unless the reverse order is fully
  guarded." — the docs-only route the finding explicitly allowed. The
  supported preload order is additionally guarded on the package side
  (`\providecommand` / `\@ifundefined` shims in `lltpaperstyle.sty` and
  `lltparagraphs.sty`); the reverse order remains unguarded in
  `lltparagraphs.sty` and is now documented as unsupported.
- W2: the 2026-07-02 `CHANGELOG.md` section now records the second commit's
  package-side fixes: the `\doiprefix` guard, lazy `inputenc` loading,
  paragraph preload ownership shims, `lltfontfallbacks` conditional repair,
  `lltfontfeatures` dash-alias repair, `lltpaperstyleminimal`'s `etoolbox`
  dependency, and the `lltlists`/`lltmathgridlocked` standalone dependency
  declarations. The W4(ii) `nobiblatex`/encoding note is present in both
  `CHANGELOG.md` and `README.md` ("With `nobiblatex`, the template does not
  load `biblatex` or `inputenc`.").
- W3: `test_latex_file` now removes root-path fallback `.aux`, `.log`,
  `.out`, `.toc`, `.bcf`, and `.run.xml` files; verified empirically — after
  a full `tests/run-tests.sh` run the repo root contains no probe artifacts.
- W4(i): the stale "% Default to parenthetical" comment is gone; the
  `\providecommand{\cite}{\citep}` line now reads "% Legacy fallback only"
  with an accurate `%% FIX:` note.

Independent verification rerun (see Verifier Validation): `make lint` passed;
forced `latexmk -g` rebuild produced `main.pdf` (41 pages) with no errors,
consistent with the visual-defaults constraint; `pytest -q` 18 passed;
`tests/run-tests.sh` Passed 115 / Failed 0 with all compatibility probes
green; `git status --short` clean; no root probe artifacts. Spot checks:
no stale `\ifinconsolataaloaded` references remain; all `##1` doubled-token
fallbacks in `lltfontfallbacks.sty` sit inside `\newcommand` bodies where
doubling is required; neither `lltfontfallbacks` nor `lltfontfeatures` is
loaded by the main package, so their repairs cannot alter default output;
`paper/modules/README.md` code fences remain balanced after the edit.

X1. **Advisory (minor, non-blocking; no material findings this pass).**
    (i) When a compatibility probe fails, `run_compatibility_probes`
    returns 1 and `set -euo pipefail` ends `tests/run-tests.sh` before the
    final "Test Summary" block; every probe still runs, each failure is
    logged, the cumulative count prints, and the exit code is nonzero, so
    the plan's full-failure-set requirement is met — only the trailing
    Passed/Failed recap is skipped in that path. (ii) `README.md` says the
    natbib preamble "provides the compatibility aliases (`\textcite`,
    `\autocite`, `\citeauthor`, `\citeyear`)"; the preamble now defines only
    the first two, while `\citeauthor`/`\citeyear` come natively from natbib
    (the self-referential aliases were correctly deleted) — the commands all
    work as documented, the attribution is just loose. (iii) The
    "% Alias for consistency" comment on `\providecommand{\citestyle}` is
    stale: with natbib loaded first the line is a deliberate no-op that
    preserves natbib's native `\citestyle`. Routing hint: fold into any
    future docs pass; none of these block `Reviewed`.

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

### 2026-07-02 review-diff-vs-plan (Verifier)

V1. `accepted-current` — The lifecycle contract was not completed and verifier
    reruns show red gates, so the plan returns to `Frozen` for re-implementation
    rather than advancing toward closeout.
V2. `accepted-current` — Planned verification failures remain current blockers;
    the re-implementation must make `pytest -q` and `tests/run-tests.sh` pass
    before recording new execution results.
V3. `accepted-current` — The natbib entry point still fails under TeX Live 2025;
    the plan now requires guarding or removing the `\doiprefix` customization and
    cleaning up stale/no-op citation aliases or comments.
V4. `accepted-current` — The manual-`biblatex` no-warning gate is valid only after
    the supported loading path or documented pattern is fixed; the plan now orders
    that fix before asserting the gate.
V5. `accepted-current` — The failing standalone/preload probes are in scope:
    repair `lltfontfeatures`, `lltfontfallbacks`, `lltpaperstyleminimal`, and the
    documented `lltparagraphs` preload path, or document any unsupported order in
    the same commit.
V6. `accepted-current` — Remove README wording that presents `lltpaperstyleminimal`
    as a `lltpaperstyle` option; keep the existing separate-package note as the
    supported contract.
V7. `accepted-current` — Align `paper/modules/README.md` standalone claims with the
    repaired probe set and table-listed support rather than leaving blanket support
    claims.
V8. `accepted-current` — Add the missing main-package `minimal` option probe beside
    the separate `lltpaperstyleminimal` package probe.
V9. `accepted-current` — The out-of-scope `.claude/commands/` metadata must not ship
    silently in the lane branch; the re-implementation preflight must remove or move
    it off the branch before PR, or block for explicit user direction.
V10. `accepted-current` — Fold the advisory probe-harness, natbib comment, and
     remaining alias cleanup into the V3/V5 re-implementation so reruns expose the
     complete compatibility failure set.

### 2026-07-02 review-diff-vs-plan (Verifier, pass 2)

W1. `accepted-current` — Document the supported optional-module load order for
    `lltparagraphs`: load optional modules before `lltpaperstyle`; loading
    `lltparagraphs` after `lltpaperstyle` is unsupported unless the reverse order
    is fully guarded.
W2. `accepted-current` — Extend the 2026-07-02 `CHANGELOG.md` entry so it records
    the material package-side compatibility fixes from the second implementation
    commit, including lazy `inputenc`, `\doiprefix`, preload shims,
    `lltfontfallbacks`, `lltfontfeatures`, and `lltpaperstyleminimal`.
W3. `accepted-current` — Fix compatibility-probe auxiliary cleanup so temporary
    probes do not leave root-level `.aux`, `.log`, `.out`, `.bcf`, or `.run.xml`
    files after `tests/run-tests.sh`.
W4. `accepted-current` — Fold the stale natbib `\cite` comment and the
    `nobiblatex`/manual-biblatex loading-order note into the W1-W3
    re-implementation pass.

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
- Status returned from `Needs Review Resolution` to `Frozen` because all
  post-review verifier findings were routed `accepted-current`.
- Re-implementation scope now explicitly includes the TeX Live 2025 natbib
  `\doiprefix` failure, manual-`biblatex` input/loading-order warning, failing
  standalone/preload module probes, invalid minimal-option documentation, blanket
  standalone-module README claims, and the missing main-package `minimal` option
  probe.
- The compatibility harness plan now requires full failure-set reporting rather
  than aborting at the first failed probe.
- The branch-footprint preflight now requires the out-of-scope dot-claude command
  metadata to be removed or moved off the lane branch, without expanding the lane
  scope allowlist or silently shipping unrelated files.
- Status advanced from `Blocked` to `Implemented` after planned verification
  passed and the implementation was committed.
- Scope was expanded to the existing
  `tests/fixtures/biblatex-manual-contract.tex` fixture so the manual-`biblatex`
  warning-free contract matches the documented supported loading order.
- The out-of-scope `.claude/commands/` files were removed from the lane branch in
  commit `6e11333`, resolving the V9 branch-footprint blocker without expanding
  Lane 2 scope.
- Status returned from `Needs Review Resolution` to `Frozen` because the pass-2
  verifier findings W1-W4 were routed `accepted-current`.
- Re-implementation scope now includes explicit README/docs wording for optional
  module load order, expanded CHANGELOG coverage for the second package-side fix
  commit, root-level auxiliary cleanup for temp compatibility probes, and cleanup
  of the stale natbib `\cite` comment / manual-biblatex loading-order note.
- Status advanced from `Implemented` to `Reviewed` after the pass-3 verifier
  confirmed W1-W4 fixed, found no material findings (X1 is advisory only), and
  independently reran the full planned verification green.
