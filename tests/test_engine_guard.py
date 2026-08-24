"""The package is pdfLaTeX-only and must say so in one message (issue #54).

Two levels of assertion. The static tests pin the guard's presence and shape so
it cannot be dropped by a refactor. The functional tests actually run XeLaTeX
and LuaLaTeX, because the thing worth protecting is not that the source
contains a guard but that a wrong-engine run stops on one legible line instead
of the font cascade underneath it.
"""

import os
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]

# The two surfaces a user is told to load. README calls them "distinct
# surfaces": lnpminimal is not reached through lanepaper.sty, so guarding only
# the main package would leave it exposed. Every other .sty is internal.
ENTRY_POINTS = ("lanepaper", "lnpminimal")

OTHER_ENGINES = ("xelatex", "lualatex")


def _source(package):
    return (ROOT / "lanepaper" / f"{package}.sty").read_text(encoding="utf-8")


@pytest.mark.parametrize("package", ENTRY_POINTS)
def test_entry_point_declares_the_engine_guard(package):
    source = _source(package)
    assert "\\RequirePackage{iftex}" in source
    assert "\\ifpdftex\\else" in source
    # \PackageError is what names the package. iftex's own \RequirePDFTeX
    # prints "pdfTeX is required to compile this document" without saying
    # which package wanted it, which is the whole point of the message.
    assert f"\\PackageError{{{package}}}" in source


def test_main_package_declares_the_format():
    assert "\\NeedsTeXFormat{LaTeX2e}" in _source("lanepaper")


def _run(engine, tmp_path, package):
    tex = tmp_path / "guard.tex"
    tex.write_text(
        textwrap.dedent(
            rf"""
            \documentclass[11pt]{{article}}
            \usepackage{{{package}}}
            \begin{{document}}
            ok
            \end{{document}}
            """
        ),
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["TEXINPUTS"] = f".:{ROOT / 'lanepaper'}:{env.get('TEXINPUTS', '')}"
    subprocess.run(
        [engine, "-interaction=nonstopmode", tex.name],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    return (tmp_path / "guard.log").read_text(encoding="utf-8", errors="ignore")


@pytest.mark.parametrize("engine", OTHER_ENGINES)
@pytest.mark.parametrize("package", ENTRY_POINTS)
def test_non_pdftex_engines_fail_with_one_message(engine, tmp_path, package):
    if shutil.which(engine) is None:
        pytest.skip(f"{engine} not installed")
    log_text = _run(engine, tmp_path, package)
    errors = [line for line in log_text.splitlines() if line.startswith("! ")]
    # Exactly one: the guard stops the run. Without the stop the error is
    # recoverable and microtype alone contributes two more on XeTeX.
    assert len(errors) == 1, f"expected one error, got {errors}"
    assert f"Package {package} Error" in errors[0]
    assert "pdfTeX is required" in errors[0]


@pytest.mark.parametrize("package", ENTRY_POINTS)
def test_pdflatex_is_unaffected_by_the_guard(tmp_path, package):
    log_text = _run("pdflatex", tmp_path, package)
    errors = [line for line in log_text.splitlines() if line.startswith("! ")]
    assert errors == []
    assert (tmp_path / "guard.pdf").exists()
