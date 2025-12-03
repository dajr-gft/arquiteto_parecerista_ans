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

"""Load historical inputs tool."""

import logging

from ..adapters import get_historico_repository

logger = logging.getLogger(__name__)


def carregar_insumos(cnpj: str, tipo_servico: str) -> dict:
    """
    Load historical opinion inputs for reference and pattern analysis.

    This tool searches for similar historical opinions to provide:
    - Similar previous opinions
    - Identified patterns
    - Text suggestions based on history

    Args:
        cnpj: Supplier CNPJ (14 digits, can include formatting)
        tipo_servico: Type of service for similarity matching

    Returns:
        Dictionary with historical inputs or empty if none found

    Example:
        >>> result = carregar_insumos("12345678000190", "API CRM")
        >>> print(result['total_encontrados'])
        2
    """
    # Normalize CNPJ
    cnpj_clean = cnpj.replace(".", "").replace("/", "").replace("-", "")

    logger.info(f"Loading historical inputs for CNPJ: {cnpj_clean}, service: {tipo_servico}")

    # Get repository (mock or API based on environment)
    repository = get_historico_repository()

    try:
        insumos = repository.search(cnpj_clean, tipo_servico, limit=5)

        return {
            "total_encontrados": insumos.total_encontrados,
            "pareceres_similares": [
                {
                    "parecer_id": p.parecer_id,
                    "data_parecer": p.data_parecer,
                    "tipo_parecer": p.tipo_parecer.value,
                    "justificativa": p.justificativa,
                    "ressalvas": p.ressalvas,
                    "analista": p.analista,
                }
                for p in insumos.pareceres_similares
            ],
            "padroes_identificados": insumos.padroes_identificados,
            "sugestoes_texto": insumos.sugestoes_texto,
        }

    except Exception as e:
        logger.error(f"Error loading historical inputs: {e}")
        return {
            "total_encontrados": 0,
            "pareceres_similares": [],
            "padroes_identificados": [],
            "sugestoes_texto": [],
            "erro": str(e),
        }

