---
title: Public Release Prep
date: 2026-08-19
updated: 2026-08-24
type: handoff
topic: public-release-prep
---

## Objective

Get `lane_latex_template` to publicly releasable. `v2.1.0` is tagged and published as
latest.

The plan changed on 2026-08-22. A design review reframed the project from "work through
a punch-list of issues" to "split the package from the template, then release the
package." The decisions are recorded in `docs/adr/0001`–`0003` and `CONTEXT.md`; the
work is issues #46–#57.

**Four of them are now built** on branch `refactor/rename-lanepaper-46`: #49 (delete
`.dtx`/`.ins`), #46 (rename to `lanepaper`, prefix `\lnp@`), #47 (package-first layout),
#53 (LPPL headers). The code says `lanepaper` and the layout is `lanepaper/` + `demo/`.

**None of it is pushed.** `main` is still at `d075ceb`, `origin` has only `main`, and all
four issues still read as open on GitHub. Shipping that branch is the first move.

## Important Details

Hard-won facts. Most cost a failed run or a review round to learn.

### The ADRs describe the target, not the code

`docs/adr/` was written aspirationally at `d075ceb`. #46, #47, #49 and #53 have since
closed the gap; #48, #50, #51, #52, #54, #55, #56, #57 have not. Check the issue before
assuming a decision has landed.

- **#42 overlaps #48 and should not be done first.** #42 asks for a full
  `\RequirePackage` audit of `src/sh/check-packages.sh`; #48 changes which packages are
  required at all (~37 loads down to ~25). Auditing against the current list is work
  that #48 discards. Either close #42 into #48 or sequence it after.
- **#52 conflicts with a prior instruction below.** The older note says
  `production-grade` survives under `docs/` on purpose (archival). #52 deletes ~30 stale
  docs including `docs/archive/`. #52 is the newer decision and wins, but the archival
  intent was deliberate once — confirm before deleting rather than assuming.
- **#45 (CONVENTIONS.md) is partly superseded.** See the comment on the issue: it must
  now say `lanepaper` and `\lnp@`, carry the configure-if-loaded rule from ADR-0003, and
  link ADR-0002 rather than restating the l3build rejection.
- **#54 and #55 cite line numbers that have moved.** #46/#47/#53 removed 137
  `\makeatletter`/`\makeatother` lines and added a 16-line header to every file.
  `\NeedsTeXFormat` is at `lanepaper/lnpminimal.sty:24`, not `lltpaperstyleminimal.sty:8`.
  Re-locate #55's `2943-2948` anchor in `lanepaper/lanepaper.sty` (3152 lines) rather
  than trusting it.

### Traps found while renaming — these will bite again

- **A `.sty` has `@` as a letter by construction, so `\makeatother` inside one revokes
  it for the rest of the file.** The old prefixes had no `@`, so 137 stray
  `\makeatletter`/`\makeatother` lines sat harmless for a year. The moment names became
  `\lnp@*`, the build died with `Command \lnp already defined`. All 137 were removed
  (pairs verified balanced, no literal `@` needed "other" catcode); `lnplists.sty` also
  had an unbalanced extra `\makeatletter`. Do not reintroduce them.
- **`\@ifundefined{name}` takes a name WITHOUT a backslash**, so a macro-name sweep
  driven by `\`-prefixed patterns silently skips it. Two sites survived the rename
  testing the old name while defining the new one — a double `\newif` on reload. Grep
  `\@ifundefined` separately after any rename.
- **biber is PAR-packed and macOS temp purges corrupt its cache.** Presents as
  `test_manual_biblatex_contract_passes` failing with exit 2 and an *empty* error log;
  the real cause is `Unicode::UCD: failed to find unicore/version`. Fix: delete the
  ~153MB `/var/folders/.../T/par-*` cache and let biber re-extract. This is not a
  regression in the repo and will recur.
- **`compare -metric AE` prints `0 (0)`, not `0`.** String-matching the whole output
  reports every page as differing. Take the first field only.

### Build and test truths

- **The engine is pdflatex, not LuaLaTeX.** `Makefile:7` pins it, `tests/run-tests.sh`
  calls it directly, `.latexmkrc` sets no engine, and there is no `fontspec` anywhere.
  A brief asserting LuaLaTeX was wrong and a worker correctly overrode it. There is
  still no engine *guard* in the source — that is #54, and nothing in `lanepaper/`
  loads `iftex` today.
- **Do not delete the "Mark workspace safe for git" step in `ci.yml`** (`ci.yml:39-41`).
  It looks redundant with `actions/checkout`, which does handle `safe.directory` — but
  only within its own step. Later steps still need it. Without it
  `tests/test_infrastructure.py` fails with `git ls-files` exit 128 (dubious ownership).
  This was a real red CI run.
- **`make check` and `make check-deps` are different and the difference matters.**
  `make check` (`Makefile:183`) uses a hardcoded Makefile list; `make check-deps`
  (`Makefile:226`) runs `src/sh/check-packages.sh`, which CI uses. Both are in scope for
  #51's Makefile cut.
- **`TEXINPUTS`/`BIBINPUTS` in the Makefile are what kept #47 invisible to CI.**
  `./lanepaper:./demo` on the path means documents `\input{preamble.tex}` bare and
  `main.pdf` still lands at the repository root. Anything that hardcodes a directory
  instead of relying on this will break the next time files move.
- **The lettrine `*** ATTENTION REQUIRED ***` warning is positional, not a defect.**
  It fires when remaining page space is less than the drop cap's depth
  (`lettrine.sty:317`). Allowlisting it would blind the harness to all future lettrine
  warnings; lettrine's `nextpage` option changes rendered output, which `AGENTS.md`
  rule 1 forbids.
- **`tests/visual/output/*.pdf` are generated, not baselines.** Regenerated by every
  `tests/run-tests.sh` run. `!demo/figures/*.pdf` in `.gitignore` is different and is
  load-bearing — `README.md` tells adopters to put real figure assets there.
- **`lnphochuli` is not loaded by the default build.** Of its refinements only the
  Pagella kerning pairs and `\parfillskip` apply on load; the rest are opt-in commands
  invoked nowhere. A README bullet claiming otherwise was caught as a false front-page
  claim. Preserve that distinction in any future wording.

### Proving that rendering did not change — read this before touching the `.sty` files

This cost three review rounds on #39, and every remaining ticket that touches typography
depends on it.

- **`pdftotext` comparison is not a rendering proof.** It reported byte-identical text
  while a page had visibly reflowed. Text extraction cannot see reflow.
- **PDF byte comparison is meaningless.** Rebuilding unchanged source yields a different
  hash every time via the embedded timestamp.
- **Raster comparison is the proof that works**, but only over documents that actually
  exercise the changed code. Per-page `pdftoppm -r 150 -png` plus per-page
  `compare -metric AE`. Fail loudly on any page-count change.
- **`main.tex` alone is not sufficient coverage.** It never exercises `\firstlinesc`;
  that path regressed and 40 pages of clean raster comparison did not notice. Render
  `tests/fixtures/opening-test.tex` too when touching small-caps or tracking.
- **Rebuild both sides the same day.** `\today` on the title page otherwise shows up as
  a real-looking diff. This wasted a cycle.
- **Read every differing page, do not tally them.** The #46–#53 baseline ends at 4
  differing pages of 40, all accounted for: the `\today` line, two pages where the demo
  prints its own `\usepackage{...}` listing, and one citing a renamed doc path.

### microtype tracking — the mental model

- **`\SetTracking` is global and order-sensitive.** `\lsstyle` selects the tracked font
  immediately; `\SetTracking` only registers a list for *later* selections. Code that
  runs `\lsstyle` before `\SetTracking{...}{N}` never applies N. Of 27 executable sites
  audited, 26 ordered it correctly and only `\spacedfirsline` was reversed — which made
  "restoring" its N a regression, not a fix.
- **microtype has no point-of-use named-list selection.** `name` and `load` declare and
  inherit lists (§5.2–5.3); there is no way to pick one inside a macro. The original #39
  plan assumed otherwise and was impossible. `\textls[N]{...}` (§7) is the working API.
- **microtype matches sizes exactly.** An explicit `\fontsize{11}` matches no named-size
  list, because `\normalsize` and `\large` are 10.95pt and 12pt in an 11pt class. That
  is why a handful of amounts were genuinely effective while most were inert.
- **Every tracking list in the repo declares `T1` only.** `lnpfontfeatures.sty` exposes
  OT1 deliberately, so amounts there were effective too.

### Tooling

- **`gh-axi` IS available via `npx -y gh-axi`** — the earlier note that it was not
  installed is wrong. Two gotchas: `--repo` must come *after* the subcommand, and
  `issue close --reason` takes `"not planned"` with a space, not `not_planned`.
- **`/grill-with-docs` and `/to-tickets` cannot be invoked by the agent** — both set
  `disable-model-invocation: true`. The user must type them. `grilling` and
  `domain-modeling` are model-invocable and are what `/grill-with-docs` calls.
- **`l3build` is already installed** (`/usr/local/texlive/2025/bin/universal-darwin/l3build`)
  and is present in the CI container, since it ships with TeX Live. No new dependency
  for #50.
- **`TEXMFHOME` here is `/Users/nathanlane/Library/texmf`**, not `~/texmf`, which does
  not exist. That is where `l3build install` will write.

### Process notes for a foreman-style session

- **Reviewers are not a substitute for running CI**, and independent review is not
  optional theatre — it rejected substantive work three times, including two claims the
  coordinator had already verified and believed.
- `close-worker.sh` must run **before** the worktree is removed, or its receipt no
  longer validates.
- `start-worker.sh` refuses a `--cwd` in a different git worktree unless it is *invoked
  from inside* that worktree. Run it via `(cd <worktree> && start-worker.sh ...)`.
- The OpenCode/kimi reviewer profile **wedges**: it repeatedly tries to spawn sub-agents
  and shell probes its own profile denies, then stops responding to `esc` and `ctrl+c`.
  Record `harness_crash` and let the selector advance. The codex-sol reviewer worked
  reliably every time.
- The inline surface **cannot bind non-Claude models**. A selected
  `codex-sol-inline-reviewer` is unlaunchable here; record `startup_failure` and take
  the herdr variant.
- **Do not judge agent liveness by screen content** — an animated progress bar makes a
  wedged agent look busy. Compare `revision` and `state_change_seq` from
  `herdr agent get` instead.
- Successive right-splits produce unusable ~20-column panes. Split `down` from a wide
  pane; close finished panes to reclaim geometry.
- **Keep `CHANGELOG.md` coordinator-owned** when two leaves run in parallel — it is the
  one file every leaf wants. Even so, two branches touching `## Unreleased` conflict at
  merge time; resolve by keeping both sections.

## Work State

Branch `refactor/rename-lanepaper-46`, 4 commits ahead of `main`, **no upstream and not
pushed**. `main` is at `d075ceb`; `origin` carries only `main`. No worktrees or agent
panes left over.

```
b61011e  feat: add LPPL 1.3c headers to all 16 package files (#53)
3fcc860  refactor: move to package-first layout (#47)
6714bc3  refactor: rename package to lanepaper, unify internal prefix to \lnp@ (#46)
9a334a3  chore: delete the stale .dtx/.ins scaffold (#49)
```

Local gates on that branch: **pytest 32 passed**, **`tests/run-tests.sh` 115 passed /
0 failed**, style validator clean, raster comparison accounted for (see above).

Open issues: #29, #35, #42, #45, #48, #50, #51, #52, #54, #55, #56, #57 — plus #46, #47,
#49 and #53, which are done locally and stay open until the PR merges.

**Correction to a previous pass of this file: #29 is open, not closed.** #34 is
genuinely closed (2026-08-21, won't-fix until CTAN — Overleaf has no supported path
until then, and ADR-0001's vendored-subtree approach replaces the resolution check the
issue asked for).

Deliberately excluded from #49: its acceptance criterion said "no remaining references
to `.dtx`". Satisfying that literally would mean editing LPPL boilerplate in `LICENSE`
and rewriting dated review records. The exclusion is documented in `CHANGELOG.md`.

## Next Move

1. **Ship the branch.** Push, open a PR against `main`, merge. It closes #46, #47, #49
   and #53. Repo template is `.github/pull_request_template.md` (`## Summary` /
   `## Test plan`).
2. **#54 engine guard** — small and self-contained. `\RequirePackage{iftex}` plus
   `\RequirePDFTeX` (or a `\PackageError` on non-pdfTeX), `\NeedsTeXFormat{LaTeX2e}` on
   the main package, pdfLaTeX-only stated in `README.md` and `INSTALL.md`, a test
   asserting the guard fires, CHANGELOG entry.
3. **#55 robustness** — the large one. 2 of ~500 user-facing macros are
   `\DeclareRobustCommand`. Wants the hand-rolled PDF-safe workaround removed and tests
   for a macro in `\section`, `\caption`, and a PDF bookmark.
4. Then the remaining spine:

```
#48 dependencies ── #56 hooks
#50 l3build ── #51 makefile
#52 docs
```

- **#45** needs rewriting against the ADRs before it is worked — see the issue comment.
- **#35** remains mostly done: local Poppler installed, CI half shipped in #40, PDF-text
  assertions running. Remaining is a `tests/check-spacing-integrity.sh` review
  (advisory, low value) and a README toolchain note. **The issue body still reads as
  unstarted and is misleading — fix it.**
- **CTAN has no date** and that is deliberate (ADR-0001). Do not file a CTAN issue; the
  readiness work is #52 (#53 is done), and submission is one `l3build upload` after.
- Optional: `actions/checkout@v4` and `upload-artifact@v4` emit a Node 20 deprecation
  annotation every run. Harmless, noisy.

### Unowned by any ticket

- **Public macro names carry no prefix** — `\tightlists`, `\centeredpar`, `\dialogue`,
  `\forceindent`. That is the documented convention and predates ADR-0001, but it is
  weak on CTAN, where a shared texmf tree makes collisions real. #55 is robustness, not
  namespacing. Noted as a known gap in `docs/package/NAMESPACE_CONVENTIONS.md`.
- **`\lanepaperinfo` is defined in `lanepaper/lanepaper.sty` and called nowhere.**
- **`docs/PACKAGE_ROADMAP.md` calls itself "the single source of truth"** while ADR-0002
  explicitly withdraws its T-402. That contradiction belongs to #52.

## Relevant Files

- `docs/adr/0001`–`0003` and `CONTEXT.md` — the decisions and the glossary. Read before
  touching anything; `CONTEXT.md` fixes Package / Template / Demo so the issues read
  unambiguously.
- `lanepaper/lanepaper.sty` — 3152 lines, the main package. #54 adds the engine guard
  here; #55's main audit target. Its convenience wrappers (`landscape`, `sideways`,
  `adjustbox`) are what #48 moves out — re-locate them, the old 2527–2590 anchor moved.
- `lanepaper/lnpminimal.sty` — holds the only `\NeedsTeXFormat` in the package
  (line 24); the pattern #54 mirrors.
- `lanepaper/lnpmicrotype.sty` — tracking lists from line 88 are the reference for
  whether any amount is effective.
- `tests/test_infrastructure.py` — carries two guards worth knowing: retired package
  names must not appear in active build inputs, and every `lanepaper/*.sty` must carry
  its LPPL header. Both are written to avoid matching their own source.
- `src/sh/check-packages.sh` — #42's target and #48's output; incomplete either way.
- `src/sh/validate_latex_style.sh` — the math-spacing check is a depth-tracking perl
  scan; `tests/test_infrastructure.py` covers it in four directions. Do not "simplify"
  it back to a bracket expression.
- `tests/fixtures/opening-test.tex` — the only document exercising `\firstlinesc`;
  required for any rendering proof touching tracking.
- `README.md` features list — carries a guardrail comment limiting claims to verified
  support. Two separate sessions have now violated it; check claims against the `.sty`
  files, never against existing prose.
- `.gitignore` — the two negations are asymmetric on purpose. #57 removes its
  `BACKLOG.md` entry.

## Suggested Skills

- `foreman` — for running the rest of the queue. Merge mode and reviewer routing must be
  re-selected per invocation; permission does not carry over. Route reviewers to
  codex-sol and skip kimi (see wedging note). The remaining work is more parallel than
  #46–#53 was, since the #46 → #47 spine is now behind us.
- `gh-axi` — issue and PR work. Available via `npx -y gh-axi`; see the tooling gotchas
  above.
- `pr-body` — this repo has `.github/pull_request_template.md` (`## Summary` /
  `## Test plan`) but no `scripts/check_pr_body.py`, so the skill's validation step is a
  no-op here and its three-section format does not match the template. Follow the repo
  template.
