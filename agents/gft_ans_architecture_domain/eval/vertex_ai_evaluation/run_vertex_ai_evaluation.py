"""
Vertex AI Evaluation Runner - Production Mode

Comprehensive evaluation runner using Google Cloud's Vertex AI Evaluation Service.
This script provides a complete workflow for evaluating the Architecture Domain ANS
agent with visual dashboards, automated metrics, and centralized storage.

Usage:
    # Full evaluation with all metrics
    python -m eval.run_vertex_ai_evaluation

    # Specific agent version
    python -m eval.run_vertex_ai_evaluation --agent-version v1.0

    # Compare two versions
    python -m eval.run_vertex_ai_evaluation --compare v1.0 v1.1

    # Query historical results
    python -m eval.run_vertex_ai_evaluation --history --limit 10

Requirements:
    - GCP Project with Vertex AI API enabled
    - Service account with permissions:
        - Vertex AI User
        - Storage Admin (for staging bucket)
        - BigQuery Data Editor (for results table)
    - Environment variables:
        - GOOGLE_CLOUD_PROJECT
        - GOOGLE_APPLICATION_CREDENTIALS (optional, uses default)
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add parent directories to path
current_dir = Path(__file__).parent
eval_dir = current_dir.parent
agent_root = eval_dir.parent

sys.path.insert(0, str(agent_root))
sys.path.insert(0, str(current_dir))

from vertex_ai_evaluation import (
    VertexAIEvaluationService,
    VertexAIEvaluationConfig,
    create_custom_metrics
)
from dataset import EVALUATION_DATASET, get_dataset_stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print evaluation banner."""
    print("\n" + "="*80)
    print("🚀 VERTEX AI EVALUATION SERVICE - Architecture Domain ANS Agent")
    print("="*80 + "\n")


def print_section(title: str):
    """Print section header."""
    print(f"\n{'─'*80}")
    print(f"📊 {title}")
    print(f"{'─'*80}\n")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run Vertex AI Evaluation for Architecture Domain ANS Agent"
    )

    # Evaluation mode
    parser.add_argument(
        "--mode",
        choices=["evaluate", "compare", "history"],
        default="evaluate",
        help="Execution mode (default: evaluate)"
    )

    # Evaluation mode
    parser.add_argument(
        "--real",
        action="store_true",
        help="Run REAL agent evaluation (executes test cases). Default is mock mode."
    )

    # Agent configuration
    parser.add_argument(
        "--agent-version",
        default="v1.0",
        help="Agent version identifier (default: v1.0)"
    )

    parser.add_argument(
        "--agent-id",
        help="Full agent ID (overrides agent-version)"
    )

    # Comparison mode
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("VERSION_A", "VERSION_B"),
        help="Compare two agent versions (e.g., --compare v1.0 v1.1)"
    )

    # History mode
    parser.add_argument(
        "--history",
        action="store_true",
        help="Query historical evaluation results"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of historical results to retrieve (default: 10)"
    )

    # GCP configuration
    parser.add_argument(
        "--project",
        default=os.getenv("GOOGLE_CLOUD_PROJECT", "gft-bu-gcp"),
        help="GCP Project ID (default: from GOOGLE_CLOUD_PROJECT env)"
    )

    parser.add_argument(
        "--location",
        default="us-central1",
        help="GCP location for Vertex AI (default: us-central1)"
    )

    parser.add_argument(
        "--staging-bucket",
        help="GCS bucket for staging data (default: {project}-eval-staging)"
    )

    # Metrics configuration
    parser.add_argument(
        "--metrics",
        nargs="+",
        default=[
            "tool_use_quality",
            "response_quality",
            "safety",
            "groundedness",
            "instruction_following"
        ],
        help="List of standard metrics to evaluate"
    )

    parser.add_argument(
        "--skip-custom-metrics",
        action="store_true",
        help="Skip custom ANS-specific metrics"
    )

    # Output configuration
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("eval/results"),
        help="Directory for saving results (default: eval/results)"
    )

    parser.add_argument(
        "--save-dataset",
        action="store_true",
        help="Save prepared dataset locally before upload"
    )

    # Dry run mode
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Prepare dataset but do not run evaluation"
    )

    return parser.parse_args()


async def run_full_evaluation(args):
    """
    Run full evaluation with Vertex AI Evaluation Service.

    Args:
        args: Command-line arguments
    """
    print_banner()

    # Configuration
    config = VertexAIEvaluationConfig(
        project_id=args.project,
        location=args.location,
        staging_bucket=args.staging_bucket
    )

    logger.info(f"Configuration:")
    logger.info(f"  Project: {config.project_id}")
    logger.info(f"  Location: {config.location}")
    logger.info(f"  Staging Bucket: gs://{config.staging_bucket}")
    logger.info(f"  BigQuery Dataset: {config.bigquery_dataset}")

    # Initialize service
    print_section("Initializing Vertex AI Evaluation Service")
    service = VertexAIEvaluationService(config)
    service.initialize()

    # Dataset statistics
    print_section("Evaluation Dataset")
    stats = get_dataset_stats(EVALUATION_DATASET)
    logger.info(f"Total test cases: {stats['total_tests']}")
    logger.info(f"Categories: {json.dumps(stats['categories'], indent=2)}")

    # Prepare dataset
    print_section("Preparing Evaluation Dataset")
    dataset_uri = service.prepare_evaluation_dataset(EVALUATION_DATASET)
    logger.info(f"✅ Dataset uploaded: {dataset_uri}")

    if args.save_dataset:
        # Save local copy
        local_file = args.output_dir / f"eval_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        args.output_dir.mkdir(parents=True, exist_ok=True)
        with open(local_file, "w", encoding="utf-8") as f:
            json.dump(EVALUATION_DATASET, f, indent=2, ensure_ascii=False)
        logger.info(f"📄 Dataset saved locally: {local_file}")

    if args.dry_run:
        logger.info("🏁 Dry run complete - evaluation not executed")
        return

    # Prepare agent ID
    agent_id = args.agent_id or f"architecture-domain-ans-{args.agent_version}"

    # Prepare custom metrics
    custom_metrics = None if args.skip_custom_metrics else create_custom_metrics()

    # Run evaluation
    print_section(f"Running Evaluation - Agent: {agent_id}")
    logger.info(f"Standard Metrics: {', '.join(args.metrics)}")
    if custom_metrics:
        logger.info(f"Custom Metrics: {len(custom_metrics)} ANS-specific metrics")

    logger.info(f"Evaluation Mode: {'REAL (executes test cases)' if args.real else 'MOCK (simulated metrics)'}")

    if args.real:
        logger.info("\n🚀 REAL EVALUATION MODE")
        logger.info("   ✅ Test cases will be executed against live agent")
        logger.info("   ✅ Real metrics will be calculated")
        logger.info("   ⏳ This may take several minutes...")
    else:
        logger.info("\n⏳ MOCK MODE - Simulated metrics will be returned")
        logger.info("   💡 Use --real flag to execute real evaluation")

    logger.info("")

    results = service.run_evaluation(
        agent_id=agent_id,
        dataset_uri=dataset_uri,
        metrics=args.metrics,
        custom_metrics=custom_metrics,
        run_real_evaluation=args.real  # Pass the flag here
    )

    # Display results
    print_section("Evaluation Results")

    # Check if mock mode
    is_mock = results.get("mock_mode", False)
    status = results.get("status")

    if status == "COMPLETED" or status == "MOCK_COMPLETED":
        # Show appropriate status
        if is_mock:
            logger.info("✅ Status: MOCK EVALUATION COMPLETED")
            logger.info("💡 Note: This is a simulated evaluation. Real metrics require Vertex AI API setup.")
        else:
            logger.info("✅ Status: COMPLETED")

        logger.info(f"📊 Dashboard: {results['dashboard_url']}")
        logger.info(f"💾 BigQuery Table: {results['bigquery_table']}")

        if results.get("metrics_summary"):
            logger.info("\n📈 Metrics Summary:")
            for metric, value in results["metrics_summary"].items():
                emoji = "🎯" if value >= 0.85 else "⚠️" if value >= 0.70 else "❌"
                logger.info(f"   {emoji} {metric}: {value:.4f}")

            # Calculate average
            avg_score = sum(results["metrics_summary"].values()) / len(results["metrics_summary"])
            logger.info(f"\n   📊 Average Score: {avg_score:.4f}")

            if avg_score >= 0.85:
                logger.info(f"   ✅ EXCELLENT performance!")
            elif avg_score >= 0.70:
                logger.info(f"   ⚠️ GOOD performance, room for improvement")
            else:
                logger.info(f"   ❌ NEEDS IMPROVEMENT")
    else:
        logger.error(f"❌ Status: {status}")
        if results.get("error"):
            logger.error(f"Error: {results.get('error')}")

    # Save results locally
    print_section("Saving Results")
    output_file = service.save_results_locally(results, args.output_dir)
    logger.info(f"✅ Results saved: {output_file}")

    # Print next steps
    print_section("Next Steps")

    if is_mock:
        logger.info("📊 View Results (MOCK MODE):")
        logger.info("")
        logger.info("1. View data in BigQuery Console:")
        logger.info(f"   {results.get('console_url', 'N/A')}")
        logger.info("")
        logger.info("2. Explore Vertex AI Console:")
        logger.info(f"   {results.get('vertex_ai_url', 'N/A')}")
        logger.info("")
        logger.info("3. Query results from command line:")
        logger.info(f"   bq query --use_legacy_sql=false \\")
        logger.info(f"     'SELECT * FROM `{results.get('bigquery_table', 'N/A')}` \\")
        logger.info(f"      ORDER BY timestamp DESC LIMIT 5'")
    else:
        logger.info("1. Open Vertex AI Console to view detailed dashboard:")
        logger.info(f"   {results.get('dashboard_url', 'N/A')}")
        logger.info("\n2. Query results from BigQuery:")
        logger.info(f"   bq query 'SELECT * FROM `{results.get('bigquery_table', 'N/A')}` LIMIT 10'")
    logger.info("\n3. Compare with previous versions:")
    logger.info(f"   python -m eval.run_vertex_ai_evaluation --compare {args.agent_version} v1.1")

    print("\n" + "="*80)
    logger.info("🎉 Evaluation complete!")
    print("="*80 + "\n")


async def run_comparison(args):
    """
    Compare two agent versions.

    Args:
        args: Command-line arguments
    """
    print_banner()
    print_section(f"Comparing Versions: {args.compare[0]} vs {args.compare[1]}")

    config = VertexAIEvaluationConfig(
        project_id=args.project,
        location=args.location
    )

    service = VertexAIEvaluationService(config)
    service.initialize()

    comparison = service.compare_versions(args.compare[0], args.compare[1])

    if "error" in comparison:
        logger.error(f"❌ Comparison failed: {comparison['error']}")
        return

    # Display comparison
    logger.info(f"\n📊 Comparison Results:")
    logger.info(f"   Version A: {comparison['version_a']}")
    logger.info(f"   Version B: {comparison['version_b']}")
    logger.info(f"\n📈 Metrics Delta:")

    for metric_name, delta_info in comparison["metrics_delta"].items():
        delta = delta_info["delta"]
        pct = delta_info["percentage_change"]
        emoji = "📈" if delta > 0 else "📉" if delta < 0 else "➡️"

        logger.info(
            f"   {emoji} {metric_name}: "
            f"{delta_info['version_a']:.4f} → {delta_info['version_b']:.4f} "
            f"({delta:+.4f}, {pct:+.2f}%)"
        )

    # Save comparison
    output_file = args.output_dir / f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False, default=str)

    logger.info(f"\n✅ Comparison saved: {output_file}")


async def run_history_query(args):
    """
    Query historical evaluation results.

    Args:
        args: Command-line arguments
    """
    print_banner()
    print_section(f"Historical Evaluation Results (Last {args.limit})")

    config = VertexAIEvaluationConfig(
        project_id=args.project,
        location=args.location
    )

    service = VertexAIEvaluationService(config)
    service.initialize()

    results = service.query_historical_results(
        limit=args.limit,
        agent_version=args.agent_version if args.agent_version != "v1.0" else None
    )

    if not results:
        logger.warning("No historical results found")
        return

    logger.info(f"Found {len(results)} evaluation runs:\n")

    for i, result in enumerate(results, 1):
        logger.info(f"{i}. {result.get('display_name', 'N/A')}")
        logger.info(f"   Agent: {result.get('agent_id', 'N/A')}")
        logger.info(f"   Timestamp: {result.get('timestamp', 'N/A')}")
        logger.info(f"   Pass Rate: {result.get('pass_rate', 'N/A')}%")
        logger.info(f"   Evaluation ID: {result.get('evaluation_id', 'N/A')}")
        logger.info("")


async def main():
    """Main entry point."""
    args = parse_arguments()

    try:
        # Determine execution mode
        if args.compare:
            await run_comparison(args)
        elif args.history:
            await run_history_query(args)
        else:
            await run_full_evaluation(args)

    except KeyboardInterrupt:
        logger.info("\n⚠️ Evaluation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Evaluation failed with error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

