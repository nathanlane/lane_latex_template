# Spacing Quantum System Documentation

> **2026-08-12 correction.** This document previously claimed a "13.2pt
> baseline grid." That premise was false: `\linespread{1.20}` scales the
> class's 13.6pt baseline (the 11pt option sets 10.95pt on 13.6pt), so the
> document baseline measures **16.32pt**, not 13.2pt. 13.2pt survives as the
> **spacing quantum** — the unit vertical spaces are multiples of. The
> decision and its evidence: `BASELINE-GRID-DECISION.md` (same directory) and
> `notes/baseline-grid-decision-brief.md`.

## Foundation Principles

A consistent spacing quantum is the fundamental organizing principle of this
template's vertical rhythm. All vertical spacing in the template is a multiple
of a 13.2pt quantum.

### Core Specifications (measured)

- **Body Text:** 10.95pt TeX Gyre Pagella (the class's `11pt` option)
- **Leading:** 16.32pt (`\linespread{1.20}` × the class's 13.6pt baseline)
- **Spacing Quantum:** 13.2pt
- **Quantum Fractions:**
  - Full quantum: 13.2pt
  - Half quantum: 6.6pt
  - Quarter quantum: 3.3pt
  - 1.5 quanta: 19.8pt
  - 0.75 quanta: 9.9pt

### Why these proportions?

The quantum proportions are optimized for TeX Gyre Pagella's characteristics:
- Larger x-height than traditional fonts
- Wider character proportions
- Stronger stroke contrast
- Academic reading patterns (dense text, mathematical content)

Note the actual leading (≈149% of the 10.95pt body) is on the generous side
of the Bringhurst/Butterick bands — appropriate for Pagella's large x-height,
the ~77-character measure, and math-dense text (see the decision brief).

## Hierarchical Alignment System

All vertical spacing is defined in quantum multiples to maintain consistent rhythm:

### Section Headings
```
\section:       3 quanta before (39.6pt), 1.5 quanta after (19.8pt)
\subsection:    2 quanta before (26.4pt), 1 quantum after (13.2pt)
\subsubsection: 1.5 quanta before (19.8pt), 0.75 quanta after (9.9pt)
\paragraph:     1 quantum before (13.2pt), run-in with 0.75em separation
```

### Display Elements
```
Display math:    1.5 quanta before/after (19.8pt)
Figures/tables:  1 quantum text/float separation (13.2pt ±3.3pt)
Block quotes:    1 quantum before/after (13.2pt)
Lists:           0.5 quanta internal spacing (6.6pt)
```

### Micro-Typography
```
Footnotes:       2 quanta before the footnote rule (26.4pt);
                 between-note separation comes from the 12pt footnote
                 baseline (\footnotesep is an inert floor, not inter-note space)
Captions:        0.5 quanta above/below (6.6pt)
```

## Implementation Details

### LaTeX Configuration
```latex
% Foundation
\linespread{1.20}          % scales class baseline: 13.6pt × 1.20 = 16.32pt actual leading
\setlength{\parskip}{0pt}  % Zero paragraph spacing
\setlength{\parindent}{14pt} % ~1.2em for Pagella

% Section spacing (quantum multiples)
\titlespacing*{\section}{0pt}{39.6pt}{19.8pt}      % 3 quanta before, 1.5 after
\titlespacing*{\subsection}{0pt}{26.4pt}{13.2pt}   % 2 quanta before, 1 after
\titlespacing*{\subsubsection}{0pt}{19.8pt}{9.9pt} % 1.5 quanta before, 0.75 after
\titlespacing*{\paragraph}{0pt}{13.2pt}{0.75em}    % 1 quantum before, run-in separation
```

### Float Spacing
```latex
\setlength{\floatsep}{13.2pt plus 3.3pt minus 3.3pt}     % 1 quantum between floats (measured)
\setlength{\textfloatsep}{13.2pt plus 3.3pt minus 3.3pt} % 1 quantum text/float (measured)
\setlength{\intextsep}{9.9pt plus 1.65pt}                % 0.75 quanta wrapped floats (measured)
```

### Mathematical Content
```latex
\abovedisplayskip=19.8pt plus 3.3pt minus 3.3pt        % 1.5 quanta
\belowdisplayskip=19.8pt plus 3.3pt minus 3.3pt        % 1.5 quanta
\abovedisplayshortskip=13.2pt plus 3.3pt minus 3.3pt   % 1 quantum
\belowdisplayshortskip=13.2pt plus 3.3pt minus 3.3pt   % 1 quantum
```

## Verification Methods

### Visual Grid Test
Load the grid overlay to verify rhythm:
```latex
\usepackage[grid]{lltpaperstyle}
\showgrid
```
The overlay's base lines step at the true body baseline (16.32pt); the
13.2pt quantum lines are reference multiples for spacing checks.

### Measurement Checklist
1. Vertical spaces between elements are quantum multiples
2. Section headings use their declared quantum multiples
3. Mathematical displays use their declared skips
4. Lists preserve consistent internal spacing through nesting levels
5. Footnote blocks separate per the 12pt footnote baseline

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
1. **Visual Consistency:** Vertical spacing derives from a single quantum
2. **Reading Rhythm:** Consistent spacing reduces cognitive load
3. **Professional Appearance:** Matches high-end journal typography
4. **Maintainability:** All spacing measurements derive from a single quantum

## Troubleshooting

### Common Issues
1. **Text drift:** Ensure \parskip is 0pt
2. **Heading spacing:** Verify spacing uses exact quantum multiples
3. **Float disruption:** Use minimal plus/minus in spacing commands
4. **Math spacing:** Check display skip settings match quantum multiples

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

The baseline grid is not decorative—it's the foundation of professional typography. This implementation ensures every vertical measurement reinforces the reading rhythm established by the 13.2pt spacing quantum.