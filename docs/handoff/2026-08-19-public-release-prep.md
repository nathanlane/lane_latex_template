---
title: Public Release Prep
date: 2026-08-19
updated: 2026-08-25
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

**Eleven are now closed**, all merged to `main`: #45, #46, #47, #48, #49, #53,
#54, #56, #57, plus #35 and #42. The package is `lanepaper`, the layout is
`lanepaper/` + `demo/`, and `CONVENTIONS.md` at the root is the authority on how
package code is written — it marks which of its own rules the code does not yet
follow.

**Remaining: #50 l3build, #51 makefile, #52 docs, #55 robustness, #29 microtype.**

Next: **#50**. Additive, unblocks #51, nothing existing changes. For CTAN the path
is #52 then #50 — ADR-0001 says submission is one `l3build upload` after those.
#55 is the last heavy package-code item.

## Important Details

Hard-won facts. Most cost a failed run or a review round to learn.

### The ADRs are now mostly built

`docs/adr/0001`–`0003` were aspirational at `d075ceb`. #46, #47, #48 and #56 have
closed the gap; #50, #51, #52 and #55 have not. Two ADR statements are now known
wrong and are corrected in place rather than rewritten:

- **ADR-0001 says "the four competing internal prefixes" and names four.** Five
  were retired — it omits `\paperstyle@`. It carries a dated erratum; the original
  sentence is deliberately left as written, because an accepted ADR records what
  was decided, not what the code is.
- **ADR-0003 says `longtable` and `tabularx` are "used zero times"** and slates
  them for deletion. False: the package sets `\LTcapwidth` and hooks
  `\lnp@tablecaptionsetup` onto the longtable environment, and `\LTcapwidth` is
  longtable's *own* length — an unguarded `\setlength` is an undefined control
  sequence. #48 treated them as configure-if-loaded instead, with the
  maintainer's agreement.

**#52 conflicts with an older instruction.** An earlier note said `production-grade`
survives under `docs/` on purpose (archival). #52 deletes ~30 stale docs including
`docs/archive/`. #52 is newer and wins, but confirm before deleting.

**`docs/PACKAGE_ROADMAP.md` is bannered SUPERSEDED, not deleted.** ADR-0002 cites
its T-402 item in order to withdraw it, so deleting the file would leave an accepted
ADR pointing at nothing. **#52 owns the deletion and must fix ADR-0002's reference
in the same change.** The file is worse than stale — its Vision describes East-Asian
typesetting and its checklist proposes an `\east@` namespace; it was imported from
another project.

### Traps that cost real debugging — these will bite again

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
- **`\AtBeginDocument` decides precedence by registration order**, which makes it
  an accident of file layout. Deferring the cleveref block in #48 inverted a
  `\crefname` precedence that had held for a year: an appendix range rendered
  "§§ 1–2" instead of "appendices 1–2". Rendered output changed and no test
  noticed — only raster comparison did. #56 removed the whole class by moving to
  package hooks; `\AtBeginDocument` is now banned and guarded by a test.
- **A command the optional package owns is a fatal error, not "less styling".**
  `\startappendices` called `\phantomsection` (hyperref's), always defined while
  the package loaded hyperref. Once #48 stopped, a bare document died on it.
  `\providecommand` it.
- **Dropping `babel` changes line breaking.** The measured `\spaceskip` values
  were tuned with babel present, so without it all five pages of
  `tests/fixtures/opening-test.tex` re-break. Neutral given the same package set;
  a bare document's typography does move.
- **`grep -c` counts lines, not registrations.** `\AtBeginDocument` matched 11
  lines when only 8 were real; three were comments. A reviewer caught that in a
  document whose whole value was that its counts were true.
- **`compare -metric AE` prints `0 (0)`, not `0`.** String-matching the whole output
  reports every page as differing. Take the first field only.

### Build and test truths

- **The engine is pdflatex, not LuaLaTeX**, and since #54 both entry points stop
  with one `\PackageError` on anything else. `iftex`'s own `\RequirePDFTeX` was not
  used: it does not name the package that wanted pdfTeX. The guard hard-stops
  (`\batchmode\@@end`) because `\PackageError` alone is recoverable and a
  `nonstopmode` build walks straight into the cascade it exists to prevent.
- **Do not delete the "Mark workspace safe for git" step in `ci.yml`** (`ci.yml:39-41`).
  It looks redundant with `actions/checkout`, which does handle `safe.directory` — but
  only within its own step. Later steps still need it. Without it
  `tests/test_infrastructure.py` fails with `git ls-files` exit 128 (dubious ownership).
  This was a real red CI run.
- **`make check` and `make check-deps` are different and the difference matters.**
  `make check` uses a hardcoded Makefile list; `make check-deps` runs
  `src/sh/check-packages.sh`, which CI uses. Both are in scope for #51's cut.
  `check-packages.sh` is now **generated from the source** — regenerate it rather
  than hand-editing, and use a pattern that matches hyphens and comma-separated
  groups. Mine did not, and silently dropped `eso-pic` and mangled
  `amsmath,amssymb` until review caught it.
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
- **A Herdr pane keeps ~24 lines of scrollback.** A long reviewer result is
  unrecoverable once it scrolls, and `--source recent-unwrapped --lines N` does
  not reach further back. Brief reviewers to answer in few lines, or ask for a
  compact re-emit.
- **`herdr agent prompt` with a multi-line body lands as an unsent paste.** The
  pane shows `[Pasted text #N]` and nothing runs until
  `herdr agent send-keys <pane> enter`. Single-line prompts submit normally.
  Stray suggestion text also appears in the input box and clears with neither
  `esc` nor backspace — it is rendered, not buffered. Ignore it; never act on it,
  and note that it sometimes reads like an instruction ("merge the branch").
- **The selector routes `bounded-substantive` and `complex-high-risk` to the kimi
  profile**, which this repo has recorded as wedging. Record `harness_crash` for
  `kimi-herdr-reviewer` in `failed_attempts` and it advances to
  `claude-opus-herdr-reviewer`. `codex-sol-inline-reviewer` still cannot bind on
  the inline surface — record `startup_failure`.
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
- **Commit before mutation-testing a guard.** Twice this session `git checkout
  <file>` — used to undo a deliberate break — silently discarded uncommitted work
  on that file. Stage the work first, then break it, then `git checkout`.
- **GitHub parses a closing keyword against the first issue number only.**
  `Closes #49, #46, #47, #53` closed exactly one issue. Write `closes` before
  each number.
- **Verify a raster baseline was built the same day.** `make build` reports
  "up-to-date" and will serve a stale `main.pdf`; that produced 9 phantom
  differing pages once, and a date rollover produced a 1-page `\today` diff
  another time. Rebuild both sides from clean, same day, before comparing.
- **Keep `CHANGELOG.md` coordinator-owned** when two leaves run in parallel — it is the
  one file every leaf wants. Even so, two branches touching `## Unreleased` conflict at
  merge time; resolve by keeping both sections.

## Work State

`main` at `ebaa106`, clean, in sync, CI green. No worktrees or agent panes left over.

Local gates: **pytest 46 passed, 0 skipped**, **`tests/run-tests.sh` 115 passed /
0 failed**, `make build` and `make check-deps` clean, style validator clean
(32 warnings — 31 was the pre-#48 baseline; the extra is a prose advisory on
`demo/landscape.tex`, which the validator can see now that it is a `.tex`).

Open: **#29, #50, #51, #52, #55.**

Merged this session, newest first: #66 (#56 hooks), #65 (#48 dependencies),
#64 (handoff), #63 (roadmap banner + ADR erratum), #62 (#45 CONVENTIONS.md),
#61 (#57 partial + #35), #60 (#54 engine guard), #59 (#46/#47/#49/#53).

**#48 was a breaking change.** `\usepackage{lanepaper}` alone no longer gives a
bibliography, links, or cross-references. Third-party loads went 45 → 33. The
package imposes **no load order at all**. `demo/preamble.tex` shows exactly what
a document must load, carrying the biblatex option set the package used to
impose. `[natbib]` and `[nobiblatex]` are deprecated and inert — still declared
so existing documents warn rather than fail on an unknown option.

Deliberately not done, with reasons:

- **#57 was closed only after #45 landed** — its last criterion needed
  `CONVENTIONS.md` to exist.
- **#49's literal criterion "no remaining references to `.dtx`" was not met.**
  Satisfying it meant editing LPPL boilerplate and dated review records.
  Documented in `CHANGELOG.md`.
- **The cleveref convenience wrappers (`\refpage`, `\pref`, `\seeref`) call
  `\cref` unguarded, deliberately.** They are wrappers over cleveref; calling one
  without it is a usage error, not a trap. A `\providecommand` fallback would emit
  a reference pointing nowhere, which is worse than the error. Reasoning is in
  `CONVENTIONS.md` §9.

## Next Move

**#50, l3build for packaging and release.** Additive — nothing existing changes —
and it unblocks #51. `l3build` is already installed and ships with TeX Live, so
there is no new dependency. ADR-0002 governs: l3build for packaging only, pytest
stays the test harness; do not let it pull the test suite along.

Then:

```
#50 l3build ── #51 makefile
#52 docs
#55 robustness   (independent)
```

- **#52 is the CTAN gate.** ADR-0001: submission is one `l3build upload` after #52
  and #50. It owns deleting `docs/PACKAGE_ROADMAP.md` **and** fixing ADR-0002's
  reference to it in the same change. Note #45 already did part of #52's work by
  absorbing both naming docs into `CONVENTIONS.md`.
- **#55 is the last heavy package-code item.** Its body was corrected on
  2026-08-24: both `\DeclareRobustCommand` uses are on *internal* macros, so **no
  public macro is robust at all**, and the count is ~315 prefix-free
  `\newcommand`, not ~500. When it lands, `CONVENTIONS.md` §8's "not met" heading
  comes off.
- **#29** (microtype `verbose=silent`) is untouched and unscheduled.
- **CTAN has no date** and that is deliberate (ADR-0001).
- Optional: `actions/checkout@v4` and `upload-artifact@v4` emit a Node 20
  deprecation annotation every run. Harmless, noisy.

### Unowned by any ticket

- **Public macro names carry no prefix** — `\tightlists`, `\centeredpar`, `\dialogue`,
  `\forceindent`. That is the documented convention and predates ADR-0001, but it is
  weak on CTAN, where a shared texmf tree makes collisions real. #55 is robustness, not
  namespacing. Recorded as a known gap in `CONVENTIONS.md` §4.
- **`\lanepaperinfo` is defined in `lanepaper/lanepaper.sty` and called nowhere.**
- **`lnpgridoverlay` is an entry point but carries no engine guard.** #54 guarded
  `lanepaper` and `lnpminimal`, the two surfaces README documents. Loading
  `lnpgridoverlay` bare on XeLaTeX gets no clear message.

## Relevant Files

- `CONVENTIONS.md` — **read this first before touching `lanepaper/`.** How package
  code is written. §8 robustness is still marked **not met** (#55); §9 hooks and
  dependencies are now met. Every count in it was measured — re-measure rather
  than copying one out, and note §9's count moved twice in one day.
- `docs/adr/0001`–`0003` and `CONTEXT.md` — the decisions and the glossary.
  `CONTEXT.md` fixes Package / Template / Demo so the issues read unambiguously.
  Two ADR statements are wrong; see the erratum notes above.
- `lanepaper/lanepaper.sty` — 3076 lines, the main package and #55's audit
  target. Its `\AddToHook{package/*/after}` blocks are where all
  configure-if-loaded styling lives.
- `demo/preamble.tex` — the worked example of what a document must now load, and
  the reference for the biblatex options the package used to impose.
- `demo/landscape.tex` — the landscape/rotation family, moved out by #48. It
  belongs to the Template once ADR-0001's separate repository exists.
- `tests/test_infrastructure.py` — five guards: retired package names, LPPL
  headers, no `\AtBeginDocument`, the five package hooks, and the format floor.
  Each is written to avoid matching its own source.
- `tests/test_option_contracts.py` — encodes the post-#48 bibliography contract
  and the bare-document regression guard.
- `src/sh/check-packages.sh` — **generated**, not hand-maintained. Regenerate from
  the source.
- `src/sh/validate_latex_style.sh` — the math-spacing check is a depth-tracking perl
  scan; `tests/test_infrastructure.py` covers it in four directions. Do not "simplify"
  it back to a bracket expression.
- `tests/fixtures/opening-test.tex` — the only document exercising `\firstlinesc`;
  required for any rendering proof touching tracking. It loads `babel` explicitly
  since #48 — do not remove that.
- `README.md` features list — carries a guardrail comment limiting claims to verified
  support. Two separate sessions have violated it; check claims against the `.sty`
  files, never against existing prose.

## Suggested Skills

- `foreman` — for the rest of the queue. **Merge mode is re-selected per invocation
  and permission does not carry over**; a named queue does not authorize merging a
  different issue. Reviewer routing: record `startup_failure` for
  `codex-sol-inline-reviewer` and `harness_crash` for `kimi-herdr-reviewer` in
  `failed_attempts` to reach `claude-opus-herdr-reviewer`, which worked every time.
  The remaining work is genuinely parallel — #52, #55 and #50 touch different files.
- `gh-axi` — issue and PR work. Available via `npx -y gh-axi`; see the tooling gotchas
  above.
- `pr-body` — this repo has `.github/pull_request_template.md` (`## Summary` /
  `## Test plan`) but no `scripts/check_pr_body.py`, so the skill's validation step is a
  no-op here and its three-section format does not match the template. Follow the repo
  template.
