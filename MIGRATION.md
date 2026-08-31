# Migrating from lanepaper v2 to v3

Lanepaper v3 is a deliberate breaking contraction, not a compatibility mode.
The package is a typography system with one public entry point; it is not a
library of writing shortcuts or a document framework. There are no v2 aliases
and no option that restores the old surface. A v2 paper therefore needs source
edits before it can use v3. This is the consequence recorded in
[ADR-0006](docs/adr/0006-one-public-entry-point-and-a-narrow-v3-interface.md).

Work through this guide from the preamble to the body. For the commands that
remain, see [API_REFERENCE.md](API_REFERENCE.md). The examples below name the
replacement that owns each responsibility: standard LaTeX, a document-loaded
package, or the retained `lanepaper` behavior.

## 1. Replace the package entry point and options

Load the package once, by its public name:

```latex
\usepackage{lanepaper}
```

The internal `lnp*.sty` files are implementation modules, not independent
entry points. Remove direct module loads and old wrapper packages. The only
package options are `[optical]` and `[nocolor]`:

| Removed surface | v3 action |
|---|---|
| `lnpminimal.sty` | Replace with `\usepackage{lanepaper}`. |
| `lnpgridoverlay.sty` | Delete the development overlay; there is no v3 replacement. |
| `lnpcompilationfixes.sty` | Delete the module. Use standard document tools such as `\resizebox` or `\overfullrule` when needed. |
| `[grid]`, `[nogrid]`, `[minimal]`, `[draft]` | Delete the option. The modes are gone. |
| `[natbib]`, `[nobiblatex]` | Load and configure `natbib` or `biblatex` in the document. |
| `[subsectionbarriers]`, `[nosubsectionbarriers]` | Delete the option. Use standard float placement or load `placeins` in the document if a barrier is required. |

The v3 package loads its six internal modules automatically. A document should
not load `lnpdimensions`, `lnpcolors`, `lnpfonts`, `lnpheadings`, `lnplists`, or
`lnpmicrotype` directly. The deleted font modules have no v3 replacement:

| Removed module | v3 action |
|---|---|
| `lnpfontfeatures.sty`, `lnpfontfallbacks.sty` | Delete the load. Use standard font commands and install the fonts required by the document. |
| `lnphochuli.sty`, `lnpparagraphs.sty` | Delete the load. Their retained behavior is owned by `lanepaper.sty` and `lnpdimensions.sty`. |

## 2. Move document-level package choices into the document

Lanepaper no longer imposes choices about content-level packages. Keep those
choices in the paper's preamble:

- Load `biblatex` or `natbib` and choose its backend, style, and options.
- Load and configure `cleveref` if smart cross-references are wanted.
- Load `babel`, `appendix`, `threeparttable`, `placeins`, `pdflscape`,
  `rotating`, or other document packages only when the paper uses them.
- Use standard `figure`, `table`, `quote`, `quotation`, and `\appendix`
  structures. Lanepaper styles those structures where it owns visible
  typography; it does not provide orchestration wrappers.

The package no longer forces a paper size. The document class chooses Letter or
A4, while v3 keeps the six-inch text measure and centered horizontal margins.

## 3. Replace inline writing and emphasis helpers

The generic writing layer was removed. Replace each helper with the standard
LaTeX command that states the intended meaning:

| Removed command | Use instead |
|---|---|
| `\strongemph`, `\importantnote` | `\textbf` |
| `\meta`, `\person`, `\acro`, `\regsc`, `\elegantsc`, `\refinedsc` | `\textsc` |
| `\critical`, `\bsc`, `\headsc`, `\inlinebsc`, `\elegantscbold` | `\textbf{\textsc{...}}` |
| `\term`, `\work`, `\subtleemph`, `\externalref`, `\smartitalic` | `\emph` |
| `\codecomment` | `\textit` |
| `\code`, `\inlinecode`, `\balancedcode`, `\filepath`, `\var` | `\texttt` |
| `\doccode{a}{b}` | Write `a: \texttt{b}`. |
| `\authorname`, `\affiliation`, `\keywords` | Use the retained title-page commands such as `\articleauthors`, or standard `\textsc`/`\emph`. |
| `\emdash`, `\emdashclassic`, `\dashparen` | `---` |
| `\endash`, `\dashrange{a}{b}` | `--`, or `a--b` |
| `\tdots`, `\fdots`, `\edots` | `\dots` |
| `\ldots`, `\cdots`, `\S`, `\P`, `\copyright`, `\dag`, `\ddag` | Use the standard LaTeX commands; they are no longer Lanepaper-owned. |
| `\thinspace`, `\medspace`, `\thickspace` | Use the standard `amsmath` commands. |
| `\euro`, `\pound`, `\cent`, `\currency` | `\texteuro`, `\textsterling`, `\textcent`, `\textcurrency` |
| `\trademark`, `\registered`, `\servicemark` | `\texttrademark`, `\textregistered`, `\textsuperscript{SM}` |
| `\degrees`, `\half`, `\quarter`, `\threequarters` | `\textdegree`, `\textonehalf`, `\textonequarter`, `\textthreequarters` |
| `\super`, `\sub` | `\textsuperscript`, `\textsubscript` |
| `\sq`, `\dq`, `\nq` | `csquotes`' `\enquote`, or standard LaTeX quotation marks |
| `\wordspace`, `\emspace`, `\twoemspace`, `\abbrspace` | `\quad`, `\qquad`, or `\,` |
| `\fig`, `\tab`, `\unit` | `Figure~\ref{...}`, `Table~\ref{...}`, or a document package such as `siunitx` |

## 4. Use standard document structures

Replace package wrappers with the underlying LaTeX structure. The retained
`\sectionopening{...}` command is an inline typographic opening; it does not
replace ordinary sectioning or paragraph structure.

| Removed surface | Use instead |
|---|---|
| `epigraph`, `emphasisquote`, `\quoteattribution` | Standard `quote` or `quotation`; write attribution text directly. |
| `openingparagraph`, `\firstlinesc`, `\abstractopening` | An ordinary paragraph, optionally beginning with retained `\sectionopening{...}`. |
| `\academicdropcap` and drop-cap support | Ordinary paragraph text or a document-selected package. |
| `\sectionsep`, `\spacebreak`, `\majorsectionspace`, `\thinrulebreak`, `\paragraphsep` | Explicit document-owned spacing where needed. |
| `\sidenote` | `\marginpar` or a document-selected sidenote package. |
| `academicitem`, `compactitem`, `displayitem`, `readableitem` | Standard `itemize`, `enumerate`, or `description`. |
| Public marker, bullet-switching, list-spacing, and list-length helpers | `enumitem` options owned by the document. |
| Float barriers, here-float wrappers, balance helpers, and float diagnostics | Standard `figure` and `table`; load `placeins` if needed. |
| `regressiontable`, caption helpers, panel helpers, and table-note commands | Standard `table`; load `threeparttable` for table notes. |
| Lanepaper's `tablenotes` definition | `threeparttable`'s native `tablenotes` environment. |
| `fignotes`, `\fignote`, `\figurenote`, `\figsource` | Retained `lanepaperfigurenotes` with ordinary text inside. |
| `\startappendices`, `\finishappendices`, `documentAppendices` | Standard `\appendix` or a package loaded by the document. |
| `\lanepaperdiagnostics`, `\lanepaperinfo` | Ordinary LaTeX logs and package inspection tools. |

For lists, use the standard environments directly. The package styles
`itemize`, `enumerate`, and `description`, and retains the `inlineitem`
environment for short parenthetical enumerations.

## 5. Replace the grid and colour APIs

The 13.2pt value remains an internal spacing quantum. It is not a public grid
system, baseline, unit register, or layout API. Replace public grid arithmetic
with the literal length or a standard document-owned setting:

| Removed surface | Use instead |
|---|---|
| `\gridunit`, `\halfgridunit`, `\quartergridunit`, `\threequartergridunit`, `\onehalfgridunit`, `\doublegridunit`, `\triplegridunit` | Write the needed length directly: `13.2pt`, `6.6pt`, `3.3pt`, `9.9pt`, `19.8pt`, `26.4pt`, or `39.6pt`. |
| `\gridmult`, `\gridmath`, `\gridspace`, `\halfbaselinespace`, `\fullbaselinespace` | Use `\vspace{...}` with the length the document needs. |
| `\roundtogrid`, `\gridincludegraphics`, `\imagegridspace`, `gridfigure` | `\includegraphics` in a standard `figure`. |
| `gridtable`, `compactgridtable`, `spaciousgridtable` | Set `\arraystretch` inside a standard `table`. |
| `\standardgrid`, `\compactgrid`, `\spaciousgrid`, `\customgrid` | Set `\arraystretch` directly. |
| `\quartergridparagraphs`, `\thirdgridparagraphs` | Set `\parindent` and `\parskip` directly. |
| `\classicalparagraphs`, `\modernparagraphs`, `\hybridparagraphs` | Set `\parindent` and `\parskip` directly. |
| `grideqnarray`, `gridgather` | `amsmath`'s `align` and `gather`. |

The package palette is private. Do not reference its colour names from a
document. A document that needs its own colours defines them with `xcolor`:

| Removed surface | Use instead |
|---|---|
| Colour names `textblack`, `sectioncolor`, `subsectioncolor`, `subsubcolor`, `paragraphcolor`, `subtlegray`, `quotegray`, `linknavy` | Define document-owned colours with `\definecolor`. |
| `\maincolor`, `\secondarycolor`, `\accentcolor`, `\codeaccent` | Apply document-owned colours with `\color` or `\textcolor`. |

`[nocolor]` is retained, but its v3 meaning is grayscale conversion through
`xcolor`; it preserves the hierarchy between the package's grey levels rather
than flattening every colour to black.

## 6. Replace math and reference wrappers

Use standard mathematics and document-owned reference packages:

| Removed command | Use instead |
|---|---|
| `\real`, `\complex`, `\integer`, `\rational`, `\natural`, `\field`, `\prob` | `\mathbb{R}`, `\mathbb{C}`, `\mathbb{Z}`, and the notation the paper defines. |
| `\hilbert`, `\banach`, `\algebra`, `\topology`, `\measure` | `\mathcal{H}`, `\mathcal{B}`, and document-defined notation. |
| `\norm`, `\abs`, `\inner`, `\set`, `\given` | `\lVert\,\rVert`, `\lvert\,\rvert`, `\langle\,\rangle`, `\{\,\}`, and `\mid`. |
| `\tr`, `\rank`, `\Span`, `\supp`, `\argmax`, `\argmin` | Declare operators with `amsmath`'s `\DeclareMathOperator`. |
| `\mathbinx`, `\mathrelx`, `\dint`, `\ssup`, `\ssub`, and the Lanepaper `\lim` redefinition | Standard `amsmath`; its `\lim` remains standard. |
| `grideqnarray`, `gridgather` | `align` and `gather` from `amsmath`. |
| `\refpage`, `\pref`, `\seeref`, `\seealso` and capitalized forms | Load and configure `cleveref`; use its `\cref`, `\Cref`, and `\cpageref`. |
| `\pdfcode`, `\pdfsc`, `\pdfemph`, `\pdfbf`, `\pdfit`, `\pdffilepath`, `\pdfvar` | `hyperref`'s `\texorpdfstring` when a bookmark needs alternate text. |

Lanepaper still styles standard display mathematics and does not define a
notation vocabulary for a paper. Its typography does not change the ownership
of `amsmath` environments or math symbols.

## 7. Remove obsolete figure, font, and module assumptions

The old demo-side `landscape.tex`, `preamble-natbib.tex`, and
`appendices/api_examples.tex` are not part of v3. Delete their inputs from a
paper rather than looking for a replacement package command. In particular,
replace demo-defined `landscapetable` and `landscapefigure` environments with
standard `table` and `figure` floats, adding document-owned `pdflscape` or
`rotating` only when the paper genuinely needs it. Configure the bibliography
in the document preamble instead of inputting the alternate natbib preamble.

The old numeral and font-feature controls are also gone:

| Removed surface | v3 action |
|---|---|
| `\oldfigs`, `\textfigs`, `\liningfigs`, `\tablefigs`, `\tabularfigs` | Accept the default lining tabular figures, or use explicit `\oldstylenums{...}` in document-owned typography. |
| `\textsup`, `\supfigs`, `\inffigs`, `\chemform` | Use standard `\textsuperscript`, `\textsubscript`, or math markup. |
| `\nolig`, `\breaklig`, `\shelfful`, `\cufflink`, `\textuppercase`, `\textlowercase` | Use standard text commands or document-owned font configuration. |

The supported production baseline is pdfTeX with TeX Live 2025. The package's
Pagella, Inconsolata, and math stack is loaded by `lanepaper`; another engine
requires a different document/package choice rather than a v3 compatibility
flag.

## 8. Finish the paper migration

Before compiling, check the paper from top to bottom:

- [ ] There is one `\usepackage{lanepaper}` and no direct `lnp*.sty` load.
- [ ] Only `[optical]` and `[nocolor]` are passed to Lanepaper.
- [ ] Bibliography, cross-reference, language, appendix, table-note, and float
      packages are loaded and configured by the document.
- [ ] Headings, lists, quotations, figures, tables, mathematics, and footnotes
      use standard LaTeX structures or the retained commands in
      [API_REFERENCE.md](API_REFERENCE.md).
- [ ] Tables use `booktabs` without vertical rules; figure captions are below
      figures and table captions are above tables.
- [ ] No removed command, environment, option, module, or colour name remains.
- [ ] Compile with `make build`, then run `make lint` and `make test`.

There is no compatibility alias to discover after these edits. If a command is
not in [API_REFERENCE.md](API_REFERENCE.md), it belongs to standard LaTeX or to
a package the document must load itself.
