# Migration Guide: v1.2 to v1.5

This guide helps you migrate from paperstyle v1.2 to the new modular v1.5.

## Overview of Changes

### Major Changes
1. **Modular Architecture**: Package split into independent modules
2. **Appendix System**: Simplified for Overleaf compatibility
3. **Section Breaks**: Removed decorative asterisks
4. **Default Spacing**: More conservative section spacing

### Breaking Changes
- `\begin{documentAppendices}` → `\startappendices`
- `\end{documentAppendices}` → `\finishappendices`
- Asterisk section breaks removed from `\sectionbreak`

## Migration Steps

### 1. Update Package Version

No changes needed for basic usage:
```latex
\usepackage{lltpaperstyle}  % Works as before
```

### 2. Update Appendix Commands

**Old (v1.2):**
```latex
\begin{documentAppendices}
  \input{appendices/appendix1.tex}
  \input{appendices/appendix2.tex}
\end{documentAppendices}
```

**New (v1.5):**
```latex
\startappendices
  \input{appendices/appendix1.tex}
  \input{appendices/appendix2.tex}
\finishappendices
```

### 3. Section Break Updates

If you were using `\sectionbreak` for decorative breaks:

**Old behavior:**
```
        *    *    *
```

**New behavior:**
Clean vertical space only (2 grid units)

**Alternative:** If you need decorative breaks, define your own:
```latex
\newcommand{\decorativebreak}{%
  \par\vspace{\gridunit}%
  {\centering * \quad * \quad *\par}%
  \vspace{\gridunit}%
}
```

### 4. Section Spacing

Default section spacing is now "moderate" (1.5 units before) instead of "spacious" (2 units before).

To restore old spacing:
```latex
\usepackage{lltpaperstyle}
\spacioussections  % Restore v1.2 spacing
```

## New Features in v1.5

### 1. Modular Loading

Load only what you need:
```latex
% Just colors and lists
\RequirePackage{lltcolors}
\RequirePackage{lltlists}
```

### 2. Module Customization

Configure modules before loading:
```latex
% Custom configuration
\RequirePackage{lltdimensions}
\setlength{\gridunit}{12pt}  % Custom grid

\usepackage{lltpaperstyle}
```

### 3. Enhanced List Styles

New list environments:
```latex
\begin{readableitem}
  \item Enhanced spacing for clarity
\end{readableitem}

\begin{inlineitem}
  \item Brief
  \item Inline
  \item Lists
\end{inlineitem}
```

### 4. Improved Documentation

- Comprehensive module documentation
- API reference
- Individual module guides

## Compatibility Notes

### Overleaf
The v1.5 appendix system is fully Overleaf compatible. The previous `documentAppendices` environment could cause compilation errors on older TeX distributions.

### Package Conflicts
The modular system reduces conflicts by allowing selective loading:
```latex
% Avoid titlesec conflicts
\usepackage{mytitlesec}
% Load lltpaperstyle without headings module
\RequirePackage{lltfonts}
\RequirePackage{lltcolors}
\RequirePackage{lltdimensions}
\RequirePackage{lltlists}
```

## Quick Reference

| Feature | v1.2 | v1.5 |
|---------|------|------|
| Architecture | Monolithic | Modular |
| Appendices | `\begin{documentAppendices}` | `\startappendices` |
| Section breaks | Asterisks | Clean space |
| Default spacing | Spacious | Moderate |
| Module loading | N/A | Supported |
| Overleaf | Issues possible | Full support |

## Getting Help

1. Check module documentation in `paper/modules/`
2. See [MODULES.md](MODULES.md) for architecture overview
3. Consult [API_REFERENCE.md](API_REFERENCE.md) for commands
4. Review examples in main documentation

## Rollback Instructions

If you need to rollback to v1.2:
1. Replace the entire `paper/` directory with v1.2
2. Update appendix commands back to environment form
3. Remove any module-specific code