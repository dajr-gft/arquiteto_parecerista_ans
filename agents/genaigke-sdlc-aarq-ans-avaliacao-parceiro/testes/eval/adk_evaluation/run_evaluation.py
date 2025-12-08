# -*- coding: utf-8 -*-
"""
Evaluation Runner for BV ANS Architecture Review Agent

This script runs comprehensive evaluations of the agent using the ADK framework.
Based on: https://google.github.io/adk-docs/evaluate/
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

import vertexai
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types
from google.genai.types import Part

# Add parent directories to path to allow imports
current_dir = Path(__file__).parent
eval_dir = current_dir.parent
bv_ans_root = eval_dir.parent.parent
sys.path.insert(0, str(bv_ans_root))
sys.path.insert(0, str(current_dir))

# Import agent and evaluation modules
from standalone_agent import root_agent
from dataset import EVALUATION_DATASET, get_dataset_stats, get_test_by_id
from metrics import evaluate_all_metrics
from mock_tools import get_mock_provider

# Load environment variables
env_path = bv_ans_root / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()  # Try to load from system


class AgentEvaluator:
    """Evaluator for the BV ANS Architecture Review Agent."""

    def __init__(self, project_id: str, location: str = "global"):
        """
        Initialize the evaluator.

        Args:
            project_id: GCP project ID
            location: GCP location (global for gemini-3-pro-preview)
        """
        self.project_id = project_id
        self.location = location
        self.runner = None
        self.results = []

        # Configure UTF-8 encoding for console
        self._configure_console_encoding()

        # Initialize Vertex AI with global location for gemini-3-pro-preview
        print(f"Initializing Vertex AI (Project: {project_id}, Location: {location})...")
        vertexai.init(project=project_id, location=location)

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
        # Format based on request type
        request = test_input.get("request", {})
        tipo_analise = request.get("tipo_analise", "geral")

        # Build query based on analysis type
        if tipo_analise in ["documento", "especificacao_tecnica", "proposta_fornecedor"]:
            documento = request.get("documento", {})
            return f"""
Analise o seguinte documento técnico:

**Arquivo**: {documento.get('filename', 'documento.pdf')}
**Tipo**: {documento.get('tipo', 'PDF')}
**Contexto**: {request.get('contexto_analise', 'Análise arquitetural')}

**Conteúdo**:
{documento.get('conteudo_simulado', '')}

Por favor, forneça um parecer arquitetural completo seguindo o framework de 8 pilares.
"""
        elif tipo_analise in ["planilha", "matriz_requisitos", "analise_orcamentaria"]:
            planilha = request.get("planilha", {})
            return f"""
Analise a seguinte planilha:

**Arquivo**: {planilha.get('filename', 'planilha.xlsx')}
**Tipo**: {planilha.get('tipo', 'XLSX')}
**Contexto**: {request.get('contexto_analise', 'Análise de dados')}

**Dados**:
{json.dumps(planilha.get('abas_simuladas', {}), ensure_ascii=False, indent=2)}

Forneça análise detalhada com métricas e identificação de gaps.
"""
        elif tipo_analise == "parecer_simples":
            return f"""
Solicitação de parecer rápido:

{request.get('descricao_demanda', '')}

Urgência: {request.get('urgencia', 'normal')}
Orçamento: {request.get('orcamento_estimado', 'Não especificado')}

Forneça parecer conciso e recomendação.
"""
        else:
            # Generic format
            return f"""
Processar solicitação:

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

        print(f"\n{'='*80}")
        print(f"📝 Running {test_id}: {scenario}")
        print(f"   Category: {test_case['category']}")
        if "subcategory" in test_case:
            print(f"   Subcategory: {test_case['subcategory']}")
        print(f"{'='*80}")

        start_time = datetime.now()

        try:
            # Prepare query
            query = self.format_payload(test_case["input"])

            # Enrich with mock data for document analysis tests
            category = test_case.get("category", "")
            if category in ["document_analysis", "spreadsheet_analysis"]:
                mock_provider = get_mock_provider()
                query = mock_provider.enrich_document_query(query, document_type=category)

            print(f"\n📤 Query (first 200 chars):\n{query[:200]}...\n")

            # Create session
            session = await self.runner.session_service.create_session(
                app_name=self.runner.app_name,
                user_id=f"eval_{test_id}"
            )

            # Prepare content
            content = types.Content(parts=[Part(text=query)])

            # Run agent
            print("🤖 Agent processing...")
            response_parts = []
            iteration_count = 0

            async for event in self.runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=content,
            ):
                iteration_count += 1
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_parts.append(part.text)

            # Combine response
            full_response = "\n".join(response_parts)

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()

            print(f"✅ Completed in {execution_time:.2f}s ({iteration_count} iterations)")
            print(f"📥 Response length: {len(full_response)} characters")

            # Prepare context for metrics
            context = {
                "test_id": test_id,
                "execution_time": execution_time,
                "iterations": iteration_count,
                "input": test_case["input"]
            }

            # Evaluate metrics
            print("\n📊 Evaluating metrics...")
            evaluation_results = evaluate_all_metrics(
                response=full_response,
                expected=test_case["expected_output"],
                context=context
            )

            # Build result
            result = {
                "test_id": test_id,
                "scenario": scenario,
                "category": test_case["category"],
                "subcategory": test_case.get("subcategory"),
                "execution_time": execution_time,
                "iterations": iteration_count,
                "response": full_response,
                "evaluation": evaluation_results,
                "passed": evaluation_results["overall_score"] >= 0.7,
                "timestamp": datetime.now().isoformat()
            }

            # Print summary
            print(f"\n{'='*80}")
            print(f"📈 Test Result: {test_id}")
            print(f"{'='*80}")
            print(f"Overall Score: {evaluation_results['overall_score']:.2%}")
            print(f"Status: {'✅ PASSED' if result['passed'] else '❌ FAILED'}")
            print(f"{'='*80}\n")

            return result

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            print(f"\n❌ Error running test {test_id}: {e}")

            return {
                "test_id": test_id,
                "scenario": scenario,
                "category": test_case["category"],
                "subcategory": test_case.get("subcategory"),
                "execution_time": execution_time,
                "error": str(e),
                "passed": False,
                "timestamp": datetime.now().isoformat()
            }

    async def run_all_tests(
        self,
        test_ids: Optional[List[str]] = None,
        categories: Optional[List[str]] = None
    ):
        """
        Run all tests or filtered subset.

        Args:
            test_ids: Specific test IDs to run (None = all)
            categories: Specific categories to run (None = all)
        """
        # Filter dataset
        dataset = EVALUATION_DATASET

        if test_ids:
            dataset = [t for t in EVALUATION_DATASET if t["test_id"] in test_ids]
        elif categories:
            dataset = [t for t in EVALUATION_DATASET if t["category"] in categories]

        print(f"\n🚀 Starting evaluation of {len(dataset)} test cases\n")

        for test_case in dataset:
            result = await self.run_test_case(test_case)
            self.results.append(result)

        print(f"\n✅ Evaluation complete: {len(self.results)} tests executed\n")

    def print_report(self):
        """Print evaluation report to console."""
        if not self.results:
            print("No results to report.")
            return

        print("\n" + "="*80)
        print("📊 EVALUATION REPORT - BV ANS AGENT")
        print("="*80)

        # Overall statistics
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.get("passed", False))
        failed_tests = total_tests - passed_tests
        avg_score = sum(r.get("evaluation", {}).get("overall_score", 0) for r in self.results) / total_tests
        total_time = sum(r.get("execution_time", 0) for r in self.results)

        print(f"\n📈 Summary:")
        print(f"   Total tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"   Average score: {avg_score:.2%}")
        print(f"   Total execution time: {total_time:.2f}s")
        print(f"   Average time per test: {total_time/total_tests:.2f}s")

        # Category breakdown
        categories = {}
        for result in self.results:
            cat = result.get("category", "unknown")
            if cat not in categories:
                categories[cat] = {"total": 0, "passed": 0}
            categories[cat]["total"] += 1
            if result.get("passed", False):
                categories[cat]["passed"] += 1

        print(f"\n📊 By Category:")
        for cat, stats in categories.items():
            success_rate = (stats["passed"] / stats["total"]) * 100
            print(f"   {cat}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")

        # Failed tests details
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.results:
                if not result.get("passed", False):
                    score = result.get("evaluation", {}).get("overall_score", 0)
                    print(f"   - {result['test_id']}: {result['scenario']} (score: {score:.2%})")

        print("\n" + "="*80 + "\n")

    def save_results(self, output_dir: str = "results"):
        """Save evaluation results to files."""
        output_path = Path(current_dir) / output_dir
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON
        json_file = output_path / f"evaluation_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": timestamp,
                "total_tests": len(self.results),
                "passed": sum(1 for r in self.results if r.get("passed", False)),
                "failed": sum(1 for r in self.results if not r.get("passed", False)),
                "results": self.results
            }, f, ensure_ascii=False, indent=2)

        print(f"📄 Results saved to: {json_file}")

        # Generate HTML report
        self._generate_html_report(output_path, timestamp)

    def _generate_html_report(self, output_path: Path, timestamp: str):
        """Generate HTML report with visualizations."""
        html_file = output_path / f"evaluation_{timestamp}.html"

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>BV ANS Agent Evaluation Report</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a73e8; border-bottom: 3px solid #1a73e8; padding-bottom: 10px; }}
        h2 {{ color: #333; margin-top: 30px; }}
        .summary {{ background: #e8f0fe; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .metric {{ display: inline-block; margin: 10px 20px 10px 0; }}
        .metric-label {{ font-weight: bold; color: #666; }}
        .metric-value {{ font-size: 24px; color: #1a73e8; }}
        .test-result {{ background: #f8f9fa; margin: 15px 0; padding: 15px; border-radius: 8px; border-left: 4px solid #ccc; }}
        .test-result.passed {{ border-left-color: #34a853; }}
        .test-result.failed {{ border-left-color: #ea4335; }}
        .test-header {{ font-weight: bold; font-size: 16px; margin-bottom: 10px; }}
        .test-details {{ color: #666; font-size: 14px; }}
        .score {{ font-weight: bold; padding: 4px 12px; border-radius: 12px; }}
        .score.excellent {{ background: #34a853; color: white; }}
        .score.good {{ background: #fbbc04; color: white; }}
        .score.fair {{ background: #ff9800; color: white; }}
        .score.poor {{ background: #ea4335; color: white; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #1a73e8; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 BV ANS Agent Evaluation Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <div class="summary">
            <h2>📊 Summary</h2>
            <div class="metric">
                <div class="metric-label">Total Tests</div>
                <div class="metric-value">{len(self.results)}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Passed</div>
                <div class="metric-value" style="color: #34a853;">{sum(1 for r in self.results if r.get("passed", False))}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Failed</div>
                <div class="metric-value" style="color: #ea4335;">{sum(1 for r in self.results if not r.get("passed", False))}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Success Rate</div>
                <div class="metric-value">{(sum(1 for r in self.results if r.get("passed", False))/len(self.results)*100):.1f}%</div>
            </div>
        </div>

        <h2>📋 Test Results</h2>
"""

        for result in self.results:
            passed = result.get("passed", False)
            score = result.get("evaluation", {}).get("overall_score", 0)

            if score >= 0.9:
                score_class = "excellent"
            elif score >= 0.75:
                score_class = "good"
            elif score >= 0.6:
                score_class = "fair"
            else:
                score_class = "poor"

            html_content += f"""
        <div class="test-result {'passed' if passed else 'failed'}">
            <div class="test-header">
                {'✅' if passed else '❌'} {result['test_id']}: {result['scenario']}
            </div>
            <div class="test-details">
                Category: {result['category']} | 
                Time: {result['execution_time']:.2f}s | 
                Score: <span class="score {score_class}">{score:.1%}</span>
            </div>
        </div>
"""

        html_content += """
    </div>
</body>
</html>
"""

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"📊 HTML report saved to: {html_file}")


async def main():
    """Main evaluation function."""
    # Get configuration from environment
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "gft-bu-gcp")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    print("="*80)
    print("🚀 BV ANS Agent - Comprehensive Evaluation")
    print("="*80)

    # Print dataset stats
    stats = get_dataset_stats()
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total tests: {stats['total_tests']}")
    print(f"   Categories: {list(stats['categories'].keys())}")
    print()

    # Initialize evaluator
    evaluator = AgentEvaluator(project_id=project_id, location=location)
    await evaluator.initialize()

    # Run all tests
    await evaluator.run_all_tests()

    # Print report
    evaluator.print_report()

    # Save results
    evaluator.save_results()

    print("\n✅ Evaluation complete!\n")


if __name__ == "__main__":
    asyncio.run(main())

