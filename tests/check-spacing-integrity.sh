#!/bin/bash
# ==============================================================================
# Spacing Integrity Checker for LaTeX Documents
# ==============================================================================
# Purpose: Detect global spacing issues that might not be caught by compilation
# This script analyzes PDFs for anomalies that indicate spacing leaks
#
# STATUS: Advisory diagnostic only (Lane 1 build-hygiene decision). It reports
# heuristic density/efficiency warnings but never fails the build: it always
# exits 0 except on genuine tooling errors (missing poppler utilities). Do not
# use it as a hard pass/fail gate unless the heuristics are recalibrated for the
# template PDF. See docs/technical/TESTING.md for the current warning policy.
#
# Usage: ./check-spacing-integrity.sh [pdf-file]
# ==============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if pdftotext is available
if ! command -v pdftotext &> /dev/null; then
    echo -e "${RED}Error: pdftotext not found. Install poppler-utils.${NC}"
    exit 1
fi

# Check if pdfinfo is available
if ! command -v pdfinfo &> /dev/null; then
    echo -e "${RED}Error: pdfinfo not found. Install poppler-utils.${NC}"
    exit 1
fi

# Function to analyze a PDF
analyze_pdf() {
    local pdf_file="$1"
    local basename=$(basename "$pdf_file" .pdf)
    
    echo -e "${YELLOW}Analyzing: $pdf_file${NC}"
    
    # Extract basic info
    local page_count=$(pdfinfo "$pdf_file" 2>/dev/null | grep "Pages:" | awk '{print $2}')
    local file_size=$(stat -f%z "$pdf_file" 2>/dev/null || stat -c%s "$pdf_file" 2>/dev/null)
    local file_size_kb=$((file_size / 1024))
    
    echo "  Pages: $page_count"
    echo "  Size: ${file_size_kb}KB"
    
    # Extract text and analyze line density
    pdftotext -layout "$pdf_file" - > "${basename}_text.tmp"
    
    # Count lines per page (rough estimate)
    local total_lines=$(wc -l < "${basename}_text.tmp")
    local lines_per_page=$((total_lines / page_count))
    
    echo "  Average lines per page: $lines_per_page"
    
    # Check for spacing anomalies
    local issues=0
    
    # Test 1: Excessive page count for content
    local word_count=$(wc -w < "${basename}_text.tmp")
    local words_per_page=$((word_count / page_count))
    
    if [ "$words_per_page" -lt 200 ]; then
        echo -e "  ${RED}WARNING: Low word density ($words_per_page words/page)${NC}"
        echo "    This might indicate excessive spacing"
        ((issues++))
    else
        echo -e "  ${GREEN}✓ Word density normal ($words_per_page words/page)${NC}"
    fi
    
    # Test 2: Check for unusual line patterns
    # Look for multiple consecutive blank lines (spacing leak indicator)
    local blank_sequences=$(grep -E "^[[:space:]]*$" "${basename}_text.tmp" | uniq -c | awk '$1 > 3' | wc -l)
    
    if [ "$blank_sequences" -gt 5 ]; then
        echo -e "  ${RED}WARNING: Excessive blank line sequences ($blank_sequences)${NC}"
        echo "    This might indicate spacing commands affecting global layout"
        ((issues++))
    else
        echo -e "  ${GREEN}✓ Blank line distribution normal${NC}"
    fi
    
    # Test 3: Page efficiency check
    # Normal academic documents have ~300-500 words per page
    if [ "$page_count" -gt 0 ]; then
        local expected_pages=$((word_count / 400))  # Assuming 400 words/page average
        local efficiency=$((expected_pages * 100 / page_count))
        
        if [ "$efficiency" -lt 60 ]; then
            echo -e "  ${RED}WARNING: Low page efficiency ($efficiency%)${NC}"
            echo "    Expected ~$expected_pages pages, got $page_count"
            ((issues++))
        else
            echo -e "  ${GREEN}✓ Page efficiency normal ($efficiency%)${NC}"
        fi
    fi
    
    # Clean up
    rm -f "${basename}_text.tmp"
    
    # Summary
    echo ""
    if [ "$issues" -eq 0 ]; then
        echo -e "${GREEN}✓ No spacing issues detected${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ $issues potential spacing issue(s) flagged (advisory)${NC}"
        return 1
    fi
}

# Main execution
if [ $# -eq 0 ]; then
    # Analyze all PDFs in tests/visual/output/
    echo "Checking all test PDFs for spacing integrity..."
    echo "============================================="
    
    failed=0
    for pdf in tests/visual/output/*.pdf; do
        if [ -f "$pdf" ]; then
            if ! analyze_pdf "$pdf"; then
                ((failed++))
            fi
            echo ""
        fi
    done
    
    if [ "$failed" -gt 0 ]; then
        echo -e "${YELLOW}Advisory: $failed PDF(s) flagged potential spacing issues (diagnostic only, not a build gate)${NC}"
    else
        echo -e "${GREEN}All PDFs pass spacing integrity heuristics${NC}"
    fi
    # %% FIX: Advisory diagnostic only (Lane 1); heuristic flags must not fail the build.
    exit 0
else
    # Analyze specific PDF
    # %% FIX: Advisory diagnostic only (Lane 1); heuristic flags must not set a non-zero build-gate status.
    analyze_pdf "$1" || true
    exit 0
fi
