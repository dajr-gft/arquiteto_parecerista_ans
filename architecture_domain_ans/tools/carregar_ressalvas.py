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

"""Load previous opinion observations tool."""

import logging

from ..adapters import get_historico_repository

logger = logging.getLogger(__name__)


def carregar_ressalvas(cnpj: str) -> dict:
    """
    Load observations from previous opinion to include in current one.

    Args:
        cnpj: Supplier CNPJ (14 digits, can include formatting)

    Returns:
        Dictionary with previous observations or empty if none found

    Example:
        >>> result = carregar_ressalvas("12345678000190")
        >>> print(result['tem_ressalvas'])
        True
    """
    # Normalize CNPJ
    cnpj_clean = cnpj.replace(".", "").replace("/", "").replace("-", "")

    logger.info(f"Loading previous observations for CNPJ: {cnpj_clean}")

    # Get repository (mock or API based on environment)
    repository = get_historico_repository()

    try:
        parecer_anterior = repository.get_last_parecer(cnpj_clean)

        if not parecer_anterior:
            return {
                "tem_ressalvas": False,
                "parecer_anterior_encontrado": False,
                "ressalvas": [],
                "mensagem": "Nenhum parecer anterior encontrado para este fornecedor",
            }

        if not parecer_anterior.ressalvas:
            return {
                "tem_ressalvas": False,
                "parecer_anterior_encontrado": True,
                "ressalvas": [],
                "parecer_anterior": {
                    "parecer_id": parecer_anterior.parecer_id,
                    "data_parecer": parecer_anterior.data_parecer,
                    "tipo_parecer": parecer_anterior.tipo_parecer.value,
                },
                "mensagem": "Parecer anterior não continha ressalvas",
            }

        return {
            "tem_ressalvas": True,
            "parecer_anterior_encontrado": True,
            "ressalvas": parecer_anterior.ressalvas,
            "parecer_anterior": {
                "parecer_id": parecer_anterior.parecer_id,
                "data_parecer": parecer_anterior.data_parecer,
                "tipo_parecer": parecer_anterior.tipo_parecer.value,
                "justificativa": parecer_anterior.justificativa,
            },
            "acao_requerida": "Incluir ressalvas anteriores no parecer atual se ainda aplicáveis",
        }

    except Exception as e:
        logger.error(f"Error loading previous observations: {e}")
        return {
            "tem_ressalvas": False,
            "parecer_anterior_encontrado": False,
            "ressalvas": [],
            "erro": str(e),
        }

