# Baseline Grid System Documentation

## Foundation Principles

The baseline grid is the fundamental organizing principle of professional typography. This template implements a rigorous 13.2pt baseline grid system optimized for academic journal articles.

### Core Specifications

- **Body Text:** 11pt TeX Gyre Pagella
- **Leading:** 120% (11pt × 1.20 = 13.2pt)
- **Grid Unit:** 13.2pt
- **Grid Fractions:** 
  - Full unit: 13.2pt
  - Half unit: 6.6pt
  - Quarter unit: 3.3pt
  - 1.5 units: 19.8pt
  - 0.75 units: 9.9pt

### Why 120% Leading?

The 120% leading ratio (13.2pt for 11pt text) is specifically optimized for TeX Gyre Pagella's characteristics:
- Larger x-height than traditional fonts
- Wider character proportions
- Stronger stroke contrast
- Academic reading patterns (dense text, mathematical content)

## Hierarchical Alignment System

All vertical spacing is defined in grid units to maintain perfect alignment:

### Section Headings
```
\section:       3 units before (39.6pt), 1.5 units after (19.8pt)
\subsection:    2 units before (26.4pt), 1 unit after (13.2pt)
\subsubsection: 1.5 units before (19.8pt), 0.75 units after (9.9pt)
\paragraph:     1 unit before (13.2pt), 0.5 units after (6.6pt)
```

### Display Elements
```
Display math:    1 unit before/after (13.2pt)
Figures/tables:  1.5 units before/after (19.8pt)
Block quotes:    1 unit before/after (13.2pt)
Lists:           0.5 unit internal spacing (6.6pt)
```

### Micro-Typography
```
Footnotes:       1 unit above first footnote (13.2pt)
                 0.5 unit between footnotes (6.6pt)
Captions:        0.5 unit above/below (6.6pt)
```

## Implementation Details

### LaTeX Configuration
```latex
% Foundation
\linespread{1.20}          % 11pt × 1.20 = 13.2pt grid
\setlength{\parskip}{0pt}  % Zero paragraph spacing
\setlength{\parindent}{14pt} % ~1.2em for Pagella

% Section spacing (grid-aligned)
\titlespacing*{\section}{0pt}{39.6pt}{19.8pt}      % 3 units before, 1.5 after
\titlespacing*{\subsection}{0pt}{26.4pt}{13.2pt}   % 2 units before, 1 after
\titlespacing*{\subsubsection}{0pt}{19.8pt}{9.9pt} % 1.5 units before, 0.75 after
\titlespacing*{\paragraph}{0pt}{13.2pt}{6.6pt}     % 1 unit before, 0.5 after
```

### Float Spacing
```latex
\setlength{\floatsep}{19.8pt plus 2pt minus 2pt}      % 1.5 units between floats
\setlength{\textfloatsep}{19.8pt plus 2pt minus 2pt}  % 1.5 units text/float
\setlength{\intextsep}{13.2pt plus 1pt minus 1pt}     % 1 unit wrapped floats
```

### Mathematical Content
```latex
\setlength{\abovedisplayskip}{13.2pt}      % 1 unit exactly
\setlength{\belowdisplayskip}{13.2pt}      % 1 unit exactly
\setlength{\abovedisplayshortskip}{6.6pt}  % 0.5 unit exactly
\setlength{\belowdisplayshortskip}{6.6pt}  % 0.5 unit exactly
```

## Verification Methods

### Visual Grid Test
Use the included `grid-test.tex` to verify alignment:
```bash
pdflatex grid-test.tex
```
This overlays gray grid lines at 13.2pt intervals for visual verification.

### Measurement Checklist
1. Body text baselines align to every grid line
2. Section headings land on grid lines after their spacing
3. Mathematical displays maintain grid registration
4. Lists preserve grid alignment through all nesting levels
5. Footnotes begin and end on grid lines

## Design Rationale

### Academic Journal Standards
This grid system follows conventions from leading economics journals (AER, QJE):
- Dense information presentation
- Clear hierarchical structure
- Mathematical content integration
- Extended reading sessions

### Typography Excellence
The system implements principles from:
- **Bringhurst:** Classical proportions and rhythm
- **Butterick:** Practical readability optimization
- **Hochuli:** Micro-typographic perfection
- **Brown:** Mathematical harmony through modular relationships

### Key Benefits
1. **Visual Consistency:** Every element aligns to the invisible grid
2. **Reading Rhythm:** Consistent spacing reduces cognitive load
3. **Professional Appearance:** Matches high-end journal typography
4. **Maintainability:** All measurements derive from single grid unit

## Troubleshooting

### Common Issues
1. **Text drift:** Ensure \parskip is 0pt
2. **Heading misalignment:** Verify spacing uses exact grid multiples
3. **Float disruption:** Use minimal plus/minus in spacing commands
4. **Math spacing:** Check display skip settings match grid units

### Testing Protocol
1. Compile with grid overlay
2. Check each section type for alignment
3. Verify lists at all nesting levels
4. Test with accented characters and math
5. Validate footnote positioning

## Future Optimizations

Potential enhancements maintaining grid integrity:
- Optical margin alignment for punctuation
- Baseline-shift compensation for superscripts
- Grid-aware widow/orphan control
- Dynamic spacing for optimal page breaks

---

The baseline grid is not decorative—it's the foundation of professional typography. This implementation ensures every vertical measurement reinforces the reading rhythm established by the 13.2pt grid.