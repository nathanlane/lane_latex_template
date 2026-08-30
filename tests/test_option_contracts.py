import os
import re
import subprocess
import textwrap

import pytest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def compile_latex(tmp_path, name, source):
    tex_file = tmp_path / f"{name}.tex"
    tex_file.write_text(textwrap.dedent(source), encoding="utf-8")
    env = os.environ.copy()
    env["TEXINPUTS"] = (
        f".:{ROOT / 'lanepaper'}:"
        f"{env.get('TEXINPUTS', '')}"
    )
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_file.name],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    log_text = (tmp_path / f"{name}.log").read_text(
        encoding="utf-8", errors="ignore"
    )
    return result, log_text


def assert_compiles(result, log_text):
    assert result.returncode == 0, result.stdout + result.stderr + log_text


REMOVED_OPTIONS = (
    "grid",
    "nogrid",
    "minimal",
    "draft",
    "natbib",
    "nobiblatex",
    "subsectionbarriers",
    "nosubsectionbarriers",
)

# The three v2 entry points a document could load directly. v3 (issue #85)
# leaves \usepackage{lanepaper} as the sole public load path.
REMOVED_ENTRY_POINTS = ("lnpminimal", "lnpgridoverlay", "lnpcompilationfixes")


def probe(tmp_path, name, body, class_options="11pt", options=""):
    """Compile a document that loads the package and runs `body` in it."""
    result, log_text = compile_latex(
        tmp_path,
        name,
        r"""
        \documentclass[%s]{article}
        \usepackage%s{lanepaper}
        \begin{document}
        %s
        Body.
        \end{document}
        """
        % (class_options, options, body),
    )
    assert_compiles(result, log_text)
    return log_text


def probe_names(tmp_path, name, names):
    r"""Report which of `names` a *document* can see after loading the package.

    Each entry is a control sequence spelled without its backslash.
    """
    log_text = probe(
        tmp_path,
        name,
        "\n".join(
            rf"\ifcsname {n}\endcsname\typeout{{LNP_SEE-{n}=yes}}"
            rf"\else\typeout{{LNP_SEE-{n}=no}}\fi"
            for n in names
        ),
    )
    seen = {}
    for n in names:
        match = re.search(rf"LNP_SEE-{re.escape(n)}=(yes|no)", log_text)
        assert match, f"probe {n} missing from log"
        seen[n] = match.group(1) == "yes"
    return seen


def measure_dimens(tmp_path, name, dimens, class_options="11pt"):
    """Compile a probe and return the named registers as floats in points."""
    log_text = probe(
        tmp_path,
        name,
        "\n".join(rf"\typeout{{LNP_DIM-{d}=\the\{d}}}" for d in dimens),
        class_options=class_options,
    )
    out = {}
    for d in dimens:
        match = re.search(rf"LNP_DIM-{d}=(-?[0-9.]+)pt", log_text)
        assert match, f"probe {d} missing from log"
        out[d] = float(match.group(1))
    return out


def test_only_optical_and_nocolor_options_are_accepted(tmp_path):
    """ADR-0006: [optical] and [nocolor] are the whole option surface."""
    log_text = probe(
        tmp_path,
        "retained-options-contract",
        r"\typeout{LNP_RETAINED_OPTIONS_OK}",
        options="[optical,nocolor]",
    )
    assert "LNP_RETAINED_OPTIONS_OK" in log_text
    assert "Unknown option" not in log_text


@pytest.mark.parametrize("option", REMOVED_OPTIONS)
def test_removed_options_are_rejected_without_aliases(tmp_path, option):
    """v3 removes the template modes outright: no alias, no inert acceptance.

    [natbib] and [nobiblatex] were kept declared-but-inert by #48 so existing
    documents got a warning instead of an error. v3 is a deliberate breaking
    contraction, so they now fail like any other unknown option.
    """
    _, log_text = compile_latex(
        tmp_path,
        f"{option}-removed-contract",
        rf"""
        \documentclass[11pt]{{article}}
        \usepackage[{option}]{{lanepaper}}
        \begin{{document}}
        Body.
        \end{{document}}
        """,
    )
    assert f"Unknown option `{option}'" in log_text.replace("\n", "")


@pytest.mark.parametrize("package", REMOVED_ENTRY_POINTS)
def test_removed_entry_points_cannot_be_loaded(tmp_path, package):
    """Issue #85: lanepaper is the sole public load path."""
    _, log_text = compile_latex(
        tmp_path,
        f"{package}-entrypoint-contract",
        rf"""
        \documentclass[11pt]{{article}}
        \usepackage{{{package}}}
        \begin{{document}}
        Body.
        \end{{document}}
        """,
    )
    assert f"File `{package}.sty' not found" in log_text


def test_optical_option_tightens_the_last_line(tmp_path):
    r"""[optical] is reserved for sourced refinements; runt control is the
    first (Hochuli: a last line should reach at least a third of the measure).

    \parfillskip's stretch is the observable: the default keeps LaTeX's
    infinite fil, [optical] caps it at a fraction of \textwidth.
    """
    log_text = probe(
        tmp_path,
        "parfillskip-optical",
        r"\typeout{LNP_PARFILL=\the\parfillskip}"
        "\n"
        r"\typeout{LNP_MEASURE=\the\textwidth}",
        options="[optical]",
    )
    stretch = re.search(r"LNP_PARFILL=(.+)", log_text).group(1).strip()
    measure = float(re.search(r"LNP_MEASURE=([0-9.]+)pt", log_text).group(1))
    # A capped stretch, not LaTeX's infinite fil.
    assert "fil" not in stretch, stretch
    plus = float(re.search(r"plus ([0-9.]+)pt", stretch).group(1))
    assert 0.5 * measure < plus < 0.9 * measure


def test_default_last_line_is_standard_latex(tmp_path):
    """Without [optical] the package leaves \\parfillskip alone."""
    log_text = probe(
        tmp_path,
        "parfillskip-plain",
        r"\typeout{LNP_PARFILL=\the\parfillskip}",
    )
    assert "LNP_PARFILL=0.0pt plus 1.0fil" in log_text, log_text


# %% FIX (#88): Keep this wrapper because run-tests.sh does not invoke the
# manual bibliography script; the two removed wrappers only reran run-tests.sh.
def test_manual_biblatex_contract_passes():
    result = subprocess.run(
        [
            "bash",
            "tests/test-bibliography.sh",
            "tests/fixtures/biblatex-manual-contract.tex",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr


# %% FIX (#88): Compare rendered line starts to protect flush-left first paragraphs.
def test_first_paragraph_after_heading_is_flush_left(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "first-paragraph-after-heading",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lanepaper}
        \begin{document}
        \section{Heading}
        \leavevmode\pdfsavepos
        \write-1{LNP_FIRST_PARAGRAPH_X=\the\pdflastxpos}
        First paragraph after the heading.
        \par
        \leavevmode\pdfsavepos
        \write-1{LNP_SECOND_PARAGRAPH_X=\the\pdflastxpos}
        Second paragraph after an ordinary paragraph break.
        \par
        \noindent
        \leavevmode\pdfsavepos
        \write-1{LNP_EXPLICIT_NOINDENT_X=\the\pdflastxpos}
        Third paragraph with an explicit noindent command.
        \end{document}
        """,
    )

    assert_compiles(result, log_text)
    first = re.search(r"LNP_FIRST_PARAGRAPH_X=(\d+)", log_text)
    second = re.search(r"LNP_SECOND_PARAGRAPH_X=(\d+)", log_text)
    explicit_noindent = re.search(r"LNP_EXPLICIT_NOINDENT_X=(\d+)", log_text)
    assert first and second and explicit_noindent, log_text
    first_x = int(first.group(1))
    second_x = int(second.group(1))
    explicit_noindent_x = int(explicit_noindent.group(1))
    gap = second_x - first_x
    assert first_x == explicit_noindent_x, log_text
    assert first_x < second_x, log_text
    # 13.2pt expressed in TeX scaled points (sp).
    assert abs(gap - 865075) <= 2, log_text


# %% FIX (#88): Keep these retired public names undefined; this guards the API
# surface independently of the internal module layout.
def test_removed_paragraph_mode_switchers_are_undefined(tmp_path):
    seen = probe_names(
        tmp_path,
        "removed-paragraph-mode-switchers",
        ["classicalparagraphs", "modernparagraphs", "hybridparagraphs"],
    )
    assert [name for name, visible in seen.items() if visible] == []


def test_spacing_quantum_is_private_and_grid_helpers_are_gone(tmp_path):
    """ADR-0006: the 13.2pt quantum is an implementation value, not an API.

    Only the absence of the public names is asserted. What the quantum is
    called internally, and what it measures, are implementation details this
    suite deliberately does not reach for; the spacing it produces is covered
    by the measured-value tests.
    """
    seen = probe_names(
        tmp_path,
        "private-quantum-contract",
        [
            "gridunit",
            "halfgridunit",
            "quartergridunit",
            "threequartergridunit",
            "onehalfgridunit",
            "doublegridunit",
            "triplegridunit",
            "gridmult",
            "gridmath",
            "gridspace",
            "halfbaselinespace",
            "fullbaselinespace",
            "roundtogrid",
            "gridincludegraphics",
            "imagegridspace",
            "standardgrid",
            "compactgrid",
            "spaciousgrid",
            "customgrid",
            "showgrid",
            "hidegrid",
            "quartergridparagraphs",
            "thirdgridparagraphs",
            # Environments: \newenvironment defines a control sequence of the
            # same name, so the same probe answers for them.
            "grideqnarray",
            "gridgather",
        ],
    )
    assert [name for name, visible in seen.items() if visible] == []


@pytest.mark.parametrize(
    "class_options,paper_width",
    [("11pt", 614.295), ("11pt,a4paper", 597.50787)],
)
def test_class_paper_is_honored_with_a_centered_six_inch_measure(
    tmp_path, class_options, paper_width
):
    """Issue #85: the class picks the sheet; the package picks the measure.

    v2 forced letterpaper in \\geometry, so [a4paper] silently produced a
    Letter page. The six-inch text block and its centering are the invariant.
    """
    dims = measure_dimens(
        tmp_path,
        "paper-" + class_options.replace(",", "-"),
        ["paperwidth", "textwidth", "oddsidemargin"],
        class_options=class_options,
    )
    assert abs(dims["paperwidth"] - paper_width) < 0.01
    # 6in at 72.27pt/in.
    assert abs(dims["textwidth"] - 433.62) < 0.01
    # \oddsidemargin is measured from a 1in reference, so a centered block
    # sits at (paperwidth - textwidth)/2 - 1in.
    expected = (dims["paperwidth"] - dims["textwidth"]) / 2 - 72.26999
    assert abs(dims["oddsidemargin"] - expected) < 0.02


def test_no_bibliography_package_is_loaded(tmp_path):
    """#48: the bibliography belongs to the document (ADR-0003 rule 2).

    The package used to load biblatex with its own option set, which fixed the
    backend, style and sorting for every document using it.
    """
    result, log_text = compile_latex(
        tmp_path,
        "no-bibliography-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lanepaper}
        \begin{document}
        The document owns its bibliography.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "biblatex.sty" not in log_text
    assert "natbib.sty" not in log_text


def test_removed_document_structures_are_gone(tmp_path):
    """Issue #86: documents own orchestration; Lanepaper owns typography."""
    removed = (
        "epigraph",
        "emphasisquote",
        "quoteattribution",
        "openingparagraph",
        "academicdropcap",
        "firstlinesc",
        "sectionsep",
        "spacebreak",
        "majorsectionspace",
        "thinrulebreak",
        "paragraphsep",
        "abstractopening",
        "sidenote",
        "softfloatbarrier",
        "hardfloatbarrier",
        "sectionendfloatbarrier",
        "tryherefigure",
        "forceherefigure",
        "herefloat",
        "showfloatstats",
        "floatwarning",
        "balancefloatpage",
        "compensatetopfloat",
        "captionsource",
        "captioncontinued",
        "regressiontable",
        "tablenotes",
        "tabnote",
        "tablenote",
        "tabsource",
        "tabstars",
        "tabdaggers",
        "fignotes",
        "fignote",
        "figurenote",
        "figsource",
        "tabsample",
        "tabvars",
        "tabmethod",
        "tabcluster",
        "panellabel",
        "panelnote",
        "startappendices",
        "finishappendices",
        "documentAppendices",
        "lanepaperdiagnostics",
        "lanepaperinfo",
        "academicitem",
        "compactitem",
        "displayitem",
        "readableitem",
        "bulletmark",
        "dashmark",
        "refinedbullet",
        "diamondmark",
        "squaremark",
        "trianglemark",
        "subtlebullet",
        "refineddash",
        "itembullet",
        "itemdash",
        "itemdiamond",
        "itemsquare",
        "itemtriangle",
        "tightlists",
        "normallists",
        "spaciouslists",
        "dashbullets",
        "trianglebullets",
        "defaultbullets",
        "listhalfquantum",
        "listquarterquantum",
        "listquantum",
        "listhalfbaseline",
        "listquarterbaseline",
        "listbaselineskip",
        "listhangindent",
        "listnestedindent",
        "listlabelsep",
    )
    seen = probe_names(tmp_path, "removed-document-structures", removed)
    assert [name for name, visible in seen.items() if visible] == []


def test_sectionopening_is_one_inline_paragraph(tmp_path):
    """The one-argument opening styles text without ending the paragraph."""
    log_text = probe(
        tmp_path,
        "inline-section-opening",
        r"""
        \newcount\lnptestparagraphs
        \everypar{\global\advance\lnptestparagraphs by 1}
        \sectionopening{Opening text} continues in the same paragraph.\par
        \typeout{LNP_PARAGRAPHS=\the\lnptestparagraphs}
        """,
    )
    assert "LNP_PARAGRAPHS=1" in log_text


def test_threeparttable_owns_tablenotes(tmp_path):
    """Issue #86: Lanepaper neither loads nor redefines threeparttable APIs."""
    result, log_text = compile_latex(
        tmp_path,
        "threeparttable-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage{threeparttable}
        \usepackage{lanepaper}
        \begin{document}
        \begin{table}[tbp]
          \caption{Document-owned table notes}
          \centering
          \begin{threeparttable}
            \begin{tabular}{@{}lc@{}}
              \toprule
              Item & Value \\
              \midrule
              A & 1 \\
              \bottomrule
            \end{tabular}
            \begin{tablenotes}
              \item Notes are owned by threeparttable.
            \end{tablenotes}
          \end{threeparttable}
        \end{table}
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Command \\tablenotes already defined" not in log_text


def test_plain_ref_does_not_emit_package_warning(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "plain-ref-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lanepaper}
        \begin{document}
        \section{Target}\label{sec:target}
        Plain reference: \ref{sec:target}.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Direct \\ref usage detected" not in log_text


def test_footmisc_option_passthrough_no_clash(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "footmisc-passthrough-contract",
        r"""
        \documentclass[11pt]{article}
        \PassOptionsToPackage{bottom}{footmisc}
        \usepackage{lanepaper}
        \begin{document}
        Text with a note.\footnote{A footnote.}
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Option clash for package footmisc" not in log_text


def test_footnote_marker_box_fits_three_digits(tmp_path):
    # Measure the widest marker (\oldstylenums{999}) at the marker's exact
    # spec (6pt, native spacing) and assert it fits the \@makefntext box.
    # (An earlier overfull-hbox assertion passed even pre-fix because
    # \hfuzz=0.2pt hid the 0.2pt two-digit overflow.)
    result, log_text = compile_latex(
        tmp_path,
        "footnote-marker-width-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lanepaper}
        \newlength{\markwidth}
        \begin{document}
        \makeatletter
        \settowidth{\markwidth}{\fontsize{6}{7}\selectfont
          \oldstylenums{999}}
        \typeout{LNP_MARK999=\the\markwidth}
        \makeatother
        Text.\footnote{A footnote.}
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    match = re.search(r"LNP_MARK999=([0-9.]+)pt", log_text)
    assert match, log_text
    # Compare against the actual \@makefntext box width in the package, not a
    # hardcoded number, so the test fails if the box is shrunk again.
    sty = (ROOT / "lanepaper" / "lanepaper.sty").read_text(encoding="utf-8")
    boxes = re.findall(r"\\makebox\[([0-9.]+)pt\]", sty)
    assert boxes, "no footnote marker box found in lanepaper.sty"
    assert float(match.group(1)) <= min(float(b) for b in boxes)
