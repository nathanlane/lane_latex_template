# latexmk configuration for Lane LaTeX Template
# This ensures the lnp* packages are found

# Add the package directory to TEXINPUTS
ensure_path('TEXINPUTS', './lanepaper:./demo:');
ensure_path('BIBINPUTS', '.:./demo:');