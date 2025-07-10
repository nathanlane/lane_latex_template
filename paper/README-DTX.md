# LaTeX Documentation Format (.dtx)

The Lane LaTeX Template is now available in standard LaTeX documentation format (.dtx) for CTAN distribution.

## Files

- `lltpaperstyle.dtx` - The documented source file containing both documentation and package code
- `lltpaperstyle.ins` - The installation file to extract the .sty file

## Building from Source

### Extract the Package
```bash
latex lltpaperstyle.ins
```
This creates `lltpaperstyle.sty` from the .dtx file.

### Build the Documentation
```bash
pdflatex lltpaperstyle.dtx
makeindex -s gind.ist lltpaperstyle.idx
makeindex -s gglo.ist -o lltpaperstyle.gls lltpaperstyle.glo
pdflatex lltpaperstyle.dtx
pdflatex lltpaperstyle.dtx
```
This creates `lltpaperstyle.pdf` with full documentation.

## For CTAN Submission

The .dtx format is the standard for LaTeX package distribution on CTAN. Benefits include:

1. **Single Source**: Documentation and code in one file
2. **Version Control**: Built-in change tracking
3. **Code Documentation**: Automatic index of macros
4. **Professional Format**: Standard LaTeX documentation style
5. **License Integration**: LPPL license properly embedded

## Module Files

The modular .sty files in the `modules/` directory should also be converted to .dtx format for complete CTAN compliance:

- `lltcolors.dtx` - Color system documentation
- `lltdimensions.dtx` - Grid system documentation
- `lltfonts.dtx` - Font configuration documentation
- `lltheadings.dtx` - Heading styles documentation
- `lltlists.dtx` - List typography documentation

Each module would have its own .ins file for extraction.

## Installation for End Users

Users installing from CTAN would:

1. Download the package
2. Run `latex lltpaperstyle.ins` to extract files
3. Move .sty files to their local texmf tree
4. Run `texhash` or equivalent to update the file database

## Development Workflow

During development, you can continue editing the .sty file directly. When ready for release:

1. Update the .dtx file with new code
2. Update version number and change log
3. Test extraction with .ins file
4. Build and review documentation
5. Submit to CTAN

The .dtx format ensures professional distribution while maintaining the development flexibility you need.