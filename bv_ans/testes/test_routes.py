"""
Testes unitários para as rotas do agente parecerista
"""
import pytest
from unittest.mock import Mock, patch
import sys
import os
 
# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
 
 
class TestAnalisarParecer:
    """Testes para a rota analisar_parecer"""
   
    @patch('routes.tools.analisar_parecer.Runner')
    @patch('routes.tools.analisar_parecer.LlmAgent')
    def test_analise_com_sucesso(self, mock_agent, mock_runner):
        """Testa análise de parecer com sucesso"""
        # Mock do runner e agente
        mock_runner_instance = Mock()
        mock_runner.return_value = mock_runner_instance
        mock_runner_instance.run.return_value = "Parecer favorável"
       
        # Importa a função da rota
        from routes.tools.analisar_parecer import analisar_parecer_completo

        # Executa
        result, status = analisar_parecer_completo({
            "fornecedor": "Tech Solutions",
            "servico": "API Gateway",
            "tipo_contratacao": "renovacao"
        })
       
        # Verifica
        assert status == 200
        assert "parecer" in result
        assert result["status"] == "sucesso"
   
    def test_analise_sem_dados_obrigatorios(self):
        """Testa análise sem dados obrigatórios"""
        from routes.tools.analisar_parecer import analisar_parecer_completo

        result, status = analisar_parecer_completo({})
       
        assert status == 400
        assert "erro" in result
 
 
class TestConsultarParecer:
    """Testes para a rota consultar_parecer_simples"""
   
    @patch('routes.tools.consultar_parecer_simples.GenerativeModel')
    def test_consulta_simples_sucesso(self, mock_model):
        """Testa consulta simples com sucesso"""
        # Mock do modelo
        mock_response = Mock()
        mock_response.text = "Análise realizada com sucesso"
        mock_model.return_value.generate_content.return_value = mock_response
       
        from routes.tools.consultar_parecer_simples import consultar_parecer_rapido

        result, status = consultar_parecer_rapido({
            "fornecedor": "Tech Corp",
            "servico": "Cloud Storage"
        })
       
        assert status == 200
        assert "resultado" in result
 
 
class TestAnalisarDocumento:
    """Testes para a rota analisar_documento"""
   
    @patch('routes.tools.analisar_documento.GenerativeModel')
    def test_upload_documento_sucesso(self, mock_model):
        """Testa upload e análise de documento com sucesso"""
        mock_response = Mock()
        mock_response.text = '{"parecer": "favoravel", "riscos": []}'
        mock_model.return_value.generate_content.return_value = mock_response
       
        from routes.tools.analisar_documento import analisar_documento_parecer

        # Simula arquivo de texto
        mock_file = Mock()
        mock_file.filename = "doc.txt"
        mock_file.read.return_value = b"Conteudo do documento"
       
        result, status = analisar_documento_parecer(mock_file)
       
        assert status == 200
        assert "analise" in result
   
    def test_upload_tipo_arquivo_invalido(self):
        """Testa upload de tipo de arquivo não permitido"""
        from routes.tools.analisar_documento import analisar_documento_parecer

        mock_file = Mock()
        mock_file.filename = "malware.exe"
       
        result, status = analisar_documento_parecer(mock_file)
       
        assert status == 400
        assert "erro" in result
 
 
class TestConsultarStatus:
    """Testes para a rota de status"""
   
    def test_health_check(self):
        """Testa health check da aplicação"""
        from routes.tools.consultar_status import health_check

        result, status = health_check()
       
        assert status == 200
        assert result["status"] == "healthy"
        assert "versao" in result
 