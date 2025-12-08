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

"""Pytest configuration and fixtures for Architecture Domain ANS Agent tests."""

import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment before running tests."""
    # Force mock mode for all tests
    os.environ["USE_MOCK"] = "true"
    yield
    # Cleanup after tests if needed


@pytest.fixture
def sample_cnpj():
    """Provide a sample CNPJ for testing."""
    return "12345678000190"


@pytest.fixture
def sample_api_id():
    """Provide a sample API ID for testing."""
    return "API-001"


@pytest.fixture
def sample_onetrust_data():
    """Provide sample OneTrust data for testing."""
    return {
        "cnpj": "12345678000190",
        "nome_fornecedor": "Tech Solutions LTDA",
        "tipo_contrato": "Renovação",
        "data_vencimento_contrato": "2025-12-31",
        "dias_ate_vencimento": 400
    }


@pytest.fixture
def sample_cmdb_data():
    """Provide sample CMDB data for testing."""
    return {
        "api_id": "API-001",
        "sigla": "CRM-API",
        "direcionador": "Evoluir",
        "descricao_servico": "API de integração com CRM",
        "tecnologia": "REST",
        "versao": "2.0"
    }


@pytest.fixture
def sample_parecer_data():
    """Provide sample parecer data for testing."""
    return {
        "cnpj": "12345678000190",
        "nome_fornecedor": "Tech Solutions LTDA",
        "api_id": "API-001",
        "sigla_servico": "CRM-API",
        "direcionador": "Evoluir",
        "tipo_requisicao": "Renovação",
        "parecer_sugerido": "Parecer Favorável",
        "justificativa": "Fornecedor atende todos os critérios.",
        "ressalvas": []
    }


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
