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

"""Pytest configuration and shared fixtures for unit tests."""

import os
import pytest
from datetime import datetime, timedelta
from typing import Dict, List


# ============================================================================
# SESSION FIXTURES - Setup and teardown
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_unit_test_environment():
    """
    Set up unit test environment before running tests.

    Forces mock mode and configures test environment variables.
    """
    # Force mock mode for all unit tests
    os.environ["USE_MOCK"] = "true"
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

    # Set test project ID
    original_project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    os.environ["GOOGLE_CLOUD_PROJECT"] = "test-project-id"

    yield

    # Restore original environment
    if original_project:
        os.environ["GOOGLE_CLOUD_PROJECT"] = original_project
    else:
        os.environ.pop("GOOGLE_CLOUD_PROJECT", None)


# ============================================================================
# SAMPLE DATA FIXTURES - CNPJ and IDs
# ============================================================================

@pytest.fixture
def valid_cnpj() -> str:
    """
    Provide a valid formatted CNPJ for testing.

    Returns:
        str: Valid CNPJ with formatting (12.345.678/0001-90)
    """
    return "12.345.678/0001-90"


@pytest.fixture
def valid_cnpj_clean() -> str:
    """
    Provide a valid clean CNPJ (without formatting) for testing.

    Returns:
        str: Valid CNPJ without formatting (12345678000190)
    """
    return "12345678000190"


@pytest.fixture
def invalid_cnpj() -> str:
    """
    Provide an invalid CNPJ for testing error cases.

    Returns:
        str: Invalid CNPJ
    """
    return "123"


@pytest.fixture
def sample_api_id() -> str:
    """
    Provide a sample API ID for testing.

    Returns:
        str: Sample API identifier
    """
    return "API-CRM-001"


@pytest.fixture
def sample_email() -> str:
    """
    Provide a sample email for testing.

    Returns:
        str: Sample email address
    """
    return "analista.teste@bancobv.com.br"


# ============================================================================
# ONETRUST DATA FIXTURES
# ============================================================================

@pytest.fixture
def onetrust_data_found(valid_cnpj_clean) -> Dict:
    """
    Provide sample OneTrust data for a found supplier.

    Simulates successful OneTrust query with complete supplier data.

    Returns:
        dict: Complete OneTrust supplier data
    """
    future_date = datetime.now() + timedelta(days=90)

    return {
        "encontrado": True,
        "cnpj": valid_cnpj_clean,
        "nome_fornecedor": "Tech Solutions LTDA",
        "tipo_contrato": "Renovação",
        "data_vencimento_contrato": future_date.isoformat(),
        "dias_ate_vencimento": 90,
        "dados_contexto": {
            "contatos": ["contato@techsolutions.com"],
            "categoria": "Serviços de TI"
        },
        "data_ultimo_update": datetime.now().isoformat()
    }


@pytest.fixture
def onetrust_data_not_found(valid_cnpj_clean) -> Dict:
    """
    Provide sample OneTrust data for a supplier not found.

    Simulates OneTrust query where supplier doesn't exist.

    Returns:
        dict: OneTrust not found response
    """
    return {
        "encontrado": False,
        "cnpj": valid_cnpj_clean,
        "mensagem": "Fornecedor não encontrado no OneTrust",
        "acao_requerida": "Cadastrar fornecedor no OneTrust antes de prosseguir"
    }


@pytest.fixture
def onetrust_data_expired_contract(valid_cnpj_clean) -> Dict:
    """
    Provide sample OneTrust data with expired contract.

    Returns:
        dict: OneTrust data with expired contract
    """
    past_date = datetime.now() - timedelta(days=30)

    return {
        "encontrado": True,
        "cnpj": valid_cnpj_clean,
        "nome_fornecedor": "Expired Contract Corp",
        "tipo_contrato": "Renovação",
        "data_vencimento_contrato": past_date.isoformat(),
        "dias_ate_vencimento": -30,
        "dados_contexto": {},
        "data_ultimo_update": datetime.now().isoformat()
    }


# ============================================================================
# CMDB DATA FIXTURES
# ============================================================================

@pytest.fixture
def cmdb_data_evoluir(sample_api_id) -> Dict:
    """
    Provide sample CMDB data with 'Evoluir' direcionador.

    Returns:
        dict: CMDB data for service marked to evolve
    """
    return {
        "encontrado": True,
        "api_id": sample_api_id,
        "sigla": "CRM-API",
        "nome_servico": "API de CRM",
        "direcionador": "Evoluir",
        "descricao": "API de integração com sistema CRM",
        "tecnologia": "REST API",
        "versao": "2.0",
        "owner": "Tecnologia",
        "status": "Ativo"
    }


@pytest.fixture
def cmdb_data_desinvestir(sample_api_id) -> Dict:
    """
    Provide sample CMDB data with 'Desinvestir' direcionador.

    Returns:
        dict: CMDB data for service marked to divest
    """
    return {
        "encontrado": True,
        "api_id": sample_api_id,
        "sigla": "LEGACY-API",
        "nome_servico": "API Legada",
        "direcionador": "Desinvestir",
        "descricao": "API legada a ser descontinuada",
        "tecnologia": "SOAP",
        "versao": "1.0",
        "owner": "Tecnologia",
        "status": "Deprecado"
    }


@pytest.fixture
def cmdb_data_not_found(sample_api_id) -> Dict:
    """
    Provide sample CMDB data for service not found.

    Returns:
        dict: CMDB not found response
    """
    return {
        "encontrado": False,
        "api_id": sample_api_id,
        "mensagem": "Serviço não encontrado no CMDB",
        "acao_requerida": "Verificar ID do serviço ou cadastrar no CMDB"
    }


# ============================================================================
# HISTORICAL DATA FIXTURES
# ============================================================================

@pytest.fixture
def historico_data_favoravel(valid_cnpj_clean) -> Dict:
    """
    Provide sample historical data with favorable opinion.

    Returns:
        dict: Historical data with positive previous opinions
    """
    return {
        "total_encontrados": 2,
        "cnpj": valid_cnpj_clean,
        "pareceres_similares": [
            {
                "parecer_id": "PAR-2024-ABC123",
                "data_parecer": "2024-06-15",
                "tipo_parecer": "Parecer Favorável",
                "tipo_servico": "API CRM",
                "justificativa": "Fornecedor com histórico positivo..."
            },
            {
                "parecer_id": "PAR-2023-XYZ789",
                "data_parecer": "2023-12-20",
                "tipo_parecer": "Parecer Favorável",
                "tipo_servico": "API Marketing",
                "justificativa": "Atende requisitos técnicos..."
            }
        ],
        "padroes_identificados": [
            "Histórico consistente de pareceres favoráveis",
            "Fornecedor com boa capacidade de integração"
        ]
    }


@pytest.fixture
def historico_data_empty(valid_cnpj_clean) -> Dict:
    """
    Provide empty historical data (no previous opinions).

    Returns:
        dict: Empty historical response
    """
    return {
        "total_encontrados": 0,
        "cnpj": valid_cnpj_clean,
        "pareceres_similares": [],
        "padroes_identificados": [],
        "mensagem": "Nenhum parecer anterior encontrado para este fornecedor"
    }


# ============================================================================
# OPINION SUGGESTION FIXTURES
# ============================================================================

@pytest.fixture
def dados_requisicao_favoravel() -> Dict:
    """
    Provide request data that should result in favorable opinion.

    Returns:
        dict: Request data with positive indicators
    """
    return {
        "tipo_requisicao": "Renovação",
        "integracoes_disponiveis": ["REST", "WEBHOOK", "MENSAGERIA"],
        "fluxo_dados": "BIDIRECIONAL",
        "direcionador": "Evoluir",
        "parecer_anterior": "Parecer Favorável",
        "armazena_dados_bv": False
    }


@pytest.fixture
def dados_requisicao_desfavoravel() -> Dict:
    """
    Provide request data that should result in unfavorable opinion.

    Returns:
        dict: Request data with negative indicators
    """
    return {
        "tipo_requisicao": "Nova Contratação",
        "integracoes_disponiveis": [],
        "fluxo_dados": None,
        "direcionador": "Desinvestir",
        "parecer_anterior": None,
        "armazena_dados_bv": True
    }


@pytest.fixture
def dados_requisicao_com_ressalvas() -> Dict:
    """
    Provide request data that should result in opinion with observations.

    Returns:
        dict: Request data with mixed indicators
    """
    return {
        "tipo_requisicao": "Renovação",
        "integracoes_disponiveis": ["REST"],
        "fluxo_dados": "OUTBOUND",
        "direcionador": "Manter",
        "parecer_anterior": "Parecer Favorável com Ressalvas",
        "armazena_dados_bv": True
    }


# ============================================================================
# COMPLETE OPINION REGISTRATION FIXTURES
# ============================================================================

@pytest.fixture
def dados_parecer_completo(valid_cnpj_clean, sample_api_id, sample_email) -> Dict:
    """
    Provide complete opinion data for registration.

    Returns:
        dict: Complete opinion data with all required fields
    """
    return {
        "cnpj": valid_cnpj_clean,
        "nome_fornecedor": "Tech Solutions LTDA",
        "api_id": sample_api_id,
        "sigla_servico": "CRM-API",
        "direcionador": "Evoluir",
        "tipo_requisicao": "Renovação",
        "parecer_sugerido": "Parecer Favorável",
        "justificativa": "Fornecedor atende todos os critérios técnicos e regulatórios...",
        "ressalvas": [],
        "email_solicitante": sample_email,
        "diretoria_solicitante": "Tecnologia",
        "score_confianca": 0.85,
        "criterios_aplicados": [
            "Parecer anterior foi favorável",
            "Múltiplas integrações disponíveis"
        ],
        "insumos_utilizados": [
            "Tipo de requisição: Renovação",
            "Integrações disponíveis: REST, WEBHOOK"
        ]
    }


@pytest.fixture
def dados_parecer_incompleto(valid_cnpj_clean) -> Dict:
    """
    Provide incomplete opinion data for testing validation.

    Returns:
        dict: Opinion data missing required fields
    """
    return {
        "cnpj": valid_cnpj_clean,
        "nome_fornecedor": "Tech Solutions LTDA",
        # Missing required fields: api_id, tipo_requisicao, parecer_sugerido, justificativa
    }


# ============================================================================
# ERROR SCENARIO FIXTURES
# ============================================================================

@pytest.fixture
def timeout_error_response() -> Dict:
    """
    Provide timeout error response for testing error handling.

    Returns:
        dict: Timeout error response
    """
    return {
        "encontrado": False,
        "erro": "TIMEOUT",
        "mensagem": "Serviço não respondeu no tempo esperado",
        "acao_requerida": "Aguardar e tentar novamente"
    }


@pytest.fixture
def connection_error_response() -> Dict:
    """
    Provide connection error response for testing error handling.

    Returns:
        dict: Connection error response
    """
    return {
        "encontrado": False,
        "erro": "CONNECTION_ERROR",
        "mensagem": "Erro ao conectar com o serviço",
        "acao_requerida": "Verificar conectividade de rede"
    }


# ============================================================================
# RESSALVAS (OBSERVATIONS) FIXTURES
# ============================================================================

@pytest.fixture
def sample_ressalvas() -> List[str]:
    """
    Provide sample list of observations/caveats.

    Returns:
        list: Sample observations
    """
    return [
        "Fornecedor armazena dados do Banco BV. Verificar conformidade com LGPD.",
        "Serviço marcado como 'Desinvestir'. Avaliar necessidade de contratação.",
        "Implementar monitoramento adicional de SLA."
    ]


# ============================================================================
# MOCK CONSTANTS
# ============================================================================

@pytest.fixture
def mock_agent_config() -> Dict:
    """
    Provide mock agent configuration for testing.

    Returns:
        dict: Mock agent configuration
    """
    return {
        "model": "gemini-3-pro-preview",
        "name": "architecture_domain_ans",
        "temperature": 1.0,
        "thinking_level": "HIGH"
    }


@pytest.fixture
def mock_project_config() -> Dict:
    """
    Provide mock project configuration.

    Returns:
        dict: Mock project configuration
    """
    return {
        "project_id": "test-project-id",
        "location": "global",
        "use_vertexai": False
    }

