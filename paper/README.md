# lanepaper Documentation

**v2.0** | **Modular LaTeX Style Package for Academic Typography**

A comprehensive LaTeX style package implementing professional typography principles from Matthew Butterick's *Practical Typography*, Tim Brown's *Modular Scale*, and Jost Hochuli's *Detail in Typography*.

## Table of Contents

- [Modular Architecture](#modular-architecture)
- [Typography Framework](#typography-framework)
- [Font System Architecture](#font-system-architecture)
- [Title Page System](#title-page-system)
- [Advanced Features](#advanced-features)
- [Chicago-Compliant Appendix System](#chicago-compliant-appendix-system)
- [Professional Figures and Tables](#professional-figures-and-tables)
- [Citation and Bibliography System](#citation-and-bibliography-system)
- [Special Characters and Symbols](#special-characters-and-symbols)
- [Technical Implementation](#technical-implementation)

For quick start, basic usage, and compilation instructions, see [`../README.md`](../README.md).

## Modular Architecture

**Since v1.5-alpha**: The package is structured as independent modules for better maintainability and customization.

### Module Structure

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
    ├── lnpheadingsgridlocked.sty      - Stricter grid alignment
    ├── lnpmathgridlocked.sty          - Minimal math flexibility
    ├── lnphochuli.sty                 - Optical adjustments; kerning pairs and last-line control apply on load; ligature suppression and hanging-quote commands are opt-in
    ├── lnpfontfeatures.sty            - Full Pagella feature access
    └── lnpfontfallbacks.sty           - Compatibility mode
```

### Using Individual Modules

Load only the features you need:

```latex
% Just the professional color system
\RequirePackage{lnpcolors}

% Or just the heading styles
\RequirePackage{lnpheadings}
```

### Custom Module Configuration

Load modules with custom settings before the main package:

```latex
% Custom grid unit
\newlength{\gridunit}
\setlength{\gridunit}{12pt}
\RequirePackage{lnpdimensions}

% Then load main package
\usepackage{lanepaper}
```

For complete module documentation, see [modules/README.md](modules/README.md).

#### List Typography Module

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

#### Paragraph Spacing Commands

Paragraph style switchers (indent and parskip per command):

```latex
\classicalparagraphs      % 13.2pt indent, 0pt parskip (default)
\modernparagraphs         % 0pt indent, 6.6pt parskip
\hybridparagraphs         % 9.9pt indent, 3.3pt parskip
\quartergridparagraphs    % 13.2pt indent, 3.3pt parskip
\thirdgridparagraphs      % 13.2pt indent, 4.4pt parskip
```

## Typography Framework

### Core Philosophy

The style synthesizes three complementary approaches:

1. **Mathematical Harmony** (Tim Brown): Perfect Fourth ratio (1.333) creates proportional hierarchy
2. **Professional Foundation** (Butterick): Optimal reading conditions with 65-character line length
3. **Archival Refinements** (Hochuli): Micro-typographic perfection and technical excellence

### Spacing Quantum System

Most spacing uses the **13.2pt spacing quantum** system (a spacing unit; the
body baseline measures 16.32pt — see `../docs/typography/BASELINE-GRID-DECISION.md`):

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

### Mathematical Typography (newpxmath + mathalfa)

```latex
% Harmonized serif mathematics
\usepackage{newpxmath}
\usepackage[cal=boondoxo,bb=boondox,frak=boondox]{mathalfa}
```

**Enhanced Symbol Sets:**
- **Calligraphic**: Boondoxo for script letters (𝒜, ℬ, 𝒞...)
- **Blackboard Bold**: Boondox for number sets (ℝ, ℂ, ℕ...)
- **Fraktur**: Boondox for Gothic letters (𝔄, 𝔅, 𝔇...)

### Monospace Typography (Inconsolata/zi4)

```latex
% Scaled for x-height harmony with Pagella
\usepackage[varqu,varl,scaled=0.96]{zi4}
```

**Optimization Features:**
- **scaled=0.96**: Precise scaling for x-height harmony with Pagella
- **varqu**: Enhanced quotation marks for code clarity
- **varl**: Improved lowercase L distinction

## Advanced Features

### Enhanced Bold Small Caps System

Following fontaxes principles with weight compensation:

```latex
% General purpose bold small caps (alias for \critical)
\bsc{Text}                    % Bold small caps, 4.5% tracking

% Contextual variants
\headsc{Heading}              % Bold small caps, 6% letterspacing
\inlinebsc{Inline}            % Bold small caps, 4.5% tracking (no size change)
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

All vertical spacing follows the 13.2pt quantum system:
- **After title**: 1.5 grid units (19.8pt)
- **After authors**: 1.5 grid units (19.8pt)
- **Before abstract**: 2 grid units (26.4pt)
- **Abstract internal**: 0.5 grid units (6.6pt)

### Footnote System

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

% Context-aware nesting handlers
\smartitalic{text}               % Italic in roman context, roman in italic context
\smartbold{text}                 % Bold in regular context, bold-italic in bold context
```

### Professional Footnote System

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
3. **Detection Logic**: `\ifnum\lnp@totalappendices>1`

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

The canonical path is to load `lanepaper`, which auto-loads the default
biblatex configuration, then register `references.bib`. Use
`\usepackage[nobiblatex]{lanepaper}` only when loading biblatex manually with
custom options.

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

For the complete command reference, see [`../API_REFERENCE.md`](../API_REFERENCE.md).

## Compatibility

**Document Classes:**
- ✅ `article` (recommended)
- ✅ `report` (chapter-based appendices)
- ✅ `book` (chapter-based appendices)
- ❌ `memoir` (requires modifications)

**Core dependencies** (auto-loaded):
`tgpagella`, `zi4`, `newpxmath`, `mathalfa`, `microtype`,
`enumitem`, `caption`, `geometry`, `appendix`, `cleveref`

For appendix count issues, delete auxiliary files and recompile:
```bash
latexmk -C main.tex  # or: rm *.aux *.out *.toc && pdflatex main.tex && pdflatex main.tex
```

`Package fontaxes Warning: Axis 'shape' not supported` is harmless and expected.

For troubleshooting, see [`../TROUBLESHOOTING.md`](../TROUBLESHOOTING.md).

## Technical Implementation

### Microtype Configuration

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

### Baseline Grid Mathematics

The body baseline is **16.32pt** (`\linespread{1.20}` scales the class's 13.6pt
baseline: 13.6 × 1.20 = 16.32pt). The **13.2pt spacing quantum** (`\gridunit`) is
a separate unit used for most vertical spacing — it is not the baseline pitch.
See `../docs/typography/BASELINE-GRID-DECISION.md` for the derivation.

```latex
Body baseline: 16.32pt  (document leading)
Spacing quantum (\gridunit): 13.2pt
Half quantum (\halfgridunit): 6.6pt
Quarter quantum (\quartergridunit): 3.3pt
```

### Appendix Counter Logic

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

### Performance Considerations

- **Compilation Speed**: Two-pass system requires `pdflatex` twice for appendix detection
- **Memory Usage**: Microtype and font loading increase memory requirements
- **Compatibility**: Tested with TeX Live 2022, 2025, 2026 (see [`../README.md`](../README.md) for details); MiKTeX not verified

---

For version history, see [`../CHANGELOG.md`](../CHANGELOG.md) and the `Version History` section of [`../README.md`](../README.md).
