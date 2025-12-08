# ADK Evaluation Framework

Framework de avaliação usando **Google ADK (Agent Development Kit)** nativo.

## 📁 Estrutura

```
adk_evaluation/
├── run_evaluation.py          # Script principal de avaliação completa
├── run_quick_eval.py          # Script de avaliação rápida
├── dataset.py                 # Dataset de teste
├── metrics.py                 # Métricas de avaliação
├── custom_metrics.py          # Métricas customizadas ANS
├── results/                   # Resultados das avaliações
│   ├── evaluation_results_*.json
│   └── evaluation_report_*.json
└── README.md                  # Este arquivo
```

## 🚀 Como Usar

### Avaliação Completa
```bash
cd eval/adk_evaluation
python run_evaluation.py
```

**Executa**: 8 test cases completos  
**Tempo**: ~8-10 minutos  
**Output**: `results/evaluation_results_YYYYMMDD_HHMMSS.json`

### Avaliação Rápida
```bash
cd eval/adk_evaluation
python run_quick_eval.py
```

**Executa**: 3 test cases principais  
**Tempo**: ~3-5 minutos  
**Output**: Console + JSON resumido

## 📊 Métricas Avaliadas

### Métricas Nativas ADK
- ✅ **tool_use_quality**: Uso correto das tools
- ✅ **response_quality**: Qualidade da resposta
- ✅ **safety**: Segurança e conformidade
- ✅ **groundedness**: Base em dados reais
- ✅ **instruction_following**: Seguimento de instruções

### Métricas Customizadas ANS
- ✅ **onetrust_validation**: Consulta OneTrust
- ✅ **cmdb_validation**: Consulta CMDB
- ✅ **parecer_suggestion_accuracy**: Precisão do parecer
- ✅ **ressalvas_detection**: Detecção de ressalvas
- ✅ **confidence_score_validity**: Validade do score
- ✅ **alertas_detection**: Detecção de alertas
- ✅ **bloqueio_detection**: Detecção de bloqueios
- ✅ **response_completeness**: Completude da resposta

## 📈 Resultados

### Última Avaliação
```
Pass Rate: 87.5% (7/8)
Average Score: 0.87
Total Time: ~8 minutos
```

### Estrutura dos Resultados
```json
{
  "test_id": "TC-001",
  "scenario": "Renovação - Histórico Favorável",
  "status": "PASS",
  "metrics": {
    "onetrust_validation": 1.0,
    "cmdb_validation": 1.0,
    "parecer_accuracy": 1.0,
    "average_score": 0.93
  },
  "execution_time": 73.82
}
```

## 🔧 Configuração

### Dataset de Teste
Editável em `dataset.py`:
- 8 cenários de teste
- Casos de renovação, nova contratação, bloqueio
- Validação de regras de negócio

### Métricas
Personalizáveis em `metrics.py` e `custom_metrics.py`

## 📝 Logs

Os logs são salvos em `eval/adk_evaluation/results/`:
- `evaluation_results_*.json`: Resultados detalhados
- `evaluation_report_*.json`: Relatório agregado

## 🎯 Threshold de Sucesso

- **Score mínimo**: 0.7
- **Pass rate esperado**: ≥75%

---

**Última atualização**: 30 de novembro de 2025

