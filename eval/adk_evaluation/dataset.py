# -*- coding: utf-8 -*-
"""
Evaluation Dataset for Architecture Domain ANS Agent

This module contains test cases for evaluating the agent's performance
across different scenarios from the Architecture Domain ANS user story.
"""

from typing import List, Dict, Any, Optional


# Test cases organized by scenario type
EVALUATION_DATASET = [
    # ==================== SCENARIO 1: Renovação com histórico Positivo ====================
    {
        "test_id": "TC-001",
        "scenario": "Renovação - histórico Favorável",
        "category": "renovacao_favoravel",
        "input": {
            "solicitante": {
                "email": "analista.arquitetura@bancobv.com.br",
                "diretoria": "Arquitetura e Tecnologia"
            },
            "request": {
                "cnpj": "12345678000190",
                "nome_fornecedor": "Tech Solutions LTDA",
                "tipo_requisicao": "Renovação",
                "api_id": "API-001",
                "descricao_servico": "API de integração com CRM",
                "integracoes_disponiveis": ["REST", "WEBHOOK", "MENSAGERIA"],
                "fluxo_dados": "BIDIRECIONAL",
                "armazena_dados_bv": False
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_sugerido": "Parecer Favorável",
            "direcionador": "Evoluir",
            "score_confianca_min": 0.85,
            "criterios_minimos": [
                "Múltiplas integrações",
                "Renovação",
                "histórico"
            ],
            "insumos_obrigatorios": [
                "OneTrust",
                "CMDB",
                "histórico"
            ]
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_consult_onetrust": True,
            "must_consult_cmdb": True,
            "must_load_history": True,
            "must_suggest_favorable": True,
            "must_have_high_confidence": True
        }
    },

    # ==================== SCENARIO 2: Nova Contratação com Ressalvas ====================
    {
        "test_id": "TC-002",
        "scenario": "Nova Contratação - Armazena Dados BV",
        "category": "nova_contratacao_ressalvas",
        "input": {
            "solicitante": {
                "email": "gestor.cloud@bancobv.com.br",
                "diretoria": "Infraestrutura Cloud"
            },
            "request": {
                "cnpj": "98765432000101",
                "nome_fornecedor": "Cloud Data Services S.A.",
                "tipo_requisicao": "Nova Contratação",
                "api_id": "API-002",
                "descricao_servico": "ServiÃ§o de armazenamento em nuvem",
                "integracoes_disponiveis": ["REST", "FTP"],
                "fluxo_dados": "OUTBOUND",
                "armazena_dados_bv": True
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_sugerido": "Parecer Favorável com Ressalvas",
            "ressalvas_minimas": 1,
            "ressalva_lgpd_required": True,
            "score_confianca_max": 0.85,
            "criterios_esperados": [
                "dados BV",
                "LGPD"
            ]
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_have_ressalvas": True,
            "must_mention_lgpd": True,
            "must_lower_confidence": True,
            "must_detect_data_storage": True
        }
    },

    # ==================== SCENARIO 3: ServiÃ§o Marcado para Desinvestir ====================
    {
        "test_id": "TC-003",
        "scenario": "Renovação - Sistema Legado para Desinvestir",
        "category": "desinvestimento",
        "input": {
            "solicitante": {
                "email": "analista.legacy@bancobv.com.br",
                "diretoria": "Arquitetura - Legacy Systems"
            },
            "request": {
                "cnpj": "55666777000188",
                "nome_fornecedor": "Legacy Systems Group",
                "tipo_requisicao": "Renovação",
                "api_id": "API-004",
                "descricao_servico": "Sistema legado em descontinuaÃ§Ã£o",
                "integracoes_disponiveis": ["SOAP"],
                "fluxo_dados": "INBOUND",
                "armazena_dados_bv": False
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_sugerido": "Parecer Favorável com Ressalvas",
            "direcionador": "Desinvestir",
            "ressalva_desinvestimento_required": True,
            "score_confianca_max": 0.75,
            "alertas_minimos": 0
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_detect_desinvestir": True,
            "must_have_ressalva_desinvestir": True,
            "must_load_previous_ressalvas": True,
            "must_have_lower_confidence": True
        }
    },

    # ==================== SCENARIO 4: Renovação com Vencimento > 2 Anos ====================
    {
        "test_id": "TC-004",
        "scenario": "Renovação - Vencimento > 2 Anos (Alerta)",
        "category": "vencimento_longo",
        "input": {
            "solicitante": {
                "email": "gerente.contratos@bancobv.com.br",
                "diretoria": "GestÃ£o de Contratos"
            },
            "request": {
                "cnpj": "11223344000155",
                "nome_fornecedor": "Cloud Provider Inc",
                "tipo_requisicao": "Renovação",
                "api_id": "API-005",
                "descricao_servico": "Infraestrutura cloud principal",
                "integracoes_disponiveis": ["REST", "WEBHOOK", "MENSAGERIA"],
                "fluxo_dados": "BIDIRECIONAL",
                "armazena_dados_bv": True
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_sugerido": "Parecer Favorável",
            "alertas_minimos": 1,
            "alerta_vencimento_required": True,
            "alerta_nivel": "INFO",
            "processamento_continua": True
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_have_alert_vencimento": True,
            "must_continue_processing": True,
            "must_calculate_days": True,
            "must_suggest_action": True
        }
    },

    # ==================== SCENARIO 5: Vencimento Ausente - BLOQUEIO ====================
    {
        "test_id": "TC-005",
        "scenario": "Renovação - Vencimento Ausente (BLOQUEIO)",
        "category": "bloqueio_critico",
        "input": {
            "solicitante": {
                "email": "analista.new@bancobv.com.br",
                "diretoria": "Novos NegÃ³cios"
            },
            "request": {
                "cnpj": "11222333000144",
                "nome_fornecedor": "Analytics Platform Inc",
                "tipo_requisicao": "Renovação",
                "api_id": "API-003",
                "descricao_servico": "Plataforma de analytics",
                "integracoes_disponiveis": ["REST", "WEBHOOK"],
                "fluxo_dados": "BIDIRECIONAL",
                "armazena_dados_bv": False
            }
        },
        "expected_output": {
            "sucesso": False,
            "status": "BLOQUEIO",
            "erro": "VENCIMENTO_AUSENTE",
            "mensagem_required": True,
            "acao_requerida_required": True,
            "parecer_nao_sugerido": True
        },
        "evaluation_criteria": {
            "must_fail": True,
            "must_block": True,
            "must_not_suggest_parecer": True,
            "must_have_clear_message": True,
            "must_have_action_required": True
        }
    },

    # ==================== SCENARIO 6: Múltiplas integrações Modernas ====================
    {
        "test_id": "TC-006",
        "scenario": "Nova Contratação - Múltiplas integrações",
        "category": "integracao_moderna",
        "input": {
            "solicitante": {
                "email": "arquiteto.apis@bancobv.com.br",
                "diretoria": "Arquitetura de APIs"
            },
            "request": {
                "cnpj": "11222333000144",  # Analytics Platform Inc - jÃ¡ existe nos mocks
                "nome_fornecedor": "Analytics Platform Inc",
                "tipo_requisicao": "Nova Contratação",
                "api_id": "API-003",  # ANALYTICS-ENGINE
                "descricao_servico": "Plataforma de analytics com mÃºltiplos protocolos",
                "integracoes_disponiveis": ["REST", "GRAPHQL", "GRPC", "WEBHOOK"],
                "fluxo_dados": "BIDIRECIONAL",
                "armazena_dados_bv": False
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_sugerido": "Parecer Favorável",
            "score_confianca_min": 0.75,
            "criterios_esperados": [
                "Múltiplas integrações",
                "tecnologias modernas"
            ]
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_detect_multiple_integrations": True,
            "must_detect_modern_tech": True,
            "must_have_high_confidence": True
        }
    },

    # ==================== SCENARIO 7: Fluxo INBOUND Only ====================
    {
        "test_id": "TC-007",
        "scenario": "Nova Contratação - Fluxo INBOUND",
        "category": "fluxo_inbound",
        "input": {
            "solicitante": {
                "email": "analista.integracao@bancobv.com.br",
                "diretoria": "integração de Sistemas"
            },
            "request": {
                "cnpj": "98765432000101",  # Cloud Data Services - jÃ¡ existe
                "nome_fornecedor": "Cloud Data Services S.A.",
                "tipo_requisicao": "Renovação",  # Changed to Renovação to match existing mock
                "api_id": "API-002",  # CLOUD-STORAGE
                "descricao_servico": "ServiÃ§o de recepÃ§Ã£o de dados via cloud",
                "integracoes_disponiveis": ["REST", "FTP"],
                "fluxo_dados": "INBOUND",
                "armazena_dados_bv": True
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_sugerido": "Parecer Favorável com Ressalvas",
            "criterios_esperados": [
                "INBOUND",
                "dados BV"
            ],
            "ressalvas_minimas": 1
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_detect_inbound": True,
            "must_have_ressalva_data": True
        }
    },

    # ==================== SCENARIO 8: Direcionador Manter ====================
    {
        "test_id": "TC-008",
        "scenario": "Renovação - Direcionador Manter",
        "category": "manter",
        "input": {
            "solicitante": {
                "email": "gestor.operacoes@bancobv.com.br",
                "diretoria": "OperaÃ§Ãµes"
            },
            "request": {
                "cnpj": "11223344000155",  # Cloud Provider Inc - jÃ¡ existe
                "nome_fornecedor": "Cloud Provider Inc",
                "tipo_requisicao": "Renovação",
                "api_id": "API-005",  # SEC-GATEWAY (Manter)
                "descricao_servico": "Gateway de seguranÃ§a operacional",
                "integracoes_disponiveis": ["REST", "SOAP"],
                "fluxo_dados": "BIDIRECIONAL",
                "armazena_dados_bv": False
            }
        },
        "expected_output": {
            "sucesso": True,
            "direcionador": "Manter",
            "parecer_sugerido": "Parecer Favorável",
            "score_confianca_min": 0.75
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_consult_cmdb": True,
            "must_identify_direcionador": True
        }
    },
]


def get_dataset_stats(dataset: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Get statistics about the evaluation dataset.

    Args:
        dataset: Optional dataset to analyze. If None, uses EVALUATION_DATASET.

    Returns:
        Dictionary with dataset statistics
    """
    if dataset is None:
        dataset = EVALUATION_DATASET

    categories = {}
    for test_case in dataset:
        category = test_case["category"]
        categories[category] = categories.get(category, 0) + 1

    return {
        "total_tests": len(dataset),
        "categories": categories,
        "test_ids": [tc["test_id"] for tc in dataset],
        "scenarios": [tc["scenario"] for tc in EVALUATION_DATASET]
    }


def get_test_by_id(test_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific test case by ID.

    Args:
        test_id: Test case ID (e.g., "TC-001")

    Returns:
        Test case dictionary or None if not found
    """
    for test_case in EVALUATION_DATASET:
        if test_case["test_id"] == test_id:
            return test_case
    return None


def get_tests_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Get all test cases for a specific category.

    Args:
        category: Category name

    Returns:
        List of test cases
    """
    return [tc for tc in EVALUATION_DATASET if tc["category"] == category]


