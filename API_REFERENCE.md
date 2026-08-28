# Lane LaTeX Template API Reference

Complete reference for all commands, environments, and options provided by the `lanepaper` package.

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
13. [Grid System Commands](#grid-system-commands)
14. [Footnote Commands](#footnote-commands)
15. [Quick Reference Card](#quick-reference-card)
16. [Bibliography and citations](#bibliography-and-citations)
17. [The font system](#the-font-system)
18. [The colour system](#the-colour-system)
19. [Page layout and dimensions](#page-layout-and-dimensions)
20. [The heading system](#the-heading-system)
21. [The list system](#the-list-system)
22. [How the package is put together](#how-the-package-is-put-together)
23. [Typography standards](#typography-standards)
24. [Removed in v3](#removed-in-v3)

## Package Options

### Loading the Package

```latex
\usepackage[options]{lanepaper}
```

### Available Options

| Option | Default | Description |
|--------|---------|-------------|
| `grid` | off | Display grid overlay (true-baseline and quantum lines) for typography debugging |
| `nogrid` | **on** | Hide grid overlay (normal mode) |
| `minimal` | off | Load only essential features (dimensions, compilation fixes) |
| `natbib` | off | Use natbib compatibility mode instead of biblatex |
| `nocolor` | off | Disable all custom colors (black text only) |
| `draft` | off | Enable draft mode with visible overfull boxes |
| `nobiblatex` | off | Disable automatic biblatex loading |

### Examples

```latex
% Standard usage
\usepackage{lanepaper}

% Show grid for debugging
\usepackage[grid]{lanepaper}

% Minimal mode for compatibility
\usepackage[minimal]{lanepaper}

% Multiple options
\usepackage[draft,grid]{lanepaper}
```

## Title Page Commands

### Main Title Commands

#### `\articletitle{title}`
Displays article title with automatic size adjustment (16-18pt based on length).

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
Creates golden-ratio width abstract block.

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

#### `\titlefootnotesetup`
Switch to symbol footnotes (*, †, ‡) for title page.

#### `\titlefootnotereset`
Return to numeric footnotes for main text.

```latex
\titlefootnotesetup
% ... title page content ...
\titlefootnotereset
```

#### `\elegantauthor{name}`
Individual author name with enhanced small caps.
- **Size:** 12pt/14pt
- **Style:** Small caps
- **Tracking:** 100 units (10% letter spacing)
- **Usage:** Within `\articleauthors` if desired

#### `\begin{articleabstract}...\end{articleabstract}`
Professional abstract environment.
- **Width:** 0.618 × text width (golden ratio)
- **Label:** "ABSTRACT" in enhanced small caps
- **Font size:** 10pt (small)
- **Spacing:** 0.5 grid units internal
## Typography Commands

### Section Opening Styles

#### `\sectionopening{first line}{rest of paragraph}`
First line in small caps.

```latex
\sectionopening{This opening line appears in small caps,} while the rest 
of the paragraph continues in normal text.
```

#### `openingparagraph` environment
First paragraph with no indentation.

```latex
\begin{openingparagraph}
The opening paragraph after a heading has no first-line indent.
\end{openingparagraph}
```

### Section Breaks

#### `\sectionsep`
Insert 2 grid units of white space.
(Formerly `\sectionbreak`; renamed because titlesec executes any defined `\<level>break` as a heading hook.)

#### `\asteriskbreak`
Three centered asterisks for thematic breaks.

```latex
\sectionsep
% or
\asteriskbreak
```

### Drop Caps

#### `\dropcap{letter}{text}`
Two-line drop cap.

```latex
\dropcap{W}{hen we consider} the importance of typography...
```

#### `\academicdropcap{letter}{text}`
Conservative drop cap for academic use.

```latex
\academicdropcap{T}{his introduction} begins with a minimal drop cap...
```

## Spacing Commands

### Grid Units

| Command | Size | Description |
|---------|------|-------------|
| `\gridunit` | 13.2pt | Spacing quantum (not the document baseline, which measures 16.32pt) |
| `\halfgridunit` | 6.6pt | Half grid unit |
| `\quartergridunit` | 3.3pt | Quarter grid unit |
| `\onehalfgridunit` | 19.8pt | 1.5 grid units |
| `\doublegridunit` | 26.4pt | 2 grid units |
| `\triplegridunit` | 39.6pt | 3 grid units |

### Usage

```latex
\vspace{\gridunit}        % Add one grid unit of vertical space
\vspace{2\gridunit}       % Add two grid units
\vspace{\halfgridunit}    % Add half a grid unit
```

### Special Spacing Commands

#### `\authorspace`
Space between author names (5% of text width).

#### `\titlespacemajor`
Major title spacing (2 grid units).

#### `\titlespaceminor`
Minor title spacing (1.5 grid units).

#### `\titlespaceinter`
Inter-element spacing (1 grid unit).

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

### Special List Environments

#### `academicitem`
En-dash lists for academic style.

```latex
\begin{academicitem}
  \item First finding
  \item Second observation
\end{academicitem}
```

#### `compactitem`
No spacing between items.

```latex
\begin{compactitem}
  \item Compact item one
  \item Compact item two
\end{compactitem}
```

#### `displayitem`
Bold items with generous spacing.

```latex
\begin{displayitem}
  \item \textbf{Key Result:} Important finding
  \item \textbf{Innovation:} Novel contribution
\end{displayitem}
```

#### `inlineitem`
Inline lists with semicolons.

```latex
The colors are: \begin{inlineitem}
  \item red
  \item green
  \item blue
\end{inlineitem}.
```

#### `readableitem`
Enhanced spacing (0.5 grid units).

```latex
\begin{readableitem}
  \item More breathing room
  \item Better for dense content
\end{readableitem}
```

## Quotation Environments

### Block Quotations

#### `quote`
Standard block quote (10.5pt, gray, indented).

```latex
\begin{quote}
Typography is the visual component of the written word.
\quoteattribution{Matthew Butterick}
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

#### `emphasisquote`
Large italic quote for emphasis.

```latex
\begin{emphasisquote}
Typography exists to honor content.
\quoteattribution{Robert Bringhurst}
\end{emphasisquote}
```

### Quote Commands

#### `\quoteattribution{name}`
Right-aligned attribution with em-dash.

## Table and Figure Environments

### Enhanced Table Environments

#### `gridtable`
Table with the standard quantum-derived row height.

```latex
\begin{gridtable}[tbp]
  \caption{Table with Standard Row Height}
  \centering
  \begin{tabular}{lrr}
    \toprule
    Item & Value & Count \\
    \midrule
    A & 10.5 & 100 \\
    B & 20.3 & 200 \\
    \bottomrule
  \end{tabular}
\end{gridtable}
```

#### `regressiontable`
19.8pt rows for regression results.

#### `compacttable`
9.9pt rows for dense data.

### Landscape Tables

#### `landscapetable`
Full-page landscape table.

```latex
\begin{landscapetable}[tbp]
  \caption{Wide Regression Results}
  \begin{tabular}{l*{10}{c}}
    % Wide table content
  \end{tabular}
\end{landscapetable}
```

#### `rotatedtable`
90-degree rotated table.

#### `fittable`
Auto-scaled table to fit width.

```latex
\begin{fittable}[tbp]{1.2\textwidth}
  \caption{Scaled Table}
  \begin{tabular}{l*{15}{c}}
    % Table content
  \end{tabular}
\end{fittable}
```

### Table Notes

#### `tablenotes` environment
Professional notes following QJE style.

```latex
\begin{tablenotes}
  \tabnote{General methodology notes}
  \tabvars{GDP in billions, CPI base 2020}
  \tabmethod{OLS with fixed effects}
  \tabcluster{Clustered at state level}
  \tabsample{N = 1,234}
  \tabsource{World Bank (2023)}
  \tabstars  % Standard significance stars
\end{tablenotes}
```

### Figure Commands

#### `gridfigure`
Figure with height rounded to a quantum multiple.

```latex
\begin{gridfigure}[tbp]
  \centering
  \gridincludegraphics[width=0.8\textwidth]{figure.pdf}
  \caption{Figure with quantum-rounded height}
\end{gridfigure}
```

#### `landscapefigure`
Full-page landscape figure.

#### `fignotes` environment
Notes for figures.

```latex
\begin{fignotes}
  \fignote{Description of the figure}
  \figsource{Data: Federal Reserve}
\end{fignotes}
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

*Note: Grid-specific equation environments may be added in future versions.*

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

### Paragraph Style Switching

#### `\classicalparagraphs`
13.2pt indent, no spacing (default).

#### `\modernparagraphs`
No indent, 6.6pt spacing.

#### `\hybridparagraphs`
9.9pt indent, 3.3pt spacing.

#### `\quartergridparagraphs`
13.2pt indent, 3.3pt flexible spacing.

#### `\thirdgridparagraphs`
13.2pt indent, 4.4pt flexible spacing.

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

#### `\compactpar` *(deprecated)*
Pulls the following paragraph 3.3pt closer (subtracts one `\quartergridunit`).
Retained for backward compatibility only; use `\vspace` directly in new
documents.

#### `\loosepars` *(deprecated)*
Adds 3.3pt before the following paragraph (one `\quartergridunit`). Retained
for backward compatibility only; use `\vspace` directly in new documents.

#### `\quoteparagraph{text}` *(requires lnphochuli module)*
Paragraph with hanging opening quote.

```latex
% Requires: \usepackage{lnphochuli}
\quoteparagraph{"When we examine the evidence..."}
```

### Dialogue Commands

#### `\dialogue{text}`
Standard dialogue with full indent. Wraps text in a new paragraph.

```latex
\dialogue{``I think we should reconsider.''}
```

Note: `\rapidexchange` and `\speaker` are not implemented.

## Color Commands

### Predefined Colors

| Color | Usage |
|-------|-------|
| `textblack` | Near-black body text |
| `linknavy` | Professional blue links |
| `sectioncolor` | Section headings |
| `subsectioncolor` | Subsection headings |
| `bulletgray` | List bullets |
| `subtlegray` | Page numbers |
| `quotegray` | Block quotes |

## Grid System Commands

### The spacing quantum

All vertical spacing in the package is a multiple of a **13.2pt quantum**. The
quantum is not the baseline: the body sets 10.95pt on a **16.32pt** baseline
(`\linespread{1.20}` scaling the class's 13.6pt, under the `11pt` option). The
two are often confused, and the distinction was settled deliberately —
see [ADR-0004](docs/adr/0004-baseline-grid-is-a-spacing-quantum.md).

| Fraction | Length |
|---|---|
| 1.5 quanta | 19.8pt |
| full quantum | 13.2pt |
| 0.75 quanta | 9.9pt |
| half quantum | 6.6pt |
| quarter quantum | 3.3pt |

The leading is roughly 149% of the body size, on the generous side of the
Bringhurst and Butterick bands. That suits TeX Gyre Pagella's large x-height, a
~77-character measure, and math-dense text.


### Grid Display

#### `\showgrid`
Display the baseline-grid overlay (lines at the real \baselineskip).

#### `\hidegrid`
Hide the grid overlay.

### Quantum-Spacing Commands

#### `\gridincludegraphics[options]{file}`
Include graphics with height rounded to a quantum multiple.

```latex
\gridincludegraphics[width=0.8\textwidth]{figure.pdf}
```

#### `\vspacegrid{units}`
Add vertical space in whole quanta.

```latex
\vspacegrid{2}  % Add 2 grid units
```

#### `\halfbaselinespace`
Insert half baseline space in tables.
- **Height:** 6.6pt (0.5 grid units)
- **Usage:** `\halfbaselinespace` between table sections

#### `\fullbaselinespace`
Insert full baseline space.
- **Height:** 13.2pt (1 quantum)

#### `\baselinespace{multiplier}`
Custom baseline space.
- **Example:** `\baselinespace{1.5}` → 19.8pt

## Footnote Commands

### Special Footnote Commands

#### `\sidenote{text}`
Margin note in footnote size.

```latex
Important point.\sidenote{This appears in the margin.}
```

---

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
\begin{academicitem}

% Quotes
\begin{quote}...\quoteattribution{Author}\end{quote}

% References (document loads cleveref)
\cref{label}
\Cref{label}

% Spacing
\vspace{\gridunit}
\vspace{\halfgridunit}
```

---

This API reference covers all major commands and environments provided by the `lanepaper` package. For additional details, see the package documentation and example files.

## Bibliography and citations

This guide explains the bibliography system for the Lane LaTeX Template, which uses **biblatex** with **biber** backend and Chicago Manual of Style (17th edition) author-date format.

### Quick Start

1. **Add citations to your text:**
   ```latex
   Recent studies demonstrate this effect~\textcite{smith2023}.
   The phenomenon has been widely observed~\autocite{jones2022,brown2021}.
   ```

2. **Compile your document:**
   ```bash
   make  # latexmk runs biber and re-runs LaTeX as needed
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
3. Run full compilation with `make pdf`

#### Switching from natbib?
The project supports legacy natbib with `preamble-natbib.tex`. To use biblatex (recommended):
1. Ensure `main.tex` includes `demo/preamble.tex`
2. Replace `\citet` → `\textcite`
3. Replace `\citep` → `\autocite`

### Style Customization

The bibliography style is configured in `demo/preamble.tex`:
```latex
\usepackage[
  backend=biber,
  style=chicago-authordate,
  natbib=true,
  hyperref=true,
  sorting=nyt
]{biblatex}
```

All bibliography entries are formatted according to Chicago Manual of Style guidelines with enhanced digital features (clickable DOIs, proper URL formatting).

## The font system

### Overview

The fonts module (`lnpfonts.sty`) configures a professional three-font typography system optimized for academic documents.

### Font Stack

#### Text Font: TeX Gyre Pagella
- Based on Palatino with enhanced features
- Superior small caps design
- Oldstyle figures for text
- Larger x-height requiring adjusted leading

#### Mathematics Font: newpxmath
- Perfectly harmonized with Pagella
- Professional mathematical symbols
- Consistent weight and proportions

#### Monospace Font: Inconsolata (zi4)
- Scaled to 95% for harmony with Pagella
- Excellent readability for code
- Professional appearance

### Features

#### Small Caps
- True small caps (not scaled capitals)
- Optimized tracking for readability
- Available in regular and bold weights

#### Oldstyle Figures
- Proportional oldstyle figures in text
- Lining figures in tables
- Proper figure selection by context

#### Mathematical Symbols
Enhanced symbol sets from mathalfa:
- Calligraphic: boondoxo
- Blackboard bold: boondox
- Fraktur: boondox

### Usage

#### Using the fonts
```latex
\RequirePackage{lnpfonts}
```

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

### Technical Details

#### Font Encoding
- T1 encoding for proper hyphenation
- UTF-8 input encoding
- Full European language support

#### Scaling
- Pagella: 100% (base size)
- Inconsolata: 95% (scaled for harmony)
- Math: Automatic sizing

#### OpenType Features
- Ligatures: Enabled
- Kerning: Optimized
- Small caps: True small caps
- Figures: Oldstyle proportional

### Compatibility

- **pdfTeX**: Full support
- **XeTeX**: Limited (use fontspec instead)
- **LuaTeX**: Limited (use fontspec instead)
- **Overleaf**: Full compatibility

### Known Limitations

1. Font selection is fixed to Pagella
2. No sans-serif font defined
3. XeTeX/LuaTeX users should use fontspec

### Future Enhancements

- [ ] Font selection options
- [ ] Sans-serif font integration
- [ ] fontspec variant for modern engines
- [ ] Custom font scaling options

## The colour system

### Overview

The colors module (`lnpcolors.sty`) provides a sophisticated color system with semantic naming, professional aesthetics, and accessibility compliance.

### Color Philosophy

Based on three principles:
1. **Restraint**: Limited palette for professional appearance
2. **Hierarchy**: Colors reinforce document structure
3. **Accessibility**: WCAG AA compliant contrast ratios

### Color Palette

#### Text Colors
```latex
textblack    % RGB(25,25,25)    - Softened black for reduced eye strain
textgray     % RGB(102,102,102) - 40% gray for secondary text
lightgray    % RGB(179,179,179) - 70% gray for subtle elements
darkgray     % RGB(64,64,64)    - 25% gray for emphasis
```

#### Heading Colors
```latex
sectioncolor    % RGB(25,50,80)   - Softened navy
subsectioncolor % RGB(40,40,55)   - Muted midnight
subsubcolor     % RGB(64,64,64)   - Medium charcoal
paragraphcolor  % RGB(89,89,89)   - Dark gray
```

#### Functional Colors
```latex
linkcolor       % RGB(0,102,180)  - Professional blue
citecolor       % RGB(0,102,180)  - Same as links
codecolor       % RGB(51,51,51)   - Dark gray for code
quotegray       % gray!15         - 15% gray for quotes
subtlegray      % gray!85         - Very dark gray
```

### Usage

#### Using the colours
```latex
\RequirePackage{lnpcolors}
```

#### Applying Colors
```latex
% Text coloring
\textcolor{textgray}{Secondary text}
\textcolor{sectioncolor}{Important heading}

% In other commands
\color{quotegray}  % Switch color
```

#### Color in Document Elements

The colors are automatically applied to:
- Section headings (sectioncolor, subsectioncolor, etc.)
- Hyperlinks (linkcolor)
- Citations (citecolor)
- Code snippets (codecolor)
- Block quotes (quotegray)

### Accessibility

All color combinations meet WCAG AA standards:

| Text Color | Background | Contrast Ratio | Rating |
|------------|------------|----------------|---------|
| textblack | white | 17.4:1 | AAA |
| textgray | white | 4.1:1 | AA |
| sectioncolor | white | 9.7:1 | AAA |
| linkcolor | white | 4.8:1 | AA |

### Customization

#### Redefining Colors
```latex
% Load module first
\RequirePackage{lnpcolors}

% Then redefine
\definecolor{sectioncolor}{RGB}{0,100,0}  % Green sections
```

#### Adding New Colors
```latex
% After loading module
\definecolor{mycolor}{RGB}{100,50,150}
```

### Color Commands

#### Semantic Text Commands
The module provides semantic commands for common uses:

```latex
\emphcolor{text}     % Uses sectioncolor
\metacolor{text}     % Uses darkgray
\codecolor{text}     % Uses codecolor
```

### Design Guidelines

#### When to Use Color

**Do:**
- Reinforce hierarchy
- Indicate functionality (links, code)
- Subtle emphasis

**Don't:**
- Decorate without purpose
- Create "rainbow" documents
- Override semantic meaning

#### Color Hierarchy

1. **Black text**: Primary content
2. **Section colors**: Major divisions
3. **Gray variations**: Supporting elements
4. **Blue**: Interactive elements only

### Technical Details

#### Color Model
- Primary model: RGB
- Gray definitions: Percentage-based
- Full xcolor syntax supported

#### Package Options
```latex
% Load with xcolor options
\RequirePackage[dvipsnames]{lnpcolors}
```

### Compatibility

- Works with all LaTeX engines
- Full xcolor compatibility
- Printer-friendly gray fallbacks
- Screen and print optimized

### Examples

#### Custom Link Colors
```latex
% Make links dark green
\definecolor{linkcolor}{RGB}{0,100,0}
```

#### Highlighted Text
```latex
% Create highlight color
\definecolor{highlight}{RGB}{255,255,200}
\newcommand{\highlight}[1]{%
  \colorbox{highlight}{#1}%
}
```

#### Conditional Colors
```latex
% Different colors for draft/final
\ifdraft
  \definecolor{sectioncolor}{RGB}{200,0,0}  % Red in draft
\fi
```

## Page layout and dimensions

### Overview

The dimensions module (`lnpdimensions.sty`) manages page geometry and implements the 13.2pt spacing quantum --- the unit spacing values are stated in (the body baseline measures 16.32pt).

### Spacing Quantum System

#### Foundation
- **Base unit**: 13.2pt spacing quantum (nominal 11pt × 1.20; the actual baseline measures 16.32pt)
- **Grid philosophy**: All vertical spacing in multiples of base unit
- **Purpose**: Spacing values drawn from one quantum scale

#### Grid Units
```latex
\gridunit         % 13.2pt (1 unit)
\halfgridunit     % 6.6pt (0.5 units)
\quartergridunit  % 3.3pt (0.25 units)
```

### Page Geometry

#### Default Layout
- **Page size**: US Letter (8.5 × 11 inches)
- **Margins**: 1.25 inches all sides
- **Text width**: ~6 inches (optimal 65 characters/line)
- **Text height**: ~8.5 inches

#### Geometry Settings
```latex
% Current settings (US Letter)
\geometry{
  letterpaper,
  left=1.25in,
  right=1.25in,
  top=1.25in,
  bottom=1.25in,
  headsep=\gridunit,
  footskip=26.4pt  % 2 grid units
}
```

### Usage

#### Using the layout
```latex
\RequirePackage{lnpdimensions}
```

#### Spacing Commands

##### Adding Vertical Space
```latex
\halfbaselinespace    % Add 6.6pt (0.5 units)
\fullbaselinespace    % Add 13.2pt (1 unit)
\gridspace{2}         % Add 2 grid units (26.4pt)
```

##### Custom Spacing
```latex
% Add 1.5 grid units
\vspace{1.5\gridunit}

% Flexible spacing
\vspace{\gridunit plus \quartergridunit minus \quartergridunit}
```

#### Paragraph Styles

The module provides three paragraph formatting styles:

```latex
\classicalparagraphs  % Default: 13.2pt indent, 0pt spacing
\modernparagraphs     % Modern: 0pt indent, 6.6pt spacing  
\hybridparagraphs     % Hybrid: 9.9pt indent, 3.3pt spacing
```

##### Classical (Default)
- First-line indent: 13.2pt (1 grid unit)
- Paragraph spacing: 0pt
- Flush left after headings

##### Modern
- First-line indent: 0pt
- Paragraph spacing: 6.6pt (0.5 units)
- Visual separation through spacing

##### Hybrid
- First-line indent: 9.9pt (0.75 units)
- Paragraph spacing: 3.3pt (0.25 units)
- Balanced approach

### Grid Development Tools

#### Visualizing the Grid
```latex
% In document preamble
\usepackage{lnpdimensions}
\usepackage{lnpgridoverlay}

% In document
\showgrid  % Display grid lines
\hidegrid  % Hide grid lines
```

#### Quantum-Sized Elements
```latex
% Manual quantum spacing (coefficient form: a bare register truncates glue)
\vspace{1\gridunit minus 0.25\gridunit}  % One quantum, shrinkable
```

### Page Layout Options

#### A4 Paper
```latex
% Before loading module
\PassOptionsToPackage{a4paper}{geometry}
\RequirePackage{lnpdimensions}
```

#### Custom Margins
```latex
% Load module first
\RequirePackage{lnpdimensions}

% Then adjust
\geometry{margin=1in}
```

#### Two-Column Layout
```latex
\documentclass[twocolumn]{article}
\usepackage{lnpdimensions}
% Grid system adapts automatically
```

### Advanced Features

#### Grid Calculations
```latex
% Derive lengths from the quantum
\newlength{\myheight}
\setlength{\myheight}{10\gridunit}  % 132pt

% Conditional spacing
\ifdim\pagetotal<20\gridunit
  \vspace{\gridunit}
\fi
```

#### Custom Grid Unit
```latex
% Must set before loading module
\newlength{\gridunit}
\setlength{\gridunit}{12pt}  % Custom grid
\RequirePackage{lnpdimensions}
```

### Best Practices

#### Staying on the Quantum Scale

1. **Use quantum units** for all vertical spacing
2. **Avoid arbitrary dimensions** like `\vspace{1cm}`
3. **Test with grid overlay** during development
4. **Account for line height** in custom environments

#### Common Patterns
```latex
% Section spacing
\vspace{2\gridunit}  % Major break
\vspace{\gridunit}   % Standard break
\vspace{\halfgridunit}  % Minor break

% Float spacing
\setlength{\floatsep}{\gridunit}
\setlength{\textfloatsep}{1.5\gridunit}
```

### Troubleshooting

#### Off-Scale Spacing
- Check for spacing not stated in quanta
- Use `\showgrid` to visualize line positions

#### Page Overfull/Underfull
- Adjust flexible spacing
- Use `\raggedbottom` for variable content
- Check float placement

### Examples

#### Grid-Perfect Figure
```latex
\begin{figure}[tb]
  \centering
  \includegraphics[height=10\gridunit]{image}
  \caption{Figure with quantum-rounded height}
\end{figure}
```

#### Custom Environment
```latex
\newenvironment{gridquote}{%
  \vspace{\gridunit}%
  \begin{quote}%
}{%
  \end{quote}%
  \vspace{\gridunit}%
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

#### Using the headings
```latex
\RequirePackage{lnpheadings}
```

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
- Before section: 26.4pt (2 grid units)
- After section: 13.2pt (1 quantum)
- Best for: Books, reports with ample space

**Moderate** (Default):
- Before section: 19.8pt (1.5 grid units)
- After section: 13.2pt (1 quantum)
- Best for: Standard academic papers

**Compact**:
- Before section: 13.2pt (1 quantum)
- After section: 13.2pt (1 quantum)
- Best for: Dense technical documents

**Tight**:
- Before section: 13.2pt (1 quantum)
- After section: 6.6pt (0.5 grid units)
- Best for: Space-constrained documents

### Special Commands

#### Section Breaks
```latex
\sectionsep  % Add 2 grid units of space
\spacebreak  % Alias for \sectionsep
```

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
- Bold headings follow the microtype module's global `series=b` rule (per-heading
  `\SetTracking` was removed: it is global and was annulled by that rule)
- Subsubsections: Normal tracking
- Small caps: Context-dependent (3-12%)

#### Color Application
All heading colors are defined in the colors module:
- `sectioncolor`: RGB(25,50,80)
- `subsectioncolor`: RGB(40,40,55)
- `subsubcolor`: RGB(64,64,64)
- `paragraphcolor`: RGB(89,89,89)

### Customization

#### Changing Heading Colors
```latex
% After loading module
\definecolor{sectioncolor}{RGB}{0,100,0}  % Green sections
```

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
  {\halfgridunit}
  {\quartergridunit}
```

### Integration with Document Classes

#### Article Class
Default settings work perfectly with standard article class.

#### Book Class
```latex
\spacioussections  % Recommended for chapters
```

#### Report Class
```latex
\moderatesections  % Good balance
```

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

#### Color Not Applying
Ensure colors module is loaded:
```latex
\RequirePackage{lnpcolors}
\RequirePackage{lnpheadings}
```

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

#### Book Chapter
```latex
\spacioussections

\section{The Beginning}
\sectionsep
\section{The Middle}
\sectionsep
\section{The End}
```

## The list system

### Overview

The lists module (`lists.sty`) implements sophisticated list typography with multiple styles, quantum-derived spacing, and professional aesthetics.

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

#### Specialized List Environments

##### Compact Lists
Minimal spacing for dense information:
```latex
\begin{compactitem}
\item Reference one
\item Reference two
\item Reference three
\end{compactitem}
```

##### Display Lists
Emphasized items with generous spacing:
```latex
\begin{displayitem}
\item \textbf{Key Finding:} Important result
\item \textbf{Innovation:} Novel contribution
\end{displayitem}
```

##### Academic Lists
En-dash bullets following university style:
```latex
\begin{academicitem}
\item First scholarly point
\item Second scholarly point
\end{academicitem}
```

##### Readable Lists
Enhanced spacing for improved readability:
```latex
\begin{readableitem}
\item First point with breathing room
\item Second point clearly separated
\end{readableitem}
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

### List Customization

#### Global Spacing Commands

Change spacing for all lists:
```latex
\tightlists      % Minimal spacing
\normallists     % Default spacing (restore)
\spaciouslists   % Generous spacing
```

#### Bullet Style Commands

Change bullet appearance globally:
```latex
\dashbullets      % Switch to en-dashes
\trianglebullets  % Switch to triangles
\defaultbullets   % Restore gray bullets
```

#### Manual Bullet Control
```latex
\begin{itemize}
\itembullet First item with bullet
\itemdash Second item with dash
\itemdiamond Third item with diamond
\itemsquare Fourth item with square
\itemtriangle Fifth item with triangle
\end{itemize}
```

### Spacing System

All list spacing uses the 13.2pt spacing quantum:

| Spacing Type | Value | Grid Units |
|--------------|-------|------------|
| Item separation | 3.3pt | 0.25 units |
| List top/bottom | 6.6pt | 0.5 units |
| Nested indent | 13.2pt | 1 unit |
| Hanging indent | 26.4pt | 2 units |

### Typography Details

#### Bullet Hierarchy
1. **Level 1**: Gray bullet (scaled 90%)
2. **Level 2**: Gray en-dash
3. **Level 3**: Gray diamond (scaled 70%)

#### Number Styles
- **Level 1**: Oldstyle figures with period
- **Level 2**: Lowercase letters with parenthesis
- **Level 3**: Lowercase roman numerals with period

#### Label Formatting
- **Description**: Small caps with 15% gray
- **Display**: Bold text
- **Academic**: Regular text with en-dash

### Advanced Usage

#### Custom List Definitions
```latex
% Create a new list type
\newlist{mylist}{itemize}{3}
\setlist[mylist,1]{
  label=\textcolor{sectioncolor}{$\star$},
  leftmargin=2em,
  itemsep=\halfgridunit
}
```

#### Mixed List Styles
```latex
\begin{itemize}
\item Regular item
\begin{compactitem}  % Switch to compact
\item Nested compact item
\item Another compact item
\end{compactitem}
\item Back to regular spacing
\end{itemize}
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

#### In Quotations
```latex
\begin{quote}
Key principles include:
\begin{compactitem}
\item Brevity
\item Clarity
\item Precision
\end{compactitem}
\end{quote}
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

#### Spacing Guidelines

**Use compact lists for:**
- References
- Brief items
- Space-constrained areas

**Use display lists for:**
- Key findings
- Important points
- Executive summaries

**Use readable lists for:**
- Detailed explanations
- Teaching materials
- When clarity is paramount

### Common Patterns

#### References List
```latex
\begin{compactitem}
\item Butterick, M. (2019). \emph{Practical Typography}.
\item Brown, T. (2018). \emph{Flexible Typographic Systems}.
\item Hochuli, J. (1987). \emph{Detail in Typography}.
\end{compactitem}
```

#### Methodology Steps
```latex
\begin{enumerate}
\item Data collection
  \begin{academicitem}
  \item Survey design
  \item Participant recruitment
  \item Response validation
  \end{academicitem}
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

**Since v1.5-alpha**: The package is structured as independent modules for better maintainability and customization.

#### Module Structure

```
lanepaper.sty (main package)
├── Core Modules (automatically loaded):
│   ├── lnpcompilationfixes.sty        - Common LaTeX warning fixes
│   ├── lnpfonts.sty                   - Font configuration (Pagella, Inconsolata, math)
│   ├── lnpcolors.sty                  - Professional color system
│   ├── lnpdimensions.sty              - Grid system and spacing definitions
│   ├── lnpheadings.sty                - Section heading styles with colors
│   ├── lnplists.sty                   - List typography with refined bullets
│   └── lnpmicrotype.sty               - Enhanced character protrusion and expansion
│
└── Optional Enhancement Modules:
    ├── lnpparagraphs.sty              - Advanced paragraph formatting
    ├── lnphochuli.sty                 - Optical adjustments; kerning pairs and last-line control apply on load; ligature suppression and hanging-quote commands are opt-in
    ├── lnpfontfeatures.sty            - Full Pagella feature access
    └── lnpfontfallbacks.sty           - Compatibility mode
```

#### Using Individual Modules

Load only the features you need:

```latex
% Just the professional color system
\RequirePackage{lnpcolors}

% Or just the heading styles
\RequirePackage{lnpheadings}
```

#### Custom Module Configuration

Load modules with custom settings before the main package:

```latex
% Custom grid unit
\newlength{\gridunit}
\setlength{\gridunit}{12pt}
\RequirePackage{lnpdimensions}

% Then load main package
\usepackage{lanepaper}
```

For complete module documentation, see [`CONVENTIONS.md` section 3](CONVENTIONS.md).

##### List Typography Module

`lnplists.sty` gives you carefully tuned list environments spaced in 13.2pt quantum multiples and a bullet hierarchy that follows Butterick & Hochuli’s guidance.

* Level 1 • Professional grey bullet  
* Level 2 – en-dash  
* Level 3 ◆ diamond

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

You can customise markers or spacing—for instance, switch the top-level bullet to a dash:
```latex
\setlist[itemize,1]{label=\dashmark}
```

Bullet symbol commands:
```latex
\refinedbullet    % 75% scaled bullet, subtlegray
\refineddash      % En-dash with micro-kern, subtlegray
```

##### Paragraph Spacing Commands

Paragraph style switchers (indent and parskip per command):

```latex
\classicalparagraphs      % 13.2pt indent, 0pt parskip (default)
\modernparagraphs         % 0pt indent, 6.6pt parskip
\hybridparagraphs         % 9.9pt indent, 3.3pt parskip
\quartergridparagraphs    % 13.2pt indent, 3.3pt parskip
\thirdgridparagraphs      % 13.2pt indent, 4.4pt parskip
```

### Title Page System

#### How the title page is built

Systematic commands for professional title pages following economics paper conventions:

```latex
% Complete title page example
\thispagestyle{empty}
\titlefootnotesetup              % Switch to symbolic footnotes
\begin{center}
  \vspace*{\gridunit}
  \articletitle{Your Title Here}
  % Or with acknowledgments:
  % \articletitlefootnote{Your Title Here}{We thank colleagues for helpful comments.}
  \articleauthors{Author One\footnote{University} \quad Author Two\footnote{University}}
  \articledate{\today}
  \begin{articleabstract}
    Abstract text...
  \end{articleabstract}
  \articlekeywords{keyword1, keyword2}
  \articlejel{A10, B20}
\end{center}
\clearpage
\titlefootnotereset              % Reset to numeric footnotes
```

#### Title Commands

**Standard Title (18pt):**
```latex
\articletitle{The Economic Impact of Policy:\\[0.3\gridunit]
Evidence from East Asia}
```

**Compact Title (16pt for many authors):**
```latex
\articletitlecompact{A Long Title That Requires Less Vertical Space}
```

**Title with Acknowledgments Footnote:**
```latex
% Standard title with footnote for acknowledgments
\articletitlefootnote{The Economic Impact of Policy:\\[0.3\baselineskip]
Evidence from East Asia}{We thank seminar participants for helpful comments.}

% Compact title with footnote
\articletitlecompactfootnote{A Long Title That Requires Less Vertical Space}{Financial support from NSF grant \#12345 is gratefully acknowledged.}
```

These commands allow authors to add acknowledgments, funding information, or other notes as a footnote to the title. The footnote appears at the bottom of the title page and uses symbolic notation (*, †, ‡) when `\titlefootnotesetup` is active.

#### Author Formatting

**Multiple Authors:**
```latex
\articleauthors{%
  Jane Smith\footnote{Harvard University, Email: jsmith@harvard.edu}
  \quad\quad
  John Doe\footnote{MIT, Email: jdoe@mit.edu}
}
```

**For 5+ Authors (two-line layout):**
```latex
\articleauthors{%
  Author One\footnote{...} \quad Author Two\footnote{...} \quad Author Three\footnote{...}\\[0.3\gridunit]
  Author Four\footnote{...} \quad Author Five\footnote{...}
}
```

#### Spacing Principles

All vertical spacing follows the 13.2pt quantum system:
- **After title**: 1.5 grid units (19.8pt)
- **After authors**: 1.5 grid units (19.8pt)
- **Before abstract**: 2 grid units (26.4pt)
- **Abstract internal**: 0.5 grid units (6.6pt)

#### Footnote System

Systematic sizing with baseline-aligned spacing:

**Sizing Hierarchy:**
- **Superscript marker**: 6pt with oldstyle numerals and +50 tracking
- **Footnote text**: 8.5pt with 12pt actual leading (10pt × \linespread)
- **Hanging indent**: 11.5pt (fits three-digit old-style markers)

**Spacing System:**
- **Above footnotes**: 26.4pt (2 quanta) to the rule
- **Between footnotes**: the 12pt footnote baseline (`\footnotesep` is an
  inert floor, not inter-note space)
- **Footnote rule**: 33% text width, 0.4pt height for subtle elegance

#### Enhanced Optical Margin Alignment

Professional character protrusion following Gutenberg's principles:

```latex
% Protrusion Settings by Context
- Punctuation: Quotes at 1400 units (40% more aggressive)
- Periods/commas: 1200 units for full hanging punctuation
- Hyphens: 1000 units for cleaner right margins
- Capitals: T, V, W, Y use negative protrusion (-50 to -80)
- Small text: Conservative 1000 units for readability
- Bold text: Reduced to 1200 units (weight compensation)
- Display sizes: Extra protrusion up to 1600 units
```

#### Semantic Emphasis Hierarchy

Sophisticated emphasis system optimized for TeX Gyre Pagella:

```latex
% Hierarchy Levels (by frequency of use)
\emph{text}            % Primary emphasis (italic↔roman)
\textbf{text}      % Bold for critical terms (<5% of text)
\emph{baseline grid}   % Technical terms (italic)
\textsc{Hermann Zapf}  % Names (small caps, 2.5% tracking)
\textsc{PDF}            % Acronyms (small caps, 4% tracking)
\emph{Book Title}     % Published works (italic)
\textbf{\textsc{WARNING}}    % Maximum emphasis (bold small caps)

% Smart nesting
\emph{outer \emph{inner} outer}  % → italic roman italic

% Context-aware nesting handlers
\emph{text}               % Italic in roman context, roman in italic context
\textbf{text}                 % Bold in regular context, bold-italic in bold context
```

#### Professional Footnote System

Foundry-optimized specifications for TeX Gyre Pagella:

```latex
% Size Hierarchy
Footnote text: 8.5pt (77% of 11pt body)
Superscript: 6pt (70% of footnote size)
Leading: 12pt actual (10pt × \linespread{1.20})
Hanging indent: 11.5pt (fits three-digit old-style markers)

% Grid-Compliant Spacing
Rule position: 26.4pt below text (2 quanta)
Rule to footnote: 13.2pt (1 quantum)
Between footnotes: 12pt footnote baseline (\footnotesep is an inert floor)
Rule specs: 33% width, 0.4pt thickness, text color

% Title Page Adjustments
\titlefootnotesetup    % Switches to symbols (*, †, ‡)
\titlefootnotereset    % Returns to numbers
```

### Chicago-Compliant Appendix System

#### How the appendix system works

Professional appendix management with automatic single/multiple detection:

```latex
\begin{documentAppendices}
  \input{appendices/first.tex}
  \input{appendices/second.tex}
\end{documentAppendices}
```

#### Automatic Behavior

**Multiple Appendices (2+):**
- Table of Contents: "Appendices" section header
- Numbering: "Appendix A", "Appendix B", etc.
- Cross-references: Full "Appendix A" format

**Single Appendix (1):**
- Table of Contents: Direct appendix entry
- Numbering: "Appendix" (no letter)
- Cross-references: Simple "Appendix" format

#### Implementation Details

The system uses a two-pass auxiliary file mechanism:

1. **First Pass**: Counts appendices and writes count to `.aux` file
2. **Second Pass**: Reads count and formats accordingly
3. **Detection Logic**: `\ifnum\lnp@totalappendices>1`

#### Usage Patterns

```latex
% Standard usage
\begin{documentAppendices}
  \input{appendices/main_appendix.tex}
  \input{appendices/tech_appendix.tex}
\end{documentAppendices}

% Legacy compatibility
\startappendices
  \input{appendices/main_appendix.tex}
\finishappendices
```

### Professional Figures and Tables

#### Figure Management

```latex
\begin{figure}[tbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/example.pdf}
  \caption{Professional Caption Below Figure}
  \label{fig:example}
  \begin{fignotes}
    \fignote{Description of what the figure shows}
    \figsource{Data source or image attribution}
  \end{fignotes}
\end{figure}
```

#### Table Design System

**Standard Professional Table:**
```latex
\begin{table}[tbp]
  \caption{Caption Above Table (Chicago Style)}
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
  \begin{tablenotes}
    \tabnote{Standard errors in parentheses}
    \tabstars  % ***p<0.01, **p<0.05, *p<0.1
  \end{tablenotes}
\end{table}
```

#### Tables with Standard Row Heights

```latex
% Standard rows (~21.8pt measured: \arraystretch 1.2 × 16.32pt + 2.2pt)
\begin{gridtable}[tbp]
  % Content with automatic \arraystretch
\end{gridtable}

% Regression tables (19.8pt rows)
\begin{regressiontable}[tbp]
  % For statistical results with standard errors
\end{regressiontable}

% Compact tables (~16.9pt rows measured)
\begin{compactgridtable}[tbp]
  % For dense information
\end{compactgridtable}
```

#### Landscape and Rotation Support

```latex
% Wide regression tables
\begin{landscapetable}[tbp]
  \caption{Wide Regression Results}
  \begin{tabular}{l*{10}{c}}
    % Content for 10+ columns
  \end{tabular}
\end{landscapetable}

% Rotated correlation matrices
\begin{rotatedtable}[tbp]
  % 90-degree rotation
\end{rotatedtable}

% Auto-scaled tables
\begin{fittable}[tbp]{1.2\textwidth}
  % Automatically scaled to fit
\end{fittable}
```

#### QJE-Style Notes System

```latex
% Table notes
\begin{tablenotes}
  \tabnote{General description}
  \tabvars{Variable definitions}
  \tabmethod{Methodology used}
  \tabcluster{Standard error clustering}
  \tabsample{Sample size and period}
  \tabsource{Data source}
  \tabstars  % Significance levels
  \tabdaggers  % Alternative: †p<0.10, ††p<0.05
\end{tablenotes}

% Figure notes
\begin{fignotes}
  \fignote{Figure description}
  \figsource{Source attribution}
\end{fignotes}

% Panel labels
\panellabel{A}  % Bold panel label
\panelnote{A}{Panel-specific note}
```

#### Float Management

```latex
% Intelligent barriers
\FloatBarrier           % Standard barrier
\softfloatbarrier       % Flexible with grid spacing
\hardfloatbarrier       % Force new page if needed
\sectionendfloatbarrier % Before major transitions

% Here-float alternatives
\tryherefigure{...}     % Attempts [h], falls back to [tbp]
\forceherefigure{...}   % Absolute placement
\begin{herefloat}
  % Standard-row-height here placement
\end{herefloat}

% Visual balance
\balancefloatpage       % Adds flexible space
\compensatetopfloat     % Adds grid unit after large floats
\showfloatstats         % Debug placement in log
```

### Compatibility

**Document Classes:**
- ✅ `article` (recommended)
- ✅ `report` (chapter-based appendices)
- ✅ `book` (chapter-based appendices)
- ❌ `memoir` (requires modifications)

**Core dependencies** (auto-loaded):
`tgpagella`, `zi4`, `newpxmath`, `mathalfa`, `microtype`,
`enumitem`, `caption`, `geometry`

Cross-references are document-owned since v3 (issue #84): load and configure
`cleveref` yourself if you want it. `appendix` is configured if the document
loads it.

For appendix count issues, delete auxiliary files and recompile:
```bash
latexmk -C main.tex  # or: rm *.aux *.out *.toc && pdflatex main.tex && pdflatex main.tex
```

`Package fontaxes Warning: Axis 'shape' not supported` is harmless and expected.

For troubleshooting, see [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

### Technical Implementation

#### Microtype Configuration

```latex
% Hochuli's optimal settings for Pagella
\usepackage[
  activate={true,nocompatibility},
  final,
  tracking=true,
  kerning=true,
  spacing=true,
  factor=1050,                     % Character protrusion
  stretch=15,                      % Word spacing flexibility
  shrink=15
]{microtype}
```

#### Baseline Grid Mathematics

The body baseline is **16.32pt** (`\linespread{1.20}` scales the class's 13.6pt
baseline: 13.6 × 1.20 = 16.32pt). The **13.2pt spacing quantum** (`\gridunit`) is
a separate unit used for most vertical spacing — it is not the baseline pitch.
See [ADR-0004](docs/adr/0004-baseline-grid-is-a-spacing-quantum.md) for the derivation.

```latex
Body baseline: 16.32pt  (document leading)
Spacing quantum (\gridunit): 13.2pt
Half quantum (\halfgridunit): 6.6pt
Quarter quantum (\quartergridunit): 3.3pt
```

#### Appendix Counter Logic

```latex
% Two-pass auxiliary file mechanism
\newcounter{appendixcount}
\newcommand{\lnp@writeappendixcount}{%
  \immediate\write\@auxout{%
    \string\gdef\string\lnp@totalappendices{\theappendixcount}%
  }%
}

% Conditional formatting based on count
\ifnum\lnp@totalappendices>1\relax
  \multipleappendicestrue
\else
  \multipleappendicesfalse
\fi
```

#### Performance Considerations

- **Compilation Speed**: Two-pass system requires `pdflatex` twice for appendix detection
- **Memory Usage**: Microtype and font loading increase memory requirements
- **Compatibility**: Tested with TeX Live 2022, 2025, 2026 (see [`README.md`](README.md) for details); MiKTeX not verified

---

For version history, see [`CHANGELOG.md`](CHANGELOG.md) and the `Version History` section of [`README.md`](README.md).

## Typography standards

### Typography Principles

#### Core Philosophy

The style package implements three complementary typographic philosophies:

1. **Butterick's Practical Typography**: Reader-focused optimization
2. **Brown's Modular Scale**: Mathematical harmony through proportional relationships  
3. **Hochuli's Detail in Typography**: Micro-refinements for archival quality

#### Golden Rules

**DO:**
- Trust the spacing quantum system - all spacing derives from 13.2pt quantum multiples
- Use semantic commands (`\emph{}`, `\textbf{\textsc{}}`, `\texttt{}`) over presentational formatting
- Maintain consistent labeling conventions (`app:`, `fig:`, `tab:`, `eq:`)
- Let the modular scale handle sizing relationships automatically

**DON'T:**
- Manually adjust spacing with `\vspace{}` or `\hspace{}`
- Use `\textbf{}` and `\textit{}` for emphasis - use `\emph{}` semantically
- Override color schemes - use provided semantic color commands
- Introduce off-scale spacing with custom line spacing

### Text Typography Standards

#### Title Capitalization Guidelines

**Headline-Style Capitalization Rules:**

**Capitalize:**
- First and last word of titles and subtitles
- First word after a colon
- All major words (nouns, pronouns, verbs, adjectives, adverbs)

**Lowercase:**
- Articles (the, a, an)
- Prepositions (regardless of length: in, on, through, between, etc.)
- Conjunctions (and, but, for, or, nor)
- Words "to" and "as"

**Special Cases:**
- Hyphenated words: Capitalize the word immediately preceding the hyphen
  - ✅ Correct: "Learning-Based Approach"  
  - ❌ Exception: "X-ray" (not "X-Ray")

**Title Verification:**
Use a title case checker to verify proper capitalization for:
- Paper titles and subtitles
- All section and subsection headings
- Figure and table captions

#### Emphasis and Formatting

```latex
% CORRECT: Semantic emphasis
This is \emph{important} text that needs emphasis.
Mathematical \emph{variables} should be emphasized in context.

% INCORRECT: Presentational formatting
This is \textit{important} text that needs emphasis.
```

**Rationale**: `\emph{}` provides contextual emphasis that adapts to surrounding formatting, while `\textit{}` provides only presentational italics.

**Advanced Emphasis Behavior:**
```latex
% Context-sensitive emphasis
Normal text with \emph{emphasized text}.
\emph{Already emphasized with \emph{de-emphasized} text inside.}
```

#### Title Page Components

The style provides systematic commands for professional title pages following economics paper conventions:

**Title Commands:**
```latex
% Standard title (18pt, perfect for most papers)
\articletitle{A Research Article Title:\\[0.3\baselineskip]
Subtitle for the Article}

% Compact title (16pt, for papers with many authors)
\articletitlecompact{Long Title That Needs Less Space}
```

**Author Formatting:**
```latex
% Multiple authors with footnotes
\articleauthors{%
  First Author\footnote{University of X, Email: author1@x.edu}
  \quad\quad
  Second Author\footnote{University of Y, Email: author2@y.edu}
}

% For 5+ authors, consider two-line layout:
\articleauthors{%
  Author One\footnote{...} \quad Author Two\footnote{...} \quad Author Three\footnote{...}\\[0.3\baselineskip]
  Author Four\footnote{...} \quad Author Five\footnote{...}
}
```

**Complete Title Page Example:**
```latex
\thispagestyle{empty}
\titlefootnotesetup  % Switch to symbolic footnotes
\begin{center}
  \vspace*{1\baselineskip}
  \articletitle{Your Title Here}
  \articleauthors{...}
  \articledate{\today}
  \begin{articleabstract}
    Abstract text following 85% width for optimal readability...
  \end{articleabstract}
  \articlekeywords{keyword1, keyword2, keyword3}
  \articlejel{A10, B20, C30}
\end{center}
\clearpage
\titlefootnotereset  % Reset to numeric footnotes
\setcounter{page}{1}
```

**Spacing Principles:**
- All vertical spacing uses the 13.2pt spacing quantum (body baseline measures 16.32pt)
- Title sizes follow Brown's modular scale (18pt = 11pt × 1.333²)
- Author names use subtle size increase (12pt = 11pt × 1.09)
- Abstract width (85%) follows Butterick's optimal reading guidelines

#### Academic Writing Quality Standards

**Sentence and Paragraph Structure:**
```latex
% CORRECT: One sentence per line (version control friendly)
This is the first sentence of the paragraph.
It clearly states the main point.
The following sentence provides supporting evidence.

% INCORRECT: Multiple sentences per line
This is the first sentence. It clearly states the main point. The following sentence provides evidence.
```

**Professional Language Standards:**
```latex
% CORRECT: Precise, academic language
The results \emph{demonstrate} a significant correlation.
The analysis \emph{reveals} important patterns.
The findings \emph{indicate} a clear relationship.

% INCORRECT: Weak or informal language
The results \emph{show} a correlation.
The analysis \emph{finds} patterns.
The findings \emph{prove} a relationship.
```

**Quantitative Precision:**
```latex
% CORRECT: Specific quantification with units
The performance improved by 23.7\% over baseline results.
Measurements were taken at 5-minute intervals ($n = 120$).
The confidence interval spans [0.15, 0.42] with $p < 0.001$.

% INCORRECT: Vague quantification
The performance improved significantly.
Measurements were taken frequently.
The results are statistically significant.
```

#### Small Caps Usage

```latex
% General purpose bold small caps
Organizations like \textbf{\textsc{UNESCO}} require careful formatting.

% Heading-style small caps with enhanced tracking
\textbf{\textsc{Chapter Opening}}

% Inline small caps for abbreviations
The \textbf{\textsc{PhD}} program requires comprehensive study.

% Color-balanced small caps for headings
Section headings use \balancedbsc{Enhanced Formatting}.
```

#### Professional Quotations

```latex
% CORRECT: LaTeX quotation marks
``Professional typography'' requires attention to detail.
Typography---like architecture---requires systematic thinking.

% INCORRECT: Straight quotes
"Professional typography" requires attention to detail.
Typography--like architecture--requires systematic thinking.
```

### Mathematical Typography Standards

#### Semantic Mathematical Commands

```latex
% Number sets (use semantic commands)
\mathbb{R}^n, \mathbb{C}, \mathbb{Z}, \mathbb{Q}, \mathbb{N}, \mathbb{F}, \mathbb{P}

% Mathematical operators
\lVert x\rVert, \lvert z\rvert, \langle u, v\rangle, \{A\}

% Mathematical spaces (calligraphic)
\mathcal{H}, \mathcal{B}, \mathcal{A}, \mathcal{T}, \mathcal{M}

% Declared operators  
\operatorname{tr}(A), \operatorname{rank}(M), \operatorname{span}\{V\}, \operatorname{supp}(f)
```

#### Display Mathematics

```latex
% CORRECT: Systematic equation formatting
\begin{equation}
f(x) = \int_{-\infty}^{\infty} g(t) e^{-2\pi i x t} \, dt
\end{equation}

% Enhanced inline mathematics
The function $f \colon \mathbb{R} \to \mathbb{C}$ satisfies $\lVert f\rVert_2 < \infty$.
```

#### Complex Mathematical Expressions

```latex
% Advanced mathematical typography
\begin{align}
\mathcal{L}[f](s) &= \int_0^{\infty} f(t) e^{-st} \, dt \\
\text{where } f &\in L^1(\mathbb{R}_+) \cap C(\mathbb{R}_+)
\end{align}
```

#### Mathematical Writing Best Practices

**Equation Integration:**
```latex
% CORRECT: Equations as part of sentence structure
The fundamental relationship is given by
\begin{equation}
E = mc^2,
\label{eq:mass-energy}
\end{equation}
where $E$ represents energy, $m$ denotes mass, and $c$ is the speed of light.

% INCORRECT: Equations as isolated elements
The fundamental relationship:
$$E = mc^2$$
$E$ = energy, $m$ = mass, $c$ = speed of light.
```

**Variable Definition Standards:**
```latex
% CORRECT: Clear variable introduction
Let $\mathbf{X} = (x_1, x_2, \ldots, x_n)^T \in \mathbb{R}^n$ denote the feature vector.
The objective function $f: \mathbb{R}^n \to \mathbb{R}$ is defined as $f(\mathbf{x}) = \|\mathbf{Ax} - \mathbf{b}\|_2^2$.

% INCORRECT: Unclear variable usage
Let $X$ be the features and $f$ be the function.
```

**Mathematical Punctuation:**
```latex
% CORRECT: Proper equation punctuation
\begin{align}
\alpha &= \beta + \gamma, \\
\delta &= \epsilon \cdot \zeta.
\end{align}

% INCORRECT: Missing or improper punctuation
\begin{align}
\alpha &= \beta + \gamma \\
\delta &= \epsilon \cdot \zeta
\end{align}
```

### Code Typography Standards

#### Inline Code Context

```latex
% Basic inline code
The \texttt{numpy.array} function handles multidimensional data.

% Micro-spaced code (prevents text flow disruption)
Python's \texttt{DataFrame.groupby()} method provides aggregation.

% File paths with proper hyphenation
Data is stored in \texttt{/data/processed/analysis_results.csv}.

% Mathematical variables in code context
The variable \texttt{learning_rate} controls optimization speed.

% Mixed documentation style
Function signature: \texttt{\textbackslash{}newcommand\{\textbackslash{}norm\}[1]}
```

#### Code Block Standards

```latex
% For longer code blocks, use standard LaTeX environments
\begin{verbatim}
def calculate_statistics(data):
    """Compute descriptive statistics."""
    return {
        'mean': np.mean(data),
        'std': np.std(data),
        'count': len(data)
    }
\end{verbatim}
```

### Footnote Standards

#### Professional Footnote Usage

```latex
% Standard footnotes with hanging indent
This important concept\footnote{The concept was first introduced by 
Smith (1995) and later refined by Johnson (2003), providing the 
foundation for modern understanding.} requires careful consideration.

% Multiple footnotes
Key findings\footnote{See Appendix A for detailed methodology.} 
support the hypothesis\footnote{Statistical significance: p < 0.001}.
```

**Automatic Features:**
- **Sizing**: 8pt superscript, 9pt text with 11pt leading
- **Spacing**: 26.4pt (2 quanta) above the footnote rule; 12pt footnote baseline between notes
- **Typography**: Oldstyle numerals, hanging indent, optimized word spacing

### Document Structure Standards

#### Professional Labeling Convention

**Systematic Label Prefixes:**
All labels must use consistent prefixes for optimal organization and cross-referencing:

| Element Type | Prefix | Example | Usage |
|--------------|---------|---------|-------|
| Table | `tbl:` | `\label{tbl:performance-results}` | Main tables |
| Subtable | `subtbl:` | `\label{subtbl:subset-analysis}` | Sub-tables within table environments |
| Figure | `fig:` | `\label{fig:system-architecture}` | Main figures |
| Subfigure | `subfig:` | `\label{subfig:component-detail}` | Sub-figures within figure environments |
| Section | `sec:` | `\label{sec:methodology}` | Main sections |
| Subsection | `subsec:` | `\label{subsec:data-collection}` | Subsections |
| Subsubsection | `subsubsec:` | `\label{subsubsec:validation-protocol}` | Subsubsections |
| Algorithm | `alg:` | `\label{alg:optimization-procedure}` | Algorithm environments |
| Code Line | `line:` | `\label{line:critical-calculation}` | Specific lines in algorithms/code |
| Equation | `eq:` | `\label{eq:fundamental-relationship}` | Mathematical equations |
| Appendix Section | `app:` | `\label{app:technical-details}` | Appendix sections (existing) |

**Labeling Best Practices:**
```latex
% CORRECT: Descriptive, systematic labels
\begin{table}[htbp]
  \caption{Performance Comparison Across Three Datasets}
  \label{tbl:performance-comparison}
  % table content
\end{table}

\begin{figure}[htbp]
  % figure content
  \caption{System Architecture Overview}
  \label{fig:system-architecture}
\end{figure}

% INCORRECT: Non-descriptive or inconsistent labels
\label{table1}
\label{fig-arch}
\label{performanceData}
```

#### Caption Placement and Formatting

**Placement Rules:**
```latex
% CORRECT: Captions above tables
\begin{table}[htbp]
  \caption{The Effectiveness of ADF in Three Datasets}
  \label{tbl:adf-effectiveness}
  \begin{tabular}{...}
    % table content
  \end{tabular}
\end{table}

% CORRECT: Captions below figures  
\begin{figure}[htbp]
  \includegraphics[width=0.8\textwidth]{analysis-results}
  \caption{Learning-Based Approach Performance Analysis}
  \label{fig:learning-performance}
\end{figure}
```

**Caption Capitalization:**
Follow the same headline-style capitalization rules as titles:
```latex
% CORRECT: Headline-style capitalization
\caption{The Effectiveness of Machine Learning in Data Analysis}
\caption{Performance Comparison Between Traditional and Novel Approaches}
\caption{X-ray Analysis Results for Medical Imaging}

% INCORRECT: Sentence case or improper capitalization
\caption{The effectiveness of machine learning in data analysis}
\caption{Performance comparison between Traditional and Novel approaches}  
\caption{X-Ray Analysis Results for Medical Imaging}
```

#### Data Presentation Standards

**Table Design Standards:**
```latex
% CORRECT: Professional table with clear structure
\begin{table}[htbp]
  \caption{Performance Metrics Across Different Models}
  \label{tbl:model-performance}
  \centering
  \begin{tabular}{@{}lrrr@{}}
    \toprule
    Model & Accuracy (\%) & F1-Score & Training Time (min) \\
    \midrule
    Baseline      & 82.3 & 0.791 &  15.2 \\
    Enhanced SVM  & 87.6 & 0.834 &  23.7 \\
    Deep Network  & 91.2 & 0.897 & 142.5 \\
    \bottomrule
  \end{tabular}
  \footnotesize
  \textit{Note:} All metrics computed on held-out test set ($n = 1{,}250$).
\end{table}

% INCORRECT: Poor table design
\begin{table}
\begin{tabular}{|l|l|l|l|}
\hline
Model & Accuracy & F1 & Time \\
\hline
Baseline & 82.3 & 0.791 & 15.2 \\
SVM & 87.6 & 0.834 & 23.7 \\
Network & 91.2 & 0.897 & 142.5 \\
\hline
\end{tabular}
\end{table}
```

**Figure Quality Standards:**
```latex
% CORRECT: High-quality figure integration
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.9\textwidth]{plots/convergence-analysis}
  \caption{Training Loss Convergence Across Different Learning Rates}
  \label{fig:convergence-analysis}
\end{figure}

% Guidelines for figure creation:
% - Minimum 300 DPI for publication quality
% - Clear, readable fonts (minimum 10pt in final size)
% - Consistent color scheme across all figures
% - Descriptive axis labels with units
% - Legend when multiple data series present
```

**Statistical Reporting Standards:**
```latex
% CORRECT: Complete statistical reporting
The proposed method achieved significantly higher accuracy 
(M = 87.6\%, SD = 2.3\%) compared to the baseline 
(M = 82.3\%, SD = 3.1\%), t(48) = 6.42, p < 0.001, 
Cohen's d = 1.85, 95\% CI [3.8\%, 6.7\%].

% INCORRECT: Incomplete statistical reporting
The proposed method was significantly better (p < 0.05).
```

#### Section Hierarchy

```latex
% CORRECT: Systematic hierarchy following modular scale
\section{Major Section}           % 18pt, Perfect Fourth ratio
\subsection{Important Subsection} % 14pt, scaled systematically  
\subsubsection{Detailed Topic}    % 12pt, proportional scaling
\paragraph{Key Point}             % 11.5pt, enhanced small caps
```

#### Front Matter Standards

```latex
% Professional title formatting
\papertitle{Short, Impactful Title}          % Tracked uppercase
\mixedtitle{Longer Descriptive Title Text}   % Mixed case for readability

% Author and affiliation
\textsc{Author Name}                     % Tracked small caps
\emph{Institution and Department}     % Italic formatting

% Keywords with tracking
\textbf{Keywords:} \emph{keyword one, keyword two, keyword three}
```

#### Bibliography Integration

```latex
% CORRECT: Chicago author-date style citations
This finding \cite{smith2023analysis} supports the hypothesis.
Recent studies \cite{jones2022methods, brown2023results} confirm...

% Multiple citations
\cite{author2020, author2021, author2022}
```

#### Reproducibility and Open Science Standards

**Code and Data Documentation:**
```latex
% CORRECT: Complete reproducibility information
All experiments were conducted using Python 3.9.7 with 
scikit-learn v1.0.2 and NumPy v1.21.3.
The complete source code and datasets are available at 
\url{https://github.com/author/paper-reproduction}.
Random seeds were fixed (seed = 42) for all experiments.

% INCORRECT: Vague implementation details
Experiments used standard machine learning libraries.
Code is available upon request.
```

**Version Control and Collaboration:**
```latex
% Best practices for academic collaboration:
% - Use meaningful commit messages
% - One sentence per line for .tex files (easier merging)
% - Systematic file organization with clear naming
% - Regular compilation checks before commits
% - Shared bibliography management
```

**Experimental Design Documentation:**
```latex
% CORRECT: Comprehensive experimental setup
The dataset was randomly split into training (60\%), 
validation (20\%), and test sets (20\%) using stratified 
sampling to maintain class distribution. 
Hyperparameters were tuned using 5-fold cross-validation 
on the training set, with performance evaluated on the 
held-out test set for final reporting.

% INCORRECT: Unclear experimental setup
Data was split and models were tuned appropriately.
```

#### Citation Quality and Academic Integrity

**Comprehensive Citation Standards:**
```latex
% CORRECT: Appropriate citation density and variety
Recent advances in deep learning~\cite{lecun2015deep} have 
revolutionized computer vision tasks. Convolutional neural 
networks~\cite{krizhevsky2012imagenet} demonstrate superior 
performance on image classification, while attention 
mechanisms~\cite{vaswani2017attention} have transformed 
natural language processing.

% INCORRECT: Sparse or inappropriate citations
Deep learning is important. CNNs work well for images.
```

**Citation Context and Integration:**
```latex
% CORRECT: Citations integrated with analysis
While Smith et al.~\cite{smith2023analysis} report accuracy 
improvements of 15\%, their approach requires 3× more 
computational resources than our proposed method. 
In contrast, the lightweight framework of 
Jones~\cite{jones2023efficient} achieves comparable results 
with reduced complexity.

% INCORRECT: Citations without context
Many papers have studied this~\cite{paper1,paper2,paper3}.
```

**Primary vs. Secondary Sources:**
```latex
% CORRECT: Preference for primary sources
The original ResNet architecture~\cite{he2016deep} introduced 
skip connections to address the vanishing gradient problem.

% INCORRECT: Citing secondary sources for primary claims
ResNet uses skip connections~\cite{tutorial2023deep}.
```

### Common Anti-Patterns

#### Typography Mistakes to Avoid

```latex
% WRONG: Manual spacing
\section{Title}\vspace{10pt}
This departs from the quantum scale.

% WRONG: Presentational formatting  
This is \textbf{important} text.
Use \emph{semantic} formatting instead.

% WRONG: Manual colors
\textcolor{red}{Warning message}
Use \textbf{Warning message} instead.

% WRONG: Inconsistent labels
\label{fig1}, \label{table-data}, \label{AppendixA}
Use \label{fig:analysis}, \label{tab:data}, \label{app:main}
```

#### Mathematical Typography Errors

```latex
% WRONG: Inconsistent notation
R^n, C, Z (mixing fonts and notation)
Use \mathbb{R}^n, \mathbb{C}, \mathbb{Z} consistently.

% WRONG: Poor spacing in math mode
$f(x)=\int_0^1g(t)dt$ (cramped spacing)
Use $f(x) = \int_0^1 g(t) \, dt$ (proper spacing).
```

## Removed in v3

v3 is a deliberate breaking contraction (issue #84, [ADR-0006](docs/adr/0006-one-public-entry-point-and-a-narrow-v3-interface.md)). `lanepaper` is a typography package, not a library of generic writing shortcuts, so the generic writing, emphasis, code, punctuation, symbol, currency, fraction, spacing, math, and reference helpers were removed rather than kept as compatibility aliases. Standard LaTeX, amsmath, and third-party packages (siunitx's `\unit`, `doc`'s `\meta`, ...) again own those names. No aliases are provided; update documents to the standard replacements below.

| Removed | Use instead |
|---------|-------------|
| `\strongemph`, `\importantnote` | `\textbf` |
| `\meta`, `\person`, `\acro`, `\regsc`, `\elegantsc`, `\refinedsc` | `\textsc` |
| `\critical`, `\bsc`, `\headsc`, `\inlinebsc`, `\elegantscbold` | `\textbf{\textsc{...}}` |
| `\term`, `\work`, `\subtleemph`, `\externalref`, `\smartitalic` | `\emph` |
| `\codecomment` | `\textit` |
| `\code`, `\inlinecode`, `\balancedcode`, `\filepath`, `\var` | `\texttt` |
| `\doccode{a}{b}` | `a: \texttt{b}` |
| `\authorname`, `\affiliation`, `\keywords` | title-page commands (`\articleauthors`, ...) or `\textsc`/`\emph` |
| `\emdash`, `\emdashclassic`, `\dashparen` | `---` |
| `\endash`, `\dashrange{a}{b}` | `--`, `a--b` |
| `\tdots`, `\fdots`, `\edots` | `\dots` |
| `\ldots`, `\cdots`, `\S`, `\P`, `\copyright`, `\dag`, `\ddag` | standard LaTeX (restored) |
| `\thinspace`, `\medspace`, `\thickspace` | standard amsmath (restored) |
| `\euro`, `\pound`, `\cent`, `\currency` | `\texteuro`, `\textsterling`, `\textcent`, `\textcurrency` |
| `\trademark`, `\registered`, `\servicemark` | `\texttrademark`, `\textregistered`, `\textsuperscript{SM}` |
| `\degrees`, `\half`, `\quarter`, `\threequarters` | `\textdegree`, `\textonehalf`, `\textonequarter`, `\textthreequarters` |
| `\super`, `\sub` | `\textsuperscript`, `\textsubscript` |
| `\sq`, `\dq`, `\nq` | csquotes' `\enquote` (or `` `...' `` / `` ``...'' ``) |
| `\wordspace`, `\emspace`, `\twoemspace`, `\abbrspace` | `\quad`, `\qquad`, `\,` |
| `\fig`, `\tab`, `\unit` | `Figure~\ref{...}`, `Table~\ref{...}`, siunitx's `\qty`/`\unit` |
| `\real`, `\complex`, `\integer`, `\rational`, `\natural`, `\field`, `\prob` | `\mathbb{R}`, `\mathbb{C}`, `\mathbb{Z}`, ... |
| `\hilbert`, `\banach`, `\algebra`, `\topology`, `\measure` | `\mathcal{H}`, `\mathcal{B}`, ... |
| `\norm`, `\abs`, `\inner`, `\set`, `\given` | `\lVert\,\rVert`, `\lvert\,\rvert`, `\langle\,\rangle`, `\{\,\}`, `\mid` |
| `\tr`, `\rank`, `\Span`, `\supp`, `\argmax`, `\argmin` | amsmath's `\DeclareMathOperator` |
| `\mathbinx`, `\mathrelx`, `\dint`, `\ssup`, `\ssub`, `\lim` | standard amsmath (`\lim` restored) |
| `\refpage`, `\pref`, `\seeref`, `\seealso` (and capitalized forms) | configure and use cleveref's `\cref`/`\Cref`/`\cpageref` |
| `\pdfcode`, `\pdfsc`, `\pdfemph`, `\pdfbf`, `\pdfit`, `\pdffilepath`, `\pdfvar` | hyperref's `\texorpdfstring` |

Cleveref is no longer configured by the package: a document that wants abbreviated names or parenthetical styles loads and configures cleveref itself. The title-page small caps this package still uses internally is private (`\lnp@titlesc`) and unchanged.
