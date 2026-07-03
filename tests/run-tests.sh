#!/bin/bash
# Simple LaTeX testing framework
# Designed for ease of use by both newbies and advanced users

set -euo pipefail

# Colors for output (works on most terminals)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FIXTURES_DIR="$SCRIPT_DIR/fixtures"
LOGS_DIR="$SCRIPT_DIR/compilation/logs"
OUTPUT_DIR="$SCRIPT_DIR/visual/output"
COMPAT_PROBES_DIR="$(mktemp -d)"

# Create necessary directories
mkdir -p "$LOGS_DIR" "$OUTPUT_DIR"
trap 'rm -rf "$COMPAT_PROBES_DIR"' EXIT

# Test results
PASSED=0
FAILED=0
SKIPPED=0

# Simple logging
log_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

log_info() {
    echo -e "${YELLOW}→${NC} $1"
}

# Test a single LaTeX file
test_latex_file() {
    local tex_file="$1"
    local basename=$(basename "$tex_file" .tex)
    local log_file="$LOGS_DIR/${basename}.log"
    local pdf_output="$OUTPUT_DIR/${basename}.pdf"
    local source_pdf="${tex_file%.tex}.pdf"
    local source_aux="${tex_file%.tex}.aux"
    local source_log="${tex_file%.tex}.log"
    local source_out="${tex_file%.tex}.out"
    local source_toc="${tex_file%.tex}.toc"
    local source_bcf="${tex_file%.tex}.bcf"
    local source_run_xml="${tex_file%.tex}.run.xml"
    local root_aux="$PROJECT_ROOT/${basename}.aux"
    local root_log="$PROJECT_ROOT/${basename}.log"
    local root_out="$PROJECT_ROOT/${basename}.out"
    local root_toc="$PROJECT_ROOT/${basename}.toc"
    local root_bcf="$PROJECT_ROOT/${basename}.bcf"
    local root_run_xml="$PROJECT_ROOT/${basename}.run.xml"
    
    log_info "Testing $basename..."
    
    # Change to project root for relative paths
    cd "$PROJECT_ROOT"
    
    # FIX: Keep direct script runs working when TEXINPUTS is unset.
    export TEXINPUTS=".:./paper:./paper/modules:${TEXINPUTS:-}"
    
    # Test 1: Basic compilation
    if pdflatex -interaction=nonstopmode -halt-on-error "$tex_file" > "$log_file" 2>&1; then
        # FIX: Run a second pass so hyperref/rerunfilecheck warnings settle.
        if ! pdflatex -interaction=nonstopmode -halt-on-error "$tex_file" > "$log_file" 2>&1; then
            log_fail "  Compilation failed on second pass (see $log_file)"
            return 1
        fi
        log_pass "  Compilation successful"
        
        # Move PDF to output directory.
        # FIX: Probe sources can live outside the repo; pdflatex writes their
        # PDF into the current directory when invoked from PROJECT_ROOT.
        local root_pdf="$PROJECT_ROOT/${basename}.pdf"
        if [ -f "$source_pdf" ]; then
            mv "$source_pdf" "$pdf_output"
        elif [ -f "$root_pdf" ]; then
            mv "$root_pdf" "$pdf_output"
        fi
    else
        log_fail "  Compilation failed (see $log_file)"
        return 1
    fi
    
    # Test 2: Check for warnings (excluding expected ones)
    # Exclude common harmless warnings
    if grep -E "(Warning|Error)" "$log_file" | \
       grep -v "Citation.*undefined" | \
       grep -v "Empty bibliography" | \
       grep -v "There were undefined references" | \
       grep -v "File.*out.*has changed" | \
       grep -v "Please.*re.*run.*Biber" | \
       grep -v "Command \\\\showhyphens" | \
       grep -v "Reference.*undefined" | \
       grep -v "Label.*may have changed" > /dev/null; then
        log_fail "  Found warnings in log"
        echo "    Warnings:"
        grep -E "(Warning|Error)" "$log_file" | \
            grep -v "Citation.*undefined" | \
            grep -v "Empty bibliography" | \
            grep -v "There were undefined references" | \
            grep -v "File.*out.*has changed" | \
            grep -v "Please.*re.*run.*Biber" | \
            grep -v "Command \\\\showhyphens" | \
            grep -v "Reference.*undefined" | \
            grep -v "Label.*may have changed" | head -5 | sed 's/^/    /'
    else
        log_pass "  No unexpected warnings found"
    fi
    
    # Test 3: Check PDF was created
    if [ -f "$pdf_output" ]; then
        log_pass "  PDF created successfully"
    else
        log_fail "  PDF not created"
    fi
    
    # Clean up auxiliary files
    # FIX: Compatibility probes can live in tmp dirs while pdflatex writes aux
    # files into PROJECT_ROOT, so clean both source-path and root fallbacks.
    rm -f "$source_aux" "$source_log" "$source_out" "$source_toc" \
          "$source_bcf" "$source_run_xml" \
          "$root_aux" "$root_log" "$root_out" "$root_toc" \
          "$root_bcf" "$root_run_xml"
    
    return 0
}

# Run a compatibility probe from a one-off inline source document.
run_compatibility_probe() {
    local name="$1"
    local tex_file="$COMPAT_PROBES_DIR/${name}.tex"

    cat > "$tex_file"
    test_latex_file "$tex_file"
}

# Run compatibility probes for API entry points that are contract-sensitive.
run_compatibility_probes() {
    log_info "Running compatibility probes (standalone and preload contracts)"
    local probe_failures=0

    if ! run_compatibility_probe "prelude-natbib-preamble" <<'EOF'
\documentclass[11pt]{article}
\input{paper/preamble-natbib.tex}

\begin{document}
\section{Natbib Preamble Contract}
\textcite{smith2020} described the framework in a foundational way.
\autocite{smith2020}

\begin{thebibliography}{1}
\bibitem[Smith(2020)]{smith2020} Smith, A. 2020. Legacy citation style.
\end{thebibliography}
\end{document}
EOF
    then
        probe_failures=$((probe_failures + 1))
    fi

    if ! run_compatibility_probe "main-package-minimal-option" <<'EOF'
\documentclass[11pt]{article}
\usepackage[minimal]{lltpaperstyle}
\begin{document}
Main package minimal option contract is stable.
\end{document}
EOF
    then
        probe_failures=$((probe_failures + 1))
    fi

    if ! run_compatibility_probe "standalone-lltpaperstyleminimal" <<'EOF'
\documentclass[11pt]{article}
\usepackage{lltpaperstyleminimal}
\begin{document}
Minimal style surface compiles standalone.
\end{document}
EOF
    then
        probe_failures=$((probe_failures + 1))
    fi

    if ! run_compatibility_probe "standalone-lltlists" <<'EOF'
\documentclass[11pt]{article}
\usepackage{lltlists}
\begin{document}
\begin{itemize}
  \item List entry one.
  \item List entry two.
  \setlist[itemize,1]{label=\dashmark}
\end{itemize}
\end{document}
EOF
    then
        probe_failures=$((probe_failures + 1))
    fi

    if ! run_compatibility_probe "standalone-lltmathgridlocked" <<'EOF'
\documentclass[11pt]{article}
\usepackage{lltmathgridlocked}
\begin{document}
\[
  E = mc^2
\]
\end{document}
EOF
    then
        probe_failures=$((probe_failures + 1))
    fi

    if ! run_compatibility_probe "standalone-lltfontfeatures" <<'EOF'
\documentclass[11pt]{article}
\usepackage{lltfontfeatures}
\begin{document}
\textfigs{123}
\chemform{E=mc^2}
\onehalf
\end{document}
EOF
    then
        probe_failures=$((probe_failures + 1))
    fi

    if ! run_compatibility_probe "preload-lltparagraphs-into-paperstyle" <<'EOF'
\documentclass[11pt]{article}
\usepackage{lltparagraphs}
\usepackage{lltpaperstyle}
\begin{document}
\paragraph{Preload contract}
This verifies paragraph module preloading compatibility.
\begin{quote}
  Modular API contracts should remain stable under preload.
\end{quote}
\end{document}
EOF
    then
        probe_failures=$((probe_failures + 1))
    fi

    if ! run_compatibility_probe "standalone-lltfontfallbacks" <<'EOF'
\documentclass[11pt]{article}
\usepackage{lltfontfallbacks}
\begin{document}
\showfontconfig
Font fallback standalone surface compiles.
\end{document}
EOF
    then
        probe_failures=$((probe_failures + 1))
    fi

    if ((probe_failures > 0)); then
        log_fail "$probe_failures compatibility probe failures"
        return 1
    else
        log_pass "All compatibility probes passed"
    fi
}

# Main test runner
main() {
    echo "🧪 LaTeX Testing Framework"
    echo "========================="
    echo
    
    # Check for pdflatex
    if ! command -v pdflatex &> /dev/null; then
        echo -e "${RED}Error: pdflatex not found. Please install a TeX distribution.${NC}"
        exit 1
    fi
    
    # FIX: Honor explicit fixture arguments for quick regression runs.
    local fixtures=()
    if [ "$#" -gt 0 ]; then
        for fixture_arg in "$@"; do
            if [ ! -f "$fixture_arg" ]; then
                echo -e "${RED}Error: fixture not found: $fixture_arg${NC}"
                exit 1
            fi
            fixtures+=("$fixture_arg")
        done
    else
        while IFS= read -r fixture; do
            fixtures+=("$fixture")
        done < <(find "$FIXTURES_DIR" -name "*.tex" -type f | sort)
    fi

    if [ ${#fixtures[@]} -eq 0 ]; then
        echo -e "${YELLOW}No test fixtures found in $FIXTURES_DIR${NC}"
        exit 0
    fi
    
    echo "Found ${#fixtures[@]} test files"
    echo
    
    # Test each fixture
    for fixture in "${fixtures[@]}"; do
        test_latex_file "$fixture" || true
        echo
    done

    run_compatibility_probes || true

    # Summary
    echo "Test Summary"
    echo "============"
    echo -e "Passed: ${GREEN}$PASSED${NC}"
    echo -e "Failed: ${RED}$FAILED${NC}"
    
    if [ $FAILED -gt 0 ]; then
        echo
        echo -e "${RED}Some tests failed. Check the log files in:${NC}"
        echo "  $LOGS_DIR"
        exit 1
    else
        echo
        echo -e "${GREEN}All tests passed! 🎉${NC}"
        echo
        echo "Visual outputs available in:"
        echo "  $OUTPUT_DIR"
    fi
}

# Run tests
main "$@"
