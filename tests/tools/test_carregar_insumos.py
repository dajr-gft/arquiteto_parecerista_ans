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

"""Unit tests for the carregar_insumos tool."""

import os
import pytest
from architecture_domain_ans.tools.carregar_insumos import carregar_insumos

# Ensure we are using mock data
os.environ["USE_MOCK"] = "true"


def test_carregar_insumos_found():
    """Test loading historical inputs with valid CNPJ."""
    # CNPJ from mock_data.py with historical opinions
    cnpj = "12345678000190"
    tipo_servico = "API de CRM"
    
    result = carregar_insumos(cnpj, tipo_servico)
    
    assert result['total_encontrados'] >= 0
    assert 'pareceres_similares' in result
    assert 'padroes_identificados' in result
    assert 'sugestoes_texto' in result


def test_carregar_insumos_with_history():
    """Test loading inputs for CNPJ with known history."""
    cnpj = "98765432000101"  # Has 2 opinions in mock data
    tipo_servico = "Cloud"
    
    result = carregar_insumos(cnpj, tipo_servico)
    
    assert result['total_encontrados'] > 0
    assert len(result['pareceres_similares']) > 0
    
    # Verify structure of returned opinions
    if result['pareceres_similares']:
        parecer = result['pareceres_similares'][0]
        assert 'parecer_id' in parecer
        assert 'tipo_parecer' in parecer
        assert 'justificativa' in parecer


def test_carregar_insumos_no_history():
    """Test loading inputs with no history."""
    cnpj = "00000000000000"  # Non-existent CNPJ
    tipo_servico = "Unknown Service"
    
    result = carregar_insumos(cnpj, tipo_servico)
    
    assert result['total_encontrados'] == 0
    assert result['pareceres_similares'] == []


def test_carregar_insumos_cnpj_formatting():
    """Test CNPJ formatting is handled correctly."""
    cnpj = "12.345.678/0001-90"  # Formatted CNPJ
    tipo_servico = "API"
    
    result = carregar_insumos(cnpj, tipo_servico)
    
    # Should work the same as unformatted CNPJ
    assert 'total_encontrados' in result
    assert 'pareceres_similares' in result
