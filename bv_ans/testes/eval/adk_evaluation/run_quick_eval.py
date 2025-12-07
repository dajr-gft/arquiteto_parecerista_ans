"""
Quick Evaluation Runner for BV ANS Architecture Review Agent

This script runs a quick evaluation with a subset of test cases.
Useful for rapid testing during development.
"""

import asyncio
import os
import sys
import io
from pathlib import Path
from dotenv import load_dotenv

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleCP(65001)
        kernel32.SetConsoleOutputCP(65001)
    except:
        pass

# Reconfigure stdout to UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from run_evaluation import AgentEvaluator
from dataset import get_dataset_stats

# Load environment variables
bv_ans_root = current_dir.parent.parent.parent
env_path = bv_ans_root / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()


async def main():
    """Main quick evaluation function."""
    # Get configuration from environment
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "gft-bu-gcp")
    location = "global"  # Using global region for gemini-3-pro-preview

    print("="*80)
    print("🚀 BV ANS Agent - Quick Evaluation")
    print("="*80)

    # Print dataset stats
    stats = get_dataset_stats()
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total tests available: {stats['total_tests']}")
    print(f"   Categories: {list(stats['categories'].keys())}")
    print()

    # Quick test selection (representative sample)
    quick_tests = [
        "TC-DOC-001",      # Document analysis - technical spec
        "TC-DOC-002",      # Document analysis - vendor proposal
        "TC-SHEET-001",    # Spreadsheet - requirements matrix
        "TC-CONTRACT-001", # Contract extraction
        "TC-OPINION-001",  # Quick opinion
        "TC-STATUS-001",   # Status check
        "TC-ERROR-001",    # Error handling
    ]

    print(f"📝 Running {len(quick_tests)} quick tests:")
    for test_id in quick_tests:
        print(f"   - {test_id}")
    print()

    # Initialize evaluator
    evaluator = AgentEvaluator(project_id=project_id, location=location)
    await evaluator.initialize()

    # Run selected tests
    await evaluator.run_all_tests(test_ids=quick_tests)

    # Print results
    evaluator.print_report()

    # Optionally save results
    save_results = os.getenv("SAVE_QUICK_EVAL_RESULTS", "true").lower() == "true"
    if save_results:
        evaluator.save_results(output_dir="results/quick")
        print("\n💾 Results saved to: bv_ans/testes/eval/adk_evaluation/results/quick/")

    print("\n✅ Quick evaluation complete!\n")


if __name__ == "__main__":
    asyncio.run(main())

