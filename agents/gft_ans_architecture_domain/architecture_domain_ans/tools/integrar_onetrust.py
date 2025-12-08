# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""OneTrust integration tool for context retrieval."""

import logging
from datetime import datetime

from ..adapters import get_onetrust_repository

logger = logging.getLogger(__name__)


def integrar_onetrust(cnpj: str) -> dict:
    """
    Query OneTrust to retrieve supplier context data.

    This tool searches the OneTrust database for supplier information including:
    - Contract expiration date
    - Contract type (Renewal/New)
    - Supplier context data

    Implementation uses repository pattern - automatically switches between
    mock and API based on USE_MOCK environment variable.

    Args:
        cnpj: Supplier CNPJ (14 digits, can include formatting)

    Returns:
        Dictionary with OneTrust context data or error message

    Example:
        >>> result = integrar_onetrust("12345678000190")
        >>> print(result['data_vencimento_contrato'])
        '2025-12-31'
    """
    # Normalize CNPJ
    cnpj_clean = cnpj.replace(".", "").replace("/", "").replace("-", "")

    logger.info(f"Integrating with OneTrust for CNPJ: {cnpj_clean}")

    # Get repository (mock or API based on environment)
    repository = get_onetrust_repository()

    try:
        onetrust_data = repository.get(cnpj_clean)

        if not onetrust_data:
            return {
                "encontrado": False,
                "cnpj": cnpj_clean,
                "mensagem": "Fornecedor não encontrado no OneTrust",
                "acao_requerida": "Cadastrar fornecedor no OneTrust antes de prosseguir",
            }

        # Calculate days until expiration if date is available
        dias_ate_vencimento = None
        if onetrust_data.data_vencimento_contrato:
            delta = onetrust_data.data_vencimento_contrato - datetime.now()
            dias_ate_vencimento = delta.days

        return {
            "encontrado": True,
            "cnpj": onetrust_data.cnpj,
            "nome_fornecedor": onetrust_data.nome_fornecedor,
            "tipo_contrato": onetrust_data.tipo_contrato,
            "data_vencimento_contrato": (
                onetrust_data.data_vencimento_contrato.isoformat()
                if onetrust_data.data_vencimento_contrato
                else None
            ),
            "dias_ate_vencimento": dias_ate_vencimento,
            "dados_contexto": onetrust_data.dados_contexto,
            "data_ultimo_update": onetrust_data.data_ultimo_update,
        }

    except TimeoutError as e:
        logger.error(f"Timeout querying OneTrust: {e}")
        return {
            "encontrado": False,
            "erro": "TIMEOUT",
            "cnpj": cnpj_clean,
            "mensagem": "OneTrust não respondeu no tempo esperado. Tente novamente em alguns minutos.",
            "acao_requerida": "Aguardar e tentar novamente",
        }

    except ConnectionError as e:
        logger.error(f"Connection error to OneTrust: {e}")
        return {
            "encontrado": False,
            "erro": "CONNECTION_ERROR",
            "cnpj": cnpj_clean,
            "mensagem": "Falha ao conectar com OneTrust. Verifique conectividade.",
            "acao_requerida": "Verificar conectividade e tentar novamente",
        }

    except Exception as e:
        logger.error(f"Unexpected error querying OneTrust: {e}")
        return {
            "encontrado": False,
            "erro": "UNKNOWN",
            "cnpj": cnpj_clean,
            "mensagem": f"Erro inesperado ao consultar OneTrust: {str(e)}",
            "acao_requerida": "Contatar suporte técnico",
        }

