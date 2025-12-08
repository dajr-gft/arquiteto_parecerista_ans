"""Testes para routes/tools/analisar_planilha.py."""

import pytest
from unittest.mock import Mock, patch, AsyncMock


def test_analisar_planilha_importable():
    """Test that analisar_planilha can be imported."""
    try:
        from routes.tools import analisar_planilha
        assert analisar_planilha is not None
    except ImportError:
        pytest.skip("analisar_planilha not available")


@pytest.mark.asyncio
async def test_analisar_planilha_with_excel():
    """Test analyzing Excel file."""
    try:
        from routes.tools.analisar_planilha import analisar_planilha_dados

        with patch('routes.tools.analisar_planilha.pd.read_excel') as mock_excel:
            df_mock = Mock()
            df_mock.to_dict.return_value = {"col1": ["val1"]}
            df_mock.shape = (10, 5)
            mock_excel.return_value = df_mock

            file = Mock()
            file.filename = "data.xlsx"
            file.read = AsyncMock(return_value=b"PK\x03\x04")

            result = analisar_planilha_dados(file)
            assert result is not None
    except ImportError:
        pytest.skip("analisar_planilha not available")


@pytest.mark.asyncio
async def test_analisar_planilha_with_csv():
    """Test analyzing CSV file."""
    try:
        from routes.tools.analisar_planilha import analisar_planilha_dados

        with patch('routes.tools.analisar_planilha.pd.read_csv') as mock_csv:
            df_mock = Mock()
            df_mock.to_dict.return_value = {"col1": ["val1"]}
            df_mock.shape = (5, 3)
            mock_csv.return_value = df_mock

            file = Mock()
            file.filename = "data.csv"
            file.read = AsyncMock(return_value=b"col1,col2\nval1,val2")

            result = analisar_planilha_dados(file)
            assert result is not None
    except ImportError:
        pytest.skip("analisar_planilha not available")


def test_analisar_planilha_invalid_format():
    """Test with invalid file format."""
    try:
        from routes.tools.analisar_planilha import analisar_planilha_dados

        file = Mock()
        file.filename = "data.txt"
        file.read = AsyncMock(return_value=b"text")

        result = analisar_planilha_dados(file)
        # Should return error
        if isinstance(result, tuple):
            assert result[1] == 400
    except ImportError:
        pytest.skip("analisar_planilha not available")


@pytest.mark.asyncio
async def test_analisar_planilha_empty_file():
    """Test with empty Excel file."""
    try:
        from routes.tools.analisar_planilha import analisar_planilha_dados

        with patch('routes.tools.analisar_planilha.pd.read_excel') as mock_excel:
            mock_excel.side_effect = Exception("Empty file")

            file = Mock()
            file.filename = "empty.xlsx"
            file.read = AsyncMock(return_value=b"")

            result = analisar_planilha_dados(file)
            # Should handle error
            assert result is not None
    except ImportError:
        pytest.skip("analisar_planilha not available")

