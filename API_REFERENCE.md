# Lane LaTeX Template API Reference

Complete reference for all commands, environments, and options provided by the `lltpaperstyle` package.

## Table of Contents

1. [Package Options](#package-options)
2. [Title Page Commands](#title-page-commands)
3. [Typography Commands](#typography-commands)
4. [Spacing Commands](#spacing-commands)
5. [Emphasis and Semantic Commands](#emphasis-and-semantic-commands)
6. [Special Characters and Symbols](#special-characters-and-symbols)
7. [List Environments](#list-environments)
8. [Quotation Environments](#quotation-environments)
9. [Table and Figure Environments](#table-and-figure-environments)
10. [Mathematical Commands](#mathematical-commands)
11. [Cross-Reference Commands](#cross-reference-commands)
12. [Paragraph Commands](#paragraph-commands)
13. [Color Commands](#color-commands)
14. [Grid System Commands](#grid-system-commands)
15. [Footnote Commands](#footnote-commands)

## Package Options

### Loading the Package

```latex
\usepackage[options]{lltpaperstyle}
```

### Available Options

| Option | Default | Description |
|--------|---------|-------------|
| `grid` | off | Display baseline grid overlay for typography debugging |
| `nogrid` | **on** | Hide baseline grid (normal mode) |
| `minimal` | off | Load only essential features (dimensions, compilation fixes) |
| `natbib` | off | Use natbib compatibility mode instead of biblatex |
| `nocolor` | off | Disable all custom colors (black text only) |
| `draft` | off | Enable draft mode with visible overfull boxes |
| `nobiblatex` | off | Disable automatic biblatex loading |

### Examples

```latex
% Standard usage
\usepackage{lltpaperstyle}

% Show grid for debugging
\usepackage[grid]{lltpaperstyle}

% Minimal mode for compatibility
\usepackage[minimal]{lltpaperstyle}

% Multiple options
\usepackage[draft,grid]{lltpaperstyle}
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

#### `\sectionbreak`
Insert 2 grid units of white space.

#### `\asteriskbreak`
Three centered asterisks for thematic breaks.

```latex
\sectionbreak
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
| `\gridunit` | 13.2pt | One baseline grid unit |
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

#### `\strongemph{text}`
Bold emphasis for critical terms.

```latex
\strongemph{Important:} Read this carefully.
```

### Semantic Markup

#### `\term{term}`
Technical terms (italic).

```latex
The \term{baseline grid} ensures vertical rhythm.
```

#### `\person{name}`
Person names (small caps with tracking).

```latex
\person{Hermann Zapf} designed Palatino.
```

#### `\acro{ACRONYM}`
Acronyms (small caps with wide tracking).

```latex
\acro{PDF} stands for Portable Document Format.
```

#### `\work{title}`
Published works (italic).

```latex
See \work{The Elements of Typographic Style} by Bringhurst.
```

#### `\meta{metadata}`
Metadata (small caps).

```latex
\meta{Version 0.1.0-alpha} released June 2025.
```

#### `\critical{text}`
Critical notices (bold small caps).

```latex
\critical{Warning:} This will delete all files.
```

## Special Characters and Symbols

### Dashes

| Command | Output | Usage |
|---------|--------|-------|
| `\emdash` | — | Em dash with thin spaces |
| `\emdashclassic` | — | Em dash without spaces |
| `\emdashopen` | — | Em dash with word spaces |
| `--` | – | En dash (standard LaTeX) |

```latex
Typography\emdash the art of arranging type\emdash is essential.
Pages 10--20
2020--2025
```


### Ellipsis Variants

| Command | Output | Usage |
|---------|--------|-------|
| `\ldots` | … | Standard ellipsis |
| `\tdots` | … | Tight ellipsis for dialogue |
| `\cdots` | ⋯ | Centered dots for math |
| `\fdots` | … | French spacing ellipsis |
| `\edots` | …. | Ellipsis before period |

### Currency Symbols

| Command | Output | Description |
|---------|--------|-------------|
| `\euro` | € | Euro symbol |
| `\pound` | £ | Pound sterling |
| `\yen` | ¥ | Yen symbol |
| `\cent` | ¢ | Cent symbol |
| `\currency` | ¤ | Generic currency |

### Technical Symbols

| Command | Output | Description |
|---------|--------|-------------|
| `\degrees` | ° | Degree symbol |
| `\trademark` | ™ | Trademark |
| `\registered` | ® | Registered |
| `\copyright` | © | Copyright |
| `\S` | § | Section symbol |
| `\P` | ¶ | Paragraph symbol |

### Mathematical Symbols in Text

| Command | Output | Description |
|---------|--------|-------------|
| `\textpm` | ± | Plus-minus |
| `\texttimes` | × | Multiplication |
| `\textdiv` | ÷ | Division |
| `\textapprox` | ≈ | Approximately |
| `\textinfty` | ∞ | Infinity |

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

#### `\sq{text}`
Smart single quotes.

```latex
\sq{quoted text}  % 'quoted text'
```

#### `\dq{text}`
Smart double quotes.

```latex
\dq{quoted text}  % "quoted text"
```

#### `\nq{outer}{inner}`
Nested quotes.

```latex
\nq{She said}{Hello}  % "She said 'Hello'"
```

## Table and Figure Environments

### Enhanced Table Environments

#### `gridtable`
Table with automatic grid-aligned row height.

```latex
\begin{gridtable}[tbp]
  \caption{Grid-Aligned Table}
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
Figure with grid-aligned dimensions.

```latex
\begin{gridfigure}[tbp]
  \centering
  \gridincludegraphics[width=0.8\textwidth]{figure.pdf}
  \caption{Grid-aligned figure}
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

### Mathematical Operators

| Command | Output | Description |
|---------|--------|-------------|
| `\tr` | tr | Trace |
| `\rank` | rank | Rank |
| `\Span` | span | Span |
| `\supp` | supp | Support |
| `\argmax` | arg max | Argmax |
| `\argmin` | arg min | Argmin |

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

### Mathematical Helpers

#### `\set{A}`
Set notation with proper spacing.

```latex
$x \in \set{A}$
```

#### `\abs{x}`
Absolute value.

```latex
$\abs{x} < \epsilon$
```

#### `\norm{v}`
Vector norm.

```latex
$\norm{v} = 1$
```

## Cross-Reference Commands

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

### Specialized References

#### `\refpage{label}`
Reference with page number.

```latex
\refpage{tab:results}  % "table 1 on page 5"
```

#### `\pref{label}`
Parenthetical reference.

```latex
The results \pref{fig:main} demonstrate...  % "The results (fig. 2) demonstrate..."
```

#### `\seealso{label}`
"See also" reference.

```latex
\seealso{sec:methods}  % "see also §2.3"
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

#### `\quoteparagraph{text}` *(requires llthochuli module)*
Paragraph with hanging opening quote.

```latex
% Requires: \usepackage{paper/modules/llthochuli}
\quoteparagraph{"When we examine the evidence..."}
```

### Dialogue Commands

#### Dialogue Commands *(not yet implemented)*

The following dialogue commands are planned but not yet implemented:
- `\dialogue{text}` - Standard dialogue formatting
- `\rapidexchange{text}` - Quick dialogue with reduced indent  
- `\speaker{name}{words}` - Dialogue with speaker name

```latex
% Future implementation:
% \speaker{Alice}{I think we should reconsider.}
% \speaker{Bob}{I agree completely.}
```

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

### Color Commands

#### `\subtleemph{text}`
Conservative blue emphasis.

#### `\importantnote{text}`
Restrained red for critical info.

#### `\codecomment{text}`
Italic gray for code comments.

#### `\externalref{text}`
Enhanced navy for external links.

## Grid System Commands

### Grid Display

#### `\showgrid`
Display baseline grid overlay.

#### `\hidegrid`
Hide baseline grid.

### Grid-Aligned Commands

#### `\gridincludegraphics[options]{file}`
Include graphics with height rounded to grid.

```latex
\gridincludegraphics[width=0.8\textwidth]{figure.pdf}
```

#### `\vspacegrid{units}`
Add grid-aligned vertical space.

```latex
\vspacegrid{2}  % Add 2 grid units
```

## Footnote Commands

### Title Page Footnotes

#### `\titlefootnotesetup`
Switch to symbols (*, †, ‡).

#### `\titlefootnotereset`
Return to numbers.

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

% Emphasis
\emph{emphasis}
\term{technical term}
\person{Name}
\acro{ACRONYM}

% Lists
\begin{itemize}
\begin{enumerate}
\begin{academicitem}

% Quotes
\begin{quote}...\quoteattribution{Author}\end{quote}

% References
\cref{label}
\Cref{label}

% Spacing
\vspace{\gridunit}
\vspace{\halfgridunit}

% Special characters
\emdash
\endash
\degrees
```

---

This API reference covers all major commands and environments provided by the `lltpaperstyle` package. For additional details, see the package documentation and example files.