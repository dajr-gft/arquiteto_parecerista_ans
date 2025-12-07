# Introdução
Esta página descreve o uso da tecnologia **genaigke**, já disponível no Portal Tech. 

Com a nossa tecnologia e nossa biblioteca python, você conseguirá levantar uma API que pode usar bibliotecas e endpoints de IA generativa do Vertex (Gemini), usando nossa biblioteca que facilita a implementação da camada de api.

Usando decoradores de nosso framework tanto em arquivos comuns python quanto ipython notebooks, apenas decorando uma função você já consegue definir uma rota POST para sua API.

Contatos:
  https://confluence.bvnet.bv/spaces/TD/pages/280627634/1.1+Quem+somos


## Estrutura básica do projeto
- **contract.yml**: arquivo de contrato, onde o cliente informa algumas coisas para a pipeline como:
  - serviceAccountName
  - dnsBase
  - configmap com project id e location do vertex
- **src**: pasta raiz da aplicação
- **src/routes/**: pasta com arquivos python e ipython notebooks decorados com nosso framework (genai_framework)
- **jenkins.properties**: arquivo de propriedades do jenkins contendo nossa tecnologia
- **requirements.txt**: arquivo de requisitos do python do projeto
- **requirements-dev.txt**: arquivo de requisitos do python do projeto usados em tempo de desenvolvimento, como bibliotecas de testes.
- **version.properties**: arquivo autogerido pela pipeline para versionar a aplicação.
- **Makefile**: makefile usado pela pipeline principalmente nas etapas de teste e cobertura
- **sonar-project.properties**: arquivo de configuração de cobertura de testes do Sonar


## Configuração inicial
Pré requisitos:
- Python 3.11.3 

Dentro da pasta do projeto (ou onde achar melhor) crie uma pasta de environment do python:

```sh
python -m venv venv
```

Criado o ambiente virtual, executar `venv/Scripts/activate` para ativar o ambiente. Ativado o 
ambiente, executar a instalação dos pacotes do requirements.txt usando o seguinte comando (não esqueça de voltar para a raiz do projeto `cd..`)

```sh
pip install -r requirements.txt requirements-dev.txt -i https://nexus.bvnet.bv/repository/pypi-public/simple/ --trusted-host nexus.bvnet.bv
```

pip install -r requirements.txt -i https://nexus.bvnet.bv/repository/pypi-public/simple/ --trusted-host nexus.bvnet.bv

Criado o ambiente, você pode começar o desenvolvimento das suas rotas na pasta **src/routes/**, com arquivos python ou ipython notebooks.

## Usando o framework
O processo de desenvolvimento usando nosso framework consiste em poucas mudanças no processo original de utilização de notebooks. Dentro de seus notebooks, apenas requisitamos que você importe a nossa biblioteca ([pylib-sgen-base-genai-framework](https://nexus.bvnet.bv/#browse/browse:pypi-public:pylib-sgen-base-genai-framework)) `from genai_framework.decorators import post_route` e decore alguma função sua no notebook com ela, passando como parâmetro para ela o nome do rota a ser gerada na api final.

```python
import json
from genai_framework.decorators import post_route

@post_route('nome_da_rota')
def alguma_funcao_que_vai_virar_rota(qualquer_parametro, qualquer_outro_parametro):
    # seu código de IA generativa aqui dentro!
    return json.dumps({'output': 'Olá mundo'}, ensure_ascii=False)
```

Na saída desse projeto teríamos uma rota POST:

`/nome_da_rota`:

Payload de envio json:
```json
{
    "qualquer_parametro": "algum_valor",
    "qualquer_outro_parametro": "algum_outro_valor"
}
```

Resposta
```
'{"output": "Olá mundo"}'
```

### Definição e uso de status code HTTP customizados
Por padrão, o framework retorna apenas os códigos HTTP 200 (sucesso) e 500 (erro genérico).
No entanto, em cenários mais complexos, pode ser necessário retornar outros códigos HTTP para representar melhor o tipo de resposta ou erro ocorrido.

Para isso, em vez de retornar apenas o conteúdo JSON, a função deve retornar uma tupla no seguinte formato:
```text
conteudo: Any, status_code: int
```

Exemplo:
```python
import json
from genai_framework.decorators import post_route

@post_route('custom_http')
def alguma_funcao_custom_http(qualquer_parametro, version):
    try:
        # Validação de versão (simulando uma regra de negócio)
        if version < 0.5:
            raise ValueError("versão inválida, atualize e tente novamente")
        # Retorno de sucesso
        return json.dumps({'output': 'Olá mundo'}, ensure_ascii=False), 200
    except ValueError as ve:
        # Erro específico de validação
        return {"error": str(ve)}, 400
    except Exception as e:
        # Erro genérico
        return {"error": str(e)}, 500
```
Na saída desse projeto teríamos uma rota POST:
`/custom_http`:

Payload de envio json:
```json
{
    "qualquer_parametro": "algum_valor",
    "version": 0.2
}
```

Resposta
```
response = '{"error": "versão invalida, atualize e tente novamente"}'
status_code = 400
```

⚠️ Caso a função não retorne uma tupla, o endpoint continuará funcionando normalmente, utilizando o comportamento padrão (200 ou 500).
Isso significa que é possível mesclar abordagens sem quebrar o código.

### Upload de arquivos com file_input_route

Além do @post_route, também é possível expor rotas que recebem upload de arquivos usando o decorador @file_input_route.
Esse decorador transforma automaticamente uma função Python que recebe um FileInput em um endpoint de upload.

```python
from genai_framework.decorators import file_input_route
from genai_framework.models import FileInput

@file_input_route("upload_exemplo")
def upload_exemplo(file: FileInput):
    if not file.filename.lower().endswith(".txt"):
        return {"error": "Apenas arquivos .txt são aceitos nesse exemplo"}
    texto = file.content.decode("utf-8")
    return {"filename": file.filename, "conteudo": texto[:200]}  # retorna uma preview
```

#### Estrutura do model FileInput

O FileInput é um DTO que representa o arquivo de entrada:

```python
class FileInput:
    content: bytes        # conteúdo bruto do arquivo
    filename: str         # nome original do arquivo
    mimetype: str         # mimetype enviado
    metadata: Optional[Dict[str, Any]] = None  # metadados opcionais
```

## Requisitos do contrato (contract.yml)
Os seguintes campos são obrigatórios:
```yaml
serviceAccountName: exemplo_sa # criado no portal do componente, na aba 'Workload Identity', CONTA DE SERVIÇOS KURBENETES, obrigatório
dnsBase: examplo_de_raiz_de_dns # (api em prd: `examplo_de_raiz_de_dns.dados.bvnet.bv/api`), obrigatório
configmap:
  variables:
    PROJECT_ID: # Utilizado pelo Vertex, obrigatório
      des: bv-sgen-des
      uat: bv-sgen-uat
      prd: bv-sgen-prd
    LOCATION: # Utilizado pelo Vertex, obrigatório
      des: us-central1
      uat: us-central1
      prd: us-central1
```

dnsBase: valor a ser usado para gerar os endereços dns nos devidos ambientes:

- DES: \<dnsBase\>.dadosdes.bvnet.bv
- UAT: \<dnsBase\>.dadosuat.bvnet.bv
- PRD: \<dnsBase\>.dados.bvnet.bv


Caso utilize o ADK, campos extras são necessários

```yaml GOOGLE_GENAI_USE_VERTEXAI:
    GOOGLE_GENAI_USE_VERTEXAI:
      des: "TRUE"
      uat: "TRUE"
      prd: "TRUE"
    GOOGLE_CLOUD_PROJECT:
      des: bv-sgen-des
      uat: bv-sgen-uat
      prd: bv-sgen-prd
    GOOGLE_CLOUD_LOCATION:
      des: us-central1
      uat: us-central1
      prd: us-central1
```