# 🧪 Avaliação Completa do Agente BV ANS (Arquiteto Parecerista)

Sistema profissional de avaliação e validação do **Agente BV ANS - Arquiteto de Negócios e Soluções**, utilizando as melhores práticas do **ADK (Agent Development Kit)** e **Vertex AI Evaluation Service**.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estrutura de Diretórios](#estrutura-de-diretórios)
- [Métodos de Avaliação](#métodos-de-avaliação)
- [Início Rápido](#início-rápido)
- [Configuração Detalhada](#configuração-detalhada)
- [Métricas Customizadas](#métricas-customizadas)
- [Interpretação de Resultados](#interpretação-de-resultados)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

Este framework de avaliação foi desenvolvido especificamente para validar:

### **Funcionalidades do Agente**
- ✅ **Análise de Documentos Técnicos** (PDFs, TXT, DOCX)
- ✅ **Análise de Planilhas** (Excel, CSV)
- ✅ **Extração de Dados de Contratos**
- ✅ **Geração de Pareceres Arquiteturais**
- ✅ **Avaliação de Propostas de Fornecedores**
- ✅ **Consulta de Status do Sistema**

### **Capacidades Avaliadas**
- 📊 **Qualidade de Resposta**: Completude, clareza e precisão
- 🎯 **Aderência ao Framework de 8 Pilares**: Business alignment, compliance, riscos
- 🛠️ **Uso Correto de Tools**: Chamadas corretas e tratamento de erros
- 🔒 **Segurança e Compliance**: Validação LGPD, ISO 27001, regulamentações
- ⚡ **Performance**: Tempo de resposta e eficiência
- 🧠 **Raciocínio Arquitetural**: Profundidade e qualidade da análise

---

## 📁 Estrutura de Diretórios

```
bv_ans/testes/eval/
├── README.md                          # Este arquivo
├── __init__.py                         # Módulo Python
│
├── adk_evaluation/                     # Avaliação com ADK Framework
│   ├── __init__.py
│   ├── README.md                       # Documentação ADK
│   ├── dataset.py                      # Dataset de casos de teste
│   ├── custom_metrics.py               # Métricas customizadas específicas
│   ├── metrics.py                      # Agregador de métricas
│   ├── run_evaluation.py               # Script principal de avaliação
│   ├── run_quick_eval.py               # Avaliação rápida (subset)
│   └── results/                        # Resultados das avaliações
│       ├── .gitkeep
│       └── [evaluation_TIMESTAMP]/
│
└── vertex_ai_evaluation/               # Avaliação com Vertex AI
    ├── __init__.py
    ├── README.md                       # Documentação Vertex AI
    ├── vertex_ai_setup.md              # Setup inicial do Vertex AI
    ├── requirements_vertex_ai.txt      # Dependências específicas
    ├── dataset.py                      # Dataset compatível com Vertex AI
    ├── custom_metrics.py               # Métricas para Vertex AI Evaluation
    ├── metrics.py                      # Métricas padrão
    ├── vertex_ai_evaluation.py         # Serviço de avaliação Vertex AI
    ├── run_vertex_ai_evaluation.py     # Script principal Vertex AI
    └── results/                        # Resultados Vertex AI
        ├── .gitkeep
        └── [evaluation_TIMESTAMP]/
```

---

## 🔬 Métodos de Avaliação

### **1. ADK Evaluation (Local/CI/CD)**

Avaliação programática usando o framework ADK da Google.

#### **Vantagens**
- ✅ Execução local rápida
- ✅ Integração fácil com CI/CD
- ✅ Controle total sobre métricas
- ✅ Resultados em JSON/HTML
- ✅ Não requer infraestrutura adicional

#### **Casos de Uso**
- Testes durante desenvolvimento
- Validação em pull requests
- Regressão automática
- Debugging de comportamentos específicos

#### **Como Executar**
```bash
# Avaliação completa
cd bv_ans/testes/eval/adk_evaluation
python run_evaluation.py

# Avaliação rápida (3-5 minutos)
python run_quick_eval.py
```

---

### **2. Vertex AI Evaluation (Produção/Dashboards)**

Avaliação gerenciada com dashboards visuais e armazenamento centralizado.

#### **Vantagens**
- ✅ Dashboard visual interativo no Google Cloud Console
- ✅ Histórico de avaliações no BigQuery
- ✅ Comparação entre versões do agente
- ✅ Métricas automatizadas (safety, groundedness, tool use)
- ✅ Relatórios executivos prontos
- ✅ Integração com MLOps

#### **Casos de Uso**
- Avaliação pré-produção
- Comparação A/B entre versões
- Relatórios para stakeholders
- Monitoramento contínuo de qualidade
- Auditorias e compliance

#### **Como Executar**
```bash
cd bv_ans/testes/eval/vertex_ai_evaluation
python run_vertex_ai_evaluation.py
```

---

## ⚡ Início Rápido

### **Pré-requisitos**

1. **Python 3.10+** instalado
2. **Credenciais GCP** configuradas:
   ```bash
   gcloud auth application-default login
   ```
3. **Variáveis de ambiente** (criar `.env` na raiz do projeto):
   ```env
   GOOGLE_CLOUD_PROJECT=gft-bu-gcp
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_GENAI_USE_VERTEXAI=True
   AGENT_NAME=bv_ans_agent
   AGENT_MODEL=gemini-2.0-flash-exp
   ```

### **Instalação de Dependências**

```bash
# Na raiz do projeto bv_ans
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Para Vertex AI Evaluation (opcional)
pip install -r testes/eval/vertex_ai_evaluation/requirements_vertex_ai.txt
```

### **Executar Avaliação Rápida (5 minutos)**

```bash
cd testes/eval/adk_evaluation
python run_quick_eval.py
```

### **Resultados**

Os resultados serão salvos em:
- **Console**: Resumo com scores
- **JSON**: `results/quick_eval_TIMESTAMP.json`
- **HTML**: `results/quick_eval_TIMESTAMP.html` (dashboard navegável)

---

## ⚙️ Configuração Detalhada

### **1. Configurar Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto `bv_ans/`:

```env
# === Google Cloud Configuration ===
GOOGLE_CLOUD_PROJECT=gft-bu-gcp
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=True

# === Agent Configuration ===
AGENT_NAME=bv_ans_agent
AGENT_MODEL=gemini-2.0-flash-exp
AGENT_DESCRIPTION="Business and Solutions Architecture Agent - Expert in ANS domain for Banco BV"

# === Evaluation Configuration ===
EVAL_OUTPUT_DIR=testes/eval/results
SAVE_EVAL_RESULTS=true
EVAL_VERBOSE=true

# === Vertex AI Evaluation (Optional) ===
VERTEX_AI_STAGING_BUCKET=gft-bu-gcp-eval-staging
VERTEX_AI_BIGQUERY_DATASET=bv_ans_evaluation
```

### **2. Personalizar Dataset**

Edite `adk_evaluation/dataset.py` ou `vertex_ai_evaluation/dataset.py` para:
- Adicionar novos casos de teste
- Modificar cenários existentes
- Ajustar critérios de avaliação

### **3. Criar Métricas Customizadas**

Adicione métricas específicas em `custom_metrics.py`:

```python
def custom_document_analysis_metric(
    response: Dict[str, Any],
    expected: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, float]:
    """
    Avalia a qualidade da análise de documentos.
    """
    score = 0.0
    feedback = []
    
    # Sua lógica de avaliação aqui
    if "parecer_final" in response:
        score += 0.5
        feedback.append("✅ Parecer final presente")
    
    return {
        "score": score,
        "feedback": " | ".join(feedback)
    }
```

---

## 📊 Métricas Customizadas

### **Métricas Específicas do BV ANS Agent**

#### **1. Document Analysis Quality (`document_analysis_metric`)**
Avalia a qualidade da análise de documentos técnicos:
- ✅ Identificação correta de elementos-chave (requisitos, riscos, compliance)
- ✅ Profundidade da análise arquitetural
- ✅ Aderência ao framework de 8 pilares
- ✅ Clareza e estruturação do parecer

#### **2. Spreadsheet Analysis Accuracy (`spreadsheet_analysis_metric`)**
Valida a análise de planilhas:
- ✅ Extração correta de dados tabulares
- ✅ Identificação de inconsistências
- ✅ Cálculo correto de métricas (totais, médias, etc.)
- ✅ Detecção de problemas de qualidade de dados

#### **3. Framework Adherence (`framework_adherence_metric`)**
Verifica aderência ao Framework de 8 Pilares:
- ✅ Cobertura dos 8 pilares arquiteturais
- ✅ Análise de riscos completa
- ✅ Avaliação de compliance e governança
- ✅ Recomendações acionáveis

#### **4. Tool Usage Correctness (`tool_usage_metric`)**
Monitora o uso correto de ferramentas:
- ✅ Chamadas de tools apropriadas para cada cenário
- ✅ Tratamento correto de erros
- ✅ Sequência lógica de chamadas
- ✅ Validação de parâmetros

#### **5. Response Completeness (`response_completeness_metric`)**
Garante completude das respostas:
- ✅ Todos os campos obrigatórios presentes
- ✅ Justificativas adequadas
- ✅ Nível de detalhe apropriado
- ✅ Formato JSON válido

#### **6. Performance Efficiency (`performance_metric`)**
Monitora eficiência:
- ✅ Tempo de resposta < 10 segundos
- ✅ Número de iterações do agente
- ✅ Uso eficiente de tokens

---

## 📈 Interpretação de Resultados

### **Scores de Avaliação**

| Score | Classificação | Ação Recomendada |
|-------|---------------|------------------|
| **0.90 - 1.00** | 🟢 Excelente | Pronto para produção |
| **0.75 - 0.89** | 🟡 Bom | Revisar casos com score baixo |
| **0.60 - 0.74** | 🟠 Adequado | Melhorias necessárias |
| **0.00 - 0.59** | 🔴 Insuficiente | Correções críticas necessárias |

### **Análise de Falhas**

1. **Falhas Críticas** (score < 0.5):
   - Revisar lógica do agente
   - Verificar prompts
   - Validar tools e integrações

2. **Falhas Moderadas** (0.5 ≤ score < 0.75):
   - Refinar prompts para melhor contexto
   - Ajustar parâmetros de temperatura
   - Adicionar exemplos few-shot

3. **Falhas Pontuais** (score ≥ 0.75):
   - Casos edge específicos
   - Ajustes finos em métricas customizadas

### **Métricas Agregadas**

```json
{
  "overall_score": 0.87,
  "metrics_breakdown": {
    "document_analysis": 0.92,
    "spreadsheet_analysis": 0.85,
    "framework_adherence": 0.89,
    "tool_usage": 0.91,
    "response_completeness": 0.88,
    "performance": 0.76
  },
  "test_cases": {
    "total": 15,
    "passed": 13,
    "failed": 2,
    "success_rate": 0.867
  }
}
```

---

## 🐛 Troubleshooting

### **Erro: "Module not found"**
```bash
# Certifique-se de estar no diretório correto
cd bv_ans/testes/eval/adk_evaluation

# Instale dependências
pip install -r ../../../requirements.txt
```

### **Erro: "Credentials not found"**
```bash
# Configure credenciais GCP
gcloud auth application-default login

# Ou defina a variável de ambiente
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### **Erro: "Agent not found"**
```bash
# Verifique se o agente está importável
cd ../../../
python -c "from src.routes.agent import root_agent; print(root_agent)"
```

### **Evaluation muito lenta**
```bash
# Use avaliação rápida com subset de testes
python run_quick_eval.py

# Ou ajuste o dataset para menos casos
# Edite dataset.py e comente casos de teste
```

### **Resultados inconsistentes**
- Verifique temperatura do modelo (recomendado: 0.2-0.4)
- Use seeds fixos para reprodutibilidade
- Aumente número de tentativas (retries)

---

## 📚 Recursos Adicionais

### **Documentação Oficial**
- [ADK Evaluation Guide](https://google.github.io/adk-docs/evaluate/)
- [Vertex AI Agent Builder Evaluation](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents)
- [Generative AI Evaluation Metrics](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview)

### **Exemplos e Tutoriais**
- `adk_evaluation/README.md` - Guia detalhado ADK
- `vertex_ai_evaluation/README.md` - Guia Vertex AI
- `vertex_ai_evaluation/vertex_ai_setup.md` - Setup passo-a-passo

### **Datasets**
- `adk_evaluation/dataset.py` - 15+ casos de teste documentados
- `vertex_ai_evaluation/dataset.py` - Dataset compatível com Vertex AI

---

## 🤝 Contribuindo

Para adicionar novos casos de teste ou métricas:

1. Edite `dataset.py` com novo caso de teste
2. Adicione métricas customizadas em `custom_metrics.py`
3. Execute avaliação para validar
4. Documente o caso de teste no código

---

## 📞 Suporte

Para dúvidas ou problemas:
- **Time de Arquitetura**: arquitetura@bancobv.com.br
- **GFT BU GCP**: bucp@gft.com
- **Documentação Interna**: Confluence BV

---

## 📝 Changelog

### **v1.0.0** (2025-12-07)
- ✅ Estrutura completa de avaliação
- ✅ 15+ casos de teste documentados
- ✅ 6 métricas customizadas específicas
- ✅ Suporte ADK e Vertex AI Evaluation
- ✅ Dashboard HTML interativo
- ✅ Integração CI/CD ready

---

**Desenvolvido com ❤️ pelo Time de Arquitetura - Banco BV & GFT**

