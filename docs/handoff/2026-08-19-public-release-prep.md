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

The plan changed on 2026-08-22: a design review reframed the project from "work through
a punch-list" to "split the package from the template, then release the package."
Decisions live in `docs/adr/0001`–`0005` and `CONTEXT.md`; the work was issues #46–#57.

**All of #46–#57 are now closed.** The package is `lanepaper`, the layout is
`lanepaper/` + `demo/`, `CONVENTIONS.md` is the authority on package code, and
`build.lua` drives packaging.

**The CTAN gate is clear.** ADR-0001 says submission is one `l3build upload` after
#50 and #52; both landed. Nothing open blocks it mechanically — but see #55.

**Open: #73, #74, #55, #29, and ADR-0005 awaiting a decision.**

## Important Details

Hard-won facts. Most cost a failed run or a review round.

### ADR-0005 is proposed and blocks work — decide it first

[ADR-0005](../adr/0005-what-the-spacing-quantum-is.md) is `status: proposed`, not
accepted. It is a decision waiting on the maintainer, and half of #73 is blocked
until it lands.

The finding, measured rather than argued: `13.2 ÷ 16.32 = 0.809`, so the spacing
quantum and the document baseline are **incommensurable** — adding one quantum never
returns text to the line grid. Measured line gaps on page 12 of the shipped demo run
1.232 / 1.842 / 1.474 quanta. **Nothing lands on a quantum multiple.** One document
runs four pitches: body 16.32pt, quote 15.84pt, display maths 13.20pt, footnote
12.00pt.

13.2pt itself came from `11 × 1.20`, and both inputs are wrong (the `11pt` option sets
10.95pt; `\linespread` scales the class's 13.6pt baseline). ADR-0004 established the
number is not the baseline; ADR-0005 exists because it never said what the number *is*.

**Cost of delay is real**: 45 hardcoded `13.2pt` literals sit in executable positions
against 162 uses of `\gridunit`. Every new one written against 13.2pt is another site
that will not follow if ADR-0005 picks a baseline-derived quantum.

### Traps that cost real debugging — these will bite again

- **A `.sty` has `@` as a letter by construction**, so `\makeatother` inside one revokes
  it for the rest of the file. 137 stray pairs sat harmless until names became `\lnp@*`,
  then the build died with `Command \lnp already defined`. Do not reintroduce them.
- **`\@ifundefined{name}` takes a name WITHOUT a backslash**, so a `\`-driven rename
  sweep silently skips it. Grep `\@ifundefined` separately after any rename.
- **`\AtBeginDocument` decides precedence by registration order** — an accident of file
  layout. Deferring a cleveref block in #48 inverted a year-old `\crefname` precedence
  and rendered "§§ 1–2" instead of "appendices 1–2". No test noticed; only raster did.
  #56 removed the class; `\AtBeginDocument` is now banned and guarded.
- **A command the optional package owns is a fatal error, not "less styling".**
  `\startappendices` called hyperref's `\phantomsection`; once #48 stopped loading
  hyperref a bare document died. `\providecommand` it.
- **Dropping `babel` changes line breaking.** Measured `\spaceskip` values were tuned
  with babel present; without it all five pages of `opening-test.tex` re-break.
- **`grep -c` counts lines, not registrations.** `\AtBeginDocument` matched 11 lines
  when only 8 were real; three were comments. Filter before quoting a count.
- **`compare -metric AE` prints `0 (0)`, not `0`.** Take the first field only.
- **biber is PAR-packed and macOS temp purges corrupt its cache.** Presents as an
  exit-2 failure with an *empty* error log; the real cause is
  `Unicode::UCD: failed to find unicore/version`. Delete `/var/folders/.../T/par-*`.
  Not a repo regression; it will recur.

### Traps found this session

- **A `.md` link guard that strips inline code is half a guard.** The one added in #52
  missed every backticked path (`` `docs/technical/TESTING.md` ``) and every path cited
  from `.sty`/`.py`/`.sh`/`.tex`. **18 dead references survived**, two of them rendered
  into the demo PDF. #71 added `test_every_referenced_documentation_path_exists` to
  cover both. `docs/adr/` is exempt like `CHANGELOG.md` — ADRs deliberately cite files
  #52 deleted.
- **`perl -0pi -e 's/…/\x{2014}/'` re-encodes the entire file.** The escape upgrades the
  string to character semantics, so every pre-existing UTF-8 byte is re-encoded: it
  corrupted 34 em dashes in `CHANGELOG.md` before it was caught. Write the raw bytes
  (`\xe2\x80\x94`) and perl stays in byte mode.
- **A markdown reference documented two ways defeats one-shaped dedup.**
  `API_REFERENCE.md` documents commands as `####` headings *and* as table rows; a
  heading-only dedup appended four duplicates. Cross-check both representations. #74
  carries the guard.
- **`chktex -q -n48 <missing-file>` exits 0.** The Makefile probe pointed at a root
  `main.tex` that does not exist, so it passed by accident; on a real file chktex exits
  non-zero when there are warnings, which would have silently dropped the flag. Probe
  `/dev/null`.
- **Changing a line's length in `demo/main.tex` repaginates the demo.** A longer
  replacement wrapped and cascaded across pages 2–7. Match the original's rendered
  length; the fix took the raster diff from 6 pages to 2.

### l3build (adopted in #50 — packaging only, ADR-0002)

- **`install` reads `installfiles` from `unpackdir`, not `sourcefiledir`.** With no
  `.ins`, `unpack` still stages sources into `build/unpacked`, which is what makes
  `install` work. Do not "simplify" `unpackfiles = {}` away.
- **`cleanfiles` defaults to `{"*.log","*.pdf","*.zip"}` applied to `maindir`** — it
  would delete the demo's `main.pdf`. Set to `{}` deliberately; `make clean` owns
  artefacts. Verified `l3build clean` now leaves `main.pdf` alone.
- **`l3build upload --dry-run` still posts metadata to CTAN's validator.** It skips the
  submission, not the network call. Do not run it casually.
- **The uploader email is deliberately absent from `build.lua`.** Supply per upload:
  `l3build upload x.y.z --email <address>`. `announcement` and `topic` are absent too —
  see the comment in `build.lua`.
- **`make release VERSION=x.y.z` was proven end-to-end in a throwaway clone**, not on
  the real repo. Do the same for any change to it.

### Build and test truths

- **The engine is pdflatex**, and since #54 both documented entry points stop with one
  `\PackageError` on anything else. `iftex`'s `\RequirePDFTeX` was not used: it does not
  name the calling package. The guard hard-stops (`\batchmode\@@end`) because
  `\PackageError` alone is recoverable.
- **Do not delete the "Mark workspace safe for git" step in `ci.yml`.** It looks
  redundant with `actions/checkout`, which handles `safe.directory` only within its own
  step. Without it `tests/test_infrastructure.py` fails with `git ls-files` exit 128.
- **`src/sh/check-packages.sh` is generated**, not hand-maintained. Regenerate from the
  source, and use a pattern matching hyphens and comma-separated groups — a naive one
  silently dropped `eso-pic` and mangled `amsmath,amssymb`.
- **`TEXINPUTS`/`BIBINPUTS` in the Makefile** (`./lanepaper:./demo`) are why documents
  `\input{preamble.tex}` bare and `main.pdf` lands at the repo root. Anything
  hardcoding a directory breaks the next time files move.
- **The lettrine `*** ATTENTION REQUIRED ***` warning is positional, not a defect.**
  Allowlisting it would blind the harness to all future lettrine warnings.
- **`tests/visual/output/*.pdf` are generated, not baselines.** `!demo/figures/*.pdf`
  in `.gitignore` is different and load-bearing.
- **`lnphochuli` is not loaded by the default build.** Only the Pagella kerning pairs
  and `\parfillskip` apply on load; the rest are opt-in. A README bullet claiming
  otherwise was caught as a false front-page claim.

### Proving that rendering did not change — read before touching the `.sty` files

- **`pdftotext` comparison is not a rendering proof.** It reported byte-identical text
  while a page had visibly reflowed.
- **PDF byte comparison is meaningless** — the embedded timestamp changes every build.
- **Per-page raster is the proof**: `pdftoppm -r 150 -png` plus `compare -metric AE`.
  Fail loudly on any page-count change.
- **`main.tex` alone is not sufficient coverage.** It never exercises `\firstlinesc`;
  that path regressed while 40 pages compared clean. Render `opening-test.tex` too when
  touching small-caps or tracking.
- **Build both sides from clean, the same day.** `make build` reports "up-to-date" and
  serves a stale `main.pdf` — that produced 9 phantom differing pages once; a date
  rollover produced a `\today` diff another time.
- **Read every differing page, do not tally them.** Every raster claim in this repo's
  history that was wrong, was wrong because someone trusted the count.

### microtype tracking — the mental model

- **`\SetTracking` is global and order-sensitive.** `\lsstyle` selects the tracked font
  immediately; `\SetTracking` only registers a list for *later* selections. Of 27 sites
  audited, only `\spacedfirsline` was reversed — which made "restoring" its N a
  regression, not a fix.
- **microtype has no point-of-use named-list selection.** `\textls[N]{...}` is the
  working API. The original #39 plan assumed otherwise and was impossible.
- **microtype matches sizes exactly.** An explicit `\fontsize{11}` matches no named-size
  list, because `\normalsize` is 10.95pt in an 11pt class.

### Tooling and process

- **GitHub parses a closing keyword against the first issue number only.**
  `Closes #49, #46, #47, #53` closed exactly one issue. Write `closes` before each.
- **Commit before mutation-testing a guard.** `git checkout <file>`, used to undo a
  deliberate break, silently discarded uncommitted work twice.
- **Two PRs branched from different bases are never CI-tested together.** #71 and #72
  each passed alone; their combination was only verified locally after merge. Check the
  merged result when the second branch predates the first's new guard.
- **`gh-axi` is available via `npx -y gh-axi`.** `--repo` must come *after* the
  subcommand; `issue close --reason` takes `"not planned"` with a space.
- **`/grill-with-docs` and `/to-tickets` cannot be invoked by the agent** — both set
  `disable-model-invocation: true`.
- **A Herdr pane keeps ~24 lines of scrollback.** A long reviewer result is
  unrecoverable once it scrolls; `--source recent-unwrapped --lines N` does not reach
  further back. Brief reviewers to answer in few lines.
- **`herdr agent prompt` with a multi-line body lands as an unsent paste** — nothing
  runs until `herdr agent send-keys <pane> enter`. Stray suggestion text in the input
  box clears with neither `esc` nor backspace; ignore it, and never act on it (it
  sometimes reads like an instruction, e.g. "merge the branch").
- **Reviewer routing**: record `startup_failure` for `codex-sol-inline-reviewer` (the
  inline surface cannot bind non-Claude models) and `harness_crash` for
  `kimi-herdr-reviewer` (it wedges) to reach `claude-opus-herdr-reviewer`.
- **Do not judge agent liveness by screen content** — an animated progress bar makes a
  wedged agent look busy. Compare `revision` and `state_change_seq`.
- **Reviewers are not a substitute for running CI.** Independent review rejected
  substantive work three times, including two claims already verified and believed.

## Work State

`main` at `0299114`, clean, in sync, CI green. No open PRs, no worktrees or panes.

Local gates: **pytest 50 passed**, **`tests/run-tests.sh` 115 passed / 0 failed**,
`make lint` and `make build` clean, style validator 0 errors / 26 warnings.

Repository shape after this session: 19 tracked markdown files (was 69), 5 ADRs,
17 guards in `tests/test_infrastructure.py`, 11 Makefile targets (was 24).

Merged this session: #69 (#51 Makefile), #70 (#52 docs), #71 (orphaned references),
#72 (ADR-0005 proposed), and earlier #68 (#50 l3build), #67 (handoff).

**#48 remains the breaking change.** `\usepackage{lanepaper}` alone gives no
bibliography, links, or cross-references; third-party loads went 45 → 33 and the
package imposes no load order. `demo/preamble.tex` shows what a document must load.

Deliberately not done, with reasons:

- **`\everydisplay{\baselineskip=13.2pt}` was left in place** (`lnpmathgridlocked.sty:130`).
  Tighter display leading may be right; it has never been *chosen*. ADR-0005 decides.
- **`docs/adr/` is exempt from the reference guard.** ADR-0001 and ADR-0002 deliberately
  cite files #52 deleted, annotated as such. An accepted ADR is a record.
- **`CHANGELOG.md` is exempt from both link guards.** Its entries point at deleted
  files; rewriting history to keep links green would falsify the record.
- **The cleveref wrappers (`\refpage`, `\pref`, `\seeref`) call `\cref` unguarded**,
  deliberately — a `\providecommand` fallback would emit a reference pointing nowhere,
  which is worse than the error. Reasoning in `CONVENTIONS.md` §9.

## Next Move

**Decide ADR-0005** (PR #72 merged it as `proposed`). Everything else in the grid
thread waits on it, and the 45 literals get more expensive with every commit. Three
options are laid out there; making the 13.2pt grid *real* is explicitly not one.

Then, in order of independence:

```
ADR-0005 decision ── #73 items 6–9
#73 items 1–5   (unblocked now)
#74             (unblocked now)
#55             (independent, and the one that matters for CTAN)
#29             (unscheduled)
```

- **#73 items 1–5 can start today**: `CONTEXT.md`'s "Grid-locked" glossary asserts the
  disproved model; `lnpmathgridlocked.sty:129`'s comment says "inline" over a
  `\everydisplay`; `\lnp@listbaselineskip` is a `topsep`; `lnpminimal.sty:176–178` are
  dead fallbacks that can never fire; and `demo/main.tex:154` prints a rhythm claim the
  measurement contradicts. That last one changes the PDF — raster-prove it.
- **#55 is the last heavy package-code item and the real CTAN risk.** Both
  `\DeclareRobustCommand` uses are on *internal* macros, so **no public macro is robust
  at all** (~315 prefix-free `\newcommand`). A CTAN reviewer's test document surfaces
  this immediately. When it lands, `CONVENTIONS.md` §8's "not met" heading comes off.
- **CTAN has no date** and that is deliberate (ADR-0001).
- Optional: `actions/checkout@v4` and `upload-artifact@v4` emit a Node 20 deprecation
  annotation every run. Harmless, noisy.

### Unowned by any ticket

- **Public macro names carry no prefix** — `\tightlists`, `\centeredpar`, `\dialogue`,
  `\forceindent`. Documented convention, predates ADR-0001, but weak on CTAN where a
  shared texmf tree makes collisions real. #55 is robustness, not namespacing. Recorded
  as a known gap in `CONVENTIONS.md` §4.
- **`\lanepaperinfo` is defined in `lanepaper/lanepaper.sty` and called nowhere.**
- **`lnpgridoverlay` is an entry point with no engine guard.** #54 guarded the two
  surfaces README documents. Loading it bare on XeLaTeX gets no clear message.
- **The CTAN archive ships no typeset manual** — 16 `.sty` plus `README.md`,
  `CHANGELOG.md`, `LICENSE`. Acceptable, but a reviewer may ask.

## Relevant Files

- `CONVENTIONS.md` — **read first before touching `lanepaper/`.** §8 robustness is still
  **not met** (#55). Every count in it was measured; re-measure rather than copying one
  out. Its module table is generated from the `\RequirePackage` lines — regenerate it.
- `docs/adr/0001`–`0005` and `CONTEXT.md` — the decisions and the glossary. **0005 is
  proposed, not accepted.** 0001 and 0002 carry dated errata and cite deleted files on
  purpose. `CONTEXT.md`'s "Grid-locked" entry is wrong (#73 item 1).
- `build.lua` — packaging only, no test files declared, guarded by
  `tests/test_infrastructure.py`. The comment block explains why each empty file list is
  set explicitly; every l3build default is wrong for this repo.
- `lanepaper/lanepaper.sty` — the main package and #55's audit target. Its
  `\AddToHook{package/*/after}` blocks hold all configure-if-loaded styling.
- `lanepaper/lnpdimensions.sty` — where `\gridunit` and `\linespread` are set, and the
  clearest statement of the quantum-vs-baseline distinction.
- `demo/preamble.tex` — the worked example of what a document must now load.
- `API_REFERENCE.md` — 3.3k lines, the single reference after #52. Documents commands as
  both `####` headings and table rows; see #74.
- `tests/test_infrastructure.py` — 17 guards, each written to avoid matching its own
  source. Includes the two markdown-reference guards and the `build.lua` contract.
- `src/sh/validate_latex_style.sh` — the math-spacing check is a depth-tracking perl
  scan covered in four directions by pytest. Do not "simplify" it to a bracket
  expression.
- `tests/fixtures/opening-test.tex` — the only document exercising `\firstlinesc`;
  required for any rendering proof touching tracking. It loads `babel` explicitly since
  #48 — do not remove that.
- `README.md` features list — carries a guardrail comment limiting claims to verified
  support. Two sessions have violated it; check claims against the `.sty` files, never
  against existing prose.

## Suggested Skills

- `foreman` — for the remaining queue. **Merge mode is re-selected per invocation and
  permission does not carry over.** Reviewer routing gotchas are in Tooling above. #73,
  #74 and #55 touch different files and are genuinely parallel.
- `gh-axi` — issue and PR work, via `npx -y gh-axi`.
- `pr-body` — this repo has `.github/pull_request_template.md` (`## Summary` /
  `## Test plan`) but no `scripts/check_pr_body.py`, so the skill's validation is a
  no-op here and its three-section format does not match. Follow the repo template.
