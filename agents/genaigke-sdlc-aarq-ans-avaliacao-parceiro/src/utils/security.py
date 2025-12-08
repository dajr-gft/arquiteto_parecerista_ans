"""
Utilitários de validação de segurança para arquivos enviados.

Este módulo contém funções para validar segurança de uploads,
incluindo validação de tamanho, MIME type e content filtering.
"""

import os
import logging
from typing import Optional, Set, List
from fastapi import UploadFile, HTTPException

logger = logging.getLogger(__name__)

# Configuration constants for security and validation
MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", str(10 * 1024 * 1024)))  # 10 MB default
MAX_FILES: int = int(os.getenv("MAX_FILES", "5"))  # 5 files max
ALLOWED_MIME_TYPES: Set[str] = {
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/plain',
    'image/png',
    'image/jpeg',
    'image/jpg',
    'image/webp',
    'image/gif'
}
ALLOWED_EXTENSIONS: Set[str] = {'pdf', 'xlsx', 'txt', 'png', 'jpg', 'jpeg', 'webp', 'gif'}
SUSPICIOUS_PATTERNS: List[str] = [
    'ignore previous instructions',
    'ignore all previous',
    'disregard previous',
    'system:',
    '<script>',
    'javascript:',
]


def validate_file_security(file: UploadFile, content: bytes) -> None:
    """
    Valida segurança do arquivo enviado.

    Args:
        file: Arquivo enviado
        content: Conteúdo do arquivo em bytes

    Raises:
        HTTPException: Se validação falhar
    """
    # Validar tamanho do arquivo
    file_size = len(content)
    if file_size > MAX_FILE_SIZE:
        logger.warning(f"File size exceeded: {file.filename} ({file_size} bytes)")
        raise HTTPException(
            status_code=413,
            detail=f"Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE / (1024 * 1024):.1f} MB"
        )

    # Validar MIME type
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        # Verificar também por extensão
        if file.filename:
            ext: str = file.filename.lower().split('.')[-1]
            if ext not in ALLOWED_EXTENSIONS:
                logger.warning(f"Invalid MIME type: {file.filename} ({file.content_type})")
                raise HTTPException(
                    status_code=415,
                    detail=f"Tipo de arquivo não suportado: {file.content_type}"
                )

    # Validar que arquivo não está vazio
    if file_size == 0:
        logger.warning(f"Empty file: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail="Arquivo vazio não é permitido"
        )

    # Content filtering básico - verificar se há tentativas de prompt injection
    if file.content_type == 'text/plain':
        try:
            text_content: str = content.decode('utf-8', errors='ignore')
            text_lower: str = text_content.lower()
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern in text_lower:
                    logger.warning(f"Suspicious content detected in: {file.filename}")
                    raise HTTPException(
                        status_code=400,
                        detail="Conteúdo suspeito detectado no arquivo"
                    )
        except Exception:
            pass  # Se não conseguir decodificar, não é texto e não precisa validar


def validate_files_count(files_count: int) -> None:
    """
    Valida número de arquivos enviados.

    Args:
        files_count: Número de arquivos

    Raises:
        HTTPException: Se exceder limite
    """
    if files_count > MAX_FILES:
        logger.warning(f"Too many files: {files_count} (max: {MAX_FILES})")
        raise HTTPException(
            status_code=400,
            detail=f"Número máximo de arquivos excedido. Máximo: {MAX_FILES}"
        )

