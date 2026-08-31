# Lanepaper v3 API Reference

Reference for the retained commands, environments, options, and document-owned
integration points of the `lanepaper` package.

## Table of Contents

1. [Package Options](#package-options)
2. [Title Page Commands](#title-page-commands)
3. [Typography Commands](#typography-commands)
4. [Spacing Commands](#spacing-commands)
5. [Emphasis and Semantic Commands](#emphasis-and-semantic-commands)
6. [List Environments](#list-environments)
7. [Quotation Environments](#quotation-environments)
8. [Table and Figure Environments](#table-and-figure-environments)
9. [Mathematical Commands](#mathematical-commands)
10. [Cross-Reference Commands](#cross-reference-commands)
11. [Paragraph Commands](#paragraph-commands)
12. [Color Commands](#color-commands)
13. [Quick Reference Card](#quick-reference-card)
14. [Bibliography and citations](#bibliography-and-citations)
15. [The font system](#the-font-system)
16. [The colour system](#the-colour-system)
17. [Page layout and dimensions](#page-layout-and-dimensions)
18. [The heading system](#the-heading-system)
19. [The list system](#the-list-system)
20. [How the package is put together](#how-the-package-is-put-together)
21. [Migration from v2](#migration-from-v2)

## Package Options

### Loading the Package

```latex
\usepackage[options]{lanepaper}
```

### Available Options

`\usepackage{lanepaper}` is the sole public load path (ADR-0006), and it takes
two options. Anything else is rejected with LaTeX's own `Unknown option`
error; see the [migration guide](MIGRATION.md) for the v2 option changes.

| Option | Default | Description |
|--------|---------|-------------|
| `optical` | off | Sourced optical refinements over the defaults; currently last-line runt control |
| `nocolor` | off | Convert the palette through xcolor's gray model, keeping its hierarchy |

`optical` is for refinements with a stated source that are not safe to impose
on every document. Runt control caps `\parfillskip`'s stretch so a paragraph's
last line reaches at least a third of the measure (Hochuli, *Detail in
Typography*); the cost is that a paragraph which cannot be rebroken pays in
interword spacing instead. Widow and orphan protection is deliberately *not*
behind this option — it is a default every document gets.

### Examples

```latex
% Standard usage
\usepackage{lanepaper}

% Sourced optical refinements
\usepackage[optical]{lanepaper}

% Single-ink printing
\usepackage[nocolor]{lanepaper}

% Both
\usepackage[optical,nocolor]{lanepaper}
```

## Title Page Commands

### Main Title Commands

#### `\articletitle{title}`
Displays an article title in the package's 22pt title style.

```latex
\articletitle{The Impact of Typography on Academic Writing}
```

#### `\articletitlefootnote{title}{footnote}`
Article title with acknowledgment footnote.

```latex
\articletitlefootnote{Typography in Academic Papers}{We thank the reviewers for helpful comments.}
```

#### `\articletitlecompact{title}`
Fixed 16pt title for papers with many authors.

```latex
\articletitlecompact{A Short Title for a Paper with Many Authors}
```

#### `\articletitlecompactfootnote{title}{footnote}`
Fixed 16pt title with an acknowledgment footnote.

```latex
\articletitlecompactfootnote{A Compact Title}{We thank the reviewers.}
```

### Author and Metadata Commands

#### `\articleauthors{names}`
Display author names with proper spacing.

```latex
\articleauthors{Jane Smith\footnote{University, email@example.edu} 
  \authorspace John Doe\footnote{Institute, john@example.edu}}
```

#### `\articledate{date}`
Display article date.

```latex
\articledate{\today}
```

### Abstract and Keywords

#### `articleabstract` environment
Creates a narrow abstract block using 72% of the text width.
- **Label:** "ABSTRACT" in enhanced small caps
- **Font size:** 10pt (small)
- **Internal spacing:** 0.5 title-space quantum

```latex
\begin{articleabstract}
This paper examines the role of typography in enhancing academic communication...
\end{articleabstract}
```

#### `\articlekeywords{keywords}`
Display keywords with refined punctuation.

```latex
\articlekeywords{typography, LaTeX, academic writing, document design}
```

#### `\articlejel{codes}`
Display JEL classification codes.

```latex
\articlejel{C01, D02, E03}
```

### Title Page Footnote Management

Use these commands as a pair around title-page content. The setup selects
symbolic title-page marks and tighter title-page spacing. The reset resets the
counter and deliberately restores Lanepaper's main footnote style: oldstyle
Arabic marks, main spacing, main footnote text formatting, and the standard
footnote rule. This is an opinionated reset, not a restoration of the
document's prior state; it overrides any document-defined `\thefootnote` or
other footnote formatting that was active before `\titlefootnotesetup`.

```latex
\titlefootnotesetup
% ... title page content ...
\titlefootnotereset
```

#### `\titlefootnotesetup`
Switch to symbol footnotes (*, †, ‡) and tighter spacing for the title page.

#### `\titlefootnotereset`
Deliberately restore Lanepaper's main footnote style after the title page,
including oldstyle Arabic marks, main spacing, formatting, and rule. This
overrides any document-defined `\thefootnote` or other footnote formatting
that was active before `\titlefootnotesetup`.

Outside the title page, footnote marks are 6pt oldstyle figures with their
native spacing, and footnote text is 8.5pt on a 10pt nominal baseline. The
package's 1.20 line spread makes that a 12pt baseline in the document. The
title-page setup keeps these sizes, changes the marks to symbols, and uses
tighter spacing.

#### `\multiplefootnotes{marks}`
Places consecutive marks in one superscript with a small inter-mark kern.
Use it when a reference needs several footnote marks together.

#### `\elegantauthor{name}`
Individual author name with consistent title-page sizing.
- **Size:** 12pt/14pt
- **Style:** Regular text
- **Usage:** Within `\articleauthors` if desired

## Typography Commands

### Section Opening Styles

#### `\sectionopening{opening text}`
Styles its one argument in small caps at the start of a paragraph. Following
text stays in that same paragraph.

```latex
\sectionopening{This opening text appears in small caps,} while the rest
of the paragraph continues in normal text.
```

## Spacing Commands

### The Spacing Quantum

Nearly all of the package's vertical spacing is a multiple of one **13.2pt
quantum**. It is an internal implementation value, not a public length or grid
API. A document states the space it wants:

```latex
\vspace{13.2pt}   % One quantum
\vspace{26.4pt}   % Two quanta
\vspace{6.6pt}    % Half a quantum
```

The quantum is not the baseline: the body sets 10.95pt on a **16.32pt**
baseline (`\linespread{1.20}` scaling the class's 13.6pt under the `11pt`
option). See [ADR-0004](docs/adr/0004-baseline-grid-is-a-spacing-quantum.md).

### Special Spacing Commands

#### `\authorspace`
Space between author names (4.5% of text width).

#### `\titlespacemajor` length
Major title spacing, set to 26.4pt (2 quanta).

#### `\titlespaceminor` length
Minor title spacing, set to 19.8pt (1.5 quanta).

#### `\titlespaceinter` length
Inter-element spacing, set to 13.2pt (1 quantum).

#### `\authorspacer` length
The length used by `\authorspace`; it defaults to 4.5% of the text width.

#### `\titlepagewidth` length
The width used by the abstract, keyword, and JEL blocks; it defaults to 72%
of the text width.

#### `\goldenratio`
The package-defined numeric constant `1.618`.

#### `\goldenratioMinor`
The package-defined numeric constant `0.618`.

#### `\modularscale`
The package-defined numeric constant `1.333`.

#### `\modularscaleMinor`
The package-defined numeric constant `0.75`.

## Emphasis and Semantic Commands

### Basic Emphasis

#### `\emph{text}`
Smart emphasis with automatic nesting.

```latex
\emph{This is emphasized and \emph{this is nested} emphasis}
```

## List Environments

### Standard Lists

#### `itemize`
Bullets with refined gray coloring.

```latex
\begin{itemize}
  \item First point
  \item Second point
\end{itemize}
```

#### `enumerate`
Oldstyle figures with classical progression.

```latex
\begin{enumerate}
  \item First item
  \item Second item
\end{enumerate}
```

#### `description`
Small caps labels in gray.

```latex
\begin{description}
  \item[Term] Definition
  \item[Concept] Explanation
\end{description}
```

#### `inlineitem`
The one package-specific list: inline parenthetical letters joined by semicolons.

```latex
The colors are: \begin{inlineitem}
  \item red
  \item green
  \item blue
\end{inlineitem}.
```

## Quotation Environments

### Block Quotations

#### `quote`
Standard block quote (10.5pt, gray, indented).

```latex
\begin{quote}
Typography is the visual component of the written word.
\hfill--- Matthew Butterick
\end{quote}
```

#### `quotation`
Multi-paragraph quotations with indentation.

```latex
\begin{quotation}
First paragraph of the quotation.

Second paragraph with maintained formatting.
\end{quotation}
```

## Table and Figure Environments

### Standard Tables

Row height is `\arraystretch` times the 16.32pt body baseline plus 2.2pt of
`\extrarowheight`. The package sets `\arraystretch` to 1.2 globally
(~21.8pt rows); a table that wants denser or looser rows sets its own inside
the float.

```latex
\begin{table}[tbp]
  \renewcommand{\arraystretch}{0.9}   % ~16.9pt rows
  \caption{Dense Table}
  \centering
  \begin{tabular}{lrr}
    \toprule
    Item & Value & Count \\
    \midrule
    A & 10.5 & 100 \\
    B & 20.3 & 200 \\
    \bottomrule
  \end{tabular}
\end{table}
```

### Table Notes

Table notes are document-owned. Load `threeparttable` and use its native note
structure; Lanepaper neither loads that package nor defines table-note
commands.

```latex
\usepackage{threeparttable}
% In the table:
\begin{threeparttable}
  \begin{tabular}{@{}lr@{}}
    \toprule
    Item & Value \\
    \bottomrule
  \end{tabular}
  % Add notes using threeparttable's native note structure.
\end{threeparttable}
```

### Standard Figures

Figures are standard. Lanepaper supplies caption typography while the document
chooses the image and float placement:

```latex
\begin{figure}[tbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figure.pdf}
  \caption{A figure}
\end{figure}
```

#### `lanepaperfigurenotes` environment
Typesets flush-left figure notes in footnote size. It is the only
Lanepaper-owned figure-note surface.

```latex
\begin{lanepaperfigurenotes}
  \emph{Notes:} Description of the figure.

  \emph{Source:} Federal Reserve.
\end{lanepaperfigurenotes}
```

## Mathematical Commands

### Mathematical Environments

#### Mathematical Alignment Environments

For aligned equations, use the standard LaTeX environments:

```latex
% Aligned equations
\begin{align}
  f(x) &= ax^2 + bx + c \\
  g(x) &= dx + e
\end{align}

% Centered equations
\begin{gather}
  \int_0^1 f(x) \, dx \\
  \sum_{n=1}^{\infty} a_n
\end{gather}
```

## Cross-Reference Commands

Cross-references are document-owned since v3 (issue #84): the commands below are
`cleveref`'s own — load and configure `cleveref` yourself, as the package no
longer loads or configures it.

### Smart References (via cleveref)

#### `\cref{label}`
Smart reference with automatic type.

```latex
See \cref{fig:example}    % "see fig. 1"
\Cref{tab:results} shows  % "Table 2 shows"
```

#### `\crefrange{label1}{label2}`
Reference range.

```latex
\crefrange{fig:a}{fig:d}  % "figs. 1–4"
```

## Paragraph Commands

### Special Paragraph Commands

#### `\noindentpar`
Force flush-left paragraph.

#### `\forceindent`
Force indentation when suppressed.

#### `\centeredpar{text}`
Centered paragraph block.

```latex
\centeredpar{This paragraph is centered on the page.}
```

#### `\compactpar` *(legacy)*
Pulls the following paragraph 3.3pt closer (a quarter quantum). It remains
defined for papers that already use the helper; new documents can state the
same spacing with `\vspace`.

#### `\loosepars` *(legacy)*
Adds 3.3pt before the following paragraph (a quarter quantum). It remains
defined for papers that already use the helper; new documents can state the
same spacing with `\vspace`.

#### `\tightpar{text}`
Sets a local, more permissive line-breaking profile for one paragraph.

#### `\loosepar{text}`
Sets a local, highly permissive line-breaking profile for one paragraph.

#### `\riverlesspar{text}`
Sets local word-space parameters intended to reduce visible rivers in one
paragraph.

#### `\balancedpar{text}`
Sets a local last-line stretch and final-hyphen penalty for a more balanced
paragraph ending.

#### `\nohyphpar{text}`
Typesets one paragraph with ordinary and explicit hyphenation penalties set to
10000.

#### `\techpar{text}`
Sets local line-breaking penalties suited to technical terms and operators.

### Dialogue Commands

#### `\dialogue{text}`
Standard dialogue with full indent. Wraps text in a new paragraph.

```latex
\dialogue{``I think we should reconsider.''}
```

For longer exchanges, use ordinary paragraphs or a document-selected dialogue
package.

## Footer and page-number commands

Lanepaper's default `plain` page style places a small, centered, gray page
number in oldstyle figures. These commands provide narrow controls for pages
that need a different numbering treatment.

#### `\protectfooter`
Adds one spacing quantum before the footer area.

#### `\fixfooter`
Uses flexible vertical fill to keep the footer clear of the page content.

#### `\frontmatterpages`
Selects roman page numbering and the package's plain page style.

#### `\mainmatterpages`
Selects Arabic page numbering and the package's plain page style.

#### `\unnumberedpage`
Applies the empty page style to the current page.

## Color Commands

The semantic palette is implementation-private. It provides visible roles for
body text, headings, supporting elements and, when the document loads
`hyperref`, links.

`[nocolor]` converts the palette through xcolor's gray model. Chroma goes; the
grayscale hierarchy between heading levels stays, because the grey steps are
already grey and pass through unchanged.

A document that wants its own colours defines and applies them itself:

```latex
\definecolor{myaccent}{RGB}{0,100,0}
\textcolor{myaccent}{Important heading}
```

## Quick Reference Card

### Most Common Commands

```latex
% Title page
\articletitle{Title}
\articleauthors{Name \authorspace Name}
\begin{articleabstract}...\end{articleabstract}
\articlekeywords{word1, word2}

% Emphasis (standard LaTeX)
\emph{emphasis}
\textbf{strong}
\textsc{small caps}

% Lists
\begin{itemize}
\begin{enumerate}
\begin{inlineitem}...\end{inlineitem}

% Quotes
\begin{quote}...\end{quote}

% Figure notes
\begin{lanepaperfigurenotes}...\end{lanepaperfigurenotes}

% References (document loads cleveref)
\cref{label}
\Cref{label}

% Spacing (the quantum is private; write the length)
\vspace{13.2pt}
\vspace{6.6pt}
```

---

This API reference covers the retained package surface. Bibliography and other
document policy remain the paper's responsibility.

## Bibliography and citations

Lanepaper does not load a bibliography package or select a citation style.
Load `biblatex`, `natbib`, or another document-owned bibliography system and
choose its backend and style in the paper. The repository demo uses `biblatex`
with Biber and `style=authoryear`.

### Quick Start

1. **Add citations to your text:**
   ```latex
   Recent studies demonstrate this effect~\textcite{smith2023}.
   The phenomenon has been widely observed~\autocite{jones2022,brown2021}.
   ```

2. **Compile your document:**
   ```bash
   make build  # latexmk runs Biber and re-runs LaTeX as needed
   ```

### Citation Commands

#### Primary Commands (biblatex)

| Command | Usage | Output Example |
|---------|-------|----------------|
| `\textcite{key}` | In-text citation | Smith (2023) argues... |
| `\autocite{key}` | Parenthetical citation | ...observed (Smith 2023) |
| `\textcite[45]{key}` | With page number | Smith (2023, 45) notes... |
| `\autocite[see][]{key}` | With prefix | (see Smith 2023) |
| `\citeauthor{key}` | Author only | Smith |
| `\citeyear{key}` | Year only | 2023 |

#### Multiple Citations

```latex
\textcite{smith2023,jones2022,brown2021}
% Output: Smith (2023), Jones (2022), and Brown (2021)

\autocite{smith2023,jones2022,brown2021}
% Output: (Smith 2023; Jones 2022; Brown 2021)
```

### Bibliography Database Format

Edit `references.bib` following these examples:

#### Journal Article
```bibtex
@article{smith2023,
  title = {Economic Development in East Asia},
  author = {Jane A. Smith and Robert B. Johnson},
  journal = {Journal of Asian Economics},
  volume = {45},
  number = {3},
  pages = {245--267},
  year = {2023},
  doi = {10.1016/j.asieco.2023.03.001}
}
```

#### Book
```bibtex
@book{world1993,
  title = {The East Asian Miracle},
  author = {{World Bank}},
  publisher = {Oxford University Press},
  address = {New York},
  year = {1993},
  isbn = {978-0-19-520993-4}
}
```

#### Working Paper/Preprint
```bibtex
@misc{kim2023,
  title = {Industrial Policy and Growth},
  author = {Thomas Kim and Lisa Park},
  year = {2023},
  eprint = {2301.12345},
  eprinttype = {arxiv},
  eprintclass = {econ.GN}
}
```

#### Online Resource
```bibtex
@online{imf2023,
  title = {Asian Economic Outlook},
  author = {{International Monetary Fund}},
  year = {2023},
  url = {https://www.imf.org/asia-outlook},
  urldate = {2023-12-15}
}
```

### Best Practices

1. **Use semantic field names:**
   - `author` not `authors`
   - `title` not `Title`
   - `pages` with en-dash: `245--267`

2. **Include DOIs when available:**
   - Use bare DOI: `doi = {10.1016/j.asieco.2023.03.001}`
   - Do NOT include `https://doi.org/`

3. **Corporate authors:**
   - Use double braces: `author = {{World Bank}}`

4. **Page ranges:**
   - Use double dash: `pages = {45--48}`

5. **Annotations (optional):**
   ```bibtex
   annotation = {Seminal work on East Asian development.}
   ```

### Compilation Workflow

#### Using Make (Recommended)
```bash
make            # latexmk runs biber and re-runs LaTeX as needed
make clean      # Remove generated output, the PDF included
make lint       # Check style compliance
```

#### Manual Compilation
```bash
pdflatex main
biber main
pdflatex main
pdflatex main
```

### Troubleshooting

#### Bibliography not updating?
1. Run `make clean` to remove cached files
2. Ensure entries in `references.bib` are properly formatted
3. Check for biber errors: look in `main.blg`

#### Citation undefined?
1. Check the citation key matches exactly
2. Ensure the entry is in `references.bib`
3. Run full compilation with `make build`

#### Migrating an existing bibliography
For a v2 document, follow the [v2-to-v3 migration guide](MIGRATION.md).
For a v3 document, load and configure the bibliography package in the document
preamble, then use its citation commands consistently.

### Style Customization

The bibliography style is configured in `demo/preamble.tex`:
```latex
\usepackage[
  backend=biber,
  style=authoryear,
  sorting=nyt
]{biblatex}
```

The bibliography style, sorting, and link presentation belong to the
document-owned bibliography and link packages.

## The font system

### Overview

The fonts module (`lnpfonts.sty`) configures a professional three-font typography system optimized for academic documents.

### Font Stack

#### Text Font: TeX Gyre Pagella
- Based on Palatino with enhanced features
- Superior small caps design
- Lining tabular figures by default
- Larger x-height requiring adjusted leading

#### Mathematics Font: newpxmath
- Perfectly harmonized with Pagella
- Professional mathematical symbols
- Consistent weight and proportions

#### Monospace Font: Inconsolata (zi4)
- Scaled to 96% for harmony with Pagella
- Excellent readability for code
- Professional appearance

### Features

#### Small Caps
- True small caps (not scaled capitals)
- Optimized tracking for readability
- Available in regular and bold weights

#### Numeral Figures
- Default text and tables use Pagella's lining tabular figures
- Oldstyle tabular figures are private to page numbers, top-level list labels,
  and body-footnote marks
- The package exposes no numeral-style API

#### Mathematical Symbols
Enhanced symbol sets from mathalfa:
- Calligraphic: boondoxo
- Blackboard bold: boondox
- Fraktur: boondox

### Usage

#### Loading the fonts
The fonts module is loaded by `lanepaper`; a document does not load it.

#### Font Commands

The module sets up fonts automatically. Available commands:

```latex
% Text emphasis (automatic)
\emph{emphasized text}
\textit{italic text}
\textbf{bold text}
\textsc{small caps}

% Math fonts (automatic)
$\mathcal{A}$  % Calligraphic
$\mathbb{R}$   % Blackboard bold
$\mathfrak{g}$ % Fraktur
```

#### Monospace
```latex
\texttt{monospace text}
```

#### `\monospacescale`
Provides the module's default monospace scale value, `0.96`.
The current package loads `zi4` at that scale; this name is not a general
font-selection interface.

#### `\mathscale`
Provides the module's default mathematics scale value, `1.0`.
The current package uses its fixed `newpxmath` setup; this name is not a
general font-selection interface.

### Technical Details

#### Font Encoding
- T1 encoding for proper hyphenation
- UTF-8 input encoding
- Full European language support

#### Scaling
- Pagella: 100% (base size)
- Inconsolata: 96% (scaled for harmony)
- Math: Automatic sizing

#### Font Features
- Ligatures: Enabled
- Kerning: Optimized
- Small caps: True small caps
- Figures: Lining tabular figures in ordinary text and tables

### Compatibility

- **pdfTeX**: Full support
- **XeTeX/LuaTeX**: Rejected by the package's pdfTeX engine guard
- **Overleaf**: Use the pdfLaTeX compiler with the supported font stack

### Known Limitations

1. Font selection is fixed to Pagella
2. No sans-serif font defined
3. The package does not provide a fontspec path for other engines

## The colour system

### Overview

`lnpcolors.sty` owns the semantic palette. Its names and definitions are not
public API; documents that need their own colours define them explicitly.

### Colour Philosophy

The visible roles are restrained and hierarchical:

| Visible role | Applied to |
|---|---|
| Primary text | Body text and title-page text |
| Heading levels | Section and subsection hierarchy |
| Supporting text | Captions, bullets, footnote rules and quotations |
| Links | Hyperref links, when the document loads `hyperref` |

### The `[nocolor]` Option

`[nocolor]` converts the palette through xcolor's gray model. Chroma goes; the
hierarchy stays, because the grey steps above are already grey and pass
through unchanged, and the two navies land on distinct dark greys.

The grayscale conversion preserves the differences between section, subsection,
subsubsection, and body text.

### Using Colour in a Document

The document owns its own colours:

```latex
\definecolor{myaccent}{RGB}{0,100,0}
\textcolor{myaccent}{An emphasised phrase}
```

### Design Guidelines

#### When to Use Colour

**Do:**
- Reinforce hierarchy
- Indicate functionality (links, code)
- Subtle emphasis

**Don't:**
- Decorate without purpose
- Create "rainbow" documents
- Override semantic meaning

#### Colour Hierarchy

1. **Primary text**: Main content
2. **Heading levels**: Major divisions
3. **Supporting text**: Captions, quotations and notes
4. **Links**: Interactive elements when the document loads `hyperref`

## Page layout and dimensions

### Overview

The dimensions module (`lnpdimensions.sty`) manages page geometry and implements
the 13.2pt spacing quantum; the body baseline measures 16.32pt.

### Spacing Quantum System

#### Foundation
- **Base unit**: 13.2pt spacing quantum (nominal 11pt × 1.20; the actual baseline measures 16.32pt)
- **Spacing principle**: Most package vertical spacing uses multiples of the quantum
- **Purpose**: Spacing values drawn from one quantum scale
- **Private**: the quantum is internal to the package; a document writes the
  length it wants when it needs document-owned spacing.

### Page Geometry

The class picks the sheet; the package fixes the six-inch measure and its
centring. `\documentclass[a4paper]{article}` therefore produces A4 while the
text block keeps the package's established measure.

#### Default Layout
- **Page size**: whatever the class selects (US Letter by default, A4 with `[a4paper]`)
- **Text width**: 6 inches, horizontally centred (~65 characters/line)
- **Vertical margins**: 1.25 inches head and foot
- **Text height**: 8.5 inches on US Letter

#### Geometry Settings
```latex
\geometry{
  textwidth=6in,       % Butterick's optimal measure
  hcentering,          % Equal side margins on whatever sheet is set
  vmargin=1.25in,      % Head and foot margins
  marginparwidth=1in
}
```

On US Letter this gives exactly the established page: (8.5in − 6in)/2 = 1.25in
side margins, 8.5in of text height.

### Usage

#### Selecting the paper size
```latex
\documentclass[11pt,a4paper]{article}
\usepackage{lanepaper}
```

#### Custom margins
```latex
\usepackage{lanepaper}
\geometry{margin=1in}   % Override afterwards
```

#### Vertical space
```latex
\vspace{13.2pt}   % One quantum
\vspace{26.4pt}   % Two quanta
\vspace{6.6pt}    % Half a quantum
```

#### Paragraph Formatting

`lanepaper` sets `\parindent` to 13.2pt and `\parskip` to 0pt, and leaves the
first paragraph after a heading flush left (titlesec's starred `\titlespacing*`).
Document-owned changes should set `\parindent` and `\parskip` directly.

### Best Practices

#### Staying on the Quantum Scale

1. **Use quantum multiples** for vertical spacing: 3.3, 6.6, 13.2, 19.8, 26.4pt
2. **Avoid arbitrary dimensions** like `\vspace{1cm}`
3. **Account for line height** in custom environments

#### Common Patterns
```latex
% Section spacing
\vspace{26.4pt}   % Major break
\vspace{13.2pt}   % Standard break
\vspace{6.6pt}    % Minor break
```

### Troubleshooting

#### Page Overfull/Underfull
- Adjust flexible spacing
- Use `\raggedbottom` for variable content
- Check float placement

### Examples

#### Custom Environment
```latex
\newenvironment{spacedquote}{%
  \vspace{13.2pt}%
  \begin{quote}%
}{%
  \end{quote}%
  \vspace{13.2pt}%
}
```

## The heading system

### Overview

The headings module (`lnpheadings.sty`) provides sophisticated section and heading formatting with quantum-multiple spacing and professional typography.

### Heading Hierarchy

#### Design Principles
- **Tim Brown's Modular Scale**: Perfect Fourth ratio (1.333)
- **Quantum Spacing**: All spacing in 13.2pt quantum multiples (the body baseline measures 16.32pt)
- **Visual Hierarchy**: Size, weight, color, and spacing

#### Heading Specifications

| Level | Size | Leading | Color | Style |
|-------|------|---------|-------|-------|
| Section | 18pt | 26.4pt | Softened navy | Bold |
| Subsection | 14pt | 19.8pt | Muted midnight | Bold |
| Subsubsection | 12pt | 13.2pt | Charcoal | Bold |
| Paragraph | 11pt | 13.2pt | Dark gray | Bold italic |

### Usage

#### Loading the headings
The headings module is loaded by `lanepaper`; a document does not load it.

#### Standard Commands
```latex
\section{Section Title}
\subsection{Subsection Title}
\subsubsection{Subsubsection Title}
\paragraph{Paragraph Title}
```

#### Section Spacing Styles

The module provides four spacing presets:

```latex
\spacioussections   % Generous: 2 units before, 1 after
\moderatesections   % Default: 1.5 units before, 1 after
\compactsections    % Compact: 1 unit before, 1 after
\tightsections      % Tight: 1 unit before, 0.5 after
```

##### Spacing Details

**Spacious** (Original generous spacing):
- Before section: 26.4pt (2 quanta)
- After section: 13.2pt (1 quantum)
- Best for: papers with ample space

**Moderate** (Default):
- Before section: 19.8pt (1.5 quanta)
- After section: 13.2pt (1 quantum)
- Best for: standard academic articles

**Compact**:
- Before section: 13.2pt (1 quantum)
- After section: 13.2pt (1 quantum)
- Best for: dense technical articles

**Tight**:
- Before section: 13.2pt (1 quantum)
- After section: 6.6pt (0.5 quantum)
- Best for: Space-constrained documents

### Special Commands

#### Safe Paragraph Heading
For Overleaf compatibility:
```latex
\safeparagraph{Heading Text}
% Use instead of \paragraph when errors occur
```

#### Alternative Paragraph Styles
```latex
\paragraphsc      % Bold small caps variant
\displayparagraph{Heading}  % Display style
```

### Advanced Features

#### Section Numbering
```latex
% Control numbering depth (default: 3)
\setcounter{secnumdepth}{2}  % Number only to subsection

% Remove numbers
\section*{Unnumbered Section}
```

#### Custom Spacing
```latex
% Temporary spacing change
{
\compactsections
\section{Tight Section}
\subsection{Tight Subsection}
}
% Returns to previous spacing
```

#### First Paragraph Control
First paragraphs after headings are automatically flush left (no indent).

### Typography Details

#### Tracking (Letter Spacing)
- Ordinary text and headings use upstream spacing
- Pagella small caps use one +50 tracking rule

#### Colour Application
Heading colours are internal to the colours module and provide the visible
hierarchy described in [The colour system](#the-colour-system).

### Customization

#### Modifying Spacing
```latex
% Custom section spacing
\titlespacing*{\section}
  {0pt}                              % Left indent
  {30pt plus 5pt minus 5pt}          % Before
  {15pt plus 2pt minus 0pt}          % After
```

#### Adding New Heading Levels
```latex
\titleformat{\subparagraph}
  {\normalfont\fontsize{10}{12}\selectfont\itshape}
  {}
  {0em}
  {}
\titlespacing*{\subparagraph}
  {0pt}
  {6.6pt}
  {3.3pt}
```

### Integration with Document Classes

#### Article Class
Default settings work perfectly with standard article class.

#### Supported document class
The package is designed and tested for the `11pt` standard `article` class.
Chapter-based `report` and `book` layouts are outside the v3 contract.

### Best Practices

#### Heading Usage
1. **Logical Hierarchy**: Don't skip levels
2. **Consistent Style**: Use one spacing style throughout
3. **Meaningful Titles**: Descriptive, not decorative

#### Spacing Consistency
- Match heading spacing to document type
- Consider total page count
- Account for figures and tables

### Troubleshooting

#### Overleaf "Missing \item" Error
Use `\safeparagraph{Title}` instead of `\paragraph{Title}`

#### Inconsistent heading spacing
- Check for manual `\vspace` commands
- Verify consistent spacing style
- Look for `\paragraph` placement

#### Colour Not Applying
Ensure `lanepaper` itself is loaded; it loads the colours and headings modules
in the right order.

### Examples

#### Academic Paper Structure
```latex
\moderatesections  % Default

\section{Introduction}
First paragraph is flush left...

\subsection{Background}
Subsequent paragraphs indented...

\paragraph{Key Concept}
Inline paragraph heading style...
```

#### Compact Technical Document
```latex
\compactsections

\section{Algorithm}
\subsection{Implementation}
\subsubsection{Data Structures}
```

## The list system

### Overview

The internal lists module styles LaTeX's standard `itemize`, `enumerate`, and
`description` environments with the package palette, hanging indents, and
quantum-derived spacing. It also provides `inlineitem` for short enumerations
within running prose.

### List Types

#### Standard Lists

##### Itemize (Bullets)
```latex
\begin{itemize}
\item First item with gray bullet
\item Second item
  \begin{itemize}
  \item Nested with en-dash
  \item Another nested item
  \end{itemize}
\end{itemize}
```

##### Enumerate (Numbers)
```latex
\begin{enumerate}
\item First item with oldstyle numeral
\item Second item
  \begin{enumerate}
  \item Nested with letter (a)
  \item Another nested (b)
  \end{enumerate}
\end{enumerate}
```

##### Description (Terms)
```latex
\begin{description}
\item[Term] Definition with small caps label
\item[Concept] Extended explanation
\end{description}
```

##### Inline Lists
For brief enumerations within text:
```latex
The three principles are:
\begin{inlineitem}
\item clarity
\item consistency  
\item precision
\end{inlineitem}.
```

### Spacing System

All list spacing uses the 13.2pt spacing quantum:

| Spacing Type | Value | Quantum Multiples |
|--------------|-------|------------|
| Item separation | 3.3pt | 0.25 |
| List top/bottom | 6.6pt | 0.5 |
| Nested indent | 13.2pt | 1 |
| Hanging indent | 26.4pt | 2 |

### Typography Details

#### Bullet Hierarchy
1. **Level 1**: Gray bullet (scaled 90%)
2. **Level 2**: Gray en-dash
3. **Level 3**: Smaller gray bullet

#### Number Styles
- **Level 1**: Oldstyle figures with period
- **Level 2**: Lowercase letters with parenthesis
- **Level 3**: Lowercase roman numerals with period

#### Label Formatting
- **Description**: Small caps with 15% gray

### Advanced Usage

#### Custom List Definitions
```latex
% Create a new list type
\newlist{mylist}{itemize}{3}
\setlist[mylist,1]{
  label=$\star$,
  leftmargin=2em,
  itemsep=6.6pt
}
```

#### Resuming Lists
```latex
\begin{enumerate}
\item First item
\item Second item
\end{enumerate}

Some intervening text...

\begin{enumerate}[resume]
\item Continues at third
\item Fourth item
\end{enumerate}
```

### Integration with Content

#### After Headings
Lists after headings automatically have appropriate spacing:
```latex
\subsection{Key Points}
\begin{itemize}
\item First paragraph after list is flush left
\item Spacing is stated in quanta
\end{itemize}
No indent here due to list above.
```

### Best Practices

#### Choosing List Types

**Use itemize when:**
- Order doesn't matter
- Items are equally important
- Showing options or examples

**Use enumerate when:**
- Order is significant
- Showing steps or sequence
- Referencing items later

**Use description when:**
- Defining terms
- Explaining concepts
- Creating glossaries

### Common Patterns

#### References List
```latex
\begin{itemize}
\item Butterick, M. (2019). \emph{Practical Typography}.
\item Brown, T. (2018). \emph{Flexible Typographic Systems}.
\item Hochuli, J. (1987). \emph{Detail in Typography}.
\end{itemize}
```

#### Methodology Steps
```latex
\begin{enumerate}
\item Data collection
  \begin{itemize}
  \item Survey design
  \item Participant recruitment
  \item Response validation
  \end{itemize}
\item Analysis
\item Interpretation
\end{enumerate}
```

#### Feature Comparison
```latex
\begin{description}
\item[Performance] 50\% faster processing
\item[Accuracy] 95\% precision rate
\item[Usability] Improved user satisfaction
\end{description}
```

### Troubleshooting

#### Inconsistent list spacing
- Check for manual `\vspace` commands
- Ensure consistent list environment usage
- Verify no paragraph breaks in items

#### Alignment Issues
- Use `\item` properly
- Don't add blank lines between items
- Check for stray spaces

#### Nested List Problems
- Maximum nesting: 3 levels
- Use consistent environment types
- Verify proper \end{} matching

## How the package is put together

### Modular Architecture

**In v3**: The package is split into internal modules for maintainability, with
load order owned by `lanepaper.sty`; documents load only the public entry point.

#### Module Structure

```
lanepaper.sty (the sole public entry point)
└── Internal modules, loaded in this order:
    ├── lnpdimensions.sty   - Page geometry, spacing quantum, and block quotations
    ├── lnpcolors.sty       - The semantic colour palette
    ├── lnpfonts.sty        - Pagella, Inconsolata, newpxmath, mathalfa
    ├── lnpheadings.sty     - Section heading styles
    ├── lnplists.sty        - List typography and refined bullets
    └── lnpmicrotype.sty    - Upstream protrusion/expansion; small-caps tracking
```

#### Module Configuration

The modules are internal and are not loaded directly (ADR-0006). Configure the
package by overriding after loading it:

```latex
% Load main package
\usepackage{lanepaper}
```

For complete module documentation, see [`CONVENTIONS.md` section 3](CONVENTIONS.md).

##### List Typography Module

`lnplists.sty` styles the standard list environments and owns the one
package-specific `inlineitem` environment.

* Level 1 • Professional grey bullet  
* Level 2 – en-dash  
* Level 3 • smaller grey bullet

Example:
```latex
\begin{itemize}
  \item Primary item
  \item Another item
    \begin{itemize}
      \item Nested item – note the en-dash marker
    \end{itemize}
\end{itemize}
```

Use enumitem's document-owned options for one-off customisation:
```latex
\begin{itemize}[itemsep=0pt]
  \item A dense list
\end{itemize}
```

##### Paragraph Spacing Commands

`lanepaper` sets `\parindent` to 13.2pt and `\parskip` to 0pt, and the first
paragraph after a heading is flush left. Set `\parindent` and `\parskip`
directly for document-owned changes.

### Standard Appendices, Figures, and Tables

Lanepaper leaves appendix orchestration to the document. Use standard LaTeX:

```latex
\appendix
\section{Supplementary Results}
```

Figures and tables remain the standard LaTeX floats. Lanepaper applies caption
typography but does not wrap placement or insert float barriers.

#### Figure Management

```latex
\begin{figure}[tbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/example.pdf}
  \caption{Professional Caption Below Figure}
  \label{fig:example}
  \begin{lanepaperfigurenotes}
    \emph{Notes:} Description of what the figure shows.

    \emph{Source:} Data source or image attribution.
  \end{lanepaperfigurenotes}
\end{figure}
```

#### Table Design System

**Standard Table:**
```latex
\begin{table}[tbp]
  \caption{Caption Above Table}
  \label{tab:example}
  \centering
  \begin{tabular}{@{}lrrr@{}}
    \toprule
    Method & Accuracy & Precision & Recall \\
    \midrule
    Baseline & 0.72*** & 0.68** & 0.71*** \\
             & (0.03) & (0.04) & (0.03) \\
    Our Method & 0.91*** & 0.89*** & 0.93*** \\
               & (0.01) & (0.02) & (0.01) \\
    \bottomrule
  \end{tabular}
\end{table}
```

Tables use `booktabs` without vertical rules. If a table needs notes, load
`threeparttable` in the document and use its native environments.

If the document loads `longtable`, Lanepaper applies the same table-caption
typography through its package hook while leaving the environment document-owned.

#### Tables with Standard Row Heights

```latex
% Standard rows (~21.8pt measured: \arraystretch 1.2 × 16.32pt + 2.2pt).
% 1.2 is the package default, so a plain table already has them.
\begin{table}[tbp]
  % Content
\end{table}

% Compact tables (~16.9pt rows measured)
\begin{table}[tbp]
  \renewcommand{\arraystretch}{0.9}
  % For dense information
\end{table}
```

### Compatibility

**Document class:** The v3 contract is the standard `11pt` `article` class.
The package does not promise chapter-based `report` or `book` layouts.

See the [dependency record in README](README.md#dependencies) for the
packages loaded by the public entry point.

Cross-references, appendix packages, and `threeparttable` are document-owned:
load and configure them yourself if needed.

`Package fontaxes Warning: Axis 'shape' not supported` is harmless and expected.

For troubleshooting, see [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

### Technical Implementation

#### Microtype Configuration

```latex
\usepackage[protrusion=true,expansion=true,tracking=true]{microtype}
\SetTracking[
  no ligatures={f}
]{
  encoding={T1},family={qpl},shape={sc}
}{50}
```

Microtype maps Pagella's `qpl` family to its shipped `ppl` protrusion tables
and supplies the default expansion table. Lanepaper adds no authored numeric
protrusion, expansion, kerning, spacing, or generic tracking table.

#### Baseline Grid Mathematics

The body baseline is **16.32pt** (`\linespread{1.20}` scales the class's 13.6pt
baseline: 13.6 × 1.20 = 16.32pt). The **13.2pt spacing quantum** is a separate,
internal unit used for most vertical spacing — it is not the baseline pitch.
See [ADR-0004](docs/adr/0004-baseline-grid-is-a-spacing-quantum.md) for the derivation.

```latex
Body baseline: 16.32pt  (document leading)
Spacing quantum: 13.2pt
Half quantum: 6.6pt
Quarter quantum: 3.3pt
```

#### Performance Considerations

- **Memory Usage**: Microtype and font loading increase memory requirements
- **Compatibility**: Verified locally with TeX Live 2025 and pdfTeX (see
  [`README.md`](README.md) for the toolchain details).

---

## Migration from v2

v3 is a deliberate breaking contraction with no compatibility aliases and no
flag that restores the v2 surface. A v2 document needs source edits; the
complete top-to-bottom replacement map is in [MIGRATION.md](MIGRATION.md).
