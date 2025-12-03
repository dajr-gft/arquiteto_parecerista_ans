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

"""Unit tests for the capturar_vencimento tool."""

import pytest
from architecture_domain_ans.tools.capturar_vencimento import capturar_vencimento


def test_capturar_vencimento_ok():
    """Test contract expiration within 2 years (OK status)."""
    data_vencimento = "2025-12-31"
    dias_ate_vencimento = 400  # ~13 months
    
    result = capturar_vencimento(data_vencimento, dias_ate_vencimento)
    
    assert result['status'] == "OK"
    assert result['dentro_prazo_2anos'] is True
    assert result['data_vencimento'] == data_vencimento
    assert result['dias_ate_vencimento'] == dias_ate_vencimento
    assert result['alerta'] is None


def test_capturar_vencimento_alerta():
    """Test contract expiration beyond 2 years (ALERTA status)."""
    data_vencimento = "2027-12-31"
    dias_ate_vencimento = 900  # ~30 months
    
    result = capturar_vencimento(data_vencimento, dias_ate_vencimento)
    
    assert result['status'] == "ALERTA"
    assert result['dentro_prazo_2anos'] is False
    assert result['data_vencimento'] == data_vencimento
    assert result['dias_ate_vencimento'] == dias_ate_vencimento
    assert "2 anos" in result['alerta']


def test_capturar_vencimento_bloqueio():
    """Test missing expiration date (BLOQUEIO status)."""
    data_vencimento = None
    dias_ate_vencimento = None
    
    result = capturar_vencimento(data_vencimento, dias_ate_vencimento)
    
    assert result['status'] == "BLOQUEIO"
    assert result['dentro_prazo_2anos'] is False
    assert result['data_vencimento'] is None
    assert "não disponível" in result['alerta']
    assert "Atualizar OneTrust" in result['acao_requerida']


def test_capturar_vencimento_edge_case_730_days():
    """Test edge case: exactly 730 days (2 years)."""
    data_vencimento = "2026-12-31"
    dias_ate_vencimento = 730
    
    result = capturar_vencimento(data_vencimento, dias_ate_vencimento)
    
    assert result['status'] == "OK"
    assert result['dentro_prazo_2anos'] is True


def test_capturar_vencimento_edge_case_731_days():
    """Test edge case: 731 days (just over 2 years)."""
    data_vencimento = "2027-01-01"
    dias_ate_vencimento = 731
    
    result = capturar_vencimento(data_vencimento, dias_ate_vencimento)
    
    assert result['status'] == "ALERTA"
    assert result['dentro_prazo_2anos'] is False
