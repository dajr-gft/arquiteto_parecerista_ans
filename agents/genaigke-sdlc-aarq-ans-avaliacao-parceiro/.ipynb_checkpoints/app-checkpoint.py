from fastapi import FastAPI, File, UploadFile, Form
from typing import List, Optional
import uvicorn
import os
from src.routes.ans_agent import agent  # ajuste o caminho

#uvicorn app:app --reload --host 0.0.0.0 --port 8080

app = FastAPI(title="ANS Agent API - Test",version="1.0.0")

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"  
 
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'bv-sgen-19562344-poc')
LOCATION = 'global'
 
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID    
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION  

 
@app.post("/ans_review")
async def ans_review(texto: Optional[str] = Form(None),
                     files: Optional[List[UploadFile]] = File(None)
                    ):
    """
    Endpoint para análise de documentos com agente ANS
    """
    try:
        if files and len(files) > 0:
            try:
                response = await agent(text=texto, files=files)
            except Exception as e:
                return {"Com arquivos": str(e)}, 500
        else:
            try:
                response = await agent(text=texto)
            except Exception as e:
                return {"Sem arquivos": str(e)}, 500
        return {'response': response}

    except Exception as e:
        return {"error": str(e)}, 500
 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True)
