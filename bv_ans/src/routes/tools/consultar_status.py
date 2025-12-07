"""
Rota para consultar status e informações do sistema de pareceres.
"""
 
import json
import os
from datetime import datetime
from genai_framework.decorators import get_route


@get_route('status')
def get_status():
    """
    Endpoint para verificar o status do sistema.
   
    Returns:
        JSON com informações do sistema
    """
    return json.dumps({
        'status': 'online',
        'service': 'Architecture Domain ANS - Parecerista',
        'version': '1.0.0',
        'project_id': os.getenv('GOOGLE_CLOUD_PROJECT', 'not-configured'),
        'location': os.getenv('GOOGLE_CLOUD_LOCATION', 'not-configured')
    })
 

@get_route('health')
def get_health():
    """
    Endpoint de health check.
   
    Returns:
        JSON com status de saúde do serviço
    """
    return json.dumps({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })
 