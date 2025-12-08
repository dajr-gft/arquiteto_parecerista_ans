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

"""Unit tests for the Architecture Domain ANS Agent."""

import pytest
from architecture_domain_ans.agent import root_agent

def test_agent_initialization():
    """Test that the agent is initialized correctly."""
    assert root_agent is not None
    assert root_agent.name == 'architecture_domain_ans'
    assert root_agent.model == 'gemini-3-pro-preview'

def test_agent_tools_registration():
    """Test that all expected tools are registered."""
    expected_tools = [
        'integrar_onetrust',
        'consultar_cmdb',
        'carregar_insumos',
        'capturar_vencimento',
        'carregar_ressalvas',
        'sugerir_parecer',
        'registrar_parecer',
    ]
    
    registered_tools = [tool.name for tool in root_agent.tools]
    
    for tool in expected_tools:
        assert tool in registered_tools
