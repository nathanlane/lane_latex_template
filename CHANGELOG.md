# Changelog

All notable changes to the Lane LaTeX Template are documented here.

## Unreleased

Contracted document structures on 2026-08-28 (issue #86). **Breaking, with no
aliases.**

- **Retained surface.** The complete title family remains, `\sectionopening`
  is one inline argument, `inlineitem` remains the sole custom list, and the
  standard `itemize`, `enumerate`, `description`, `quote`, `quotation`,
  `figure`, `table`, and `\appendix` paths retain their styling or native
  behavior.
- **Standard document ownership.** Float placement and appendix sequencing now
  remain standard LaTeX behavior. `booktabs` stays required and the examples
  use no vertical rules. `threeparttable` is document-owned: Lanepaper neither
  loads it nor defines `tablenotes`. Figure notes use the single collision-safe
  `lanepaperfigurenotes` environment, while longtable caption width remains
  configured only when the document loads `longtable`.
- **Removed structures.** Float barriers and wrappers, grid/table/image
  helpers, appendix orchestration, diagnostic commands, epigraph and ornamental
  quote helpers, drop caps, sidenotes, decorative break shapes, specialized
  list environments, and table-note wrappers are deleted without compatibility
  aliases. Active documentation and fixtures now show only the retained paths;
  migration replacements are collected in `API_REFERENCE.md`.
- **Coherence cleanup.** The loaded modules now own their dependencies without
  duplicate master-file loads; active examples no longer claim unsupported
  accessibility certification or expose dormant modules, and the retained
  display-paragraph command uses the private palette name introduced by #85.

Made `\usepackage{lanepaper}` the sole public load path and narrowed the
package foundations (issue #85, ADR-0006). **Breaking, with no aliases.**

- **Entry points.** `lnpminimal.sty` and `lnpgridoverlay.sty` are deleted, and
  so is `lnpcompilationfixes.sty`; nothing in it survived scrutiny. Its widow,
  orphan, `\raggedbottom` and float-spacing values were standalone fallbacks
  that the canonical block in `lanepaper.sty` already overrode; its
  `\PassOptionsToPackage{uniquename=init}{biblatex}` pre-configured a package
  the document owns (ADR-0003 rule 2); its `\hyphenation` exceptions were
  measured to change nothing (the demo still builds with zero overfull boxes);
  and `\fitwide`, `\showoverfulls` and `\hideoverfulls` were wrappers over
  `\resizebox` and `\overfullrule`. The remaining `lnp*.sty` files are
  internal owners: loading one directly is unsupported. The standalone
  scaffolding is gone from the six modules `lanepaper` actually loads — the
  `\@ifpackageloaded{lnpcolors}`/`{lnpdimensions}` dependency fallbacks in
  `lnpheadings` and `lnplists`, the `\@ifundefined{iflnp@nocolor}` shim in
  `lnpcolors`, the `\@ifundefined{iflnp@draft}` shim in `lnpmicrotype`, and
  the `\@ifpackageloaded` wrappers around the module loads themselves. In
  `lanepaper.sty`, definitions whose only duplicate owner was the unloaded
  `lnpparagraphs` are `\newcommand` again rather than `\providecommand`, and
  the `epigraph`, `emphasisquote` and `openingparagraph` environments lost
  their `\@ifundefined` wrappers, so a genuine name collision errors at load
  time as CONVENTIONS §8 requires. Issue #86 subsequently removed those
  structures and the duplicate `lnpheadings` opening/spacing seam.
- **The four unloaded v2 modules are untouched.** `lnpfontfallbacks`,
  `lnpfontfeatures` (#29), `lnphochuli` and `lnpparagraphs` (#87) are carried
  over as-is apart from the `\lnp@` rename sweep. This pass did not refactor
  them and they still duplicate definitions held in `lanepaper.sty`.
- **Options.** Only `[optical]` and `[nocolor]` remain. `[grid]`, `[nogrid]`,
  `[minimal]`, `[draft]`, `[natbib]`, `[nobiblatex]`,
  `[subsectionbarriers]` and `[nosubsectionbarriers]` are removed and now
  raise LaTeX's own `Unknown option` error. Issue #86 subsequently removed the
  unconditional barriers, leaving standard LaTeX float placement. `[optical]` is new and
  carries sourced refinements that are not safe as defaults — currently
  last-line runt control, capping `\parfillskip`'s stretch so a paragraph's
  last line reaches at least a third of the measure (Hochuli). Widow and
  orphan protection stays a default for every document.
- **The spacing quantum is private.** `\gridunit` is now `\lnp@gridunit`, and
  the derived lengths (`\halfgridunit` … `\triplegridunit`), the arithmetic
  helpers (`\gridmult`, `\gridmath`, `\gridspace`, `\halfbaselinespace`,
  `\fullbaselinespace`, `\roundtogrid`), the grid image system
  (`\gridincludegraphics`, `\imagegridspace`, `gridfigure`), the grid table
  environments (`gridtable`, `compactgridtable`, `spaciousgridtable`), the
  `\arraystretch` aliases (`\standardgrid`, `\compactgrid`, `\spaciousgrid`,
  `\customgrid`), the quantum-fraction paragraph switchers
  (`\quartergridparagraphs`, `\thirdgridparagraphs`) and the quantum-fraction
  display wrappers (`grideqnarray`, `gridgather`) are removed. Documents write
  the length they mean, and use amsmath's `align` and `gather` directly.
- **Paper size.** `\geometry` no longer forces `letterpaper`, so
  `\documentclass[a4paper]{article}` really produces A4. What the package
  fixes is the six-inch measure and its centring (`textwidth=6in`,
  `hcentering`, `vmargin=1.25in`). The established US Letter page is byte-for-
  byte unchanged: 433.62pt text width, 614.295pt text height, 18.0675pt
  `\oddsidemargin`, −18.9325pt `\topmargin`.
- **Colours are namespaced and private.** All eight used colours are
  `\lnp@`-prefixed; the bare `textblack`, `linknavy`, `sectioncolor`, … names
  are gone, as are `\maincolor`, `\secondarycolor`, `\accentcolor` and
  `\codeaccent` and the nine colours nothing used. `[nocolor]` changed
  meaning: it converts the palette through xcolor's gray model instead of
  redefining every name as gray 0, so the grayscale hierarchy between heading
  levels survives where v2 flattened it to one black.
- **Hyperref is now only the visible link theme.** One `\hypersetup` instead
  of three, naming `\lnp@linknavy` once (`[nocolor]` greys it in the palette
  itself). `bookmarksnumbered`, `pdfborder` and `pdfencoding` are removed:
  under ADR-0003 rule 2 a bookmark-tree policy, a link-border policy and a
  PDF-string encoding choice are the document's, not this package's. The
  `\pdfstringdefDisableCommands` block is deleted rather than narrowed —
  every command in it (`\textsc`, `\textbf`, `\textit`, `\emph`,
  `\SetTracking`, `\lsstyle`, `\\`, `\hspace`, `\vspace`, `\kern`, `~`)
  belongs to standard LaTeX or microtype and is hyperref's own business, and
  the single Lanepaper name in it, `\lnp@titlesc`, is private to abstract,
  keywords and JEL front matter, which generates no bookmarks. No retained
  Lanepaper command can reach a bookmark, so the block guarded nothing.
- Obsolete standalone-module and preload probes were deleted from
  `tests/run-tests.sh` rather than replaced: the option and layout contracts
  are asserted once, in `tests/test_option_contracts.py`, at the `lanepaper`
  boundary.

Contracted the public API for v3 (issue #84, ADR-0006). The generic writing,
emphasis, code, punctuation, symbol, currency, fraction, spacing, math, and
reference helpers were removed rather than kept as compatibility aliases,
restoring standard LaTeX, amsmath, and third-party ownership of the names they
shadowed or collided with — including `\unit` (siunitx), `\meta` (doc), `\S`,
`\P`, `\copyright`, `\dag`, `\ddag`, `\ldots`, `\cdots`, `\natural`, `\lim`,
`\thinspace`, `\medspace`, and `\thickspace`. The cleveref format/name
configuration and the reference wrappers (`\refpage`, `\pref`, `\seeref`,
`\seealso`, ...) were removed too: cross-references are now fully
document-owned (ADR-0003 rule 3), so a document loads and configures cleveref
itself. The `\pdf*` bookmark wrappers were removed with the emphasis/code
helpers they wrapped. The defensible title-page small caps used by the
retained front matter (abstract, keywords, JEL) is kept but made private
(`\lnp@titlesc`) and is visually unchanged. `API_REFERENCE.md` drops the
removed commands from the active API and gains a "Removed in v3" migration
table; two focused fixtures probe the standard/package collisions and the
retained title surface. No compatibility aliases were added. Demo call sites
were mechanically repointed to the standard equivalents to keep the build
green; the demo/documentation rewrite remains issue #89.

Recorded the accepted v3 package boundary in ADR-0006 and corrected the older
architecture records and glossary to match it. Public-release execution now
lives in GitHub issue #82 and its dependency-ordered children; the operational
handoff was removed after its decisions and follow-ups were transferred. CTAN
submission remains explicitly on hold.

Removed the unrelated `src/py/example_analysis.py` scaffold. It had no package
or test callers and failed the repository's installed-Black lint gate.
The non-pdfTeX guard test now requires one clear Lanepaper-owned error and no
PDF instead of assuming the local engine emits no earlier environment errors.

Guarded `API_REFERENCE.md` against duplicate command documentation (issue
#74): a test now collects commands from both `####` headings and table rows
and fails if any name appears twice (variant rows inside one table are a
single entry); the guard is mutation-checked against both representations.
The eight generic subheadings the #52 fold left colliding ("Basic Usage" x4,
"Inconsistent Spacing" x2, "Overview" x2) are renamed to what they cover, and
a second test keeps `####` heading text unique so markdown auto-anchors stay
position-independent.

Post-merge external review of #79 found four robustness defects, fixed here:
`\thefootnote` is deliberately un-robustified (protection froze footnote
labels at the wrong number — the fixture now asserts this differentially);
`\gridmult`/`\gridmath` are exempted as deliberately expandable value
helpers; `lnpfontfallbacks`' runtime redefinitions of `\textsc` and
`\oldstylenums` re-robustify at the definition site; hook-defined `\yen` is
robustified where defined; and the PDF-bookmark fallbacks now cover the
currency and symbol macros, whose `\kern` guards previously mangled bookmark
strings.

Made every public macro robust (issue #55). All 372 prefix-free macros across
the 14 modules are now protected against expansion in moving arguments —
section titles, captions, footnotes, and the `.aux` round-trip — via etoolbox
`\robustify` (e-TeX `\protected`), applied in a `ROBUSTNESS (#55)` block at
the end of each module. Definitions stay `\newcommand`, so load-time name
collisions with other packages still error instead of silently clobbering.
The `\pdfstringdefDisableCommands` block gains plain-text fallbacks for the
semantic and symbol macros likely to appear in headings, so PDF bookmarks
degrade without warnings. New contract fixture
`tests/fixtures/robustness-test.tex` exercises macros in a section title,
caption, footnote, and bookmarks over two passes. Rendering proved unchanged:
all 40 demo pages and all 5 `opening-test` pages byte-identical at 150dpi,
built from clean on both sides.

Cleared the remaining spacing-quantum defects (issue #73): renamed the
`\lnp@list*baseline*` lengths to `\lnp@list*quantum` (they hold quantum
fractions used as topsep/itemsep; the measured list baselineskip is 16.32pt),
deleted `lnpminimal.sty`'s dead `\gridunit` fallbacks, and rewrote the
demo's nine printed rhythm claims to match ADR-0005. The prose edits change
the PDF: raster-diffed at 150dpi, seven pages differ, each read and confined
to the edited sentences plus a one-line reflow on pages 22–23.

Post-review fixes from an external code review of #77: restored the live
`\halfgridunit`/`\quartergridunit` fallbacks in `lnpminimal.sty` (only the
`\gridunit` one was dead), kept the v2.1.0 `\list*baseline*` aliases as
deprecated names, corrected two stale baseline comments, and cleared the
remaining grid-alignment claims the first pass missed ("Grid Compliance",
"Grid-Aligned" headings and captions). Two standalone regression probes added.

Swept the last old-model vocabulary from the documentation: `README.md` and
`API_REFERENCE.md` no longer claim rhythm or grid alignment (the worst was
"The baseline grid ensures vertical rhythm"), the documented-but-nonexistent
`gridbox` environment example is gone, a documented `\vspace` example no
longer carries the bare-register glue trap, and the demo appendix's
"Grid-Aligned" heading and caption are renamed (2 pages changed, both read).

Accepted ADR-0005: `\gridunit` (13.2pt) is a plain spacing quantum with no
relationship to where text lands; all rhythm and grid-locking claims are
being removed (issue #73, ADR-0005).

**Removed `lnpheadingsgridlocked.sty` and `lnpmathgridlocked.sty`.** Nothing
loaded them — not `lanepaper.sty`, not the demo — and their "grid recovery"
mechanisms were `\vspace{0pt plus X minus X}` glue centred on zero, which
snaps to nothing. Measured proof that the demo never ran their code: align
rows in the shipped PDF pitch at 26.1pt (baseline 16.32pt + `\jot` 9.9pt),
not the 23.1pt the module would set. Their references in README,
INSTALL, TROUBLESHOOTING, API_REFERENCE, the CONVENTIONS module table, and
the `run-tests.sh` standalone probe are gone with them.

The `[grid]` overlay now draws only the real baseline grid (lines every
`\baselineskip`); the 13.2pt quantum lines are gone — a spacing unit is not
a set of positions. The unused debug helpers (`\checkgrid`,
`\markposition`, `\showbaseline`) went with them, and `\showgrid[color]`
now actually honours its color argument.

Spacing values are now stated in `\gridunit` multiples instead of 45
scattered point literals; derived lengths (`\halfgridunit` …
`\triplegridunit`) single-source from the quantum. `\parindent` is
deliberately a `13.2pt` literal — a horizontal indent must not follow the
vertical quantum. Proven rendering-neutral: all 40 demo pages byte-identical
at 150dpi.

Consolidated the documentation (issue #52).

**69 markdown files and 16,249 lines down to 18 files and 7,313 lines.** Ten at
the root, plus `docs/adr/`, `docs/handoff/`, `tests/README.md` and the two
`.github/` templates. `docs/archive/`, `docs/development/`, `docs/technical/`,
`docs/style/`, `docs/typography/`, `docs/guides/` and `docs/package/` are gone.

Most of it was deletion: 22 files had not been touched since a single
2025-07-09 import, and `docs/archive/` was a second, worse copy of git history
that landed in every grep. What was reference-grade was folded rather than
dropped:

- `CUSTOM_COMMANDS.md` into `API_REFERENCE.md`, which goes from **83
  documented commands to 109**. The package defines about 385 public macros,
  so this is still short — but the gap is now visible in one file.
- The five module documents, the bibliography guide, and the spacing-quantum
  document into `API_REFERENCE.md` as system sections.
- `STYLE_GUIDE.md` and `docs/package/README.md` selectively: only the sections
  not already covered. Seven of eleven, and six of twelve, respectively.
- `LATEX_STYLE_STANDARDS.md` into `CONTRIBUTING.md`, which is what
  `CONVENTIONS.md` already deferred to for document source style.
- `docs/technical/TESTING.md` (894 lines) into `tests/README.md`, rewritten
  rather than concatenated, and corrected: it still described `paperstyle.sty`
  and `\input{paper/preamble.tex}`.
- `docs/style/CHANGELOG.md` into this file as its earliest history. It covered
  a 2024-06-30 release that nothing else recorded.

`docs/typography/BASELINE-GRID-DECISION.md` was **promoted to
[ADR-0004](docs/adr/0004-baseline-grid-is-a-spacing-quantum.md)**. It was
already a decision record and predated `docs/adr/`.

The module table in `CONVENTIONS.md` section 3 is generated from the
`\RequirePackage` lines rather than maintained by hand. The one it replaces
listed 9 of 16 modules.

`tests/test_infrastructure.py` gains a guard that every relative markdown link
resolves, with `CHANGELOG.md` exempt: its entries point at files that have
since been deleted, and rewriting past entries to keep links green would
falsify the record.

Two ADR citations of deleted files are annotated in place rather than rewritten
(ADR-0001's fork audit, ADR-0002's roadmap); an accepted ADR is a record, not a
live description.

One document did contradict the code. `docs/GRID_SYSTEM_REFERENCE.md` still
taught that `\gridunit` is "11pt body × 1.20 leading = 13.2pt" — the exact
premise ADR-0004 overturned. It is deleted.

`AGENTS.md` and `CONTRIBUTING.md` both listed the pre-commit gates. `AGENTS.md`
now names the three targets and defers to `CONTRIBUTING.md` and
`tests/README.md` for what they cover.

Cut the Makefile from 24 targets to 11 (issue #51).

The aliases are deleted, not forwarded. Four targets used to run the tests and
nobody could tell which one CI used; `pdf`, `quick` and `build` were three
routes to the same compile; `clean`, `distclean` and `test-clean` overlapped.

What survives: `build`, `lint`, `test`, `clean`, `check-deps`, `watch`,
`install`, `uninstall`, `ctan`, `release`, `help`. The last four came from #50,
which landed after this issue was written -- the issue's own target list was
eight, and these are packaging jobs rather than aliases.

Two targets changed meaning:

- `lint` now runs `src/sh/validate_latex_style.sh` after chktex. The math-
  spacing checker previously had its own `style-check` target that CI never
  ran, so this is a check CI gains.
- `clean` now removes the PDF as well. `distclean` was the only way to get a
  genuinely clean tree, and a stale `main.pdf` has silently passed for a fresh
  build here before.

`make test` runs pytest and then the shell harness, and CI calls that single
target instead of the two commands, so what CI runs and what a contributor
runs cannot drift apart.

Deleted with no replacement target: `fmt`, `format`, `figures`, `diagnose`,
`warnings`, `dev`, `setup`, `validate`, `all`. The formatter commands they
wrapped are documented directly in `AGENTS.md` and `docs/technical/TESTING.md`.

Also fixed a latent bug in the chktex probe: it tested `-n48` support against a
root `main.tex` that does not exist. chktex exits 0 on a missing file and
non-zero on a real file with warnings, so pointing the probe at a real document
would have silently dropped the flag. It now probes `/dev/null`.

Stale `make` instructions were corrected across `README.md`, `INSTALL.md`,
`TROUBLESHOOTING.md`, `CONTRIBUTING.md`, `AGENTS.md`, `demo/main.tex`,
`tests/README.md`, `docs/guides/BIBLIOGRAPHY_GUIDE.md` and
`docs/technical/TESTING.md`, and `src/sh/validate_latex_style.sh` no longer
tells the user to run a target that no longer exists.

Adopted l3build for packaging and release (issue #50).

`build.lua` at the repository root drives four targets: `install` copies the
package into `TEXMFHOME`, `tag` stamps one version and date into every
`\ProvidesPackage`, `ctan` builds the archive, and `upload` submits it. The
Makefile stays the entry point for humans: `make install`, `make ctan`, and
`make release VERSION=x.y.z`.

l3build is packaging only. `build.lua` declares **no test files** and CI keeps
running `python3 -m pytest -q` unchanged - see
[ADR-0002](docs/adr/0002-l3build-for-packaging-pytest-for-tests.md) for why
log-diffing with `l3build check` is a poor fit for a package that loads this
many third-party dependencies.

`l3build tag` is what fixes the version drift: the 16 modules carried three
different version namespaces (`v1.1`, `v1.2`, `v2.0`) while the repository was
tagged `v2.1.0`. `\ProvidesPackage` is the only place a version appears in the
package, so one stamping pass covers all of it. Nothing is stamped yet - the
next `make release` does it.

Pushing a `v*` tag now builds the CTAN archive and publishes a GitHub release
(`.github/workflows/release.yml`). Submission to CTAN stays a manual step,
because it cannot be undone.

The archive currently ships the 16 `.sty` files plus `README.md`,
`CHANGELOG.md`, and `LICENSE`. It has no typeset manual; documentation is
issue #52's, which is also the remaining CTAN gate.

Migrated to the LaTeX2e hook system (issue #56).

All **11** `\AtBeginDocument` registrations are gone - the issue said seven,
counted before #48 added several while deferring the configure-if-loaded checks.
Six became `\AddToHook{begindocument}`; the five configure-if-loaded checks
became **package hooks**, which is the better instrument:

```latex
\AddToHook{package/hyperref/after}{...}
```

fires exactly when hyperref loads, whether that is before or after this package,
and never fires at all if the document does not load it. All three cases were
verified against a probe rather than assumed, and against `latexrelease`
rollbacks at 2020-10-01, 2021-06-01 and 2021-11-15.

That removes the class of bug #48 hit rather than working around it.
`\AtBeginDocument` runs callbacks in registration order, so precedence was an
accident of file layout: deferring the cleveref block inverted a `\crefname`
precedence that had held for a year, changing rendered output with no test
noticing. Nothing in the package depends on registration order now, so there is
**no `\DeclareHookRule`** - rules for hooks touching disjoint state would be
noise, not safety.

`\NeedsTeXFormat` rises from `2018/01/01` to **`2020/10/01`** on both entry
points, the release that made `\AddToHook` format-native. README and INSTALL
state the requirement.

Three guards in `tests/test_infrastructure.py`: no `\AtBeginDocument` may
return, the five packages must stay on their load hooks, and the declared floor
must match. Two were confirmed to fail when a hook is reverted.

`main.tex` renders identically (0 of 40 pages differ) and `opening-test.tex`
0 of 5, both built from clean the same day - the earlier run showed a one-page
diff that was only the `\today` line after the date rolled over.

Applied the configure-if-loaded dependency policy (issue #48, ADR-0003).
**This is a breaking change for documents that relied on the package to supply
their bibliography, links, or cross-references.**

`lnpminimal.sty` loaded hyperref at end of preamble if the document had not.
That is the same load-order imposition the policy removes, so it goes too:
applying the rule to one of the two entry points would leave the package
incoherent. lnpminimal calls no hyperref command, so nothing needed guarding.

Third-party loads went from **45 to 33**. ADR-0003 estimated ~37 down to ~25;
both numbers were low, measured before the count was checked.

- **Configure if loaded, never load:** `hyperref`, `cleveref`, `biblatex`,
  `babel`, `appendix`, `longtable`, `tabularx`. The package styles each one
  when the document loads it. A style package that loads `hyperref` dictates
  load order to every document using it, which ADR-0003 calls the single most
  likely thing to break an adopter. **The package now imposes no load order.**
- **Moved to the document:** the landscape and rotation conveniences
  (`landscapetable`, `landscapefigure`, `rotatedtable`, `wideregressiontable`,
  `fittable`, `landscapelongtable` and the rotation helpers) are in
  `demo/landscape.tex`, taking `pdflscape`, `rotating` and `adjustbox` with
  them. They belong to the Template once ADR-0001's separate repository exists.
- `longtable` and `tabularx` were **not** deleted, as ADR-0003 and the issue
  both specified. Their premise - "used zero times" - was wrong: the package
  sets `\LTcapwidth` and hooks `\lnp@tablecaptionsetup` onto the longtable
  environment, and `\LTcapwidth` is longtable's own length, so an unguarded
  `\setlength` is an undefined control sequence for any document without it.
  Treated under rule 2 instead, so the typography survives.
- `[natbib]` and `[nobiblatex]` are **deprecated and inert**: with no
  bibliography package loaded there is nothing to switch. Both stay declared
  and warn, so existing documents get a notice rather than an "Unknown option"
  error.
- Checks are deferred to `\AtBeginDocument` rather than done inline, because
  `hyperref` is conventionally loaded late - typically after this package - so
  an inline `\@ifpackageloaded` would run first and configure nothing.

Three consequences that raster comparison caught and no test did:

- Deferring the cleveref block **inverted a precedence that had held for a
  year**. Two `\AtBeginDocument` hooks set the same `\crefname`; once both were
  deferred, registration order decided, and an appendix range on demo page 38
  rendered "§§ 1-2" instead of "appendices 1-2". All cleveref naming now lives
  in one guarded block in the original effective order.
- `\startappendices` called `\phantomsection`, which is `hyperref`'s. It was
  always defined while the package loaded hyperref; a bare document reached it
  undefined and died. Now `\providecommand`-guarded - a fatal error, not the
  "less styling" ADR-0003 anticipated.
- **Dropping `babel` changes line breaking.** The package's measured
  `\spaceskip` values were tuned with babel present, so without it every one of
  the five pages of `tests/fixtures/opening-test.tex` re-breaks. The fixture
  loads babel and is byte-identical again: the package change is neutral given
  the same package set, but a bare document's line breaking does change.

`src/sh/check-packages.sh` is regenerated from the source and now lists `zi4`,
`mathalfa` and `eso-pic`, which it had omitted - the first two were issue #42.
Font fallbacks loaded inside `\IfFileExists` are deliberately excluded, and
`biber` is kept as a binary check. Review caught that the first regeneration
used a name pattern that could not match a hyphen or a comma-separated group,
silently dropping `eso-pic` and splitting `amsmath,amssymb`.

`demo/preamble.tex` now loads what the document owns, with the exact biblatex
option set the package used to impose. `main.tex` renders identically: 0 of 40
pages differ; `opening-test.tex` 0 of 5.

Neutralised two documents that contradicted the settled decisions:

- `docs/PACKAGE_ROADMAP.md` carries a SUPERSEDED banner. It called itself "the
  single source of truth" while proposing an `expl3` migration
  (`\ProvidesExplPackage`, `l3keys`, `\cs_new:Npn`), an `\east@` namespace, and
  removal of `\makeatletter` pairs "by switching to `expl3`" - all of which
  contradict `CONVENTIONS.md` and ADR-0002. Its Vision describes East-Asian
  typesetting, which this package does not do; much of the file was imported
  from a different project. Its module tasks name `colors.sty` and
  `dimensions.sty`, gone since July 2025.
- It is **not** deleted, because ADR-0002 cites its T-402 item in order to
  withdraw it, and deleting a file an accepted ADR references would break the
  record. Deletion belongs to #52, whose target document set does not include
  it. `docs/README.md` now marks the pointer superseded rather than
  "historical".
- ADR-0001 says "the four competing internal prefixes" and names four.
  Implementing it in #46 found a fifth, `\paperstyle@` (6 occurrences). The ADR
  now carries a dated erratum; the original sentence is left as written, because
  an accepted ADR records what was decided rather than describing the current
  code. `CONVENTIONS.md`, `docs/package/NAMESPACE_CONVENTIONS.md` and the guard
  in `tests/test_infrastructure.py` all say five.

Added `CONVENTIONS.md` (issue #45):

- States how package code in `lanepaper/` is written: LaTeX2e baseline (no
  expl3), engine support, naming, the public/private boundary, message policy,
  package-code style, the `%% FIX:` convention, robustness, hooks and load
  order, lint policy, versioning and licensing.
- Every count and anchor in it was measured at writing time rather than carried
  over from the issue, and one of the issue's figures was wrong: `%% FIX:`
  appears 116 times, not 112. `\AtBeginDocument` is at 8 sites, not the 7 the
  issue claimed and not the 11 a plain grep reports - three matches are
  comments rather than registrations.
- Sections that state a rule the code does not follow say so and name the issue
  that fixes it: robustness (#55), hooks (#56), and the configure-if-loaded
  dependency policy (#48). Nothing in the document implies compliance it does
  not have.
- Sharpened one claim in the process: #55 describes robustness as "2 of ~500",
  but both `\DeclareRobustCommand` uses are on internal macros
  (`\lnp@textapprox`, `\lnp@textinfty`), so **no public macro is robust at
  all**.
- `docs/package/NAMESPACE_CONVENTIONS.md` told contributors to "always use
  `\makeatletter`/`\makeatother` when defining `@` commands". That is the rule
  that broke the build in #46 - a `.sty` has `@` as a letter already, so a
  stray `\makeatother` revokes it for the rest of the file. The advice is now
  inverted at its source as well as stated in `CONVENTIONS.md`.
- `CONTRIBUTING.md` and `AGENTS.md` point at the new document.
- Naming content is absorbed rather than linked, because
  `docs/PACKAGE_NAMING_CONVENTION.md` and
  `docs/package/NAMESPACE_CONVENTIONS.md` are both slated for deletion in #52 -
  a document cannot link to a file scheduled to disappear.

#57's last open criterion, the ChkTeX suppression policy, lands here as §10.

Consolidated work tracking on GitHub Issues (issue #57, partial) and closed out
the Poppler gates (issue #35):

- `BACKLOG.md` is deleted and its `.gitignore` entry removed. It was gitignored,
  so its contents were invisible to CI and to collaborators while the issue
  tracker was live. No build, CI or code path referenced it; the only mentions
  were prose, in this file and in the release-prep handoff, which is updated
  here.
- Its seven lines were a ChkTeX lint policy, not a backlog: the suppressed
  warning classes (W01, W03, W08, W11, W13, W18, W24, W36, W39, W42, W46, W48)
  and the rule that they are revisited only in a pass where rendered output may
  change. #57 requires that policy to land in `CONVENTIONS.md`, which does not
  exist yet - it is #45. The text is recorded on #45 so deleting the file did
  not lose it, and #57 stays open on that one criterion.
- Added `.github/issue_template.md` with the house structure (What to build /
  Acceptance criteria / Blocked by), as a single file matching the existing
  `.github/pull_request_template.md` rather than an `ISSUE_TEMPLATE/` directory,
  so no template is added for any other issue type.
- `README.md` now records Poppler as part of the verified local setup:
  `pdftotext` 26.08.0 and `pdfinfo` on PATH, so the PDF-text assertions in
  `tests/test_regression_harness.py` run rather than skip and
  `tests/check-spacing-integrity.sh` runs instead of exiting 1. Confirmed by
  `pytest -q` reporting 41 passed and 0 skipped.
- `tests/check-spacing-integrity.sh main.pdf` was run and reviewed. It is
  advisory and flags two items on the demo document - 158 words per page and
  37% page efficiency against an expected ~15 pages. Both are artifacts of
  measuring a typography specimen full of headings, figures and short examples
  against prose-shaped thresholds, not defects. No change made.

Added an engine guard (issue #54):

- `lanepaper` and `lnpminimal` now load `iftex` and stop with a single
  `\PackageError` naming the package when the engine is not pdfTeX. Both are
  guarded because README documents them as distinct surfaces: `lnpminimal` is
  not reached through `lanepaper.sty`, so guarding only the main package would
  have left it exposed. The other 14 files are internal and reachable only
  through a guarded entry point.
- The guard stops the run (`\batchmode\@@end`). Without the stop the error is
  recoverable, so a `nonstopmode` build continues into the font cascade the
  guard exists to prevent - on XeTeX `microtype` alone adds two more errors.
- `iftex`'s own `\RequirePDFTeX` was not used: it prints "pdfTeX is required to
  compile this document" without naming the package that wanted it.
- `\NeedsTeXFormat{LaTeX2e}[2018/01/01]` is now declared on the main package,
  matching the floor `lnpminimal.sty` already declared. Nothing in the package
  uses a post-2018 kernel feature, so no higher floor is claimed.
- The header comment in `lanepaper.sty` claimed "pdfTeX or LuaTeX". LuaTeX was
  never supported; the line now says pdfTeX only.
- `tests/test_engine_guard.py` asserts the guard's presence, and runs XeLaTeX
  and LuaLaTeX against both entry points to confirm each fails with exactly one
  error naming the package, while pdfLaTeX still compiles. Confirmed the tests
  fail when the hard stop is removed and when the guard is removed.
- pdfLaTeX output is unchanged: the guard is inert on the supported engine.

Corrected package paths in the adopter-facing docs that #47 left stale:

- `README.md`'s directory diagram still showed `lanepaper/preamble.tex` and a
  `lanepaper/modules/` subdirectory. Neither exists: `preamble.tex` lives with
  the document in `demo/`, and #47 flattened the modules into `lanepaper/`.
- `README.md`'s first-document instructions told adopters to
  `\input{demo/preamble.tex}` — a path inside this repository, not theirs.
  Replaced with the two lines that file actually contains.
- `README.md`'s version history and `CONTRIBUTING.md`'s namespace section both
  cited `paper/lanepaper.sty`, a path removed by #47.

The stale-name guard in `tests/test_infrastructure.py` scans `.tex`, `.sty`,
`.sh` and `.py` only, so none of these were caught automatically.

Added LPPL 1.3c headers to all 16 package files (issue #53):

- Every file in `lanepaper/` now carries the license, the `maintained`
  maintenance status, and the Current Maintainer. Previously 0 of 16 did, which
  is a CTAN review blocker: `LICENSE` at the repository root is not sufficient.
- The header text comes from `licenses/LICENSE.txt`, which already named
  Nathan Lane as copyright holder and Current Maintainer. Two things changed
  there: the year is now 2025-2026, and "This work consists of the file .sty
  files and content of this repo" became "the files in `lanepaper/`". After
  #47 that line matters — it defines the licensed Work, and `demo/`, `docs/`
  and `tests/` are not part of what ships.
- `tests/test_infrastructure.py` asserts every `lanepaper/*.sty` carries the
  header, so a new module cannot skip it. Confirmed the guard fails when a
  header is removed.
- Fixed the banner comment in all 16 files: each named a pre-2025 filename
  (`PAPERSTYLE.STY`, `COLORS.STY`, `MICROTYPE-CONFIG.STY`). These are
  uppercase, so the #46 rename sweep did not reach them.
- Replaced three `% Author: Academic Paper Template Project` placeholders,
  which contradicted the project's own license file.

Headers are comments: `main.pdf` is unchanged, byte for byte, against the
pre-rename baseline. `pytest -q` 32 passed; `tests/run-tests.sh` 115 passed.

Moved to the package-first layout (branch `refactor/rename-lanepaper-46`,
issue #47, ADR-0001):

- `lanepaper/` holds the 16 `.sty` files and nothing else, flattened — the
  `modules/` subdirectory is gone, so `TEXINPUTS` is one entry instead of two
  and the directory is exactly what `l3build install` installs and what a
  `git subtree` pull carries.
- `demo/` holds the CI fixture document: `main.tex`, `preamble.tex`,
  `preamble-natbib.tex`, `titlepage.tex`, `appendices/`, `figures/`, and
  `references.bib`. It is not a starting point for papers.
- `paper/` no longer exists. Its eleven Markdown files moved to
  `docs/package/`, except `MIGRATION.md` and `MODULARIZATION_ACTION_PLAN.md`
  which are historical and moved to `docs/archive/`. `paper/modules/README.md`
  became `docs/package/modules.md` to avoid colliding with `paper/README.md`.
- `TEXINPUTS` now covers `./lanepaper:./demo` and `BIBINPUTS` covers `.:./demo`,
  so `main` and `references.bib` still resolve from the repository root and
  `main.pdf` is still written there. CI needed no path changes as a result,
  including the `upload-artifact` path and the `safe.directory` step.
- `.gitignore`'s figure negation is now `!demo/figures/*.pdf`; verified that a
  PDF there is tracked while other PDFs stay ignored.
- Fixed 16 test fixtures and development documents that loaded
  `\input{paper/preamble.tex}` by path, plus the `prelude-natbib-preamble`
  compatibility probe in `tests/run-tests.sh`.
- Regenerated `docs/PACKAGE_NAMING_CONVENTION.md` from the actual file list and
  repaired five documentation links that the move had broken or silently
  repointed.

Verified by 150dpi raster comparison against the pre-rename baseline. Four of
40 pages differ, each for a stated reason: the title page's `\today` line
(the baseline was built two days earlier), two pages where the demo prints its
own `\usepackage` line, and one where it cites the style guide's new path.
`pytest -q` 31 passed; `tests/run-tests.sh` 115 passed, 0 failed;
`make lint`, `make build`, and the style validator all clean.

Renamed the package to `lanepaper` and unified the internal prefix to `\lnp@`
(branch `refactor/rename-lanepaper-46`, issue #46, ADR-0001):

- `\usepackage{lltpaperstyle}` is now `\usepackage{lanepaper}`. The 16 `.sty`
  files were renamed: `paper/lanepaper.sty` is the package, `lnpminimal` and
  `lnpgridoverlay` are the other entry points, and the 13 modules are `lnp` +
  role. The short prefix follows CTAN practice — `biblatex` ships `blx-*.sty`
  with `\blx@` macros; compare `\MT@`, `\Hy@`, `\Gm@`, `\ttl@`.
- Five competing internal prefixes collapsed into `\lnp@`: `\paper@` (105),
  `\ifllt@` (32), `\llt@` (27), `\paperstyle@` (6), `\lltpaperstyle@` (4) and
  `\lltfontfeatures@` (5). LaTeX kernel macros (`\p@`, `\f@`, `\z@`,
  `\tagform@`, `\maketag@`, `\g@`) are untouched — verified by count.
- The undecorated `\paperstyle*` family (24 macros) went the same way. The 22
  internal ones are now `\lnp@*`; the two entry points a user actually types
  are `\lanepaperdiagnostics` and `\lanepaperinfo`. `\lanepaperinfo` is
  defined but never called anywhere — left in place, worth revisiting.
- Removed 137 `\makeatletter`/`\makeatother` lines from the package files.
  `@` is a letter inside a `.sty` by construction, so each `\makeatother` was
  revoking that for the rest of the file; the old macro names had no `@` so
  nothing noticed. With `\lnp@` names this broke the build outright at 39
  sites. `lnplists.sty` also had one unbalanced `\makeatletter`.
- `tests/test_infrastructure.py` now guards both generations of retired names —
  the pre-2025 `paper/paperstyle` layout and the `llt*` / prefix names — and
  builds its pattern by concatenation so it cannot match its own source.
- `docs/PACKAGE_NAMING_CONVENTION.md` was regenerated from the actual file
  list; it had carried four modules that never existed
  (`lltcompilationfixessimple`, `lltmicrotypeconfig`,
  `lltmathematicsgridlocked`, `llthochulirefinements`) since July 2025.
  `NAMESPACE_CONVENTIONS.md` records why `\lnp@` was chosen over `\lane@`.
- Archival documents keep the old names on purpose: the ADRs, `CONTEXT.md`'s
  glossary, dated reviews and audits under `docs/`, `docs/archive/`,
  `paper/MIGRATION.md`, and this file's history.

Verified by per-page raster comparison at 150dpi against the pre-rename build.
`main.pdf`: 38 of 40 pages byte-identical; pages 4 and 39 differ only where the
demo prints `\usepackage{lltpaperstyle}` in its own code listing, which the
rename is supposed to change. `tests/fixtures/opening-test.tex`, the only
document exercising `\firstlinesc`, is identical on all 5 pages. `pytest -q`
31 passed; `tests/run-tests.sh` 115 passed, 0 failed.

Deleted the stale `.dtx`/`.ins` scaffold (branch `chore/delete-dtx-scaffold-49`,
issue #49):

- Removed `paper/lltpaperstyle.dtx`, `paper/lltpaperstyle.ins`, and
  `paper/README-DTX.md`. The `.ins` declared
  `\generate{\file{lltpaperstyle.sty}{\from{lltpaperstyle.dtx}{package}}}`, but the
  `.dtx` was a 252-line v1.6 scaffold from 2025-07-09 against a shipping `.sty`
  of 3206 lines at v2.0, and it ended with "the rest of the implementation would
  continue here". Running the documented docstrip workflow would have replaced
  the package with a stub.
- Nothing built from them: no reference in `Makefile`, `.latexmkrc`,
  `compile.sh`, the shell harnesses, the pytest suite, or CI.
- CTAN accepts plain `.sty` plus README and documentation; per ADR-0002 the
  release path is `l3build ctan`, not docstrip.
- Surviving `.dtx` mentions are deliberate: LPPL boilerplate in `LICENSE`,
  history in this file, and the dated review records under `docs/`. The
  contradictions in `docs/PACKAGE_ROADMAP.md` belong to issue #52.

Stopped the microtype tracking-list churn (branch `fix/tracking-lists-39`, issue #39):

- `main.log` tracking-override messages: 40 -> 0. Every per-invocation
  `\SetTracking` in an executable macro body is now `\textls`, which states the
  amount at the point of use instead of declaring a global list. The nine
  package-load declarations in `lltmicrotype.sty` are intentional and unchanged.
- The original plan for this issue — declaring named lists at load and selecting
  them per macro — is not possible: microtype provides `name` and `load` for
  declaring and inheriting lists, but no point-of-use selection.
- Most per-site amounts turned out to be inert, clobbered by `\SetTracking`'s
  global scope, and were dropped. Four contexts where the amount really did
  apply keep it explicitly: `\firstlinesc` and `lltparagraphs`' opening (exact
  11pt matches no named-size list), and the three OT1 sites in
  `lltfontfeatures.sty` (every tracking list declares `T1` only).
- Fixed a tracking leak in `\articletitlefootnote`: `\lsstyle` ran unscoped and
  bled past the title into its `\footnote`. It is now `{\lsstyle #1}\footnote{#2}`.
  This is the one intended rendering change.

Verified by per-page raster comparison at 150dpi rather than text extraction,
which cannot see reflow: 39 of 40 pages of `main.pdf` are byte-identical, and
page 1 differs only in the title and thanks-footnote bands. Because `main.tex`
does not exercise `\firstlinesc`, `tests/fixtures/opening-test.tex` was rendered
and compared as well — all 5 pages identical.

Documentation pass over the entry docs (branch `docs/entry-docs-pass`, issue #41):

- Cut `paper/README.md` from 1115 to roughly 690 lines, mostly duplication with
  `README.md` and `API_REFERENCE.md`.
- Corrected the documented font stack. `paper/README.md` claimed
  `newtxmath[libertine]`, `scaled=0.93`, and Bembo; the packages actually loaded
  are tgpagella, zi4 at `scaled=0.96`, newpxmath, and mathalfa
  (`paper/modules/lltfonts.sty`).
- Corrected microtype values (`1050/15/15`, not `1100/10/10`), the `\linespread`
  figure (1.20), the citation style (`authoryear`, not Chicago), and the
  bold-small-caps documentation, which described scaling and a `\balancedbsc`
  command that do not exist.
- Corrected two module classifications that contradicted the loader:
  `lltmicrotype` is always loaded, `lltmathgridlocked` never is.
- Removed a dead `examples/` reference from `INSTALL.md` and a
  `docs/typography/` path that resolved relative to `paper/`.
- Restored documentation for `\smartitalic`, `\smartbold`,
  `\thirdgridparagraphs`, `\refinedbullet`, and `\refineddash`, which an
  earlier draft of this pass had deleted while they remained implemented, and
  marked `\compactpar` and `\loosepars` deprecated to match the code.
- Narrowed claims to what is actually verified: tested TeX Live versions are
  named individually, MiKTeX is marked unverified, and quantum spacing is
  described as covering most rather than all vertical space, since
  `paper/modules/lltheadings.sty` uses 18pt and 6pt.

Cleanup nits (branch `chore/cleanup-nits-32`, issue #32):

- Retargeted `AGENTS.md` §7's dead `CLAUDE.md` reference to `paper/STYLE_GUIDE.md`
  and `docs/typography/`. No `CLAUDE.md` has ever existed in this repository.
- Fixed the BSD-grep `invalid character range` warning emitted by
  `src/sh/validate_latex_style.sh` on every file (43 per run). The math-operator
  bracket expressions used `[=+\-*/]`; BSD grep reads `\` literally inside a
  bracket expression, so this parsed as the reversed range `\`(0x5C)→`*`(0x2A).
- Rewrote that check to exempt subscript and superscript spans before testing
  for unspaced operators. Repairing the bracket expression alone made the check
  fire on `\sum_{i=1}^n` in `main.tex` and `tests/fixtures/full-features.tex`;
  indices are conventionally unspaced, so those were false positives the broken
  expression had been masking. The exemption is deliberately narrow — exempting
  every brace group would hide real defects such as `$\sqrt{x+y}$` and `${x=y}$`
  — and it tracks brace depth, since indices nest (`x_{\mathrm{i=1}}`).
- Spaced the operator in `\frac{1}{n-1}` at `main.tex:309`, the one genuine hit
  the repaired check found. TeX ignores whitespace in math mode; the rendered
  PDF text is unchanged (verified by `pdftotext` comparison — the PDF's bytes
  differ only through its embedded build timestamp).
- Added regression coverage for the check in `tests/test_infrastructure.py`, in
  all four directions: unspaced operators flag, operators inside brace groups
  still flag, and neither flat nor nested unspaced indices do. The check previously had no
  behavioural test, which is how one that silently malfunctioned went unnoticed.
- Added `poppler-utils` to the CI workflow's apt step. The PDF-text regression
  assertions in `tests/test_regression_harness.py` were skipping silently in CI
  for want of `pdftotext`, so footnote-mark and appendix-title leakage was
  caught only on machines with Poppler installed.

## v2.1.0 — 2026-08-19

Release polish pass (branch `chore/release-polish`):

- Removed byline and IPG attribution from README.md and `pdfauthor` metadata in main.tex.
- Updated tagline: "A living LaTeX template… Actively used and revised."
- Removed "production-grade" phrasing from README.md, main.tex (prose and `\subsection{Production-Grade Features}` heading), paper/README.md, and Makefile comment.
- Rewrote stub bullet in README.md features list with accurate, opt-in-aware claims about `llthochuli` optical refinements.
- Deleted research-repo scaffolding: `.env.example`, `data/raw/.gitkeep`, `data/processed/.gitkeep`; removed dead `cp .env.example .env` instructions from README.md and SECURITY.md; removed `touch .gitkeep` from `make setup` target.
- Updated Version History in README.md to `v2.1.0`.
- Fixed stale module filenames in paper/README.md module tree.

Added GitHub Actions CI workflow (branch `ci/build-and-test`, merged 2026-08-19): build, lint, and test gates now run on push and pull request.

## 2026-08-18

Pre-release hygiene batch (branch `chore/pre-release-hygiene`):

- Fixed `tests/fixtures/opening-test.tex`: added `\clearpage` before the
  `\section{Conservative Drop Cap Guidelines}` so the `\academicdropcap{W}{…}`
  call no longer falls at the bottom of page 3 where lettrine emits
  `*** ATTENTION REQUIRED ***`. Suite now reports 0 failures.
- Fixed `.gitignore`: `!figures/*.pdf` carried a trailing inline comment
  (`# …`), which git does not parse — the negation was silently inert. Moved
  the comment to its own preceding line; `git check-ignore -v figures/test.pdf`
  now returns the negation rule. Dropped `!tests/visual/output/*.pdf` entirely:
  those PDFs are regenerated on every `tests/run-tests.sh` run and should stay
  ignored.
- Removed 21 tracked internal-workspace files (`archive/**`, `tmp/ai-plans/**`,
  `docs/superpowers/plans/**`, `docs/tmp/plans/**`, `docs/ai-workflow/**`,
  `notes/**`). History retains the full content. Fixed all dead links in
  surviving tracked files that pointed into these paths (README.md,
  docs/README.md, docs/typography/BASELINE-GRID.md,
  docs/typography/BASELINE-GRID-DECISION.md, CHANGELOG.md).
- README.md: removed dead link to `CLAUDE.md` (gitignored, absent for
  cloners) and dead link to deleted plan doc; retargeted Contributing
  section to new `CONTRIBUTING.md`.
- Version reconciliation: bumped `\ProvidesPackage` in `lltcolors.sty`,
  `lltfonts.sty`, and `llthochuli.sty` from `v1.0 [2025/07/0x]` to
  `v1.1 [2026/08/12]` to align with the 2026-08-12 release date shared by
  all other modules; `lltpaperstyle.sty` (`v2.0`) and `lltmicrotype.sty`
  (`v1.2`) are unchanged.
- Added `CONTRIBUTING.md`: build (`make`), test suites (`bash tests/run-tests.sh`,
  `python3 -m pytest -q`, `make test`), `llt` namespace convention, and
  module doc locations.

## v2.0.0 — 2026-08-12

Release cut after the adopter defect report (see git history:
`notes/ADOPTER-DEFECT-REPORT-2026-08-11.md`). Two breaking changes:
`\sectionbreak` → `\sectionsep` and `\paragraphbreak` → `\paragraphsep`
(no aliases — the old names collide with titlesec's `\<level>break` hook and
must not be defined), and the `\le`/`\ge`/`\epsilon`/`\phi`/`\vec`
redefinitions moved behind the new `mathredefs` option (default off).
Migration: `paper/MIGRATION.md`.

All 2026-08-12 entries below constitute the release.

## 2026-08-12

- Fixed the three pre-existing overfull hboxes in the `main.tex` demo prose
  (8.2pt section heading, 16.8pt and 49.5pt `verbatim` examples) by
  rewording/reformatting demo content only — no template tolerance touched.
  `main.log` now reports zero overfull hboxes.

- **Breaking rename:** `\sectionbreak` → `\sectionsep` and `\paragraphbreak` →
  `\paragraphsep`. titlesec executes any defined `\<level>break` macro as a
  hook during heading construction; `\paragraphbreak` made run-in `\paragraph`
  fail with "perhaps a missing `\item`", and `\sectionbreak` silently injected
  `\vspace{2\gridunit}` (26.4pt) before every `\section` in place of the
  intended `\@secpenalty`. After the rename, section spacing matches the
  declared `\titlespacing` values — rendered output loses the accidental
  26.4pt per-section gap and regains break-before-section penalties.
- Removed `\SetTracking`/`\lsstyle` from the `\titleformat` blocks for
  `\section` and `\subsection`: `\SetTracking` is global and the package's own
  microtype `series=b` rule annulled the declared +80/+60 heading tracking, so
  the lines were dead code that also churned the tracking list document-wide
  (122 override messages per build).
- Fixed run-in `\paragraph` emitting zero space before the following text
  ("RobustnessEstimates"): dropped the `[~]` after-code and set the
  `\titlespacing` after-value to `0.75em` (same fix applied to `\paragraphsc`).
- Filed the adopter defect report (see git history: `notes/ADOPTER-DEFECT-REPORT-2026-08-11.md`).
- Harness hardening: `make lint` now covers `paper/` and `appendices/` (was
  root-only) and probes `-n48` support so ChkTeX 1.7.6 (TeX Live 2022) no
  longer fails the gate; committed the missing `src/sh/check-packages.sh`
  and made `make check-deps` fail loudly instead of echoing a fake-healthy
  fallback; fixed `src/sh/validate_latex_style.sh` (errexit killed it on the
  first diagnostic, paths escaped the repo root, and it checked another
  project's files); rewrote the TESTING.md log-analysis section that
  documented a never-committed `context/tools/log-parsing/` toolchain;
  added `tests/test_measured_values.py` — compile-time assertions on the
  measured `\baselineskip` (16.32pt), `\jot` (9.9pt), `\footnotesep` (inert
  floor), canonical penalties, and the `\DeclareMathSizes` firing — the
  regression net the defect report called for. Gates verified on both
  TeX Live 2022 and 2026; TROUBLESHOOTING documents the stale-aux failure
  when switching TeX Live versions.
- Deleted silently overridden duplicate assignments: `\spaceskip`/`\xspaceskip`
  (0.35em/0.5em declared early, 0.33em/0.48em in force), `\brokenpenalty`
  (5000 → 2000 in force), `\postdisplaypenalty` (10000 → 2000 in force), and
  the duplicate `\raggedbottom`, `\parindent`, and `\arraystretch`/`\tabcolsep`
  defaults. The in-force values were kept, so rendering is unchanged
  (verified: measured values byte-identical before/after). Widow/orphan
  penalties now have one canonical home in `lltpaperstyle.sty` (10000/10000/
  10000); the `lltheadings` and `lltcompilationfixes` restatements are gone,
  and the gridlocked modules' softer penalties (5000) are documented as an
  intentional grid-mode variant regime.
- Footnote machinery: marker box widened 7pt → 11.5pt (body and title-page
  blocks). Measured at the marker's spec, Pagella's tabular old-style digits
  are 3.6pt each: two-digit markers (7.2pt) already overflowed the 7pt box
  (hidden by `\hfuzz`) and three-digit markers (10.8pt) overprinted note
  text; wrapped-line indent matches the wider box. Rendered delta: footnote
  text shifts right 4.5pt (single-digit gap 3.4pt → 7.9pt, two-digit gap
  → 4.3pt). Dropped footmisc's inert `hang,flushmargin` options
  (Lane's own `\@makefntext` replaced their implementation) and the inert
  `\footnotemargin` settings; documented `\PassOptionsToPackage` before
  `\usepackage{lltpaperstyle}` as the supported way to pass footmisc options
  such as `bottom` without an option clash. Corrected the `\footnote`
  redefinition comment (the `\nobreak` acts on footnote text, not the mark).
- **Behavior change:** the `\le`/`\ge`/`\epsilon`/`\phi`/`\vec` redefinitions
  moved behind a new `mathredefs` package option, default off. A typography
  package must not change what a manuscript's mathematics says; documents
  relying on the variants should pass
  `\usepackage[mathredefs]{lltpaperstyle}`.
- Fixed `\SetTracking` leaking its tracking amount into PDF bookmarks
  ("1 60Identification Strategy"): the `\pdfstringdefDisableCommands`
  substitution now discards both arguments.
- Corrected the `\hfuzz=0.2pt` comment: it is *looser* than LaTeX's 0.1pt
  default, not "tighter" (value unchanged).
- Split the qpl protrusion lists by encoding: TS1-only symbols
  (`\textdagger`, `\textdaggerdbl`, `\textparagraph`,
  `\textasteriskcentered`, `\texteuro`) moved to a TS1 list, OT1 dropped
  (all twelve symbol keys fail microtype's OT1 slot lookup), brace keys
  re-spelled `\textbraceleft`/`\textbraceright` in the T1 list, and a
  mistyped `\ ` (control space) backslash key spelled `\textbackslash`.
  "Unknown slot number" microtype messages per build: 231 → 0. Intended
  rendering delta: title-page footnote marks (`*`, †, ‡) now actually
  protrude (~1pt left shift); everything else unchanged (39 pages).
- Recorded the baseline-grid decision in
  `docs/typography/BASELINE-GRID-DECISION.md`: re-document the true measured
  values (10.95pt body, 16.32pt baseline) and treat `\gridunit` as a spacing
  quantum, not the document baseline; making the 13.2pt grid real was rejected
  because it requires removing `\linespread` and would shrink documents ~19%.
  Research brief archived in git history as `notes/baseline-grid-decision-brief.md`.
- Re-documented the grid-derived constants to match the measured build
  (decision (b) follow-through; rendering unchanged except where noted):
  every "13.2pt baseline/leading" claim in code comments and docs now states
  the true values (10.95pt body, 16.32pt baseline, 13.2pt spacing quantum);
  the `[grid]` overlay's base lines step at the real `\baselineskip` instead
  of confirming the false premise; `\DeclareMathSizes` is keyed to 10.95pt so
  it actually fires (scriptscript 6.1pt → 6pt, the declared value);
  `\jot` (ships as 9.9pt), `\footnotesep` (inert floor, not inter-note
  space), `\extrarowheight`/table-row (~21.8pt rows), footnote leading (12pt
  actual), and the `\spaceskip` body-size freeze comments now describe what
  the build does. Review sweep also corrected: float-skip values in
  BASELINE-GRID.md (now the measured 13.2/13.2/9.9pt), table-row arithmetic
  (~21.8pt standard), remaining false claims in STYLE_GUIDE,
  CUSTOM_COMMANDS, modules docs, and the `main.tex` demo prose (main.pdf
  demo text now states 10.95pt/16.32pt; 40 pages).

## 2026-07-04

- Removed active documentation claims about unverified external build support,
  keeping the public setup guidance tied to locally verified `latexmk`, `chktex`,
  pytest, and shell-harness checks.
- Replaced stale `paper/paperstyle` examples in installation and troubleshooting
  docs with current `lltpaperstyle` package names while preserving the README
  migration note for older documents.
- Reworked active repository-identity text, testing guidance, docs index,
  supported-version policy, and release/version wording around the Lane LaTeX
  Template.
- Added a root `LICENSE` containing the LPPL v1.3c text, renamed the legacy
  short-notice directory to `licenses/` to avoid a case-folding collision, and
  archived the duplicate troubleshooting guide under `docs/archive/`.

## 2026-07-02

- Added compatibility fixes for natbib entry-point and standalone module contracts:
  `paper/preamble-natbib.tex` now loads `lltpaperstyle` in `natbib` mode and
  uses conditional citation aliases to avoid duplicate command-definition errors;
  the legacy DOI prefix customization is guarded for TeX Live variants without
  `\doiprefix`.
- Reworked `lltpaperstyle` package loading so `inputenc` is loaded lazily before
  bibliography setup and never after manually loaded `biblatex`; documented that
  `nobiblatex` leaves both bibliography and encoding setup to the caller unless a
  modern LaTeX UTF-8 default is sufficient.
- Added explicit standalone dependency declarations for `lltlists` (`graphicx`,
  `etoolbox`) and `lltmathgridlocked` (`etoolbox`) so hooks and marker
  rendering work when loaded outside `lltpaperstyle`.
- Added paragraph preload ownership shims in `lltpaperstyle`/`lltparagraphs` so
  the supported optional-module-before-main-package order remains stable, and
  documented that loading `lltparagraphs` after `lltpaperstyle` is unsupported
  unless the reverse order is fully guarded.
- Repaired standalone module/package surfaces for `lltfontfallbacks` local
  font-availability conditionals, `lltfontfeatures` dash/text-symbol aliases,
  and `lltpaperstyleminimal`'s package-hook dependency on `etoolbox`.
- Marked `.dtx/.ins` usage as non-authoritative in `paper/README-DTX.md` and
  updated compatibility wording in `paper/modules/README.md` and `README.md` for
  the separate `lltpaperstyleminimal` package surface.
- Extended test harnesses with compatibility probes for standalone/preload contract
  paths, including `lltfontfeatures`, and fixed root-level auxiliary artifact
  cleanup for temporary compatibility probes.
- Added manual biblatex-warning enforcement in `tests/test-bibliography.sh`.
- Added regression assertion that `tests/run-tests.sh` executes compatibility
  probes in the pytest harness.
- Hardened compatibility-probe control flow in `tests/run-tests.sh` so all probes
  execute and report cumulative failures before failing the lane harness.
- Removed the stale `lltpaperstyleminimal` option claim from `README.md` package
  options and aligned standalone-module documentation language in
  `paper/modules/README.md` with validated dependency requirements.

## 2026-07-01

- Added a consolidated deep review findings note covering maintainability,
  repository documentation/professionalism, and typography.
- Added a master roadmap plan for turning the deep review findings into
  serialized build, package API, documentation, and typography lane plans.
- Added lane-1 build hygiene fixes: removed malformed ISBN metadata warnings
  from `references.bib`, made `tests/compilation/logs/*.log` transient in
  `.gitignore`, and documented the verification artifact contract.
- Classified `main.log`/`main.blg` warning policy and spacing-integrity check as
  advisory in this lane; updated verification guidance in `README.md`,
  `tests/README.md`, and `docs/technical/TESTING.md`.
- Made `tests/check-spacing-integrity.sh` self-describe as an advisory diagnostic
  that always exits 0 except on genuine tooling errors, matching the documented
  non-gating role (previously it exited 1 on heuristic spacing flags).
- Corrected the `tlmgr install` list in `README.md` to match the fonts actually
  loaded (`tgpagella`, `inconsolata`, `newpx`/newpxmath, `mathalfa`, `booktabs`);
  removed the spurious sans-serif math entry (`newpxsf`, no such package; the
  template loads no sans math).

## 2026-05-28

- Added a LaTeX package code review report focused on maintainability, option contracts, and package API risks.
- Added a checkpointed implementation plan for resolving the LaTeX package maintainability findings.
- Added reviewer findings for the LaTeX maintainability implementation plan.
- Updated the maintainability implementation plan to resolve reviewer findings before implementation.
- Added option-contract regression coverage for `nocolor`, `minimal,nocolor`, `draft`, `natbib`, `nobiblatex`, normal `\ref`, and subsection float-barrier modes.
- Made `nocolor` option-aware by loading semantic colors consistently and mapping template colors to black/grayscale values.
- Implemented native `natbib` mode, preserved `nobiblatex`, and removed the runtime warning wrapper around LaTeX's standard `\ref`.
- Made subsection float barriers an explicit package option with `nosubsectionbarriers` support.
- Consolidated active `microtype` loading and tuning into `lltmicrotype` while preserving default raster output.
- Resolved follow-up P1/P2 review findings for public text-symbol commands and active microtype ownership in `lltmicrotype`.
- Restored legacy emphasis, small-caps, dash, ellipsis, note, divider, and symbol command compatibility covered by existing fixtures.
- Fixed quote/list environment closure, nested `readableitem` labels, dagger recursion, and floatless caption warnings surfaced by the fixture harness.
- Updated LaTeX fixtures to use current package names and a two-pass compile harness for stable hyperref/rerun checks.
- Clarified the canonical bibliography loading contract and documented the manual `nobiblatex` override path.
- Added regression coverage for manually loaded biblatex with `lltpaperstyle[nobiblatex]`.
- Fixed the bibliography test harness package search path for direct fixture runs.
- Documented the Poppler `pdftotext` dependency used by PDF text regression assertions.
- Made the compatibility regression test skip PDF text assertions clearly when `pdftotext` is unavailable.

## 2026-05-27

- Restored optional footnote mark support and appendix section compatibility for starred and short-title forms.
- Added a focused regression fixture for footnote and appendix compatibility backports.
- Restored the repository infrastructure contract so the AGENTS.md lint, build, and regression gates are runnable from the root.
- Resolved the active merge marker in `main.tex` without changing the intended LaTeX layout.
- Updated active build and test references from the removed package name to `lltpaperstyle`.
- Added pytest coverage for build-target drift, executable shell harnesses, root changelog presence, active package references, and the minimal LaTeX regression harness.

## 2024-06-30 and earlier

Folded in from `docs/style/CHANGELOG.md` when the docs were consolidated
(issue #52). It was a second changelog for the style modules, in Keep a
Changelog format, covering history older than anything above. Its entries are
reproduced verbatim; the dates and wording are as they were written.

### Pre-2026 module changelog, unreleased at the time

### Added
- Sophisticated list typography system with multiple environments
- Professional testing framework with visual output validation
- Comprehensive typography documentation
- Grid-aligned table system
- Enhanced citation support with biblatex
- Professional footnote system optimized for TeX Gyre Pagella
- Testing infrastructure with Make targets
- Repository audit documentation

### Changed
- Updated from Bembo (fbb) to TeX Gyre Pagella font system
- Bullet colors adjusted from 45% to 20% gray for better visibility
- Renamed `\endashmark` to `\dashmark` to avoid conflicts
- Improved section heading typography with color and tracking

### Fixed
- LaTeX compilation errors with duplicate command definitions
- Cross-reference warnings in test fixtures
- Bibliography processing in test suite
- Overleaf "Incomplete \iffalse" error by properly protecting @ commands in user macros
- Microtype warnings for unavailable character slots (now gracefully handled)

### v0.1.0 — 2024-06-30

### Added
- Initial LaTeX template with sophisticated typography
- TeX Gyre Pagella font integration
- Modular scale typography system
- Chicago Manual of Style citation support
- Professional appendix management
- Baseline grid implementation
