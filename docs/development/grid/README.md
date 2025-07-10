# Grid System Development Files

This directory contains comprehensive documentation and test files for the 13.2pt baseline grid system implementation.

## Core Documentation
- `GRID-CONSTRUCTION-PROCESS.md` - Philosophy, construction process, and implementation of the grid system
- `GRID-TECHNICAL-IMPLEMENTATION.md` - Technical details, code snippets, and LaTeX implementation guide
- `GRID-IMPROVEMENTS-SUMMARY.md` - Complete summary of all grid improvements and compliance metrics
- `GRID-AUDIT-REPORT.md` - Initial audit findings (75% compliance)
- `GRID-ALIGNED-TABLES.md` - Documentation for grid-aligned table system

## Test Files
- `grid-overlay-test.tex` - Demonstrates the visual grid overlay system
- `grid-heading-system.tex` - Tests heading alignment with optical adjustments
- `grid-image-system.tex` - Tests image height constraint system
- `grid-audit.tex` - Comprehensive grid audit with numbered lines
- `grid-test.tex` - Basic visual grid verification
- `grid-improvements.tex` - Proposed improvements documentation

## Supporting Files
- `grid-heading-alignment.sty` - Early heading alignment experiments

## Usage
These files are for development and testing only. The actual grid system is implemented in:
- `/paper/paperstyle.sty` - Main implementation
- `/paper/gridoverlay.sty` - Visual overlay for testing

To use the grid overlay in development:
```latex
\usepackage{paper/gridoverlay}
\showgrid  % Show grid
\hidegrid  % Hide grid
```