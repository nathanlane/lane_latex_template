# Grid System Conversion Plan

**Goal:** Replace all hardcoded values with grid-relative measurements  
**Approach:** Systematic, tested conversion to maintain exact spacing while gaining flexibility

## Phase 1: Preparation

### 1.1 Verify Existing Grid Definitions
Currently defined in `modules/dimensions.sty`:
```latex
\newlength{\gridunit}          % 13.2pt
\newlength{\halfgridunit}      % 6.6pt  
\newlength{\quartergridunit}   % 3.3pt
\newlength{\doublegridunit}    % 26.4pt
\newlength{\triplegridunit}    % 39.6pt
```

### 1.2 Add Missing Grid Helpers
Need to add these common multiples:
```latex
% In dimensions.sty after existing definitions:
\newlength{\threequartergridunit}
\setlength{\threequartergridunit}{9.9pt}   % 0.75 × gridunit

\newlength{\onehalfgridunit}
\setlength{\onehalfgridunit}{19.8pt}       % 1.5 × gridunit

% For more complex calculations:
\newcommand{\gridmult}[1]{\dimexpr#1\gridunit\relax}
\newcommand{\gridmath}[1]{\the\dimexpr#1\gridunit\relax}
```

### 1.3 Create Test Document
```latex
% tests/grid-test.tex
\documentclass{article}
\usepackage{paper/paperstyle}
\usepackage{paper/gridoverlay}  % Visual grid

\begin{document}
\showgrid  % Display grid lines

\section{Grid Test}
This document tests grid alignment.

\begin{quote}
A test quotation to verify spacing.
\end{quote}

\subsection{Subsection Test}
Paragraph after subsection.

\begin{itemize}
\item First item
\item Second item
\end{itemize}

Text after list.

\end{document}
```

## Phase 2: Systematic Replacement Strategy

### 2.1 Order of Replacement (Safest to Most Complex)

1. **Simple \vspace and \hspace commands** (Low risk)
2. **Length settings in environments** (Medium risk)  
3. **Flexible spacing (plus/minus)** (Medium risk)
4. **Math spacing commands** (High risk)
5. **Complex calculations** (High risk)

### 2.2 Replacement Mappings

#### Direct Replacements:
```latex
% Before                        % After
3.3pt                          \quartergridunit
6.6pt                          \halfgridunit  
9.9pt                          \threequartergridunit
13.2pt                         \gridunit
19.8pt                         \onehalfgridunit
26.4pt                         \doublegridunit
39.6pt                         \triplegridunit
```

#### Calculated Replacements:
```latex
% Before                        % After
4.4pt                          \dimexpr\gridunit/3\relax
2.2pt                          \dimexpr\gridunit/6\relax
1.65pt                         \dimexpr\gridunit/8\relax
```

#### Flexible Spacing:
```latex
% Before                        % After
13.2pt plus 3.3pt minus 0pt    \gridunit plus \quartergridunit minus 0pt
6.6pt plus 1pt minus 1pt       \halfgridunit plus 1pt minus 1pt
```

## Phase 3: Section-by-Section Conversion

### 3.1 Start with dimensions.sty
- Already uses grid units correctly
- Add missing helper definitions
- Test compilation

### 3.2 Convert Simple Spacing (paperstyle.sty lines 640-670)
```latex
% Original:
\newcommand{\compactpar}{\vspace{-3.3pt}}
\newcommand{\loosepars}{\vspace{3.3pt}}

% Converted:
\newcommand{\compactpar}{\vspace{-\quartergridunit}}
\newcommand{\loosepars}{\vspace{\quartergridunit}}
```

### 3.3 Convert Quote Environments (lines 690-765)
```latex
% Original:
\vspace{13.2pt}
\setlength{\leftmargin}{26.4pt}
\setlength{\parsep}{6.6pt}

% Converted:
\vspace{\gridunit}
\setlength{\leftmargin}{\doublegridunit}
\setlength{\parsep}{\halfgridunit}
```

### 3.4 Convert Section Headings (headings.sty)
This is more complex due to flexible spacing:
```latex
% Original:
\titlespacing*{\section}{0pt}
  {39.6pt plus 6.6pt minus 6.6pt}
  {13.2pt plus 3.3pt minus 0pt}

% Converted:
\titlespacing*{\section}{0pt}
  {\triplegridunit plus \halfgridunit minus \halfgridunit}
  {\gridunit plus \quartergridunit minus 0pt}
```

## Phase 4: Testing Protocol

### 4.1 After Each Section Conversion:
1. Run `pdflatex tests/grid-test.tex`
2. Check for compilation errors
3. Visually verify spacing unchanged
4. Check grid alignment with overlay

### 4.2 Regression Tests:
```bash
# Create reference PDFs before changes
pdflatex tests/grid-test.tex
mv tests/grid-test.pdf tests/grid-test-reference.pdf

# After changes, compare visually
pdflatex tests/grid-test.tex
# Use diff-pdf or manual comparison
```

### 4.3 Edge Cases to Test:
- Nested environments
- Math displays
- Footnotes
- Floats near page breaks
- Multi-column layouts

## Phase 5: Special Considerations

### 5.1 Math Mode Spacing
Math mode uses different units (mu). Be careful with:
```latex
\thinmuskip=3mu    % Don't change these
\medmuskip=4mu     % They're not pt-based
\thickmuskip=5mu   
```

### 5.2 Font-Size Dependent Values
Some values scale with font size:
```latex
\fontsize{10.5}{13.2}  % Second parameter should use \gridunit
```

### 5.3 Flexible Spacing
Preserve the plus/minus flexibility:
```latex
% Good:
\vspace{\gridunit plus \quartergridunit minus 0pt}

% Bad (loses flexibility):
\vspace{\gridunit}
```

## Phase 6: Documentation Updates

### 6.1 Update Comments
```latex
% Before:
\vspace{13.2pt}  % 1 grid unit

% After:
\vspace{\gridunit}  % Base grid spacing
```

### 6.2 Create Migration Guide
Document what changed and why for future maintainers.

## Expected Timeline

- **Day 1:** Setup and simple replacements (lines 1-1000)
- **Day 2:** Environment conversions (lines 1000-2000)
- **Day 3:** Complex spacing and math (lines 2000-3000)
- **Day 4:** Module files and testing
- **Day 5:** Final testing and documentation

## Success Criteria

1. **No visual changes** - Output PDFs identical
2. **Compilation success** - No new errors
3. **Grid compliance** - All elements align to grid
4. **Flexibility gained** - Can change grid unit in one place
5. **Code clarity** - Semantic spacing values

## Rollback Plan

1. Git commit before each major section
2. Keep original files as `.bak`
3. Test incrementally
4. Document any issues found

This careful approach ensures we maintain the typography quality while gaining the flexibility and maintainability benefits of a proper grid system.