# Makefile for East Asian Miracle Paper
# Production-grade LaTeX compilation workflow

# Variables
MAIN = main
LATEX = pdflatex
BIBER = biber
LATEXFLAGS = -interaction=nonstopmode -halt-on-error
PYTHON = python3
BLACK = black

# Set TEXINPUTS to find new package names
export TEXINPUTS := ./paper:./paper/modules:$(TEXINPUTS)

# Directories
PAPER_DIR = paper
APPENDICES_DIR = appendices
FIGURES_DIR = figures
SRC_DIR = src
DATA_DIR = data

# Source files
TEX_SOURCES = $(MAIN).tex $(wildcard $(PAPER_DIR)/*.tex) $(wildcard $(APPENDICES_DIR)/*.tex)
BIB_SOURCES = references.bib
STYLE_SOURCES = $(PAPER_DIR)/lltpaperstyle.sty $(PAPER_DIR)/preamble.tex

# Python sources
PY_SOURCES = $(wildcard $(SRC_DIR)/py/*.py)

# Default target
.PHONY: all
all: pdf

# Main PDF compilation with full bibliography processing
.PHONY: pdf
pdf: $(MAIN).pdf

$(MAIN).pdf: $(TEX_SOURCES) $(BIB_SOURCES) $(STYLE_SOURCES)
	@echo "==> Initial LaTeX compilation..."
	$(LATEX) $(LATEXFLAGS) $(MAIN)
	@echo "==> Running Biber for bibliography..."
	$(BIBER) $(MAIN)
	@echo "==> Second LaTeX compilation..."
	$(LATEX) $(LATEXFLAGS) $(MAIN)
	@echo "==> Final LaTeX compilation..."
	$(LATEX) $(LATEXFLAGS) $(MAIN)
	@echo "==> PDF compilation complete: $(MAIN).pdf"

# Quick compilation (no bibliography)
.PHONY: quick
quick:
	@echo "==> Quick LaTeX compilation (no bibliography)..."
	@if $(LATEX) $(LATEXFLAGS) $(MAIN); then \
		echo "==> Quick compilation complete: $(MAIN).pdf"; \
	else \
		echo "==> ERROR: Compilation failed. Check syntax and missing packages."; \
		exit 1; \
	fi

# Clean auxiliary files but keep PDF
.PHONY: clean
clean:
	@echo "==> Cleaning auxiliary files..."
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).bcf $(MAIN).blg
	rm -f $(MAIN).log $(MAIN).out $(MAIN).run.xml $(MAIN).toc
	rm -f $(MAIN).nav $(MAIN).snm $(MAIN).vrb
	rm -f $(PAPER_DIR)/*.aux $(APPENDICES_DIR)/*.aux
	rm -f texput.log
	@echo "==> Clean complete (PDF preserved)"

# Deep clean including PDF
.PHONY: distclean
distclean: clean
	@echo "==> Removing PDF output..."
	rm -f $(MAIN).pdf
	@echo "==> Deep clean complete"

# Watch mode for development (requires inotify-tools or fswatch)
.PHONY: watch
watch:
	@echo "==> Starting watch mode (Ctrl+C to stop)..."
	@echo "==> Watching: $(TEX_SOURCES) $(STYLE_SOURCES)"
	@if command -v fswatch >/dev/null 2>&1; then \
		fswatch -o $(TEX_SOURCES) $(STYLE_SOURCES) | while read; do \
			echo "==> File changed, recompiling..."; \
			$(MAKE) quick; \
		done; \
	elif command -v inotifywait >/dev/null 2>&1; then \
		while inotifywait -r -e modify $(PAPER_DIR) $(APPENDICES_DIR) >/dev/null 2>&1; do \
			echo "==> File changed, recompiling..."; \
			$(MAKE) quick; \
		done; \
	else \
		echo "==> ERROR: Please install fswatch (macOS) or inotify-tools (Linux)"; \
		echo "==> macOS: brew install fswatch"; \
		echo "==> Linux: sudo apt-get install inotify-tools"; \
		exit 1; \
	fi

# Validate template integrity
.PHONY: validate
validate:
	@echo "==> Validating template integrity..."
	@if ! test -f $(PAPER_DIR)/paperstyle.sty; then \
		echo "==> ERROR: paperstyle.sty not found"; exit 1; \
	fi
	@if ! test -f references.bib; then \
		echo "==> ERROR: references.bib not found"; exit 1; \
	fi
	@echo "==> Checking for required LaTeX packages..."
	@if ! kpsewhich biblatex.sty >/dev/null 2>&1; then \
		echo "==> WARNING: biblatex package not found"; \
	fi
	@if ! kpsewhich microtype.sty >/dev/null 2>&1; then \
		echo "==> WARNING: microtype package not found"; \
	fi
	@echo "==> Template validation complete"

# Development workflow
.PHONY: dev
dev: clean validate quick
	@echo "==> Development build complete"

# Format Python code with black
.PHONY: format
format:
	@if [ -n "$(PY_SOURCES)" ]; then \
		echo "==> Formatting Python code with black..."; \
		$(BLACK) $(SRC_DIR)/py/; \
	else \
		echo "==> No Python files to format"; \
	fi

# Validate LaTeX style compliance (alternative target)
.PHONY: style-check
style-check:
	@echo "==> Validating LaTeX style compliance..."
	@$(SRC_DIR)/sh/validate_latex_style.sh

# Generate all figures from Python scripts
.PHONY: figures
figures:
	@echo "==> Generating figures..."
	@for script in $(PY_SOURCES); do \
		echo "Running $$script..."; \
		$(PYTHON) $$script; \
	done

# Old watch target removed - using enhanced version above

# Check for required tools and packages
.PHONY: check
check:
	@echo "==> Checking for required tools..."
	@which $(LATEX) > /dev/null || (echo "ERROR: pdflatex not found" && exit 1)
	@which $(BIBER) > /dev/null || (echo "ERROR: biber not found" && exit 1)
	@which $(PYTHON) > /dev/null || (echo "ERROR: python3 not found" && exit 1)
	@which $(BLACK) > /dev/null || echo "WARNING: black not found (needed for Python formatting)"
	@echo "==> All required tools found"
	@echo ""
	@echo "==> Checking for required LaTeX packages..."
	@for pkg in biblatex microtype booktabs caption enumitem titlesec fancyhdr \
		geometry graphicx hyperref cleveref csquotes tgpagella inconsolata \
		newpx amsmath amssymb xcolor adjustbox; do \
		if kpsewhich $$pkg.sty >/dev/null 2>&1; then \
			echo "✓ $$pkg"; \
		else \
			echo "✗ $$pkg - Install with: tlmgr install $$pkg"; \
			MISSING=1; \
		fi; \
	done
	@if [ "$$MISSING" = "1" ]; then \
		echo ""; \
		echo "==> Some packages are missing. Install them with tlmgr or mpm."; \
		exit 1; \
	else \
		echo ""; \
		echo "==> All required packages found!"; \
	fi

# Setup project structure
.PHONY: setup
setup: check
	@echo "==> Setting up project structure..."
	@mkdir -p $(FIGURES_DIR) $(DATA_DIR)/raw $(DATA_DIR)/processed
	@touch $(DATA_DIR)/raw/.gitkeep $(DATA_DIR)/processed/.gitkeep
	@echo "==> Testing minimal compilation..."
	@if $(MAKE) test-quick; then \
		echo "==> Setup complete! You can now run 'make pdf' to build the paper."; \
	else \
		echo "==> Setup incomplete. Check the errors above."; \
		exit 1; \
	fi

# Check package dependencies only
.PHONY: check-deps
check-deps:
	@echo "==> Checking LaTeX package dependencies..."
	@$(SRC_DIR)/sh/check-packages.sh || echo "Script not found - checking manually..."
	@for pkg in biblatex microtype booktabs; do \
		kpsewhich $$pkg.sty >/dev/null 2>&1 || echo "Missing: $$pkg"; \
	done

# Testing targets
.PHONY: test
test:
	@echo "==> Running all tests..."
	@tests/run-tests.sh

.PHONY: test-compile
test-compile:
	@echo "==> Running compilation tests..."
	@tests/run-tests.sh

.PHONY: test-quick
test-quick:
	@echo "==> Running quick tests (minimal fixture only)..."
	@tests/run-tests.sh tests/fixtures/minimal.tex

.PHONY: test-clean
test-clean: clean
	@echo "==> Testing from clean state..."
	@$(MAKE) test

# Diagnostic commands
.PHONY: diagnose
diagnose:
	@echo "==> Running LaTeX diagnostics..."
	@echo "\\documentclass{article}" > diagnose.tex
	@echo "\\usepackage{paper/paperstyle}" >> diagnose.tex
	@echo "\\begin{document}" >> diagnose.tex
	@echo "\\paperstylediagnostics" >> diagnose.tex
	@echo "\\end{document}" >> diagnose.tex
	@$(LATEX) -interaction=nonstopmode diagnose.tex > /dev/null 2>&1 || true
	@rm -f diagnose.*
	@echo "==> Check main.log for diagnostic output"

.PHONY: warnings
warnings:
	@echo "==> Analyzing compilation warnings..."
	@if [ -f main.log ]; then \
		echo ""; \
		echo "Overfull hboxes:"; \
		grep "Overfull \\\\hbox" main.log | wc -l; \
		echo ""; \
		echo "Underfull hboxes:"; \
		grep "Underfull \\\\hbox" main.log | wc -l; \
		echo ""; \
		echo "Package warnings (excluding hyperref):"; \
		grep "Warning:" main.log | grep -v "hyperref Warning: Token" | head -10; \
	else \
		echo "No main.log found. Run 'make pdf' first."; \
	fi

# Help target
.PHONY: help
help:
	@echo "East Asian Miracle Paper - Makefile targets:"
	@echo ""
	@echo "Compilation targets:"
	@echo "  make pdf        - Full compilation with bibliography (default)"
	@echo "  make quick      - Quick compilation without bibliography"
	@echo "  make clean      - Remove auxiliary files (keep PDF)"
	@echo "  make distclean  - Remove all generated files including PDF"
	@echo ""
	@echo "Development targets:"
	@echo "  make dev        - Development build (clean + validate + quick)"
	@echo "  make watch      - Auto-rebuild on file changes (requires fswatch/inotify)"
	@echo "  make validate   - Check template integrity and dependencies"
	@echo "  make style-check - Check LaTeX style compliance"
	@echo "  make format     - Format Python code with black"
	@echo "  make figures    - Generate all figures from Python scripts"
	@echo ""
	@echo "Setup requirements:"
	@echo "  macOS: brew install fswatch"
	@echo "  Linux: sudo apt-get install inotify-tools"
	@echo ""
	@echo "Testing targets:"
	@echo "  make test       - Run all tests"
	@echo "  make test-compile - Test LaTeX compilation"
	@echo "  make test-quick - Quick test with minimal fixture"
	@echo "  make test-clean - Test from clean state"
	@echo ""
	@echo "  make help       - Show this help message"