# Vertex AI Evaluation Service

Framework de avaliação usando **Google Cloud Vertex AI Evaluation Service** (Enterprise).

## 📁 Estrutura

```
vertex_ai_evaluation/
├── run_vertex_ai_evaluation.py    # Script principal de execução
├── vertex_ai_evaluation.py        # Classe de avaliação Vertex AI
├── vertex_ai_setup.md             # Guia de configuração
├── requirements_vertex_ai.txt     # Dependências adicionais
├── dataset.py                     # Dataset de teste
├── metrics.py                     # Métricas de avaliação
├── custom_metrics.py              # Métricas customizadas ANS
├── results/                       # Resultados das avaliações
│   └── vertex_ai_evaluation_*.json
└── README.md                      # Este arquivo
```

## 🚀 Como Usar

### Pré-requisitos
```bash
# Instalar dependências
pip install -r requirements_vertex_ai.txt

# Configurar autenticação GCP
gcloud auth application-default login

# Configurar variáveis
export PROJECT_ID="gft-bu-gcp"
export LOCATION="us-central1"
```

### Execução

#### Modo Real (Executa Test Cases)
```bash
cd eval/vertex_ai_evaluation
python run_vertex_ai_evaluation.py --agent-version v1.0 --real
```

**Executa**: 8 test cases reais  
**Tempo**: ~8-10 minutos  
**Output**: BigQuery + GCS + JSON local

#### Dry Run (Validação)
```bash
cd eval/vertex_ai_evaluation
python run_vertex_ai_evaluation.py --dry-run
```

**Executa**: Validação de configuração  
**Tempo**: ~1 minuto  
**Output**: Console apenas

## ☁️ Recursos GCP Utilizados

### BigQuery
- **Dataset**: `architecture_domain_ans_eval`
- **Tabela**: `evaluation_results`
- **Retenção**: 90 dias

### Cloud Storage
- **Bucket**: `gs://gft-bu-gcp-eval-staging`
- **Path**: `datasets/eval_dataset_*.jsonl`
- **Lifecycle**: 30 dias

### Vertex AI
- **Service**: Evaluation API (Preview)
- **Location**: us-central1
- **Model**: gemini-3-pro-preview

## 📊 Métricas Avaliadas

### Standard Metrics (Vertex AI)
- ✅ **tool_use_quality**: Uso de ferramentas
- ✅ **response_quality**: Qualidade geral
- ✅ **safety**: Segurança
- ✅ **groundedness**: Fundamentação
- ✅ **instruction_following**: Conformidade

### Custom Metrics (ANS Domain)
- ✅ **onetrust_validation**: 0.0 - 1.0
- ✅ **cmdb_validation**: 0.0 - 1.0
- ✅ **parecer_suggestion_accuracy**: 0.0 - 1.0
- ✅ **ressalvas_detection**: 0.0 - 1.0
- ✅ **confidence_score_validity**: 0.0 - 1.0
- ✅ **alertas_detection**: 0.0 - 1.0
- ✅ **bloqueio_detection**: 0.0 - 1.0
- ✅ **response_completeness**: 0.0 - 1.0

## 📈 Resultados

### Última Avaliação (v1.0)
```
Date: 2025-11-30 02:09
Pass Rate: 87.5% (7/8)
Average Score: 0.93
Status: ✅ EXCELLENT
```

### Acesso aos Resultados

#### 1. Vertex AI Console
```
https://console.cloud.google.com/vertex-ai/generative/evaluation/eval-20251130-020950?project=gft-bu-gcp
```

#### 2. BigQuery
```sql
SELECT 
  test_id,
  scenario,
  status,
  average_score,
  execution_time
FROM `gft-bu-gcp.architecture_domain_ans_eval.evaluation_results`
ORDER BY timestamp DESC
LIMIT 10;
```

#### 3. Arquivo Local
```bash
cat eval/vertex_ai_evaluation/results/vertex_ai_evaluation_20251130_020950.json
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
PROJECT_ID="gft-bu-gcp"
LOCATION="us-central1"
STAGING_BUCKET="gs://gft-bu-gcp-eval-staging"
BQ_DATASET="architecture_domain_ans_eval"
```

### Permissões IAM Necessárias
- ✅ `roles/aiplatform.user`
- ✅ `roles/bigquery.dataEditor`
- ✅ `roles/storage.objectAdmin`

## 📝 Estrutura dos Resultados

```json
{
  "evaluation_id": "eval-20251130-020950",
  "agent_version": "v1.0",
  "timestamp": "2025-11-30T02:09:50",
  "summary": {
    "total_tests": 8,
    "passed": 7,
    "failed": 1,
    "pass_rate": 0.875,
    "average_score": 0.93
  },
  "test_results": [
    {
      "test_id": "TC-001",
      "status": "PASS",
      "score": 1.00,
      "metrics": { ... }
    }
  ],
  "gcp_resources": {
    "bigquery_table": "gft-bu-gcp.architecture_domain_ans_eval.evaluation_results",
    "gcs_dataset": "gs://gft-bu-gcp-eval-staging/datasets/eval_dataset_20251130_020950.jsonl",
    "dashboard_url": "https://console.cloud.google.com/vertex-ai/..."
  }
}
```

## 🎯 Threshold de Sucesso

- **Score mínimo**: 0.7
- **Pass rate esperado**: ≥75%
- **Execução completa**: 8/8 testes

## 🐛 Troubleshooting

### Erro: "Permission Denied"
```bash
gcloud auth application-default login
gcloud config set project gft-bu-gcp
```

### Erro: "BigQuery table not found"
O script cria automaticamente. Verifique permissões.

### Erro: "Bucket not found"
```bash
gsutil mb -p gft-bu-gcp -l us-central1 gs://gft-bu-gcp-eval-staging
```

## 📚 Documentação Adicional

- **Setup Guide**: `vertex_ai_setup.md`
- **API Reference**: Google Cloud Vertex AI Evaluation
- **Pricing**: https://cloud.google.com/vertex-ai/pricing

---

**Última atualização**: 30 de novembro de 2025  
**Status**: ✅ **PRODUÇÃO - SCORES OTIMIZADOS**

