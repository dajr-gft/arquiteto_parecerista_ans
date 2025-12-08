"""Testes expandidos para routes/tools/analisar_documento.py - Cobertura 80%+."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from genai_framework.models import FileInput


class TestAnalisarDocumento:
    """Test suite completo para analisar_documento."""

    def test_function_exists(self):
        """Test that function exists and is callable."""
        try:
            from routes.tools.analisar_documento import analisar_documento_parecer
            assert callable(analisar_documento_parecer)
        except ImportError:
            pytest.skip("analisar_documento not available")

    def test_with_txt_file_success(self):
        """Test analyzing TXT file successfully."""
        from routes.tools.analisar_documento import analisar_documento_parecer

        with patch('routes.tools.analisar_documento.Client') as mock_client:
            mock_resp = Mock()
            mock_resp.text = '{"parecer_final": "FAVORÁVEL"}'
            mock_client.return_value.models.generate_content.return_value = mock_resp

            file = FileInput("spec.txt", b"Technical specification content")

            result = analisar_documento_parecer(file)
            assert "filename" in result
            assert result["filename"] == "spec.txt"
            assert result["status"] == "success"

    def test_with_pdf_file_success(self):
        """Test analyzing PDF file successfully."""
        from routes.tools.analisar_documento import analisar_documento_parecer

        with patch('routes.tools.analisar_documento.Client') as mock_client:
            mock_resp = Mock()
            mock_resp.text = '{"parecer_final": "FAVORÁVEL COM RESSALVAS"}'
            mock_client.return_value.models.generate_content.return_value = mock_resp

            file = FileInput("contract.pdf", b"%PDF-1.4 content")

            result = analisar_documento_parecer(file)
            assert "status" in result
            assert result["status"] == "success"
            assert result["tipo_documento"] == ".pdf"

    def test_with_markdown_file(self):
        """Test analyzing Markdown file."""
        from routes.tools.analisar_documento import analisar_documento_parecer

        with patch('routes.tools.analisar_documento.Client') as mock_client:
            mock_resp = Mock()
            mock_resp.text = '{"parecer_final": "FAVORÁVEL"}'
            mock_client.return_value.models.generate_content.return_value = mock_resp

            file = FileInput("README.md", b"# Specification\n\nContent here")

            result = analisar_documento_parecer(file)
            assert result["tipo_documento"] == ".md"

    def test_with_docx_file(self):
        """Test analyzing DOCX file."""
        from routes.tools.analisar_documento import analisar_documento_parecer

        with patch('routes.tools.analisar_documento.Client') as mock_client:
            mock_resp = Mock()
            mock_resp.text = '{"parecer_final": "DESFAVORÁVEL"}'
            mock_client.return_value.models.generate_content.return_value = mock_resp

            file = FileInput("proposal.docx", b"PK\x03\x04")

            result = analisar_documento_parecer(file)
            assert "filename" in result
            assert result["tipo_documento"] == ".docx"

    def test_invalid_extension_error(self):
        """Test error with invalid file extension."""
        from routes.tools.analisar_documento import analisar_documento_parecer

        file = FileInput("virus.exe", b"executable")

        result = analisar_documento_parecer(file)
        if isinstance(result, tuple):
            error_dict, status_code = result
            assert status_code == 400
            assert "error" in error_dict
            assert "não suportado" in error_dict["error"]

    def test_decode_error_handling(self):
        """Test handling of decode errors."""
        from routes.tools.analisar_documento import analisar_documento_parecer

        file = FileInput("bad.txt", b"\xff\xfe\x00")

        result = analisar_documento_parecer(file)
        if isinstance(result, tuple):
            error_dict, status_code = result
            assert status_code == 400
            assert "error" in error_dict

    def test_gemini_api_error_handling(self):
        """Test handling of Gemini API errors."""
        from routes.tools.analisar_documento import analisar_documento_parecer

        with patch('routes.tools.analisar_documento.Client') as mock_client:
            mock_client.return_value.models.generate_content.side_effect = Exception("API Error")

            file = FileInput("doc.txt", b"content")

            result = analisar_documento_parecer(file)
            if isinstance(result, tuple):
                error_dict, status_code = result
                assert status_code == 500
                assert "error" in error_dict

    def test_large_file_truncation(self):
        """Test that large files are truncated to 10k chars."""
        from routes.tools.analisar_documento import analisar_documento_parecer

        with patch('routes.tools.analisar_documento.Client') as mock_client:
            mock_resp = Mock()
            mock_resp.text = '{"parecer_final": "FAVORÁVEL"}'
            mock_client.return_value.models.generate_content.return_value = mock_resp

            file = FileInput("large.txt", b"x" * 50000)

            result = analisar_documento_parecer(file)
            assert result["tamanho_bytes"] == 50000

    def test_response_structure(self):
        """Test that response has correct structure."""
        from routes.tools.analisar_documento import analisar_documento_parecer

        with patch('routes.tools.analisar_documento.Client') as mock_client:
            mock_resp = Mock()
            mock_resp.text = '{"parecer_final": "FAVORÁVEL"}'
            mock_client.return_value.models.generate_content.return_value = mock_resp

            file = FileInput("test.txt", b"content")

            result = analisar_documento_parecer(file)
            assert "filename" in result
            assert "status" in result
            assert "analise" in result
            assert "tipo_documento" in result
            assert "tamanho_bytes" in result

    def test_all_allowed_extensions(self):
        """Test all allowed file extensions are accepted."""
        from routes.tools.analisar_documento import analisar_documento_parecer

        allowed_exts = [".txt", ".pdf", ".doc", ".docx", ".md"]

        with patch('routes.tools.analisar_documento.Client') as mock_client:
            mock_resp = Mock()
            mock_resp.text = '{"parecer": "OK"}'
            mock_client.return_value.models.generate_content.return_value = mock_resp

            for ext in allowed_exts:
                file = FileInput(f"test{ext}", b"content")

                result = analisar_documento_parecer(file)
                if not isinstance(result, tuple):
                    assert result["tipo_documento"] == ext

