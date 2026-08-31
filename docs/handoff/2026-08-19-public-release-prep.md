---
title: Public Release Prep
date: 2026-08-19
updated: 2026-08-31
type: handoff
topic: public-release-prep
---

## Objective

Get `lane_latex_template` to publicly releasable. `v2.1.0` is tagged and published as
latest.

The plan changed twice. A design review on 2026-08-22 reframed the project from "work
through a punch-list" to "split the package from the template, then release the
package" — issues #46–#57, all closed. Then ADR-0006 (2026-08-28) defined **v3**: a
deliberate breaking contraction to one public entry point and a narrow interface,
tracked as epic **#82** with children C1–C8 (#83–#90).

**C1–C7 are complete in this worktree.** The package is `lanepaper`, now **7 modules**
(down from 14), `CONVENTIONS.md` is the authority on package code, and `build.lua`
drives packaging.

**The CTAN build is ON HOLD** — the maintainer said "hold off on CTAN build" on
2026-08-26. Do not run `l3build ctan` or `l3build upload` until told. This bound an
agent on 2026-08-30 that ran `l3build ctan` locally to verify an archive fix; pass the
hold down to every delegate explicitly, because it is not inferable from the repo.

**Open: C8 (#90), plus #91 and #92 as post-v3.**

## Important Details

Hard-won facts. Most cost a failed run or a review round.

### What v3 removed, C1 through C6

- **C1–C3** (#93, #94, #95, #96): recorded the v3 architecture, removed the generic
  public API, made `\usepackage{lanepaper}` the sole load path, and narrowed document
  structures.
- **C4** (#97): replaced the custom Microtype tables with upstream Pagella defaults
  plus `+50` small-caps tracking. `lnpmicrotype.sty` is now 45 lines with two live
  declarations. Deleted the font-feature and fallback modules.
- **C5** (#98): deleted `lnphochuli.sty` and `lnpparagraphs.sty` (627 lines, neither
  ever loaded) and made `lnpdimensions.sty` the single paragraph owner. Two behavior
  changes: the first paragraph after a heading is now flush left, and
  `\interfootnotelinepenalty` is back to the kernel default of 100 so footnotes can
  split across pages.
- **C6** (#99): removed the duplicate harness path, the bespoke validators, the broken
  commands, and the release automation. See "The surviving command set" below.

`lnpgridoverlay`, `lnphochuli`, `lnpparagraphs`, `lnpfontfeatures` and
`lnpfontfallbacks` are all **gone**. Do not look for them; do not reinstate a claim
that references them.

### The surviving command set — C6 (#88) deleted the rest

Make targets are exactly `build lint test clean install uninstall ctan help`.
`make lint` is **ChkTeX only** and reports 0 warnings. `make test` is `pytest -q` then
`bash tests/run-tests.sh`, each run once.

Deleted and not replaced, by design — no gate, threshold, suite or workflow took their
place (ADR-0006 forbids it): `make check-deps`, `make watch`, `make release`,
`compile.sh`, `SECURITY.md`, the whole `src/` tree (`validate_latex_style.sh`,
`check-packages.sh`), `tests/check-spacing-integrity.sh`,
`tests/test_regression_harness.py`, and `.github/workflows/release.yml`.

Two consequences are **intended, not oversights**: math-operator spacing is no longer
machine-checked (the convention stands in `CONTRIBUTING.md` without a checker), and
there is no vulnerability-reporting channel.

### Licensing is split — do not restate it as one license

`lanepaper/` is **LPPL 1.3c**; the root `LICENSE` is the verbatim LPPL text and must
never be edited (the LPPL forbids modifying the license document). **Every other
original file** — `demo/`, `docs/`, `tests/`, `Makefile`, `build.lua`, the repository
documentation — is **MIT**, under `licenses/LICENSE-MIT.txt`. Stated in `README.md`,
`CONVENTIONS.md` §12, and the `AGENTS.md` copyright line.

The CTAN archive ships both notices. `build.lua`'s `textfiles` includes
`licenses/LICENSE-MIT.txt` precisely because the archive carries `README.md` and
`CHANGELOG.md`, which are MIT, under an `lppl1.3c` declaration.

### README is the authoritative dependency record

C6 deleted `check-packages.sh`, the machine check.
C7 absorbed the former standalone installation guide into `README.md`, which now
owns the dependency list and the GitHub installation instructions.
That list is user-facing and is derived from the surviving package and demo loads.

**Two dependencies are selected by option values, not package names, and a grep for
`\RequirePackage`/`\usepackage` cannot see them:**

- `boondox` — via `\RequirePackage[cal=boondoxo,bb=boondox,frak=boondox]{mathalfa}`
  at `lanepaper/lnpfonts.sty:45`.
- `babel-english` — via `\usepackage[english]{babel}` at `demo/preamble.tex:57`,
  which needs `english.ldf`.

`mathalfa` is the only option-bearing load inside `lanepaper/` whose values name a
separate file. Re-derive with that in mind if the list is ever rebuilt.

### Traps found 2026-08-29/30 (C5 and C6)

- **This machine has two TeX distributions and `PATH` decides.** TeX Live 2025 at
  `/usr/local/texlive/2025` and TinyTeX 2024 at `/usr/local/bin`. They produce
  **different PDF byte sizes from identical sources** (411570 vs 409922). This
  produced two false alarms in one session — a worker's correct proof was called wrong
  because the two sides were built under different distributions, and `make build`
  then served the worker's artifact as current. CI uses TL2025; hold the toolchain
  constant and use `latexmk -g` to force a rebuild.
- **Deleting a pytest wrapper can orphan a shell script nothing else runs.** Removing
  `test_regression_harness.py` left `tests/test-bibliography.sh` with no caller —
  `run-tests.sh` never invoked it — so the manual biblatex contract silently stopped
  running. One wrapper was restored on purpose; check callers before deleting a test.
- **`pdftotext -bbox-layout` embeds the input filename in its header**, so a naive
  diff reports every page as changed. Compare only the `<line>` elements.
- **`\pdfsavepos` + deferred `\write-1` works in a single pass** — the write expands at
  shipout, after the position whatsits are processed. That is what makes the
  flush-left assertion in `test_option_contracts.py` a one-compile test.
- **zsh does not word-split unquoted parameters**, so `set -- $spec` in a loop passes
  one argument, not several. Bit a cleanup script.
- **A finding of "0 differing lines" is only as good as the two builds behind it.**
  Verify a delegate's proof by re-running it yourself under a known toolchain.

### Delegating with foreman and Herdr — what actually bites

Two C6 review findings were defects no gate would have caught, so the review round is
worth its cost. The mechanics are where the time goes:

- **`herdr agent list` reports a stale `agent_status`.** A Codex pane sat at `working`
  long after it had finished and printed its report. Detect completion from the pane
  text — the `Worked for …` banner present *and* `esc to interrupt` absent — not from
  the status field. `watch-workers.sh` trusts that field, so it never fired.
- **`herdr pane read` returns only a short tail.** A long reviewer report scrolls out
  of reach and cannot be recovered. Ask for findings in severity batches, and widen the
  pane first with `herdr pane resize --pane <id> --direction up --amount 0.45`.
  `herdr pane zoom` does *not* grow the readable buffer.
- **A Herdr reviewer is launched read-only** and cannot write findings to a file, even
  outside the checkout. Plan to read them off the pane.
- **`close-worker.sh` needs `--session`**, and launch receipts are written with
  `agent_session` empty. The real session id appears in `herdr agent list` once the
  agent is running — capture it from there, not from the receipt.
- **`gh pr merge --delete-branch` fails when another worktree holds `main`**
  (`fatal: 'main' is already used by worktree at …`). The merge still succeeds; only
  the cleanup fails, leaving the remote branch alive. Delete it with
  `gh api -X DELETE repos/<owner>/<repo>/git/refs/heads/<branch>`.
- **`pr-readiness.py` requires `outcome: "clean"`**, not `"findings"`, once
  `unresolved_findings` is 0. `"findings"` blocks the gate regardless of the count.
- **Pass the CTAN hold to every delegate explicitly.** Nothing in the repository
  implies it, and a worker asked to verify an archive fix will reach for
  `l3build ctan`.

### Traps that cost real debugging — these will bite again

- **A `.sty` has `@` as a letter by construction**, so `\makeatother` inside one revokes
  it for the rest of the file. 137 stray pairs sat harmless until names became `\lnp@*`,
  then the build died with `Command \lnp already defined`. Do not reintroduce them.
- **`\@ifundefined{name}` takes a name WITHOUT a backslash**, so a `\`-driven rename
  sweep silently skips it. Grep `\@ifundefined` separately after any rename.
- **`\AtBeginDocument` decides precedence by registration order** — an accident of file
  layout. #56 removed the class; `\AtBeginDocument` is now banned and guarded.
- **A command the optional package owns is a fatal error, not "less styling".**
  `\providecommand` fallbacks for cross-package commands (`\phantomsection`).
- **Dropping `babel` changes line breaking.** `opening-test.tex` loads it explicitly.
- **`\skip=\gridunit plus 3.3pt` silently truncates**: a bare glue register after `=`
  copies and ends the assignment; `plus …` leaks into the document as text. Coefficient
  form (`1\gridunit plus …`) scans as a dimension. `CONVENTIONS.md` §6.
- **`\def\kern#1{}` in `pdfstringdefDisableCommands` gobbles only the `0`** of
  `\kern0.05em`. Symbol macros map to PU glyphs instead.
- **`\AtEndDocument{...}` is not a definition** — `##` inside it is a syntax error.
- **`\pdfmatch` is pdfTeX-only** — fine in fixtures, not in package code.
- **`grep -c` counts lines, not registrations.** Filter before quoting a count.
- **`compare -metric AE` prints `0 (0)`, not `0`.** Take the first field only.
- **ImageMagick `crop 100%x300` reads both axes as percentages.** Give explicit pixels.
- **biber is PAR-packed and macOS temp purges corrupt its cache.** Exit-2 with an
  *empty* error log, signature `Unicode::UCD: failed to find unicore/version`. Delete
  `/var/folders/.../T/par-*`. Recurs — C7 (#89) requires recording this in
  `TROUBLESHOOTING.md`.
- **`perl -0pi -e 's/…/\x{2014}/'` re-encodes the entire file.** Write raw bytes.
- **`chktex -q -n48 <missing-file>` exits 0.** Probe `/dev/null`; the Makefile does.
- **Squash-merge eats unpushed follow-ups — bitten twice.** Branch follow-ups off fresh
  `main`, and hold merges until external review lands. A squash-merged branch is not an
  ancestor of `main`: verify with `git diff <branch> origin/main`.
- **`git checkout <file>` to undo a deliberate mutation discards uncommitted work.**
  Commit before mutation-testing, no exceptions.
- **External review catches what rasters cannot.** Every review round this project has
  run has returned real defects, including two in C6 that no gate would have caught.
  Review before merge.

### Robustness (#55) — done, with deliberate exemptions

All 372 public macros are robust via etoolbox `\robustify` in a `ROBUSTNESS (#55)`
block ending each module — **not** `\DeclareRobustCommand`, which would silently
clobber on name collisions. Rule and mechanism in `CONVENTIONS.md` §8. Do not
"complete" these exemptions:

- **`\thefootnote` must stay expandable**: the kernel's `\protected@edef` freezes the
  footnote number into `\@currentlabel`; protection made a `\label` in footnote 1
  resolve to 2. `tests/fixtures/robustness-test.tex` asserts this differentially.
- **The former `\gridmult`/`\gridmath` value helpers are gone.** C7's migration
  guide directs documents to literal dimensions or standard `\vspace`; no public
  quantum helper remains.
- Any new runtime redefinition must re-`\robustify` immediately after.
- A new public macro is not done until its name is in its module's robustness block.

### l3build (adopted in #50 — packaging only, ADR-0002)

- **Stamping is now `l3build tag <version>` run directly.** `make release` was its only
  wrapper and C6 deleted it. **`make ctan` does not stamp before archiving**, so run
  `l3build tag` first when an archive needs synchronized versions. Current tree: five
  modules at `v1.1`, `lnpmicrotype.sty` at `v1.3`, `lanepaper.sty` at `v2.0`.
- **`install` reads `installfiles` from `unpackdir`, not `sourcefiledir`.** Do not
  "simplify" `unpackfiles = {}` away.
- **`cleanfiles` defaults would delete the demo's `main.pdf`.** Set to `{}`
  deliberately; `make clean` owns artefacts.
- **`l3build upload --dry-run` still posts metadata to CTAN's validator.** Do not run
  it casually — and the CTAN build is on hold regardless.
- **The uploader email is deliberately absent from `build.lua`.** Supply per upload.
- **`textfiles` paths are flattened into the archive root**, so `licenses/LICENSE-MIT.txt`
  lands as `lanepaper/LICENSE-MIT.txt`.

### Build and test truths

- **The engine is pdflatex.** There is now exactly one entry point, `lanepaper.sty`,
  and it hard-stops on any other engine with one package-owned error (#54).
- **Do not delete the "Mark workspace safe for git" step in `ci.yml`.**
- **`TEXINPUTS`/`BIBINPUTS` in the Makefile** (`./lanepaper:./demo`) are why documents
  `\input{preamble.tex}` bare and `main.pdf` lands at the repo root.
- **`tests/visual/output/*.pdf` are generated, not baselines.**
- **`tests/test-bibliography.sh` is invoked only by pytest**, deliberately.

### Proving that rendering did not change — read before touching the `.sty` files

- **Per-page raster is the proof**: `pdftoppm -r 150` + per-page compare. `pdftotext`
  and PDF byte comparison are not proofs.
- **`main.tex` alone is not sufficient coverage** — render `opening-test.tex` too when
  touching small-caps or tracking.
- **Build both sides from clean, the same day, with the same distribution.**
  `make build` serves stale PDFs; `latexmk -g` forces; a date rollover produces a
  `\today` diff on page 1.
- **Read every differing page, do not tally them.** A count alone has passed for
  "no change" here before, and been wrong.

### microtype tracking — the mental model

`\SetTracking` is global and order-sensitive; `\textls[N]{...}` is the working
point-of-use API; microtype matches sizes exactly (`\normalsize` is 10.95pt).
`\lsstyle` is render-neutral, `\textls` is not.

## Work State

This worktree is on `docs/v3-demo-and-docs` at `1bd2af4`; the current #102 review
follow-up is uncommitted. The accepted v3 work is present through C7, including
the one public entry point, the curated demo, the migration guide, and the
contracted API reference.

Local gates in this worktree, all verified under **TeX Live 2025**: `make lint` 0,
`make build` 0 producing a **7-page** PDF, **pytest 54 passed**, and
`tests/run-tests.sh` **60 passed / 0 failed** across 20 fixtures.
`test_infrastructure.py` holds 16 guards.

**The primary checkout is on a stale branch.** `~/code/lane_latex_template` sits on
`fix/api-guards-74` at `2a691af`, which predates every v3 PR — the handoff file there
is the pre-#100 version. Work from a worktree on `main`, or check out `main` first.
Running `reorient` in the primary reads that stale copy and reports a state two weeks
out of date.

Deliberately not done, with reasons:

- **`docs/adr/` and `CHANGELOG.md` stay exempt from the reference guards** — records
  deliberately cite deleted files.
- **The cleveref wrappers call `\cref` unguarded**, deliberately (`CONVENTIONS.md` §9).
- **#48 remains the breaking change**: `\usepackage{lanepaper}` alone gives no
  bibliography, links, or cross-references; `demo/preamble.tex` shows what to load.

## Next Move

**Nothing is in flight.** The queue:

1. **C8 (#90)** — stamp, rename, and manually publish v3 from the exact green SHA.
   It follows the completed C7 demo and documentation contraction.
   Depends on C7.
2. **#91, #92** — post-v3: figure/table-note APIs after adopter evidence, and a deeper
   simplification sweep.
3. **CTAN, only when un-held** — ADR-0001: no date, no pressure.

### Unowned by any ticket

- **Public macro names carry no prefix** — known gap in `CONVENTIONS.md` §4;
  namespacing, not robustness. Worth settling before CTAN.
- **`\lanepaperinfo` is defined and called nowhere.**
- **The CTAN archive ships no typeset manual** — 7 `.sty` plus `README.md`,
  `CHANGELOG.md` and both licenses. Acceptable, but a reviewer may ask.
- `actions/checkout@v4`/`upload-artifact@v4` Node 20 deprecation annotations. Noisy,
  harmless.

## Relevant Files

- `CONVENTIONS.md` — **read first before touching `lanepaper/`.** §6 the glue-coefficient
  rule, §8 the robustness mechanism, §11 versions and stamping, §12 the license split.
  Every count was measured; re-measure rather than copying one out.
- `docs/adr/0006-one-public-entry-point-and-a-narrow-v3-interface.md` — the binding
  constraint on this release line: no new suite, gate, threshold, score, screenshot
  automation, or release workflow.
- `docs/adr/0005-what-the-spacing-quantum-is.md` — accepted; its sub-decisions list is
  the authority on what stays a literal and why.
- `README.md` — the authoritative dependency record and GitHub installation guide.
- `MIGRATION.md` — the top-to-bottom v2-to-v3 replacement map.
- `lanepaper/lanepaper.sty` — the `ROBUSTNESS (#55)` block, the
  `\pdfstringdefDisableCommands` fallbacks, and the `%% FIX` exemption comments.
- `tests/test_option_contracts.py` — package and document contracts, including the
  flush-left paragraph proof and the bibliography wrapper.
- `build.lua` — packaging only; every l3build default is wrong for this repo, and the
  comment block says why.
- `demo/preamble.tex` — the worked example of what a document must load.

## Suggested Skills

- `foreman` — decomposition, delegate routing, review, and the GitHub lifecycle. Ran
  C5 and C6. Launch profiles live in `~/.config/lane-agents/foreman.json`; two Qwen
  reviewer profiles are parked in `foreman.qwen-parked.json` by maintainer choice.
  What worked for C6: one `codex-luna-max` Herdr worker holding the whole branch, with
  a `claude-opus` reviewer at xhigh. Ask for the merge mode up front — it is per-run
  and does not carry over.
- `gh-axi` — issue and PR work, via `npx -y gh-axi`.
- `pr-body` — repo template is `## Summary` / `## Test plan`; no checker script exists,
  so the skill's validation step is a no-op here.
- `code-review` — this repo's precedent is external review **before** merge, by a
  reviewer from a different model family than the author.
- `reorient` / `make-handoff` — this file is the anchor; update it in place, and run
  either one from a worktree on `main` (see Work State).
