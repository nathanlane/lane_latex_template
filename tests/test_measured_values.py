"""Measured-value regression tests.

These assert the *measured* build values, not the comments — the failure mode
of the adopter defect report (archived in git history as
the adopter defect report of 2026-08-11, in git history), where comments claimed 13.2pt
and the build shipped 16.32pt. If the template
ever makes the 13.2pt grid real (decision (a)), update these expectations
deliberately; they encode decision (b) in
docs/adr/0004-baseline-grid-is-a-spacing-quantum.md.
"""

import re

from test_option_contracts import assert_compiles, compile_latex


def measure(tmp_path, name, probes, preamble_option=""):
    """Compile a fixture that typeouts the requested register values."""
    lines = "\n".join(f"\\typeout{{LNP_MEASURE-{label}={cmd}}}" for label, cmd in probes)
    result, log_text = compile_latex(
        tmp_path,
        name,
        r"""
        \documentclass[11pt]{article}
        \usepackage%s{lanepaper}
        \begin{document}
        %s
        Text.
        \end{document}
        """
        % (preamble_option, lines),
    )
    assert_compiles(result, log_text)
    out = {}
    for label, _ in probes:
        match = re.search(rf"LNP_MEASURE-{label}=([^\s]+)", log_text)
        assert match, f"probe {label} missing from log"
        out[label] = match.group(1)
    return out


def pt(value):
    return float(value.replace("pt", ""))


def test_measured_baseline_and_body_size(tmp_path):
    values = measure(
        tmp_path,
        "measure-baseline",
        [
            ("BASELINESKIP", r"\the\baselineskip"),
            ("GRIDUNIT", r"\the\gridunit"),
        ],
    )
    # size11.clo sets 10.95pt on 13.6pt; \linespread{1.20} scales the 13.6pt.
    assert abs(pt(values["BASELINESKIP"]) - 16.31996) < 0.01
    assert abs(pt(values["GRIDUNIT"]) - 13.2) < 0.001


def test_measured_jot_is_9pt9(tmp_path):
    values = measure(tmp_path, "measure-jot", [("JOT", r"\the\jot")])
    # 6.6pt base + unconditional 0.25\gridunit AtBeginDocument addition.
    assert abs(pt(values["JOT"]) - 9.9) < 0.01


def test_measured_footnotesep_below_strut_floor(tmp_path):
    # \footnotesep is a floor on each note's first-line height, not inter-note
    # space; it is deliberately documented as inert (below the ~8.4pt strut).
    result, log_text = compile_latex(
        tmp_path,
        "measure-footnotesep",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lanepaper}
        \begin{document}
        Text.\footnote{%
          \typeout{LNP_MEASURE-FNSEP=\the\footnotesep}
          \typeout{LNP_MEASURE-FNSKIP=\the\baselineskip}
          A note.}
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    fnsep = pt(re.search(r"LNP_MEASURE-FNSEP=([0-9.]+)pt", log_text).group(1))
    fnskip = pt(re.search(r"LNP_MEASURE-FNSKIP=([0-9.]+)pt", log_text).group(1))
    assert abs(fnsep - 3.3) < 0.01
    assert abs(fnskip - 12.0) < 0.01
    assert fnsep < 8.4  # inert: below the footnote strut


def test_measured_penalties_are_canonical(tmp_path):
    values = measure(
        tmp_path,
        "measure-penalties",
        [
            ("CLUB", r"\the\clubpenalty"),
            ("WIDOW", r"\the\widowpenalty"),
            ("DISPWIDOW", r"\the\displaywidowpenalty"),
            ("BROKEN", r"\the\brokenpenalty"),
            ("POSTDISP", r"\the\postdisplaypenalty"),
        ],
    )
    assert values["CLUB"] == "10000"
    assert values["WIDOW"] == "10000"
    assert values["DISPWIDOW"] == "10000"
    assert values["BROKEN"] == "2000"
    assert values["POSTDISP"] == "2000"


def test_measured_scriptscript_size_fires(tmp_path):
    # \DeclareMathSizes is keyed to 10.95pt; before the fix it never fired and
    # scriptscript shipped as 6.1pt instead of the declared 6pt.
    result, log_text = compile_latex(
        tmp_path,
        "measure-mathsizes",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lanepaper}
        \begin{document}
        $a_{b_{c}}$
        \makeatletter
        \typeout{LNP_MEASURE-SSFONT=\the\scriptscriptfont0}
        \makeatother
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    match = re.search(r"LNP_MEASURE-SSFONT=.*n/(\d+(?:\.\d+)?)", log_text)
    assert match, log_text
    assert abs(float(match.group(1)) - 6.0) < 0.001
