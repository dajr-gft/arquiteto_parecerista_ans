# -*- coding: utf-8 -*-
"""
Evaluation Runner for Architecture Domain ANS Agent

This script runs comprehensive evaluations of the agent using the ADK framework.
Based on: https://google.github.io/adk-docs/evaluate/
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

import vertexai
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

# Add parent directories to path to allow imports
current_dir = Path(__file__).parent
eval_dir = current_dir.parent
agent_root = eval_dir.parent

sys.path.insert(0, str(agent_root))
sys.path.insert(0, str(eval_dir))

from architecture_domain_ans.agent import root_agent
from dataset import EVALUATION_DATASET, get_dataset_stats
from metrics import evaluate_all_metrics

# Load environment variables
load_dotenv()


class AgentEvaluator:
    """Evaluator for the Architecture Domain ANS Agent."""

    def __init__(self, project_id: str, location: str = "global"):
        """
        Initialize the evaluator.

        Args:
            project_id: GCP project ID
            location: GCP location
        """
        self.project_id = project_id
        self.location = location
        self.runner = None
        self.results = []

        # Configure UTF-8 encoding for console
        self._configure_console_encoding()

    def _configure_console_encoding(self):
        """Configure console to use UTF-8 encoding."""
        import sys
        import io

        # Force UTF-8 encoding for Windows console
        if sys.platform == 'win32':
            # Set console code page to UTF-8 (65001)
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleCP(65001)
                kernel32.SetConsoleOutputCP(65001)
            except:
                pass

        # Reconfigure stdout/stderr with UTF-8
        try:
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            else:
                # Python < 3.7 fallback
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

            if hasattr(sys.stderr, 'reconfigure'):
                sys.stderr.reconfigure(encoding='utf-8', errors='replace')
            else:
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except Exception as e:
            # Silently fail if reconfiguration not possible
            pass

    async def initialize(self):
        """Initialize Vertex AI and agent runner."""
        print(f"Initializing Vertex AI (Project: {self.project_id}, Location: {self.location})...")
        vertexai.init(project=self.project_id, location=self.location)
        self.runner = InMemoryRunner(agent=root_agent)
        print("✅ Initialization complete\n")

    def format_payload(self, test_input: Dict[str, Any]) -> str:
        """Format test input as agent query."""
        return f"""
Processar solicitação de parecer de arquitetura:

{json.dumps(test_input, ensure_ascii=False, indent=2)}
"""

    async def run_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single test case.

        Args:
            test_case: Test case from dataset

        Returns:
            Test result with metrics
        """
        test_id = test_case["test_id"]
        scenario = test_case["scenario"]

        print(f"📝 Running {test_id}: {scenario}")
        print(f"   Category: {test_case['category']}")

        start_time = datetime.now()

        try:
            # Prepare query
            query = self.format_payload(test_case["input"])

            # Create session
            session = await self.runner.session_service.create_session(
                app_name=self.runner.app_name,
                user_id=f"eval_{test_id}"
            )

            # Prepare content
            content = UserContent(parts=[Part(text=query)])

            # Run agent
            response_parts = []
            async for event in self.runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=content,
            ):
                if event.content.parts and event.content.parts[0].text:
                    response_parts.append(event.content.parts[0].text)

            # Combine response
            full_response = "\n".join(response_parts)

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()

            # Evaluate metrics
            metrics_result = evaluate_all_metrics(
                expected=test_case["expected_output"],
                actual=full_response
            )

            # Build result
            result = {
                "test_id": test_id,
                "scenario": scenario,
                "category": test_case["category"],
                "status": "PASS" if metrics_result["average_score"] >= 0.7 else "FAIL",
                "execution_time_seconds": execution_time,
                "metrics": metrics_result,
                "response": full_response,
                "timestamp": datetime.now().isoformat()
            }

            print(f"   ✅ Status: {result['status']}")
            print(f"   📊 Average Score: {metrics_result['average_score']:.2f}")
            print(f"   ⏱️  Time: {execution_time:.2f}s\n")

            return result

        except Exception as e:
            print(f"   ❌ Error: {str(e)}\n")
            return {
                "test_id": test_id,
                "scenario": scenario,
                "category": test_case["category"],
                "status": "ERROR",
                "error": str(e),
                "execution_time_seconds": (datetime.now() - start_time).total_seconds(),
                "timestamp": datetime.now().isoformat()
            }

    async def run_all_tests(self, test_ids: List[str] = None) -> List[Dict[str, Any]]:
        """
        Run all test cases or specific ones.

        Args:
            test_ids: Optional list of test IDs to run (e.g., ["TC-001", "TC-002"])

        Returns:
            List of test results
        """
        # Filter tests if specific IDs provided
        tests_to_run = EVALUATION_DATASET
        if test_ids:
            tests_to_run = [tc for tc in EVALUATION_DATASET if tc["test_id"] in test_ids]

        print(f"🚀 Starting evaluation of {len(tests_to_run)} test(s)...\n")

        self.results = []
        for test_case in tests_to_run:
            result = await self.run_test_case(test_case)
            self.results.append(result)

        return self.results

    def generate_report(self) -> Dict[str, Any]:
        """
        Generate evaluation report.

        Returns:
            Dictionary with report data
        """
        if not self.results:
            return {"error": "No results to report"}

        # Calculate statistics
        total_tests = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        errors = sum(1 for r in self.results if r["status"] == "ERROR")

        # Calculate average metrics
        metric_scores = {}
        for result in self.results:
            if "metrics" in result:
                for metric_name, metric_data in result["metrics"]["metrics"].items():
                    if metric_name not in metric_scores:
                        metric_scores[metric_name] = []
                    metric_scores[metric_name].append(metric_data["score"])

        average_metrics = {
            name: sum(scores) / len(scores) if scores else 0.0
            for name, scores in metric_scores.items()
        }

        # Calculate average execution time
        avg_time = sum(r["execution_time_seconds"] for r in self.results) / total_tests

        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "pass_rate": f"{(passed / total_tests * 100):.1f}%",
                "average_execution_time_seconds": f"{avg_time:.2f}"
            },
            "metric_averages": {
                name: f"{score:.2%}"
                for name, score in average_metrics.items()
            },
            "test_results": [
                {
                    "test_id": r["test_id"],
                    "scenario": r["scenario"],
                    "status": r["status"],
                    "average_score": r.get("metrics", {}).get("average_score", 0.0)
                }
                for r in self.results
            ],
            "timestamp": datetime.now().isoformat()
        }

        return report

    def save_results(self, output_dir: str = "eval/results"):
        """
        Save evaluation results to files.

        Args:
            output_dir: Directory to save results
        """
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save detailed results
        results_file = output_path / f"evaluation_results_{timestamp}.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        # Save report
        report = self.generate_report()
        report_file = output_path / f"evaluation_report_{timestamp}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Results saved:")
        print(f"   📄 {results_file}")
        print(f"   📊 {report_file}")

        return results_file, report_file

    def print_report(self):
        """Print evaluation report to console."""
        report = self.generate_report()

        print("\n" + "=" * 80)
        print("📊 EVALUATION REPORT")
        print("=" * 80)

        print("\n📋 Summary:")
        for key, value in report["summary"].items():
            print(f"   {key}: {value}")

        print("\n📈 Metric Averages:")
        for metric, score in report["metric_averages"].items():
            print(f"   {metric}: {score}")

        print("\n✅ Test Results:")
        for test in report["test_results"]:
            status_icon = "✅" if test["status"] == "PASS" else "❌" if test["status"] == "FAIL" else "⚠️"
            print(f"   {status_icon} {test['test_id']}: {test['scenario']} (Score: {test['average_score']:.2f})")

        print("\n" + "=" * 80)


async def main():
    """Main evaluation function."""
    # Get configuration from environment
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "gft-bu-gcp")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")

    # Print dataset stats
    stats = get_dataset_stats()
    print("📊 Evaluation Dataset Statistics:")
    print(f"   Total tests: {stats['total_tests']}")
    print(f"   Categories: {stats['categories']}")
    print()

    # Initialize evaluator
    evaluator = AgentEvaluator(project_id=project_id, location=location)
    await evaluator.initialize()

    # Run tests
    # You can specify test IDs to run specific tests:
    # await evaluator.run_all_tests(test_ids=["TC-001", "TC-002"])
    await evaluator.run_all_tests()

    # Print and save results
    evaluator.print_report()
    evaluator.save_results()


if __name__ == "__main__":
    asyncio.run(main())

