"""
Health check endpoints for monitoring and orchestration.

Este módulo fornece endpoints de health check para Kubernetes
e ferramentas de monitoramento.
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any
from genai_framework.decorators import post_route

logger = logging.getLogger(__name__)


@post_route('health')
def health_check() -> Dict[str, Any]:
    """
    Endpoint de health check básico.

    Retorna o status de saúde do serviço.
    Usado por Kubernetes liveness probe.

    Returns:
        Dict com status e timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "genaigke-sdlc-aarq-ans-avaliacao-parceiro"
    }


@post_route('ready')
def readiness_check() -> Dict[str, Any]:
    """
    Endpoint de readiness check.

    Verifica se o serviço está pronto para receber tráfego.
    Usado por Kubernetes readiness probe.

    Valida:
    - Variáveis de ambiente críticas
    - Conexão com Vertex AI (via env vars)

    Returns:
        Dict com status e detalhes

    Raises:
        HTTPException: Se serviço não está pronto
    """
    checks: Dict[str, Any] = {
        "status": "ready",
        "timestamp": datetime.now().isoformat(),
        "service": "genaigke-sdlc-aarq-ans-avaliacao-parceiro",
        "checks": {}
    }

    # Check 1: Environment variables
    required_env_vars = [
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_LOCATION",
        "GOOGLE_GENAI_USE_VERTEXAI"
    ]

    env_check_passed = True
    for var in required_env_vars:
        if not os.getenv(var):
            env_check_passed = False
            logger.warning(f"Readiness check failed: missing {var}")

    checks["checks"]["environment_variables"] = {
        "status": "ok" if env_check_passed else "failed",
        "required_vars": required_env_vars,
        "all_present": env_check_passed
    }

    # Check 2: Agent model configuration
    agent_model = os.getenv("AGENT_MODEL", "gemini-2.5-pro")
    checks["checks"]["agent_configuration"] = {
        "status": "ok",
        "model": agent_model
    }

    # Overall status
    if not env_check_passed:
        checks["status"] = "not_ready"
        return checks, 503  # Service Unavailable

    return checks


@post_route('info')
def service_info() -> Dict[str, Any]:
    """
    Endpoint com informações sobre o serviço.

    Retorna metadados úteis para debugging e monitoramento.

    Returns:
        Dict com informações do serviço
    """
    return {
        "service": "genaigke-sdlc-aarq-ans-avaliacao-parceiro",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "agent": {
            "name": os.getenv("AGENT_NAME", "ans_expert_agent"),
            "model": os.getenv("AGENT_MODEL", "gemini-2.5-pro"),
        },
        "vertex_ai": {
            "project": os.getenv("GOOGLE_CLOUD_PROJECT", "not-set"),
            "location": os.getenv("GOOGLE_CLOUD_LOCATION", "not-set"),
            "enabled": os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "not-set")
        },
        "timestamp": datetime.now().isoformat()
    }

