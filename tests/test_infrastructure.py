import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_SOURCE_SUFFIXES = (".tex", ".sty", ".sh", ".py")
ACTIVE_SCAN_ROOTS = ("demo/", "lanepaper/", "src/", "tests/", "Makefile")


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


def test_active_build_inputs_do_not_use_removed_package_names():
    # Two generations of retired names: the pre-2025 path-based layout, and
    # the package names and the four competing macro prefixes retired by the
    # lanepaper rename (#46). Spelling any of them literally here would make
    # this file match its own pattern.
    # Each fragment is built by concatenation so this file never contains a
    # literal that matches its own pattern.
    legacy_path = "paper/" + "paperstyle"
    legacy_file = "paperstyle" + r"\.sty"
    legacy_pkg = r"\b" + "llt" + r"[a-z]+"
    legacy_prefix = r"\\(" + "llt" + r"|paper|paperstyle)@"
    stale_re = re.compile(
        "|".join([legacy_path, legacy_file, legacy_pkg, legacy_prefix])
    )
    offenders = []
    for rel_path, path in tracked_active_source_files():
        if rel_path.startswith(("docs/", "archive/")):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if stale_re.search(text):
            offenders.append(rel_path)
    assert offenders == []


def run_math_spacing_check(body):
    """Run validate_latex_style.sh over a probe .tex and report whether the
    math-operator check fired for it.

    The validator scans `find . -name "*.tex"` from the repo root and ignores
    arguments, so the probe must live inside the checkout. The directory name
    is unique per process so concurrent runs cannot clobber each other, and
    mkdir is exclusive so an unrelated pre-existing path is never destroyed.
    """
    stem = f"mathspacingprobe{os.getpid()}"
    probe_dir = ROOT / f".style-probe-{os.getpid()}"
    probe = probe_dir / f"{stem}.tex"
    probe_dir.mkdir()
    try:
        probe.write_text(body, encoding="utf-8")
        result = subprocess.run(
            ["bash", "src/sh/validate_latex_style.sh"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
    finally:
        probe.unlink(missing_ok=True)
        probe_dir.rmdir()
    output = result.stdout + result.stderr
    assert "invalid character range" not in output, output
    # The validator must not be failing for an unrelated reason, or the
    # substring assertions below would be meaningless.
    assert result.returncode == 0, output
    return f"math operators in {stem}.tex" in output


def test_math_spacing_check_flags_unspaced_operators():
    assert run_math_spacing_check("Inline $x=y+z$ here.\n")


def test_math_spacing_check_flags_operators_inside_brace_groups():
    # A brace group is not an exemption: these are real defects.
    assert run_math_spacing_check(r"Inline $\sqrt{x+y}$ here." + "\n")
    assert run_math_spacing_check(r"Inline ${x=y}$ here." + "\n")


def test_math_spacing_check_ignores_nested_subscripts():
    # Indices nest; the exemption must follow brace depth, not stop at the
    # first closing brace.
    body = (
        r"Inline $x_{\mathrm{i=1}}$ and $x^{\mathrm{n+1}}$ here."
        "\n"
    )
    assert not run_math_spacing_check(body)


def test_math_spacing_check_ignores_unspaced_subscripts():
    # Indices are conventionally unspaced; flagging them is a false positive.
    # Regression guard for the BSD-grep bracket-range fix.
    body = (
        r"Inline $\norm{x}_2 = \sqrt{\sum_{i=1}^n x_i^2}$ and"
        "\n"
        r"$\bar{x} = \frac{1}{n}\sum_{i=1}^n x_i$ here."
        "\n"
    )
    assert not run_math_spacing_check(body)


def test_every_package_sty_carries_an_lppl_header():
    # CTAN review requires a per-file license statement; LICENSE at the repo
    # root is not sufficient. A new module must not be able to skip this.
    required = (
        "LaTeX Project Public License",
        "maintenance status `maintained'",
        "The Current Maintainer of this work is Nathan Lane.",
    )
    sty_files = sorted((ROOT / "lanepaper").glob("*.sty"))
    assert sty_files, "no .sty files found in lanepaper/"
    offenders = []
    for path in sty_files:
        head = path.read_text(encoding="utf-8")[:1200]
        if not all(phrase in head for phrase in required):
            offenders.append(path.name)
    assert offenders == [], f"missing or incomplete LPPL header: {offenders}"
