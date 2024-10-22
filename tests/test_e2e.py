import pytest
import subprocess
import os

EXAMPLES_DIR = "examples/basic"

@pytest.mark.parametrize("script", [
    "bridge_example.py",
    "example.py",
    "originate_example.py",
    "playback_example.py"
])
def test_example_scripts(script):
    script_path = os.path.join(EXAMPLES_DIR, script)
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script} failed with return code {result.returncode}"
    assert "ERROR" not in result.stderr, f"Script {script} produced errors: {result.stderr}"
    assert "Traceback" not in result.stderr, f"Script {script} produced a traceback: {result.stderr}"
