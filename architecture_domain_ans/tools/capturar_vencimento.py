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

"""Contract expiration capture tool."""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def capturar_vencimento(data_vencimento: str, dias_ate_vencimento: int) -> dict:
    """
    Validate if contract expiration date is available and within 2 years.

    Args:
        data_vencimento: Expiration date from OneTrust (ISO format)
        dias_ate_vencimento: Days until expiration

    Returns:
        Dictionary with validation result and alert if needed

    Example:
        >>> result = capturar_vencimento("2025-12-31", 400)
        >>> print(result['status'])
        'OK'
    """
    logger.info(f"Validating contract expiration: {data_vencimento}")

    if not data_vencimento:
        return {
            "status": "BLOQUEIO",
            "data_vencimento": None,
            "dias_ate_vencimento": None,
            "dentro_prazo_2anos": False,
            "alerta": "Data de vencimento não disponível no OneTrust. Cadastro obrigatório.",
            "acao_requerida": "Atualizar OneTrust com data de vencimento do contrato",
        }

    # 2 years = 730 days
    dentro_prazo = dias_ate_vencimento <= 730

    if not dentro_prazo:
        return {
            "status": "ALERTA",
            "data_vencimento": data_vencimento,
            "dias_ate_vencimento": dias_ate_vencimento,
            "dentro_prazo_2anos": False,
            "alerta": f"Contrato vence em {dias_ate_vencimento} dias (>2 anos). Revisar necessidade de parecer.",
            "acao_requerida": "Verificar se renovação antecipada é necessária",
        }

    return {
        "status": "OK",
        "data_vencimento": data_vencimento,
        "dias_ate_vencimento": dias_ate_vencimento,
        "dentro_prazo_2anos": True,
        "alerta": None,
        "acao_requerida": None,
    }

