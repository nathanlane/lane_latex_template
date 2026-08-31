# Makefile for the lanepaper package and its demo document.
#
# One target per job. Aliases were deleted in issue #51 rather than kept as
# forwarders: when four targets ran the tests, nobody could tell which one CI
# used. Every gate below is the one CI runs.

# Tools
LATEXMK = latexmk
CHKTEX  = chktex
L3BUILD = l3build

# chktex warning classes suppressed for this project's prose conventions.
CHKTEXFLAGS = -q -n1 -n3 -n8 -n11 -n13 -n18 -n24 -n36 -n39 -n42 -n46
# -n48 exists only in chktex >= 1.7.7; older binaries (TeX Live 2022's 1.7.6)
# error out with "Illegal warning number". Probe once at make time. The probe
# runs against /dev/null on purpose: it must answer "does this binary accept
# the flag", not "does some file have warnings", and chktex exits non-zero
# when a real file has any.
CHKTEX_N48 := $(shell $(CHKTEX) -q -n48 /dev/null >/dev/null 2>&1 && echo " -n48")
CHKTEXFLAGS += $(CHKTEX_N48)

# Directories
MAIN           = main
DEMO_DIR       = demo

# Find the package and the demo's bibliography without installing them.
export TEXINPUTS := ./lanepaper:./demo:$(TEXINPUTS)
export BIBINPUTS := .:./demo:$(BIBINPUTS)

# `make` with no target builds the demo.
.PHONY: build
build:
	$(LATEXMK) -pdf -interaction=nonstopmode $(DEMO_DIR)/$(MAIN).tex

# ChkTeX checks the demo sources.
.PHONY: lint
lint:
	$(CHKTEX) $(CHKTEXFLAGS) $(DEMO_DIR)/*.tex

# The whole suite, in the order CI runs it.
.PHONY: test
test:
	python3 -m pytest -q
	bash tests/run-tests.sh

# Removes generated output, the PDF included. Everything here is rebuilt by
# `make build`.
.PHONY: clean
clean:
	$(LATEXMK) -C $(DEMO_DIR)/$(MAIN).tex >/dev/null 2>&1 || true
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).bcf $(MAIN).blg $(MAIN).fdb_latexmk \
		$(MAIN).fls $(MAIN).log $(MAIN).out $(MAIN).run.xml $(MAIN).toc $(MAIN).pdf
	rm -f $(DEMO_DIR)/*.aux
	rm -f texput.log
	@echo "==> Clean complete"

# ==============================================================================
# Packaging
# ==============================================================================
# l3build packages; pytest tests. build.lua declares no test files. See
# docs/adr/0002-l3build-for-packaging-pytest-for-tests.md.

# Install into TEXMFHOME so \usepackage{lanepaper} resolves outside this
# repository. Repository builds are unaffected: TEXINPUTS above puts
# ./lanepaper first, so the working tree always wins over an installed copy.
.PHONY: install
install:
	@echo "==> Installing lanepaper into $$(kpsewhich -var-value=TEXMFHOME)..."
	$(L3BUILD) install

.PHONY: uninstall
uninstall:
	$(L3BUILD) uninstall

# Build lanepaper-ctan.zip without submitting it.
.PHONY: ctan
ctan:
	$(L3BUILD) ctan

.PHONY: help
help:
	@echo "lanepaper - make targets:"
	@echo ""
	@echo "  build       Compile the demo document (default)"
	@echo "  lint        ChkTeX over the demo sources"
	@echo "  test        pytest plus the shell harness"
	@echo "  clean       Remove generated output, PDF included"
	@echo ""
	@echo "  install     Install the package into TEXMFHOME"
	@echo "  uninstall   Remove it from TEXMFHOME"
	@echo "  ctan        Build lanepaper-ctan.zip without submitting it"
	@echo ""
	@echo "  help        This message"
