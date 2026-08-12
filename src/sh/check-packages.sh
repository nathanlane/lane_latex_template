#!/usr/bin/env bash
# check-packages.sh - verify LaTeX package dependencies for lltpaperstyle
# Exits 0 when every required package resolves via kpsewhich, 1 otherwise.
# Follows Google Shell Style Guide with strict mode.

set -o errexit
set -o nounset
set -o pipefail

# External packages loaded by lltpaperstyle and its modules (llt* modules are
# resolved via TEXINPUTS and checked separately by the build).
required_packages=(
  adjustbox
  amsmath
  amssymb
  appendix
  array
  booktabs
  caption
  cleveref
  csquotes
  enumitem
  etoolbox
  fancyhdr
  footmisc
  geometry
  graphicx
  hyperref
  lettrine
  longtable
  microtype
  newpxmath
  pdflscape
  placeins
  rotating
  scalefnt
  tabularx
  textcase
  tgpagella
  biblatex
  biber
)

missing=0
for pkg in "${required_packages[@]}"; do
  # biber is a binary, not a .sty
  if [[ "$pkg" == "biber" ]]; then
    if ! command -v biber >/dev/null 2>&1; then
      echo "Missing binary: biber"
      missing=1
    fi
    continue
  fi
  if ! kpsewhich "${pkg}.sty" >/dev/null 2>&1; then
    echo "Missing package: ${pkg}.sty"
    missing=1
  fi
done

if [[ "$missing" -eq 0 ]]; then
  echo "All ${#required_packages[@]} dependencies found."
fi
exit "$missing"
