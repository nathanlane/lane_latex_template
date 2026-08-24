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

Entry points are loaded directly by a document: `lanepaper`, `lnpminimal`,
`lnpgridoverlay`. Everything else is a module, loaded by `lanepaper` **by
package name, never by path**. Module resolution depends on `TEXINPUTS`
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

Document source style — as opposed to package code — is covered by
[`docs/guides/LATEX_STYLE_STANDARDS.md`](docs/guides/LATEX_STYLE_STANDARDS.md)
and enforced by `src/sh/validate_latex_style.sh`. Do not restate it here, and
do not "simplify" that script's math-spacing check back to a bracket
expression; it is a depth-tracking scan and `tests/test_infrastructure.py`
covers it in four directions.

## 7. The `%% FIX:` comment convention

`%% FIX:` marks a deliberate, non-obvious decision that must not be
"simplified" away. It appears **116** times across `lanepaper/`. Treat one as
you would a test: if you are about to remove the code it guards, find out why
it is there first. Add one when you make a choice whose reason is not evident
from the code.

## 8. Robustness — **not met**

Any macro a user can place in a heading, caption, or PDF bookmark must be
`\DeclareRobustCommand`, because it will be written to and re-read from the
`.aux` file.

Current state: **2** `\DeclareRobustCommand` in the whole package, and both are
on *internal* macros (`\lnp@textapprox`, `\lnp@textinfty` at
`lanepaper/lanepaper.sty:457-458`). **No public macro is robust**, against
roughly 315 prefix-free `\newcommand` definitions. `\protected` is used 0
times.

Issue #55 is the fix. Until it lands, this section states the rule, not the
practice.

## 9. Hooks and load order — **not met**

The 2e-native hook is `\AddToHook`, which makes ordering explicit. The package
uses `\AtBeginDocument` at **8** sites and `\AddToHook` at **0**. (A plain grep
reports 11 — three of those are comments, not registrations.) Issue #56 is the
migration.

**The load-order contract is currently only a source comment.** The package
loads `hyperref` and then `cleveref` at `lanepaper/lanepaper.sty:2129-2130`
(`cleveref` must follow `hyperref`). A document wanting its own `hyperref`
options must therefore load it first or use `\PassOptionsToPackage`.

That contract is scheduled to disappear. [ADR-0003](docs/adr/0003-configure-if-loaded-dependency-policy.md)
rules that the package **configures third-party packages and does not load
them**: `hyperref`, `cleveref`, `biblatex`, `babel`, and `appendix` become
configure-if-loaded via `\@ifpackageloaded`, never `\RequirePackage`. A style
package that loads `hyperref` itself dictates load order to every document that
uses it, which is the single most likely thing to break an adopter. Issue #48
implements it.

Three rules from that ADR govern any new dependency:

1. **Load** what implementing the typography requires.
2. **Configure if loaded**, never load, anything the document is entitled to own.
3. **Neither** — delete it, or move it to the demo.

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
