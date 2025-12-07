import base64
from typing import List, Optional
from fastapi import File, UploadFile, Form
import uuid
from genai_framework.decorators import post_route
from google.adk.agents import LlmAgent
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from .prompt import ANS_PROMPT
from google.genai import types
import os
import pandas as pd
from io import BytesIO

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"  
 
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'gft-bu-gcp')
LOCATION = 'us-central1'
 
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID    
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION  

# Create and expose the root agent for ADK Web Server
root_agent = LlmAgent(
    name="ans_expert_agent",
    model="gemini-2.5-pro",
    description="Business and Solutions Architecture Agent - Expert in ANS domain for Banco BV",
    instruction=ANS_PROMPT
)

async def agent(text: str = None, files: List[UploadFile] = None):
    """
    Funo principal do agente que processa texto e arquivos
    """
    # Use the module-level root_agent instead of creating a new one
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
 
    APP_NAME = "ans_expert_agent"
    SESSION_ID = str(uuid.uuid4())
    USER_ID = str(uuid.uuid4())
 
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
            filename = file.filename
            mime_type = file.content_type
            # Converter para base64
            base64_data = base64.b64encode(content).decode('utf-8')
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
        raise ValueError("Nenhum conteúdo fornecido (texto ou arquivos)")
    # Criar o objeto Content com todas as partes
    new = types.Content(
        role="user",
        parts=content_parts
    )
 
    # Executar o agente
    for event in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=new):
        if event.is_final_response():
            if event.content and event.content.parts:
                return event.content.parts[0].text
 
@post_route('ans_review')
async def ans_review(
    texto: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None)
):
    """
    Endpoint que recebe texto e/ou arquivos e retorna a resposta do agente
    """

    try:
        # Normaliza lista de arquivos: [] -> None
        file_list = files if files and len(files) > 0 else None

        # Nenhum conteúdo fornecido
        if (texto is None or texto.strip() == "") and not file_list:
            return {"error": str(e)}

        # Três caminhos: ambos, só arquivos, só texto
        if file_list and (texto is not None and texto.strip() != ""):
            # Texto + arquivos
            try:
                response = await agent(text=texto, files=file_list)
            except Exception as e:
                return {"error": str(e)}

        elif file_list and (texto is None or texto.strip() == ""):
            # Somente arquivos
            try:
                response = await agent(text=None, files=file_list)
            except Exception as e:
                return {"error": str(e)}

        else:
            # Somente texto (file_list é None)
            try:
                response = await agent(text=texto, files=None)
            except Exception as e:
                return {"error": str(e)}

        return {"response": response}
    except ValueError as ve:
        return {"error": str(ve)}, 400
    except FileNotFoundError as fe:
        return {"error": str(fe)}, 415
    except Exception as e:
        return {"error": f"erro genérico: {str(e)}"}, 500