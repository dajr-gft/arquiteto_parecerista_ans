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

"""Unit tests for the registrar_parecer tool."""

import os
import pytest
from architecture_domain_ans.tools.registrar_parecer import registrar_parecer

# Ensure we are using mock data
os.environ["USE_MOCK"] = "true"


def test_registrar_parecer_success():
    """Test successful opinion registration."""
    dados_completos = {
        "cnpj": "12345678000190",
        "nome_fornecedor": "Tech Solutions LTDA",
        "api_id": "API-001",
        "sigla_servico": "CRM-API",
        "direcionador": "Evoluir",
        "tipo_requisicao": "Renovação",
        "parecer_sugerido": "Parecer Favorável",
        "justificativa": "Fornecedor atende todos os critérios estabelecidos.",
        "ressalvas": [],
        "email_solicitante": "analista@example.com",
        "diretoria_solicitante": "TI",
        "score_confianca": 0.95,
        "criterios_aplicados": ["Histórico positivo"],
        "insumos_utilizados": ["OneTrust", "CMDB"]
    }
    
    result = registrar_parecer(dados_completos)
    
    assert result['sucesso'] is True
    assert 'parecer_id' in result
    assert result['parecer_id'].startswith('PAR-')
    assert 'data_registro' in result
    assert 'status' in result


def test_registrar_parecer_missing_required_fields():
    """Test registration with missing required fields."""
    dados_incompletos = {
        "cnpj": "12345678000190",
        "nome_fornecedor": "Tech Solutions LTDA",
        # Missing: api_id, tipo_requisicao, parecer_sugerido, justificativa
    }
    
    result = registrar_parecer(dados_incompletos)
    
    assert result['sucesso'] is False
    assert result['erro'] == "CAMPOS_OBRIGATORIOS_AUSENTES"
    assert 'campos_faltantes' in result
    assert len(result['campos_faltantes']) > 0


def test_registrar_parecer_minimal_data():
    """Test registration with minimal required data."""
    dados_minimos = {
        "cnpj": "12345678000190",
        "nome_fornecedor": "Tech Solutions LTDA",
        "api_id": "API-001",
        "tipo_requisicao": "Nova Contratação",
        "parecer_sugerido": "Parecer Favorável com Ressalvas",
        "justificativa": "Justificativa mínima.",
    }
    
    result = registrar_parecer(dados_minimos)
    
    assert result['sucesso'] is True
    assert 'parecer_id' in result


def test_registrar_parecer_with_ressalvas():
    """Test registration with observations."""
    dados_com_ressalvas = {
        "cnpj": "12345678000190",
        "nome_fornecedor": "Tech Solutions LTDA",
        "api_id": "API-001",
        "tipo_requisicao": "Renovação",
        "parecer_sugerido": "Parecer Favorável com Ressalvas",
        "justificativa": "Aprovado com ressalvas.",
        "ressalvas": [
            "Documentação deve ser atualizada trimestralmente",
            "SLA deve ser revisado após 6 meses"
        ]
    }
    
    result = registrar_parecer(dados_com_ressalvas)
    
    assert result['sucesso'] is True
    assert result['dados_parecer']['total_ressalvas'] == 2


def test_registrar_parecer_parecer_id_format():
    """Test that parecer_id follows expected format."""
    dados = {
        "cnpj": "12345678000190",
        "nome_fornecedor": "Tech Solutions LTDA",
        "api_id": "API-001",
        "tipo_requisicao": "Renovação",
        "parecer_sugerido": "Parecer Favorável",
        "justificativa": "Teste.",
    }
    
    result = registrar_parecer(dados)
    
    assert result['sucesso'] is True
    # Format: PAR-YYYY-XXXXXXXX
    parecer_id = result['parecer_id']
    parts = parecer_id.split('-')
    assert len(parts) == 3
    assert parts[0] == 'PAR'
    assert len(parts[1]) == 4  # Year
    assert len(parts[2]) == 8  # UUID prefix
