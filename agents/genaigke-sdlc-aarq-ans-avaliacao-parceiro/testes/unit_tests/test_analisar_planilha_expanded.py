"""Testes expandidos para routes/tools/analisar_planilha.py."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from genai_framework.models import FileInput


def test_analisar_planilha_with_csv_success():
    """Test analyzing CSV file successfully."""
    from routes.tools.analisar_planilha import analisar_planilha_parecer

    with patch('routes.tools.analisar_planilha.pd') as mock_pd, \
         patch('routes.tools.analisar_planilha.Client') as mock_client:

        # Mock DataFrame properly
        df_mock = Mock()
        columns_mock = Mock()
        columns_mock.tolist.return_value = ['col1', 'col2']
        columns_mock.__len__ = Mock(return_value=2)  # CRITICAL: add len()
        df_mock.columns = columns_mock
        df_mock.shape = (5, 2)
        df_mock.__len__ = Mock(return_value=5)
        df_mock.head.return_value = df_mock
        df_mock.to_string.return_value = "col1  col2\nval1  val2"
        df_mock.describe.return_value = df_mock

        # Mock select_dtypes to return empty columns
        select_dtypes_mock = Mock()
        select_dtypes_mock.columns = []
        df_mock.select_dtypes.return_value = select_dtypes_mock

        # Mock isnull chain
        isnull_mock = Mock()
        sum_mock = Mock()
        sum_mock.any.return_value = False
        isnull_mock.sum.return_value = sum_mock
        df_mock.isnull.return_value = isnull_mock

        mock_pd.read_csv.return_value = df_mock

        # Mock Gemini Client
        mock_resp = Mock()
        mock_resp.text = '{"parecer": "FAVORÁVEL"}'
        mock_client.return_value.models.generate_content.return_value = mock_resp

        file = FileInput("data.csv", b"col1,col2\nval1,val2")
        result = analisar_planilha_parecer(file)

        assert result is not None
        assert "status" in result
        assert result["status"] == "success"


def test_analisar_planilha_with_xlsx_success():
    """Test analyzing Excel file successfully."""
    from routes.tools.analisar_planilha import analisar_planilha_parecer

    with patch('routes.tools.analisar_planilha.pd') as mock_pd, \
         patch('routes.tools.analisar_planilha.Client') as mock_client:

        # Mock DataFrame properly
        df_mock = Mock()
        columns_mock = Mock()
        columns_mock.tolist.return_value = ['col1', 'col2']
        columns_mock.__len__ = Mock(return_value=2)  # CRITICAL: add len()
        df_mock.columns = columns_mock
        df_mock.shape = (10, 2)
        df_mock.__len__ = Mock(return_value=10)
        df_mock.head.return_value = df_mock
        df_mock.to_string.return_value = "col1  col2\nval1  val2"
        df_mock.describe.return_value = df_mock

        # Mock select_dtypes to return empty columns
        select_dtypes_mock = Mock()
        select_dtypes_mock.columns = []
        df_mock.select_dtypes.return_value = select_dtypes_mock

        # Mock isnull chain
        isnull_mock = Mock()
        sum_mock = Mock()
        sum_mock.any.return_value = False
        isnull_mock.sum.return_value = sum_mock
        df_mock.isnull.return_value = isnull_mock

        # Mock ExcelFile
        excel_mock = Mock()
        excel_mock.sheet_names = ['Sheet1']
        mock_pd.ExcelFile.return_value = excel_mock
        mock_pd.read_excel.return_value = df_mock

        # Mock Gemini Client
        mock_resp = Mock()
        mock_resp.text = '{"parecer": "FAVORÁVEL"}'
        mock_client.return_value.models.generate_content.return_value = mock_resp

        file = FileInput("data.xlsx", b"PK\x03\x04")
        result = analisar_planilha_parecer(file)

        assert result is not None
        assert "status" in result


def test_analisar_planilha_invalid_extension():
    """Test with invalid file extension."""
    from routes.tools.analisar_planilha import analisar_planilha_parecer

    file = FileInput("data.txt", b"text")
    result = analisar_planilha_parecer(file)

    assert isinstance(result, tuple)
    assert result[1] == 400
    assert "error" in result[0]


def test_analisar_planilha_pandas_not_installed():
    """Test when pandas is not installed."""
    from routes.tools.analisar_planilha import analisar_planilha_parecer

    with patch('routes.tools.analisar_planilha.pd', None):
        file = FileInput("data.xlsx", b"PK\x03\x04")
        result = analisar_planilha_parecer(file)

        assert isinstance(result, tuple)
        assert result[1] == 500
        assert "pandas" in result[0]["error"].lower()


def test_analisar_planilha_processing_error():
    """Test handling of processing errors."""
    from routes.tools.analisar_planilha import analisar_planilha_parecer

    with patch('routes.tools.analisar_planilha.pd') as mock_pd:
        mock_pd.read_csv.side_effect = Exception("Processing error")

        file = FileInput("data.csv", b"col1,col2\nval1,val2")
        result = analisar_planilha_parecer(file)

        assert isinstance(result, tuple)
        assert result[1] == 400  # Processing errors return 400


def test_analisar_planilha_multiple_sheets():
    """Test Excel with multiple sheets."""
    from routes.tools.analisar_planilha import analisar_planilha_parecer

    with patch('routes.tools.analisar_planilha.pd') as mock_pd, \
         patch('routes.tools.analisar_planilha.Client') as mock_client:

        df_mock = Mock()
        df_mock.columns = ['col1']
        df_mock.shape = (3, 1)
        df_mock.head.return_value = df_mock
        df_mock.to_string.return_value = "col1\nval1"
        df_mock.describe.return_value = df_mock
        df_mock.__len__ = Mock(return_value=3)

        excel_mock = Mock()
        excel_mock.sheet_names = ['Sheet1', 'Sheet2']
        mock_pd.ExcelFile.return_value = excel_mock
        mock_pd.read_excel.return_value = df_mock
        mock_pd.isna = lambda x: False

        mock_resp = Mock()
        mock_resp.text = '{"parecer": "OK"}'
        mock_client.return_value.models.generate_content.return_value = mock_resp

        file = FileInput("multi.xlsx", b"PK\x03\x04")
        result = analisar_planilha_parecer(file)

        assert result is not None
        # Should call read_excel for each sheet
        assert mock_pd.read_excel.call_count >= 1

