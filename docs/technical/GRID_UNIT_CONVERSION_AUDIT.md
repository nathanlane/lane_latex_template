# Grid Unit Conversion Audit for paperstyle.sty

This document identifies all hardcoded spacing values in `paperstyle.sty` that should be converted to grid units for consistency with the 13.2pt baseline grid system.

## Grid Unit Reference
- **1 grid unit** = 13.2pt (baseline)
- **0.5 grid units** = 6.6pt (half baseline)
- **0.25 grid units** = 3.3pt (quarter baseline)
- **0.75 grid units** = 9.9pt
- **1.5 grid units** = 19.8pt
- **2 grid units** = 26.4pt
- **3 grid units** = 39.6pt

## Identified Hardcoded Values by Section

### I. SMALL CAPS AND SPACING COMMANDS (Lines 121-260)

1. **Line 131**: `\fontsize{11pt}{13pt}` → Should use `\fontsize{11pt}{\gridunit}`
2. **Lines 172-183**: Em/en dash kerning values (0.08em, 0.16em) - These are relative, OK as-is
3. **Lines 188-196**: Degree/prime spacing (0.05em, 0.02em) - Relative units, OK
4. **Lines 234-242**: Quote kerning (0.02em, 0.03em) - Relative units, OK
5. **Lines 254-259**: Space commands (fractions of em) - Relative units, OK

### II. BLOCK QUOTATION SYSTEM (Lines 678-759)

6. **Line 686**: `\vspace{13.2pt}` → `\vspace{\gridunit}`
7. **Line 688**: `\setlength{\leftmargin}{26.4pt}` → `\setlength{\leftmargin}{2\gridunit}`
8. **Line 689**: `\setlength{\rightmargin}{26.4pt}` → `\setlength{\rightmargin}{2\gridunit}`
9. **Line 692**: `\setlength{\parsep}{6.6pt}` → `\setlength{\parsep}{0.5\gridunit}`
10. **Line 695**: `\fontsize{10.5}{13.2}` → `\fontsize{10.5}{\gridunit}`
11. **Line 701**: `\vspace{13.2pt}` → `\vspace{\gridunit}`
12. **Line 710**: `\vspace{13.2pt}` → `\vspace{\gridunit}`
13. **Line 712-713**: Same margin values as above (26.4pt → 2\gridunit)
14. **Line 716-718**: parsep and indent values
15. **Line 719**: `\fontsize{10.5}{13.2}` → `\fontsize{10.5}{\gridunit}`
16. **Line 725**: `\vspace{13.2pt}` → `\vspace{\gridunit}`
17. **Line 733**: `\vspace{6.6pt}` → `\vspace{0.5\gridunit}`
18. **Line 734**: `\fontsize{10}{13.2}` → `\fontsize{10}{\gridunit}`
19. **Line 742**: `\vspace{19.8pt}` → `\vspace{1.5\gridunit}`
20. **Line 744-745**: `\setlength{\leftmargin}{39.6pt}` → `\setlength{\leftmargin}{3\gridunit}`
21. **Line 748**: `\setlength{\parsep}{6.6pt}` → `\setlength{\parsep}{0.5\gridunit}`
22. **Line 756**: `\vspace{19.8pt}` → `\vspace{1.5\gridunit}`

### III. PARAGRAPH FORMATTING (Lines 635-660)

23. **Line 635**: `\vspace{-3.3pt}` → `\vspace{-0.25\gridunit}`
24. **Line 636**: `\vspace{3.3pt}` → `\vspace{0.25\gridunit}`
25. **Line 647**: `\vspace{13.2pt}` → `\vspace{\gridunit}`
26. **Line 652**: `\setlength{\parskip}{6.6pt}` → `\setlength{\parskip}{0.5\gridunit}`
27. **Line 656**: `\vspace{13.2pt}` → `\vspace{\gridunit}`

### IV. SECTION OPENING STYLES (Lines 828-886)

28. **Line 828**: `\fontsize{11}{13.2}` → `\fontsize{11}{\gridunit}`
29. **Line 848**: `\vspace{26.4pt}` → `\vspace{2\gridunit}`
30. **Line 861**: `\vspace{13.2pt plus 3.3pt minus 0pt}` → `\vspace{\gridunit plus 0.25\gridunit minus 0pt}`
31. **Line 869**: `\setlength{\baselineskip}{13.2pt}` → `\setlength{\baselineskip}{\gridunit}`
32. **Line 870**: `\fontsize{11}{13.2}` → `\fontsize{11}{\gridunit}`
33. **Line 873**: `\setlength{\parindent}{13.2pt}` → `\setlength{\parindent}{\gridunit}`
34. **Line 880**: `\fontsize{12}{13.2}` → `\fontsize{12}{\gridunit}`
35. **Line 884**: `\vspace{6.6pt}` → `\vspace{0.5\gridunit}`
36. **Lines 893, 899**: `3.3pt` and `4.4pt` spacing values

### V. MATHEMATICAL SPACING (Lines 946-956, 2396-2514)

37. **Line 946-949**: Display skip values already use grid units correctly
38. **Line 2396-2399**: Display skip values with flexibility
39. **Line 2402**: `\jot=6.6pt` → `\jot=0.5\gridunit`
40. **Line 2426**: `\addtolength{\jot}{3.3pt}` → `\addtolength{\jot}{0.25\gridunit}`
41. **Line 2436**: `\setlength{\jot}{6.6pt}` → `\setlength{\jot}{0.5\gridunit}`
42. **Line 2443**: `\vspace{6.6pt}` → `\vspace{0.5\gridunit}`
43. **Line 2447**: `\vspace{6.6pt}` → `\vspace{0.5\gridunit}`

### VI. CAPTION SYSTEM (Lines 1049-1064)

44. **Line 1049**: `aboveskip=13.2pt` → `aboveskip=\gridunit`
45. **Line 1050**: `belowskip=9.9pt` → `belowskip=0.75\gridunit`
46. **Line 1059**: `aboveskip=9.9pt` → `aboveskip=0.75\gridunit`
47. **Line 1060**: `belowskip=13.2pt` → `belowskip=\gridunit`

### VII. FLOAT SPACING (Lines 1100-1161)

48. **Line 1100**: `\setlength{\@fpsep}{13.2pt plus 1fil}` → `\setlength{\@fpsep}{\gridunit plus 1fil}`
49. **Line 1106-1110**: Float separation values already use grid units correctly
50. **Line 1145-1148**: `\vspace{0pt plus 13.2pt}` → `\vspace{0pt plus \gridunit}`
51. **Line 1157-1159**: `\vspace{13.2pt}` → `\vspace{\gridunit}`
52. **Line 1175-1180**: Grid space values already correct
53. **Line 1185**: `\vspace{13.2pt plus 3.3pt minus 3.3pt}` → Already uses grid values correctly

### VIII. TABLE NOTES (Lines 1278-1367)

54. **Line 1278**: `\par\vspace{3.3pt}` → `\par\vspace{0.25\gridunit}`
55. **Line 1281**: `\setlength{\parskip}{3.3pt}` → `\setlength{\parskip}{0.25\gridunit}`
56. **Line 1286**: `\par\vspace{6.6pt}` → `\par\vspace{0.5\gridunit}`
57. **Line 1316**: `\par\vspace{-3.3pt}` → `\par\vspace{-0.25\gridunit}`
58. **Line 1319**: `\setlength{\parskip}{3.3pt}` → `\setlength{\parskip}{0.25\gridunit}`
59. **Line 1324**: `\par\vspace{6.6pt}` → `\par\vspace{0.5\gridunit}`

### IX. TITLE PAGE SYSTEM (Lines 1410-1561)

Most values here already use \gridunit correctly through derived lengths!

60. **Line 1424**: `\fontsize{22pt}{26.4pt}` → `\fontsize{22pt}{2\gridunit}`
61. **Line 1432**: `\fontsize{22pt}{26.4pt}` → `\fontsize{22pt}{2\gridunit}`
62. **Line 1439**: `\fontsize{16pt}{19.8pt}` → `\fontsize{16pt}{1.5\gridunit}`
63. **Line 1445**: `\fontsize{16pt}{19.8pt}` → `\fontsize{16pt}{1.5\gridunit}`
64. **Line 1511**: `\setlength{\skip\footins}{13.2pt plus 2pt minus 1pt}` → `\setlength{\skip\footins}{\gridunit plus 2pt minus 1pt}`
65. **Line 1512**: `\setlength{\footnotesep}{9.9pt}` → `\setlength{\footnotesep}{0.75\gridunit}`
66. **Line 1531**: `\vspace*{13.2pt}` → `\vspace*{\gridunit}`
67. **Line 1539**: `\setlength{\skip\footins}{26.4pt plus 2pt minus 1pt}` → `\setlength{\skip\footins}{2\gridunit plus 2pt minus 1pt}`
68. **Line 1540**: `\setlength{\footnotesep}{3.3pt}` → `\setlength{\footnotesep}{0.25\gridunit}`
69. **Line 1559**: `\vspace*{13.2pt}` → `\vspace*{\gridunit}`

### X. FOOTNOTE SYSTEM (Lines 1603-1635)

70. **Line 1605**: `\setlength{\parindent}{7pt}` - Not a grid value, OK as is (special case)
71. **Line 1607**: `\makebox[7pt][l]` - Matches indent, OK
72. **Line 1623**: `\setlength{\skip\footins}{26.4pt plus 2pt minus 1pt}` → `\setlength{\skip\footins}{2\gridunit plus 2pt minus 1pt}`
73. **Line 1624**: `\setlength{\footnotesep}{3.3pt}` → `\setlength{\footnotesep}{0.25\gridunit}`
74. **Line 1634**: `\vspace*{13.2pt}` → `\vspace*{\gridunit}`

### XI. TABLE ROW HEIGHTS (Lines 2027-2114)

75. **Line 2027**: `\setlength{\extrarowheight}{2.2pt}` - This is a fine adjustment, not grid-based
76. **Line 2097**: `\noalign{\vspace{6.6pt}}` → `\noalign{\vspace{0.5\gridunit}}`
77. **Line 2102**: `\noalign{\vspace{13.2pt}}` → `\noalign{\vspace{\gridunit}}`

### XII. GRID-ALIGNED IMAGES (Lines 2140-2180)

78. **Line 2140**: `\setlength{\dimen0}{13.2pt}` → `\setlength{\dimen0}{\gridunit}`
79. **Line 2146**: `\ifdim\dimen1>6.6pt` → `\ifdim\dimen1>0.5\gridunit`
80. **Line 2147**: `\advance#2 by 13.2pt` → `\advance#2 by \gridunit`

### XIII. TABLE CAPTION SPACING (Lines 2364-2366)

81. **Line 2364**: `aboveskip=9.9pt` → `aboveskip=0.75\gridunit`
82. **Line 2365**: `belowskip=6.6pt` → `belowskip=0.5\gridunit`

### XIV. LANDSCAPE SPACING (Lines 2359-2360)

83. **Line 2359**: `\vspace{13.2pt}` → `\vspace{\gridunit}`

### XV. PARAGRAPH STYLE SETTINGS (Lines 2579-2585)

84. **Line 2579**: `\parindent=13.2pt` → `\parindent=\gridunit`

### XVI. PARAGRAPH COMMANDS (Lines 2906-2914)

85. **Line 2913**: `\parfillskip=0pt plus 0.75\textwidth` - This is a proportion, OK

### XVII. FOOTER CONFIGURATION (Lines 2957-2975)

86. **Line 2958**: `footskip=39.6pt` → `footskip=3\gridunit`
87. **Line 2966**: `\fontsize{10}{13.2}` → `\fontsize{10}{\gridunit}`
88. **Line 3007**: `\vspace{13.2pt}` → `\vspace{\gridunit}`

## Summary

The majority of spacing values in `paperstyle.sty` should be converted to use `\gridunit` or its multiples. This will ensure:

1. **Consistency**: All spacing derives from the same base unit
2. **Maintainability**: Changing the grid unit updates all spacing proportionally
3. **Clarity**: Code becomes self-documenting about grid relationships
4. **Flexibility**: Easy to adjust the entire grid system if needed

### Priority Conversions

High priority (affect major document structure):
- Block quotation margins and spacing
- Section opening spacing
- Mathematical display spacing
- Float separation values
- Title page spacing
- Footnote spacing

Medium priority (affect local elements):
- Caption spacing
- Table notes spacing
- Paragraph spacing commands

Low priority (fine adjustments):
- Small spacing adjustments (< 3.3pt)
- Relative em-based spacing
- Font-specific adjustments

### Implementation Notes

1. Define `\gridunit` early in the package (already done in dimensions module)
2. Use fractional commands like `0.5\gridunit` for clarity
3. Test thoroughly after conversion to ensure no visual changes
4. Consider defining semantic lengths for common fractions:
   ```latex
   \newlength{\halfgridunit}
   \setlength{\halfgridunit}{0.5\gridunit}
   \newlength{\quartergridunit}
   \setlength{\quartergridunit}{0.25\gridunit}
   ```