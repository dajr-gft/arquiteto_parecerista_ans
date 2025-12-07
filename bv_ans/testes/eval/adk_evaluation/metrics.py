"""
Custom Evaluation Metrics Aggregator for BV ANS Agent

This module aggregates and applies all custom metrics for evaluating
agent responses according to BV ANS architectural review requirements.
"""

import json
import re
from typing import Dict, Any, Tuple, List
from custom_metrics import CUSTOM_METRICS, apply_custom_metric


class AgentMetrics:
    """Aggregator for all agent evaluation metrics."""

    @staticmethod
    def extract_json_from_response(response: str) -> Dict[str, Any]:
        """Extract JSON object from agent response."""
        try:
            # Try to find JSON in markdown code block first
            json_match = re.search(r'```json\s*(\{[\s\S]*?\})\s*```', response, re.MULTILINE)
            if json_match:
                return json.loads(json_match.group(1))

            # Fallback: Try to find any JSON in response
            json_match = re.search(r'\{[\s\S]*}', response)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def evaluate_success(
        response: Any,
        expected: Dict[str, Any]
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Evaluate if the agent succeeded in its task.

        Returns:
            Tuple of (score, details) where score is 0.0 or 1.0
        """
        details = {
            "metric": "success",
            "pass": False,
            "reason": ""
        }

        response_text = str(response)
        expected_success = expected.get("sucesso", True)

        # Check for error indicators
        has_hard_error = (
            "erro" in response_text.lower() and "validacao" in response_text.lower()
        ) or (
            "error" in response_text.lower() and "validation" in response_text.lower()
        ) or (
            response_text.startswith("ERRO:") or response_text.startswith("ERROR:")
        )

        # Check for success indicators - agent provided analysis
        has_analysis = (
            len(response_text) >= 800 and  # Substantial response
            any(keyword in response_text.lower() for keyword in [
                "análise", "analysis", "parecer", "avaliação", "evaluation",
                "recomenda", "recommend", "risco", "risk"
            ])
        )

        # "Erro" mentioned but analysis provided = still success
        mentions_limitations = (
            "documento" in response_text.lower() and
            ("obrigatório" in response_text.lower() or "necessário" in response_text.lower())
        )

        # Evaluate based on expectation
        if expected_success:
            if has_hard_error:
                details["reason"] = "Agent returned hard error (validation error)"
                return 0.0, details
            elif has_analysis:
                details["pass"] = True
                if mentions_limitations:
                    details["reason"] = "Agent provided analysis despite mentioning document limitations"
                else:
                    details["reason"] = "Agent completed task successfully with comprehensive analysis"
                return 1.0, details
            else:
                details["reason"] = "Response unclear or incomplete"
                return 0.3, details
        else:
            # Failure expected (e.g., validation error, missing data)
            if has_hard_error:
                details["pass"] = True
                details["reason"] = "Agent correctly identified error condition"
                return 1.0, details
            else:
                details["reason"] = "Agent should have reported error but didn't"
                return 0.0, details

    @staticmethod
    def evaluate_response_quality(
        response: Any,
        expected: Dict[str, Any]
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Evaluate overall response quality.

        Returns:
            Tuple of (score, details)
        """
        details = {
            "metric": "response_quality",
            "components": {}
        }

        response_text = str(response)
        score = 0.0
        max_score = 4.0

        # Component 1: Response length appropriateness
        length = len(response_text)
        if 500 <= length <= 5000:
            score += 1.0
            details["components"]["length"] = "appropriate"
        elif 200 <= length < 500:
            score += 0.6
            details["components"]["length"] = "short but acceptable"
        elif length > 5000:
            score += 0.7
            details["components"]["length"] = "verbose"
        else:
            score += 0.2
            details["components"]["length"] = "too short"

        # Component 2: Structured content
        has_structure = any(marker in response_text for marker in ["##", "**", "===", "1.", "2."])
        if has_structure:
            score += 1.0
            details["components"]["structure"] = "well-structured"
        else:
            score += 0.3
            details["components"]["structure"] = "unstructured"

        # Component 3: Professional language
        professional_indicators = ["análise", "avaliação", "recomend", "consider", "parecer"]
        prof_count = sum(1 for ind in professional_indicators if ind in response_text.lower())
        if prof_count >= 3:
            score += 1.0
            details["components"]["professionalism"] = "professional"
        elif prof_count >= 1:
            score += 0.5
            details["components"]["professionalism"] = "adequate"
        else:
            score += 0.2
            details["components"]["professionalism"] = "needs improvement"

        # Component 4: Actionable content
        actionable_keywords = ["deve", "should", "recomend", "sugest", "próxim", "next"]
        if any(kw in response_text.lower() for kw in actionable_keywords):
            score += 1.0
            details["components"]["actionability"] = "actionable"
        else:
            score += 0.3
            details["components"]["actionability"] = "limited actionability"

        details["score"] = score / max_score
        return score / max_score, details


def evaluate_all_metrics(
    response: Any,
    expected: Dict[str, Any],
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Apply all evaluation metrics to an agent response.

    Args:
        response: Agent response (can be string or dict)
        expected: Expected output from test case
        context: Additional context (execution time, iterations, etc.)

    Returns:
        Dictionary with all metric scores and details
    """
    if context is None:
        context = {}

    results = {
        "overall_score": 0.0,
        "metrics": {},
        "summary": {
            "total_metrics": 0,
            "passed_metrics": 0,
            "failed_metrics": 0
        }
    }

    # Ensure response is in proper format
    if isinstance(response, str):
        response_dict = {"text": response}
    else:
        response_dict = response

    # Apply basic metrics
    success_score, success_details = AgentMetrics.evaluate_success(response_dict, expected)
    results["metrics"]["success"] = {
        "score": success_score,
        "details": success_details
    }

    quality_score, quality_details = AgentMetrics.evaluate_response_quality(response_dict, expected)
    results["metrics"]["response_quality"] = {
        "score": quality_score,
        "details": quality_details
    }

    # Apply all custom metrics
    for metric_name, metric_func in CUSTOM_METRICS.items():
        try:
            metric_result = apply_custom_metric(
                metric_name,
                response_dict,
                expected,
                context
            )
            results["metrics"][metric_name] = metric_result
        except Exception as e:
            results["metrics"][metric_name] = {
                "score": 0.0,
                "error": str(e),
                "feedback": f"❌ Error applying metric: {e}"
            }

    # Calculate overall score
    total_score = 0.0
    total_metrics = len(results["metrics"])
    passed = 0
    failed = 0

    for metric_name, metric_data in results["metrics"].items():
        score = metric_data.get("score", 0.0)
        total_score += score

        if score >= 0.7:
            passed += 1
        else:
            failed += 1

    results["overall_score"] = total_score / total_metrics if total_metrics > 0 else 0.0
    results["summary"]["total_metrics"] = total_metrics
    results["summary"]["passed_metrics"] = passed
    results["summary"]["failed_metrics"] = failed

    return results


def get_metric_summary(evaluation_results: Dict[str, Any]) -> str:
    """
    Generate a human-readable summary of evaluation results.

    Args:
        evaluation_results: Results from evaluate_all_metrics

    Returns:
        Formatted summary string
    """
    summary_lines = []
    summary_lines.append("=" * 60)
    summary_lines.append("EVALUATION SUMMARY")
    summary_lines.append("=" * 60)

    overall_score = evaluation_results["overall_score"]
    summary_lines.append(f"\n📊 Overall Score: {overall_score:.2%}")

    # Classification
    if overall_score >= 0.90:
        classification = "🟢 EXCELENTE - Pronto para produção"
    elif overall_score >= 0.75:
        classification = "🟡 BOM - Revisar casos com score baixo"
    elif overall_score >= 0.60:
        classification = "🟠 ADEQUADO - Melhorias necessárias"
    else:
        classification = "🔴 INSUFICIENTE - Correções críticas necessárias"

    summary_lines.append(f"Classification: {classification}\n")

    # Metrics breakdown
    summary_lines.append("📈 Metrics Breakdown:")
    summary_lines.append("-" * 60)

    for metric_name, metric_data in evaluation_results["metrics"].items():
        score = metric_data.get("score", 0.0)
        feedback = metric_data.get("feedback", "No feedback")

        # Icon based on score
        if score >= 0.8:
            icon = "✅"
        elif score >= 0.6:
            icon = "⚠️"
        else:
            icon = "❌"

        summary_lines.append(f"{icon} {metric_name}: {score:.2%}")
        if feedback and len(feedback) <= 100:
            summary_lines.append(f"   {feedback}")

    summary_lines.append("-" * 60)
    summary_lines.append(f"Total: {evaluation_results['summary']['total_metrics']} metrics")
    summary_lines.append(f"Passed (≥70%): {evaluation_results['summary']['passed_metrics']}")
    summary_lines.append(f"Failed (<70%): {evaluation_results['summary']['failed_metrics']}")
    summary_lines.append("=" * 60)

    return "\n".join(summary_lines)


if __name__ == "__main__":
    # Example test
    print("🧪 Testing BV ANS Agent Metrics\n")

    sample_response = {
        "text": """
        ## Parecer Arquitetural
        
        Após análise detalhada da proposta técnica, identifico os seguintes pontos:
        
        **Análise de Arquitetura:**
        A solução proposta utiliza microserviços e arquitetura cloud-native, adequada
        para os requisitos de escalabilidade.
        
        **Riscos Identificados:**
        1. Dependência de fornecedor único para serviços cloud
        2. Necessidade de capacitação da equipe em Kubernetes
        
        **Recomendações:**
        - Implementar estratégia multi-cloud para mitigação de riscos
        - Planejar treinamento da equipe técnica
        
        **Conformidade:**
        A solução atende aos requisitos de LGPD e possui certificação ISO 27001.
        
        **Parecer Final: FAVORÁVEL COM RESSALVAS**
        """
    }

    sample_expected = {
        "sucesso": True,
        "parecer_final": ["FAVORÁVEL", "FAVORÁVEL COM RESSALVAS"],
        "analise_obrigatoria": {
            "riscos_identificados": True,
            "recomendacoes": True
        }
    }

    sample_context = {
        "execution_time": 5.2,
        "iterations": 2
    }

    results = evaluate_all_metrics(sample_response, sample_expected, sample_context)
    print(get_metric_summary(results))

