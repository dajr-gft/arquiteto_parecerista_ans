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

"""Register opinion tool."""

import logging
import uuid
from datetime import datetime

from ..adapters import get_parecer_repository

logger = logging.getLogger(__name__)


def registrar_parecer(dados_completos: dict) -> dict:
    """
    Register complete opinion in the system.

    Persists all opinion data including suggested type, justification,
    observations, and metadata.

    Args:
        dados_completos: Complete opinion data including:
            - cnpj: Supplier CNPJ
            - nome_fornecedor: Supplier name
            - api_id: Service ID in CMDB
            - sigla_servico: Service acronym
            - direcionador: Service direcionador
            - tipo_requisicao: Request type
            - parecer_sugerido: Suggested opinion type
            - justificativa: Justification
            - ressalvas: List of observations
            - email_solicitante: Requester email
            - diretoria_solicitante: Requester directorate

    Returns:
        Dictionary with registration confirmation

    Example:
        >>> result = registrar_parecer({...})
        >>> print(result['parecer_id'])
        'PAR-2025-A1B2C3D4'
    """
    logger.info("Registering complete opinion")

    # Validate required fields
    required_fields = [
        "cnpj",
        "nome_fornecedor",
        "api_id",
        "tipo_requisicao",
        "parecer_sugerido",
        "justificativa",
    ]

    missing_fields = [field for field in required_fields if not dados_completos.get(field)]

    if missing_fields:
        return {
            "sucesso": False,
            "erro": "CAMPOS_OBRIGATORIOS_AUSENTES",
            "mensagem": f"Campos obrigatórios ausentes: {', '.join(missing_fields)}",
            "campos_faltantes": missing_fields,
        }

    # Generate unique ID
    parecer_id = f"PAR-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"

    # Prepare data for persistence
    parecer_data = {
        "parecer_id": parecer_id,
        "cnpj": dados_completos["cnpj"],
        "nome_fornecedor": dados_completos["nome_fornecedor"],
        "api_id": dados_completos["api_id"],
        "sigla_servico": dados_completos.get("sigla_servico"),
        "direcionador": dados_completos.get("direcionador"),
        "tipo_requisicao": dados_completos["tipo_requisicao"],
        "parecer_sugerido": dados_completos["parecer_sugerido"],
        "justificativa": dados_completos["justificativa"],
        "ressalvas": dados_completos.get("ressalvas", []),
        "data_parecer": datetime.now().isoformat(),
        "analista": "Agente IA - Parecerista ANS",
        "email_solicitante": dados_completos.get("email_solicitante"),
        "diretoria_solicitante": dados_completos.get("diretoria_solicitante"),
        "metadata": {
            "score_confianca": dados_completos.get("score_confianca"),
            "criterios_aplicados": dados_completos.get("criterios_aplicados", []),
            "insumos_utilizados": dados_completos.get("insumos_utilizados", []),
            "versao_agente": "1.0",
        },
    }

    # Get repository (mock or API based on environment)
    repository = get_parecer_repository()

    try:
        result = repository.save(parecer_data)

        if result.get("sucesso"):
            return {
                "sucesso": True,
                "parecer_id": result["parecer_id"],
                "data_registro": result["data_registro"],
                "status": result["status"],
                "proximo_status": result.get("proximo_status"),
                "mensagem": f"Parecer registrado com sucesso: {result['parecer_id']}",
                "dados_parecer": {
                    "tipo_parecer": dados_completos["parecer_sugerido"],
                    "sigla_servico": dados_completos.get("sigla_servico"),
                    "direcionador": dados_completos.get("direcionador"),
                    "total_ressalvas": len(dados_completos.get("ressalvas", [])),
                },
            }
        else:
            return {
                "sucesso": False,
                "erro": "FALHA_REGISTRO",
                "mensagem": "Falha ao registrar parecer no sistema",
                "detalhes": result,
            }

    except TimeoutError as e:
        logger.error(f"Timeout registering opinion: {e}")
        return {
            "sucesso": False,
            "erro": "TIMEOUT",
            "mensagem": "Sistema não respondeu no tempo esperado",
            "acao_requerida": "Tentar novamente ou registrar manualmente",
        }

    except ConnectionError as e:
        logger.error(f"Connection error registering opinion: {e}")
        return {
            "sucesso": False,
            "erro": "CONNECTION_ERROR",
            "mensagem": "Falha ao conectar com sistema de registro",
            "acao_requerida": "Verificar conectividade",
        }

    except Exception as e:
        logger.error(f"Unexpected error registering opinion: {e}")
        return {
            "sucesso": False,
            "erro": "UNKNOWN",
            "mensagem": f"Erro inesperado: {str(e)}",
            "acao_requerida": "Contatar suporte técnico",
        }

