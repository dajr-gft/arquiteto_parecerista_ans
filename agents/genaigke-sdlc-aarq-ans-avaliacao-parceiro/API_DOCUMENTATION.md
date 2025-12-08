# 📚 Documentação de API - genaigke-sdlc-aarq-ans-avaliacao-parceiro

## Visão Geral

API REST para análise de propostas de fornecedores e geração de pareceres técnicos especializados no domínio ANS (Arquitetura de Negócios e Soluções).

**Base URL**: `/`  
**Versão**: 1.0.0  
**Framework**: FastAPI + Google ADK  

---

## 🔌 Endpoints Disponíveis

### 1. Health Check

#### `POST /health`
Verifica se o serviço está operacional.

**Request:**
```json
{}
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-07T15:30:00.000Z",
  "service": "genaigke-sdlc-aarq-ans-avaliacao-parceiro"
}
```

---

### 2. Readiness Check

#### `POST /ready`
Verifica se o serviço está pronto para receber tráfego.

**Request:**
```json
{}
```

**Response (200 OK):**
```json
{
  "status": "ready",
  "timestamp": "2025-12-07T15:30:00.000Z",
  "service": "genaigke-sdlc-aarq-ans-avaliacao-parceiro",
  "checks": {
    "environment_variables": {
      "status": "ok",
      "required_vars": [
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_LOCATION",
        "GOOGLE_GENAI_USE_VERTEXAI"
      ],
      "all_present": true
    },
    "agent_configuration": {
      "status": "ok",
      "model": "gemini-2.5-pro"
    }
  }
}
```

**Response (503 Service Unavailable):**
```json
{
  "status": "not_ready",
  "checks": {
    "environment_variables": {
      "status": "failed",
      "all_present": false
    }
  }
}
```

---

### 3. Service Info

#### `POST /info`
Retorna informações sobre o serviço.

**Request:**
```json
{}
```

**Response (200 OK):**
```json
{
  "service": "genaigke-sdlc-aarq-ans-avaliacao-parceiro",
  "version": "1.0.0",
  "environment": "production",
  "agent": {
    "name": "ans_expert_agent",
    "model": "gemini-2.5-pro"
  },
  "vertex_ai": {
    "project": "gft-bu-gcp",
    "location": "us-central1",
    "enabled": "True"
  },
  "timestamp": "2025-12-07T15:30:00.000Z"
}
```

---

### 4. Analisar Documento

#### `POST /analisar_documento_parecer`
Analisa documentos técnicos (PDF, TXT, DOCX) e gera parecer arquitetural.

**Request:**
```http
Content-Type: multipart/form-data

file: <binary_file>
```

**Tipos de arquivo aceitos:**
- `.txt` - Texto plano
- `.pdf` - Documentos PDF
- `.doc`, `.docx` - Documentos Word
- `.md` - Markdown

**Limite de tamanho**: 10 MB

**Response (200 OK):**
```json
{
  "filename": "especificacao_tecnica.pdf",
  "status": "success",
  "analise": {
    "parecer_final": "FAVORÁVEL COM RESSALVAS",
    "justificativa": "A solução proposta atende aos requisitos...",
    "riscos_identificados": [
      "Dependência de tecnologia proprietária",
      "Necessidade de capacitação da equipe"
    ],
    "recomendacoes": [
      "Implementar plano de contingência",
      "Estabelecer SLA rigoroso"
    ],
    "pontos_atencao": [
      "Conformidade LGPD requer validação adicional"
    ]
  },
  "tipo_documento": ".pdf",
  "tamanho_bytes": 2456789
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Tipo de arquivo não suportado. Aceitos: .txt, .pdf, .doc, .docx, .md",
  "filename": "arquivo.exe"
}
```

**Response (413 Payload Too Large):**
```json
{
  "detail": "Arquivo muito grande. Tamanho máximo: 10.0 MB"
}
```

**Response (500 Internal Server Error):**
```json
{
  "error": "Erro ao gerar parecer: <detalhes>",
  "filename": "especificacao.pdf"
}
```

---

### 5. Analisar Planilha

#### `POST /analisar_planilha_parecer`
Analisa planilhas (Excel, CSV) com dados estruturados.

**Request:**
```http
Content-Type: multipart/form-data

file: <binary_file>
```

**Tipos de arquivo aceitos:**
- `.xlsx` - Excel
- `.csv` - CSV

**Response (200 OK):**
```json
{
  "filename": "dados_fornecedor.xlsx",
  "status": "success",
  "analise": {
    "total_registros": 150,
    "validacoes": {
      "campos_obrigatorios": "ok",
      "tipos_dados": "ok"
    },
    "resumo": "..."
  }
}
```

---

### 6. Consultar Status

#### `POST /consultar_status`
Consulta o status de processamento de um parecer.

**Request:**
```json
{
  "parecer_id": "PAR-2025-001234"
}
```

**Response (200 OK):**
```json
{
  "parecer_id": "PAR-2025-001234",
  "status": "CONCLUÍDO",
  "timestamp": "2025-12-07T15:30:00.000Z",
  "resultado": {
    "parecer_final": "FAVORÁVEL",
    "data_conclusao": "2025-12-07T15:25:00.000Z"
  }
}
```

**Possíveis status:**
- `EM_PROCESSAMENTO` - Parecer sendo processado
- `CONCLUÍDO` - Parecer concluído com sucesso
- `ERRO` - Erro no processamento
- `AGUARDANDO_APROVAÇÃO` - Aguardando revisão

---

## 🔒 Segurança

### Validações Implementadas

1. **Tamanho de Arquivo**: Máximo 10 MB por arquivo
2. **Quantidade de Arquivos**: Máximo 5 arquivos por requisição
3. **Tipos de Arquivo**: Apenas tipos permitidos (PDF, XLSX, TXT, imagens)
4. **Content Filtering**: Detecção de prompt injection em arquivos texto
5. **MIME Type Validation**: Validação de tipo de conteúdo

### HTTP Status Codes

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | Bad Request - Dados inválidos |
| 413 | Payload Too Large - Arquivo muito grande |
| 415 | Unsupported Media Type - Tipo de arquivo não suportado |
| 500 | Internal Server Error - Erro interno |
| 503 | Service Unavailable - Serviço não disponível |

---

## 📝 Exemplos de Uso

### cURL - Health Check
```bash
curl -X POST http://localhost:8000/health \
  -H "Content-Type: application/json" \
  -d '{}'
```

### cURL - Analisar Documento
```bash
curl -X POST http://localhost:8000/analisar_documento_parecer \
  -F "file=@especificacao_tecnica.pdf"
```

### Python - Consultar Status
```python
import requests

response = requests.post(
    "http://localhost:8000/consultar_status",
    json={"parecer_id": "PAR-2025-001234"}
)

print(response.json())
```

### JavaScript/Fetch - Service Info
```javascript
fetch('http://localhost:8000/info', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({})
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## 🔧 Variáveis de Ambiente

### Obrigatórias

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `GOOGLE_CLOUD_PROJECT` | ID do projeto GCP | `gft-bu-gcp` |
| `GOOGLE_CLOUD_LOCATION` | Região do Vertex AI | `us-central1` |
| `GOOGLE_GENAI_USE_VERTEXAI` | Flag para usar Vertex AI | `True` |

### Opcionais

| Variável | Descrição | Default |
|----------|-----------|---------|
| `AGENT_NAME` | Nome do agente | `ans_expert_agent` |
| `AGENT_MODEL` | Modelo Gemini | `gemini-2.5-pro` |
| `MAX_FILE_SIZE` | Tamanho máx arquivo (bytes) | `10485760` (10MB) |
| `MAX_FILES` | Número máx de arquivos | `5` |
| `APP_VERSION` | Versão da aplicação | `1.0.0` |
| `ENVIRONMENT` | Ambiente de execução | `development` |

---

## 📊 Rate Limits

Atualmente não há rate limiting implementado. Recomenda-se implementar em proxy reverso (ex: NGINX) ou API Gateway.

**Recomendação**:
- 100 requisições por minuto por IP
- 1000 requisições por hora por usuário

---

## 🐛 Troubleshooting

### Erro: "Missing required environment variables"
**Causa**: Variáveis de ambiente não configuradas  
**Solução**: Configurar todas as variáveis obrigatórias no arquivo `.env`

### Erro: "Arquivo muito grande"
**Causa**: Arquivo excede 10 MB  
**Solução**: Reduzir tamanho do arquivo ou aumentar `MAX_FILE_SIZE`

### Erro: "Tipo de arquivo não suportado"
**Causa**: Extensão ou MIME type não permitido  
**Solução**: Usar apenas tipos suportados (PDF, XLSX, TXT, etc)

### Status 503 no /ready
**Causa**: Serviço não está pronto para receber tráfego  
**Solução**: Verificar logs e configuração de environment variables

---

## 📞 Suporte

Para questões técnicas, consulte:
- **Confluence**: https://confluence.bvnet.bv/spaces/TD/pages/280627634
- **Logs**: Verificar logs estruturados do serviço
- **Monitoramento**: Dashboard Sonar e Jenkins

---

**Versão da Documentação**: 1.0  
**Última Atualização**: 07 de Dezembro de 2025

