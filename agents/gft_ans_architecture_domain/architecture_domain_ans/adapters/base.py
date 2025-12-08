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

"""Base repository interfaces for data access abstraction."""

from abc import ABC, abstractmethod
from typing import Optional, List

from ..models import (
    OneTrustContexto,
    CMDBData,
    ParecerAnterior,
    InsumoHistorico,
)


class OneTrustRepository(ABC):
    """
    Abstract repository for OneTrust data access.

    Implementations can use mock data, REST API, GraphQL, database, etc.
    """

    @abstractmethod
    def get(self, cnpj: str) -> Optional[OneTrustContexto]:
        """
        Retrieve supplier context data from OneTrust.

        Args:
            cnpj: Supplier CNPJ (normalized, 14 digits)

        Returns:
            OneTrustContexto if found, None otherwise

        Raises:
            TimeoutError: If request times out
            ConnectionError: If connection fails
            ValueError: If API returns error
        """
        pass


class CMDBRepository(ABC):
    """
    Abstract repository for CMDB data access.

    Implementations can use mock data, REST API, database, etc.
    """

    @abstractmethod
    def get(self, api_id: str) -> Optional[CMDBData]:
        """
        Retrieve service data from CMDB.

        Args:
            api_id: Service/API identifier in CMDB

        Returns:
            CMDBData if found, None otherwise

        Raises:
            TimeoutError: If request times out
            ConnectionError: If connection fails
            ValueError: If API returns error
        """
        pass


class HistoricoRepository(ABC):
    """
    Abstract repository for opinion history data access.

    Implementations can use mock data, REST API, database, etc.
    """

    @abstractmethod
    def get_last_parecer(self, cnpj: str) -> Optional[ParecerAnterior]:
        """
        Retrieve last opinion for supplier.

        Args:
            cnpj: Supplier CNPJ (normalized, 14 digits)

        Returns:
            ParecerAnterior if found, None otherwise

        Raises:
            TimeoutError: If request times out
            ConnectionError: If connection fails
        """
        pass

    @abstractmethod
    def search(self, cnpj: str, tipo_servico: str, limit: int = 5) -> InsumoHistorico:
        """
        Search for similar historical opinions.

        Args:
            cnpj: Supplier CNPJ (normalized, 14 digits)
            tipo_servico: Type of service
            limit: Maximum number of results

        Returns:
            InsumoHistorico with similar opinions

        Raises:
            TimeoutError: If request times out
            ConnectionError: If connection fails
        """
        pass


class ParecerRepository(ABC):
    """
    Abstract repository for opinion registration.

    Implementations can use mock data, REST API, database, etc.
    """

    @abstractmethod
    def save(self, dados: dict) -> dict:
        """
        Persist opinion data in the system.

        Args:
            dados: Complete opinion data to persist

        Returns:
            Dictionary with:
                - sucesso: bool
                - parecer_id: str
                - data_registro: str (ISO8601)
                - status: str

        Raises:
            TimeoutError: If request times out
            ConnectionError: If connection fails
            ValueError: If data validation fails
        """
        pass

