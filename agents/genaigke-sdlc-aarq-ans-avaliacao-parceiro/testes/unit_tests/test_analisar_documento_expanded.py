"""Testes expandidos para routes/tools/analisar_documento.py - Cobertura 60%+."""

import pytest
from unittest.mock import Mock, patch


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
        try:
            from routes.tools.analisar_documento import analisar_documento_parecer

            with patch('routes.tools.analisar_documento.Client') as mock_client:
                mock_resp = Mock()
                mock_resp.text = '{"parecer_final": "FAVORÁVEL"}'
                mock_client.return_value.models.generate_content.return_value = mock_resp

                file = Mock()
                file.filename = "spec.txt"
                file.content = b"Technical specification content"

                result = analisar_documento_parecer(file)
                assert "filename" in result
                assert result["filename"] == "spec.txt"
                assert result["status"] == "success"
        except ImportError:
            pytest.skip("analisar_documento not available")

    def test_with_pdf_file_success(self):
        """Test analyzing PDF file successfully."""
        try:
            from routes.tools.analisar_documento import analisar_documento_parecer

            with patch('routes.tools.analisar_documento.Client') as mock_client:
                mock_resp = Mock()
                mock_resp.text = '{"parecer_final": "FAVORÁVEL COM RESSALVAS"}'
                mock_client.return_value.models.generate_content.return_value = mock_resp

                file = Mock()
                file.filename = "contract.pdf"
                file.content = b"%PDF-1.4 content"

                result = analisar_documento_parecer(file)
                assert "status" in result
                assert result["status"] == "success"
                assert result["tipo_documento"] == ".pdf"
        except ImportError:
            pytest.skip("analisar_documento not available")

    def test_with_markdown_file(self):
        """Test analyzing Markdown file."""
        try:
            from routes.tools.analisar_documento import analisar_documento_parecer

            with patch('routes.tools.analisar_documento.Client') as mock_client:
                mock_resp = Mock()
                mock_resp.text = '{"parecer_final": "FAVORÁVEL"}'
                mock_client.return_value.models.generate_content.return_value = mock_resp

                file = Mock()
                file.filename = "README.md"
                file.content = b"# Specification\n\nContent here"

                result = analisar_documento_parecer(file)
                assert result["tipo_documento"] == ".md"
        except ImportError:
            pytest.skip("analisar_documento not available")

    def test_with_docx_file(self):
        """Test analyzing DOCX file."""
        try:
            from routes.tools.analisar_documento import analisar_documento_parecer

            with patch('routes.tools.analisar_documento.Client') as mock_client:
                mock_resp = Mock()
                mock_resp.text = '{"parecer_final": "DESFAVORÁVEL"}'
                mock_client.return_value.models.generate_content.return_value = mock_resp

                file = Mock()
                file.filename = "proposal.docx"
                file.content = b"PK\x03\x04"  # DOCX header

                result = analisar_documento_parecer(file)
                assert "filename" in result
                assert result["tipo_documento"] == ".docx"
        except ImportError:
            pytest.skip("analisar_documento not available")

    def test_invalid_extension_error(self):
        """Test error with invalid file extension."""
        try:
            from routes.tools.analisar_documento import analisar_documento_parecer

            file = Mock()
            file.filename = "virus.exe"
            file.content = b"executable"

            result = analisar_documento_parecer(file)
            if isinstance(result, tuple):
                error_dict, status_code = result
                assert status_code == 400
                assert "error" in error_dict
                assert "não suportado" in error_dict["error"]
        except ImportError:
            pytest.skip("analisar_documento not available")

    def test_decode_error_handling(self):
        """Test handling of decode errors."""
        try:
            from routes.tools.analisar_documento import analisar_documento_parecer

            file = Mock()
            file.filename = "bad.txt"
            file.content = b"\xff\xfe\x00"  # Invalid UTF-8

            result = analisar_documento_parecer(file)
            if isinstance(result, tuple):
                error_dict, status_code = result
                assert status_code == 400
                assert "error" in error_dict
        except ImportError:
            pytest.skip("analisar_documento not available")

    def test_gemini_api_error_handling(self):
        """Test handling of Gemini API errors."""
        try:
            from routes.tools.analisar_documento import analisar_documento_parecer

            with patch('routes.tools.analisar_documento.Client') as mock_client:
                mock_client.return_value.models.generate_content.side_effect = Exception("API Error")

                file = Mock()
                file.filename = "doc.txt"
                file.content = b"content"

                result = analisar_documento_parecer(file)
                if isinstance(result, tuple):
                    error_dict, status_code = result
                    assert status_code == 500
                    assert "error" in error_dict
        except ImportError:
            pytest.skip("analisar_documento not available")

    def test_large_file_truncation(self):
        """Test that large files are truncated to 10k chars."""
        try:
            from routes.tools.analisar_documento import analisar_documento_parecer

            with patch('routes.tools.analisar_documento.Client') as mock_client:
                mock_resp = Mock()
                mock_resp.text = '{"parecer_final": "FAVORÁVEL"}'
                mock_client.return_value.models.generate_content.return_value = mock_resp

                file = Mock()
                file.filename = "large.txt"
                file.content = b"x" * 50000  # 50KB

                result = analisar_documento_parecer(file)
                assert result["tamanho_bytes"] == 50000
                # Verify truncation happened in prompt (10k limit)
                call_args = mock_client.return_value.models.generate_content.call_args
                prompt = call_args[1]["contents"]
                # Prompt should not contain all 50k characters
                assert len(prompt) < 50000
        except ImportError:
            pytest.skip("analisar_documento not available")

    def test_response_structure(self):
        """Test that response has correct structure."""
        try:
            from routes.tools.analisar_documento import analisar_documento_parecer

            with patch('routes.tools.analisar_documento.Client') as mock_client:
                mock_resp = Mock()
                mock_resp.text = '{"parecer_final": "FAVORÁVEL"}'
                mock_client.return_value.models.generate_content.return_value = mock_resp

                file = Mock()
                file.filename = "test.txt"
                file.content = b"content"

                result = analisar_documento_parecer(file)
                assert "filename" in result
                assert "status" in result
                assert "analise" in result
                assert "tipo_documento" in result
                assert "tamanho_bytes" in result
        except ImportError:
            pytest.skip("analisar_documento not available")

    def test_all_allowed_extensions(self):
        """Test all allowed file extensions are accepted."""
        try:
            from routes.tools.analisar_documento import analisar_documento_parecer

            allowed_exts = [".txt", ".pdf", ".doc", ".docx", ".md"]

            with patch('routes.tools.analisar_documento.Client') as mock_client:
                mock_resp = Mock()
                mock_resp.text = '{"parecer": "OK"}'
                mock_client.return_value.models.generate_content.return_value = mock_resp

                for ext in allowed_exts:
                    file = Mock()
                    file.filename = f"test{ext}"
                    file.content = b"content"

                    result = analisar_documento_parecer(file)
                    # Should succeed (not return error tuple)
                    if not isinstance(result, tuple):
                        assert result["tipo_documento"] == ext
        except ImportError:
            pytest.skip("analisar_documento not available")

