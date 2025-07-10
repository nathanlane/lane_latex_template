# Grid System Reference Guide

## Overview

The typography framework now uses a variable-based grid system for all spacing, replacing hardcoded point values. This ensures perfect baseline grid alignment and makes the system more maintainable.

## Core Grid Unit

- **Base unit:** `\gridunit` = 13.2pt
- **Derived from:** 11pt body text × 1.20 leading = 13.2pt
- **Optimized for:** TeX Gyre Pagella's x-height and character proportions

## Grid Unit Variables

All spacing in the framework is now expressed as multiples of `\gridunit`:

| Variable | Value | Common Usage |
|----------|-------|--------------|
| `0.125\gridunit` | 1.65pt | Fine adjustments |
| `0.25\gridunit` | 3.3pt | Quarter unit - footnote separation, minimal spacing |
| `0.5\gridunit` | 6.6pt | Half unit - paragraph spacing, between quotes |
| `0.75\gridunit` | 9.9pt | Three-quarter unit - caption spacing |
| `\gridunit` | 13.2pt | Full unit - standard spacing |
| `1.5\gridunit` | 19.8pt | One and half units - section spacing |
| `2\gridunit` | 26.4pt | Two units - major spacing, margins |
| `3\gridunit` | 39.6pt | Three units - dramatic spacing |

## Conversion Examples

### Before (Hardcoded):
```latex
\vspace{13.2pt}
\setlength{\parskip}{6.6pt}
\setlength{\leftmargin}{26.4pt}
```

### After (Variable-based):
```latex
\vspace{\gridunit}
\setlength{\parskip}{0.5\gridunit}
\setlength{\leftmargin}{2\gridunit}
```

## Common Grid Patterns

### Block Quotations
- Before quote: `\gridunit` (1 unit)
- After quote: `\gridunit` (1 unit)
- Left/right margins: `2\gridunit` (2 units)
- Between paragraphs: `0.5\gridunit` (0.5 units)

### Mathematical Displays
- Above display: `\gridunit` (1 unit)
- Below display: `\gridunit` (1 unit)
- Short skip: `0.5\gridunit` (0.5 units)
- Between equations: `0.5\gridunit` (0.5 units)

### Footnotes
- To footnote rule: `2\gridunit` (2 units)
- Rule to first note: `\gridunit` (1 unit)
- Between footnotes: `0.25\gridunit` (0.25 units)

### Floats
- Text to float: `\gridunit ± 0.25\gridunit`
- Between floats: `\gridunit ± 0.25\gridunit`
- Caption spacing: `0.75\gridunit` to `\gridunit`

## Flexible Spacing

Many spacing commands include flexibility for better page breaking:

```latex
\vspace{\gridunit plus 0.25\gridunit minus 0.25\gridunit}
```

This allows ±0.25 grid units of flexibility while maintaining the baseline grid.

## Benefits

1. **Consistency:** All spacing follows the same 13.2pt rhythm
2. **Maintainability:** Change grid unit in one place affects entire document
3. **Clarity:** Intent is clear from variable names
4. **Flexibility:** Easy to experiment with different grid sizes
5. **Precision:** Perfect baseline grid alignment throughout

## Implementation Notes

- Grid units are defined in `paper/modules/dimensions.sty`
- All conversions maintain backward compatibility
- Font sizes still use explicit point values (as required by `\fontsize`)
- Em-based spacing (0.08em, etc.) remains unchanged as it's relative to font size

## Future Enhancements

The grid system could be extended with:
- `\quartergridunit` for 3.3pt (already exists as `0.25\gridunit`)
- `\thirdgridunit` for 4.4pt spacing
- `\sixthgridunit` for 2.2pt fine adjustments

However, the current system with fractional multiples (0.25, 0.5, 0.75, 1.5, 2, 3) covers all necessary spacing requirements.