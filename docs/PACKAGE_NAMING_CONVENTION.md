# Package Naming Convention

The package is **`lanepaper`**. Everything it ships is named from that one word.

## The rule

| What | Name | Why |
|------|------|-----|
| The package a document loads | `lanepaper` | The CTAN name; what `\usepackage` takes |
| Every other `.sty` file | `lnp` + role | Short abbreviation of `lanepaper` |
| Every internal macro | `\lnp@` + role | Same abbreviation, so files and macros agree |
| Public commands | no prefix | See `docs/package/NAMESPACE_CONVENTIONS.md` |

The short abbreviation follows CTAN practice rather than repeating the package
name on every file. `biblatex` is the closest parallel: CTAN name `biblatex`,
shipped files `blx-*.sty`, internal macros `\blx@`. Compare `\MT@` (microtype),
`\Hy@` (hyperref), `\Gm@` (geometry), `\ttl@` (titlesec).

## Entry points

Loaded directly by a document.

| Package | File |
|---------|------|
| `lanepaper` | `lanepaper/lanepaper.sty` |
| `lnpgridoverlay` | `lanepaper/lnpgridoverlay.sty` |
| `lnpminimal` | `lanepaper/lnpminimal.sty` |

## Modules

Loaded by `lanepaper`, by name and never by path.

| Package | File |
|---------|------|
| `lnpcolors` | `lanepaper/lnpcolors.sty` |
| `lnpcompilationfixes` | `lanepaper/lnpcompilationfixes.sty` |
| `lnpdimensions` | `lanepaper/lnpdimensions.sty` |
| `lnpfontfallbacks` | `lanepaper/lnpfontfallbacks.sty` |
| `lnpfontfeatures` | `lanepaper/lnpfontfeatures.sty` |
| `lnpfonts` | `lanepaper/lnpfonts.sty` |
| `lnpheadings` | `lanepaper/lnpheadings.sty` |
| `lnpheadingsgridlocked` | `lanepaper/lnpheadingsgridlocked.sty` |
| `lnphochuli` | `lanepaper/lnphochuli.sty` |
| `lnplists` | `lanepaper/lnplists.sty` |
| `lnpmathgridlocked` | `lanepaper/lnpmathgridlocked.sty` |
| `lnpmicrotype` | `lanepaper/lnpmicrotype.sty` |
| `lnpparagraphs` | `lanepaper/lnpparagraphs.sty` |

## Loading

Load by package name. Paths are not package names:

```latex
\usepackage{lanepaper}        % correct
\usepackage{paper/paperstyle}  % wrong - removed, and never a package name
```

Module resolution depends on `TEXINPUTS` covering `./lanepaper`. That is set in
`Makefile`, `.latexmkrc`, `compile.sh`, `tests/run-tests.sh`, and
`tests/test-bibliography.sh`. Once the package is installed into a texmf tree
via `l3build install`, that is no longer needed.

## Retired names

`tests/test_infrastructure.py` fails the build if any of these reappears in an
active source file:

- `paper/paperstyle`, `paperstyle.sty` - the pre-2025 path-based layout
- `llt*` - the 2025-2026 package names, retired by ADR-0001
- `\paper@`, `\llt@`, `\lltpaperstyle@`, `\lltfontfeatures@`, `\paperstyle@` -
  the four competing macro prefixes, collapsed into `\lnp@`
