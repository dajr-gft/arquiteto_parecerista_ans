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

"""Unit tests for the sugerir_parecer tool."""

import pytest
from architecture_domain_ans.tools.sugerir_parecer import sugerir_parecer

def test_sugerir_parecer_favoravel():
    """Test suggesting a favorable opinion."""
    dados_requisicao = {
        "tipo_requisicao": "Renovação",
        "integracoes_disponiveis": ["REST", "WEBHOOK", "MENSAGERIA"],
        "fluxo_dados": "BIDIRECIONAL",
        "direcionador": "Evoluir",
        "parecer_anterior": "Parecer Favorável",
        "armazena_dados_bv": False
    }
    
    result = sugerir_parecer(dados_requisicao)
    
    assert result['parecer_sugerido'] == "Parecer Favorável"
    assert "Requisição atende todos os critérios" in result['justificativa']

def test_sugerir_parecer_desfavoravel_cmdb():
    """Test suggesting an unfavorable opinion due to CMDB driver."""
    dados_requisicao = {
        "tipo_requisicao": "Renovação",
        "integracoes_disponiveis": [],
        "fluxo_dados": "INBOUND",
        "direcionador": "Desinvestir",
        "parecer_anterior": "Parecer Favorável",
        "armazena_dados_bv": False
    }
    
    result = sugerir_parecer(dados_requisicao)
    
    # Score calculation:
    # Start: 0.5
    # Renovação + Favorável: +0.3 => 0.8
    # Fluxo INBOUND: +0.1 => 0.9
    # Desinvestir: -0.2 => 0.7
    # Result: 0.7 => Favorável com Ressalvas (>= 0.5)
    
    # Wait, let's re-read the logic.
    # If score >= 0.8: Favorável
    # If score >= 0.5: Favorável com Ressalvas
    # Else: Desfavorável
    
    # To get Desfavorável, we need score < 0.5.
    
    # Let's try to lower the score.
    dados_requisicao_low = {
        "tipo_requisicao": "Nova Contratação", # No bonus
        "integracoes_disponiveis": [],
        "fluxo_dados": None,
        "direcionador": "Desinvestir", # -0.2
        "parecer_anterior": None,
        "armazena_dados_bv": True # -0.1
    }
    # Start: 0.5
    # Desinvestir: -0.2 => 0.3
    # Armazena BV: -0.1 => 0.2
    # Result: 0.2 => Desfavorável
    
    result = sugerir_parecer(dados_requisicao_low)
    
    assert result['parecer_sugerido'] == "Parecer Desfavorável"
    assert "Requisição não atende critérios mínimos" in result['justificativa']
    assert any("Desinvestir" in r for r in result['ressalvas'])

def test_sugerir_parecer_ressalvas():
    """Test suggesting an opinion with reservations."""
    dados_requisicao = {
        "tipo_requisicao": "Renovação",
        "integracoes_disponiveis": ["REST"], # +0.1
        "fluxo_dados": "INBOUND", # +0.1
        "direcionador": "Manter", # +0.05
        "parecer_anterior": "Parecer Favorável com Ressalvas", # +0.15
        "armazena_dados_bv": True # -0.1
    }
    
    # Start: 0.5
    # Renovação + Ressalvas: +0.15 => 0.65
    # Integracoes: +0.1 => 0.75
    # Modern tech (REST): +0.1 => 0.85
    # Fluxo: +0.1 => 0.95
    # Manter: +0.05 => 1.0
    # Armazena BV: -0.1 => 0.9
    
    # This is getting too high. Let's adjust to target 0.5 - 0.79 range.
    
    dados_requisicao_mid = {
        "tipo_requisicao": "Nova Contratação", # 0
        "integracoes_disponiveis": ["SOAP"], # +0.1 (>=1)
        "fluxo_dados": "INBOUND", # +0.1
        "direcionador": "Manter", # +0.05
        "parecer_anterior": None,
        "armazena_dados_bv": False
    }
    # Start: 0.5
    # SOAP: +0.1 => 0.6
    # INBOUND: +0.1 => 0.7
    # Manter: +0.05 => 0.75
    # Result: 0.75 => Favorável com Ressalvas
    
    result = sugerir_parecer(dados_requisicao_mid)
    
    assert result['parecer_sugerido'] == "Parecer Favorável com Ressalvas"
