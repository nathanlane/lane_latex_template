# latexmk configuration for Lane LaTeX Template
# This ensures the llt* packages are found

# Add paper directories to TEXINPUTS
ensure_path('TEXINPUTS', './paper:./paper/modules:');