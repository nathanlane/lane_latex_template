# lanepaper Style Modules

This directory contains the modular components of the lanepaper LaTeX package. Each module provides specific functionality; standalone use is supported where documented dependencies are present.

As of this compatibility lane, the modules that declare standalone entry points are
supported as independent loads; each module in this list now states required local
dependencies and compatibility mode is validated through harness probes.

> **Note**: Modules are named `lnp` + role (e.g. `lnpcolors.sty`) and are loaded
> by package name, never by path. See
> [`docs/PACKAGE_NAMING_CONVENTION.md`](../../docs/PACKAGE_NAMING_CONVENTION.md).

## Module Overview
(The Lists module is now fully active as of v1.6-alpha.)

| Module | Purpose | Dependencies |
|--------|---------|--------------|
| `lnpfonts.sty` | Font configuration and math typography | fontenc, tgpagella, zi4, newpxmath |
| `lnpcolors.sty` | Professional color system | xcolor |
| `lnpdimensions.sty` | Page geometry and grid system | geometry |
| `lnpheadings.sty` | Section and heading formatting | titlesec, lnpcolors, lnpdimensions |
| `lnplists.sty` | List typography and environments | enumitem, etoolbox, graphicx, lnpcolors, lnpdimensions |
| `lnpmathgridlocked.sty` | Grid-aware display-math hooks | etoolbox, lnpdimensions |
| `lnpparagraphs.sty` | Paragraph and quote behavior | lettrine, etoolbox, lnpcolors, lnpdimensions |
| `lnpfontfallbacks.sty` | Font availability fallback diagnostics | amssymb |
| `lnpfontfeatures.sty` | Font feature helpers | textcomp |

## Quick Start

### Using All Modules (Recommended)

```latex
\usepackage{lanepaper}
```

### Using Individual Modules

```latex
% Just the color system
\RequirePackage{lnpcolors}
% Just the list styles
\RequirePackage{lnplists}

% Change first-level bullet to an en-dash
\setlist[itemize,1]{label=\dashmark}
```

## Module Documentation

- [Fonts Module](fonts.md) - Typography and font configuration (`lnpfonts.sty`)
- [Colors Module](colors.md) - Color definitions and usage (`lnpcolors.sty`)
- [Dimensions Module](dimensions.md) - Page layout and spacing (`lnpdimensions.sty`)
- [Headings Module](headings.md) - Section formatting (`lnpheadings.sty`)
- [Lists Module](lists.md) - List environments and styles (`lnplists.sty`)

## Design Principles

All modules follow these core principles:

1. **Spacing Quantum**: All vertical spacing is a multiple of the 13.2pt quantum (the body baseline measures 16.32pt)
2. **Professional Typography**: Based on Butterick, Brown, and Hochuli
3. **Modular Independence**: Validated standalone modules list explicit dependency requirements
4. **Graceful Degradation**: Fallbacks for missing dependencies
5. **Overleaf Compatibility**: Tested on cloud LaTeX platforms

## Version History

- v1.0-alpha (2025-07-03): Initial alpha modular release
