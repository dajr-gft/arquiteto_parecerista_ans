"""
Tools module for ADK routes
Contains all tool functions and endpoints
"""

# Import all tools to make them available when the module is loaded
from .analisar_documento import analisar_documento_parecer
from .analisar_planilha import analisar_planilha_parecer
from .consultar_parecer_simples import sugerir_parecer_simples
from .consultar_status import get_status, get_health

__all__ = [
    'analisar_documento_parecer',
    'analisar_planilha_parecer',
    'sugerir_parecer_simples',
    'get_status',
    'get_health'
]

