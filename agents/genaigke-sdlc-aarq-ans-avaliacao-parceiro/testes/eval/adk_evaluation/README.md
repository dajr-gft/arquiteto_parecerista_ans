# 🧪 ADK Evaluation - BV ANS Agent

Avaliação local programática usando o framework ADK (Agent Development Kit) da Google.

---

## 📋 Visão Geral

Este módulo fornece avaliação rápida e local do agente BV ANS, ideal para:
- ✅ Desenvolvimento e debugging
- ✅ Testes em CI/CD pipelines
- ✅ Validação rápida de mudanças
- ✅ Análise detalhada de casos específicos

---

## 🚀 Início Rápido

### **Pré-requisitos**

```bash
# Certifique-se de estar no diretório correto
cd bv_ans/testes/eval/adk_evaluation

# Verifique se as dependências estão instaladas
pip install -r ../../../../requirements.txt
```

### **Avaliação Rápida (5-7 minutos)**

```bash
python run_quick_eval.py
```

Executa 7 casos de teste representativos cobrindo:
- Análise de documentos
- Análise de planilhas
- Extração de contratos
- Pareceres rápidos
- Tratamento de erros
- Status do sistema

### **Avaliação Completa (15-20 minutos)**

```bash
python run_evaluation.py
```

Executa todos os 15 casos de teste do dataset completo.

---

## 📊 Casos de Teste

### **Categorias**

| Categoria | Casos | Descrição |
|-----------|-------|-----------|
| `document_analysis` | 2 | Análise de especificações técnicas e propostas |
| `spreadsheet_analysis` | 2 | Análise de planilhas Excel/CSV |
| `contract_extraction` | 1 | Extração de dados de contratos |
| `multi_document_analysis` | 1 | Comparação entre múltiplos documentos |
| `simple_opinion` | 1 | Pareceres rápidos |
| `system_status` | 1 | Verificação de status |
| `error_handling` | 2 | Tratamento de erros |
| `complex_analysis` | 1 | Análise complexa técnica+comercial |
| `performance` | 1 | Testes de performance |
| `edge_case` | 1 | Casos limite |
| `real_world` | 1 | Caso real compliance |
| `integration` | 1 | Teste de integração completa |

### **Visualizar Dataset**

```bash
python dataset.py
```

Output:
```
📊 BV ANS Agent Evaluation Dataset Statistics

Total test cases: 15

Categories:
  - document_analysis: 2 tests
  - spreadsheet_analysis: 2 tests
  - contract_extraction: 1 tests
  ...
```

---

## 📈 Métricas Avaliadas

### **Métricas Básicas**
1. **Success**: Agente completou a tarefa com sucesso?
2. **Response Quality**: Qualidade geral da resposta

### **Métricas Customizadas** (específicas BV ANS)
3. **Document Analysis**: Qualidade de análise de documentos
4. **Spreadsheet Analysis**: Precisão em análise de planilhas
5. **Framework Adherence**: Aderência ao framework de 8 pilares
6. **Tool Usage**: Uso correto de ferramentas
7. **Response Completeness**: Completude da resposta
8. **Performance**: Eficiência e tempo de resposta

Cada métrica retorna:
- **Score**: 0.0 a 1.0 (0% a 100%)
- **Feedback**: Comentários descritivos
- **Details**: Breakdown detalhado

---

## 📄 Resultados

### **Formato JSON**

Resultados são salvos em `results/evaluation_YYYYMMDD_HHMMSS.json`:

```json
{
  "timestamp": "20251207_143022",
  "total_tests": 15,
  "passed": 13,
  "failed": 2,
  "results": [
    {
      "test_id": "TC-DOC-001",
      "scenario": "Análise de Especificação Técnica Completa",
      "category": "document_analysis",
      "execution_time": 8.45,
      "iterations": 3,
      "passed": true,
      "evaluation": {
        "overall_score": 0.87,
        "metrics": {
          "success": {"score": 1.0},
          "document_analysis": {"score": 0.92},
          "framework_adherence": {"score": 0.88},
          ...
        }
      }
    }
  ]
}
```

### **Relatório HTML**

Dashboard interativo salvo em `results/evaluation_YYYYMMDD_HHMMSS.html`:

- 📊 Resumo executivo com scores
- ✅ Testes passados/falhados
- 📈 Breakdown por categoria
- 🔍 Detalhes de cada teste
- 🎨 Visualização colorida

Abra no navegador para navegação interativa.

---

## 🔧 Personalização

### **Executar Casos Específicos**

```python
# run_custom.py
import asyncio
from run_evaluation import AgentEvaluator

async def main():
    evaluator = AgentEvaluator(
        project_id="gft-bu-gcp",
        location="us-central1"
    )
    await evaluator.initialize()
    
    # Executar apenas testes de documento
    await evaluator.run_all_tests(test_ids=[
        "TC-DOC-001",
        "TC-DOC-002"
    ])
    
    evaluator.print_report()
    evaluator.save_results()

asyncio.run(main())
```

### **Executar por Categoria**

```python
# Executar apenas testes de spreadsheet
await evaluator.run_all_tests(categories=["spreadsheet_analysis"])
```

### **Adicionar Novo Caso de Teste**

Edite `dataset.py`:

```python
{
    "test_id": "TC-CUSTOM-001",
    "scenario": "Meu Caso de Teste Customizado",
    "category": "custom",
    "input": {
        "request": {
            "tipo_analise": "custom",
            # ... seus dados
        }
    },
    "expected_output": {
        "sucesso": True,
        # ... expectativas
    },
    "evaluation_criteria": {
        "must_succeed": True,
        # ... critérios
    }
}
```

---

## 🎯 Interpretação de Scores

| Score Range | Classificação | Ação |
|-------------|---------------|------|
| 0.90 - 1.00 | 🟢 Excelente | Pronto para produção |
| 0.75 - 0.89 | 🟡 Bom | Revisar falhas pontuais |
| 0.60 - 0.74 | 🟠 Adequado | Melhorias necessárias |
| 0.00 - 0.59 | 🔴 Insuficiente | Correções críticas |

### **Análise de Falhas**

Quando um teste falha (score < 0.70):

1. **Verifique o feedback**: Cada métrica fornece feedback específico
2. **Analise a resposta**: Veja `response` no JSON
3. **Compare com esperado**: Veja `expected_output`
4. **Revise os critérios**: Veja `evaluation_criteria`

---

## 🐛 Troubleshooting

### **Erro: "Cannot import root_agent"**

```bash
# Verifique o caminho do agente
cd ../../../
python -c "from src.routes.agent import root_agent; print(root_agent)"

# Se falhar, ajuste sys.path em run_evaluation.py
```

### **Testes muito lentos**

```bash
# Use quick eval
python run_quick_eval.py

# Ou reduza o dataset temporariamente em dataset.py
```

### **Errors de encoding (Windows)**

O script já inclui correção automática de encoding UTF-8. Se ainda houver problemas:

```bash
# No PowerShell, execute:
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python run_evaluation.py
```

### **Vertex AI credentials**

```bash
# Configure credenciais
gcloud auth application-default login

# Ou defina variável de ambiente
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\key.json"
```

---

## 📚 Estrutura de Arquivos

```
adk_evaluation/
├── __init__.py              # Módulo Python
├── README.md                # Este arquivo
├── dataset.py               # 15 casos de teste documentados
├── custom_metrics.py        # 6 métricas customizadas
├── metrics.py               # Agregador de métricas
├── run_evaluation.py        # Script principal (todos os testes)
├── run_quick_eval.py        # Script rápido (7 testes)
└── results/                 # Resultados salvos
    ├── .gitkeep
    ├── evaluation_*.json    # Resultados detalhados
    └── evaluation_*.html    # Dashboard interativo
```

---

## 🔄 Integração CI/CD

### **GitHub Actions**

```yaml
name: Agent Evaluation

on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Quick Evaluation
        env:
          GOOGLE_CLOUD_PROJECT: ${{ secrets.GCP_PROJECT }}
          GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GCP_SA_KEY }}
        run: |
          cd bv_ans/testes/eval/adk_evaluation
          python run_quick_eval.py
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: evaluation-results
          path: bv_ans/testes/eval/adk_evaluation/results/
```

### **GitLab CI**

```yaml
evaluate:
  stage: test
  script:
    - pip install -r requirements.txt
    - cd bv_ans/testes/eval/adk_evaluation
    - python run_quick_eval.py
  artifacts:
    paths:
      - bv_ans/testes/eval/adk_evaluation/results/
    expire_in: 1 week
```

---

## 📞 Suporte

**Dúvidas?**
- Time de Arquitetura: arquitetura@bancobv.com.br
- GFT BU GCP: bucp@gft.com
- Documentação ADK: https://google.github.io/adk-docs/evaluate/

---

**Desenvolvido com ❤️ pelo Time de Arquitetura - Banco BV & GFT**

