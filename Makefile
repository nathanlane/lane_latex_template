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

# Recursive assignment: `date` runs when the recipe runs, not at parse time.
RELEASE_DATE = $(shell date +%Y-%m-%d)

# Directories
MAIN           = main
PKG_DIR        = lanepaper
DEMO_DIR       = demo
APPENDICES_DIR = demo/appendices
SRC_DIR        = src

# Watched sources
TEX_SOURCES   = $(wildcard $(DEMO_DIR)/*.tex) $(wildcard $(APPENDICES_DIR)/*.tex)
STYLE_SOURCES = $(wildcard $(PKG_DIR)/*.sty)

# Find the package and the demo's bibliography without installing them.
export TEXINPUTS := ./lanepaper:./demo:$(TEXINPUTS)
export BIBINPUTS := .:./demo:$(BIBINPUTS)

# `make` with no target builds the demo.
.PHONY: build
build:
	$(LATEXMK) -pdf -interaction=nonstopmode $(DEMO_DIR)/$(MAIN).tex

# Both source checks. chktex reads the demo's prose; validate_latex_style.sh
# checks math spacing, which chktex does not cover.
.PHONY: lint
lint:
	$(CHKTEX) $(CHKTEXFLAGS) $(DEMO_DIR)/*.tex $(APPENDICES_DIR)/*.tex
	$(SRC_DIR)/sh/validate_latex_style.sh

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
	rm -f $(DEMO_DIR)/*.aux $(APPENDICES_DIR)/*.aux
	rm -f texput.log
	@echo "==> Clean complete"

.PHONY: check-deps
check-deps:
	$(SRC_DIR)/sh/check-packages.sh

.PHONY: watch
watch:
	@echo "==> Watching for changes (Ctrl+C to stop)..."
	@if command -v fswatch >/dev/null 2>&1; then \
		fswatch -o $(TEX_SOURCES) $(STYLE_SOURCES) | while read; do \
			$(MAKE) build; \
		done; \
	elif command -v inotifywait >/dev/null 2>&1; then \
		while inotifywait -r -e modify $(DEMO_DIR) $(PKG_DIR) >/dev/null 2>&1; do \
			$(MAKE) build; \
		done; \
	else \
		echo "==> ERROR: install fswatch (macOS: brew install fswatch)"; \
		echo "==>        or inotify-tools (Linux: apt-get install inotify-tools)"; \
		exit 1; \
	fi

# ==============================================================================
# Packaging and release
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

# make release VERSION=x.y.z
#
# Stamps one version and date into every \ProvidesPackage, proves the archive
# still builds from the stamped sources, promotes the CHANGELOG's Unreleased
# section, commits, and tags. Pushing is deliberate and separate:
#
#     git push origin main --follow-tags
#
# Pushing the tag is what builds the CTAN archive and publishes the GitHub
# release (.github/workflows/release.yml). Submitting to CTAN stays a manual
# step, because it is not reversible:
#
#     l3build upload x.y.z --email <address>
.PHONY: release
release:
	@test -n "$(VERSION)" || { echo "ERROR: make release VERSION=x.y.z"; exit 1; }
	@echo "$(VERSION)" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$$' \
		|| { echo "ERROR: VERSION must be x.y.z, got '$(VERSION)'"; exit 1; }
	@test -z "$$(git status --porcelain)" \
		|| { echo "ERROR: working tree is not clean"; exit 1; }
	@git rev-parse -q --verify "refs/tags/v$(VERSION)" >/dev/null \
		&& { echo "ERROR: tag v$(VERSION) already exists"; exit 1; } || true
	@which $(L3BUILD) >/dev/null \
		|| { echo "ERROR: $(L3BUILD) not found (it ships with TeX Live)"; exit 1; }
	@echo "==> Stamping v$(VERSION) into every \\ProvidesPackage..."
	$(L3BUILD) tag $(VERSION)
	@echo "==> Building the archive from the stamped sources..."
	@$(L3BUILD) ctan >/dev/null \
		|| { echo "ERROR: l3build ctan failed. Recover with: git checkout -- ."; exit 1; }
	@echo "==> Promoting the CHANGELOG's Unreleased section..."
	@grep -q '^## Unreleased$$' CHANGELOG.md \
		|| { echo "ERROR: CHANGELOG.md has no '## Unreleased' section"; exit 1; }
	@# The em dash is written as raw UTF-8 bytes, not \x{2014}: that escape
	@# upgrades the string to character semantics, so perl re-encodes the whole
	@# file and mangles every em dash already in it. Byte mode leaves them be.
	@perl -0pi -e 's/^## Unreleased$$/## Unreleased\n\n## v$(VERSION) \xe2\x80\x94 $(RELEASE_DATE)/m' CHANGELOG.md
	@git add -A
	@git commit -q -m "release: v$(VERSION)"
	@git tag -a "v$(VERSION)" -m "v$(VERSION)"
	@echo "==> Tagged v$(VERSION). Push with: git push origin main --follow-tags"

.PHONY: help
help:
	@echo "lanepaper - make targets:"
	@echo ""
	@echo "  build       Compile the demo document (default)"
	@echo "  lint        chktex plus the math-spacing checker"
	@echo "  test        pytest plus the shell harness"
	@echo "  clean       Remove generated output, PDF included"
	@echo "  check-deps  Verify the required LaTeX packages are installed"
	@echo "  watch       Rebuild on change (needs fswatch or inotify-tools)"
	@echo ""
	@echo "  install     Install the package into TEXMFHOME"
	@echo "  uninstall   Remove it from TEXMFHOME"
	@echo "  ctan        Build lanepaper-ctan.zip without submitting it"
	@echo "  release VERSION=x.y.z"
	@echo "              Stamp versions, update the CHANGELOG, commit and tag"
	@echo ""
	@echo "  help        This message"
