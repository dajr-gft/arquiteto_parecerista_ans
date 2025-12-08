"""
Mock dos decoradores do genai_framework para desenvolvimento local.
Em produção no genaigke, os decoradores reais serão utilizados.
"""
 
import functools
import json
from typing import Callable, Any, Optional
 
def post_route(route_name: Optional[str] = None) -> Callable:
    """
    Mock do decorador @post_route.
    Em produção, transforma a função em endpoint POST.
   
    Args:
        route_name: Nome opcional da rota. Se não fornecido, usa o nome da função.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Em desenvolvimento local, apenas executa a função
            return func(*args, **kwargs)
       
        # Adiciona metadados para documentação
        wrapper._route_type = 'POST'
        wrapper._route_name = route_name or func.__name__
        return wrapper
   
    # Se chamado diretamente com função, decora imediatamente
    if callable(route_name):
        func = route_name
        route_name = None
        return decorator(func)
   
    # Se chamado com argumentos, retorna decorator
    return decorator
 
def get_route(route_name: Optional[str] = None) -> Callable:
    """
    Mock do decorador @get_route.
    Em produção, transforma a função em endpoint GET.
   
    Args:
        route_name: Nome opcional da rota. Se não fornecido, usa o nome da função.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Em desenvolvimento local, apenas executa a função
            return func(*args, **kwargs)
       
        # Adiciona metadados para documentação
        wrapper._route_type = 'GET'
        wrapper._route_name = route_name or func.__name__
        return wrapper
   
    # Se chamado diretamente com função, decora imediatamente
    if callable(route_name):
        func = route_name
        route_name = None
        return decorator(func)
   
    # Se chamado com argumentos, retorna decorator
    return decorator
 
def file_input_route(route_name: Optional[str] = None) -> Callable:
    """
    Mock do decorador @file_input_route.
    Em produção, transforma a função em endpoint que aceita upload de arquivos.
   
    Args:
        route_name: Nome opcional da rota. Se não fornecido, usa o nome da função.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Em desenvolvimento local, apenas executa a função
            # O primeiro argumento deve ser o conteúdo do arquivo (bytes)
            # O segundo argumento deve ser o nome do arquivo (string)
            return func(*args, **kwargs)
       
        # Adiciona metadados para documentação
        wrapper._route_type = 'POST'
        wrapper._route_name = route_name or func.__name__
        wrapper._accepts_file = True
        return wrapper
   
    # Se chamado diretamente com função, decora imediatamente
    if callable(route_name):
        func = route_name
        route_name = None
        return decorator(func)
   
    # Se chamado com argumentos, retorna decorator
    return decorator