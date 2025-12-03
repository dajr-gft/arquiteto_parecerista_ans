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

"""Unit tests for the consultar_cmdb tool."""

import os
import pytest
from architecture_domain_ans.tools.consultar_cmdb import consultar_cmdb

# Ensure we are using mock data
os.environ["USE_MOCK"] = "true"

def test_consultar_cmdb_found():
    """Test finding a valid service."""
    # API ID from mock_data.py
    api_id = "API-001"
    result = consultar_cmdb(api_id)
    
    assert result['encontrado'] is True
    assert result['api_id'] == api_id
    assert result['sigla'] == "CRM-API"
    assert result['direcionador'] == "Evoluir"

def test_consultar_cmdb_not_found():
    """Test searching for a non-existent service."""
    api_id = "API-999"
    result = consultar_cmdb(api_id)
    
    assert result['encontrado'] is False
    assert "não encontrado" in result['mensagem']


def test_consultar_cmdb_direcionador_evoluir():
    """Test service with Evoluir direcionador."""
    api_id = "API-001"  # CRM-API with Evoluir
    result = consultar_cmdb(api_id)
    
    assert result['encontrado'] is True
    assert result['direcionador'] == "Evoluir"


def test_consultar_cmdb_direcionador_manter():
    """Test service with Manter direcionador."""
    api_id = "API-002"  # CLOUD-STORAGE with Manter
    result = consultar_cmdb(api_id)
    
    assert result['encontrado'] is True
    assert result['direcionador'] == "Manter"


def test_consultar_cmdb_direcionador_desinvestir():
    """Test service with Desinvestir direcionador."""
    api_id = "API-004"  # LEGACY-SYSTEM with Desinvestir
    result = consultar_cmdb(api_id)
    
    assert result['encontrado'] is True
    assert result['direcionador'] == "Desinvestir"


def test_consultar_cmdb_service_details():
    """Test that all service details are returned."""
    api_id = "API-001"
    result = consultar_cmdb(api_id)
    
    assert result['encontrado'] is True
    assert 'sigla' in result
    assert 'descricao_servico' in result
    assert 'tecnologia' in result
    assert 'versao' in result
    assert 'responsavel' in result
