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

"""Data models for Architecture Domain ANS Agent."""

from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator


class TipoRequisicao(str, Enum):
    """Type of request."""

    RENOVACAO = "Renovação"
    NOVA_CONTRATACAO = "Nova Contratação"


class Direcionador(str, Enum):
    """Service direcionador according to CMDB."""

    EVOLUIR = "Evoluir"
    MANTER = "Manter"
    DESINVESTIR = "Desinvestir"


class TipoParecer(str, Enum):
    """Opinion types."""

    FAVORAVEL = "Parecer Favorável"
    FAVORAVEL_COM_RESSALVAS = "Parecer Favorável com Ressalvas"
    DESFAVORAVEL = "Parecer Desfavorável"


class TipoIntegracao(str, Enum):
    """Integration types available."""

    REST = "REST"
    SOAP = "SOAP"
    WEBHOOK = "WebHook"
    MENSAGERIA = "Mensageria"
    FTP = "FTP"
    ARQUIVO = "Arquivo"
    OUTRO = "Outro"


class FluxoDados(str, Enum):
    """Data flow direction."""

    INBOUND = "Inbound"
    OUTBOUND = "Outbound"
    BIDIRECIONAL = "Bidirecional"


class RequisicaoData(BaseModel):
    """Complete request data model."""

    cnpj: str = Field(..., pattern=r"^\d{14}$", description="Supplier CNPJ (14 digits)")
    nome_fornecedor: str = Field(..., description="Supplier name")
    tipo_requisicao: TipoRequisicao = Field(..., description="Type of request")
    api_id: str = Field(..., description="API/Service ID in CMDB")
    descricao_servico: str = Field(..., description="Service description")
    email_solicitante: str = Field(..., description="BV requester email")
    diretoria_solicitante: str = Field(..., description="Requester's directorate")
    integracoes_disponiveis: List[TipoIntegracao] = Field(
        default_factory=list, description="Available integration types"
    )
    fluxo_dados: Optional[FluxoDados] = Field(None, description="Data flow direction")
    armazena_dados_bv: bool = Field(
        default=False, description="Stores BV data in infrastructure"
    )

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        """Validate CNPJ format."""
        v = v.replace(".", "").replace("/", "").replace("-", "")
        if len(v) != 14 or not v.isdigit():
            raise ValueError("CNPJ must have exactly 14 digits")
        return v


class OneTrustContexto(BaseModel):
    """OneTrust API response model for ANS context."""

    cnpj: str
    existe_cadastro: bool
    data_vencimento_contrato: Optional[datetime] = None
    tipo_contrato: Optional[str] = None
    nome_fornecedor: Optional[str] = None
    dados_contexto: dict = Field(default_factory=dict)
    data_ultimo_update: Optional[str] = None


class CMDBData(BaseModel):
    """CMDB API response model."""

    api_id: str
    existe_cadastro: bool
    sigla: Optional[str] = None
    direcionador: Optional[Direcionador] = None
    descricao_servico: Optional[str] = None
    tecnologia: Optional[str] = None
    versao: Optional[str] = None
    responsavel: Optional[str] = None


class ParecerAnterior(BaseModel):
    """Previous opinion model."""

    parecer_id: str
    data_parecer: str
    tipo_parecer: TipoParecer
    justificativa: str
    ressalvas: List[str] = Field(default_factory=list)
    analista: str
    cnpj_fornecedor: str
    tipo_servico: str


class InsumoHistorico(BaseModel):
    """Historical input model."""

    pareceres_similares: List[ParecerAnterior] = Field(default_factory=list)
    total_encontrados: int = 0
    padroes_identificados: List[str] = Field(default_factory=list)
    sugestoes_texto: List[str] = Field(default_factory=list)


class ParecerSugerido(BaseModel):
    """Suggested opinion model."""

    tipo: TipoParecer
    justificativa: str
    ressalvas: List[str] = Field(default_factory=list)
    criterios_aplicados: List[str] = Field(default_factory=list)
    score_confianca: float = Field(ge=0.0, le=1.0)
    insumos_utilizados: List[str] = Field(default_factory=list)


class ParecerCompleto(BaseModel):
    """Complete opinion result model."""

    parecer_id: str
    cnpj: str
    nome_fornecedor: str
    api_id: str
    sigla_servico: Optional[str] = None
    direcionador: Optional[str] = None
    tipo_requisicao: TipoRequisicao
    parecer_sugerido: TipoParecer
    justificativa: str
    ressalvas: List[str] = Field(default_factory=list)
    data_parecer: str
    analista: str = "Agente IA - Parecerista ANS"
    alertas: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class VencimentoValidacao(BaseModel):
    """Contract expiration validation model."""

    data_vencimento: Optional[datetime] = None
    dias_ate_vencimento: Optional[int] = None
    dentro_prazo_2anos: bool = False
    alerta: Optional[str] = None
    status: str  # "OK", "ALERTA", "BLOQUEIO"

