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

# Create necessary directories
mkdir -p "$LOGS_DIR" "$OUTPUT_DIR"

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
    
    log_info "Testing $basename..."
    
    # Change to project root for relative paths
    cd "$PROJECT_ROOT"
    
    # Set TEXINPUTS to include paper directory for new package names
    export TEXINPUTS=".:./paper:./paper/modules:$TEXINPUTS"
    
    # Test 1: Basic compilation
    if pdflatex -interaction=nonstopmode -halt-on-error "$tex_file" > "$log_file" 2>&1; then
        log_pass "  Compilation successful"
        
        # Move PDF to output directory
        if [ -f "${basename}.pdf" ]; then
            mv "${basename}.pdf" "$pdf_output"
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
    rm -f "${basename}.aux" "${basename}.log" "${basename}.out" "${basename}.toc"
    
    return 0
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
    
    # Find all test fixtures
    local fixtures=($(find "$FIXTURES_DIR" -name "*.tex" -type f | sort))
    
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