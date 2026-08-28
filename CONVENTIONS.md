# Conventions for package code in `lanepaper/`

How the package is written. The rules below are already in the code but were
nowhere written down, so each contributor re-derived them — and the most likely
wrong guess is importing modern CTAN expl3 conventions, which do not apply here.

Counts and line anchors were measured against the tree at the time of writing.
Re-measure before relying on one; do not copy a number out of this file into a
commit message without checking it.

Where a rule is **not yet met**, this document says so and names the issue that
fixes it. Nothing here should be read as a description of compliance.

---

## 1. LaTeX2e baseline

**This is a classic LaTeX2e package, not an expl3 package.** No
`\ExplSyntaxOn`, `l3keys`, `l3msg`, or `xparse` appears anywhere in
`lanepaper/*.sty` — measured at 0 occurrences. Do not introduce them.

The format floor is **2020/10/01**, the release that made `\AddToHook`
format-native; both entry points declare it.

Options are `\newif` + `\DeclareOption` + `\ProcessOptions`: the 8 option
flags are declared at `lanepaper/lanepaper.sty:166-176` and the options
themselves at `179-195`. (The file holds 13 `\newif` in total; the other 5 are
internal state, not options.) Guards are `\@ifpackageloaded` and
`\@ifundefined`.

The l3build question is settled and is not reopened here: see
[ADR-0002](docs/adr/0002-l3build-for-packaging-pytest-for-tests.md). l3build is
for packaging and release; pytest is the test harness.

## 2. Engine

**pdfLaTeX only.** The font stack is 8-bit and pdfTeX-shaped — T1 `fontenc`,
`utf8` `inputenc`, `newpxmath`, `mathalfa`, `zi4`, Type1 `tgpagella` — with no
`fontspec` path, and `microtype` font expansion is unsupported on XeTeX.

Both documented entry points (`lanepaper`, `lnpminimal`) carry an engine guard
that stops the run with one `\PackageError` naming the package. Do not add a
compatibility layer for another engine without changing the font stack first.

## 3. Naming

| What | Name | Example |
|------|------|---------|
| The package a document loads | `lanepaper` | `\usepackage{lanepaper}` |
| Every other `.sty` file | `lnp` + role | `lnpcolors.sty`, `lnpfonts.sty` |
| Every internal macro | `\lnp@` + role | `\lnp@listhalfbaseline` |
| Public commands | **no prefix** | `\tightlists`, `\spacioussections` |

`lnp` abbreviates `lanepaper`, and the same abbreviation names both the module
files and the internal macros so the two agree. It is deliberately short
because that is how CTAN packages do it: `\MT@` (microtype), `\Hy@` (hyperref),
`\Gm@` (geometry), `\ttl@` (titlesec). `biblatex` is the closest parallel to
this package's layout — CTAN name `biblatex`, shipped files `blx-*.sty`,
internal macros `\blx@`.

`\lanepaper@` was rejected as too long for something appearing on every
internal identifier. `\lane@` was rejected for dropping half the package name.
`lnp` is less immediately readable than either; that cost was accepted
deliberately in exchange for matching what a CTAN reviewer expects. See
[ADR-0001](docs/adr/0001-package-first-with-separate-template.md).

Use `\lnp@` for internal lengths, temporary variables, helper commands,
counters, and boxes — anything with a generic name. Do not prefix environment
names or colour definitions; LaTeX and `xcolor` manage those namespaces.

The prefix is not a licence to be vague: name for the job, not the type.
`\lnp@listitemspacing` says what it controls; `\lnp@temp` says nothing and will
collide with the next person's `\lnp@temp`. Group related definitions together
so the set is visible at once.

When a public name has to change, keep the old one as an alias and mark it in
the same line that defines it, so the removal is findable later:

```latex
% Compatibility alias — DEPRECATED, remove in the next major release
\let\oldname\newname
```

Entry points are loaded directly by a document: `lanepaper`, `lnpminimal`,
`lnpgridoverlay`. Everything else is a module, loaded by `lanepaper` **by
package name, never by path**.

| Module | Purpose | Requires |
|---|---|---|
| `lnpcolors.sty` | Professional Color System | xcolor |
| `lnpcompilationfixes.sty` | Simple Compilation Fixes | — |
| `lnpdimensions.sty` | Page Layout and Spacing | geometry |
| `lnpfontfallbacks.sty` | Font Fallback System | amssymb, courier, mathpazo, mathptmx, newpxmath, palatino, tgpagella, zi4 |
| `lnpfontfeatures.sty` | Font Features Module | textcomp |
| `lnpfonts.sty` | Font System Configuration | amsmath, amssymb, fontenc, inputenc, letterspace, mathalfa, newpxmath, scalefnt, textcase, textcomp, tgpagella, zi4 |
| `lnpgridoverlay.sty` **(entry point)** | Visual Grid Overlay System | calc, eso-pic, tikz, xcolor |
| `lnpheadings.sty` | Heading Typography System | etoolbox, lnpcolors, lnpdimensions, titlesec |
| `lnphochuli.sty` | Hochuli Optical Refinements | lnpdimensions, microtype, ragged2e |
| `lnplists.sty` | List Typography System | enumitem, etoolbox, graphicx, lnpcolors, lnpdimensions |
| `lnpmicrotype.sty` | Microtype Configuration | microtype |
| `lnpminimal.sty` **(entry point)** | Minimal Typography | amsmath, amssymb, array, booktabs, caption, enumitem, etoolbox, fontenc, geometry, graphicx, iftex, inputenc, tgpagella, titlesec, xcolor, zi4 |
| `lnpparagraphs.sty` | Paragraph Typography | etoolbox, lettrine, lnpcolors, lnpdimensions |

Loading a module on its own works where its own `\RequirePackage` line covers
its dependencies; the table above is generated from those lines, not
maintained by hand. Module resolution depends on `TEXINPUTS`
covering `./lanepaper`, which the `Makefile`, `.latexmkrc`, `compile.sh`, and
the test scripts all set; once installed into a texmf tree that is no longer
needed.

`tests/test_infrastructure.py` fails the build if a retired name reappears in
an active source file: the pre-2025 path-based layout, the `llt*` package
names, and the five macro prefixes collapsed into `\lnp@`.

## 4. Public versus private API

The prefix is the boundary. `\lnp@foo` is private and may change without
notice. A prefix-free macro is public: it is part of the contract, it belongs
in `API_REFERENCE.md`, and removing or changing its signature is a breaking
change.

The package's own diagnostic entry points carry the full package name because
that is what a user types: `\lanepaperdiagnostics`, `\lanepaperinfo`.

**Known gap, unowned by any issue.** Prefix-free public names are safe inside
one repository but weak in a shared texmf tree, where `\centeredpar`,
`\dialogue`, or `\forceindent` could collide with another package. This is a
namespacing question, not a robustness one, so #55 does not cover it. Worth
settling before CTAN submission.

## 5. Message policy

Every message names its package and states a remedy.

| Macro | Use when | Current uses |
|-------|----------|--------------|
| `\PackageError` | The document cannot produce correct output | 2 |
| `\PackageWarning` | Output is produced but something was substituted or skipped | 10 |
| `\PackageInfo` | Log-only detail a user did not ask for | 13 |

The engine guard is the worked example: it names the package, says what is
wrong, and ends with `Compile with pdflatex.` A message that states a problem
without a remedy is incomplete.

## 6. Package-code style

**Never write `\makeatletter` or `\makeatother` in a `.sty` file.** This is the
most important rule here, and it reverses advice that was in this repository
for a year.

A `.sty` already has `@` as a letter by construction. A stray `\makeatother`
silently revokes that for the rest of the file. 137 such lines sat harmless
while the internal prefixes contained no `@`; the moment the prefix became
`\lnp@`, the build failed with `Command \lnp already defined`. All 137 were
removed and `lanepaper/` now contains **0**. They are only correct in a `.tex`
document, where `@` is not a letter.

**`\@ifundefined{name}` takes a name without a backslash.** A rename sweep
driven by `\`-prefixed patterns skips it silently. Two sites survived the
`\lnp@` rename testing the *old* name while defining the new one, which would
have caused a double `\newif` on reload. Grep `\@ifundefined` separately after
any rename.

**Trailing `%`.** End a line inside a macro definition with `%` wherever a line
break would otherwise emit a space.

**Glue values start with a coefficient, never a bare register.** In
`\abovedisplayskip=\gridunit plus 3.3pt`, TeX copies the register and ends
the assignment — `plus 3.3pt` leaks into the document as text. Write
`1\gridunit plus 0.25\gridunit`; the coefficient form is scanned as a
dimension, after which `plus`/`minus` parse. Point literals never had this
trap, so it appeared only when spacing moved to `\gridunit` terms
(ADR-0005).

Document source style — as opposed to package code — is covered by
[`CONTRIBUTING.md`](CONTRIBUTING.md) and enforced by
`src/sh/validate_latex_style.sh`. Do not restate it here, and
do not "simplify" that script's math-spacing check back to a bracket
expression; it is a depth-tracking scan and `tests/test_infrastructure.py`
covers it in four directions.

## 7. The `%% FIX:` comment convention

`%% FIX:` marks a deliberate, non-obvious decision that must not be
"simplified" away. It appears **116** times across `lanepaper/`. Treat one as
you would a test: if you are about to remove the code it guards, find out why
it is there first. Add one when you make a choice whose reason is not evident
from the code.

## 8. Robustness

Any macro a user can place in a heading, caption, or PDF bookmark must be
robust, because it will be written to and re-read from the `.aux` file.

The mechanism (#55): definitions stay `\newcommand` — so a name collision
with another package still errors at load time — and every module ends with a
`ROBUSTNESS (#55)` block that applies etoolbox `\robustify` (e-TeX
`\protected`) to each public macro, guarded by `\ifdefmacro` for names that
resolve to registers in some load orders. A new public macro is not done until
its name is in that block. **372** macros are robustified across the 14
modules; re-measure rather than copying that number.

Robustness does not make formatting valid inside PDF bookmark strings — the
`\pdfstringdefDisableCommands` block in `lanepaper.sty` supplies plain-text
fallbacks for that, and stays. `tests/fixtures/robustness-test.tex` is the
contract: package macros in a section title, a caption, a footnote, and PDF
bookmarks, compiled twice.

## 9. Hooks and load order

**Use the LaTeX2e hook system. `\AtBeginDocument` is banned** and
`tests/test_infrastructure.py` fails if one returns.

`\AtBeginDocument` runs its callbacks in registration order, which makes
precedence an accident of file layout. That bit for real: deferring the cleveref
block in #48 inverted a `\crefname` precedence that had held for a year, because
two `\AtBeginDocument` hooks set the same name and the later registration won.
It changed rendered output and no test caught it — only raster comparison did.

The package uses `\AddToHook{begindocument}` at **6** sites and package hooks at
**5**. Nothing depends on registration order any more, so there is no
`\DeclareHookRule` anywhere; adding rules for hooks that touch disjoint state
would be noise, not safety.

### The package configures; it does not load

[ADR-0003](docs/adr/0003-configure-if-loaded-dependency-policy.md) governs, and
#48 implemented it. Three rules for any dependency:

1. **Load** what implementing the typography requires.
2. **Configure if loaded**, never load, anything the document is entitled to
   own: `hyperref`, `biblatex`, `babel`, `appendix`, `longtable`, `tabularx`.
3. **Neither** — delete it, or move it to the document. The landscape and
   rotation conveniences went this way, taking `pdflscape`, `rotating` and
   `adjustbox` with them; v3 (issue #84) moved `cleveref` here too, so
   cross-references are fully document-owned and the package no longer
   configures cleveref.

A style package that loads `hyperref` dictates load order to every document
using it. That is gone: **the package no longer imposes any load order.**

Consequences that are not merely "less styling", and that a new configure-if-loaded
rule must respect:

- **Use the package's own load hook, not a check.** `\AddToHook{package/hyperref/after}{...}`
  fires exactly when hyperref loads — before or after this package — and never
  fires if it is absent. It replaced an `\AtBeginDocument` + `\@ifpackageloaded`
  pair that worked but put the timing back in the author's hands. An inline
  `\@ifpackageloaded` is simply wrong here: `hyperref` is conventionally loaded
  late, usually after this package, so the check runs first and configures
  nothing.
- **Never call a command the optional package owns without a guard.**
  `\startappendices` called `\phantomsection`, which is hyperref's; it was
  always defined while the package loaded hyperref, and became a fatal
  undefined control sequence for a bare document. `\providecommand` it.
- **Distinguish a path the document chose from one it did not.**
  `\phantomsection` sat on `\startappendices`' fallback branch, which a bare
  document reaches without asking, so it is guarded with `\providecommand`: a
  document that never loaded the optional package must not hit an undefined
  control sequence from a fallback path. (v3, issue #84, removed the cleveref
  wrappers — `\refpage`, `\pref`, `\seeref`, `\seealso` and friends — that used
  to illustrate the opposite, deliberately-unguarded case; the package now ships
  no cleveref-dependent command.)
- **Dropping a package can change line breaking.** The measured `\spaceskip`
  values in this package were tuned with `babel` loaded. Without it, every
  line of `tests/fixtures/opening-test.tex` re-breaks. Documents wanting the
  measured typography should load `babel`.

`[natbib]` and `[nobiblatex]` are **deprecated** and inert: with no bibliography
package loaded there is nothing for them to switch. They remain declared so
existing documents get a warning rather than an "Unknown option" error.

## 10. Lint policy

`make lint` runs ChkTeX with these classes suppressed: **W01, W03, W08, W11,
W13, W18, W24, W36, W39, W42, W46, W48** (the `-n` flags in `AGENTS.md`).

They are suppressed because they fire on intentional template constructs, and
silencing them narrowly is preferred to changing rendered output. **Revisit
them only in a visual or editorial pass where rendered output changes are
explicitly allowed** — not as a drive-by lint cleanup.

`-n48` requires ChkTeX ≥ 1.7.7; older binaries reject it and the Makefile
probes for support before passing it.

## 11. Versioning

Git tags are semantic (`v2.1.0`). `\ProvidesPackage` strings are LaTeX
date+version and are *not* the same number: currently 14 modules at `v1.1`, one
at `v1.2`, and `lanepaper.sty` at `v2.0`.

Keep the LaTeX date+version form. Every `\ProvidesPackage` date is synced on
release.

## 12. Licensing

Every file in `lanepaper/` carries an LPPL 1.3c header naming the maintainer
and the maintenance status. `tests/test_infrastructure.py` fails if one is
missing, so a new module cannot skip it. The licensed Work is the contents of
`lanepaper/` — `demo/`, `docs/`, and `tests/` are not part of what ships.

## 13. Out of scope

expl3 naming, `l3keys`, `l3msg`, and `l3doc` are deliberately not used; see §1.
The l3build decision is in ADR-0002 and is not restated here.
