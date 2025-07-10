# Custom Commands Reference

This document provides a comprehensive reference for all custom commands defined in `paperstyle.sty` and the template system.

## Typography Commands

### Emphasis and Small Caps

#### `\elegantsc{text}`
Enhanced small caps with superior visibility and tracking.
- **Tracking:** 80 units (8% letter spacing)
- **Usage:** General small caps text with optimal readability
- **Example:** `\elegantsc{introduction}` → INTRODUCTION (with tracking)

#### `\elegantscbold{text}`
Bold small caps with generous tracking for emphasis.
- **Tracking:** 100 units (10% letter spacing)
- **Weight:** Bold with tracking compensation
- **Example:** `\elegantscbold{key finding}` → KEY FINDING (bold with tracking)

#### `\titlesc{text}`
Title page small caps with maximum elegance.
- **Size:** 11pt/13pt
- **Tracking:** 120 units (12% letter spacing)
- **Usage:** Title page elements requiring exceptional visibility
- **Example:** `\titlesc{abstract}` → ABSTRACT (larger with extensive tracking)

#### `\bsc{text}`
Standard bold small caps command.
- **Weight:** Bold
- **Usage:** Inline emphasis, shorter text
- **Example:** `\bsc{note}` → NOTE (bold small caps)

#### `\subtleemph{text}`
Subtle blue emphasis for special cases.
- **Color:** Deep emphasis blue (RGB 0,34,68)
- **Usage:** Rare, special emphasis only
- **Example:** `\subtleemph{critical}` → critical (in blue)

### Code and Monospace

#### `\code{text}`
Weight-compensated inline code.
- **Font:** Inconsolata scaled to 98%
- **Color:** Code color (RGB 25,25,25)
- **Usage:** Inline code snippets
- **Example:** `\code{git commit}` → `git commit`

#### `\inlinecode{text}`
Inline code with micro-spacing.
- **Spacing:** 0.05em padding on each side
- **Usage:** Code within flowing text
- **Example:** `Use \inlinecode{npm start} to begin`

#### `\filepath{path}`
File paths with proper hyphenation.
- **Font:** Monospace with hyphenation enabled
- **Usage:** File and directory paths
- **Example:** `\filepath{/Users/name/documents/file.tex}`

#### `\var{name}`
Variable names in monospace.
- **Font:** Monospace in code color
- **Usage:** Mathematical or programming variables
- **Example:** `\var{x}` → x (monospace)

## Title Page Commands

### Title Formatting

#### `\articletitle{title}`
Dynamic article title with elegant formatting.
- **Size:** 22pt/26.4pt
- **Weight:** Bold
- **Color:** Softened navy (RGB 25,50,80)
- **Tracking:** 20 units (2% letter spacing)
- **Spacing after:** 2 grid units (26.4pt)
- **Example:** `\articletitle{The East Asian Miracle}`

#### `\articletitlefootnote{title}{footnote}`
Article title with acknowledgment footnote.
- **Same styling as `\articletitle`**
- **Footnote:** Uses symbolic marks (*, †, ‡)
- **Example:** `\articletitlefootnote{Title}{We thank...}`

#### `\articletitlecompact{title}`
Compact title for papers with many authors.
- **Size:** 16pt/19.8pt
- **Weight:** Bold
- **Spacing after:** 1.5 grid units (19.8pt)
- **Usage:** When author list is extensive

### Author and Metadata

#### `\articleauthors{authors}`
Author names with systematic spacing.
- **Size:** 13pt/16pt
- **Color:** Near-black
- **Spacing between:** Use `\authorspace`
- **Example:** `\articleauthors{Jane Doe\authorspace John Smith}`

#### `\authorspace`
Systematic spacing between author names.
- **Width:** 4.5% of text width
- **Usage:** Between author names
- **Replaces:** Manual `\quad\quad`

#### `\elegantauthor{name}`
Individual author name with enhanced small caps.
- **Size:** 12pt/14pt
- **Style:** Small caps
- **Tracking:** 100 units (10% letter spacing)
- **Usage:** Within `\articleauthors` if desired

#### `\articledate{date}`
Date line with enhanced visibility.
- **Format:** "This version: [date]"
- **Label color:** Medium charcoal (25% gray)
- **Date color:** Near-black
- **Spacing after:** 2 grid units
- **Example:** `\articledate{\today}`

### Abstract and Keywords

#### `\begin{articleabstract}...\end{articleabstract}`
Professional abstract environment.
- **Width:** 0.618 × text width (golden ratio)
- **Label:** "ABSTRACT" in enhanced small caps
- **Font size:** 10pt (small)
- **Spacing:** 0.5 grid units internal

#### `\articlekeywords{keywords}`
Keywords with refined formatting.
- **Label:** "Keywords:" in small caps
- **Spacing:** 0.5em after label
- **Width:** 72% of text width
- **Example:** `\articlekeywords{economics, development, Asia}`

#### `\articlejel{codes}`
JEL classification codes.
- **Label:** "JEL Classification:" in small caps
- **Format:** Same as keywords
- **Example:** `\articlejel{O10, O14, O53}`

### Footnote Control

#### `\titlefootnotesetup`
Switch to symbolic footnotes for title page.
- **Marks:** *, †, ‡, §, ¶, ‖
- **Usage:** Before title page content

#### `\titlefootnotereset`
Reset to numeric footnotes.
- **Usage:** After title page
- **Resets:** Counter and format

## Mathematical Commands

### Number Sets

#### `\real`
Real numbers ℝ
- **Font:** Blackboard bold
- **Example:** `$x \in \real$`

#### `\complex`
Complex numbers ℂ

#### `\integer`
Integer numbers ℤ

#### `\rational`
Rational numbers ℚ

#### `\natural`
Natural numbers ℕ

#### `\field`
Generic field 𝔽

#### `\prob`
Probability measure ℙ

### Operators and Norms

#### `\norm{x}`
Norm notation
- **Output:** ‖x‖
- **Example:** `$\norm{x} \leq 1$`

#### `\abs{x}`
Absolute value
- **Output:** |x|
- **Example:** `$\abs{x - y} < \epsilon$`

#### `\inner{x}{y}`
Inner product
- **Output:** ⟨x, y⟩
- **Example:** `$\inner{u}{v} = 0$`

#### `\set{elements}`
Set notation
- **Output:** {elements}
- **Example:** `$\set{1, 2, 3}$`

### Spaces

#### `\hilbert`
Hilbert space ℋ

#### `\banach`
Banach space ℬ

#### `\algebra`
Algebra 𝒜

#### `\topology`
Topology 𝒯

#### `\measure`
Measure space ℳ

## Grid System Commands

### Table Environments

#### `\begin{gridtable}[placement]...\end{gridtable}`
Standard grid-aligned table.
- **Row height:** 13.2pt (1 grid unit)
- **Usage:** Normal data tables

#### `\begin{regressiontable}[placement]...\end{regressiontable}`
Regression table with spacious rows.
- **Row height:** 19.8pt (1.5 grid units)
- **Usage:** Statistical results

#### `\begin{compacttable}[placement]...\end{compacttable}`
Compact table for dense data.
- **Row height:** 9.9pt (0.75 grid units)
- **Font:** Small size

### Grid Spacing

#### `\halfbaselinespace`
Insert half baseline space in tables.
- **Height:** 6.6pt (0.5 grid units)
- **Usage:** `\halfbaselinespace` between table sections

#### `\fullbaselinespace`
Insert full baseline space.
- **Height:** 13.2pt (1 grid unit)

#### `\baselinespace{multiplier}`
Custom baseline space.
- **Example:** `\baselinespace{1.5}` → 19.8pt

### Image Commands

#### `\gridincludegraphics[options]{file}`
Include image with grid-aligned height.
- **Height:** Automatically rounded to nearest grid multiple
- **Usage:** Maintains vertical rhythm

#### `\begin{gridfigure}[placement]...\end{gridfigure}`
Grid-aware figure environment.
- **Centering:** Automatic
- **Usage:** Wrapper for grid-aligned figures

## List Commands

### Specialized Lists

#### `\begin{compactitem}...\end{compactitem}`
Compact itemize with no inter-item spacing.
- **Spacing:** No space between items
- **Bullet:** Professional gray

#### `\begin{displayitem}...\end{displayitem}`
Display list for key findings.
- **Spacing:** Generous (1 baseline unit between)
- **Style:** Bold items
- **Bullet:** Full black

#### `\begin{academicitem}...\end{academicitem}`
Academic style with en-dash.
- **Bullet:** En-dash (–)
- **Usage:** Formal academic lists

#### `\begin{inlineitem}...\end{inlineitem}`
Inline enumeration.
- **Format:** (a); (b); (c)
- **Separator:** Semicolon
- **Usage:** Brief inline lists

## Special Characters

### Dashes

#### `\dashmark`
En-dash for lists and ranges
- **Output:** –
- **Note:** Replaces deprecated `\endashmark`

#### `\emdash`
Em-dash with proper spacing
- **Output:** —
- **Spacing:** Optimized for Pagella

### Typography Symbols

#### `\degrees`
Degree symbol
- **Output:** °
- **Example:** `45\degrees`

#### `\trademark`
Trademark symbol
- **Output:** ™

#### `\copyright`
Copyright symbol
- **Output:** ©

## Utility Commands

### Spacing

#### `\titlespacemajor`
Major title page spacing
- **Height:** 26.4pt (2 grid units)

#### `\titlespaceminor`
Minor title page spacing
- **Height:** 19.8pt (1.5 grid units)

#### `\titlespaceinter`
Inter-element spacing
- **Height:** 13.2pt (1 grid unit)

### Development Tools

#### `\showgrid`
Display baseline grid overlay
- **Usage:** Development only
- **Requires:** `\usepackage{paper/gridoverlay}`

#### `\hidegrid`
Hide grid overlay
- **Usage:** Before final compilation

---

*This reference covers all major custom commands. For package-specific commands (booktabs, biblatex, etc.), consult their respective documentation.*