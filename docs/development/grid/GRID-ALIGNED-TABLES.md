# Grid-Aligned Table Row System

## Overview

The grid-aligned table row system ensures that tables maintain the document's baseline grid (13.2pt = 11pt × 1.20), improving vertical rhythm and professional appearance. This system is fully compatible with regression tables and all academic table formats.

## Key Benefits

1. **Visual Harmony**: Tables align with body text baselines
2. **Professional Appearance**: Consistent vertical rhythm throughout document
3. **Flexibility**: Multiple grid options for different table densities
4. **Compatibility**: Works seamlessly with booktabs and regression tables

## Usage

### Standard Grid Table (13.2pt rows)

```latex
\begin{gridtable}
  \caption{Your Caption}
  \centering
  \begin{tabular}{lrr}
    \toprule
    Column 1 & Column 2 & Column 3 \\
    \midrule
    Data & 123 & 456 \\
    More & 789 & 012 \\
    \bottomrule
  \end{tabular}
\end{gridtable}
```

### Regression Table (Optimized spacing)

```latex
\begin{regressiontable}
  \caption{Regression Results}
  \centering
  \begin{tabular}{lcc}
    \toprule
    & (1) & (2) \\
    & OLS & Fixed Effects \\
    \midrule
    Variable 1 & 0.234*** & 0.187** \\
               & (0.045)  & (0.052) \\
    \halfbaselinespace  % Add vertical space
    Variable 2 & -0.156** & -0.143* \\
               & (0.071)  & (0.089) \\
    \midrule
    Observations & 1,234 & 1,234 \\
    R-squared    & 0.45  & 0.52  \\
    \bottomrule
  \end{tabular}
\end{regressiontable}
```

### Compact Grid Table (9.9pt rows)

```latex
\begin{compactgridtable}
  \caption{Dense Information}
  \centering
  \begin{tabular}{lr}
    \toprule
    Item & Value \\
    \midrule
    Alpha & 1.23 \\
    Beta & 2.34 \\
    Gamma & 3.45 \\
    \bottomrule
  \end{tabular}
\end{compactgridtable}
```

### Spacious Grid Table (19.8pt rows)

```latex
\begin{spaciousgridtable}
  \caption{Important Results}
  \centering
  \begin{tabular}{lrr}
    \toprule
    Category & Result & Change \\
    \midrule
    Primary & 95.2 & +12.3 \\
    Secondary & 87.6 & +8.7 \\
    \bottomrule
  \end{tabular}
\end{spaciousgridtable}
```

## Manual Control Commands

For existing tables, use these commands within the table environment:

- `\standardgrid` - Set to 13.2pt rows (default)
- `\compactgrid` - Set to 9.9pt rows
- `\spaciousgrid` - Set to 19.8pt rows
- `\customgrid{1.5}` - Set to custom multiple (1.5 × 13.2pt)

## Vertical Spacing Commands

Add grid-aligned vertical space within tables:

- `\halfbaselinespace` - Add 6.6pt (0.5 baseline units)
- `\fullbaselinespace` - Add 13.2pt (1 baseline unit)
- `\baselinespace{1.5}` - Add custom multiple (1.5 × 13.2pt)

## Technical Details

### Grid Alignment Mathematics

- **Baseline Grid**: 13.2pt (11pt text × 1.20 leading)
- **Standard Rows**: `\arraystretch{1.2}` = exactly 13.2pt
- **Compact Rows**: `\arraystretch{0.9}` = 9.9pt (0.75 units)
- **Spacious Rows**: `\arraystretch{1.8}` = 19.8pt (1.5 units)
- **Regression Tables**: `\arraystretch{1.15}` = optimized for coefficients

### Implementation

The system modifies `\arraystretch` and `\extrarowheight` to achieve precise grid alignment:

```latex
% Standard configuration
\setlength{\extrarowheight}{2.2pt}  % Base adjustment
\renewcommand{\arraystretch}{1.2}   % Grid multiplier
```

### Compatibility

- **Booktabs**: Full compatibility with `\toprule`, `\midrule`, `\bottomrule`
- **Regression Tables**: Optimized spacing for coefficient/standard error pairs
- **Multi-column**: Works with `tabular`, `tabularx`, and `longtable`
- **Captions**: Maintains proper spacing above/below tables

## Best Practices

1. **Choose Appropriate Density**: 
   - Standard for most tables
   - Compact for reference tables or many rows
   - Spacious for emphasis or few rows
   - Regression for econometric results

2. **Use Vertical Spacing**: 
   - Add `\halfbaselinespace` between variable groups in regression tables
   - Use `\fullbaselinespace` for major sections within tables

3. **Maintain Consistency**: 
   - Use the same grid system for similar tables
   - Keep regression tables consistent throughout document

4. **Test Alignment**: 
   - Verify that table rows align with adjacent text
   - Check multi-page tables maintain grid alignment

## Example Output

Tables using this system will have rows that align precisely with the document's baseline grid, creating a harmonious vertical rhythm that enhances readability and professional appearance.