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

**Eight of them are now closed**, all merged to `main`: #49 (delete `.dtx`/`.ins`),
#46 (rename to `lanepaper`, prefix `\lnp@`), #47 (package-first layout), #53 (LPPL
headers), #54 (engine guard), #61 (#57 partial + #35 Poppler), #45
(`CONVENTIONS.md`), and #57 (closed once `CONVENTIONS.md` carried the ChkTeX
policy). The code says `lanepaper`, the layout is `lanepaper/` + `demo/`, and
`CONVENTIONS.md` at the root is now the authority on how package code is written.

Remaining: **#48** dependencies, **#50** l3build, **#51** makefile, **#52** docs,
**#55** robustness, **#56** hooks, plus #29 and #42.

Next: #48. It is the top of the remaining spine, it unblocks #56, it absorbs #42,
and doing it before #52 means the docs consolidation describes the final
dependency set rather than one #48 immediately invalidates.

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
- **`grep -c` counts lines, not registrations.** `\AtBeginDocument` matches 11
  lines in `lanepaper/` but only **8** are registrations; three are comments.
  A reviewer caught this in a document whose entire value was that its counts
  were true. Filter comments before quoting a count.
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
- **`make build` will hand you a stale `main.pdf`.** It reports "All targets are
  up-to-date" and leaves the old file in place. Raster-comparing against that
  showed 9 of 40 pages differing for a change that touches no package code;
  rebuilding both sides after `make clean` showed 0, byte-identical. **Build
  both sides from clean before comparing**, every time.
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
- **GitHub parses a closing keyword against the first issue number only.**
  `Closes #49, #46, #47, #53` closed only #49. Write `closes` before each number,
  or close the rest by hand.
- **A Herdr pane keeps roughly 24 lines of scrollback.** A long reviewer result
  is unrecoverable once it scrolls; `--source recent-unwrapped --lines N` does
  not reach further back. Ask the reviewer for a compact re-emit, or brief it to
  answer in few lines from the start.
- **`herdr agent prompt` with a multi-line body lands as an unsent paste.** The
  pane shows `[Pasted text #N]` and nothing runs until `herdr agent send-keys
  <pane> enter`. Single-line prompts submit normally. Stray suggestion text also
  appears in the input box and does not clear with `esc` or backspace — it is
  rendered, not buffered; ignore it rather than fighting it.
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

`main` at `05831b5`, clean, in sync, CI green. No worktrees or agent panes left
over.

```
05831b5  docs: supersede PACKAGE_ROADMAP.md, add ADR-0001 erratum (#63)
1c08e0b  Add CONVENTIONS.md for package code in lanepaper/ (#62)
3fb556d  Delete gitignored BACKLOG.md, add issue template, record Poppler setup (#61)
14e1e32  feat: add an engine guard, fail clearly on non-pdfTeX engines (#54) (#60)
e5fdfdc  Package-first: rename to lanepaper, flatten layout, add LPPL headers (#59)
```

Local gates: **pytest 41 passed, 0 skipped**, **`tests/run-tests.sh` 115 passed /
0 failed**, `make build` clean, style validator clean (31 warnings, unchanged
baseline).

Open issues: #29, #42, #48, #50, #51, #52, #55, #56.

Deliberately not done, with reasons:

- `docs/PACKAGE_ROADMAP.md` is **superseded-bannered, not deleted**. ADR-0002
  cites its T-402 item in order to withdraw it, so deleting the file would leave
  an accepted ADR pointing at nothing. #52 owns the deletion and must fix
  ADR-0002's reference at the same time. The file is worse than stale: its
  Vision describes East-Asian typesetting and its checklist proposes an `\east@`
  namespace — it was imported from another project.
- ADR-0001 says "the four competing internal prefixes" and names four. Five were
  retired; `\paperstyle@` is missing from its list. The ADR carries a dated
  erratum and the original sentence is left intact, because an accepted ADR
  records what was decided rather than describing current code.
- #49's literal criterion "no remaining references to `.dtx`" was not satisfied;
  doing so would mean editing LPPL boilerplate and dated review records.
  Documented in `CHANGELOG.md`.

## Next Move

**#48, the configure-if-loaded dependency policy** (ADR-0003). Top of the
remaining spine, unblocks #56, absorbs #42, and must precede #52 so the docs
consolidation describes the final dependency set.

Measured 2026-08-24: **45 distinct third-party packages** are loaded, not the
~37 ADR-0003 estimated. All five of its "delete outright" packages are still
loaded — `longtable`, `tabularx`, `rotating`, `pdflscape`, `adjustbox`.

This is the first genuinely behaviour-changing item since #46; everything since
has been renames and documents. It removes packages and moves `hyperref` and
`cleveref` to `\@ifpackageloaded`, so it needs full raster proof on both
`main.tex` and `tests/fixtures/opening-test.tex`, and the demo may break where it
uses `\begin{landscape}`, `\begin{sideways}`, or `\adjustbox`.

Then the rest:

```
#48 dependencies ── #56 hooks
#50 l3build ── #51 makefile
#52 docs
```

- **#55 robustness** is independent and is the last heavy package-code item. Its
  body was corrected on 2026-08-24: both `\DeclareRobustCommand` uses are on
  *internal* macros, so **no public macro is robust at all**, and the count is
  ~315 prefix-free `\newcommand`, not ~500.
- **CTAN** has no date and that is deliberate (ADR-0001). The readiness work is
  #52; #53 is done. Submission is one `l3build upload` after.
- Optional: `actions/checkout@v4` and `upload-artifact@v4` emit a Node 20
  deprecation annotation every run. Harmless, noisy.

### Unowned by any ticket

- **Public macro names carry no prefix** — `\tightlists`, `\centeredpar`, `\dialogue`,
  `\forceindent`. That is the documented convention and predates ADR-0001, but it is
  weak on CTAN, where a shared texmf tree makes collisions real. #55 is robustness, not
  namespacing. Noted as a known gap in `docs/package/NAMESPACE_CONVENTIONS.md`.
- **`\lanepaperinfo` is defined in `lanepaper/lanepaper.sty` and called nowhere.**
- **`docs/PACKAGE_ROADMAP.md` calls itself "the single source of truth"** while ADR-0002
  explicitly withdraws its T-402. That contradiction belongs to #52.

## Relevant Files

- `CONVENTIONS.md` — **read this first before touching `lanepaper/`.** How package
  code is written, and it marks which of its own rules the code does not yet
  follow (robustness #55, hooks #56, dependencies #48). Every count in it was
  measured; re-measure rather than copying one out.
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
- `.gitignore` — the two negations are asymmetric on purpose. Its `BACKLOG.md`
  entry is gone (#57).

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
