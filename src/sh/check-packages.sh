#!/usr/bin/env bash
# check-packages.sh - verify LaTeX package dependencies for lanepaper
# Exits 0 when every required package resolves via kpsewhich, 1 otherwise.
# Follows Google Shell Style Guide with strict mode.

set -o errexit
set -o nounset
set -o pipefail

# External packages loaded by lanepaper and its modules (lnp* modules are
# resolved via TEXINPUTS and checked separately by the build).
# Regenerated from the source by issue #48. Every entry below is an
# unconditional \RequirePackage in lanepaper/*.sty; lnp* modules resolve via
# TEXINPUTS and are checked by the build.
#
# NOT listed, deliberately: hyperref and longtable are configure-if-loaded
# (ADR-0003 rule 2), while cleveref, biblatex, babel, appendix, threeparttable,
# tabularx, csquotes, and placeins are document-owned. pdflscape, rotating and
# adjustbox moved to the demo with the landscape wrappers. courier, mathpazo,
# mathptmx and palatino are
# font fallbacks loaded only inside \IfFileExists, so their absence is not a
# missing dependency.
required_packages=(
  amsmath
  amssymb
  array
  booktabs
  calc
  caption
  enumitem
  eso-pic
  etoolbox
  fancyhdr
  fontenc
  footmisc
  geometry
  graphicx
  iftex
  inputenc
  letterspace
  lettrine
  mathalfa
  microtype
  newpxmath
  ragged2e
  scalefnt
  textcase
  textcomp
  tgpagella
  tikz
  titlesec
  xcolor
  zi4
  # Not a .sty: the loop below checks it as a binary.
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
