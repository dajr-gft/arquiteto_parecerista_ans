# Suíte de Testes Unitários - Architecture Domain ANS Agent

## 📋 Visão Geral

Esta é a suíte de testes unitários para o agente **Architecture Domain ANS**, desenvolvido com Google Agent Development Kit (ADK). A suíte foi projetada para garantir qualidade, confiabilidade e cobertura mínima de 85% do código.

## 🏗️ Estrutura da Suíte

```
bv_ans/testes/unit_tests/
├── __init__.py                 # Inicialização do pacote de testes
├── conftest.py                 # Fixtures compartilhadas e configuração pytest
├── test_agent_core.py          # Testes do núcleo do agente
├── test_tools.py               # Testes das ferramentas (tools)
└── test_prompts.py             # Testes dos prompts e templates
```

### Descrição dos Arquivos

#### `conftest.py`
Contém fixtures reutilizáveis e configuração de ambiente de teste:
- **Fixtures de Dados**: CNPJs válidos/inválidos, IDs de API, emails
- **Fixtures OneTrust**: Dados de fornecedores encontrados/não encontrados
- **Fixtures CMDB**: Dados de serviços com diferentes direcionadores
- **Fixtures Histórico**: Pareceres anteriores para análise
- **Fixtures Sugestão**: Dados de requisição com diferentes cenários
- **Fixtures Registro**: Dados completos/incompletos para registro de pareceres

#### `test_agent_core.py`
Testes focados no núcleo do agente:
- ✅ Inicialização e configuração do agente
- ✅ Configuração de modelo (Gemini 3 Pro)
- ✅ Configuração de ferramentas (7 tools esperadas)
- ✅ Configuração de planner e thinking
- ✅ Variáveis de ambiente e integração Vertex AI
- ✅ Logging e constantes
- ✅ Validação de metadados e descrições

**Total**: 40+ testes organizados em 13 classes

#### `test_tools.py`
Testes abrangentes para todas as ferramentas do agente:
- ✅ **integrar_onetrust**: Consulta de fornecedores, normalização de CNPJ, cálculo de vencimento
- ✅ **consultar_cmdb**: Consulta de serviços, direcionadores, metadados
- ✅ **carregar_insumos**: Carregamento de histórico, normalização, padrões identificados
- ✅ **sugerir_parecer**: Lógica de sugestão, critérios aplicados, score de confiança
- ✅ **registrar_parecer**: Validação de campos, geração de ID, persistência
- ✅ **capturar_vencimento**: Verificação de existência e importação
- ✅ **carregar_ressalvas**: Verificação de existência e importação

**Total**: 50+ testes organizados em 7 classes

#### `test_prompts.py`
Testes dos prompts e templates do sistema:
- ✅ Estrutura e existência de prompts
- ✅ Conteúdo e keywords importantes
- ✅ Formatação e qualidade do texto
- ✅ Prompts otimizados vs. base
- ✅ Consistência entre versões
- ✅ Tom profissional e clareza
- ✅ Definição de outputs e contexto

**Total**: 35+ testes organizados em 9 classes

## 🚀 Como Executar os Testes

### Pré-requisitos

1. **Instalar dependências**:
```powershell
pip install -r requirements.txt
```

Isso instalará:
- `pytest>=8.3.5` - Framework de testes
- `pytest-asyncio>=0.26.0` - Suporte para testes assíncronos
- `pytest-cov>=6.0.0` - Cobertura de código
- `pytest-mock>=3.14.0` - Mocking avançado

### Executar Todos os Testes Unitários

```powershell
pytest bv_ans/testes/unit_tests/ -v
```

### Executar com Relatório de Cobertura

```powershell
pytest bv_ans/testes/unit_tests/ -v --cov=architecture_domain_ans --cov-report=term-missing
```

### Executar com Relatório HTML

```powershell
pytest bv_ans/testes/unit_tests/ -v --cov=architecture_domain_ans --cov-report=html
```

O relatório HTML será gerado em `htmlcov/index.html`.

### Executar Arquivo Específico

```powershell
# Apenas testes do agente
pytest bv_ans/testes/unit_tests/test_agent_core.py -v

# Apenas testes de tools
pytest bv_ans/testes/unit_tests/test_tools.py -v

# Apenas testes de prompts
pytest bv_ans/testes/unit_tests/test_prompts.py -v
```

### Executar Teste Específico

```powershell
pytest bv_ans/testes/unit_tests/test_agent_core.py::TestAgentInitialization::test_agent_has_correct_model -v
```

### Executar com Marcadores

```powershell
# Apenas testes rápidos
pytest bv_ans/testes/unit_tests/ -v -m "not slow"

# Apenas testes unitários
pytest bv_ans/testes/unit_tests/ -v -m unit
```

## 📊 Cobertura de Código

### Meta de Cobertura

**Mínimo obrigatório**: 85%

A configuração no `pytest.ini` inclui `--cov-fail-under=85`, o que significa que os testes falharão se a cobertura for inferior a 85%.

### Verificar Cobertura Atual

```powershell
pytest bv_ans/testes/unit_tests/ --cov=architecture_domain_ans --cov-report=term-missing
```

### Interpretar Relatório de Cobertura

O relatório mostrará:
- **Stmts**: Número total de statements
- **Miss**: Statements não cobertos
- **Cover**: Percentual de cobertura
- **Missing**: Linhas específicas não cobertas

Exemplo:
```
Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
architecture_domain_ans/agent.py          45      3    93%    67-69
architecture_domain_ans/tools/...        120      8    93%    150-152, 200-205
---------------------------------------------------------------------
TOTAL                                    500     40    92%
```

## 🔧 Configuração Avançada

### pytest.ini

O arquivo `pytest.ini` na raiz do projeto contém:

```ini
[pytest]
testpaths = tests bv_ans/testes/unit_tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts = 
    -v
    --strict-markers
    --tb=short
    --cov=architecture_domain_ans
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=85
```

### Variáveis de Ambiente

Os testes unitários automaticamente configuram:
- `USE_MOCK=true` - Força modo mock
- `GOOGLE_GENAI_USE_VERTEXAI=False` - Desabilita Vertex AI
- `GOOGLE_CLOUD_PROJECT=test-project-id` - Define projeto de teste

Essas configurações são definidas no `conftest.py` através da fixture `setup_unit_test_environment`.

## 📝 Como Adicionar Novos Testes

### 1. Escolha o Arquivo Correto

- **Testes de lógica do agente**: `test_agent_core.py`
- **Testes de ferramentas**: `test_tools.py`
- **Testes de prompts**: `test_prompts.py`

### 2. Siga o Padrão AAA

```python
def test_nome_descritivo_do_teste(self, fixture_name):
    """
    Breve descrição do que está sendo testado.
    
    Scenario: Contexto do teste
    Expected: Resultado esperado
    """
    # ARRANGE - Preparar dados e mocks
    dados = {"campo": "valor"}
    
    # ACT - Executar a função
    resultado = funcao_testada(dados)
    
    # ASSERT - Verificar resultados
    assert resultado['sucesso'] is True
    assert resultado['campo'] == 'valor_esperado'
```

### 3. Use Fixtures do conftest.py

```python
def test_com_fixture(self, valid_cnpj, onetrust_data_found):
    """Test usando fixtures pré-definidas."""
    resultado = integrar_onetrust(valid_cnpj)
    assert resultado['encontrado'] is True
```

### 4. Adicione Novas Fixtures se Necessário

No `conftest.py`:

```python
@pytest.fixture
def nova_fixture():
    """
    Descrição da fixture.
    
    Returns:
        tipo: Descrição do retorno
    """
    return {"dados": "teste"}
```

### 5. Use Mocking para Dependências Externas

```python
from unittest.mock import Mock, patch

def test_com_mock(self):
    """Test usando mock de repositório."""
    with patch('modulo.get_repository') as mock_repo:
        mock_instance = Mock()
        mock_instance.get.return_value = {"resultado": "mockado"}
        mock_repo.return_value = mock_instance
        
        resultado = funcao_testada()
        assert resultado is not None
```

### 6. Nomenclatura de Testes

Siga o padrão: `test_<funcionalidade>_<cenário>_<resultado_esperado>`

Exemplos:
- `test_agent_initialization_with_valid_config_succeeds`
- `test_tool_execution_with_invalid_input_returns_error`
- `test_prompt_structure_has_minimum_length`

## 🎯 Boas Práticas

### ✅ FAÇA

- **Isole os testes**: Cada teste deve ser independente
- **Use fixtures**: Reutilize dados com fixtures do conftest.py
- **Mock dependências externas**: APIs, bancos de dados, Vertex AI
- **Teste edge cases**: Inputs vazios, inválidos, extremos
- **Documente testes**: Docstrings claras com Scenario/Expected
- **Mantenha testes rápidos**: < 1 segundo por teste unitário
- **Um conceito por teste**: Não teste múltiplas coisas no mesmo teste

### ❌ NÃO FAÇA

- Não dependa da ordem de execução dos testes
- Não use valores hardcoded (use fixtures)
- Não teste múltiplas funcionalidades em um teste
- Não faça chamadas reais a APIs externas
- Não compartilhe estado entre testes
- Não ignore testes falhando (`@pytest.mark.skip` sem razão válida)

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"

```powershell
# Certifique-se de estar no diretório raiz do projeto
cd "C:\Users\dajr\OneDrive - GFT Technologies SE\Documents\GFT\BU GCP\Agent Reviewer\repo\arquiteto_parecerista_ans"

# Instale as dependências
pip install -r requirements.txt
```

### Erro: "Fixture not found"

Verifique se a fixture está definida no `conftest.py` do diretório correto.

### Erro: Cobertura < 85%

1. Execute com `--cov-report=term-missing` para ver linhas não cobertas
2. Adicione testes para as linhas faltantes
3. Considere se algumas linhas podem ser excluídas da cobertura

### Testes Lentos

```powershell
# Identifique testes lentos
pytest bv_ans/testes/unit_tests/ --durations=10

# Marque testes lentos
@pytest.mark.slow
def test_operacao_lenta():
    pass
```

## 📚 Recursos Adicionais

### Documentação Oficial

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Google ADK Documentation](https://cloud.google.com/agent-development-kit/docs)

### Comandos Úteis

```powershell
# Ver todos os testes sem executar
pytest bv_ans/testes/unit_tests/ --collect-only

# Executar com output detalhado
pytest bv_ans/testes/unit_tests/ -vv

# Parar no primeiro erro
pytest bv_ans/testes/unit_tests/ -x

# Modo quiet (menos output)
pytest bv_ans/testes/unit_tests/ -q

# Executar testes que falharam na última execução
pytest bv_ans/testes/unit_tests/ --lf

# Depurar teste específico com PDB
pytest bv_ans/testes/unit_tests/test_agent_core.py::test_nome -vv --pdb
```

## 🤝 Contribuindo

Ao adicionar novos recursos ao agente:

1. **Escreva os testes primeiro** (TDD - Test Driven Development)
2. **Garanta cobertura mínima de 85%** para o novo código
3. **Execute toda a suíte** antes de fazer commit
4. **Documente casos especiais** nos testes
5. **Atualize este README** se necessário

## 📞 Suporte

Para dúvidas sobre os testes:

1. Consulte este README
2. Veja exemplos nos arquivos de teste existentes
3. Consulte a documentação do pytest
4. Entre em contato com a equipe de QA

---

**Versão**: 1.0  
**Última Atualização**: Dezembro 2025  
**Autor**: Equipe de Engenharia de Qualidade - Arquiteto Parecerista ANS

