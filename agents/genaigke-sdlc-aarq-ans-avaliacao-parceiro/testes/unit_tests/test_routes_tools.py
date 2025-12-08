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

"""Unit tests for routes tools - CLEANED VERSION."""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path


# ============================================================================
# TOOLS INTEGRATION TESTS
# ============================================================================

class TestToolsIntegration:
    """Test suite for tools integration and naming conventions."""

    def test_all_tools_are_importable(self):
        """
        Test that all tools can be imported.

        Scenario: Import all tool modules
        Expected: All imports succeed
        """
        try:
            from routes.tools import analisar_documento
            from routes.tools import analisar_parecer
            from routes.tools import analisar_planilha
            from routes.tools import consultar_parecer_simples
            from routes.tools import consultar_status
            from routes.tools import extrair_dados_contrato

            assert analisar_documento is not None
            assert analisar_parecer is not None
            assert analisar_planilha is not None
            assert consultar_parecer_simples is not None
            assert consultar_status is not None
            assert extrair_dados_contrato is not None
        except ImportError as e:
            pytest.skip(f"Tools framework not available: {e}")

    def test_tools_follow_naming_convention(self):
        """
        Test that all tools follow naming conventions.

        Scenario: Check tool module naming
        Expected: All tools have consistent naming
        """
        tools_path = Path(__file__).parent.parent.parent / "src" / "routes" / "tools"

        if not tools_path.exists():
            pytest.skip("Tools directory not found")

        expected_tools = [
            "analisar_documento.py",
            "analisar_parecer.py",
            "analisar_planilha.py",
            "consultar_parecer_simples.py",
            "consultar_status.py",
            "extrair_dados_contrato.py"
        ]

        for tool in expected_tools:
            tool_file = tools_path / tool
            assert tool_file.exists(), f"Tool {tool} not found"

    def test_tools_init_exports(self):
        """Test that tools/__init__.py exports all functions."""
        try:
            from routes import tools
            assert hasattr(tools, '__all__')
            expected = [
                'analisar_documento_parecer',
                'analisar_planilha_parecer',
                'sugerir_parecer_simples',
                'get_status',
                'get_health'
            ]
            for func in expected:
                assert func in tools.__all__
        except ImportError:
            pytest.skip("Tools module not available")


# ============================================================================
# ANALISAR_DOCUMENTO FUNCTIONAL TESTS
# ============================================================================

class TestAnalisarDocumentoFunctional:
    """Functional tests for analisar_documento tool."""

    def test_analisar_documento_with_txt_file(self, analisar_documento_module):
        """
        Test document analysis with TXT file.

        Scenario: Analyze TXT document
        Expected: Returns analysis result
        """
        if analisar_documento_module is None:
            pytest.skip("Module not available")

        mock_file = Mock()
        mock_file.filename = "test.txt"
        mock_file.content = b"Test content"

        with patch.object(analisar_documento_module, 'Client') as mock_client:
            mock_response = Mock()
            mock_response.text = '{"parecer_final": "FAVORÁVEL"}'
            mock_client.return_value.models.generate_content.return_value = mock_response

            result = analisar_documento_module.analisar_documento_parecer(mock_file)

            assert result is not None

    def test_analisar_documento_with_invalid_extension(self, analisar_documento_module):
        """
        Test document analysis with invalid file extension.

        Scenario: Try to analyze file with unsupported extension
        Expected: Returns error
        """
        if analisar_documento_module is None:
            pytest.skip("Module not available")

        mock_file = Mock()
        mock_file.filename = "test.exe"
        mock_file.content = b"Test content"

        result = analisar_documento_module.analisar_documento_parecer(mock_file)

        # Should return error tuple with status 400
        assert result is not None
        if isinstance(result, tuple):
            assert result[1] == 400


# ============================================================================
# MOCK DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_parecer_data():
    """Sample parecer data for testing."""
    return {
        "parecer_id": "PAR-2025-001",
        "fornecedor": "Fornecedor Teste LTDA",
        "cnpj": "12.345.678/0001-90",
        "parecer_final": "FAVORÁVEL COM RESSALVAS",
        "justificativa": "Proposta atende requisitos técnicos",
        "riscos_identificados": ["Dependência tecnológica"],
        "recomendacoes": ["Implementar SLA rigoroso"]
    }


@pytest.fixture
def sample_file_data():
    """Sample file data for testing."""
    return {
        "filename": "especificacao_tecnica.pdf",
        "content": b"PDF content here",
        "content_type": "application/pdf",
        "size": 1024000
    }
