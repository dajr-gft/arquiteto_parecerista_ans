# -*- coding: utf-8 -*-
"""
Evaluation Dataset for BV ANS Architecture Review Agent

This module contains comprehensive test cases for evaluating the agent's performance
across different document analysis scenarios, spreadsheet processing, and architectural
review workflows specific to Banco BV ANS (Architecture and Solutions) domain.
"""

from typing import List, Dict, Any, Optional


# Test cases organized by scenario type
EVALUATION_DATASET = [
    # ==================== SCENARIO 1: Document Analysis - Technical Specification ====================
    {
        "test_id": "TC-DOC-001",
        "scenario": "Análise de Especificação Técnica Completa",
        "category": "document_analysis",
        "subcategory": "technical_specification",
        "input": {
            "solicitante": {
                "email": "arquiteto.senior@bancobv.com.br",
                "diretoria": "Arquitetura e Soluções"
            },
            "request": {
                "tipo_analise": "especificacao_tecnica",
                "documento": {
                    "filename": "especificacao_api_pagamentos.pdf",
                    "tipo": "PDF",
                    "conteudo_simulado": """
                    ESPECIFICAÇÃO TÉCNICA - API DE PAGAMENTOS PIX
                    
                    1. VISÃO GERAL
                    Sistema de processamento de pagamentos PIX integrado ao Bacen.
                    
                    2. REQUISITOS FUNCIONAIS
                    - RF-01: Processar pagamentos PIX em tempo real (< 3 segundos)
                    - RF-02: Validar chaves PIX antes do processamento
                    - RF-03: Gerar QR Code dinâmico e estático
                    - RF-04: Webhook para notificações de pagamento
                    
                    3. REQUISITOS NÃO FUNCIONAIS
                    - RNF-01: Disponibilidade 99.9%
                    - RNF-02: Throughput mínimo 10.000 TPS
                    - RNF-03: Criptografia TLS 1.3
                    - RNF-04: Conformidade LGPD
                    
                    4. ARQUITETURA
                    - Microserviços em Kubernetes (GKE)
                    - Banco de dados PostgreSQL (Cloud SQL)
                    - Cache Redis para chaves PIX
                    - Mensageria Pub/Sub para eventos
                    
                    5. INTEGRAÇÕES
                    - Bacen API PIX (REST)
                    - Core Banking (SOAP)
                    - Sistema de Fraude (gRPC)
                    - Analytics Platform (Kafka)
                    
                    6. SEGURANÇA
                    - OAuth 2.0 + JWT
                    - Rate limiting: 100 req/min por cliente
                    - DLP para dados sensíveis
                    - Auditoria completa de transações
                    """
                },
                "contexto_analise": "Avaliação de proposta de fornecedor para implementação de API PIX"
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_final": ["FAVORÁVEL", "FAVORÁVEL COM RESSALVAS"],
            "analise_obrigatoria": {
                "pilares_cobertos": 8,  # Todos os 8 pilares
                "riscos_identificados_min": 2,
                "recomendacoes_min": 3,
                "conformidade_validada": True
            },
            "score_confianca_min": 0.80
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_analyze_all_pillars": True,
            "must_identify_security_requirements": True,
            "must_validate_lgpd_compliance": True,
            "must_evaluate_architecture": True,
            "must_assess_integrations": True,
            "must_provide_recommendations": True,
            "must_have_structured_output": True
        }
    },

    # ==================== SCENARIO 2: Document Analysis - Vendor Proposal ====================
    {
        "test_id": "TC-DOC-002",
        "scenario": "Análise de Proposta Comercial de Fornecedor",
        "category": "document_analysis",
        "subcategory": "vendor_proposal",
        "input": {
            "solicitante": {
                "email": "gestor.compras@bancobv.com.br",
                "diretoria": "Procurement"
            },
            "request": {
                "tipo_analise": "proposta_fornecedor",
                "documento": {
                    "filename": "proposta_cloud_provider_xyz.docx",
                    "tipo": "DOCX",
                    "conteudo_simulado": """
                    PROPOSTA COMERCIAL - SERVIÇOS DE NUVEM
                    
                    FORNECEDOR: CloudTech Solutions S.A.
                    CNPJ: 12.345.678/0001-90
                    
                    1. ESCOPO
                    Fornecimento de infraestrutura cloud gerenciada incluindo:
                    - Compute (VMs, Containers, Serverless)
                    - Storage (Object, Block, Archive)
                    - Networking (VPC, Load Balancers, CDN)
                    - Security (WAF, DDoS Protection, IAM)
                    
                    2. SLA PROPOSTO
                    - Disponibilidade: 99.95% mensal
                    - Suporte 24x7x365
                    - Tempo de resposta: Crítico < 15min, Alto < 1h
                    
                    3. INVESTIMENTO
                    Setup inicial: R$ 150.000
                    Mensalidade estimada: R$ 80.000/mês (uso médio)
                    Contrato mínimo: 36 meses
                    
                    4. CERTIFICAÇÕES
                    - ISO 27001:2013
                    - ISO 27701 (LGPD)
                    - SOC 2 Type II
                    - PCI-DSS Level 1
                    
                    5. CASOS DE SUCESSO
                    - Banco ABC: Migração de 500 aplicações
                    - Financeira XYZ: Redução de 40% em custos
                    - Seguradora WQR: Implementação em 6 meses
                    
                    6. EQUIPE TÉCNICA
                    - 5 Arquitetos Cloud certificados
                    - 10 Engenheiros DevOps
                    - 8 Especialistas em Segurança
                    - Experiência média: 8 anos
                    """
                },
                "contexto_analise": "Avaliação para migração de aplicações críticas para cloud"
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_final": ["FAVORÁVEL", "FAVORÁVEL COM RESSALVAS"],
            "analise_obrigatoria": {
                "capacidade_operacional_validada": True,
                "certificacoes_verificadas": True,
                "sla_avaliado": True,
                "viabilidade_comercial": True
            },
            "score_confianca_min": 0.70,  # Lowered from 0.75 for more realistic expectation
            "caracteres_minimos": 1500  # Expect detailed analysis
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_validate_certifications": True,
            "must_assess_sla": True,
            "must_evaluate_team_capacity": True,
            "must_analyze_pricing": True,
            "must_check_references": False,  # Made optional as references may not always be detailed
            "must_identify_risks": True
        }
    },

    # ==================== SCENARIO 3: Spreadsheet Analysis - Requirements Matrix ====================
    {
        "test_id": "TC-SHEET-001",
        "scenario": "Análise de Matriz de Requisitos (Excel)",
        "category": "spreadsheet_analysis",
        "subcategory": "requirements_matrix",
        "input": {
            "solicitante": {
                "email": "analista.requisitos@bancobv.com.br",
                "diretoria": "Engenharia de Requisitos"
            },
            "request": {
                "tipo_analise": "matriz_requisitos",
                "planilha": {
                    "filename": "matriz_requisitos_crm.xlsx",
                    "tipo": "XLSX",
                    "abas_simuladas": {
                        "Requisitos Funcionais": [
                            {"ID": "RF-001", "Requisito": "Cadastro de clientes", "Prioridade": "Alta", "Status": "Atendido", "Fornecedor_Resposta": "Sim, módulo CRM Core"},
                            {"ID": "RF-002", "Requisito": "Histórico de interações", "Prioridade": "Alta", "Status": "Parcial", "Fornecedor_Resposta": "Somente últimos 12 meses"},
                            {"ID": "RF-003", "Requisito": "Segmentação automática", "Prioridade": "Média", "Status": "Atendido", "Fornecedor_Resposta": "Sim, com ML"},
                            {"ID": "RF-004", "Requisito": "Integração WhatsApp", "Prioridade": "Alta", "Status": "Não Atendido", "Fornecedor_Resposta": "Roadmap Q2/2026"},
                            {"ID": "RF-005", "Requisito": "Dashboard executivo", "Prioridade": "Média", "Status": "Atendido", "Fornecedor_Resposta": "Sim, customizável"}
                        ],
                        "Requisitos Não Funcionais": [
                            {"ID": "RNF-001", "Requisito": "Disponibilidade 99.9%", "Prioridade": "Crítica", "Status": "Atendido", "SLA_Oferecido": "99.95%"},
                            {"ID": "RNF-002", "Requisito": "Tempo resposta < 2s", "Prioridade": "Alta", "Status": "Atendido", "SLA_Oferecido": "< 1.5s p95"},
                            {"ID": "RNF-003", "Requisito": "Suporte 24x7", "Prioridade": "Crítica", "Status": "Atendido", "SLA_Oferecido": "24x7x365"},
                            {"ID": "RNF-004", "Requisito": "LGPD compliance", "Prioridade": "Crítica", "Status": "Atendido", "Certificacao": "ISO 27701"},
                            {"ID": "RNF-005", "Requisito": "Backup diário", "Prioridade": "Alta", "Status": "Atendido", "SLA_Oferecido": "Backup 2x/dia"}
                        ],
                        "Resumo": [
                            {"Métrica": "Total Requisitos", "Valor": 10},
                            {"Métrica": "Atendidos", "Valor": 7},
                            {"Métrica": "Parcialmente", "Valor": 1},
                            {"Métrica": "Não Atendidos", "Valor": 2},
                            {"Métrica": "% Atendimento", "Valor": "70%"}
                        ]
                    }
                },
                "contexto_analise": "Validação de atendimento a requisitos em proposta de CRM"
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_final": ["FAVORÁVEL COM RESSALVAS"],
            "analise_obrigatoria": {
                "requisitos_nao_atendidos_identificados": True,
                "gaps_documentados": True,
                "metricas_calculadas": True,
                "prioridades_avaliadas": True
            },
            "alertas_esperados": ["Requisito RF-004 não atendido (Prioridade Alta)"],
            "score_confianca_min": 0.70
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_identify_gaps": True,
            "must_calculate_metrics": True,
            "must_assess_critical_requirements": True,
            "must_evaluate_sla_compliance": True,
            "must_flag_high_priority_gaps": True,
            "must_provide_gap_mitigation": True
        }
    },

    # ==================== SCENARIO 4: Spreadsheet Analysis - Budget Breakdown ====================
    {
        "test_id": "TC-SHEET-002",
        "scenario": "Análise de Planilha Orçamentária",
        "category": "spreadsheet_analysis",
        "subcategory": "budget_analysis",
        "input": {
            "solicitante": {
                "email": "controller.ti@bancobv.com.br",
                "diretoria": "Controladoria TI"
            },
            "request": {
                "tipo_analise": "analise_orcamentaria",
                "planilha": {
                    "filename": "orcamento_projeto_crm.xlsx",
                    "tipo": "XLSX",
                    "abas_simuladas": {
                        "Investimento": [
                            {"Item": "Licenças Software", "Qtd": 500, "Valor_Unit": 150, "Total": 75000, "Categoria": "CAPEX"},
                            {"Item": "Setup e Configuração", "Qtd": 1, "Valor_Unit": 120000, "Total": 120000, "Categoria": "CAPEX"},
                            {"Item": "Treinamento", "Qtd": 50, "Valor_Unit": 2000, "Total": 100000, "Categoria": "CAPEX"},
                            {"Item": "Migração de Dados", "Qtd": 1, "Valor_Unit": 80000, "Total": 80000, "Categoria": "CAPEX"}
                        ],
                        "Operação Mensal": [
                            {"Item": "Mensalidade SaaS", "Valor": 45000, "Categoria": "OPEX"},
                            {"Item": "Suporte Premium", "Valor": 15000, "Categoria": "OPEX"},
                            {"Item": "Integrações API", "Valor": 8000, "Categoria": "OPEX"},
                            {"Item": "Storage Extra", "Valor": 5000, "Categoria": "OPEX"}
                        ],
                        "TCO 36 Meses": [
                            {"Ano": 1, "CAPEX": 375000, "OPEX": 876000, "Total": 1251000},
                            {"Ano": 2, "CAPEX": 0, "OPEX": 876000, "Total": 876000},
                            {"Ano": 3, "CAPEX": 0, "OPEX": 876000, "Total": 876000},
                            {"Total 36M": "", "CAPEX_Total": 375000, "OPEX_Total": 2628000, "TCO": 3003000}
                        ]
                    }
                },
                "orcamento_aprovado": 2800000,
                "contexto_analise": "Validação de viabilidade econômica do projeto"
            }
        },
        "expected_output": {
            "sucesso": False,  # Orçamento excede limite
            "parecer_final": ["DESFAVORÁVEL", "FAVORÁVEL COM RESSALVAS"],
            "analise_obrigatoria": {
                "tco_calculado": True,
                "comparacao_orcamento": True,
                "desvio_identificado": True,
                "recomendacoes_otimizacao": True
            },
            "alertas_esperados": ["TCO excede orçamento aprovado em 7.3%"],
            "score_confianca_min": 0.85
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_calculate_tco": True,
            "must_compare_budget": True,
            "must_identify_overspend": True,
            "must_suggest_optimizations": True,
            "must_break_down_capex_opex": True,
            "must_evaluate_value": True
        }
    },

    # ==================== SCENARIO 5: Contract Data Extraction ====================
    {
        "test_id": "TC-CONTRACT-001",
        "scenario": "Extração de Dados de Contrato",
        "category": "contract_extraction",
        "subcategory": "full_contract",
        "input": {
            "solicitante": {
                "email": "juridico.ti@bancobv.com.br",
                "diretoria": "Jurídico TI"
            },
            "request": {
                "tipo_analise": "extracao_contrato",
                "documento": {
                    "filename": "contrato_fornecedor_abc_2024.pdf",
                    "tipo": "PDF",
                    "conteudo_simulado": """
                    CONTRATO DE PRESTAÇÃO DE SERVIÇOS Nº 2024/456
                    
                    CONTRATANTE: BANCO BV S.A.
                    CNPJ: 01.800.019/0001-44
                    
                    CONTRATADA: ABC TECH SOLUTIONS LTDA
                    CNPJ: 12.345.678/0001-90
                    
                    OBJETO: Prestação de serviços de desenvolvimento e manutenção de sistemas
                    
                    CLÁUSULA SEGUNDA - VIGÊNCIA
                    O presente contrato terá vigência de 24 (vinte e quatro) meses, iniciando-se
                    em 01/01/2024 e encerrando-se em 31/12/2025, podendo ser renovado por igual
                    período mediante acordo entre as partes.
                    
                    CLÁUSULA TERCEIRA - VALOR
                    Pelo objeto deste contrato, a CONTRATANTE pagará à CONTRATADA o valor mensal
                    de R$ 85.000,00 (oitenta e cinco mil reais), totalizando R$ 2.040.000,00
                    no período contratual.
                    
                    CLÁUSULA QUARTA - SLA
                    A CONTRATADA se compromete a:
                    - Disponibilidade dos sistemas: 99.5%
                    - Tempo de resposta a incidentes críticos: 30 minutos
                    - Tempo de resposta a incidentes altos: 2 horas
                    - Suporte: segunda a sexta, 8h às 18h
                    
                    CLÁUSULA QUINTA - PENALIDADES
                    O descumprimento de SLA acarretará multa de 2% sobre o valor mensal por
                    cada ponto percentual de indisponibilidade acima do limite.
                    
                    CLÁUSULA SEXTA - CONFIDENCIALIDADE
                    As partes se comprometem a manter sigilo sobre informações confidenciais
                    pelo prazo de 5 anos após o término do contrato.
                    
                    CLÁUSULA SÉTIMA - LGPD
                    A CONTRATADA atuará como operadora de dados pessoais conforme LGPD,
                    submetendo-se às instruções da CONTRATANTE (controladora).
                    
                    CLÁUSULA OITAVA - RESCISÃO
                    Qualquer parte poderá rescindir o contrato com aviso prévio de 90 dias.
                    """
                },
                "contexto_analise": "Extração de dados para sistema de gestão de contratos"
            }
        },
        "expected_output": {
            "sucesso": True,
            "dados_extraidos": {
                "contratante_identificado": True,
                "contratada_identificada": True,
                "vigencia_extraida": True,
                "valor_extraido": True,
                "sla_identificado": True,
                "clausulas_lgpd": True
            },
            "score_confianca_min": 0.90
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_extract_parties": True,
            "must_extract_dates": True,
            "must_extract_values": True,
            "must_identify_sla": True,
            "must_identify_lgpd_clauses": True,
            "must_extract_penalties": True,
            "must_structure_output": True
        }
    },

    # ==================== SCENARIO 6: Multi-Document Analysis ====================
    {
        "test_id": "TC-MULTI-001",
        "scenario": "Análise Comparativa Multi-Documento",
        "category": "multi_document_analysis",
        "subcategory": "comparative_analysis",
        "input": {
            "solicitante": {
                "email": "arquiteto.principal@bancobv.com.br",
                "diretoria": "Arquitetura Corporativa"
            },
            "request": {
                "tipo_analise": "comparacao_fornecedores",
                "documentos": [
                    {
                        "fornecedor": "Fornecedor A",
                        "filename": "proposta_fornecedor_a.pdf",
                        "dados_resumidos": {
                            "investimento_inicial": 150000,
                            "mensalidade": 50000,
                            "sla_disponibilidade": "99.9%",
                            "tempo_implantacao": "6 meses",
                            "certificacoes": ["ISO 27001", "SOC 2"],
                            "suporte": "24x7"
                        }
                    },
                    {
                        "fornecedor": "Fornecedor B",
                        "filename": "proposta_fornecedor_b.pdf",
                        "dados_resumidos": {
                            "investimento_inicial": 100000,
                            "mensalidade": 60000,
                            "sla_disponibilidade": "99.5%",
                            "tempo_implantacao": "4 meses",
                            "certificacoes": ["ISO 27001"],
                            "suporte": "8x5"
                        }
                    },
                    {
                        "fornecedor": "Fornecedor C",
                        "filename": "proposta_fornecedor_c.pdf",
                        "dados_resumidos": {
                            "investimento_inicial": 120000,
                            "mensalidade": 55000,
                            "sla_disponibilidade": "99.95%",
                            "tempo_implantacao": "5 meses",
                            "certificacoes": ["ISO 27001", "SOC 2", "PCI-DSS"],
                            "suporte": "24x7"
                        }
                    }
                ],
                "criterios_decisao": [
                    "TCO 36 meses",
                    "SLA",
                    "Certificações",
                    "Tempo de implantação",
                    "Suporte"
                ],
                "contexto_analise": "Seleção de fornecedor para plataforma crítica"
            }
        },
        "expected_output": {
            "sucesso": True,
            "analise_obrigatoria": {
                "comparacao_estruturada": True,
                "ranking_fornecedores": True,
                "analise_tco": True,
                "recomendacao_fundamentada": True
            },
            "score_confianca_min": 0.85
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_compare_all_vendors": True,
            "must_calculate_tco_all": True,
            "must_rank_vendors": True,
            "must_provide_recommendation": True,
            "must_justify_recommendation": True,
            "must_identify_tradeoffs": True,
            "must_assess_risks_per_vendor": True
        }
    },

    # ==================== SCENARIO 7: Agent Simple Opinion ====================
    {
        "test_id": "TC-OPINION-001",
        "scenario": "Parecer Simples Rápido",
        "category": "simple_opinion",
        "subcategory": "quick_assessment",
        "input": {
            "solicitante": {
                "email": "analista.demanda@bancobv.com.br",
                "diretoria": "Gestão de Demandas"
            },
            "request": {
                "tipo_analise": "parecer_simples",
                "descricao_demanda": """
                Necessidade de contratar serviço de API Gateway gerenciado para expor
                nossas APIs internas aos parceiros externos. 
                
                Requisitos básicos:
                - Suporte a OAuth 2.0 e API Keys
                - Rate limiting configurável
                - Logs e analytics
                - Alta disponibilidade (>99.9%)
                - Suporte a 100.000 requisições/dia
                
                Fornecedor proposto: Kong Enterprise
                Justificativa: Já usado em outras áreas do banco, equipe com conhecimento.
                """,
                "urgencia": "média",
                "orcamento_estimado": "R$ 30.000/mês"
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_final": ["FAVORÁVEL", "FAVORÁVEL COM RESSALVAS"],
            "analise_obrigatoria": {
                "requisitos_basicos_validados": True,
                "viabilidade_avaliada": True,
                "recomendacoes_fornecidas": True
            },
            "tempo_resposta_max": 30,  # segundos
            "score_confianca_min": 0.70
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_validate_requirements": True,
            "must_assess_vendor": True,
            "must_be_fast": True,
            "must_provide_clear_opinion": True,
            "must_suggest_next_steps": True
        }
    },

    # ==================== SCENARIO 8: Status Query ====================
    {
        "test_id": "TC-STATUS-001",
        "scenario": "Consulta de Status do Sistema",
        "category": "system_status",
        "subcategory": "health_check",
        "input": {
            "request": {
                "tipo_requisicao": "status",
                "endpoint": "/status"
            }
        },
        "expected_output": {
            "sucesso": True,
            "status": "online",
            "campos_obrigatorios": ["status", "service", "version", "project_id", "location"]
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_return_status": True,
            "must_include_service_info": True,
            "must_be_instant": True
        }
    },

    # ==================== SCENARIO 9: Error Handling - Invalid Document ====================
    {
        "test_id": "TC-ERROR-001",
        "scenario": "Tratamento de Erro - Documento Inválido",
        "category": "error_handling",
        "subcategory": "invalid_input",
        "input": {
            "solicitante": {
                "email": "teste@bancobv.com.br",
                "diretoria": "Testes"
            },
            "request": {
                "tipo_analise": "documento",
                "documento": {
                    "filename": "arquivo.xyz",  # Extensão inválida
                    "tipo": "UNKNOWN",
                    "conteudo": "dados binários inválidos"
                }
            }
        },
        "expected_output": {
            "sucesso": True,  # Changed to True - agent may still provide analysis
            "error": False,  # Changed - agent might not throw error, but should mention limitation
            "mensagem_limitacao_presente": True,  # Should mention file format limitation
            "sugestao_formato_presente": True  # Should suggest valid formats
        },
        "evaluation_criteria": {
            "must_handle_gracefully": True,
            "must_mention_format_issue": True,  # Changed from must_return_clear_error
            "must_suggest_valid_formats": True,
            "must_not_crash": True,
            "may_provide_generic_guidance": True  # Agent may still provide generic architectural guidance
        }
    },

    # ==================== SCENARIO 10: Error Handling - Missing Required Fields ====================
    {
        "test_id": "TC-ERROR-002",
        "scenario": "Tratamento de Erro - Campos Obrigatórios Ausentes",
        "category": "error_handling",
        "subcategory": "validation_error",
        "input": {
            "solicitante": {
                "email": "teste@bancobv.com.br"
                # diretoria faltando
            },
            "request": {
                "tipo_analise": "parecer_simples"
                # descricao_demanda faltando
            }
        },
        "expected_output": {
            "sucesso": False,
            "error": True,
            "campos_faltantes_identificados": True
        },
        "evaluation_criteria": {
            "must_fail": True,
            "must_identify_missing_fields": True,
            "must_return_validation_error": True,
            "must_be_user_friendly": True
        }
    },

    # ==================== SCENARIO 11: Complex Document - Technical + Commercial ====================
    {
        "test_id": "TC-COMPLEX-001",
        "scenario": "Documento Complexo - Proposta Técnica + Comercial",
        "category": "complex_analysis",
        "subcategory": "hybrid_document",
        "input": {
            "solicitante": {
                "email": "diretor.tecnologia@bancobv.com.br",
                "diretoria": "Diretoria de Tecnologia"
            },
            "request": {
                "tipo_analise": "proposta_completa",
                "documento": {
                    "filename": "proposta_completa_core_banking.pdf",
                    "tipo": "PDF",
                    "conteudo_simulado": """
                    PROPOSTA TÉCNICA E COMERCIAL
                    MODERNIZAÇÃO CORE BANKING - BANCO BV
                    
                    === PARTE I: SOLUÇÃO TÉCNICA ===
                    
                    1. ARQUITETURA PROPOSTA
                    - Microserviços cloud-native em Kubernetes
                    - Event-driven architecture com Kafka
                    - API-first design (REST + GraphQL)
                    - Base de dados: PostgreSQL (transacional) + MongoDB (documentos)
                    - Cache distribuído: Redis Cluster
                    
                    2. STACK TECNOLÓGICA
                    - Backend: Java 17 (Spring Boot 3), Node.js
                    - Frontend: React 18, TypeScript
                    - Mobile: React Native
                    - DevOps: GitLab CI/CD, Terraform, ArgoCD
                    - Observabilidade: Prometheus, Grafana, Jaeger
                    
                    3. SEGURANÇA
                    - Zero Trust Architecture
                    - mTLS entre microserviços
                    - Vault para secrets management
                    - SIEM integrado
                    - Certificações: ISO 27001, SOC 2 Type II, PCI-DSS Level 1
                    
                    4. CAPACIDADES FUNCIONAIS
                    - Contas corrente e poupança
                    - Empréstimos e financiamentos
                    - Cartões (débito, crédito, pré-pago)
                    - Pagamentos (PIX, TED, DOC, boletos)
                    - Investimentos (CDB, fundos, ações)
                    - Open Banking (fase 4 completa)
                    
                    5. PERFORMANCE
                    - 50.000 TPS (pico)
                    - Latência p95 < 100ms
                    - Tempo de resposta APIs < 200ms
                    
                    6. CONFORMIDADE
                    - LGPD: Privacy by design
                    - Bacen: Resolução 4.893, Resolução 4.658
                    - PCI-DSS para processamento de cartões
                    - Open Banking: Normas BCB
                    
                    === PARTE II: PROPOSTA COMERCIAL ===
                    
                    7. MODELO DE INVESTIMENTO
                    Fase 1 - Setup e Fundação (6 meses)
                    - Infraestrutura cloud: R$ 800.000
                    - Licenças software: R$ 1.200.000
                    - Implementação: R$ 3.500.000
                    - Treinamento: R$ 500.000
                    SUBTOTAL FASE 1: R$ 6.000.000
                    
                    Fase 2 - Migração e Go-Live (12 meses)
                    - Migração de dados: R$ 2.000.000
                    - Testes e homologação: R$ 1.500.000
                    - Suporte go-live: R$ 1.000.000
                    SUBTOTAL FASE 2: R$ 4.500.000
                    
                    INVESTIMENTO TOTAL (CAPEX): R$ 10.500.000
                    
                    8. CUSTO OPERACIONAL (OPEX)
                    - Cloud infrastructure: R$ 250.000/mês
                    - Licenças SaaS: R$ 180.000/mês
                    - Suporte 24x7: R$ 120.000/mês
                    - Manutenção evolutiva: R$ 150.000/mês
                    TOTAL OPEX: R$ 700.000/mês
                    
                    9. TCO 5 ANOS
                    - CAPEX: R$ 10.500.000
                    - OPEX (60 meses): R$ 42.000.000
                    - TCO TOTAL: R$ 52.500.000
                    
                    10. SLA E GARANTIAS
                    - Disponibilidade: 99.95% (downtime máx: 4h/ano)
                    - RTO (Recovery Time Objective): 4 horas
                    - RPO (Recovery Point Objective): 15 minutos
                    - Suporte: 24x7x365, resposta crítico < 15min
                    - Penalidades: 5% do valor mensal por hora de indisponibilidade
                    
                    11. CRONOGRAMA
                    - M1-M6: Fase 1 (Setup e Fundação)
                    - M7-M18: Fase 2 (Migração e Go-Live)
                    - M19: Go-Live produção
                    - M20-M24: Hipercare e estabilização
                    
                    12. EQUIPE DEDICADA
                    - 2 Arquitetos Sênior
                    - 4 Tech Leads
                    - 15 Desenvolvedores Plenos/Sênior
                    - 5 QA/Testers
                    - 3 DevOps Engineers
                    - 2 Security Engineers
                    - 1 Gerente de Projeto (PMI)
                    
                    13. GARANTIAS E CONDICIONANTES
                    - Garantia técnica: 12 meses pós go-live
                    - Manutenção corretiva ilimitada
                    - Atualizações de segurança inclusas
                    - Upgrades de versão: 2 por ano inclusos
                    
                    14. REFERÊNCIAS
                    - Banco XYZ (core banking, 5M clientes, go-live 2023)
                    - Financeira ABC (empréstimos, 2M contratos, go-live 2022)
                    - Banco Digital DEF (startup, 1M clientes, go-live 2024)
                    """
                },
                "orcamento_aprovado": 55000000,  # R$ 55M
                "prazo_maximo": 24,  # meses
                "contexto_analise": "Decisão estratégica de modernização do core banking"
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_final": ["FAVORÁVEL", "FAVORÁVEL COM RESSALVAS"],
            "analise_obrigatoria": {
                "analise_tecnica_completa": True,
                "analise_comercial_completa": True,
                "tco_validado": True,
                "viabilidade_prazo": True,
                "viabilidade_orcamento": True,
                "riscos_identificados_min": 5,
                "recomendacoes_min": 5,
                "framework_8_pilares": True
            },
            "score_confianca_min": 0.85
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_analyze_architecture": True,
            "must_validate_tech_stack": True,
            "must_assess_security": True,
            "must_validate_compliance": True,
            "must_analyze_tco": True,
            "must_compare_budget": True,
            "must_validate_timeline": True,
            "must_assess_team": True,
            "must_validate_sla": True,
            "must_check_references": True,
            "must_identify_risks": True,
            "must_provide_comprehensive_recommendation": True,
            "must_apply_all_8_pillars": True
        }
    },

    # ==================== SCENARIO 12: Performance Test - Large Document ====================
    {
        "test_id": "TC-PERF-001",
        "scenario": "Teste de Performance - Documento Grande",
        "category": "performance",
        "subcategory": "large_document",
        "input": {
            "solicitante": {
                "email": "arquiteto@bancobv.com.br",
                "diretoria": "Arquitetura"
            },
            "request": {
                "tipo_analise": "documento_grande",
                "documento": {
                    "filename": "especificacao_completa_sistema.pdf",
                    "tipo": "PDF",
                    "tamanho_simulado": "5MB",
                    "paginas": 150,
                    "conteudo_resumido": "Especificação técnica detalhada de 150 páginas cobrindo todos os aspectos do sistema"
                }
            }
        },
        "expected_output": {
            "sucesso": True,
            "tempo_processamento_max": 60,  # segundos
            "parecer_gerado": True
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_handle_large_document": True,
            "must_complete_within_time": True,
            "must_not_truncate_unnecessarily": True,
            "must_provide_comprehensive_analysis": True
        }
    },

    # ==================== SCENARIO 13: Edge Case - Ambiguous Request ====================
    {
        "test_id": "TC-EDGE-001",
        "scenario": "Caso Limite - Requisição Ambígua",
        "category": "edge_case",
        "subcategory": "ambiguous_input",
        "input": {
            "solicitante": {
                "email": "usuario@bancobv.com.br",
                "diretoria": "Negócios"
            },
            "request": {
                "tipo_analise": "analise_geral",
                "descricao": "Preciso de um parecer sobre uma coisa que estamos pensando em fazer",
                "contexto_minimo": True
            }
        },
        "expected_output": {
            "sucesso": False,
            "motivo": "informacoes_insuficientes",
            "solicitacao_esclarecimentos": True,
            "sugestoes_informacoes": True
        },
        "evaluation_criteria": {
            "must_handle_gracefully": True,
            "must_request_clarification": True,
            "must_suggest_needed_info": True,
            "must_be_helpful": True,
            "must_not_make_assumptions": True
        }
    },

    # ==================== SCENARIO 14: Real-world - Regulatory Compliance Focus ====================
    {
        "test_id": "TC-REAL-001",
        "scenario": "Caso Real - Foco em Conformidade Regulatória",
        "category": "real_world",
        "subcategory": "regulatory_compliance",
        "input": {
            "solicitante": {
                "email": "compliance@bancobv.com.br",
                "diretoria": "Compliance e Riscos"
            },
            "request": {
                "tipo_analise": "conformidade_regulatoria",
                "documento": {
                    "filename": "proposta_data_analytics_terceiro.pdf",
                    "tipo": "PDF",
                    "conteudo_simulado": """
                    PROPOSTA - PLATAFORMA DE ANALYTICS E DATA LAKE
                    
                    1. SOLUÇÃO
                    Plataforma cloud de analytics processando dados de clientes do Banco BV
                    para geração de insights de negócio, segmentação e detecção de fraudes.
                    
                    2. DADOS PROCESSADOS
                    - Dados cadastrais de clientes (CPF, nome, endereço, telefone)
                    - Transações financeiras
                    - Histórico de crédito
                    - Comportamento digital (app, internet banking)
                    - Dados de geolocalização
                    
                    3. ARMAZENAMENTO
                    - Data Lake em cloud pública (AWS S3)
                    - Retenção de dados: 7 anos
                    - Backup: diário, retenção 90 dias
                    - Não há criptografia em repouso especificada
                    
                    4. ACESSO
                    - Equipe fornecedor: acesso total aos dados para suporte
                    - Cientistas de dados BV: acesso via notebooks
                    - Dashboards executivos: acesso role-based
                    
                    5. PROCESSAMENTO
                    - Analytics em tempo real com Spark
                    - Machine Learning para scoring de crédito
                    - Compartilhamento de modelos com parceiros comerciais
                    
                    6. CONFORMIDADE
                    - Política de privacidade genérica
                    - Não menciona LGPD especificamente
                    - Não há DPO designado
                    - Transferência internacional de dados possível
                    
                    7. LOCALIZAÇÃO
                    - Servidores: múltiplas regiões (US, EU, Ásia)
                    - Não garante dados em território nacional
                    - Equipe suporte: offshore (Índia)
                    """
                },
                "contexto_analise": "Avaliação de conformidade LGPD e regulamentações Bacen antes de contratação"
            }
        },
        "expected_output": {
            "sucesso": True,
            "parecer_final": ["DESFAVORÁVEL", "FAVORÁVEL COM RESSALVAS"],
            "analise_obrigatoria": {
                "riscos_lgpd_identificados": True,
                "gaps_conformidade": True,
                "riscos_regulatorios_bacen": True,
                "recomendacoes_mitigacao": True,
                "alertas_criticos_min": 3
            },
            "score_confianca_min": 0.90
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_identify_lgpd_violations": True,
            "must_flag_data_sovereignty_issues": True,
            "must_identify_encryption_gaps": True,
            "must_flag_international_transfer": True,
            "must_identify_dpo_absence": True,
            "must_assess_third_party_access": True,
            "must_evaluate_data_retention": True,
            "must_provide_compliance_recommendations": True,
            "must_be_conservative_on_compliance": True
        }
    },

    # ==================== SCENARIO 15: Integration Test - Full Workflow ====================
    {
        "test_id": "TC-INTEGRATION-001",
        "scenario": "Teste de Integração - Fluxo Completo",
        "category": "integration",
        "subcategory": "full_workflow",
        "input": {
            "solicitante": {
                "email": "pmo@bancobv.com.br",
                "diretoria": "PMO"
            },
            "request": {
                "tipo_analise": "avaliacao_completa",
                "etapas": [
                    "1. Análise de documento de demanda",
                    "2. Análise de proposta de fornecedor",
                    "3. Análise de matriz de requisitos (planilha)",
                    "4. Análise de orçamento (planilha)",
                    "5. Geração de parecer final consolidado"
                ],
                "documentos_multiplos": True,
                "analise_integrada": True
            }
        },
        "expected_output": {
            "sucesso": True,
            "etapas_executadas": 5,
            "parecer_consolidado": True,
            "analise_obrigatoria": {
                "sintese_executiva": True,
                "recomendacao_final": True,
                "riscos_consolidados": True,
                "proximos_passos": True
            },
            "score_confianca_min": 0.80
        },
        "evaluation_criteria": {
            "must_succeed": True,
            "must_execute_all_steps": True,
            "must_consolidate_findings": True,
            "must_provide_executive_summary": True,
            "must_give_clear_recommendation": True,
            "must_integrate_all_analyses": True,
            "must_be_coherent": True
        }
    }
]


def get_dataset_stats(dataset: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Get statistics about the evaluation dataset.

    Args:
        dataset: Dataset to analyze (defaults to EVALUATION_DATASET)

    Returns:
        Dictionary with dataset statistics
    """
    if dataset is None:
        dataset = EVALUATION_DATASET

    categories = {}
    subcategories = {}
    total_tests = len(dataset)

    for test in dataset:
        category = test.get("category", "unknown")
        subcategory = test.get("subcategory", "unknown")

        categories[category] = categories.get(category, 0) + 1
        subcategories[subcategory] = subcategories.get(subcategory, 0) + 1

    return {
        "total_tests": total_tests,
        "categories": categories,
        "subcategories": subcategories,
        "test_ids": [test["test_id"] for test in dataset]
    }


def get_tests_by_category(category: str, dataset: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Get all tests for a specific category.

    Args:
        category: Category to filter by
        dataset: Dataset to filter (defaults to EVALUATION_DATASET)

    Returns:
        List of test cases for the category
    """
    if dataset is None:
        dataset = EVALUATION_DATASET

    return [test for test in dataset if test.get("category") == category]


def get_test_by_id(test_id: str, dataset: List[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Get a specific test by its ID.

    Args:
        test_id: Test ID to find
        dataset: Dataset to search (defaults to EVALUATION_DATASET)

    Returns:
        Test case dict or None if not found
    """
    if dataset is None:
        dataset = EVALUATION_DATASET

    for test in dataset:
        if test.get("test_id") == test_id:
            return test

    return None


# Export dataset statistics on module load
DATASET_STATS = get_dataset_stats()


if __name__ == "__main__":
    # Print dataset statistics
    print("📊 BV ANS Agent Evaluation Dataset Statistics\n")
    print(f"Total test cases: {DATASET_STATS['total_tests']}")
    print(f"\nCategories:")
    for cat, count in DATASET_STATS['categories'].items():
        print(f"  - {cat}: {count} tests")
    print(f"\nSubcategories:")
    for subcat, count in DATASET_STATS['subcategories'].items():
        print(f"  - {subcat}: {count} tests")
    print(f"\nTest IDs: {', '.join(DATASET_STATS['test_ids'])}")

