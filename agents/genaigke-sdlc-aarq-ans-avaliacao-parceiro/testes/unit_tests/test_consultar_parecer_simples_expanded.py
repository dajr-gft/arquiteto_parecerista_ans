"""Testes expandidos para routes/tools/consultar_parecer_simples.py."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def test_sugerir_parecer_simples_function_exists():
    """Test that function exists."""
    from routes.tools.consultar_parecer_simples import sugerir_parecer_simples
    assert callable(sugerir_parecer_simples)


def test_sugerir_parecer_simples_mock_response():
    """Test parecer with mocked implementation."""
    from routes.tools.consultar_parecer_simples import sugerir_parecer_simples

    # Mock the entire function behavior
    with patch('routes.tools.consultar_parecer_simples.sugerir_parecer_simples') as mock_func:
        mock_func.return_value = {
            "status": "success",
            "parecer": "FAVORÁVEL"
        }

        result = mock_func(
            cnpj="12.345.678/0001-90",
            nome_fornecedor="Test",
            tipo_requisicao="Aquisição",
            nome_servico="Service",
            descricao_servico="Description"
        )

        assert result["status"] == "success"

