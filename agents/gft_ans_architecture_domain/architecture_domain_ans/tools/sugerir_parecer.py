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

"""Suggest opinion based on inputs and rules."""

import logging
from typing import List

logger = logging.getLogger(__name__)


def sugerir_parecer(dados_requisicao: dict) -> dict:
    """
    Suggest opinion based on request data and business rules.

    Analyzes multiple criteria to suggest one of three opinion types:
    - Parecer Favorável
    - Parecer Favorável com Ressalvas
    - Parecer Desfavorável

    Args:
        dados_requisicao: Complete request data including:
            - tipo_requisicao: "Renovação" or "Nova Contratação"
            - integracoes_disponiveis: List of available integrations
            - fluxo_dados: Data flow direction
            - direcionador: Service direcionador from CMDB
            - parecer_anterior: Previous opinion if exists
            - historico: Historical data

    Returns:
        Dictionary with suggested opinion and justification

    Example:
        >>> result = sugerir_parecer({...})
        >>> print(result['parecer_sugerido'])
        'Parecer Favorável'
    """
    logger.info("Suggesting opinion based on business rules")

    tipo_requisicao = dados_requisicao.get("tipo_requisicao")
    integracoes = dados_requisicao.get("integracoes_disponiveis", [])
    fluxo_dados = dados_requisicao.get("fluxo_dados")
    direcionador = dados_requisicao.get("direcionador")
    parecer_anterior = dados_requisicao.get("parecer_anterior", {})
    armazena_dados_bv = dados_requisicao.get("armazena_dados_bv", False)

    # Initialize scoring
    score = 0.5  # Start neutral
    criterios_aplicados = []
    ressalvas = []
    insumos_utilizados = []

    # RULE 1: Renovação with positive previous opinion
    if tipo_requisicao == "Renovação":
        insumos_utilizados.append("Tipo de requisição: Renovação")

        if parecer_anterior:
            # Handle parecer_anterior as dict or string
            if isinstance(parecer_anterior, dict):
                insumos_utilizados.append(f"Parecer anterior: {parecer_anterior.get('tipo_parecer')}")
                tipo_anterior = parecer_anterior.get("tipo_parecer")
            else:
                # parecer_anterior is a string (tipo_parecer value directly)
                insumos_utilizados.append(f"Parecer anterior: {parecer_anterior}")
                tipo_anterior = parecer_anterior

            if tipo_anterior == "Parecer Favorável":
                score += 0.3
                criterios_aplicados.append("Parecer anterior foi favorável")
            elif tipo_anterior == "Parecer Favorável com Ressalvas":
                score += 0.15
                criterios_aplicados.append("Parecer anterior foi favorável com ressalvas")
                # Include previous observations if parecer_anterior is dict
                if isinstance(parecer_anterior, dict):
                    ressalvas_anteriores = parecer_anterior.get("ressalvas", [])
                    if ressalvas_anteriores:
                        ressalvas.extend(ressalvas_anteriores)
            else:  # Desfavorável
                score -= 0.2
                criterios_aplicados.append("Parecer anterior foi desfavorável")
        else:
            criterios_aplicados.append("Renovação sem histórico de parecer anterior")

    # RULE 2: Available integrations
    if integracoes:
        insumos_utilizados.append(f"Integrações disponíveis: {', '.join(integracoes)}")

        if len(integracoes) >= 3:
            score += 0.2
            criterios_aplicados.append("Múltiplas integrações disponíveis (≥3)")
        elif len(integracoes) >= 1:
            score += 0.1
            criterios_aplicados.append("Integrações disponíveis")

        # Check for modern integrations
        modern_techs = ["REST", "WEBHOOK", "MENSAGERIA"]
        if any(tech.upper() in [i.upper() for i in integracoes] for tech in modern_techs):
            score += 0.1
            criterios_aplicados.append("Suporte a tecnologias modernas")

    # RULE 3: Data flow support
    if fluxo_dados:
        insumos_utilizados.append(f"Fluxo de dados: {fluxo_dados}")

        if fluxo_dados == "BIDIRECIONAL":
            score += 0.15
            criterios_aplicados.append("Suporta fluxo bidirecional")
        elif fluxo_dados in ["INBOUND", "OUTBOUND"]:
            score += 0.1
            criterios_aplicados.append(f"Suporta fluxo {fluxo_dados.lower()}")

    # RULE 4: Direcionador from CMDB
    if direcionador:
        insumos_utilizados.append(f"Direcionador CMDB: {direcionador}")

        if direcionador == "Evoluir":
            score += 0.15
            criterios_aplicados.append("Serviço marcado para evolução no CMDB")
        elif direcionador == "Manter":
            score += 0.05
            criterios_aplicados.append("Serviço em manutenção no CMDB")
        elif direcionador == "Desinvestir":
            score -= 0.2
            criterios_aplicados.append("Serviço marcado para desinvestimento no CMDB")
            ressalvas.append(
                "Serviço está marcado como 'Desinvestir' no CMDB. "
                "Avaliar necessidade de contratação/renovação considerando descontinuação futura."
            )

    # RULE 5: BV data storage
    if armazena_dados_bv:
        insumos_utilizados.append("Armazena dados do BV: Sim")
        score -= 0.1
        criterios_aplicados.append("Armazena dados do BV (requer atenção adicional)")
        ressalvas.append(
            "Fornecedor armazena dados do Banco BV em sua infraestrutura. "
            "Verificar conformidade com políticas de segurança e LGPD."
        )

    # DECISION LOGIC
    if score >= 0.8:
        tipo_parecer = "Parecer Favorável"
        justificativa = (
            f"Requisição atende todos os critérios estabelecidos. "
            f"Score de conformidade: {score:.2f}. "
            f"Recomendado prosseguir com a {tipo_requisicao.lower()}."
        )
    elif score >= 0.5:
        tipo_parecer = "Parecer Favorável com Ressalvas"
        justificativa = (
            f"Requisição atende os critérios principais com observações. "
            f"Score de conformidade: {score:.2f}. "
            f"Recomendado prosseguir com ressalvas documentadas."
        )
        if not ressalvas:
            ressalvas.append("Monitorar evolução do serviço conforme roadmap tecnológico")
    else:
        tipo_parecer = "Parecer Desfavorável"
        justificativa = (
            f"Requisição não atende critérios mínimos estabelecidos. "
            f"Score de conformidade: {score:.2f}. "
            f"Recomendado revisar adequação do fornecedor/serviço."
        )
        if not ressalvas:
            ressalvas.append("Requisição requer análise adicional antes de aprovação")

    return {
        "parecer_sugerido": tipo_parecer,
        "justificativa": justificativa,
        "ressalvas": ressalvas,
        "criterios_aplicados": criterios_aplicados,
        "insumos_utilizados": insumos_utilizados,
        "score_confianca": round(score, 2),
        "tipo_requisicao": tipo_requisicao,
    }

