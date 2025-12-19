import subprocess
from pathlib import Path


def run_bash_n(path: Path):
    """Run `bash -n` (syntax check) on a file. Raises CalledProcessError on failure."""
    subprocess.run(["bash", "-n", str(path)], check=True)


def test_plugins_readme_exists():
    p = Path("plugins/README.md")
    assert p.exists() and p.is_file(), "plugins/README.md is missing"


def test_scorch_and_obrar_syntax():
    # Check core scripts exist and have valid bash syntax. Skip missing ones.
    for name in ("scorch", "obrar"):
        p = Path(name)
        if p.exists():
            run_bash_n(p)


def test_scorch_version_invokable():
    p = Path("scorch")
    if not p.exists():
        return
    # `scorch -v` should exit 0 and print program/version
    completed = subprocess.run(["./scorch", "-v"], capture_output=True, text=True)
    assert completed.returncode == 0
    assert "scorch" in completed.stdout.lower() or "scorch" in completed.stderr.lower()
