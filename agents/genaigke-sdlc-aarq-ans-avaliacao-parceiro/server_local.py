"""
Servidor local FastAPI para simular o comportamento do genaigke.
Este servidor expõe as rotas definidas com os decorators do genai_framework.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from typing import List, Optional
 
from fastapi.responses import JSONResponse
import sys
import os
import importlib
import uvicorn

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Adicionar src ao path
sys.path.insert(0, 'src')
sys.path.insert(0, 'genai_frameork')

from src.routes.agent import agent

def import_fresh(module_path):
    """Importa um módulo forçando o reload"""
    if module_path in sys.modules:
        del sys.modules[module_path]
    return importlib.import_module(module_path)
 
app = FastAPI(
    title="Agente Parecerista ANS",
    description="API do Agente Parecerista para análise arquitetural de soluções ANS",
    version="1.0.0"
)
 
# Rotas GET
@app.get("/status")
async def route_status():
    """Health check da aplicação"""
    try:
        consultar_status = import_fresh('routes.tools.consultar_status')
        result, code = consultar_status.status()
        return JSONResponse(
            content=result if isinstance(result, dict) else eval(result),
            status_code=code
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e), "details": "Erro ao executar status"})
 
@app.get("/health")
async def route_health():
    """Health check detalhado"""
    try:
        consultar_status = import_fresh('routes.tools.consultar_status')
        result, code = consultar_status.health()
        return JSONResponse(
            content=result if isinstance(result, dict) else eval(result),
            status_code=code
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e), "details": "Erro ao executar health"})
 
# Rotas POST
@app.post("/consultar_parecer_simples")
async def route_parecer_simples(request: Request):
    """Análise simplificada sem agente ADK"""
    try:
        data = await request.json()
        if not data:
            raise HTTPException(status_code=400, detail={"error": "JSON body required"})
       
        consultar_parecer_simples_module = import_fresh('routes.tools.consultar_parecer_simples')
        result, code = consultar_parecer_simples_module.consultar_parecer_simples(data)
        return JSONResponse(
            content=result if isinstance(result, dict) else eval(result),
            status_code=code
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})
 
@app.post("/analisar_parecer")
async def route_analisar_parecer(request: Request):
    """Análise completa com agente ADK e ferramentas"""
    try:
        data = await request.json()
        if not data:
            raise HTTPException(status_code=400, detail={"error": "JSON body required"})
       
        analisar_parecer_module = import_fresh('routes.tools.analisar_parecer')
        result, code = analisar_parecer_module.analisar_parecer(data)
        return JSONResponse(
            content=result if isinstance(result, dict) else eval(result),
            status_code=code
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})
 
# Rotas de upload de arquivos
@app.post("/analisar_documento_parecer")
async def route_analisar_documento(file: UploadFile = File(...)):
    """Upload e análise de documentos técnicos"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail={"error": "Empty filename"})
       
        analisar_documento_module = import_fresh('routes.tools.analisar_documento')
        file_content = await file.read()
        result, code = analisar_documento_module.analisar_documento_parecer(file_content, file.filename)
        return JSONResponse(
            content=result if isinstance(result, dict) else eval(result),
            status_code=code
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})
 
@app.post("/extrair_dados_contrato")
async def route_extrair_contrato(file: UploadFile = File(...)):
    """Extração de dados de contratos"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail={"error": "Empty filename"})
       
        extrair_dados_module = import_fresh('routes.tools.extrair_dados_contrato')
        file_content = await file.read()
        result, code = extrair_dados_module.extrair_dados_contrato(file_content, file.filename)
        return JSONResponse(
            content=result if isinstance(result, dict) else eval(result),
            status_code=code
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})
 
@app.post("/analisar_planilha_parecer")
async def route_analisar_planilha(file: UploadFile = File(...)):
    """Upload e análise de planilhas Excel (.xlsx, .xls) ou CSV"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail={"error": "Empty filename"})
       
        # Criar objeto FileInput mock
        from types import SimpleNamespace
        file_content = await file.read()
        file_input = SimpleNamespace(content=file_content, filename=file.filename)
       
        analisar_planilha_module = import_fresh('routes.tools.analisar_planilha')
        result = analisar_planilha_module.analisar_planilha_parecer(file_input)
       
        # Se retornou tupla (result, code)
        if isinstance(result, tuple):
            return JSONResponse(
                content=result[0] if isinstance(result[0], dict) else eval(result[0]),
                status_code=result[1]
            )
        # Se retornou apenas o resultado
        return JSONResponse(content=result if isinstance(result, dict) else eval(result))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e), "details": "Erro ao processar planilha"})
 
 
@app.post("/ans_review")
async def ans_review(texto: Optional[str] = Form(None),
                     files: List[UploadFile] = File(None)):
    """
    Endpoint para análise de documentos com agente ANS
    """
    try:
        response = await agent(text=texto, files=files)
        return {'response': response}
 
    except Exception as e:
        return {"error": str(e)}, 500
 
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Servidor Local do Agente Parecerista ANS (FastAPI)")
    print("="*60)
    print("\n📍 Endpoints disponíveis:")
    print("   GET  http://localhost:8080/status")
    print("   GET  http://localhost:8080/health")
    print("   GET http://localhost:8080/ans_review")
    print("   POST http://localhost:8080/consultar_parecer_simples")
    print("   POST http://localhost:8080/analisar_parecer")
    print("   POST http://localhost:8080/analisar_documento_parecer")
    print("   POST http://localhost:8080/extrair_dados_contrato")
    print("   POST http://localhost:8080/analisar_planilha_parecer ")
    print("\n📚 Documentação interativa:")
    print("   http://localhost:8080/docs (Swagger UI)")
    print("   http://localhost:8080/redoc (ReDoc)")
    print("\n⚠️  Configuração:")
    print("   Configure as variáveis no arquivo .env (copie de .env.example)")
    print("\n" + "="*60 + "\n")
   
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")