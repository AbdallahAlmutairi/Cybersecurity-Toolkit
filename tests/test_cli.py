import subprocess
import sys


def test_help():
    result = subprocess.run(
        [sys.executable, "-m", "cybertool.cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "scan-ports" in result.stdout
