# Bibliography Workflow Guide

This guide explains the bibliography system for the East Asian Miracle paper, which uses **biblatex** with **biber** backend and Chicago Manual of Style (17th edition) author-date format.

## Quick Start

1. **Add citations to your text:**
   ```latex
   Recent studies demonstrate this effect~\textcite{smith2023}.
   The phenomenon has been widely observed~\autocite{jones2022,brown2021}.
   ```

2. **Compile your document:**
   ```bash
   make pdf  # Full compilation with bibliography
   ```

## Citation Commands

### Primary Commands (biblatex)

| Command | Usage | Output Example |
|---------|-------|----------------|
| `\textcite{key}` | In-text citation | Smith (2023) argues... |
| `\autocite{key}` | Parenthetical citation | ...observed (Smith 2023) |
| `\textcite[45]{key}` | With page number | Smith (2023, 45) notes... |
| `\autocite[see][]{key}` | With prefix | (see Smith 2023) |
| `\citeauthor{key}` | Author only | Smith |
| `\citeyear{key}` | Year only | 2023 |

### Multiple Citations

```latex
\textcite{smith2023,jones2022,brown2021}
% Output: Smith (2023), Jones (2022), and Brown (2021)

\autocite{smith2023,jones2022,brown2021}
% Output: (Smith 2023; Jones 2022; Brown 2021)
```

## Bibliography Database Format

Edit `references.bib` following these examples:

### Journal Article
```bibtex
@article{smith2023,
  title = {Economic Development in East Asia},
  author = {Jane A. Smith and Robert B. Johnson},
  journal = {Journal of Asian Economics},
  volume = {45},
  number = {3},
  pages = {245--267},
  year = {2023},
  doi = {10.1016/j.asieco.2023.03.001}
}
```

### Book
```bibtex
@book{world1993,
  title = {The East Asian Miracle},
  author = {{World Bank}},
  publisher = {Oxford University Press},
  address = {New York},
  year = {1993},
  isbn = {978-0-19-520993-4}
}
```

### Working Paper/Preprint
```bibtex
@misc{kim2023,
  title = {Industrial Policy and Growth},
  author = {Thomas Kim and Lisa Park},
  year = {2023},
  eprint = {2301.12345},
  eprinttype = {arxiv},
  eprintclass = {econ.GN}
}
```

### Online Resource
```bibtex
@online{imf2023,
  title = {Asian Economic Outlook},
  author = {{International Monetary Fund}},
  year = {2023},
  url = {https://www.imf.org/asia-outlook},
  urldate = {2023-12-15}
}
```

## Best Practices

1. **Use semantic field names:**
   - `author` not `authors`
   - `title` not `Title`
   - `pages` with en-dash: `245--267`

2. **Include DOIs when available:**
   - Use bare DOI: `doi = {10.1016/j.asieco.2023.03.001}`
   - Do NOT include `https://doi.org/`

3. **Corporate authors:**
   - Use double braces: `author = {{World Bank}}`

4. **Page ranges:**
   - Use double dash: `pages = {45--48}`

5. **Annotations (optional):**
   ```bibtex
   annotation = {Seminal work on East Asian development.}
   ```

## Compilation Workflow

### Using Make (Recommended)
```bash
make pdf        # Full compilation with bibliography
make quick      # Quick compilation (no bibliography update)
make clean      # Remove auxiliary files
make validate   # Check style compliance
```

### Manual Compilation
```bash
pdflatex main
biber main
pdflatex main
pdflatex main
```

## Troubleshooting

### Bibliography not updating?
1. Run `make clean` to remove cached files
2. Ensure entries in `references.bib` are properly formatted
3. Check for biber errors: look in `main.blg`

### Citation undefined?
1. Check the citation key matches exactly
2. Ensure the entry is in `references.bib`
3. Run full compilation with `make pdf`

### Switching from natbib?
The project supports legacy natbib with `preamble-natbib.tex`. To use biblatex (recommended):
1. Ensure `main.tex` includes `paper/preamble.tex`
2. Replace `\citet` → `\textcite`
3. Replace `\citep` → `\autocite`

## Style Customization

The bibliography style is configured in `paper/preamble.tex`:
```latex
\usepackage[
  backend=biber,
  style=chicago-authordate,
  natbib=true,
  hyperref=true,
  sorting=nyt
]{biblatex}
```

All bibliography entries are formatted according to Chicago Manual of Style guidelines with enhanced digital features (clickable DOIs, proper URL formatting).