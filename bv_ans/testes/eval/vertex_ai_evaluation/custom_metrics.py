"""
Custom Metrics for BV ANS Architecture Review Agent

This module implements custom evaluation metrics specific to the
BV ANS agent, designed to work with ADK Evaluation Framework and
Vertex AI Evaluation Service.

These metrics evaluate business-specific logic, architectural review quality,
and compliance validation that standard metrics cannot capture.
"""

from typing import Dict, Any, List
import json
import re


def custom_document_analysis_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Evaluate document analysis quality for technical specifications and proposals.

    Checks:
    - Identification of key elements (requirements, risks, compliance)
    - Depth of architectural analysis
    - Adherence to 8-pillar framework
    - Clarity and structure of opinion

    Args:
        response: Agent response
        expected: Expected output
        context: Additional context

    Returns:
        Dictionary with scores (0.0-1.0)
    """
    score = 0.0
    max_score = 5.0
    feedback = []

    response_text = str(response)

    # Check if parecer final is present
    if "parecer_final" in response or "parecer" in response_text.lower():
        score += 1.0
        feedback.append("✅ Parecer final presente")
    else:
        feedback.append("❌ Parecer final ausente")

    # Check for architectural analysis elements
    arch_keywords = ["arquitetura", "architecture", "microservi", "integra", "segurança", "security"]
    arch_count = sum(1 for kw in arch_keywords if kw in response_text.lower())
    if arch_count >= 3:
        score += 1.0
        feedback.append(f"✅ Análise arquitetural presente ({arch_count} elementos)")
    else:
        feedback.append(f"⚠️ Análise arquitetural limitada ({arch_count} elementos)")

    # Check for risk identification
    if "risco" in response_text.lower() or "risk" in response_text.lower():
        score += 1.0
        feedback.append("✅ Identificação de riscos presente")
    else:
        feedback.append("❌ Identificação de riscos ausente")

    # Check for recommendations
    if "recomenda" in response_text.lower() or "sugest" in response_text.lower():
        score += 1.0
        feedback.append("✅ Recomendações fornecidas")
    else:
        feedback.append("⚠️ Recomendações ausentes")

    # Check for compliance validation (LGPD, ISO, etc.)
    compliance_keywords = ["lgpd", "iso", "compliance", "conformidade", "regulat"]
    compliance_count = sum(1 for kw in compliance_keywords if kw in response_text.lower())
    if compliance_count >= 1:
        score += 1.0
        feedback.append(f"✅ Análise de conformidade presente ({compliance_count} menções)")
    else:
        feedback.append("⚠️ Análise de conformidade limitada")

    return {
        "score": score / max_score,
        "feedback": " | ".join(feedback),
        "details": {
            "points_earned": score,
            "max_points": max_score,
            "coverage": f"{(score/max_score)*100:.1f}%"
        }
    }


def custom_spreadsheet_analysis_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Evaluate spreadsheet analysis accuracy and completeness.

    Checks:
    - Correct data extraction from tables
    - Identification of inconsistencies
    - Calculation of metrics (totals, averages, etc.)
    - Detection of data quality issues

    Args:
        response: Agent response
        expected: Expected output
        context: Additional context

    Returns:
        Dictionary with scores (0.0-1.0)
    """
    score = 0.0
    max_score = 5.0
    feedback = []

    response_text = str(response)

    # Check if data was extracted
    data_indicators = ["total", "soma", "média", "average", "linhas", "rows", "colunas", "columns"]
    data_count = sum(1 for ind in data_indicators if ind in response_text.lower())
    if data_count >= 2:
        score += 1.5
        feedback.append(f"✅ Extração de dados detectada ({data_count} indicadores)")
    else:
        feedback.append(f"⚠️ Extração de dados limitada ({data_count} indicadores)")

    # Check for gap/inconsistency identification
    if "gap" in response_text.lower() or "inconsist" in response_text.lower() or "problema" in response_text.lower():
        score += 1.0
        feedback.append("✅ Identificação de gaps/problemas")
    else:
        feedback.append("⚠️ Gaps/problemas não identificados explicitamente")

    # Check for metrics calculation
    number_pattern = r'\d+[.,]?\d*\s*%|\d+\s*(requisitos|items|registros)'
    if re.search(number_pattern, response_text.lower()):
        score += 1.0
        feedback.append("✅ Métricas calculadas presente")
    else:
        feedback.append("⚠️ Métricas calculadas não evidentes")

    # Check for quality assessment
    quality_keywords = ["qualidade", "quality", "válido", "valid", "correto", "correct", "precis"]
    if any(kw in response_text.lower() for kw in quality_keywords):
        score += 1.0
        feedback.append("✅ Avaliação de qualidade de dados")
    else:
        feedback.append("⚠️ Avaliação de qualidade não explícita")

    # Check for actionable insights
    action_keywords = ["deve", "should", "necessário", "required", "corrigir", "fix", "ajustar"]
    if any(kw in response_text.lower() for kw in action_keywords):
        score += 0.5
        feedback.append("✅ Insights acionáveis fornecidos")
    else:
        feedback.append("⚠️ Faltam insights acionáveis")

    return {
        "score": score / max_score,
        "feedback": " | ".join(feedback),
        "details": {
            "points_earned": score,
            "max_points": max_score,
            "coverage": f"{(score/max_score)*100:.1f}%"
        }
    }


def custom_framework_adherence_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Evaluate adherence to the 8-pillar architectural framework.

    The 8 pillars:
    1. Aderência aos Requisitos de Negócio
    2. Aderência Técnica e Funcional
    3. Capacidade Operacional
    4. Governança e Compliance
    5. Maturidade Tecnológica
    6. Análise de Riscos
    7. Viabilidade de Implementação
    8. Alinhamento Stakeholder

    Args:
        response: Agent response
        expected: Expected output
        context: Additional context

    Returns:
        Dictionary with scores (0.0-1.0)
    """
    score = 0.0
    max_score = 8.0
    feedback = []
    pillars_found = []

    response_text = str(response).lower()

    # Pillar 1: Business Requirements
    if any(kw in response_text for kw in ["negócio", "business", "requisitos", "requirements", "objetiv"]):
        score += 1.0
        pillars_found.append("1-Requisitos Negócio")

    # Pillar 2: Technical Adherence
    if any(kw in response_text for kw in ["técnic", "technical", "funcional", "functional", "capacidade"]):
        score += 1.0
        pillars_found.append("2-Aderência Técnica")

    # Pillar 3: Operational Capacity
    if any(kw in response_text for kw in ["operacion", "operational", "infraestrutura", "infrastructure", "suporte", "support"]):
        score += 1.0
        pillars_found.append("3-Capacidade Operacional")

    # Pillar 4: Governance and Compliance
    if any(kw in response_text for kw in ["governança", "governance", "compliance", "conformidade", "lgpd", "iso", "certificação"]):
        score += 1.0
        pillars_found.append("4-Governança/Compliance")

    # Pillar 5: Technology Maturity
    if any(kw in response_text for kw in ["maturidade", "maturity", "tecnológica", "technology", "solidez", "estabilidade"]):
        score += 1.0
        pillars_found.append("5-Maturidade Tecnológica")

    # Pillar 6: Risk Analysis
    if any(kw in response_text for kw in ["risco", "risk", "ameaça", "threat", "vulnerabilidade", "vulnerability"]):
        score += 1.0
        pillars_found.append("6-Análise Riscos")

    # Pillar 7: Implementation Feasibility
    if any(kw in response_text for kw in ["viabilidade", "feasibility", "implementação", "implementation", "prazo", "timeline", "cronograma"]):
        score += 1.0
        pillars_found.append("7-Viabilidade Implementação")

    # Pillar 8: Stakeholder Alignment
    if any(kw in response_text for kw in ["stakeholder", "parte interessada", "alinhamento", "alignment", "usuário", "user"]):
        score += 1.0
        pillars_found.append("8-Alinhamento Stakeholder")

    # Provide feedback
    if len(pillars_found) >= 6:
        feedback.append(f"✅ Cobertura adequada dos pilares ({len(pillars_found)}/8)")
    elif len(pillars_found) >= 4:
        feedback.append(f"⚠️ Cobertura parcial dos pilares ({len(pillars_found)}/8)")
    else:
        feedback.append(f"❌ Cobertura insuficiente dos pilares ({len(pillars_found)}/8)")

    feedback.append(f"Pilares identificados: {', '.join(pillars_found) if pillars_found else 'nenhum'}")

    return {
        "score": score / max_score,
        "feedback": " | ".join(feedback),
        "details": {
            "points_earned": score,
            "max_points": max_score,
            "pillars_found": len(pillars_found),
            "pillars_list": pillars_found,
            "coverage": f"{(score/max_score)*100:.1f}%"
        }
    }


def custom_tool_usage_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Evaluate correct usage of agent tools.

    Checks:
    - Appropriate tool calls for scenario
    - Correct error handling
    - Logical sequence of calls
    - Parameter validation

    Args:
        response: Agent response
        expected: Expected output
        context: Additional context

    Returns:
        Dictionary with scores (0.0-1.0)
    """
    score = 0.0
    max_score = 4.0
    feedback = []

    response_text = str(response)

    # Check if tools were mentioned/used
    tool_indicators = ["analisar_documento", "analisar_planilha", "extrair_dados", "consultar", "status"]
    tools_used = [tool for tool in tool_indicators if tool in response_text.lower()]

    if len(tools_used) >= 1:
        score += 1.0
        feedback.append(f"✅ Uso de ferramentas detectado ({len(tools_used)} ferramentas)")
    else:
        feedback.append("⚠️ Uso de ferramentas não evidente")

    # Check for appropriate error handling
    if "erro" in response_text.lower() or "error" in response_text.lower():
        # If there's an error, check if it's handled gracefully
        if "tente" in response_text.lower() or "verifique" in response_text.lower():
            score += 1.0
            feedback.append("✅ Erro tratado adequadamente")
        else:
            score += 0.5
            feedback.append("⚠️ Erro reportado mas tratamento pode melhorar")
    else:
        # No error is also good (successful execution)
        if "sucesso" in response_text.lower() or "success" in response_text.lower() or len(response_text) > 100:
            score += 1.0
            feedback.append("✅ Execução aparentemente bem-sucedida")

    # Check for structured output (JSON format expected)
    try:
        # Try to extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            json.loads(json_match.group())
            score += 1.0
            feedback.append("✅ Saída estruturada (JSON válido)")
        else:
            score += 0.5
            feedback.append("⚠️ Saída não estruturada em JSON")
    except json.JSONDecodeError:
        score += 0.3
        feedback.append("⚠️ JSON inválido ou formato não estruturado")

    # Check for completeness of response
    response_len = len(response_text)
    if response_len >= 500:  # Substantial response
        score += 1.0
        feedback.append(f"✅ Resposta completa ({response_len} chars)")
    elif response_len >= 200:
        score += 0.5
        feedback.append(f"⚠️ Resposta moderada ({response_len} chars)")
    else:
        feedback.append(f"❌ Resposta muito curta ({response_len} chars)")

    return {
        "score": score / max_score,
        "feedback": " | ".join(feedback),
        "details": {
            "points_earned": score,
            "max_points": max_score,
            "tools_detected": len(tools_used),
            "response_length": len(response_text),
            "coverage": f"{(score/max_score)*100:.1f}%"
        }
    }


def custom_response_completeness_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Evaluate completeness of agent response.

    Checks:
    - All mandatory fields present
    - Adequate justifications
    - Appropriate level of detail
    - Valid JSON format

    Args:
        response: Agent response
        expected: Expected output
        context: Additional context

    Returns:
        Dictionary with scores (0.0-1.0)
    """
    score = 0.0
    max_score = 5.0
    feedback = []

    response_text = str(response)
    expected_analysis = expected.get("analise_obrigatoria", {})

    # Check for mandatory elements based on expected output
    mandatory_elements = {
        "parecer/opinião": ["parecer", "opinião", "opinion", "recomend"],
        "justificativa": ["justificativa", "justification", "porque", "because", "razão", "reason"],
        "riscos": ["risco", "risk"],
        "próximos passos": ["próxim", "next", "passo", "step", "ação", "action"]
    }

    elements_found = 0
    for element_name, keywords in mandatory_elements.items():
        if any(kw in response_text.lower() for kw in keywords):
            elements_found += 1
            feedback.append(f"✅ {element_name.capitalize()}")
        else:
            feedback.append(f"❌ {element_name.capitalize()} ausente")

    score += (elements_found / len(mandatory_elements)) * 2.0  # Max 2 points

    # Check detail level
    if len(response_text) >= 1000:  # Detailed response
        score += 1.5
        feedback.append("✅ Nível de detalhe adequado")
    elif len(response_text) >= 500:
        score += 1.0
        feedback.append("⚠️ Nível de detalhe moderado")
    else:
        score += 0.5
        feedback.append("⚠️ Resposta pode ter mais detalhes")

    # Check for structured sections
    section_indicators = ["##", "**", "===", "---", "1.", "2.", "3."]
    sections_found = sum(1 for ind in section_indicators if ind in response_text)
    if sections_found >= 3:
        score += 1.0
        feedback.append("✅ Resposta bem estruturada")
    elif sections_found >= 1:
        score += 0.5
        feedback.append("⚠️ Estruturação parcial")

    # Check for specific expected fields
    expected_fields_present = 0
    expected_fields_total = len(expected_analysis)

    if expected_fields_total > 0:
        for field_name, field_value in expected_analysis.items():
            field_key = field_name.replace("_", " ")
            if field_key in response_text.lower():
                expected_fields_present += 1

        if expected_fields_present >= expected_fields_total * 0.7:  # 70% threshold
            score += 0.5
            feedback.append(f"✅ Campos esperados presentes ({expected_fields_present}/{expected_fields_total})")
        else:
            feedback.append(f"⚠️ Alguns campos esperados ausentes ({expected_fields_present}/{expected_fields_total})")

    return {
        "score": min(score / max_score, 1.0),  # Cap at 1.0
        "feedback": " | ".join(feedback[:5]),  # Limit feedback items
        "details": {
            "points_earned": score,
            "max_points": max_score,
            "elements_found": elements_found,
            "total_elements": len(mandatory_elements),
            "response_length": len(response_text),
            "coverage": f"{(min(score, max_score)/max_score)*100:.1f}%"
        }
    }


def custom_performance_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Evaluate performance efficiency.

    Checks:
    - Response time < threshold
    - Number of agent iterations
    - Token usage efficiency

    Args:
        response: Agent response
        expected: Expected output
        context: Additional context (should include timing info)

    Returns:
        Dictionary with scores (0.0-1.0)
    """
    score = 0.0
    max_score = 3.0
    feedback = []

    # Get execution time from context
    execution_time = context.get("execution_time", 0)
    max_time = expected.get("tempo_processamento_max", 60)  # Default 60s

    if execution_time > 0:
        if execution_time <= max_time * 0.5:  # Excellent: < 50% of max time
            score += 1.5
            feedback.append(f"✅ Tempo excelente: {execution_time:.2f}s")
        elif execution_time <= max_time:  # Good: within max time
            score += 1.0
            feedback.append(f"✅ Tempo adequado: {execution_time:.2f}s")
        else:  # Slow: exceeds max time
            score += 0.3
            feedback.append(f"⚠️ Tempo acima do esperado: {execution_time:.2f}s (max: {max_time}s)")
    else:
        score += 0.5  # Neutral if no timing info
        feedback.append("⚠️ Tempo de execução não medido")

    # Check iterations (if available)
    iterations = context.get("iterations", 0)
    if iterations > 0:
        if iterations <= 3:
            score += 1.0
            feedback.append(f"✅ Iterações eficientes: {iterations}")
        elif iterations <= 5:
            score += 0.7
            feedback.append(f"⚠️ Iterações moderadas: {iterations}")
        else:
            score += 0.3
            feedback.append(f"⚠️ Muitas iterações: {iterations}")
    else:
        score += 0.5  # Neutral if no iteration info

    # Check response efficiency (not too verbose, not too short)
    response_len = len(str(response))
    if 500 <= response_len <= 3000:  # Optimal range
        score += 0.5
        feedback.append(f"✅ Resposta otimizada ({response_len} chars)")
    elif response_len < 500:
        score += 0.3
        feedback.append(f"⚠️ Resposta muito concisa ({response_len} chars)")
    else:
        score += 0.4
        feedback.append(f"⚠️ Resposta muito verbosa ({response_len} chars)")

    return {
        "score": score / max_score,
        "feedback": " | ".join(feedback),
        "details": {
            "points_earned": score,
            "max_points": max_score,
            "execution_time": execution_time,
            "iterations": iterations,
            "response_length": response_len,
            "coverage": f"{(score/max_score)*100:.1f}%"
        }
    }


# Mapping of metric names to functions
CUSTOM_METRICS = {
    "document_analysis": custom_document_analysis_metric,
    "spreadsheet_analysis": custom_spreadsheet_analysis_metric,
    "framework_adherence": custom_framework_adherence_metric,
    "tool_usage": custom_tool_usage_metric,
    "response_completeness": custom_response_completeness_metric,
    "performance": custom_performance_metric
}


def get_all_custom_metrics() -> Dict[str, callable]:
    """
    Get all available custom metrics.

    Returns:
        Dictionary mapping metric names to functions
    """
    return CUSTOM_METRICS.copy()


def apply_custom_metric(
    metric_name: str,
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Apply a specific custom metric.

    Args:
        metric_name: Name of the metric to apply
        response: Agent response
        expected: Expected output
        context: Additional context

    Returns:
        Metric result dictionary

    Raises:
        ValueError: If metric name is not found
    """
    if metric_name not in CUSTOM_METRICS:
        raise ValueError(f"Unknown metric: {metric_name}. Available: {list(CUSTOM_METRICS.keys())}")

    metric_func = CUSTOM_METRICS[metric_name]
    return metric_func(response, expected, context)


if __name__ == "__main__":
    # Example usage
    print("🎯 BV ANS Agent Custom Metrics\n")
    print(f"Available metrics: {len(CUSTOM_METRICS)}")
    for metric_name in CUSTOM_METRICS.keys():
        print(f"  - {metric_name}")

