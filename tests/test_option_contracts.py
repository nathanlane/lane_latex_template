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


def test_nocolor_maps_semantic_colors_to_black(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "nocolor-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[nocolor]{lanepaper}
        \makeatletter
        \newcommand{\showcolorhex}[2]{%
          \convertcolorspec{named}{#1}{HTML}{#2}%
        }
        \makeatother
        \begin{document}
        \showcolorhex{sectioncolor}{\lnpsectionhex}
        \showcolorhex{linknavy}{\lnplinkhex}
        \typeout{LNP_SECTION_HEX=\lnpsectionhex}
        \typeout{LNP_LINK_HEX=\lnplinkhex}
        \section{No Color}
        Body text.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "LNP_SECTION_HEX=000000" in log_text
    assert "LNP_LINK_HEX=000000" in log_text


def test_minimal_nocolor_compiles(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "minimal-nocolor-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[minimal,nocolor]{lanepaper}
        \begin{document}
        \typeout{LNP_MINIMAL_NOCOLOR_OK}
        Minimal no-color contract.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "LNP_MINIMAL_NOCOLOR_OK" in log_text


def test_draft_option_reports_microtype_draft_mode(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "draft-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[draft]{lanepaper}
        \begin{document}
        Draft mode contract.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert re.search(
        r"Package (lanepaper|lnpmicrotype) Info: microtype draft mode active",
        log_text,
    )


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


@pytest.mark.parametrize("option", ["natbib", "nobiblatex"])
def test_deprecated_bibliography_options_are_accepted_and_inert(tmp_path, option):
    """Both options are deprecated by #48 but must not break existing documents.

    They stay declared so a document passing one gets a warning rather than
    LaTeX's "Unknown option" error, and neither loads anything.
    """
    result, log_text = compile_latex(
        tmp_path,
        f"{option}-deprecated-contract",
        rf"""
        \documentclass[11pt]{{article}}
        \usepackage[{option}]{{lanepaper}}
        \begin{{document}}
        Deprecated option accepted.
        \end{{document}}
        """,
    )
    assert_compiles(result, log_text)
    assert "Unknown option" not in log_text
    assert "deprecated" in log_text
    assert "natbib.sty" not in log_text
    assert "biblatex.sty" not in log_text


def test_bare_package_survives_without_hyperref(tmp_path):
    r"""#48 regression guard.

    \startappendices' fallback branch calls \phantomsection, which is
    hyperref's. While the package loaded hyperref unconditionally that was
    always defined; once it stopped, a bare document hit a fatal undefined
    control sequence rather than merely losing styling.
    """
    result, log_text = compile_latex(
        tmp_path,
        "bare-appendices-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lanepaper}
        \begin{document}
        Body.
        \startappendices
        \section{An appendix}
        Text.
        \finishappendices
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Undefined control sequence" not in log_text


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


def test_subsection_barriers_are_explicitly_reported(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "barrier-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lanepaper}
        \begin{document}
        \section{One}
        \subsection{Two}
        Body text.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert re.search(
        r"Package lanepaper Info: subsection float barriers (enabled|disabled)",
        log_text,
    )


def test_nosubsectionbarriers_reports_disabled_mode(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "no-subsection-barrier-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[nosubsectionbarriers]{lanepaper}
        \begin{document}
        \section{One}
        \subsection{Two}
        Body text.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Package lanepaper Info: subsection float barriers disabled" in log_text


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
    # spec (6pt, +50 tracking) and assert it fits the \@makefntext box.
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
          \SetTracking{encoding={T1,OT1}}{50}\lsstyle\oldstylenums{999}}
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
