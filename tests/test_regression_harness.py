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
