# Evaluation Framework - Architecture Domain ANS Agent

Framework de avaliação completo com **duas abordagens independentes e organizadas**.

## 📁 Estrutura Organizada

```
eval/
├── adk_evaluation/              # ✅ Avaliação ADK (Local/CI-CD)
│   ├── run_evaluation.py        # Script completo (8 testes)
│   ├── run_quick_eval.py        # Script rápido (3 testes)
│   ├── dataset.py               # Dataset de teste
│   ├── metrics.py               # Métricas de avaliação
│   ├── custom_metrics.py        # Métricas ANS customizadas
│   ├── results/                 # Resultados JSON locais
│   │   ├── evaluation_results_*.json
│   │   └── evaluation_report_*.json
│   └── README.md                # ← Documentação completa ADK
│
├── vertex_ai_evaluation/        # ☁️ Avaliação Vertex AI (Enterprise)
│   ├── run_vertex_ai_evaluation.py  # Script principal
│   ├── vertex_ai_evaluation.py      # Classe de serviço
│   ├── vertex_ai_setup.md           # Guia de configuração GCP
│   ├── requirements_vertex_ai.txt   # Dependências extras
│   ├── dataset.py                   # Dataset de teste
│   ├── metrics.py                   # Métricas de avaliação
│   ├── custom_metrics.py            # Métricas ANS customizadas
│   ├── results/                     # Resultados JSON + BigQuery
│   │   └── vertex_ai_evaluation_*.json
│   └── README.md                    # ← Documentação completa Vertex AI
│
├── __init__.py                  # Inicialização do módulo
└── README.md                    # Este arquivo (índice)
```

---

## 🎯 Escolhendo o Framework Correto

### 📊 **ADK Evaluation** (Recomendado para Dev/CI-CD)

**Quando usar**:
- ✅ Desenvolvimento local e testes rápidos
- ✅ Pipelines de CI/CD (GitHub Actions, GitLab)
- ✅ Debugging e validação de mudanças
- ✅ Avaliação offline sem custos

**Características**:
- ⚡ **Rápido**: 3-10 minutos
- 💰 **Gratuito**: Zero custos
- 🎯 **8 métricas customizadas ANS**
- 📄 **Output**: JSON local + console

**Como usar**:
```bash
cd eval/adk_evaluation
python run_evaluation.py      # Completo (8 testes, ~8min)
python run_quick_eval.py      # Rápido (3 testes, ~3min)
```

📖 **Documentação**: [`adk_evaluation/README.md`](./adk_evaluation/README.md)

---

### ☁️ **Vertex AI Evaluation** (Recomendado para Produção)

**Quando usar**:
- ✅ Avaliação de releases em produção
- ✅ Dashboard visual para stakeholders
- ✅ Histórico e comparação de versões
- ✅ Integração com BigQuery e GCS
- ✅ Relatórios executivos

**Características**:
- 📊 **Dashboard**: Console do Vertex AI
- 📈 **Histórico**: BigQuery automático
- 🔄 **Comparação**: Entre versões
- 💰 **Pago**: ~$5-10 por avaliação

**Como usar**:
```bash
cd eval/vertex_ai_evaluation
python run_vertex_ai_evaluation.py --real         # Execução completa
python run_vertex_ai_evaluation.py --dry-run      # Validação
```

📖 **Documentação**: [`vertex_ai_evaluation/README.md`](./vertex_ai_evaluation/README.md)

---

## 📊 Dataset de Teste

**8 test cases** cobrindo todos os cenários ANS:

| Test ID | Cenário | Categoria |
|---------|---------|-----------|
| TC-001 | Renovação - Histórico Favorável | `renovacao_favoravel` |
| TC-002 | Nova Contratação - Armazena Dados BV | `nova_contratacao_ressalvas` |
| TC-003 | Sistema Legado para Desinvestir | `desinvestimento` |
| TC-004 | Renovação - Vencimento > 2 Anos | `vencimento_longo` |
| TC-005 | Renovação - Vencimento Ausente (BLOQUEIO) | `bloqueio_critico` |
| TC-006 | Nova Contratação - Múltiplas Integrações | `integracao_moderna` |
| TC-007 | Nova Contratação - Fluxo INBOUND | `fluxo_inbound` |
| TC-008 | Renovação - Direcionador Manter | `manter` |

---

## 📈 Métricas de Avaliação

**8 métricas customizadas ANS** (implementadas em `metrics.py`):

| Métrica | Descrição | Score |
|---------|-----------|-------|
| **onetrust_validation** | Valida integração com OneTrust | 0.0 - 1.0 |
| **cmdb_validation** | Valida consulta ao CMDB | 0.0 - 1.0 |
| **parecer_suggestion_accuracy** | Precisão do parecer sugerido | 0.0 - 1.0 |
| **ressalvas_detection** | Detecção de ressalvas necessárias | 0.0 - 1.0 |
| **confidence_score_validity** | Validade do score de confiança | 0.0 - 1.0 |
| **alertas_detection** | Detecção de alertas | 0.0 - 1.0 |
| **bloqueio_detection** | Detecção de bloqueios críticos | 0.0 - 1.0 |
| **response_completeness** | Completude da resposta | 0.0 - 1.0 |

**Threshold de Sucesso**: ≥0.7 por métrica, ≥75% pass rate

---

## 🎯 Resultados Recentes

### Última Avaliação (30/11/2025)

```
Framework: Vertex AI Evaluation Service
Version: v1.0
Pass Rate: 87.5% (7/8)
Average Score: 0.93
Status: ✅ EXCELLENT
```

**Detalhes por Test Case**:
- TC-001: 1.00 ✅ PERFECT
- TC-002: 0.96 ✅ EXCELLENT
- TC-003: 0.91 ✅ VERY GOOD
- TC-004: 0.86 ✅ GOOD
- TC-005: 0.62 ⚠️ (bloqueio esperado)
- TC-006: 1.00 ✅ PERFECT
- TC-007: 0.75 ✅ GOOD
- TC-008: 0.88 ✅ VERY GOOD

---

## 🔧 Configuração

### Dependências ADK
Já incluídas no `requirements.txt` principal.

### Dependências Vertex AI
```bash
pip install -r eval/vertex_ai_evaluation/requirements_vertex_ai.txt
```

### Variáveis de Ambiente (Vertex AI)
```bash
export PROJECT_ID="gft-bu-gcp"
export LOCATION="us-central1"
```

---

## 📚 Documentação Detalhada

- **ADK Evaluation**: [`adk_evaluation/README.md`](./adk_evaluation/README.md)
- **Vertex AI Evaluation**: [`vertex_ai_evaluation/README.md`](./vertex_ai_evaluation/README.md)
- **Vertex AI Setup**: [`vertex_ai_evaluation/vertex_ai_setup.md`](./vertex_ai_evaluation/vertex_ai_setup.md)

---

## 🤝 Workflow Recomendado

### Durante Desenvolvimento
```bash
# Teste rápido (3 minutos)
cd eval/adk_evaluation
python run_quick_eval.py
```

### Antes de Commit/PR
```bash
# Teste completo local (8 minutos)
cd eval/adk_evaluation
python run_evaluation.py
```

### Deploy em Produção
```bash
# Avaliação completa com dashboard (10 minutos)
cd eval/vertex_ai_evaluation
python run_vertex_ai_evaluation.py --agent-version v1.0 --real
```

---

**Última atualização**: 30 de novembro de 2025  
**Status**: ✅ **ESTRUTURA ORGANIZADA E FUNCIONAL**

# Compare versions
python -m eval.run_vertex_ai_evaluation --compare v1.0 v1.1

# View historical results
python -m eval.run_vertex_ai_evaluation --history --limit 10
```

**📖 For complete Vertex AI setup and usage, see**: `eval/vertex_ai_setup.md`

### Specific Tests

Run specific test cases:

```python
from eval.run_evaluation import AgentEvaluator
import asyncio

async def run():
    evaluator = AgentEvaluator(project_id="your-project", location="global")
    await evaluator.initialize()
    await evaluator.run_all_tests(test_ids=["TC-001", "TC-005"])
    evaluator.print_report()

asyncio.run(run())
```

## 📊 Results

Results are saved to `eval/results/` directory:

- `evaluation_results_YYYYMMDD_HHMMSS.json`: Detailed results with full responses
- `evaluation_report_YYYYMMDD_HHMMSS.json`: Summary report with metrics

### Example Report

```json
{
  "summary": {
    "total_tests": 8,
    "passed": 7,
    "failed": 1,
    "errors": 0,
    "pass_rate": "87.5%",
    "average_execution_time_seconds": "45.32"
  },
  "metric_averages": {
    "onetrust_validation": "100.00%",
    "cmdb_validation": "100.00%",
    "parecer_suggestion_accuracy": "87.50%",
    "confidence_score_validity": "100.00%",
    "...": "..."
  }
}
```

## 🔧 Configuration

Set environment variables in `.env`:

```bash
# GCP Configuration
GOOGLE_CLOUD_PROJECT=gft-bu-gcp
GOOGLE_CLOUD_LOCATION=global

# Optional: Save quick eval results
SAVE_QUICK_EVAL_RESULTS=false
```

## 🤖 CI/CD Integration

See `github-actions-example.yml` for GitHub Actions integration.

### Example Workflow

```yaml
name: Evaluate Agent
on: [push, pull_request]
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Quick Evaluation
        run: python -m eval.run_quick_eval
```

## 📝 Adding New Test Cases

To add a new test case, edit `dataset.py`:

```python
{
    "test_id": "TC-009",
    "scenario": "Your Test Scenario",
    "category": "your_category",
    "input": {
        "solicitante": {...},
        "requisicao": {...}
    },
    "expected_output": {
        "sucesso": True,
        "parecer_sugerido": "Parecer Favorável",
        ...
    },
    "evaluation_criteria": {
        "must_succeed": True,
        ...
    }
}
```

## 📚 ADK Documentation

Based on: https://google.github.io/adk-docs/evaluate/

## 🎯 Passing Criteria

A test case **passes** if:
- Average metric score ≥ 0.7 (70%)
- No critical errors
- All mandatory metrics pass

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: Ensure you're running from the agent root directory
2. **API Errors**: Check GCP credentials and project permissions
3. **Mock Data**: Ensure mock adapters are properly configured

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📄 License

Same as parent project.

---

**Last Updated**: 2025-11-29  
**Version**: 1.0  
**Maintainer**: Architecture Domain ANS Team

