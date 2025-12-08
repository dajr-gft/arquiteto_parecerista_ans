# 📁 src/utils/ - Utilitários do Agente

Este diretório contém módulos utilitários usados pelo agente BV ANS.

## 📦 Módulos Ativos

### `security.py`
Validações de segurança para uploads de arquivos.

**Funções:**
- `validate_file_security(file, content)` - Valida tamanho, MIME type e conteúdo
- `validate_files_count(count)` - Valida número de arquivos

**Configuração via .env:**
- `MAX_FILE_SIZE` - Tamanho máximo de arquivo (padrão: 10 MB)
- `MAX_FILES` - Número máximo de arquivos (padrão: 5)

---

### `audit.py`
Logging estruturado e auditoria para compliance.

**Funções:**
- `log_request_audit(...)` - Registra auditoria de requisições
- `log_response_audit(...)` - Registra auditoria de respostas

**Informações capturadas:**
- Request ID único
- User ID e Session ID
- Timestamps
- Métricas de latência
- Status de sucesso/falha

---

## 🔐 Autenticação

Este agente usa **autenticação do GCP (IAM) via Service Account**.

Configurado em: `contract.yml`
```yaml
serviceAccountName: ans-agent-sa
```

**Não é necessário API Keys** - a autenticação é automática via Vertex AI.

---

## 📂 Diretório examples/

Contém exemplos de código e implementações opcionais que podem ser úteis no futuro, mas não estão em uso atualmente.

### `examples/auth_example.py`
Implementação de autenticação via API Keys (OPCIONAL).

**Quando usar:**
- Chamadas externas ao GCP
- Controle de acesso por departamento
- Desenvolvimento local sem GCP

**Como habilitar:**
Veja documentação em `AUTHENTICATION_GUIDE.md` na raiz do projeto.

---

## 📝 Como Usar

### Importar validação de segurança:
```python
from src.utils.security import validate_file_security

# Validar arquivo
content = await file.read()
validate_file_security(file, content)
```

### Importar auditoria:
```python
from src.utils.audit import log_request_audit, log_response_audit

# Log de requisição
log_request_audit(
    request_id=request_id,
    user_id=user_id,
    session_id=session_id,
    text_length=len(text),
    files_count=len(files),
    files_info=files_info
)
```

---

## 🧪 Testes

Testes unitários para estes módulos devem estar em:
```
tests/utils/
├── test_security.py
└── test_audit.py
```

---

**Criado:** 07/12/2025  
**Versão:** 1.0

