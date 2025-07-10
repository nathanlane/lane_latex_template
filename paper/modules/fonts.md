# Fonts Module Documentation

## Overview

The fonts module (`lltfonts.sty`) configures a professional three-font typography system optimized for academic documents.

## Font Stack

### Text Font: TeX Gyre Pagella
- Based on Palatino with enhanced features
- Superior small caps design
- Oldstyle figures for text
- Larger x-height requiring adjusted leading

### Mathematics Font: newpxmath
- Perfectly harmonized with Pagella
- Professional mathematical symbols
- Consistent weight and proportions

### Monospace Font: Inconsolata (zi4)
- Scaled to 95% for harmony with Pagella
- Excellent readability for code
- Professional appearance

## Features

### Small Caps
- True small caps (not scaled capitals)
- Optimized tracking for readability
- Available in regular and bold weights

### Oldstyle Figures
- Proportional oldstyle figures in text
- Lining figures in tables
- Proper figure selection by context

### Mathematical Symbols
Enhanced symbol sets from mathalfa:
- Calligraphic: boondoxo
- Blackboard bold: boondox
- Fraktur: boondox

## Usage

### Basic Usage
```latex
\RequirePackage{lltfonts}
```

### Font Commands

The module sets up fonts automatically. Available commands:

```latex
% Text emphasis (automatic)
\emph{emphasized text}
\textit{italic text}
\textbf{bold text}
\textsc{small caps}

% Math fonts (automatic)
$\mathcal{A}$  % Calligraphic
$\mathbb{R}$   % Blackboard bold
$\mathfrak{g}$ % Fraktur
```

### Monospace
```latex
\texttt{monospace text}
```

## Technical Details

### Font Encoding
- T1 encoding for proper hyphenation
- UTF-8 input encoding
- Full European language support

### Scaling
- Pagella: 100% (base size)
- Inconsolata: 95% (scaled for harmony)
- Math: Automatic sizing

### OpenType Features
- Ligatures: Enabled
- Kerning: Optimized
- Small caps: True small caps
- Figures: Oldstyle proportional

## Compatibility

- **pdfTeX**: Full support
- **XeTeX**: Limited (use fontspec instead)
- **LuaTeX**: Limited (use fontspec instead)
- **Overleaf**: Full compatibility

## Known Limitations

1. Font selection is fixed to Pagella
2. No sans-serif font defined
3. XeTeX/LuaTeX users should use fontspec

## Future Enhancements

- [ ] Font selection options
- [ ] Sans-serif font integration
- [ ] fontspec variant for modern engines
- [ ] Custom font scaling options