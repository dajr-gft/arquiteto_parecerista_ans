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

"""Mock adapter implementations - wraps existing mock functionality."""

import logging
import uuid
from datetime import datetime
from typing import Optional

from .base import (
    CMDBRepository,
    HistoricoRepository,
    OneTrustRepository,
    ParecerRepository,
)
from ..mock import (
    get_cmdb_data,
    get_last_parecer,
    get_onetrust_contexto,
    search_pareceres_similares,
)
from ..models import CMDBData, InsumoHistorico, OneTrustContexto, ParecerAnterior

logger = logging.getLogger(__name__)


class MockOneTrustRepository(OneTrustRepository):
    """Mock implementation of OneTrust repository using existing mock data."""

    def get(self, cnpj: str) -> Optional[OneTrustContexto]:
        """
        Retrieve supplier context data from mock database.

        Args:
            cnpj: Supplier CNPJ (14 digits)

        Returns:
            OneTrustContexto if found, None otherwise
        """
        logger.info(f"[MOCK] Querying OneTrust context for CNPJ: {cnpj}")
        return get_onetrust_contexto(cnpj)


class MockCMDBRepository(CMDBRepository):
    """Mock implementation of CMDB repository using existing mock data."""

    def get(self, api_id: str) -> Optional[CMDBData]:
        """
        Retrieve service data from mock CMDB database.

        Args:
            api_id: Service/API identifier

        Returns:
            CMDBData if found, None otherwise
        """
        logger.info(f"[MOCK] Querying CMDB for API ID: {api_id}")
        return get_cmdb_data(api_id)


class MockHistoricoRepository(HistoricoRepository):
    """Mock implementation of Historico repository using existing mock data."""

    def get_last_parecer(self, cnpj: str) -> Optional[ParecerAnterior]:
        """
        Retrieve last opinion from mock database.

        Args:
            cnpj: Supplier CNPJ (14 digits)

        Returns:
            ParecerAnterior if found, None otherwise
        """
        logger.info(f"[MOCK] Querying last opinion for CNPJ: {cnpj}")
        return get_last_parecer(cnpj)

    def search(self, cnpj: str, tipo_servico: str, limit: int = 5) -> InsumoHistorico:
        """
        Search for similar opinions in mock database.

        Args:
            cnpj: Supplier CNPJ (14 digits)
            tipo_servico: Type of service
            limit: Maximum number of results

        Returns:
            InsumoHistorico with similar opinions
        """
        logger.info(
            f"[MOCK] Searching similar opinions for CNPJ: {cnpj}, "
            f"service: {tipo_servico}, limit: {limit}"
        )
        return search_pareceres_similares(cnpj, tipo_servico, limit)


class MockParecerRepository(ParecerRepository):
    """Mock implementation of Parecer repository - simulates registration."""

    def save(self, dados: dict) -> dict:
        """
        Simulate opinion registration.

        Args:
            dados: Complete opinion data

        Returns:
            Registration confirmation with generated ID
        """
        logger.info("[MOCK] Registering opinion (simulated)")

        parecer_id = f"PAR-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"

        return {
            "sucesso": True,
            "parecer_id": parecer_id,
            "data_registro": datetime.now().isoformat(),
            "status": "REGISTRADO",
            "proximo_status": "AGUARDANDO_REVISAO_ANALISTA",
        }

