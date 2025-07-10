#!/bin/bash
# ==============================================================================
# Bibliography Testing Script
# ==============================================================================
# Purpose: Test full bibliography compilation cycle with biber
# This ensures citations are properly resolved
#
# Usage: ./test-bibliography.sh [tex-file]
# ==============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Default test file
TEST_FILE="${1:-tests/fixtures/minimal.tex}"
BASENAME=$(basename "$TEST_FILE" .tex)
OUTPUT_DIR="tests/compilation"
LOG_DIR="$OUTPUT_DIR/logs"

# Create directories
mkdir -p "$LOG_DIR"

echo -e "${YELLOW}Testing bibliography compilation for: $TEST_FILE${NC}"

# Step 1: First LaTeX compilation
echo "Step 1: Initial LaTeX compilation..."
if pdflatex -interaction=nonstopmode -halt-on-error "$TEST_FILE" > "$LOG_DIR/${BASENAME}_pass1.log" 2>&1; then
    echo -e "  ${GREEN}✓${NC} First pass successful"
else
    echo -e "  ${RED}✗${NC} First pass failed"
    tail -20 "$LOG_DIR/${BASENAME}_pass1.log"
    exit 1
fi

# Check if .bcf file was created (indicates biblatex is being used)
if [ -f "${BASENAME}.bcf" ]; then
    echo -e "  ${GREEN}✓${NC} Bibliography control file created"
    
    # Step 2: Run biber
    echo "Step 2: Running biber..."
    if biber "$BASENAME" > "$LOG_DIR/${BASENAME}_biber.log" 2>&1; then
        echo -e "  ${GREEN}✓${NC} Biber processing successful"
        
        # Check for biber warnings
        local biber_warnings=$(grep -c "WARN" "$LOG_DIR/${BASENAME}_biber.log" || true)
        if [ "$biber_warnings" -gt 0 ]; then
            echo -e "  ${YELLOW}⚠${NC}  Biber warnings: $biber_warnings"
            grep "WARN" "$LOG_DIR/${BASENAME}_biber.log" | head -3 | sed 's/^/    /'
        fi
    else
        echo -e "  ${RED}✗${NC} Biber processing failed"
        tail -20 "$LOG_DIR/${BASENAME}_biber.log"
        exit 1
    fi
else
    echo -e "  ${YELLOW}⚠${NC}  No .bcf file - document may not use biblatex"
fi

# Step 3: Second LaTeX compilation
echo "Step 3: Second LaTeX compilation..."
if pdflatex -interaction=nonstopmode -halt-on-error "$TEST_FILE" > "$LOG_DIR/${BASENAME}_pass2.log" 2>&1; then
    echo -e "  ${GREEN}✓${NC} Second pass successful"
else
    echo -e "  ${RED}✗${NC} Second pass failed"
    exit 1
fi

# Step 4: Third LaTeX compilation (for final cross-references)
echo "Step 4: Final LaTeX compilation..."
if pdflatex -interaction=nonstopmode -halt-on-error "$TEST_FILE" > "$LOG_DIR/${BASENAME}_pass3.log" 2>&1; then
    echo -e "  ${GREEN}✓${NC} Final pass successful"
else
    echo -e "  ${RED}✗${NC} Final pass failed"
    exit 1
fi

# Step 5: Check final result
echo -e "\n${YELLOW}Checking final document...${NC}"

# Check for undefined citations
undefined_citations=$(grep -c "Citation.*undefined" "$LOG_DIR/${BASENAME}_pass3.log" || true)
if [ "$undefined_citations" -gt 0 ]; then
    echo -e "  ${RED}✗${NC} Still have undefined citations: $undefined_citations"
    grep "Citation.*undefined" "$LOG_DIR/${BASENAME}_pass3.log" | head -5 | sed 's/^/    /'
    exit 1
else
    echo -e "  ${GREEN}✓${NC} All citations resolved"
fi

# Check for missing references
missing_refs=$(grep -c "Reference.*undefined" "$LOG_DIR/${BASENAME}_pass3.log" || true)
if [ "$missing_refs" -gt 0 ]; then
    echo -e "  ${RED}✗${NC} Undefined references: $missing_refs"
    grep "Reference.*undefined" "$LOG_DIR/${BASENAME}_pass3.log" | head -5 | sed 's/^/    /'
else
    echo -e "  ${GREEN}✓${NC} All references resolved"
fi

# Check page count
if [ -f "${BASENAME}.pdf" ]; then
    page_count=$(pdfinfo "${BASENAME}.pdf" 2>/dev/null | grep "Pages:" | awk '{print $2}')
    echo -e "  ${GREEN}✓${NC} PDF created with $page_count pages"
    
    # Move to output directory
    mv "${BASENAME}.pdf" "$OUTPUT_DIR/"
fi

# Clean up
rm -f "${BASENAME}.aux" "${BASENAME}.log" "${BASENAME}.out" "${BASENAME}.toc" 
rm -f "${BASENAME}.bcf" "${BASENAME}.bbl" "${BASENAME}.blg" "${BASENAME}.run.xml"

echo -e "\n${GREEN}Bibliography test complete!${NC}"