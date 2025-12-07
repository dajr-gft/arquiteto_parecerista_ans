"""
Rota simplificada para sugestão rápida de parecer sem usar o agente completo.
"""
 
import json
import logging
from genai_framework.decorators import post_route
 
from architecture_domain_ans.tools import sugerir_parecer
 
logger = logging.getLogger(__name__)
 
 
@post_route('sugerir_parecer_simples')
def sugerir_parecer_simples(
    cnpj: str,
    nome_fornecedor: str,
    tipo_requisicao: str,
    nome_servico: str,
    descricao_servico: str,
    api_id: str = None,
    direcionador: str = None
):
    """
    Endpoint simplificado para sugestão rápida de parecer.
   
    Não utiliza o agente completo, apenas a ferramenta de sugestão direta.
    Útil para análises rápidas ou validações preliminares.
   
    Args:
        cnpj: CNPJ do fornecedor
        nome_fornecedor: Nome do fornecedor
        tipo_requisicao: Tipo da requisição
        nome_servico: Nome do serviço
        descricao_servico: Descrição do serviço
        api_id: ID da API (opcional)
        direcionador: Direcionador tecnológico (opcional)
       
    Returns:
        JSON com sugestão de parecer
    """
    try:
        logger.info(f"Sugestão simples de parecer para: {nome_fornecedor}")
       
        # Montar dados da requisição
        dados_requisicao = {
            "cnpj": cnpj,
            "nome_fornecedor": nome_fornecedor,
            "tipo_requisicao": tipo_requisicao,
            "nome_servico": nome_servico,
            "descricao_servico": descricao_servico,
        }
       
        if api_id:
            dados_requisicao["api_id"] = api_id
        if direcionador:
            dados_requisicao["direcionador"] = direcionador
       
        # Chamar ferramenta de sugestão diretamente
        resultado = sugerir_parecer(dados_requisicao)
       
        logger.info("Sugestão de parecer concluída")
       
        return {
            'success': True,
            'parecer': resultado
        }, 200
 
    except ValueError as ve:
        logger.error(f"Erro de validação: {str(ve)}")
        return {"error": f"Erro de validação: {str(ve)}"}, 400
 
    except Exception as e:
        logger.error(f"Erro ao sugerir parecer: {str(e)}")
        return {"error": "Erro interno ao processar a sugestão"}, 500
 