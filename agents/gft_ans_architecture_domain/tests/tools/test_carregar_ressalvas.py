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

"""Unit tests for the carregar_ressalvas tool."""

import os
import pytest
from architecture_domain_ans.tools.carregar_ressalvas import carregar_ressalvas

# Ensure we are using mock data
os.environ["USE_MOCK"] = "true"


def test_carregar_ressalvas_with_ressalvas():
    """Test loading observations with previous opinion that has ressalvas."""
    # CNPJ from mock_data.py with ressalvas
    cnpj = "98765432000101"
    
    result = carregar_ressalvas(cnpj)
    
    assert result['tem_ressalvas'] is True
    assert result['parecer_anterior_encontrado'] is True
    assert len(result['ressalvas']) > 0
    assert 'parecer_anterior' in result
    assert 'acao_requerida' in result


def test_carregar_ressalvas_no_previous_opinion():
    """Test loading with no previous opinion."""
    cnpj = "00000000000000"  # Non-existent CNPJ
    
    result = carregar_ressalvas(cnpj)
    
    assert result['tem_ressalvas'] is False
    assert result['parecer_anterior_encontrado'] is False
    assert result['ressalvas'] == []
    assert "Nenhum parecer anterior" in result['mensagem']


def test_carregar_ressalvas_no_ressalvas():
    """Test loading with previous opinion but no observations."""
    # CNPJ with opinion but no ressalvas
    cnpj = "12345678000190"
    
    result = carregar_ressalvas(cnpj)
    
    assert result['tem_ressalvas'] is False
    assert result['parecer_anterior_encontrado'] is True
    assert result['ressalvas'] == []
    assert 'parecer_anterior' in result
    assert "não continha ressalvas" in result['mensagem']


def test_carregar_ressalvas_cnpj_formatting():
    """Test CNPJ formatting is handled correctly."""
    cnpj = "98.765.432/0001-01"  # Formatted CNPJ
    
    result = carregar_ressalvas(cnpj)
    
    # Should work the same as unformatted CNPJ
    assert 'tem_ressalvas' in result
    assert 'parecer_anterior_encontrado' in result


def test_carregar_ressalvas_structure():
    """Test the structure of returned data."""
    cnpj = "98765432000101"
    
    result = carregar_ressalvas(cnpj)
    
    # Verify all required fields are present
    assert 'tem_ressalvas' in result
    assert 'parecer_anterior_encontrado' in result
    assert 'ressalvas' in result
    
    if result['parecer_anterior_encontrado']:
        assert 'parecer_anterior' in result
        parecer = result['parecer_anterior']
        assert 'parecer_id' in parecer
        assert 'tipo_parecer' in parecer
