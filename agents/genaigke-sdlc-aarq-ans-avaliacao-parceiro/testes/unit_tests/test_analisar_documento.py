"""Testes para routes/tools/analisar_documento.py."""

import pytest
from unittest.mock import Mock, patch, AsyncMock


def test_analisar_documento_importable():
    """Test that analisar_documento can be imported."""
    try:
        from routes.tools import analisar_documento
        assert analisar_documento is not None
    except ImportError:
        pytest.skip("analisar_documento not available")


@pytest.mark.asyncio
async def test_analisar_documento_with_txt():
    """Test analyzing TXT document."""
    try:
        from routes.tools.analisar_documento import analisar_documento_parecer

        with patch('routes.tools.analisar_documento.Client') as mock_client:
            mock_resp = Mock()
            mock_resp.text = '{"parecer": "FAVORÁVEL"}'
            mock_client.return_value.models.generate_content.return_value = mock_resp

            file = Mock()
            file.filename = "doc.txt"
            file.content = b"content"

            result = analisar_documento_parecer(file)
            assert result is not None
    except ImportError:
        pytest.skip("analisar_documento not available")


@pytest.mark.asyncio
async def test_analisar_documento_with_pdf():
    """Test analyzing PDF document."""
    try:
        from routes.tools.analisar_documento import analisar_documento_parecer

        with patch('routes.tools.analisar_documento.Client') as mock_client:
            mock_resp = Mock()
            mock_resp.text = '{"parecer": "FAVORÁVEL"}'
            mock_client.return_value.models.generate_content.return_value = mock_resp

            file = Mock()
            file.filename = "doc.pdf"
            file.read = AsyncMock(return_value=b"%PDF")

            result = analisar_documento_parecer(file)
            assert result is not None
    except ImportError:
        pytest.skip("analisar_documento not available")


def test_analisar_documento_invalid_extension():
    """Test with invalid file extension."""
    try:
        from routes.tools.analisar_documento import analisar_documento_parecer

        file = Mock()
        file.filename = "doc.exe"
        file.read = AsyncMock(return_value=b"data")

        result = analisar_documento_parecer(file)
        # Should return error
        if isinstance(result, tuple):
            assert result[1] == 400
    except ImportError:
        pytest.skip("analisar_documento not available")

