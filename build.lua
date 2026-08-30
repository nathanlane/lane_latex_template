--[[

  Build configuration for the lanepaper package.

  l3build is adopted for PACKAGING ONLY: install, tag, ctan, upload. It is
  deliberately not the test harness -- pytest is, and CI runs
  `python3 -m pytest -q` unchanged. See
  docs/adr/0002-l3build-for-packaging-pytest-for-tests.md for why log-diffing
  with `l3build check` is a poor fit for a package with this many third-party
  dependencies.

  Every file list below is set explicitly, including the empty ones, because
  each l3build default is wrong for this repository:

    sourcefiles   default matches *.dtx, *.ins and dated .sty names; the
                  sources here are 11 plain, hand-written .sty files
    unpackfiles   there is no .ins -- the .dtx/.ins scaffold was deleted in
                  issue #49. Unpack still stages the sources into unpackdir,
                  which is where `install` reads installfiles from.
    checkfiles    ADR-0002: no test files are declared, on purpose
    typesetfiles  no .dtx, so there is nothing to typeset
    cleanfiles    the default (*.log, *.pdf, *.zip) is applied to maindir,
                  which would delete the demo's main.pdf. `make clean` owns
                  build artefacts here.

--]]

module  = "lanepaper"
ctanpkg = "lanepaper"

-- Sources: hand-written .sty files, no generated intermediates.
sourcefiledir = "lanepaper"
sourcefiles   = {"*.sty"}
installfiles  = {"*.sty"}
unpackfiles   = {}

-- Packaging only. Nothing to check, nothing to typeset.
checkfiles   = {}
checkengines = {}
typesetfiles = {}
cleanfiles   = {}

-- Shipped alongside the package in the CTAN archive.
textfiles  = {"README.md", "CHANGELOG.md", "LICENSE", "licenses/LICENSE-MIT.txt"}
ctanreadme = "README.md"

-- `l3build tag <version>` stamps one version and date into every
-- \ProvidesPackage. That is the whole point of adopting it: the modules
-- had drifted to three different version namespaces (v1.1, v1.2, v2.0) while
-- the repository was tagged v2.1.0.
tagfiles = {"*.sty"}

function update_tag(filename, content, tagname, tagdate)
  if not tagname then
    error("A version is required: l3build tag <version>")
  end
  -- Accept both `2.2.0` and `v2.2.0`; \ProvidesPackage always gets one `v`.
  local version = tagname:gsub("^v", "")
  -- l3build hands the date over as YYYY-MM-DD; LaTeX wants YYYY/MM/DD.
  local date = tagdate:gsub("%-", "/")
  -- Rewrite only the date and version, keeping each module's own description.
  return (content:gsub(
    "(\\ProvidesPackage%s*{[^}]*}%s*%[)%d%d%d%d/%d%d/%d%d%s+v[%w%.%-]+%s+",
    "%1" .. date .. " v" .. version .. " "
  ))
end

-- Metadata for `l3build upload`, so a CTAN submission cannot drift from the
-- source. Three fields are deliberately absent:
--
--   email         supplied per upload: `l3build upload x.y.z --email <address>`
--                 An uploader's address does not belong in a public repository.
--   announcement  supplied per release: `--message "..."` or `-F notes.txt`
--   topic         CTAN validates topic names against its own list and rejects
--                 an unknown one; leaving it out lets CTAN assign.
--
-- `upload` is never run by CI. It is not reversible, so it stays manual.
uploadconfig = {
  author     = "Nathan Lane",
  uploader   = "Nathan Lane",
  license    = "lppl1.3c",
  ctanPath   = "/macros/latex/contrib/lanepaper",
  summary    = "Academic typography for LaTeX: a spacing quantum, Pagella fonts, refined headings, lists and spacing",
  description = [[
    lanepaper is a pdfLaTeX package for academic papers. It states most
    vertical spacing in multiples of a single 13.2pt quantum, pairs TeX Gyre
    Pagella text with newpx maths, and tunes headings, lists, floats and
    footnotes to that scale. \usepackage{lanepaper} is the only load path; it
    takes two options, [optical] for sourced optical refinements and [nocolor]
    for a grayscale palette.

    Bibliography, cross-reference and appendix packages are document-owned.
    If present, lanepaper only applies narrow link styling to hyperref and
    sets longtable's caption width.
  ]],
  home       = "https://github.com/nathanlane/lane_latex_template",
  repository = "https://github.com/nathanlane/lane_latex_template",
  bugtracker = "https://github.com/nathanlane/lane_latex_template/issues",
}
