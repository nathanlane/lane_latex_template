import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_SOURCE_SUFFIXES = (".tex", ".sty", ".sh", ".py")
ACTIVE_SCAN_ROOTS = ("main.tex", "appendices/", "paper/", "src/", "tests/", "Makefile")


def run_git(args):
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def tracked_active_source_files():
    result = run_git(["ls-files"])
    for rel_path in result.stdout.splitlines():
        path = ROOT / rel_path
        if rel_path.startswith(("archive/", "docs/archive/")):
            continue
        if rel_path == "Makefile" or rel_path.endswith(ACTIVE_SOURCE_SUFFIXES):
            yield rel_path, path


def test_no_unresolved_merge_markers_in_active_sources():
    marker_re = re.compile(r"^(<{7}|={7}|>{7})", re.MULTILINE)
    offenders = []
    for rel_path, path in tracked_active_source_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if marker_re.search(text):
            offenders.append(rel_path)
    assert offenders == []


def test_makefile_exposes_agents_targets():
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    for target in ("build", "lint", "fmt"):
        assert re.search(rf"^\.PHONY:.*\b{target}\b", makefile, re.MULTILINE)
        assert re.search(rf"^{target}:", makefile, re.MULTILINE)


def test_required_shell_harnesses_are_executable():
    rel_paths = [
        "src/sh/validate_latex_style.sh",
        "tests/run-tests.sh",
        "tests/test-bibliography.sh",
        "tests/check-spacing-integrity.sh",
    ]
    non_executable = [
        rel_path
        for rel_path in rel_paths
        if not os.access(ROOT / rel_path, os.X_OK)
    ]
    assert non_executable == []


def test_root_changelog_exists():
    assert (ROOT / "CHANGELOG.md").is_file()


def test_active_build_inputs_do_not_use_removed_paperstyle_package():
    legacy_path = "paper/" + "paperstyle"
    legacy_file = r"(?<!llt)" + "paperstyle" + r"\.sty"
    stale_re = re.compile(rf"{legacy_path}|{legacy_file}")
    offenders = []
    for rel_path, path in tracked_active_source_files():
        if rel_path.startswith(("docs/", "archive/")):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if stale_re.search(text):
            offenders.append(rel_path)
    assert offenders == []
