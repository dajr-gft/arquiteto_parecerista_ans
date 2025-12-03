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

"""Integration tests for the Architecture Domain ANS Agent."""

import os
import pytest

# Ensure we are using mock data
os.environ["USE_MOCK"] = "true"

from architecture_domain_ans.tools.integrar_onetrust import integrar_onetrust
from architecture_domain_ans.tools.consultar_cmdb import consultar_cmdb
from architecture_domain_ans.tools.carregar_insumos import carregar_insumos
from architecture_domain_ans.tools.carregar_ressalvas import carregar_ressalvas
from architecture_domain_ans.tools.sugerir_parecer import sugerir_parecer
from architecture_domain_ans.tools.registrar_parecer import registrar_parecer


def test_integration_renewal_with_positive_history():
    """Test complete flow for renewal with positive history."""
    cnpj = "12345678000190"
    api_id = "API-001"
    
    # Step 1: Get OneTrust data
    onetrust_result = integrar_onetrust(cnpj)
    assert onetrust_result['encontrado'] is True
    
    # Step 2: Get CMDB data
    cmdb_result = consultar_cmdb(api_id)
    assert cmdb_result['encontrado'] is True
    
    # Step 3: Load historical inputs
    insumos_result = carregar_insumos(cnpj, "API de CRM")
    
    # Step 4: Load previous observations
    ressalvas_result = carregar_ressalvas(cnpj)
    
    # Step 5: Suggest opinion
    dados_requisicao = {
        "tipo_requisicao": "Renovação",
        "integracoes_disponiveis": ["REST", "WEBHOOK"],
        "fluxo_dados": "BIDIRECIONAL",
        "direcionador": cmdb_result['direcionador'],
        "parecer_anterior": "Parecer Favorável",
        "armazena_dados_bv": False
    }
    parecer_result = sugerir_parecer(dados_requisicao)
    assert parecer_result['parecer_sugerido'] in ["Parecer Favorável", "Parecer Favorável com Ressalvas"]
    
    # Step 6: Register opinion
    dados_completos = {
        "cnpj": cnpj,
        "nome_fornecedor": onetrust_result['nome_fornecedor'],
        "api_id": api_id,
        "sigla_servico": cmdb_result['sigla'],
        "direcionador": cmdb_result['direcionador'],
        "tipo_requisicao": "Renovação",
        "parecer_sugerido": parecer_result['parecer_sugerido'],
        "justificativa": parecer_result['justificativa'],
        "ressalvas": parecer_result['ressalvas'],
    }
    registro_result = registrar_parecer(dados_completos)
    assert registro_result['sucesso'] is True


def test_integration_new_contract():
    """Test complete flow for new contract."""
    cnpj = "11222333000144"
    api_id = "API-003"
    
    # Step 1: Get OneTrust data
    onetrust_result = integrar_onetrust(cnpj)
    assert onetrust_result['encontrado'] is True
    
    # Step 2: Get CMDB data
    cmdb_result = consultar_cmdb(api_id)
    assert cmdb_result['encontrado'] is True
    
    # Step 3: Suggest opinion for new contract
    dados_requisicao = {
        "tipo_requisicao": "Nova Contratação",
        "integracoes_disponiveis": ["GraphQL"],
        "fluxo_dados": "BIDIRECIONAL",
        "direcionador": cmdb_result['direcionador'],
        "parecer_anterior": None,
        "armazena_dados_bv": False
    }
    parecer_result = sugerir_parecer(dados_requisicao)
    assert parecer_result['parecer_sugerido'] is not None


def test_integration_desinvestir_scenario():
    """Test complete flow with Desinvestir direcionador."""
    cnpj = "12345678000190"
    api_id = "API-004"  # LEGACY-SYSTEM with Desinvestir
    
    # Step 1: Get CMDB data
    cmdb_result = consultar_cmdb(api_id)
    assert cmdb_result['encontrado'] is True
    assert cmdb_result['direcionador'] == "Desinvestir"
    
    # Step 2: Suggest opinion
    dados_requisicao = {
        "tipo_requisicao": "Renovação",
        "integracoes_disponiveis": [],
        "fluxo_dados": None,
        "direcionador": cmdb_result['direcionador'],
        "parecer_anterior": None,
        "armazena_dados_bv": False
    }
    parecer_result = sugerir_parecer(dados_requisicao)
    
    # Should have ressalvas about Desinvestir
    assert any("Desinvestir" in r for r in parecer_result['ressalvas'])


def test_integration_with_ressalvas():
    """Test complete flow with previous observations."""
    cnpj = "98765432000101"  # Has previous opinion with ressalvas
    api_id = "API-002"
    
    # Step 1: Load previous observations
    ressalvas_result = carregar_ressalvas(cnpj)
    assert ressalvas_result['tem_ressalvas'] is True
    
    # Step 2: Get CMDB data
    cmdb_result = consultar_cmdb(api_id)
    assert cmdb_result['encontrado'] is True
    
    # Step 3: Suggest opinion considering previous ressalvas
    dados_requisicao = {
        "tipo_requisicao": "Renovação",
        "integracoes_disponiveis": ["S3-Compatible"],
        "fluxo_dados": "BIDIRECIONAL",
        "direcionador": cmdb_result['direcionador'],
        "parecer_anterior": "Parecer Favorável com Ressalvas",
        "armazena_dados_bv": False
    }
    parecer_result = sugerir_parecer(dados_requisicao)
    
    # Should suggest Favorável com Ressalvas due to history
    assert "Ressalvas" in parecer_result['parecer_sugerido'] or parecer_result['parecer_sugerido'] == "Parecer Favorável"
