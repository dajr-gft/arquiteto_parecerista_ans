"""
Módulo de autenticação via API Keys (OPCIONAL).

Este módulo implementa autenticação adicional via API Keys para proteger
os endpoints do agente ANS.

IMPORTANTE: Este módulo é OPCIONAL e desabilitado por padrão.
- Se rodando no GCP com Vertex AI, a autenticação é feita via Service Account (IAM)
- API Keys são úteis apenas para ambientes externos ou controle adicional por cliente

Para HABILITAR autenticação via API Key:
1. Defina a variável de ambiente: ENABLE_API_KEY_AUTH=true
2. Defina as API keys válidas: API_KEYS=key1,key2,key3
"""

import os
import secrets
import logging
from typing import Optional
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

logger = logging.getLogger(__name__)

# Verifica se autenticação via API Key está habilitada
ENABLE_API_KEY_AUTH = os.getenv("ENABLE_API_KEY_AUTH", "false").lower() == "true"

# Header para API Key
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Carrega API keys válidas do ambiente (apenas se habilitado)
# Formato: API_KEYS=key1,key2,key3
VALID_API_KEYS = set(
    key.strip()
    for key in os.getenv("API_KEYS", "").split(",")
    if key.strip()
) if ENABLE_API_KEY_AUTH else set()


def generate_api_key() -> str:
    """
    Gera uma nova API key segura.

    Returns:
        str: API key gerada (32 caracteres hexadecimais)

    Example:
        >>> key = generate_api_key()
        >>> print(key)
        'a1b2c3d4e5f6...'  # 64 caracteres
    """
    return secrets.token_urlsafe(32)


async def verify_api_key(api_key: str = Security(api_key_header)) -> Optional[str]:
    """
    Verifica se a API key fornecida é válida.

    IMPORTANTE: Se ENABLE_API_KEY_AUTH=false (padrão), esta função retorna None
    e permite todas as requisições (confia no IAM do GCP).

    Args:
        api_key: API key fornecida no header X-API-Key

    Returns:
        Optional[str]: API key validada ou None se autenticação desabilitada

    Raises:
        HTTPException: 401 se API key ausente (quando habilitado), 403 se inválida

    Example:
        ```python
        @post_route('protected_endpoint')
        async def protected(api_key: str = Depends(verify_api_key)):
            # Se api_key for None, autenticação está desabilitada
            # Confia no IAM do GCP/Vertex AI
            ...
        ```
    """
    # Se autenticação via API Key está desabilitada, permitir acesso
    if not ENABLE_API_KEY_AUTH:
        logger.debug("API Key authentication disabled - relying on GCP IAM")
        return None

    # Verificar se API key foi fornecida
    if not api_key:
        logger.warning("API key missing in request (auth enabled)")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key ausente. Forneça via header 'X-API-Key'",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # Verificar se há keys configuradas
    if not VALID_API_KEYS:
        logger.error("API key auth enabled but no keys configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Servidor não configurado corretamente. Contate o administrador.",
        )

    # Verificar se a key é válida
    if api_key not in VALID_API_KEYS:
        logger.warning(f"Invalid API key attempt: {api_key[:8]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida. Verifique suas credenciais.",
        )

    logger.info(f"API key validated successfully: {api_key[:8]}...")
    return api_key


def is_authentication_enabled() -> bool:
    """
    Verifica se autenticação via API Key está habilitada.

    Returns:
        bool: True se ENABLE_API_KEY_AUTH=true e há API keys configuradas

    Note:
        Por padrão retorna False, confiando na autenticação do GCP (IAM/Vertex AI)
    """
    return ENABLE_API_KEY_AUTH and bool(VALID_API_KEYS)

