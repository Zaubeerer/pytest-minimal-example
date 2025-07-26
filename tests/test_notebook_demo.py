"""
Test file demonstrating how to test Jupyter notebooks using pytest-nbval.

This file shows different ways to run pytest-nbval tests on our sum_function_demo.ipynb notebook.
"""

import subprocess
import sys
from pathlib import Path


def test_notebook_with_nbval():
    """
    Test that demonstrates running pytest-nbval on our notebook.

    This test runs pytest-nbval on the sum_function_demo.ipynb notebook
    and ensures all cells execute successfully with expected outputs.
    """
    notebook_path = Path(__file__).parent.parent / "sum_function_demo.ipynb"

    # Run pytest-nbval on the notebook
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--nbval", str(notebook_path)],
        capture_output=True,
        text=True,
    )

    # Check that the test passed
    assert result.returncode == 0, (
        f"Notebook test failed:\n{result.stdout}\n{result.stderr}"
    )

    # Verify that tests were actually run
    assert "passed" in result.stdout
    assert str(notebook_path.name) in result.stdout


def test_notebook_with_nbval_ignore_output():
    """
    Test that demonstrates running pytest-nbval with --nbval-lax option.

    The --nbval-lax option only checks that cells execute without error,
    but ignores output differences. This is useful for notebooks with
    non-deterministic outputs.
    """
    notebook_path = Path(__file__).parent.parent / "sum_function_demo.ipynb"

    # Run pytest-nbval with lax checking
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--nbval-lax", str(notebook_path)],
        capture_output=True,
        text=True,
    )

    # Check that the test passed
    assert result.returncode == 0, (
        f"Notebook lax test failed:\n{result.stdout}\n{result.stderr}"
    )


if __name__ == "__main__":
    # This allows running the test directly
    test_notebook_with_nbval()
    test_notebook_with_nbval_ignore_output()
    print("All notebook tests passed!")
