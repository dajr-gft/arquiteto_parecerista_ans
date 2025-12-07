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

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"  
 
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'bv-sgen-19562344-poc')
LOCATION = 'global'
 
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID    
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION  

async def agent(text: str = None, files: List[UploadFile] = None):
    """
    Função principal do agente que processa texto e arquivos
    """
    root_agent = LlmAgent(
        name="ans_expert_agent",
        model="gemini-2.5-flash",
        description="Business and Solutions Architecture Agent",
        instruction=ANS_PROMPT
    )
 
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
                content_parts.append(types.Part.from_image(
                    image_data=base64_data,
                    mime_type=mime_type
                ))
            elif mime_type == 'application/pdf':
                # PDF nativo
                content_parts.append(types.Part.from_document(
                    document_data=base64_data,
                    mime_type='application/pdf'
                ))
            elif mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or \
                 (filename and filename.endswith('.xlsx')):
                # Excel nativo
                content_parts.append(types.Part.from_document(
                    document_data=base64_data,
                    mime_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                ))
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
        if files and len(files) > 0:
            try:
                response = await agent(text=texto, files=files)
            except Exception as e:
                return {"error": str(e)}, 500
        else:
            try:
                response = await agent(text=texto)
            except Exception as e:
                return {"error": str(e)}, 500
        return {'response': response}, 200
    except ValueError as ve:
        return {"error": str(ve)}, 400
    except FileNotFoundError as fe:
        return {"error": str(fe)}, 415
    except Exception as e:
        return {"error": f"erro genérico: {str(e)}"}, 500