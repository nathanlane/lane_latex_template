import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def test_minimal_fixture_regression_harness_passes():
    result = subprocess.run(
        ["bash", "tests/run-tests.sh", "tests/fixtures/minimal-root.tex"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_compatibility_backports_fixture_passes():
    result = subprocess.run(
        ["bash", "tests/run-tests.sh", "tests/fixtures/compatibility-backports.tex"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    if shutil.which("pdftotext") is None:
        pytest.skip("pdftotext is required for PDF text regression assertions")

    pdf_text = subprocess.run(
        ["pdftotext", "tests/visual/output/compatibility-backports.pdf", "-"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout
    assert "Optional mark footnote text." in pdf_text
    assert "Long Appendix Title" in pdf_text
    assert "7]Optional" not in pdf_text
    assert "A *" not in pdf_text
    assert "B [" not in pdf_text
    assert "Short Appendix]Long Appendix" not in pdf_text
