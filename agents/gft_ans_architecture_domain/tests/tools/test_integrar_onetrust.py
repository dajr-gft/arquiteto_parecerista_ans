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

"""Unit tests for the integrar_onetrust tool."""

import os
import pytest
from architecture_domain_ans.tools.integrar_onetrust import integrar_onetrust

# Ensure we are using mock data
os.environ["USE_MOCK"] = "true"

def test_integrar_onetrust_found():
    """Test finding a valid supplier."""
    # CNPJ from mock_data.py
    cnpj = "12345678000190"
    result = integrar_onetrust(cnpj)
    
    assert result['encontrado'] is True
    assert result['cnpj'] == cnpj
    assert result['nome_fornecedor'] == "Tech Solutions LTDA"
    assert result['tipo_contrato'] == "Renovação"

def test_integrar_onetrust_not_found():
    """Test searching for a non-existent supplier."""
    cnpj = "00000000000000"
    result = integrar_onetrust(cnpj)
    
    assert result['encontrado'] is False
    assert "não encontrado" in result['mensagem']

def test_integrar_onetrust_formatting():
    """Test that CNPJ formatting is handled correctly."""
    # CNPJ with formatting
    cnpj = "12.345.678/0001-90"
    result = integrar_onetrust(cnpj)
    
    assert result['encontrado'] is True
    assert result['cnpj'] == "12345678000190"


def test_integrar_onetrust_expiration_calculation():
    """Test that days until expiration is calculated."""
    cnpj = "12345678000190"
    result = integrar_onetrust(cnpj)
    
    assert result['encontrado'] is True
    assert 'dias_ate_vencimento' in result
    assert result['dias_ate_vencimento'] is not None
    assert isinstance(result['dias_ate_vencimento'], int)


def test_integrar_onetrust_missing_expiration():
    """Test supplier with missing expiration date."""
    cnpj = "11222333000144"  # Has None expiration in mock data
    result = integrar_onetrust(cnpj)
    
    assert result['encontrado'] is True
    assert result['data_vencimento_contrato'] is None
    assert result['dias_ate_vencimento'] is None
