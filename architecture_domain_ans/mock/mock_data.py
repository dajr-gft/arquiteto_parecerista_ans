# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Mock data stores for Architecture Domain ANS Agent."""

from datetime import datetime, timedelta
from typing import Optional, List

from ..models import (
    CMDBData,
    Direcionador,
    InsumoHistorico,
    OneTrustContexto,
    ParecerAnterior,
    TipoParecer,
)

# Mock OneTrust Database (context for ANS)
ONETRUST_DATABASE = {
    "12345678000190": OneTrustContexto(
        cnpj="12345678000190",
        existe_cadastro=True,
        data_vencimento_contrato=datetime.now() + timedelta(days=540),  # ~18 meses
        tipo_contrato="Renovação",
        nome_fornecedor="Tech Solutions LTDA",
        dados_contexto={
            "categoria": "Tecnologia",
            "ultima_renovacao": "2024-01-15",
            "valor_contrato": "R$ 250.000,00"
        },
        data_ultimo_update="2024-10-15",
    ),
    "98765432000101": OneTrustContexto(
        cnpj="98765432000101",
        existe_cadastro=True,
        data_vencimento_contrato=datetime.now() + timedelta(days=650),  # ~21 meses
        tipo_contrato="Renovação",
        nome_fornecedor="Cloud Data Services S.A.",
        dados_contexto={
            "categoria": "Cloud",
            "ultima_renovacao": "2023-06-01",
            "valor_contrato": "R$ 1.200.000,00"
        },
        data_ultimo_update="2024-11-01",
    ),
    "11222333000144": OneTrustContexto(
        cnpj="11222333000144",
        existe_cadastro=True,
        data_vencimento_contrato=None,  # Missing expiration date
        tipo_contrato="Nova Contratação",
        nome_fornecedor="Analytics Platform Inc",
        dados_contexto={
            "categoria": "Analytics",
            "primeira_contratacao": True
        },
        data_ultimo_update="2024-09-20",
    ),
    "55666777000188": OneTrustContexto(
        cnpj="55666777000188",
        existe_cadastro=True,
        data_vencimento_contrato=datetime.now() + timedelta(days=450),  # ~15 meses
        tipo_contrato="Renovação",
        nome_fornecedor="Security Consulting Group",
        dados_contexto={
            "categoria": "Segurança",
            "ultima_renovacao": "2024-03-01",
            "valor_contrato": "R$ 180.000,00"
        },
        data_ultimo_update="2024-11-10",
    ),
    "11223344000155": OneTrustContexto(
        cnpj="11223344000155",
        existe_cadastro=True,
        data_vencimento_contrato=datetime.now() + timedelta(days=900),  # ~30 meses (> 2 anos)
        tipo_contrato="Renovação",
        nome_fornecedor="Cloud Provider Inc",
        dados_contexto={
            "categoria": "Cloud",
            "ultima_renovacao": "2022-12-01",
            "valor_contrato": "R$ 3.500.000,00"
        },
        data_ultimo_update="2024-11-15",
    ),
}

# Mock CMDB Database
CMDB_DATABASE = {
    "API-001": CMDBData(
        api_id="API-001",
        existe_cadastro=True,
        sigla="CRM-API",
        direcionador=Direcionador.EVOLUIR,
        descricao_servico="API de integração com CRM",
        tecnologia="REST",
        versao="2.0",
        responsavel="Arquitetura - Squad CRM",
    ),
    "API-002": CMDBData(
        api_id="API-002",
        existe_cadastro=True,
        sigla="CLOUD-STORAGE",
        direcionador=Direcionador.MANTER,
        descricao_servico="Serviço de armazenamento em nuvem",
        tecnologia="S3-Compatible",
        versao="1.5",
        responsavel="Infraestrutura Cloud",
    ),
    "API-003": CMDBData(
        api_id="API-003",
        existe_cadastro=True,
        sigla="ANALYTICS-ENGINE",
        direcionador=Direcionador.EVOLUIR,
        descricao_servico="Motor de analytics e BI",
        tecnologia="GraphQL",
        versao="3.1",
        responsavel="Arquitetura - Squad Analytics",
    ),
    "API-004": CMDBData(
        api_id="API-004",
        existe_cadastro=True,
        sigla="LEGACY-SYSTEM",
        direcionador=Direcionador.DESINVESTIR,
        descricao_servico="Sistema legado em descontinuação",
        tecnologia="SOAP",
        versao="1.0",
        responsavel="Arquitetura - Legacy",
    ),
    "API-005": CMDBData(
        api_id="API-005",
        existe_cadastro=True,
        sigla="SEC-GATEWAY",
        direcionador=Direcionador.MANTER,
        descricao_servico="Gateway de segurança",
        tecnologia="REST + OAuth2",
        versao="2.5",
        responsavel="Segurança da Informação",
    ),
}

# Mock Historical Opinions Database
HISTORICO_PARECERES = {
    "12345678000190": [
        ParecerAnterior(
            parecer_id="PAR-2024-001",
            data_parecer="2024-01-15",
            tipo_parecer=TipoParecer.FAVORAVEL,
            justificativa="Fornecedor com histórico positivo. Renovação de contrato sem alterações significativas.",
            ressalvas=[],
            analista="João Silva",
            cnpj_fornecedor="12345678000190",
            tipo_servico="API de CRM",
        ),
    ],
    "98765432000101": [
        ParecerAnterior(
            parecer_id="PAR-2024-002",
            data_parecer="2023-06-01",
            tipo_parecer=TipoParecer.FAVORAVEL_COM_RESSALVAS,
            justificativa="Fornecedor adequado para o serviço, porém com ressalvas sobre documentação.",
            ressalvas=[
                "Documentação técnica deve ser atualizada trimestralmente",
                "SLA deve ser revisado após 6 meses de operação",
            ],
            analista="Maria Santos",
            cnpj_fornecedor="98765432000101",
            tipo_servico="Cloud Storage",
        ),
        ParecerAnterior(
            parecer_id="PAR-2023-045",
            data_parecer="2022-12-10",
            tipo_parecer=TipoParecer.FAVORAVEL,
            justificativa="Primeira contratação aprovada com base em análise de mercado.",
            ressalvas=[],
            analista="Carlos Oliveira",
            cnpj_fornecedor="98765432000101",
            tipo_servico="Cloud Infrastructure",
        ),
    ],
    "55666777000188": [
        ParecerAnterior(
            parecer_id="PAR-2024-003",
            data_parecer="2024-03-01",
            tipo_parecer=TipoParecer.FAVORAVEL_COM_RESSALVAS,
            justificativa="Consultoria aprovada com ressalvas sobre escopo de atuação.",
            ressalvas=[
                "Atuação restrita a análise e recomendações, sem acesso direto aos sistemas produtivos",
                "Relatórios devem ser revisados pela equipe de Segurança antes de implementação",
            ],
            analista="Ana Costa",
            cnpj_fornecedor="55666777000188",
            tipo_servico="Consultoria de Segurança",
        ),
    ],
}


def get_onetrust_contexto(cnpj: str) -> Optional[OneTrustContexto]:
    """
    Retrieve supplier context data from OneTrust.

    Args:
        cnpj: Supplier CNPJ (14 digits)

    Returns:
        OneTrustContexto if found, None otherwise
    """
    return ONETRUST_DATABASE.get(cnpj)


def get_cmdb_data(api_id: str) -> Optional[CMDBData]:
    """
    Retrieve service data from CMDB.

    Args:
        api_id: Service/API identifier

    Returns:
        CMDBData if found, None otherwise
    """
    return CMDB_DATABASE.get(api_id)


def get_last_parecer(cnpj: str) -> Optional[ParecerAnterior]:
    """
    Retrieve last opinion for supplier.

    Args:
        cnpj: Supplier CNPJ (14 digits)

    Returns:
        ParecerAnterior if found, None otherwise
    """
    pareceres = HISTORICO_PARECERES.get(cnpj, [])
    return pareceres[0] if pareceres else None


def search_pareceres_similares(cnpj: str, tipo_servico: str, limit: int = 5) -> InsumoHistorico:
    """
    Search for similar historical opinions.

    Args:
        cnpj: Supplier CNPJ (14 digits)
        tipo_servico: Type of service
        limit: Maximum number of results

    Returns:
        InsumoHistorico with similar opinions
    """
    pareceres = HISTORICO_PARECERES.get(cnpj, [])

    # Filter by service type (simple substring match)
    pareceres_filtrados = [
        p for p in pareceres
        if tipo_servico.lower() in p.tipo_servico.lower()
    ][:limit]

    # Extract patterns from historical opinions
    padroes = []
    sugestoes = []

    if pareceres_filtrados:
        # Count opinion types
        tipos_count = {}
        for p in pareceres_filtrados:
            tipos_count[p.tipo_parecer] = tipos_count.get(p.tipo_parecer, 0) + 1

        tipo_mais_comum = max(tipos_count, key=tipos_count.get)
        padroes.append(f"Histórico mostra {tipos_count[tipo_mais_comum]} parecer(es) do tipo: {tipo_mais_comum.value}")

        # Extract common phrases from justifications
        if any(p.tipo_parecer == TipoParecer.FAVORAVEL for p in pareceres_filtrados):
            sugestoes.append("Fornecedor com histórico positivo de entregas")

        if any(p.ressalvas for p in pareceres_filtrados):
            padroes.append("Pareceres anteriores continham ressalvas que devem ser consideradas")

    return InsumoHistorico(
        pareceres_similares=pareceres_filtrados,
        total_encontrados=len(pareceres_filtrados),
        padroes_identificados=padroes,
        sugestoes_texto=sugestoes,
    )


def has_ressalvas_pendentes(cnpj: str) -> bool:
    """
    Check if supplier has pending observations from previous opinions.

    Args:
        cnpj: Supplier CNPJ (14 digits)

    Returns:
        True if pending observations exist
    """
    ultimo_parecer = get_last_parecer(cnpj)
    return bool(ultimo_parecer and ultimo_parecer.ressalvas)

