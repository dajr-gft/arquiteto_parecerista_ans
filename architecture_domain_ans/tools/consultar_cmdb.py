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

"""CMDB consultation tool."""

import logging

from ..adapters import get_cmdb_repository

logger = logging.getLogger(__name__)


def consultar_cmdb(api_id: str) -> dict:
    """
    Query CMDB to retrieve service/API data.

    This tool searches the CMDB database for service information including:
    - Service acronym (sigla)
    - Direcionador (Evoluir/Manter/Desinvestir)
    - Service description
    - Technology and version

    Args:
        api_id: Service/API identifier in CMDB

    Returns:
        Dictionary with CMDB data or error message

    Example:
        >>> result = consultar_cmdb("API-001")
        >>> print(result['sigla'])
        'CRM-API'
    """
    logger.info(f"Consulting CMDB for API ID: {api_id}")

    # Get repository (mock or API based on environment)
    repository = get_cmdb_repository()

    try:
        cmdb_data = repository.get(api_id)

        if not cmdb_data:
            return {
                "encontrado": False,
                "api_id": api_id,
                "mensagem": "Serviço/API não encontrado no CMDB",
                "acao_requerida": "Verificar ID do serviço ou cadastrar no CMDB",
            }

        return {
            "encontrado": True,
            "api_id": cmdb_data.api_id,
            "sigla": cmdb_data.sigla,
            "direcionador": cmdb_data.direcionador.value if cmdb_data.direcionador else None,
            "descricao_servico": cmdb_data.descricao_servico,
            "tecnologia": cmdb_data.tecnologia,
            "versao": cmdb_data.versao,
            "responsavel": cmdb_data.responsavel,
        }

    except TimeoutError as e:
        logger.error(f"Timeout querying CMDB: {e}")
        return {
            "encontrado": False,
            "erro": "TIMEOUT",
            "api_id": api_id,
            "mensagem": "CMDB não respondeu no tempo esperado.",
            "acao_requerida": "Aguardar e tentar novamente",
        }

    except ConnectionError as e:
        logger.error(f"Connection error to CMDB: {e}")
        return {
            "encontrado": False,
            "erro": "CONNECTION_ERROR",
            "api_id": api_id,
            "mensagem": "Falha ao conectar com CMDB.",
            "acao_requerida": "Verificar conectividade",
        }

    except Exception as e:
        logger.error(f"Unexpected error querying CMDB: {e}")
        return {
            "encontrado": False,
            "erro": "UNKNOWN",
            "api_id": api_id,
            "mensagem": f"Erro inesperado: {str(e)}",
            "acao_requerida": "Contatar suporte técnico",
        }

