"""
Quick Evaluation Runner for Architecture Domain ANS Agent

This script runs a quick evaluation with a subset of test cases.
Useful for rapid testing during development.
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from run_evaluation import AgentEvaluator
from dataset import get_dataset_stats

# Load environment variables
load_dotenv()


async def main():
    """Main quick evaluation function."""
    # Get configuration from environment
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "gft-bu-gcp")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")

    print("🚀 Quick Evaluation - Architecture Domain ANS Agent\n")

    # Print dataset stats
    stats = get_dataset_stats()
    print("📊 Dataset Statistics:")
    print(f"   Total tests available: {stats['total_tests']}")
    print(f"   Categories: {list(stats['categories'].keys())}")
    print()

    # Quick test selection (first test of each critical category)
    quick_tests = [
        "TC-001",  # Renovação com histórico
        "TC-002",  # Nova contratação com ressalvas
        "TC-005",  # Bloqueio crítico
    ]

    print(f"📝 Running {len(quick_tests)} quick tests: {quick_tests}\n")

    # Initialize evaluator
    evaluator = AgentEvaluator(project_id=project_id, location=location)
    await evaluator.initialize()

    # Run selected tests
    await evaluator.run_all_tests(test_ids=quick_tests)

    # Print results
    evaluator.print_report()

    # Optionally save results
    save_results = os.getenv("SAVE_QUICK_EVAL_RESULTS", "false").lower() == "true"
    if save_results:
        evaluator.save_results(output_dir="eval/results/quick")


if __name__ == "__main__":
    asyncio.run(main())

