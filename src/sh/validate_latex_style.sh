#!/usr/bin/env bash
# validate_latex_style.sh - LaTeX style compliance checker
# Follows Google Shell Style Guide with strict mode

set -o errexit
set -o nounset
set -o pipefail

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Exit codes
readonly SUCCESS=0
readonly ERROR=1

# Counters
errors=0
warnings=0

# Function to print colored output
print_error() {
  echo -e "${RED}ERROR: $1${NC}" >&2
  ((errors++))
}

print_warning() {
  echo -e "${YELLOW}WARNING: $1${NC}" >&2
  ((warnings++))
}

print_success() {
  echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
  echo -e "$1"
}

# Check if file exists
check_file_exists() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    print_error "Required file not found: $file"
    return $ERROR
  fi
  return $SUCCESS
}

# Validate LaTeX source formatting
check_latex_formatting() {
  local file="$1"
  local filename=$(basename "$file")
  
  print_info "\nChecking $filename..."
  
  # Check for one sentence per line
  if grep -E '\.( )+[A-Z]' "$file" | grep -v '\\' > /dev/null; then
    print_warning "Multiple sentences on same line detected in $filename"
    print_info "  LaTeX best practice: one sentence per line for clean diffs"
  fi
  
  # Check for consistent emphasis usage
  if grep -E '\\textit\{[^}]*\}' "$file" | grep -v 'non-emphatic' > /dev/null; then
    if ! grep -q 'specifically need italic' "$file"; then
      print_warning "Using \\textit{} for emphasis in $filename"
      print_info "  Use \\emph{} for semantic emphasis (handles nesting correctly)"
    fi
  fi
  
  # Check for proper label prefixes
  local bad_labels=$(grep -E '\\label\{[^}]*\}' "$file" | \
    grep -vE '\\label\{(sec|subsec|fig|tab|eq|alg|lst|thm|def|app):' || true)
  
  if [[ -n "$bad_labels" ]]; then
    print_error "Invalid label prefixes found in $filename:"
    echo "$bad_labels" | head -5
    print_info "  Required prefixes: sec:, subsec:, fig:, tab:, eq:, alg:, lst:, thm:, def:, app:"
  fi
  
  # Check for spacing around math operators
  if grep -E '\$[^$]*[=+\-*/][^ =+\-*/\$][^$]*\$' "$file" > /dev/null; then
    print_warning "Missing spaces around math operators in $filename"
    print_info "  Use spaces: \$x = y + z\$ not \$x=y+z\$"
  fi
  
  # Check for non-breaking spaces before citations
  if grep -E '[^~]\\cite\{' "$file" > /dev/null; then
    print_warning "Missing non-breaking space before \\cite in $filename"
    print_info "  Use ~\\cite{} to prevent line breaks before citations"
  fi
  
  # Check for proper figure/table references
  if grep -E 'Figure [0-9]|Table [0-9]' "$file" | grep -v '~' > /dev/null; then
    print_warning "Hard-coded figure/table numbers in $filename"
    print_info "  Use Figure~\\ref{fig:name} for automatic numbering"
  fi
}

# Check Python code style
check_python_style() {
  local py_files=$(find ../src/py -name "*.py" 2>/dev/null)
  
  if [[ -z "$py_files" ]]; then
    print_info "\nNo Python files to check"
    return $SUCCESS
  fi
  
  print_info "\nChecking Python style compliance..."
  
  # Check if black is available
  if ! command -v black &> /dev/null; then
    print_warning "black formatter not installed - skipping Python checks"
    return $SUCCESS
  fi
  
  # Check Python formatting
  for file in $py_files; do
    if ! black --check --quiet "$file" 2>/dev/null; then
      print_error "Python file needs formatting: $file"
      print_info "  Run: make format"
    else
      print_success "Python formatting OK: $(basename $file)"
    fi
  done
}

# Check bibliography entries
check_bibliography() {
  local bib_file="../references.bib"
  
  if [[ ! -f "$bib_file" ]]; then
    print_warning "Bibliography file not found: $bib_file"
    return $SUCCESS
  fi
  
  print_info "\nChecking bibliography..."
  
  # Check for missing fields in entries
  local entry_count=$(grep -c '^@' "$bib_file" || true)
  print_success "Found $entry_count bibliography entries"
  
  # Check for DOI formatting
  if grep -E 'doi\s*=\s*{[^}]*http' "$bib_file" > /dev/null; then
    print_warning "DOI fields should not include http:// prefix"
    print_info "  Use: doi = {10.1000/journal.2023}"
  fi
}

# Main validation function
main() {
  print_info "=== LaTeX Style Compliance Validator ==="
  print_info "Checking East Asian Miracle paper..."
  
  # Change to repository root
  cd "$(dirname "$0")/../.."
  
  # Check required files exist
  local required_files=(
    "main.tex"
    "paper/lltpaperstyle.sty"
    "paper/preamble.tex"
    "references.bib"
    "CLAUDE.md"
  )
  
  for file in "${required_files[@]}"; do
    check_file_exists "$file"
  done
  
  # Check main LaTeX files
  local tex_files=$(find . -name "*.tex" -not -path "./context/*" | sort)
  
  for file in $tex_files; do
    check_latex_formatting "$file"
  done
  
  # Check Python style
  check_python_style
  
  # Check bibliography
  check_bibliography
  
  # Summary
  print_info "\n=== Validation Summary ==="
  if [[ $errors -eq 0 ]]; then
    print_success "No errors found!"
  else
    print_error "Found $errors error(s)"
  fi
  
  if [[ $warnings -gt 0 ]]; then
    print_warning "Found $warnings warning(s)"
  fi
  
  # Return appropriate exit code
  if [[ $errors -gt 0 ]]; then
    return $ERROR
  fi
  
  return $SUCCESS
}

# Run main function
main "$@"