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

"""Architecture Domain ANS Agent - Main agent definition."""

import logging
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from . import prompts
from .tools import (
    capturar_vencimento,
    carregar_insumos,
    carregar_ressalvas,
    consultar_cmdb,
    integrar_onetrust,
    registrar_parecer,
    sugerir_parecer,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

# Force Vertex AI usage
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# Get environment variables for logging
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'gft-bu-gcp')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION', 'global')

# Set Vertex AI configuration
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", PROJECT_ID)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", LOCATION)

root_agent = Agent(
    model='gemini-3-pro-preview',
    name='architecture_domain_ans',
    description=(
        'Assistente inteligente para análise e emissão de pareceres de arquitetura. '
        'Automatiza o processo de avaliação de fornecedores e serviços considerando '
        'integrações disponíveis, histórico de pareceres, direcionadores tecnológicos '
        'e conformidade com políticas do Banco BV. Sugere pareceres (Favorável, '
        'Favorável com Ressalvas, ou Desfavorável) com base em critérios objetivos.'
    ),
    instruction=prompts.SYSTEM_PROMPT,
    tools=[
        FunctionTool(integrar_onetrust),
        FunctionTool(consultar_cmdb),
        FunctionTool(carregar_insumos),
        FunctionTool(capturar_vencimento),
        FunctionTool(carregar_ressalvas),
        FunctionTool(sugerir_parecer),
        FunctionTool(registrar_parecer),
    ],
)

logger.info(f"Architecture Domain ANS Agent initialized (Project: {PROJECT_ID}, Location: {LOCATION})")
logger.info("Note: Agent will use gcloud auth credentials. Run 'gcloud auth application-default login' if needed.")

