"""
Utilitários de auditoria e logging estruturado.

Este módulo contém funções para registrar auditoria de requisições
e respostas para compliance e rastreabilidade.
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


def log_request_audit(
    request_id: str,
    user_id: str,
    session_id: str,
    text_length: int,
    files_count: int,
    files_info: List[Dict[str, Any]]
) -> None:
    """
    Registra auditoria da requisição para compliance.

    Args:
        request_id: ID único da requisição
        user_id: ID do usuário
        session_id: ID da sessão
        text_length: Tamanho do texto enviado
        files_count: Número de arquivos
        files_info: Informações dos arquivos
    """
    audit_data: Dict[str, Any] = {
        "request_id": request_id,
        "user_id": user_id,
        "session_id": session_id,
        "timestamp": datetime.utcnow().isoformat(),
        "text_length": text_length,
        "files_count": files_count,
        "files_info": files_info
    }

    logger.info(
        "REQUEST_AUDIT",
        extra=audit_data
    )


def log_response_audit(
    request_id: str,
    session_id: str,
    response_length: int,
    processing_time: float,
    success: bool,
    error: Optional[str] = None
) -> None:
    """
    Registra auditoria da resposta para compliance.

    Args:
        request_id: ID único da requisição
        session_id: ID da sessão
        response_length: Tamanho da resposta
        processing_time: Tempo de processamento em segundos
        success: Se foi bem-sucedido
        error: Mensagem de erro se houver
    """
    logger.info(
        "RESPONSE_AUDIT",
        extra={
            "request_id": request_id,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "response_length": response_length,
            "processing_time_seconds": processing_time,
            "success": success,
            "error": error
        }
    )

