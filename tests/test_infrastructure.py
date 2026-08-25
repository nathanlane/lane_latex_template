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


def test_makefile_exposes_one_target_per_job():
    """Issue #51: the aliases were deleted, not turned into forwarders.

    Four targets used to run the tests and nobody could tell which one CI
    used. The set is asserted exactly, so a convenience alias cannot creep
    back in unnoticed -- adding a genuinely new job means updating this list
    on purpose.
    """
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    declared = set(re.findall(r"^\.PHONY:\s*(\S+)", makefile, re.MULTILINE))
    assert declared == {
        "build",
        "lint",
        "test",
        "clean",
        "check-deps",
        "watch",
        "install",
        "uninstall",
        "ctan",
        "release",
        "help",
    }
    # AGENTS.md gates these two by name.
    for target in ("build", "lint"):
        assert re.search(rf"^{target}:", makefile, re.MULTILINE), target


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
    # the package names and the five competing macro prefixes retired by the
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


def test_package_uses_the_latex2e_hook_system_not_atbegindocument():
    """#56: hooks, not \\AtBeginDocument.

    \\AtBeginDocument runs its callbacks in registration order, which made
    precedence an accident of file layout. That bit once for real: deferring the
    cleveref block in #48 inverted a \\crefname precedence that had held for a
    year, and only raster comparison caught it. Package hooks remove the class
    of bug -- they fire when the package loads, in either order, and never fire
    if it is absent.
    """
    offenders = []
    for path in sorted((ROOT / "lanepaper").glob("*.sty")):
        for number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            stripped = line.lstrip()
            if stripped.startswith("%"):
                continue
            if "\\AtBegin" + "Document{" in stripped:
                offenders.append(f"{path.name}:{number}")
    assert offenders == [], (
        "use \\AddToHook{begindocument} or a package hook instead: " f"{offenders}"
    )


def test_configure_if_loaded_uses_package_hooks():
    """The five configure-if-loaded packages are wired to their load hooks.

    A package hook fires whether the document loads the package before or after
    this one, and not at all when it is absent -- which is exactly the
    configure-if-loaded contract from ADR-0003.
    """
    source = (ROOT / "lanepaper" / "lanepaper.sty").read_text(encoding="utf-8")
    for package in ("hyperref", "cleveref", "longtable", "appendix", "biblatex"):
        assert f"\\AddToHook{{package/{package}/after}}" in source, package


def test_entry_points_require_a_format_new_enough_for_hooks():
    """\\AddToHook is format-native from 2020-10-01; the floor must say so."""
    for name in ("lanepaper", "lnpminimal"):
        source = (ROOT / "lanepaper" / f"{name}.sty").read_text(encoding="utf-8")
        assert "\\NeedsTeXFormat{LaTeX2e}[2020/10/01]" in source, name


def test_build_lua_declares_no_test_files():
    """ADR-0002: l3build packages, pytest tests. Nothing declares test files.

    This is the one part of build.lua that is easy to undo by accident -- an
    l3build default, or a copied config, quietly reintroduces log-diffing and
    the `ctan` target starts gating releases on `.tlg` files that do not exist.
    """
    source = (ROOT / "build.lua").read_text(encoding="utf-8")
    for name in ("checkfiles", "checkengines", "typesetfiles", "unpackfiles"):
        assert re.search(rf"^{name}\s*=\s*\{{\s*\}}\s*$", source, re.M), name


def test_build_lua_stamps_versions_where_the_package_keeps_them():
    """`l3build tag` is only useful if it rewrites the real version strings.

    Every version in the package lives in a \\ProvidesPackage optional
    argument and nowhere else, so tagfiles must reach the .sty files and
    update_tag must target that macro.
    """
    source = (ROOT / "build.lua").read_text(encoding="utf-8")
    assert re.search(r"^tagfiles\s*=\s*\{\"\*\.sty\"\}", source, re.M)
    assert "\\\\ProvidesPackage" in source


def test_every_relative_markdown_link_resolves():
    """Issue #52: consolidation deletes documents other documents link to.

    `CHANGELOG.md` is exempt because its entries are a historical record --
    several point at files that have since been deleted, and rewriting past
    entries to keep the links green would falsify the record. `docs/handoff/`
    and `docs/archive/` are working and historical material, not published
    documentation.

    Link targets inside code fences and inline code are skipped: LaTeX like
    `\\mathcal{L}[f](s)` reads as a markdown link otherwise.
    """
    link = re.compile(r"\[[^\]]*\]\(([^)\s#]+)(?:#[^)]*)?\)")
    fence = re.compile(r"^\s*(```|~~~)")
    broken = []
    for rel in run_git(["ls-files", "*.md"]).stdout.split():
        if rel == "CHANGELOG.md" or rel.startswith(("docs/handoff/", "docs/archive/")):
            continue
        path = ROOT / rel
        in_fence = False
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if fence.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for target in link.findall(re.sub(r"`[^`]*`", "", line)):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                if not (path.parent / target).resolve().exists():
                    broken.append(f"{rel}:{number} -> {target}")
    assert broken == []
