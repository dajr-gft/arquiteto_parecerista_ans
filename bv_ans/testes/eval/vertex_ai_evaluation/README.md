# 🎯 Vertex AI Evaluation - BV ANS Agent

Avaliação gerenciada com dashboards visuais e armazenamento centralizado usando **Vertex AI Evaluation Service**.

---

## 📋 Visão Geral

Este módulo fornece avaliação enterprise-grade do agente BV ANS usando a infraestrutura Google Cloud, ideal para:
- ✅ Avaliações pré-produção
- ✅ Comparação A/B entre versões
- ✅ Relatórios executivos com dashboards
- ✅ Histórico de avaliações no BigQuery
- ✅ Auditorias e compliance
- ✅ Monitoramento contínuo de qualidade

---

## 🚀 Setup Inicial

### **1. Instalar Dependências**

```bash
cd bv_ans/testes/eval/vertex_ai_evaluation
pip install -r requirements_vertex_ai.txt
```

### **2. Configurar GCP**

```bash
# Autenticar
gcloud auth application-default login

# Definir projeto
gcloud config set project gft-bu-gcp

# Habilitar APIs necessárias
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable bigquery.googleapis.com
```

### **3. Criar Recursos GCS e BigQuery**

O script cria automaticamente:
- **GCS Bucket**: `gft-bu-gcp-eval-staging`
- **BigQuery Dataset**: `bv_ans_evaluation`
- **BigQuery Table**: `evaluation_results`

---

## 🎯 Executar Avaliação

### **Avaliação Completa com Vertex AI**

```bash
python run_vertex_ai_evaluation.py
```

Isso irá:
1. ✅ Criar dataset de avaliação no GCS
2. ✅ Executar avaliação gerenciada no Vertex AI
3. ✅ Salvar resultados no BigQuery
4. ✅ Gerar link para dashboard visual
5. ✅ Salvar relatório local

### **Visualizar Resultados**

Após a execução, você receberá:

1. **Console Output**:
   ```
   ✅ Evaluation completed!
   📊 Dashboard URL: https://console.cloud.google.com/vertex-ai/...
   💾 Results saved to BigQuery: bv_ans_evaluation.evaluation_results
   ```

2. **Dashboard Visual** (Google Cloud Console):
   - Métricas agregadas
   - Comparação entre testes
   - Breakdown por categoria
   - Histórico de execuções

3. **BigQuery** (para análises customizadas):
   ```sql
   SELECT 
     evaluation_id,
     display_name,
     timestamp,
     metrics_summary
   FROM `gft-bu-gcp.bv_ans_evaluation.evaluation_results`
   ORDER BY timestamp DESC
   LIMIT 10;
   ```

---

## 📊 Vantagens sobre ADK Local

| Recurso | ADK Local | Vertex AI |
|---------|-----------|-----------|
| Dashboard Visual | ❌ | ✅ Console interativo |
| Histórico Centralizado | ❌ | ✅ BigQuery |
| Comparação de Versões | Manual | ✅ Automática |
| Métricas Automatizadas | Limitado | ✅ Safety, Groundedness, Tool Use |
| Escalabilidade | Local | ✅ Cloud managed |
| Relatórios Executivos | HTML básico | ✅ Dashboards profissionais |
| Auditoria | JSON local | ✅ BigQuery auditável |

---

## 🔧 Configuração Avançada

### **Customizar Avaliação**

Edite `run_vertex_ai_evaluation.py`:

```python
config = VertexAIEvaluationConfig(
    project_id="gft-bu-gcp",
    location="us-central1",
    staging_bucket="meu-bucket-eval",
    bigquery_dataset="meu_dataset_eval",
    evaluation_display_name="BV-ANS-v2.0-eval"
)
```

### **Adicionar Métricas Vertex AI Padrão**

O Vertex AI Evaluation Service inclui métricas automáticas:

- **Safety**: Detecção de conteúdo inseguro/inapropriado
- **Groundedness**: Aderência a fontes/documentos
- **Fluency**: Fluência e naturalidade do texto
- **Tool Use Quality**: Qualidade no uso de ferramentas
- **Fulfillment**: Atendimento completo à requisição

Para habilitar:

```python
# Em vertex_ai_evaluation.py
metrics = [
    "safety",
    "groundedness",
    "tool_use_quality",
    "fulfillment"
]
```

---

## 📈 Análises no BigQuery

### **Evolução de Scores ao Longo do Tempo**

```sql
SELECT 
  DATE(timestamp) as data,
  AVG(JSON_VALUE(metrics_summary, '$.overall_score')) as avg_score,
  COUNT(*) as num_evaluations
FROM `gft-bu-gcp.bv_ans_evaluation.evaluation_results`
WHERE agent_id = 'bv_ans_agent'
GROUP BY data
ORDER BY data DESC;
```

### **Comparar Duas Versões**

```sql
WITH v1 AS (
  SELECT * FROM `gft-bu-gcp.bv_ans_evaluation.evaluation_results`
  WHERE display_name LIKE '%v1.0%'
  ORDER BY timestamp DESC LIMIT 1
),
v2 AS (
  SELECT * FROM `gft-bu-gcp.bv_ans_evaluation.evaluation_results`
  WHERE display_name LIKE '%v2.0%'
  ORDER BY timestamp DESC LIMIT 1
)
SELECT 
  'v1.0' as version,
  JSON_VALUE(v1.metrics_summary, '$.overall_score') as score
FROM v1
UNION ALL
SELECT 
  'v2.0' as version,
  JSON_VALUE(v2.metrics_summary, '$.overall_score') as score
FROM v2;
```

### **Identificar Testes com Falhas Recorrentes**

```sql
SELECT 
  JSON_VALUE(metrics_summary, '$.test_id') as test_id,
  COUNT(*) as num_failures,
  AVG(JSON_VALUE(metrics_summary, '$.score')) as avg_score
FROM `gft-bu-gcp.bv_ans_evaluation.evaluation_results`,
  UNNEST(JSON_QUERY_ARRAY(metrics_summary, '$.failed_tests')) as failed_test
WHERE status = 'completed'
GROUP BY test_id
HAVING num_failures > 3
ORDER BY num_failures DESC;
```

---

## 🎨 Dashboard Vertex AI Console

Acesse: `https://console.cloud.google.com/vertex-ai/generative/evaluate`

**Recursos do Dashboard**:

1. **Overview**:
   - Score geral da última avaliação
   - Tendência ao longo do tempo
   - Comparação com baseline

2. **Test Cases**:
   - Lista todos os casos de teste
   - Filtros por categoria, status, score
   - Drill-down em cada teste

3. **Metrics Breakdown**:
   - Gráficos de cada métrica
   - Distribuição de scores
   - Identificação de outliers

4. **Comparisons**:
   - Comparar duas avaliações
   - Ver diferenças de score
   - Identificar regressões

5. **History**:
   - Histórico completo
   - Export para CSV/JSON
   - Anotações e comentários

---

## 🐛 Troubleshooting

### **Erro: "Permission denied"**

```bash
# Garantir permissões necessárias
gcloud projects add-iam-policy-binding gft-bu-gcp \
  --member="user:seu-email@gft.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding gft-bu-gcp \
  --member="user:seu-email@gft.com" \
  --role="roles/bigquery.dataEditor"
```

### **Erro: "Bucket already exists"**

```python
# Em run_vertex_ai_evaluation.py, use bucket existente
config = VertexAIEvaluationConfig(
    staging_bucket="existing-bucket-name"
)
```

### **Evaluation não aparece no Console**

1. Verifique o projeto correto no Console
2. Aguarde alguns minutos (processamento assíncrono)
3. Verifique região (deve ser us-central1)
4. Confira logs em Cloud Logging

---

## 📚 Documentação Oficial

- [Vertex AI Evaluation API](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview)
- [Agent Evaluation Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents)
- [Custom Metrics](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-metrics)
- [BigQuery ML](https://cloud.google.com/bigquery-ml/docs)

---

## 📞 Suporte

**Dúvidas sobre Vertex AI Evaluation?**
- Time de Arquitetura: arquitetura@bancobv.com.br
- GFT BU GCP: bucp@gft.com
- Google Cloud Support: Abra caso via Console

---

**Desenvolvido com ❤️ pelo Time de Arquitetura - Banco BV & GFT**

