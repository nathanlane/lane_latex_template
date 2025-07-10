# paperstyle.sty Style Guide

**Typography Standards and Best Practices**

This document provides comprehensive guidelines for using the paperstyle.sty package effectively, ensuring consistent, professional academic typography.

## Typography Principles

### Core Philosophy

The style package implements three complementary typographic philosophies:

1. **Butterick's Practical Typography**: Reader-focused optimization
2. **Brown's Modular Scale**: Mathematical harmony through proportional relationships  
3. **Hochuli's Detail in Typography**: Micro-refinements for archival quality

### Golden Rules

**DO:**
- Trust the baseline grid system - all spacing derives from 12.65pt units
- Use semantic commands (`\emph{}`, `\bsc{}`, `\code{}`) over presentational formatting
- Maintain consistent labeling conventions (`app:`, `fig:`, `tab:`, `eq:`)
- Let the modular scale handle sizing relationships automatically

**DON'T:**
- Manually adjust spacing with `\vspace{}` or `\hspace{}`
- Use `\textbf{}` and `\textit{}` for emphasis - use `\emph{}` semantically
- Override color schemes - use provided semantic color commands
- Break the baseline grid with custom line spacing

## Text Typography Standards

### Title Capitalization Guidelines

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

### Emphasis and Formatting

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

### Title Page Components

The style provides systematic commands for professional title pages following economics paper conventions:

**Title Commands:**
```latex
% Standard title (18pt, perfect for most papers)
\articletitle{The East Asian Miracle:\\[0.3\baselineskip]
Industrial Policy and Economic Development}

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
- All vertical spacing uses baseline units (12.65pt) from Hochuli's grid
- Title sizes follow Brown's modular scale (18pt = 11pt × 1.333²)
- Author names use subtle size increase (12pt = 11pt × 1.09)
- Abstract width (85%) follows Butterick's optimal reading guidelines

### Academic Writing Quality Standards

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

### Small Caps Usage

```latex
% General purpose bold small caps
Organizations like \bsc{UNESCO} require careful formatting.

% Heading-style small caps with enhanced tracking
\headsc{Chapter Opening}

% Inline small caps for abbreviations
The \inlinebsc{PhD} program requires comprehensive study.

% Color-balanced small caps for headings
Section headings use \balancedbsc{Enhanced Formatting}.
```

### Professional Quotations

```latex
% CORRECT: LaTeX quotation marks
``Professional typography'' requires attention to detail.
Typography---like architecture---requires systematic thinking.

% INCORRECT: Straight quotes
"Professional typography" requires attention to detail.
Typography--like architecture--requires systematic thinking.
```

## Mathematical Typography Standards

### Semantic Mathematical Commands

```latex
% Number sets (use semantic commands)
\real^n, \complex, \integer, \rational, \natural, \field, \prob

% Mathematical operators
\norm{x}, \abs{z}, \inner{u}{v}, \set{A}

% Mathematical spaces (calligraphic)
\hilbert, \banach, \algebra, \topology, \measure

% Declared operators  
\tr(A), \rank(M), \Span{V}, \supp(f)
```

### Display Mathematics

```latex
% CORRECT: Systematic equation formatting
\begin{equation}
f(x) = \int_{-\infty}^{\infty} g(t) e^{-2\pi i x t} \, dt
\end{equation}

% Enhanced inline mathematics
The function $f \colon \real \to \complex$ satisfies $\norm{f}_2 < \infty$.
```

### Complex Mathematical Expressions

```latex
% Advanced mathematical typography
\begin{align}
\mathcal{L}[f](s) &= \int_0^{\infty} f(t) e^{-st} \, dt \\
\text{where } f &\in L^1(\real_+) \cap C(\real_+)
\end{align}
```

### Mathematical Writing Best Practices

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
Let $\mathbf{X} = (x_1, x_2, \ldots, x_n)^T \in \real^n$ denote the feature vector.
The objective function $f: \real^n \to \real$ is defined as $f(\mathbf{x}) = \|\mathbf{Ax} - \mathbf{b}\|_2^2$.

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

## Sophisticated List Typography

### Design Philosophy

The list system implements advanced typography principles from three masters:
- **Butterick**: Professional bullet symbols, optimal hanging indents, clean spacing
- **Brown**: Mathematical spacing relationships via modular scale, baseline grid alignment
- **Hochuli**: Micro-typographic refinements, sophisticated bullet hierarchy

### Standard List Environments

**Basic Itemize Lists:**
```latex
% Primary level: Subtle gray bullet with optimal hanging indent
\begin{itemize}
\item First major point with professional typography
\item Second major point maintains baseline grid alignment
  \begin{itemize}
  \item Nested point uses en-dash (Butterick's recommendation)
  \item Maintains progressive indentation for hierarchy
    \begin{itemize}
    \item Third level uses subtle gray diamond
    \item All spacing derived from 13.2pt baseline
    \end{itemize}
  \end{itemize}
\end{itemize}
```

**Enumerated Lists with Oldstyle Figures:**
```latex
% Hochuli's preference for oldstyle numerals in running text
\begin{enumerate}
\item First numbered item with oldstyle figures
\item Second item maintains consistent spacing
  \begin{enumerate}
  \item Lowercase letters with parenthesis
  \item Progressive indentation per level
    \begin{enumerate}
    \item Roman numerals for third level
    \item Maintains readability hierarchy
    \end{enumerate}
  \end{enumerate}
\end{enumerate}
```

**Description Lists with Small Caps:**
```latex
% Professional term definitions with hanging format
\begin{description}
\item[First Term] Definition with small caps label in paragraph color
\item[Second Term] Maintains consistent hanging indent of 1.8em
\item[Complex Term] Longer definitions wrap correctly with proper alignment
\end{description}
```

### Specialized List Environments

**Compact Lists for Dense Information:**
```latex
% Minimal spacing for references or brief points
\begin{compactitem}
\item Smith (2023): Original framework development
\item Jones (2024): Extension to complex domains
\item Brown (2024): Theoretical analysis
\end{compactitem}
```

**Display Lists for Key Findings:**
```latex
% Emphasized lists with generous spacing and bold text
\begin{displayitem}
\item Primary finding with significant impact
\item Secondary finding supporting the hypothesis
\item Tertiary finding suggesting future work
\end{displayitem}
```

**Academic Lists with En-Dash:**
```latex
% Following university style guide preferences
\begin{academicitem}
\item First scholarly point with en-dash marker
\item Second point maintaining academic tone
\item Third point with proper citation integration
\end{academicitem}
```

**Inline Lists for Brief Enumerations:**
```latex
% Butterick's recommendation for short lists within paragraphs
The analysis considers three factors: 
\begin{inlineitem}
\item data quality
\item model complexity  
\item computational resources
\end{inlineitem}
which collectively determine performance.
```

### Custom Bullet Commands

```latex
% Manual control for special cases
\begin{itemize}
\itembullet Traditional bullet point
\itemdash En-dash for variety
\itemdiamond Diamond for emphasis
\itemsquare Square for distinction
\itemtriangle Triangle for hierarchy
\end{itemize}
```

### List Typography Best Practices

**Spacing Principles:**
- All vertical spacing derives from 13.2pt baseline (11pt × 1.20)
- Item separation: 3.3pt (quarter baseline) for tight lists
- List margins: 6.6pt (half baseline) above/below
- Progressive indentation: 1.2em per nesting level

**Bullet Symbol Hierarchy:**
1. **Primary**: Subtle gray bullet (45% gray for refinement)
2. **Secondary**: Subtle gray en-dash (Butterick's preference)
3. **Tertiary**: Subtle gray diamond (geometric variety)

**Professional Guidelines:**
```latex
% CORRECT: Consistent punctuation and capitalization
\begin{itemize}
\item First item ends with appropriate punctuation;
\item Second item maintains parallel structure;
\item Final item completes the thought.
\end{itemize}

% INCORRECT: Inconsistent formatting
\begin{itemize}
\item first item lacks proper capitalization
\item Second item - inconsistent punctuation style;
\item Final item
\end{itemize}
```

**Nested List Considerations:**
```latex
% CORRECT: Clear hierarchy with appropriate markers
\begin{itemize}
\item Main point with comprehensive explanation
  \begin{itemize}
  \item Supporting detail with en-dash
  \item Additional evidence maintaining flow
  \end{itemize}
\item Second main point continuing discussion
\end{itemize}

% Avoid excessive nesting (maximum 3 levels recommended)
```

## Code Typography Standards

### Inline Code Context

```latex
% Basic inline code
The \code{numpy.array} function handles multidimensional data.

% Micro-spaced code (prevents text flow disruption)
Python's \inlinecode{DataFrame.groupby()} method provides aggregation.

% File paths with proper hyphenation
Data is stored in \filepath{/data/processed/analysis_results.csv}.

% Mathematical variables in code context
The variable \var{learning_rate} controls optimization speed.

% Mixed documentation style
\doccode{Function signature}{\textbackslash{}newcommand\{\textbackslash{}norm\}[1]}
```

### Code Block Standards

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

## Color System Guidelines

### Professional Color Usage

```latex
% Subtle emphasis (use sparingly)
This finding represents a \subtleemph{significant breakthrough} in the field.

% Important warnings or critical information
\importantnote{Warning}: This configuration may cause data loss.

% External references and URLs
See the documentation at \externalref{https://example.com/docs}.

% Internal document references (automatically applied)
Reference to \cref{fig:results} shows the relationship.
```

### Color Accessibility

All colors meet WCAG 2.1 AA accessibility standards:
- **Text contrast**: 4.5:1 minimum ratio
- **Link contrast**: Enhanced navy blue for external links
- **Hierarchy contrast**: Graduated grays for document structure

## Footnote Standards

### Professional Footnote Usage

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
- **Spacing**: 12.65pt above footnotes, 6.325pt between
- **Typography**: Oldstyle numerals, hanging indent, optimized word spacing

## Appendix Management

### Chicago-Compliant Appendices

```latex
% CORRECT: Modern documentAppendices environment
\begin{documentAppendices}
  \input{appendices/main_appendix.tex}
  \input{appendices/tech_appendix.tex}
  \input{appendices/data_appendix.tex}
\end{documentAppendices}

% LEGACY: Backward compatible (still supported)
\startappendices
  \input{appendices/main_appendix.tex}
\finishappendices
```

### Appendix Content Standards

```latex
% In appendix files, use \section{} for appendix titles
\section{Technical Implementation Details}
\label{app:technical}

% Subsections use standard formatting
\subsection{Algorithm Implementation}
\label{app:algorithm}

% Systematic cross-referencing
This appendix supplements the analysis in \cref{sec:methodology}.
```

### Professional Cross-Referencing and Citations

**Non-Breaking Spaces with References:**
```latex
% CORRECT: Use ~ (non-breaking space) before citations and references
A and B developed a new approach~\cite{paper-id}.
Figure~\ref{fig:results} shows the overall framework.
The analysis in Table~\ref{tab:data} confirms our hypothesis.

% INCORRECT: Regular spaces allow awkward line breaks
A and B developed a new approach \cite{paper-id}.
Figure \ref{fig:results} shows the framework.
```

**Capitalization in Cross-References:**
```latex
% CORRECT: Capitalize Figure and Table in references
In Figure~\ref{fig:analysis}, we observe clear patterns.
Table~\ref{tab:results} summarizes the key findings.

% INCORRECT: Lowercase figure and table
In figure~\ref{fig:analysis}, we observe patterns.
table~\ref{tab:results} summarizes the findings.
```

**Enhanced Cleveref Integration:**
```latex
% Enhanced cleveref automatically handles capitalization and formatting
\cref{app:main}              % → "appendix A" 
\Cref{app:main}              % → "Appendix A"
\cref{fig:app:diagram}       % → "figure A.1"
\cref{tab:app:results}       % → "table A.2"
\cref{eq:app:formula}        % → "equation A.3"
```

## Document Structure Standards

### Professional Labeling Convention

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

### Caption Placement and Formatting

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

### Data Presentation Standards

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

### Section Hierarchy

```latex
% CORRECT: Systematic hierarchy following modular scale
\section{Major Section}           % 18pt, Perfect Fourth ratio
\subsection{Important Subsection} % 14pt, scaled systematically  
\subsubsection{Detailed Topic}    % 12pt, proportional scaling
\paragraph{Key Point}             % 11.5pt, enhanced small caps
```

### Front Matter Standards

```latex
% Professional title formatting
\papertitle{Short, Impactful Title}          % Tracked uppercase
\mixedtitle{Longer Descriptive Title Text}   % Mixed case for readability

% Author and affiliation
\authorname{Author Name}                     % Tracked small caps
\affiliation{Institution and Department}     % Italic formatting

% Keywords with tracking
\keywords{keyword one, keyword two, keyword three}
```

### Bibliography Integration

```latex
% CORRECT: Chicago author-date style citations
This finding \cite{smith2023analysis} supports the hypothesis.
Recent studies \cite{jones2022methods, brown2023results} confirm...

% Multiple citations
\cite{author2020, author2021, author2022}
```

### Reproducibility and Open Science Standards

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

### Citation Quality and Academic Integrity

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

## Common Anti-Patterns

### Typography Mistakes to Avoid

```latex
% WRONG: Manual spacing
\section{Title}\vspace{10pt}
This breaks the baseline grid.

% WRONG: Presentational formatting  
This is \textbf{important} text.
Use \emph{semantic} formatting instead.

% WRONG: Manual colors
\textcolor{red}{Warning message}
Use \importantnote{Warning message} instead.

% WRONG: Inconsistent labels
\label{fig1}, \label{table-data}, \label{AppendixA}
Use \label{fig:analysis}, \label{tab:data}, \label{app:main}
```

### Mathematical Typography Errors

```latex
% WRONG: Inconsistent notation
R^n, C, Z (mixing fonts and notation)
Use \real^n, \complex, \integer consistently.

% WRONG: Poor spacing in math mode
$f(x)=\int_0^1g(t)dt$ (cramped spacing)
Use $f(x) = \int_0^1 g(t) \, dt$ (proper spacing).
```

## Quality Assurance Checklist

### Pre-Submission Review

**Typography Quality:**
- [ ] All emphasis uses semantic commands (`\emph{}`, not `\textit{}`)
- [ ] Small caps use provided commands (`\bsc{}`, `\headsc{}`)
- [ ] Mathematical notation uses semantic commands
- [ ] Code typography uses appropriate commands for context
- [ ] Colors use semantic commands, not manual `\textcolor{}`

**Title and Caption Standards:**
- [ ] All titles use headline-style capitalization (checked with title case tool)
- [ ] Section and subsection headings follow capitalization rules
- [ ] Figure captions placed below figures with proper capitalization
- [ ] Table captions placed above tables with proper capitalization
- [ ] Hyphenated words capitalized correctly (e.g., "Learning-Based")

**Labeling and Cross-Referencing:**
- [ ] All labels use systematic prefixes (`tbl:`, `fig:`, `sec:`, `subsec:`, `alg:`, etc.)
- [ ] Labels are descriptive, not generic (`fig:system-architecture`, not `fig1`)
- [ ] Non-breaking spaces used before all citations (`~\cite{}`)
- [ ] Non-breaking spaces used before all references (`Figure~\ref{}`, `Table~\ref{}`)
- [ ] "Figure" and "Table" capitalized in cross-references
- [ ] Cleveref commands used for enhanced formatting when appropriate

**Document Structure:**
- [ ] Section hierarchy follows modular scale automatically
- [ ] Cross-references use `\cref{}` for enhanced formatting
- [ ] Bibliography uses Chicago author-date style consistently
- [ ] Appendices use `documentAppendices` environment

**Academic Writing Quality:**
- [ ] One sentence per line for version control compatibility
- [ ] Precise, academic language (demonstrate, reveal, indicate vs. show, find, prove)
- [ ] Specific quantification with units and confidence intervals
- [ ] Mathematical equations integrated as part of sentence structure
- [ ] Variables clearly defined upon introduction
- [ ] Proper mathematical punctuation in multi-line equations

**Data Presentation Standards:**
- [ ] Tables use professional design (booktabs, no vertical lines)
- [ ] Figures meet publication quality (minimum 300 DPI, readable fonts)
- [ ] Statistical reporting includes complete information (M, SD, CI, effect sizes)
- [ ] Table notes provide essential context and sample sizes
- [ ] Consistent color schemes and formatting across all figures

**Reproducibility and Research Integrity:**
- [ ] Complete software version documentation
- [ ] Random seeds and experimental setup clearly described
- [ ] Code and data availability statements included
- [ ] Appropriate citation density with context integration
- [ ] Primary sources cited for original claims
- [ ] Citation formatting consistent throughout

**Technical Quality:**
- [ ] Document compiles without errors in two passes
- [ ] All cross-references resolve correctly
- [ ] Appendix numbering appears correctly (A, B, C... or single "Appendix")
- [ ] Bibliography appears and formats correctly
- [ ] PDF meets accessibility standards

### Final Production Check

```bash
# Clean compilation test
rm *.aux *.bbl *.bcf *.blg *.log *.out *.toc *.run.xml
pdflatex main.tex
biber main  
pdflatex main.tex
pdflatex main.tex

# Verify output
- Check appendix numbering and ToC formatting
- Verify all cross-references resolve
- Confirm bibliography formatting
- Test PDF accessibility features
```

---

This style guide ensures consistent, professional academic typography that meets the highest standards for scholarly publication. When in doubt, trust the systematic design of the style package rather than manual formatting overrides.