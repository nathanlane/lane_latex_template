import subprocess
from pathlib import Path

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


def test_manual_biblatex_contract_passes():
    result = subprocess.run(
        ["bash", "tests/test-bibliography.sh", "tests/fixtures/biblatex-manual-contract.tex"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_run_tests_includes_compatibility_probes():
    result = subprocess.run(
        ["bash", "tests/run-tests.sh", "tests/fixtures/minimal-root.tex"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=240,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "compatibility probes" in result.stdout.lower()
