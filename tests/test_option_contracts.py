import os
import re
import subprocess
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def compile_latex(tmp_path, name, source):
    tex_file = tmp_path / f"{name}.tex"
    tex_file.write_text(textwrap.dedent(source), encoding="utf-8")
    env = os.environ.copy()
    env["TEXINPUTS"] = (
        f".:{ROOT / 'paper'}:{ROOT / 'paper/modules'}:"
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
        \usepackage[nocolor]{lltpaperstyle}
        \makeatletter
        \newcommand{\showcolorhex}[2]{%
          \convertcolorspec{named}{#1}{HTML}{#2}%
        }
        \makeatother
        \begin{document}
        \showcolorhex{sectioncolor}{\lltsectionhex}
        \showcolorhex{linknavy}{\lltlinkhex}
        \typeout{LLT_SECTION_HEX=\lltsectionhex}
        \typeout{LLT_LINK_HEX=\lltlinkhex}
        \section{No Color}
        Body text.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "LLT_SECTION_HEX=000000" in log_text
    assert "LLT_LINK_HEX=000000" in log_text


def test_minimal_nocolor_compiles(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "minimal-nocolor-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[minimal,nocolor]{lltpaperstyle}
        \begin{document}
        \typeout{LLT_MINIMAL_NOCOLOR_OK}
        Minimal no-color contract.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "LLT_MINIMAL_NOCOLOR_OK" in log_text


def test_draft_option_reports_microtype_draft_mode(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "draft-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[draft]{lltpaperstyle}
        \begin{document}
        Draft mode contract.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert re.search(
        r"Package llt(paperstyle|microtype) Info: microtype draft mode active",
        log_text,
    )


def test_natbib_option_provides_native_natbib_commands(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "natbib-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[natbib]{lltpaperstyle}
        \begin{document}
        Natbib cite commands compile:
        \citet[chap.~2]{smith2020} and \citep[see][45]{smith2020}.
        \begin{thebibliography}{9}
        \bibitem[Smith(2020)]{smith2020} Smith, A. 2020. Title.
        \end{thebibliography}
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Undefined control sequence" not in log_text


def test_nobiblatex_does_not_load_biblatex(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "nobiblatex-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[nobiblatex]{lltpaperstyle}
        \begin{document}
        No automatic bibliography package.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "biblatex.sty" not in log_text


def test_text_symbol_commands_compile_in_t1_encoding(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "text-symbol-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lltpaperstyle}
        \begin{document}
        The value is \textapprox 3.14159.
        The limit approaches \textinfty.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Command \\textapprox unavailable in encoding T1" not in log_text
    assert "Command \\textinfty unavailable in encoding T1" not in log_text


def test_plain_ref_does_not_emit_package_warning(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "plain-ref-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lltpaperstyle}
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
        \usepackage{lltpaperstyle}
        \begin{document}
        \section{One}
        \subsection{Two}
        Body text.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert re.search(
        r"Package lltpaperstyle Info: subsection float barriers (enabled|disabled)",
        log_text,
    )


def test_nosubsectionbarriers_reports_disabled_mode(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "no-subsection-barrier-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[nosubsectionbarriers]{lltpaperstyle}
        \begin{document}
        \section{One}
        \subsection{Two}
        Body text.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Package lltpaperstyle Info: subsection float barriers disabled" in log_text
