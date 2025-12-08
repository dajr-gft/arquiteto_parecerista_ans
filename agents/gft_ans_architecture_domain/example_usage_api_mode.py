#!/usr/bin/env python3
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

"""Example usage of the Architecture Domain ANS Agent - API Mode.

This example demonstrates how to use the agent in API mode, where it processes
structured JSON payloads and returns structured responses without interactive prompts.
"""

import asyncio
import json
import os
import sys

import vertexai
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

from architecture_domain_ans.agent import root_agent

# Load environment variables
load_dotenv()

# Configure UTF-8 output for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def format_json_payload(data: dict) -> str:
    """Format dictionary as JSON string for API-style input."""
    return json.dumps(data, ensure_ascii=False, indent=2)


def validate_response_structure(response_text: str) -> dict:
    """Validate if response contains expected JSON structure.

    Args:
        response_text: The agent's response text

    Returns:
        dict with validation results
    """
    validation = {
        "is_json": False,
        "has_status": False,
        "has_parecer_id": False,
        "has_parecer_sugerido": False,
        "has_sigla_servico": False,
        "has_direcionador": False,
        "has_justificativa": False,
        "issues": []
    }

    try:
        # Try to find JSON in response
        import re
        json_match = re.search(r'\{[\s\S]*}', response_text)
        if json_match:
            response_json = json.loads(json_match.group())
            validation["is_json"] = True

            # Validate required fields
            validation["has_status"] = "sucesso" in response_json
            validation["has_parecer_id"] = "parecer_id" in response_json
            validation["has_parecer_sugerido"] = "parecer_sugerido" in response_json
            validation["has_sigla_servico"] = "sigla_servico" in response_json
            validation["has_direcionador"] = "direcionador" in response_json
            validation["has_justificativa"] = "justificativa" in response_json

            # Check for issues
            if not validation["has_status"]:
                validation["issues"].append("Missing 'sucesso' field")
            if not validation["has_parecer_sugerido"]:
                validation["issues"].append("Missing 'parecer_sugerido' field")

            return validation
    except json.JSONDecodeError:
        validation["issues"].append("Response is not valid JSON")
    except Exception as e:
        validation["issues"].append(f"Validation error: {str(e)}")

    return validation


async def example_1_renovacao_favoravel():
    """Example 1: Renewal with positive history - Parecer Favorável."""

    print("="*80)
    print("Example 1: Renovação com Histórico Positivo - Parecer Favorável (API Mode)")
    print("="*80)

    # Prepare payload in API format
    payload = {
        "solicitante": {
            "email": "analista.arquitetura@bancobv.com.br",
            "diretoria": "Arquitetura e Tecnologia"
        },
        "request": {
            "cnpj": "12345678000190",
            "nome_fornecedor": "Tech Solutions LTDA",
            "tipo_requisicao": "Renovação",
            "api_id": "API-001",
            "descricao_servico": "API de integração com CRM",
            "integracoes_disponiveis": ["REST", "WEBHOOK", "MENSAGERIA"],
            "fluxo_dados": "BIDIRECIONAL",
            "armazena_dados_bv": False
        }
    }

    print("\n📥 Request Payload:")
    print(format_json_payload(payload))
    print("\n" + "="*80)

    # Format query for agent
    query = f"""
Processar requisição de parecer de arquitetura:

{format_json_payload(payload)}
"""

    print("\n⚙️ Processing...\n")

    # Run agent with correct API
    runner = InMemoryRunner(agent=root_agent)

    # Create session
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="api_user_1"
    )

    # Prepare content
    content = UserContent(parts=[Part(text=query)])

    # Run async
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            print(event.content.parts[0].text)

    print("\n" + "="*80)
    print("✅ Example 1 completed successfully!")
    print("="*80)


async def example_2_nova_contratacao_com_ressalvas():
    """Example 2: New contract with observations - Parecer Favorável com Ressalvas."""

    print("\n" + "="*80)
    print("Example 2: Nova Contratação com Ressalvas (API Mode)")
    print("="*80)

    # Prepare payload in API format
    payload = {
        "solicitante": {
            "email": "gestor.cloud@bancobv.com.br",
            "diretoria": "Infraestrutura Cloud"
        },
        "request": {
            "cnpj": "98765432000101",
            "nome_fornecedor": "Cloud Data Services S.A.",
            "tipo_requisicao": "Nova Contratação",
            "api_id": "API-002",
            "descricao_servico": "Serviço de armazenamento em nuvem",
            "integracoes_disponiveis": ["REST", "FTP"],
            "fluxo_dados": "OUTBOUND",
            "armazena_dados_bv": True
        }
    }

    print("\n📥 Request Payload:")
    print(format_json_payload(payload))
    print("\n⚠️ Note: Stores BV data → Ressalva automática sobre LGPD")
    print("Expected: Parecer Favorável com Ressalvas")
    print("\n" + "="*80)

    # Format query for agent
    query = f"""
Processar requisição de parecer de arquitetura:

{format_json_payload(payload)}
"""

    print("\n⚙️ Processing...\n")

    # Run agent with correct API
    runner = InMemoryRunner(agent=root_agent)

    # Create session
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="api_user_2"
    )

    # Prepare content
    content = UserContent(parts=[Part(text=query)])

    # Run async
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            print(event.content.parts[0].text)

    print("\n" + "="*80)
    print("✅ Example 2 completed successfully!")
    print("="*80)


async def example_3_desinvestir_desfavoravel():
    """Example 3: Service marked for disinvestment - Parecer Desfavorável."""

    print("\n" + "="*80)
    print("Example 3: Serviço Marcado para Desinvestir - Parecer Desfavorável (API Mode)")
    print("="*80)

    # Prepare payload
    payload = {
        "solicitante": {
            "email": "analista.legacy@bancobv.com.br",
            "diretoria": "Arquitetura - Legacy Systems"
        },
        "request": {
            "cnpj": "55666777000188",
            "nome_fornecedor": "Legacy Systems Group",
            "tipo_requisicao": "Renovação",
            "api_id": "API-004",
            "descricao_servico": "Sistema legado em descontinuação",
            "integracoes_disponiveis": ["SOAP"],
            "fluxo_dados": "INBOUND",
            "armazena_dados_bv": False
        }
    }

    print("\n📥 Request Payload:")
    print(format_json_payload(payload))
    print("\n⚠️ Note: API-004 is marked as 'Desinvestir' in CMDB")
    print("Expected: Parecer Desfavorável or Favorável com Ressalvas")
    print("\n" + "="*80)

    # Format query for agent
    query = f"""
Processar requisição de parecer de arquitetura:

{format_json_payload(payload)}
"""

    print("\n⚙️ Processing...\n")

    # Run agent with correct API
    runner = InMemoryRunner(agent=root_agent)

    # Create session
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="api_user_3"
    )

    # Prepare content
    content = UserContent(parts=[Part(text=query)])

    # Run async
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            print(event.content.parts[0].text)

    print("\n" + "="*80)
    print("✅ Example 3 completed successfully!")
    print("="*80)


async def example_4_renovacao_com_vencimento_alerta():
    """Example 4: Renewal with expiration date alert (> 2 years)."""

    print("\n" + "="*80)
    print("Example 4: Renovação com Vencimento > 2 Anos - Alerta (API Mode)")
    print("="*80)

    # Prepare payload
    payload = {
        "solicitante": {
            "email": "gerente.contratos@bancobv.com.br",
            "diretoria": "Gestão de Contratos"
        },
        "request": {
            "cnpj": "11223344000155",
            "nome_fornecedor": "Cloud Provider Inc",
            "tipo_requisicao": "Renovação",
            "api_id": "API-005",
            "descricao_servico": "Infraestrutura cloud principal",
            "integracoes_disponiveis": ["REST", "WEBHOOK", "MENSAGERIA"],
            "fluxo_dados": "BIDIRECIONAL",
            "armazena_dados_bv": True
        }
    }

    print("\n📥 Request Payload:")
    print(format_json_payload(payload))
    print("\n⚠️ Note: Contract expires in > 2 years (900 days)")
    print("Expected: ALERTA but processing continues")
    print("\n" + "="*80)

    # Format query for agent
    query = f"""
Processar requisição de parecer de arquitetura:

{format_json_payload(payload)}
"""

    print("\n⚙️ Processing...\n")

    # Run agent with correct API
    runner = InMemoryRunner(agent=root_agent)

    # Create session
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="api_user_4"
    )

    # Prepare content
    content = UserContent(parts=[Part(text=query)])

    # Run async
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            print(event.content.parts[0].text)

    print("\n" + "="*80)
    print("✅ Example 4 completed successfully!")
    print("="*80)


async def example_5_vencimento_ausente_bloqueio():
    """Example 5: Missing expiration date - BLOQUEIO."""

    print("\n" + "="*80)
    print("Example 5: Vencimento Ausente - BLOQUEIO (API Mode)")
    print("="*80)

    # Prepare payload
    payload = {
        "solicitante": {
            "email": "analista.new@bancobv.com.br",
            "diretoria": "Novos Negócios"
        },
        "request": {
            "cnpj": "11222333000144",
            "nome_fornecedor": "Analytics Platform Inc",
            "tipo_requisicao": "Renovação",
            "api_id": "API-003",
            "descricao_servico": "Plataforma de analytics",
            "integracoes_disponiveis": ["REST", "WEBHOOK"],
            "fluxo_dados": "BIDIRECIONAL",
            "armazena_dados_bv": False
        }
    }

    print("\n📥 Request Payload:")
    print(format_json_payload(payload))
    print("\n⚠️ Note: This CNPJ has no expiration date in OneTrust")
    print("Expected: STATUS = BLOQUEIO, processing stops")
    print("\n" + "="*80)

    # Format query for agent
    query = f"""
Processar requisição de parecer de arquitetura:

{format_json_payload(payload)}
"""

    print("\n⚙️ Processing...\n")

    # Run agent with correct API
    runner = InMemoryRunner(agent=root_agent)

    # Create session
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="api_user_5"
    )

    # Prepare content
    content = UserContent(parts=[Part(text=query)])

    # Run async
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            print(event.content.parts[0].text)

    print("\n" + "="*80)
    print("✅ Example 5 completed successfully!")
    print("="*80)


async def main():
    """Run all examples."""

    print("\n" + "🚀"*40)
    print("Architecture Domain ANS Agent - API Mode Examples")
    print("🚀"*40 + "\n")

    try:
        # Initialize Vertex AI
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'gft-bu-gcp')
        location = os.getenv('GOOGLE_CLOUD_LOCATION', 'global')

        print(f"📍 Initializing Vertex AI...")
        print(f"   Project: {project_id}")
        print(f"   Location: {location}")
        vertexai.init(project=project_id, location=location)
        print("✅ Vertex AI initialized\n")

        # Run examples sequentially
        await example_1_renovacao_favoravel()
        await asyncio.sleep(2)  # Brief pause between examples

        await example_2_nova_contratacao_com_ressalvas()
        await asyncio.sleep(2)

        await example_3_desinvestir_desfavoravel()
        await asyncio.sleep(2)

        await example_4_renovacao_com_vencimento_alerta()
        await asyncio.sleep(2)

        await example_5_vencimento_ausente_bloqueio()

        print("\n" + "🎉"*40)
        print("All examples completed successfully!")
        print("🎉"*40 + "\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

