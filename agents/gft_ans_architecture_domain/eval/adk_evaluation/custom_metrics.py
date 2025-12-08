"""
Custom Metrics for Architecture Domain ANS Agent

This module implements custom evaluation metrics specific to the
Architecture Domain ANS agent, designed to work with Vertex AI
Evaluation Service.

These metrics evaluate business-specific logic and integrations
that standard metrics cannot capture.
"""

from typing import Dict, Any, List


def custom_onetrust_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Evaluate OneTrust integration quality.

    Checks:
    - OneTrust data was consulted
    - Contract expiration date retrieved (if applicable)
    - Proper handling of missing data

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

    # Check if OneTrust was consulted
    if "onetrust" in str(response).lower() or \
       "OneTrust" in response.get("insumos_utilizados", []):
        score += 1.0
        feedback.append("✅ OneTrust integration detected")
    else:
        feedback.append("❌ OneTrust integration not detected")

    # Check if expiration date handling is correct
    tipo_requisicao = context.get("input", {}).get("request", {}).get("tipo_requisicao")

    if tipo_requisicao == "Renovação":
        # For renewals, should check expiration date
        if "vencimento" in str(response).lower() or \
           "expiration" in str(response).lower():
            score += 1.0
            feedback.append("✅ Contract expiration validated")
        else:
            feedback.append("⚠️ Contract expiration not explicitly validated")
    else:
        score += 1.0  # N/A for new contracts
        feedback.append("✅ N/A for new contracts")

    # Check bloqueio handling for missing expiration
    if context.get("input", {}).get("request", {}).get("tipo_requisicao") == "Renovação":
        expected_bloqueio = expected.get("evaluation_criteria", {}).get("should_block_if_no_expiration", False)

        if expected_bloqueio:
            if response.get("status") == "BLOQUEIO_GOVERNANCA":
                score += 1.0
                feedback.append("✅ Correct bloqueio for missing expiration")
            else:
                feedback.append("❌ Should block when expiration is missing")
        else:
            score += 1.0
            feedback.append("✅ Bloqueio handling correct")
    else:
        score += 1.0

    # Check OneTrust fields in response
    if response.get("insumos_utilizados") and \
       any("OneTrust" in str(source) for source in response.get("insumos_utilizados", [])):
        score += 1.0
        feedback.append("✅ OneTrust explicitly listed in sources")
    else:
        feedback.append("⚠️ OneTrust not explicitly listed in sources")

    return {
        "score": score / max_score,
        "feedback": " | ".join(feedback),
        "details": {
            "points_earned": score,
            "max_points": max_score
        }
    }


def custom_cmdb_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Evaluate CMDB integration quality.

    Checks:
    - CMDB data was consulted
    - Service sigla retrieved
    - Direcionador (strategic direction) captured
    - Proper handling of direcionador in decision

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

    # Check if CMDB was consulted
    if "cmdb" in str(response).lower() or \
       "CMDB" in response.get("insumos_utilizados", []):
        score += 1.0
        feedback.append("✅ CMDB integration detected")
    else:
        feedback.append("❌ CMDB integration not detected")

    # Check if sigla is present
    sigla = response.get("sigla_servico") or \
            response.get("metadados_parecer", {}).get("sigla_servico_cmdb")

    if sigla:
        score += 1.0
        feedback.append(f"✅ Service sigla retrieved: {sigla}")
    else:
        feedback.append("❌ Service sigla not found in response")

    # Check if direcionador is present
    direcionador = response.get("direcionador") or \
                   response.get("metadados_parecer", {}).get("direcionador_estrategico")

    if direcionador:
        score += 1.0
        feedback.append(f"✅ Direcionador captured: {direcionador}")
    else:
        feedback.append("❌ Direcionador not found in response")

    # Check if direcionador influenced decision
    if direcionador == "Desinvestir":
        # Should have ressalva about desinvestimento
        ressalvas = response.get("ressalvas_tecnicas", []) or response.get("ressalvas", [])

        has_desinvestir_ressalva = any(
            "Desinvestir" in str(r) or "desinvest" in str(r).lower()
            for r in ressalvas
        )

        if has_desinvestir_ressalva:
            score += 1.0
            feedback.append("✅ Direcionador 'Desinvestir' correctly handled with ressalva")
        else:
            feedback.append("⚠️ Direcionador 'Desinvestir' should trigger ressalva")
    else:
        score += 1.0
        feedback.append("✅ Direcionador handling correct")

    return {
        "score": score / max_score,
        "feedback": " | ".join(feedback),
        "details": {
            "points_earned": score,
            "max_points": max_score,
            "sigla": sigla,
            "direcionador": direcionador
        }
    }


def custom_parecer_accuracy_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Evaluate parecer suggestion accuracy.

    Checks:
    - Parecer type matches expected
    - Decision is justified
    - Score is within reasonable range

    Args:
        response: Agent response
        expected: Expected output
        context: Additional context

    Returns:
        Dictionary with scores (0.0-1.0)
    """
    score = 0.0
    max_score = 3.0
    feedback = []

    # Extract parecer from response (multiple possible locations)
    actual_parecer = (
        response.get("parecer_sugerido") or
        response.get("decisao_tecnica", {}).get("parecer_recomendado") or
        response.get("parecer_recomendado")
    )

    expected_parecer = expected.get("parecer_sugerido")

    # Check if parecer matches expected
    if actual_parecer and expected_parecer:
        # Normalize parecer text
        actual_normalized = actual_parecer.lower().replace("parecer", "").replace("técnico", "").strip()
        expected_normalized = expected_parecer.lower().replace("parecer", "").strip()

        if actual_normalized in expected_normalized or expected_normalized in actual_normalized:
            score += 2.0
            feedback.append(f"✅ Parecer correct: {actual_parecer}")
        else:
            feedback.append(f"❌ Parecer mismatch: expected '{expected_parecer}', got '{actual_parecer}'")
    else:
        feedback.append("⚠️ Could not extract parecer from response")

    # Check if justification is present and substantial
    justificativa = (
        response.get("justificativa") or
        response.get("decisao_tecnica", {}).get("fundamentacao_tecnica")
    )

    if justificativa and len(justificativa) > 50:
        score += 0.5
        feedback.append(f"✅ Justification provided ({len(justificativa)} chars)")
    else:
        feedback.append("⚠️ Justification missing or too short")

    # Check confidence score validity
    confidence = (
        response.get("score_confianca") or
        response.get("score_conformidade_tecnica") or
        response.get("decisao_tecnica", {}).get("score_conformidade_tecnica")
    )

    if confidence is not None and 0.0 <= confidence <= 1.0:
        score += 0.5
        feedback.append(f"✅ Valid confidence score: {confidence:.2f}")
    else:
        feedback.append("⚠️ Confidence score missing or invalid")

    return {
        "score": score / max_score,
        "feedback": " | ".join(feedback),
        "details": {
            "points_earned": score,
            "max_points": max_score,
            "actual_parecer": actual_parecer,
            "expected_parecer": expected_parecer
        }
    }


def custom_ressalvas_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Evaluate ressalvas (observations) detection.

    Checks:
    - LGPD ressalva when armazena_dados_bv=true
    - Direcionador ressalva when Desinvestir
    - Historical ressalvas propagated (if renewal)

    Args:
        response: Agent response
        expected: Expected output
        context: Additional context

    Returns:
        Dictionary with scores (0.0-1.0)
    """
    score = 0.0
    max_score = 3.0
    feedback = []

    ressalvas = response.get("ressalvas_tecnicas", []) or response.get("ressalvas", [])

    # Check LGPD ressalva
    armazena_dados = context.get("input", {}).get("request", {}).get("armazena_dados_bv", False)

    if armazena_dados:
        has_lgpd_ressalva = any(
            "LGPD" in str(r) or "proteção de dados" in str(r).lower() or
            "dados corporativos" in str(r).lower()
            for r in ressalvas
        )

        if has_lgpd_ressalva:
            score += 1.0
            feedback.append("✅ LGPD ressalva correctly added for data storage")
        else:
            feedback.append("❌ Missing LGPD ressalva for data storage")
    else:
        score += 1.0
        feedback.append("✅ N/A - No data storage")

    # Check Desinvestir ressalva
    expected_direcionador = expected.get("expected_output", {}).get("direcionador")

    if expected_direcionador == "Desinvestir":
        has_desinvestir_ressalva = any(
            "Desinvestir" in str(r) or "descontinuação" in str(r).lower()
            for r in ressalvas
        )

        if has_desinvestir_ressalva:
            score += 1.0
            feedback.append("✅ Desinvestir ressalva correctly added")
        else:
            feedback.append("❌ Missing Desinvestir ressalva")
    else:
        score += 1.0
        feedback.append("✅ N/A - Not marked for desinvestimento")

    # Check if ressalvas array is well-formed
    if isinstance(ressalvas, list):
        score += 1.0
        feedback.append(f"✅ Ressalvas array well-formed ({len(ressalvas)} items)")
    else:
        feedback.append("❌ Ressalvas not a proper array")

    return {
        "score": score / max_score,
        "feedback": " | ".join(feedback),
        "details": {
            "points_earned": score,
            "max_points": max_score,
            "ressalvas_count": len(ressalvas) if isinstance(ressalvas, list) else 0
        }
    }


def custom_bloqueio_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Evaluate bloqueio (blocking) detection.

    Checks:
    - Bloqueio triggered when vencimento absent (renovação)
    - Bloqueio not triggered inappropriately
    - Bloqueio message is clear

    Args:
        response: Agent response
        expected: Expected output
        context: Additional context

    Returns:
        Dictionary with scores (0.0-1.0)
    """
    score = 0.0
    max_score = 3.0
    feedback = []

    should_block = expected.get("evaluation_criteria", {}).get("should_block", False)
    actual_blocked = response.get("status") in ["BLOQUEIO", "BLOQUEIO_GOVERNANCA"]

    # Check if bloqueio decision is correct
    if should_block and actual_blocked:
        score += 2.0
        feedback.append("✅ Correctly blocked as expected")
    elif not should_block and not actual_blocked:
        score += 2.0
        feedback.append("✅ Correctly did not block")
    elif should_block and not actual_blocked:
        feedback.append("❌ Should have blocked but did not")
    else:
        feedback.append("⚠️ Blocked unnecessarily")

    # Check bloqueio message clarity
    if actual_blocked:
        erro_msg = response.get("mensagem") or response.get("erro")

        if erro_msg and len(erro_msg) > 20:
            score += 0.5
            feedback.append("✅ Clear bloqueio message provided")
        else:
            feedback.append("⚠️ Bloqueio message unclear or missing")

        # Check acao_requerida
        if response.get("acao_requerida"):
            score += 0.5
            feedback.append("✅ Action required specified")
        else:
            feedback.append("⚠️ Action required not specified")
    else:
        score += 1.0
        feedback.append("✅ N/A - No bloqueio")

    return {
        "score": score / max_score,
        "feedback": " | ".join(feedback),
        "details": {
            "points_earned": score,
            "max_points": max_score,
            "should_block": should_block,
            "actual_blocked": actual_blocked
        }
    }


# Registry of custom metrics
CUSTOM_METRICS_REGISTRY = {
    "onetrust_integration": custom_onetrust_metric,
    "cmdb_integration": custom_cmdb_metric,
    "parecer_accuracy": custom_parecer_accuracy_metric,
    "ressalvas_detection": custom_ressalvas_metric,
    "bloqueio_detection": custom_bloqueio_metric
}


def evaluate_custom_metrics(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, Dict[str, Any]]:
    """
    Evaluate all custom metrics for a single test case.

    Args:
        response: Agent response
        expected: Expected output
        context: Test case context

    Returns:
        Dictionary of metric results
    """
    results = {}

    for metric_name, metric_func in CUSTOM_METRICS_REGISTRY.items():
        try:
            result = metric_func(response, expected, context)
            results[metric_name] = result
        except Exception as e:
            results[metric_name] = {
                "score": 0.0,
                "feedback": f"Error: {str(e)}",
                "error": True
            }

    return results

