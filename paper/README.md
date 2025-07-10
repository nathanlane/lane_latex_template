# paperstyle.sty Documentation

**Version 1.6** | **Modular LaTeX Style Package for Academic Typography**

A comprehensive LaTeX style package implementing professional typography principles from Matthew Butterick's *Practical Typography*, Tim Brown's *Modular Scale*, and Jost Hochuli's *Detail in Typography*.

## Table of Contents

- [Quick Start](#quick-start)
- [Modular Architecture](#modular-architecture)
- [Typography Framework](#typography-framework)
- [Font System Architecture](#font-system-architecture)
- [Title Page System](#title-page-system)
- [Advanced Features](#advanced-features)
- [Chicago-Compliant Appendix System](#chicago-compliant-appendix-system)
- [Professional Figures and Tables](#professional-figures-and-tables)
- [Citation and Bibliography System](#citation-and-bibliography-system)
- [Special Characters and Symbols](#special-characters-and-symbols)
- [API Reference](#api-reference)
- [Configuration Options](#configuration-options)
- [Troubleshooting](#troubleshooting)
- [Technical Implementation](#technical-implementation)

## Quick Start

### Basic Usage

```latex
\documentclass[11pt]{article}
\usepackage{lltpaperstyle}

\begin{document}
\section{Your Content}
Professional typography is automatically applied.
\end{document}
```

### With Bibliography

```latex
\documentclass[11pt]{article}
\input{paper/preamble.tex}  % Includes lltpaperstyle + biblatex-chicago

\begin{document}
Your content with citations~\cite{key}.
\printbibliography
\end{document}
```

### With Appendices

```latex
\begin{document}
Main content...

\startappendices
  \input{appendices/main_appendix.tex}
  \input{appendices/tech_appendix.tex}
\finishappendices
\end{document}
```

## Modular Architecture

**Since v1.6**: The package is structured as independent modules for better maintainability and customization.

### Module Structure

```
lltpaperstyle.sty (main package)
├── Core Modules (automatically loaded):
│   ├── lltcompilation-fixes-simple.sty - Common LaTeX warning fixes
│   ├── lltfonts.sty                   - Font configuration (Pagella, Inconsolata, math)
│   ├── lltcolors.sty                  - Professional color system
│   ├── lltdimensions.sty              - Grid system and spacing definitions
│   ├── lltheadings.sty                - Section heading styles with colors
│   └── lltlists.sty                   - List typography with refined bullets
│
└── Optional Enhancement Modules:
    ├── lltparagraphs.sty              - Advanced paragraph formatting
    ├── lltmicrotype-config.sty        - Enhanced character protrusion
    ├── lltheadings-gridlocked.sty     - Stricter grid alignment
    ├── lltmathematics-gridlocked.sty  - Minimal math flexibility
    ├── llthochuli-refinements.sty     - Advanced optical adjustments
    ├── lltfont-features.sty           - Full Pagella feature access
    └── lltfont-fallbacks.sty          - Compatibility mode
```

### Using Individual Modules

Load only the features you need:

```latex
% Just the professional color system
\RequirePackage{lltcolors}

% Or just the heading styles
\RequirePackage{lltheadings}
```

### Custom Module Configuration

Load modules with custom settings before the main package:

```latex
% Custom grid unit
\newlength{\gridunit}
\setlength{\gridunit}{12pt}
\RequirePackage{lltdimensions}

% Then load main package
\usepackage{lltpaperstyle}
```

For complete module documentation, see [MODULES.md](MODULES.md).

#### List Typography Module

`lists.sty` gives you production-grade list environments aligned to the 13.2 pt baseline grid and a bullet hierarchy that follows Butterick & Hochuli’s guidance.

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

## Typography Framework

### Core Philosophy

The style synthesizes three complementary approaches:

1. **Mathematical Harmony** (Tim Brown): Perfect Fourth ratio (1.333) creates proportional hierarchy
2. **Professional Foundation** (Butterick): Optimal reading conditions with 65-character line length
3. **Archival Refinements** (Hochuli): Micro-typographic perfection and technical excellence

### Baseline Grid System

All spacing uses the **13.2pt grid unit** system:

```latex
\vspace{\gridunit}        % 1 unit (13.2pt)
\vspace{0.5\gridunit}     % 0.5 units (6.6pt)  
\vspace{2\gridunit}       % 2 units (26.4pt)
```

### Modular Scale Hierarchy

**Size Progression** following Perfect Fourth ratio (1.333):

| Element | Size | Scale Factor | Usage |
|---------|------|--------------|-------|
| Section | 18pt | 1.333³ | `\section{}` |
| Subsection | 14pt | 1.333¹ | `\subsection{}` |
| Subsubsection | 12pt | 1.333^0.5 | `\subsubsection{}` |
| Body text | 11pt | 1.0 (base) | Standard text |
| Footnotes | 9pt | 1/1.2 | `\footnote{}` |

## Font System Architecture

### Text Typography (TeX Gyre Pagella)

```latex
% Professional Palatino-based typography
\usepackage{tgpagella}
% With oldstyle figures and superior small caps
```

**Features:**
- **altP**: Historical open P form for authentic Renaissance appearance
- **osf**: Oldstyle figures (0123456789) for text integration
- **p**: Proportional figure spacing
- **sups**: Superior figures for ordinals and footnotes
- **swashQ**: Elegant swash Q for enhanced typographic texture

### Mathematical Typography (newtxmath + mathalfa)

```latex
% Harmonized serif mathematics
\usepackage[libertine]{newtxmath}
\usepackage[cal=boondoxo,bb=boondox,frak=boondox]{mathalfa}
```

**Enhanced Symbol Sets:**
- **Calligraphic**: Boondoxo for script letters (𝒜, ℬ, 𝒞...)
- **Blackboard Bold**: Boondox for number sets (ℝ, ℂ, ℕ...)
- **Fraktur**: Boondox for Gothic letters (𝔄, 𝔅, 𝔇...)

### Monospace Typography (Inconsolata/zi4)

```latex
% Optimized for Bembo harmony
\usepackage[varqu,varl,scaled=0.93]{zi4}
```

**Optimization Features:**
- **scaled=0.93**: Precise scaling for x-height harmony with Bembo
- **varqu**: Enhanced quotation marks for code clarity
- **varl**: Improved lowercase L distinction
- **Weight compensation**: 98% scaling prevents visual dominance

## Advanced Features

### Enhanced Bold Small Caps System

Following fbb/fontaxes principles with weight compensation:

```latex
% General purpose bold small caps
\bsc{Text}                    % 0.97× scaling for weight balance

% Contextual variants
\headsc{Heading}              % Large with 5% letterspacing
\inlinebsc{Inline}            % Footnote-sized for inline use
\balancedbsc{Balanced}        % Color-compensated for headings
```

### Professional Color System

Accessibility-compliant (WCAG 2.1 AA) with comprehensive color palette:

```latex
% Text Colors
textblack       % Near-black (5% gray) for body text
subtlegray      % 45% gray for page numbers, subtle elements
bulletgray      % 25% gray for list bullets
dashgray        % 30% gray for en-dash markers
circlegray      % 35% gray for tertiary bullets

% Heading Colors (Hierarchy)
sectioncolor     % Softened navy (RGB 25,50,80)
subsectioncolor  % Muted midnight (RGB 40,40,55)
subsubcolor      % Medium charcoal (25% gray)
paragraphcolor   % Dark gray (15% gray)

% Link Colors
linknavy        % Professional navy (RGB 0,102,180)
linkblue        % Deeper blue (RGB 0,68,136) for DOIs

% Special Colors
codecolor       % Dark gray (RGB 26,26,26) for monospace
diglinkcolor    % Blue-purple for digital links

% Semantic Commands
\subtleemph{text}      % Conservative blue emphasis
\importantnote{text}   % Restrained red for critical info
\externalref{text}     % Enhanced navy blue for links
```

### Intelligent Code Typography

Systematic commands for different code contexts:

```latex
\code{inline-code}                 % Weight-compensated general use
\inlinecode{spaced-code}           % Micro-kerned to prevent text disruption
\balancedcode{general-mono}        % Color-balanced monospace
\filepath{/path/to/file}           % Proper hyphenation for long paths
\var{variable_name}                % Italic emphasis for variables
\doccode{Description}{code}        % Mixed serif/mono documentation
```

## Title Page System

### Overview

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

### Title Commands

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

### Author Formatting

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

### Spacing Principles

All vertical spacing follows the 13.2pt grid system:
- **After title**: 1.5 grid units (19.8pt)
- **After authors**: 1.5 grid units (19.8pt)
- **Before abstract**: 2 grid units (26.4pt)
- **Abstract internal**: 0.5 grid units (6.6pt)

### Footnote System

Systematic sizing with baseline-aligned spacing:

**Sizing Hierarchy:**
- **Superscript**: 8pt (11pt ÷ 1.375) with oldstyle numerals
- **Footnote text**: 9pt (11pt ÷ 1.2) with 11pt leading
- **Hanging indent**: 1.5em for optimal visual balance

**Spacing System:**
- **Above footnotes**: 13.2pt (1 grid unit)
- **Between footnotes**: 6.6pt (0.5 grid units)
- **Footnote rule**: 2in width, 0.4pt height for subtle elegance

### Enhanced Optical Margin Alignment

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

### Semantic Emphasis Hierarchy

Sophisticated emphasis system optimized for TeX Gyre Pagella:

```latex
% Hierarchy Levels (by frequency of use)
\emph{text}            % Primary emphasis (italic↔roman)
\strongemph{text}      % Bold for critical terms (<5% of text)
\term{baseline grid}   % Technical terms (italic)
\person{Hermann Zapf}  % Names (small caps, 2.5% tracking)
\acro{PDF}            % Acronyms (small caps, 4% tracking)
\work{Book Title}     % Published works (italic)
\critical{WARNING}    % Maximum emphasis (bold small caps)

% Smart nesting
\emph{outer \emph{inner} outer}  % → italic roman italic
```

### Professional Footnote System

Foundry-optimized specifications for TeX Gyre Pagella:

```latex
% Size Hierarchy
Footnote text: 8.5pt (77% of 11pt body)
Superscript: 6pt (70% of footnote size)
Leading: 11pt (aligns to 0.833 gridlines)
Hanging indent: 7pt (0.53 grid units)

% Grid-Compliant Spacing
Rule position: 26.4pt below text (2 grid units)
Rule to footnote: 13.2pt (1 grid unit)
Between footnotes: 3.3pt (0.25 grid units)
Rule specs: 33% width, 0.4pt thickness, text color

% Title Page Adjustments
\titlefootnotesetup    % Switches to symbols (*, †, ‡)
\titlefootnotereset    % Returns to numbers
```

## Chicago-Compliant Appendix System

### Overview

Professional appendix management with automatic single/multiple detection:

```latex
\begin{documentAppendices}
  \input{appendices/first.tex}
  \input{appendices/second.tex}
\end{documentAppendices}
```

### Automatic Behavior

**Multiple Appendices (2+):**
- Table of Contents: "Appendices" section header
- Numbering: "Appendix A", "Appendix B", etc.
- Cross-references: Full "Appendix A" format

**Single Appendix (1):**
- Table of Contents: Direct appendix entry
- Numbering: "Appendix" (no letter)
- Cross-references: Simple "Appendix" format

### Implementation Details

The system uses a two-pass auxiliary file mechanism:

1. **First Pass**: Counts appendices and writes count to `.aux` file
2. **Second Pass**: Reads count and formats accordingly
3. **Detection Logic**: `\ifnum\paperstyle@totalappendices>1`

### Usage Patterns

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

## Professional Figures and Tables

### Figure Management

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

### Table Design System

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

### Grid-Aligned Tables

```latex
% Standard 13.2pt rows
\begin{gridtable}[tbp]
  % Content with automatic \arraystretch
\end{gridtable}

% Regression tables (19.8pt rows)
\begin{regressiontable}[tbp]
  % For statistical results with standard errors
\end{regressiontable}

% Compact tables (9.9pt rows)
\begin{compacttable}[tbp]
  % For dense information
\end{compacttable}
```

### Landscape and Rotation Support

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

### QJE-Style Notes System

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

### Float Management

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
  % Grid-aligned here placement
\end{herefloat}

% Visual balance
\balancefloatpage       % Adds flexible space
\compensatetopfloat     % Adds grid unit after large floats
\showfloatstats         % Debug placement in log
```

## Citation and Bibliography System

### Primary System (biblatex with biber)

```latex
% Essential citation commands
\textcite{key}                    % Smith (2023) argues...
\autocite{key}                    % ...results (Smith 2023)
\textcite[45--48]{key}           % Smith (2023, 45-48)
\autocite[see also][]{key}       % (see also Smith 2023)
\autocite[][chap. 3]{key}        % (Smith 2023, chap. 3)
\textcite{key1,key2,key3}        % Smith (2023), Jones (2023), and Brown (2023)

% Specialized citations
\citeauthor{key}                  % Smith
\citeyear{key}                    % (2023)
\citetitle{key}                   % Article Title
```

### Bibliography Database Best Practices

```bibtex
% Enhanced article entry
@article{smith2023,
  title = {Academic Typography Standards},
  author = {Jane A. Smith and Robert B. Johnson},
  journal = {Journal of Academic Design},
  volume = {15},
  number = {3},
  pages = {245--267},
  year = {2023},
  doi = {10.1000/journal.2023.15.3.245},
  annotation = {Demonstrates professional citation integration.}
}

% Online resource
@online{guidelines2023,
  title = {Typography Guidelines for Academic Institutions},
  author = {{University Typography Consortium}},
  year = {2023},
  url = {https://typography.edu/guidelines},
  urldate = {2025-06-28}
}

% Preprint
@misc{preprint2023,
  title = {Machine Learning Typography Optimization},
  author = {Emma Rodriguez and Thomas Kim},
  year = {2023},
  eprint = {2301.12345},
  eprinttype = {arxiv},
  eprintclass = {cs.HC}
}
```

### Cross-Reference Typography (cleveref)

```latex
% Smart references
\cref{fig:example}              % → "figure 1"
\Cref{fig:example}              % → "Figure 1" (sentence start)
\cref{fig:a,fig:b,fig:c}        % → "figures 1, 2 and 3"
\crefrange{fig:a}{fig:d}        % → "figures 1–4"

% Specialized references
\refpage{tab:results}           % → "table 1 on page 5"
\pref{fig:summary}              % → "(fig. 8)" parenthetical
\seealso{sec:methods}           % → "see also §2.3"

% Equations (automatic parentheses)
\cref{eq:main}                  % → "(1)"
\Cref{eq:main}                  % → "Equation (1)"
```

## Special Characters and Symbols

### Comprehensive Symbol System

```latex
% Dashes with context-aware spacing
\emdash                      % Em dash with thin spaces
\endash                      % En dash for ranges
\dashrange{2000}{2025}       % Smart range: 2000–2025
\dashcompound{twenty}{first} % Compound: twenty-first

% Ellipsis variants
\ldots                       % Standard with word spaces
\tdots                       % Tight for dialogue
\cdots                       % Mathematical (centered)
\fdots                       % French spacing
\edots                       % Before period

% Technical symbols
\degrees                     % Degree with spacing (25°C)
\primetext                   % Prime mark (6′)
\dblprimetext               % Double prime (6″)
\ordst, \ordnd, \ordrd, \ordth % Ordinals (1st, 2nd, 3rd, 4th)
\S, \P                      % Section § and paragraph ¶

% Currency symbols
\euro, \pound, \yen          % €, £, ¥ with proper spacing
\cent, \currency            % ¢, ¤ with tighter spacing

% Legal and copyright
\trademark                   % ™ superscript
\registered                  % ® superscript
\copyright                   % © with spacing
\servicemark                % ℠ superscript

% Mathematical in text
\textpm                      % ± with spacing
\texttimes                   % × with spacing
\textdiv                     % ÷ with spacing
\textapprox                  % ≈ with spacing
\textinfty                   % ∞ with spacing

% Arrows
\larrow, \rarrow             % ← → with spacing
\uarrow, \darrow             % ↑ ↓ with spacing

% Smart quotes
\sq{text}                    % 'text' with kerning
\dq{text}                    % "text" with kerning
\nq{outer}{inner}            % "outer 'inner' outer"

% Fractions and scripts
\half, \quarter              % ½, ¼
\threequarters               % ¾
\super{text}                 % Superscript with spacing
\sub{text}                   % Subscript with spacing

% Smart references
\fig{1}                      % Figure~1 (non-breaking)
\tab{2}                      % Table~2 (non-breaking)
\unit{5}{km}                 % 5 km with proper spacing

% Special spacing
\thinspace                   % 1/16 em (hair space)
\medspace                    % 1/8 em
\thickspace                  % 1/4 em
\wordspace                   % 1/3 em
\emspace                     % 1 em
\twoemspace                  % 2 em

% Other special
\apos                        % Smart apostrophe
\dag, \ddag                  % †, ‡ with spacing
```

## API Reference

### Typography Commands

#### Text Formatting

```latex
% Semantic emphasis hierarchy
\emph{text}                        % Primary emphasis (italic↔roman)
\strongemph{text}                  % Strong emphasis (bold)
\term{technical term}              % Technical terms (italic)
\person{Name}                      % Person names (small caps, 2.5% tracking)
\acro{NASA}                        % Acronyms (small caps, 4% tracking)
\work{Title}                       % Published works (italic)
\meta{metadata}                    % General metadata (small caps, 3% tracking)
\critical{WARNING}                 % Critical emphasis (bold small caps, 4.5% tracking)

% Smart nesting handlers
\smartitalic{text}                 % Context-aware italic
\smartbold{text}                   % Context-aware bold

% Special formatting
\refinedsc{text}                   % Regular small caps with tracking
\refinedscbold{text}               % Bold small caps with tracking
\titlesc{text}                     % Title small caps (8-12% tracking)
```

#### Mathematical Notation

```latex
% Number sets
\real, \complex, \integer, \rational, \natural, \field, \prob

% Operators
\norm{vector}                      % ||vector||
\abs{number}                       % |number|
\inner{u}{v}                       % ⟨u,v⟩
\set{elements}                     % {elements}

% Mathematical spaces (calligraphic)
\hilbert, \banach, \algebra, \topology, \measure

% Operators
\tr, \rank, \Span, \supp, \argmax, \argmin
```

#### Code Typography

```latex
\code{basic-code}                  % General inline code
\inlinecode{spaced-code}           % Micro-spaced code
\balancedcode{mono-text}           % Balanced monospace
\filepath{/path/to/file}           % File paths with hyphenation
\var{variable_name}                % Italic variables
\doccode{Description}{code}        % Mixed serif/mono
```

#### Color and Emphasis

```latex
\subtleemph{text}                  % Conservative blue emphasis
\importantnote{text}               % Restrained red for warnings
\externalref{text}                 % Navy blue for external links
\internalref{text}                 % Gray for internal references
\codecomment{text}                 % Italic gray for code comments
```

### Appendix System Commands

```latex
% Modern interface
\begin{documentAppendices}
  \input{appendices/file.tex}
\end{documentAppendices}

% Legacy interface (backward compatible)
\startappendices
\finishappendices
```

### Title Page Commands

```latex
% Dynamic title commands
\articletitle{Title}                        % Auto-adjusts size (16-18pt)
\articletitlefootnote{Title}{Acknowledgment} % Title with footnote
\articletitlecompact{Title}                 % Fixed 16pt for many authors
\articletitlecompactfootnote{Title}{Note}   % Compact with footnote

% Author formatting
\articleauthors{Names}                      % 12pt with \authorspace between
\authorspace                                % 5% of text width
\elegantauthor{Name}                        % Small caps author name

% Supporting elements
\articledate{\today}                        % Near-black for visibility
\begin{articleabstract}                     % Golden ratio width (0.618×textwidth)
  Abstract text...
\end{articleabstract}
\articlekeywords{keyword1, keyword2}        % Refined punctuation spacing
\articlejel{A10, B20, C30}                 % JEL code formatting

% Footnote modes
\titlefootnotesetup                         % Switch to symbols (*, †, ‡)
\titlefootnotereset                         % Return to numbers
```

### Paragraph Typography Commands

```latex
% Style switching
\classicalparagraphs      % 13.2pt indent, 0pt spacing (default)
\modernparagraphs         % 0pt indent, 6.6pt spacing
\hybridparagraphs         % 9.9pt indent, 3.3pt spacing
\quartergridparagraphs    % 13.2pt indent, 3.3pt spacing
\thirdgridparagraphs      % 13.2pt indent, 4.4pt spacing

% Special paragraphs
\noindentpar              % Force flush left
\forceindent              % Force indentation
\centeredpar{text}        % Centered block
\compactpar               % Reduces space before by 3.3pt
\loosepars                % Adds 3.3pt before

% Optical refinements
\quoteparagraph{"Quote"} % Hanging opening quote
\dropcap{L}{etter}        % Two-line drop cap
\paragraphbreak           % Three asterisks
\numberedparagraph        % Margin numbering
\resetparnumbers          % Reset counter
\sidenote{text}           % Margin annotation

% Dialogue formatting
\dialogue{text}           % Standard dialogue
\rapidexchange{text}      % Quick exchange
\speaker{Name}{words}     % Small caps speaker
```

### Quotation Environments

```latex
% Standard block quote
\begin{quote}
  Typography is the visual component of the written word.
  \quoteattribution{Matthew Butterick}
\end{quote}

% Multi-paragraph quotation
\begin{quotation}
  First paragraph with indentation.
  
  Second paragraph maintains structure.
\end{quotation}

% Emphasis quote
\begin{emphasisquote}
  Typography exists to honor content.
  \quoteattribution{Robert Bringhurst}
\end{emphasisquote}
```

### List Typography Commands

```latex
% Available environments
\begin{itemize}           % Standard with refined bullets
\begin{academicitem}      % En-dash primary marker
\begin{compactitem}       % No inter-item spacing
\begin{displayitem}       % Bold items with generous spacing
\begin{readableitem}      % Enhanced 0.5 unit spacing
\begin{inlineitem}        % Inline (a); (b); (c)
\begin{enumerate}         % Oldstyle figures
\begin{description}       % Small caps labels

% Bullet symbols
\refinedbullet            % 80% scaled, 25% gray
\refineddash              % En-dash, 30% gray
\refinedcircle            % Open circle, 35% gray
\refineddot               % Centered dot separator
```

### Grid Development Tools

```latex
% Visual overlay
\usepackage{lltgridoverlay}
\showgrid                 % Display grid lines
\hidegrid                 % Hide grid lines

% Grid-aligned images
\gridincludegraphics[width=0.8\textwidth]{file}
\begin{gridfigure}[tbp]
  % Complete grid-aligned figure
\end{gridfigure}

% Grid spacing
\gridunit                 % 13.2pt
\halfgridunit             % 6.6pt
\quartergridunit          % 3.3pt
```

## Configuration Options

### Customizable Typography

**Modular Scale Alternatives:**
```latex
% Replace Perfect Fourth (1.333) with:
% Major Third: 1.25
% Golden Ratio: 1.618
% Major Sixth: 1.667
```

**Spacing Adjustments:**
```latex
% Classical indentation system (Bringhurst/Hochuli)
\setlength{\parindent}{12pt}                         % ~1.1em for Bembo
\setlength{\parskip}{0pt plus 1pt minus 0.5pt}       % Minimal spacing
\setlength{\abovedisplayskip}{12.65pt plus 3pt minus 3pt}
```

**Color Customization:**
```latex
% Redefine any color in the professional palette
\definecolor{paragraphgray}{gray}{0.25}    % Adjust contrast
\definecolor{linknavy}{RGB}{0,102,180}     % Modify link color
```

### Microtype Tuning

```latex
% Enhanced character protrusion
factor=1100                        % Conservative protrusion for Bembo

% Word spacing flexibility  
stretch=10, shrink=10              % Subtle elasticity

% Small caps tracking
\SetTracking{encoding={T1}, shape=sc}{30}  % 3% for Bembo
```

## Troubleshooting

### Common Issues

**Package Loading Order:**
```latex
% Correct order (implemented in paperstyle.sty)
\usepackage{hyperref}              % Must load before cleveref
\usepackage{cleveref}              % Enhanced cross-referencing
```

**Appendix Count Issues:**
```latex
% If appendix detection fails, delete auxiliary files and recompile
rm *.aux *.out *.toc
pdflatex main.tex
pdflatex main.tex
```

**Font Warnings:**
```latex
% Common fontaxes warnings are expected and harmless
Package fontaxes Warning: Axis `shape` not supported...
```

### Compatibility

**Document Classes:**
- ✅ `article` (recommended)
- ✅ `report` (chapter-based appendices)
- ✅ `book` (chapter-based appendices)
- ❌ `memoir` (requires modifications)

**Required Packages:**
```latex
% Core dependencies (auto-loaded)
fbb, zi4, newtxmath, mathalfa, microtype, titlesec,
enumitem, caption, geometry, appendix, cleveref
```

## Technical Implementation

### Microtype Configuration

```latex
% Hochuli's optimal settings for fbb/Bembo
\usepackage[
  activate={true,nocompatibility},
  final,
  tracking=true,
  kerning=true,
  spacing=true,
  factor=1100,                     % Enhanced character protrusion
  stretch=10,                      % Conservative word spacing
  shrink=10
]{microtype}
```

### Baseline Grid Mathematics

```latex
% All spacing derives from 12.65pt baseline
Base leading: 11pt × 1.15 = 12.65pt
Half baseline: 12.65pt ÷ 2 = 6.325pt
Display math: 12.65pt ± 3pt
Paragraph skip: 6.325pt + 2pt - 1pt
```

### Appendix Counter Logic

```latex
% Two-pass auxiliary file mechanism
\newcounter{appendixcount}
\newcommand{\paperstyle@writeappendixcount}{%
  \immediate\write\@auxout{%
    \string\gdef\string\paperstyle@totalappendices{\theappendixcount}%
  }%
}

% Conditional formatting based on count
\ifnum\paperstyle@totalappendices>1\relax
  \multipleappendicestrue
\else
  \multipleappendicesfalse
\fi
```

### Performance Considerations

- **Compilation Speed**: Two-pass system requires `pdflatex` twice for appendix detection
- **Memory Usage**: Microtype and font loading increase memory requirements
- **Compatibility**: Tested with TeX Live 2023+ and MiKTeX current

---

## Version History

- **v1.6** (2025-07): Full modularization with enhanced features:
  - Separated microtype-config module with 1400-unit protrusion
  - Added paragraphs module for advanced formatting
  - Implemented grid-locked variants for strict alignment
  - Added landscape/rotation support for social science papers
  - Enhanced color system with semantic hierarchy
  - Improved footnote system with title page variants
- **v1.5** (2025-07): Modularization and optical margin alignment:
  - Split into independent modules (fonts, colors, dimensions, headings, lists)
  - Enhanced character protrusion with size/weight-specific settings
  - Added compilation-fixes-simple module
- **v1.4** (2025-07): Cross-reference typography with cleveref
- **v1.3** (2025-07): Mathematical typography optimization for Pagella
- **v1.2** (2025-06): Added Chicago-compliant appendix system
- **v1.1** (2025-06): Enhanced bold small caps system
- **v1.0** (2025-06): Initial release with Butterick/Brown/Hochuli synthesis

For support and updates, see the main repository documentation.