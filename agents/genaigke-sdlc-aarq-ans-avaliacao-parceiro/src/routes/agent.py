import os
import uuid
import logging
import time
from io import BytesIO
from pathlib import Path
from typing import List, Optional
from datetime import datetime

import pandas as pd
from fastapi import File, Form, UploadFile, HTTPException
from genai_framework.decorators import post_route
from google.adk.agents import LlmAgent
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .prompt import ANS_PROMPT
from ..utils.security import validate_file_security, validate_files_count
from ..utils.audit import log_request_audit, log_response_audit

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    # dotenv not installed, will use system environment variables
    pass

# Validate critical environment variables
def validate_environment_variables() -> None:
    """
    Validate that all critical environment variables are set.
    Raises ValueError if any required variable is missing.
    """
    required_vars = {
        "GOOGLE_CLOUD_PROJECT": "Google Cloud Project ID is required for Vertex AI",
        "GOOGLE_CLOUD_LOCATION": "Google Cloud Location is required for Vertex AI",
        "GOOGLE_GENAI_USE_VERTEXAI": "Vertex AI flag must be set"
    }

    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"{var}: {description}")

    if missing_vars:
        error_msg = "Missing required environment variables:\n" + "\n".join(f"  - {var}" for var in missing_vars)
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info("All required environment variables validated successfully")

# Setup Google Cloud environment variables (only if not already set)
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "True"))
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", os.getenv("GOOGLE_CLOUD_PROJECT", "gft-bu-gcp"))
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"))

# Validate environment variables before creating agent
try:
    validate_environment_variables()
except ValueError as e:
    logger.critical(f"Environment validation failed: {e}")
    # Re-raise to prevent agent creation with invalid config
    raise

# Create and expose the root agent for ADK Web Server
root_agent = LlmAgent(
    name=os.getenv("AGENT_NAME", "ans_expert_agent"),
    model=os.getenv("AGENT_MODEL", "gemini-2.5-pro"),
    description=os.getenv("AGENT_DESCRIPTION", "Business and Solutions Architecture Agent - Expert in ANS domain for Banco BV"),
    instruction=ANS_PROMPT
)



async def agent(text: str = None, files: List[UploadFile] = None):
    """
    Função principal do agente que processa texto e arquivos
    """
    # Generate request ID for audit trail
    request_id = str(uuid.uuid4())
    start_time = time.time()

    # Use the module-level root_agent instead of creating a new one
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
 
    APP_NAME = os.getenv("AGENT_NAME", "ans_expert_agent")
    SESSION_ID = str(uuid.uuid4())
    USER_ID = str(uuid.uuid4())

    # Validate number of files
    if files:
        validate_files_count(len(files))

    # Collect files info for audit
    files_info = []
    if files:
        for file in files:
            files_info.append({
                "filename": file.filename,
                "content_type": file.content_type,
                "size": file.size if hasattr(file, 'size') else None
            })

    # Log request audit
    log_request_audit(
        request_id=request_id,
        user_id=USER_ID,
        session_id=SESSION_ID,
        text_length=len(text) if text else 0,
        files_count=len(files) if files else 0,
        files_info=files_info
    )

    logger.info(f"Processing request {request_id} - Session: {SESSION_ID}, Files: {len(files) if files else 0}")

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service
    )
 
    await session_service.create_session(
        app_name=APP_NAME,
        session_id=SESSION_ID,
        user_id=USER_ID
    )
 
    # Preparar as partes do conteúdo
    content_parts = []
    # Adicionar texto se fornecido
    if text:
        content_parts.append(types.Part.from_text(text=text))
    # Processar arquivos se fornecidos
    if files:
        for file in files:
            # Ler o conteúdo completo UMA VEZ
            content = await file.read()

            # VALIDAÇÃO DE SEGURANÇA
            validate_file_security(file, content)

            filename = file.filename
            mime_type = file.content_type

            logger.info(f"Processing file: {filename} ({mime_type}, {len(content)} bytes)")

            # Determinar o tipo e enviar nativamente
            if mime_type and mime_type.startswith('image/'):
                # Imagens: PNG, JPEG, WEBP, GIF
                content_parts.append({"inline_data":{"mime_type": mime_type,
                                                     "data":content}})
            elif mime_type == 'application/pdf':
                # PDF nativo
                content_parts.append({"inline_data":{"mime_type": mime_type,
                                                     "data":content}})
            elif mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or (filename and filename.endswith('.xlsx')):
                # Excel - converter para texto
                try:
                    excel_file = BytesIO(content)
                    # Ler todas as abas
                    excel_data = pd.read_excel(excel_file, sheet_name=None)
                    text_content = f"Arquivo Excel: {filename}\n\n"
                    for sheet_name, df in excel_data.items():
                        text_content += f"=== Aba: {sheet_name} ===\n"
                        # Converter para string formatada (CSV-like ou tabela)
                        text_content += df.to_csv(index=False, sep='\t')
                        text_content += "\n\n"
                    content_parts.append({"text": text_content})
                except Exception as e:
                    # Se falhar, informar o erro
                    content_parts.append({"text": f"Erro ao processar Excel {filename}: {str(e)}"})
            elif mime_type == 'text/plain' or (filename and filename.endswith('.txt')):
                # TXT: Tentar decodificar como texto
                text_content = None
                encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
                for encoding in encodings:
                    try:
                        text_content = content.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                if text_content:
                    content_parts.append(types.Part.from_text(
                        text=f"Conteúdo do arquivo {filename}:\n\n{text_content}"
                    ))
                else:
                    raise ValueError(f"Não foi possível decodificar o arquivo de texto: {filename}")
            else:
                # Tipo não suportado
                raise ValueError(f"Tipo de arquivo não suportado: {mime_type or 'desconhecido'} ({filename})")
    # Verificar se há conteúdo para processar
    if not content_parts:
        logger.warning(f"Request {request_id}: No content provided")
        raise ValueError("Nenhum conteúdo fornecido (texto ou arquivos)")

    # Criar o objeto Content com todas as partes
    new = types.Content(
        role="user",
        parts=content_parts
    )
 
    try:
        # Executar o agente
        logger.info(f"Request {request_id}: Starting agent execution")
        response_text = None
        for event in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=new):
            if event.is_final_response():
                if event.content and event.content.parts:
                    response_text = event.content.parts[0].text

        # Calculate processing time
        processing_time = time.time() - start_time

        # Log successful response
        log_response_audit(
            request_id=request_id,
            session_id=SESSION_ID,
            response_length=len(response_text) if response_text else 0,
            processing_time=processing_time,
            success=True
        )

        logger.info(f"Request {request_id}: Completed successfully in {processing_time:.2f}s")
        return response_text

    except Exception as e:
        # Calculate processing time
        processing_time = time.time() - start_time

        # Log failed response
        log_response_audit(
            request_id=request_id,
            session_id=SESSION_ID,
            response_length=0,
            processing_time=processing_time,
            success=False,
            error=str(e)
        )

        logger.error(f"Request {request_id}: Failed after {processing_time:.2f}s - Error: {str(e)}")
        raise

@post_route('health')
async def health_check():
    """
    Health check endpoint para monitoramento.

    Returns:
        dict: Status do serviço
    """
    return {
        "status": "healthy",
        "service": "ans_expert_agent",
        "timestamp": datetime.utcnow().isoformat(),
        "version": os.getenv("APP_VERSION", "1.0.0")
    }


@post_route('ans_review')
async def ans_review(
    texto: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None)
):
    """
    Endpoint que recebe texto e/ou arquivos e retorna a resposta do agente
    """
    request_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        # Normaliza lista de arquivos: [] -> None
        file_list = files if files and len(files) > 0 else None

        # Nenhum conteúdo fornecido
        if (texto is None or texto.strip() == "") and not file_list:
            logger.warning(f"Request {request_id}: No content provided")
            return {"error": "Nenhum conteúdo fornecido (texto ou arquivos)"}, 400

        # Três caminhos: ambos, só arquivos, só texto
        if file_list and (texto is not None and texto.strip() != ""):
            # Texto + arquivos
            response = await agent(text=texto, files=file_list)
        elif file_list and (texto is None or texto.strip() == ""):
            # Somente arquivos
            response = await agent(text=None, files=file_list)
        else:
            # Somente texto (file_list é None)
            response = await agent(text=texto, files=None)

        processing_time = time.time() - start_time
        logger.info(f"Request {request_id}: API call completed in {processing_time:.2f}s")

        return {"response": response}

    except HTTPException as he:
        # HTTP exceptions já tem status code apropriado
        processing_time = time.time() - start_time
        logger.warning(f"Request {request_id}: HTTP error after {processing_time:.2f}s - {he.detail}")
        raise

    except ValueError as ve:
        processing_time = time.time() - start_time
        logger.error(f"Request {request_id}: Validation error after {processing_time:.2f}s - {str(ve)}")
        return {"error": str(ve)}, 400

    except FileNotFoundError as fe:
        processing_time = time.time() - start_time
        logger.error(f"Request {request_id}: File not found after {processing_time:.2f}s - {str(fe)}")
        return {"error": str(fe)}, 415

    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Request {request_id}: Unexpected error after {processing_time:.2f}s - {str(e)}", exc_info=True)
        return {"error": f"Erro interno do servidor: {str(e)}"}, 500
