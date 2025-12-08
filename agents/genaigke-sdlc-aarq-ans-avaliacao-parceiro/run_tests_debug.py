#!/usr/bin/env python
"""Script para executar testes e gerar relatório."""

import subprocess
import sys
from pathlib import Path

def run_tests():
    """Execute tests and return results."""
    test_dir = Path(__file__).parent / "testes" / "unit_tests"

    print("=" * 80)
    print("EXECUTANDO SUITE DE TESTES")
    print("=" * 80)
    print(f"Diretório de testes: {test_dir}")
    print()

    # Execute pytest
    cmd = [
        sys.executable, "-m", "pytest",
        str(test_dir),
        "-v",
        "--tb=short",
        "--co"  # Collect only first to see if tests are found
    ]

    print(f"Comando: {' '.join(cmd)}")
    print()

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    print("STDOUT:")
    print(result.stdout)
    print()
    print("STDERR:")
    print(result.stderr)
    print()
    print(f"Return code: {result.returncode}")

    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)

