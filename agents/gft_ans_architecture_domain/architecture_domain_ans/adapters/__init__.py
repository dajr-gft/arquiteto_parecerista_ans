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

"""
Repository adapters for Architecture Domain ANS Agent.

This module provides abstraction layer for data access, allowing easy
switching between mock implementations and real APIs.
"""

import logging
import os
from typing import Optional

from .base import (
    CMDBRepository,
    HistoricoRepository,
    OneTrustRepository,
    ParecerRepository,
)

logger = logging.getLogger(__name__)

# Cache for singleton repositories
_onetrust_repo: Optional[OneTrustRepository] = None
_cmdb_repo: Optional[CMDBRepository] = None
_historico_repo: Optional[HistoricoRepository] = None
_parecer_repo: Optional[ParecerRepository] = None


def get_onetrust_repository() -> OneTrustRepository:
    """
    Factory method to create OneTrust repository.

    Returns mock or API implementation based on USE_MOCK environment variable.
    Uses singleton pattern to reuse same instance.

    Returns:
        OneTrustRepository implementation
    """
    global _onetrust_repo

    if _onetrust_repo is None:
        use_mock = os.getenv("USE_MOCK", "true").lower() == "true"

        if use_mock:
            logger.info("Initializing MOCK OneTrust repository")
            from .mock_adapter import MockOneTrustRepository

            _onetrust_repo = MockOneTrustRepository()
        else:
            logger.info("Initializing API OneTrust repository")
            # from .api_adapter import APIOneTrustRepository
            # _onetrust_repo = APIOneTrustRepository()
            raise NotImplementedError("API OneTrust repository not yet implemented")

    return _onetrust_repo


def get_cmdb_repository() -> CMDBRepository:
    """
    Factory method to create CMDB repository.

    Returns mock or API implementation based on USE_MOCK environment variable.
    Uses singleton pattern to reuse same instance.

    Returns:
        CMDBRepository implementation
    """
    global _cmdb_repo

    if _cmdb_repo is None:
        use_mock = os.getenv("USE_MOCK", "true").lower() == "true"

        if use_mock:
            logger.info("Initializing MOCK CMDB repository")
            from .mock_adapter import MockCMDBRepository

            _cmdb_repo = MockCMDBRepository()
        else:
            logger.info("Initializing API CMDB repository")
            # from .api_adapter import APICMDBRepository
            # _cmdb_repo = APICMDBRepository()
            raise NotImplementedError("API CMDB repository not yet implemented")

    return _cmdb_repo


def get_historico_repository() -> HistoricoRepository:
    """
    Factory method to create Historico repository.

    Returns mock or API implementation based on USE_MOCK environment variable.
    Uses singleton pattern to reuse same instance.

    Returns:
        HistoricoRepository implementation
    """
    global _historico_repo

    if _historico_repo is None:
        use_mock = os.getenv("USE_MOCK", "true").lower() == "true"

        if use_mock:
            logger.info("Initializing MOCK Historico repository")
            from .mock_adapter import MockHistoricoRepository

            _historico_repo = MockHistoricoRepository()
        else:
            logger.info("Initializing API Historico repository")
            # from .api_adapter import APIHistoricoRepository
            # _historico_repo = APIHistoricoRepository()
            raise NotImplementedError("API Historico repository not yet implemented")

    return _historico_repo


def get_parecer_repository() -> ParecerRepository:
    """
    Factory method to create Parecer repository.

    Returns mock or API implementation based on USE_MOCK environment variable.
    Uses singleton pattern to reuse same instance.

    Returns:
        ParecerRepository implementation
    """
    global _parecer_repo

    if _parecer_repo is None:
        use_mock = os.getenv("USE_MOCK", "true").lower() == "true"

        if use_mock:
            logger.info("Initializing MOCK Parecer repository")
            from .mock_adapter import MockParecerRepository

            _parecer_repo = MockParecerRepository()
        else:
            logger.info("Initializing API Parecer repository")
            # from .api_adapter import APIParecerRepository
            # _parecer_repo = APIParecerRepository()
            raise NotImplementedError("API Parecer repository not yet implemented")

    return _parecer_repo


__all__ = [
    "get_cmdb_repository",
    "get_historico_repository",
    "get_onetrust_repository",
    "get_parecer_repository",
]

