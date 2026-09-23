"""
Módulo de Rotas REST da API (OpenAPI / Swagger 3.0).

Fornece endpoints RESTful complementares ao serviço SOAP, documentados
integralmente com especificações OpenAPI/Swagger, tratamento de erros,
validações via Pydantic e segurança via API Key.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
import httpx

from src.core.config import APP_NAME, APP_VERSION
from src.core.security import require_api_key, sanitize_input
from src.services.viacep_client import (
    buscar_viacep_por_logradouro,
    consultar_viacep,
    formatar_cep,
    validar_formato_cep,
)

router = APIRouter(prefix="/api/v1", tags=["Consulta de CEP"])


# ============================================================================
# Modelos Pydantic (Esquemas OpenAPI)
# ============================================================================

class EnderecoSchema(BaseModel):
    """Esquema de dados completo de um endereço."""
    cep: str = Field(..., examples=["01001-000"], description="Código de Endereçamento Postal formatado")
    logradouro: str = Field(..., examples=["Praça da Sé"], description="Nome do logradouro / rua / avenida")
    complemento: Optional[str] = Field("", examples=["lado ímpar"], description="Complemento do endereço")
    bairro: str = Field(..., examples=["Sé"], description="Bairro")
    localidade: str = Field(..., examples=["São Paulo"], description="Cidade / Município")
    uf: str = Field(..., examples=["SP"], description="Unidade Federativa")
    ibge: Optional[str] = Field("", examples=["3550308"], description="Código IBGE do município")
    gia: Optional[str] = Field("", examples=["1004"], description="Código GIA")
    ddd: Optional[str] = Field("", examples=["11"], description="Código DDD")
    siafi: Optional[str] = Field("", examples=["7107"], description="Código SIAFI")
    sucesso: bool = Field(True, examples=[True], description="Indicador de sucesso da consulta")
    mensagem: str = Field("CEP localizado com sucesso.", examples=["CEP localizado com sucesso."])


class ValidacaoSchema(BaseModel):
    """Esquema de resultado de validação de CEP."""
    cep: str = Field(..., examples=["01001000"], description="CEP analisado")
    valido: bool = Field(..., examples=[True], description="Indica se o formato é válido")
    cep_formatado: str = Field("", examples=["01001-000"], description="CEP formatado com máscara se válido")
    mensagem: str = Field(..., examples=["Formato válido de 8 dígitos numéricos."])


class StatusServicoSchema(BaseModel):
    """Esquema de verificação de status e integridade."""
    servico: str = Field(..., examples=["API Servidor SOAP & REST de CEP"])
    versao: str = Field(..., examples=["2.0.0"])
    status: str = Field("OPERACIONAL", examples=["OPERACIONAL"])
    protocolos: List[str] = Field(["SOAP 1.1", "REST HTTP/JSON"], examples=[["SOAP 1.1", "REST HTTP/JSON"]])
    seguranca: Dict[str, Any] = Field(
        {
            "autenticacao": "API Key / Bearer Token",
            "rate_limiting": "Ativo (60 req/min)",
            "security_headers": "Ativo (HSTS, CSP, X-Frame-Options, nosniff)",
            "sanitizacao_xxe": "Ativo",
        }
    )


class SoapRawRequest(BaseModel):
    """Requisição para o executor de SOAP XML Raw."""
    xml_envelope: str = Field(
        ...,
        examples=[
            (
                '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">\n'
                '   <soapenv:Header/>\n'
                '   <soapenv:Body>\n'
                '      <spy:consultar_cep>\n'
                '         <spy:cep>01001000</spy:cep>\n'
                '      </spy:consultar_cep>\n'
                '   </soapenv:Body>\n'
                '</soapenv:Envelope>'
            )
        ],
        description="Envelope XML completo SOAP 1.1",
    )
    soap_action: Optional[str] = Field("consultar_cep", examples=["consultar_cep"], description="Cabeçalho SOAPAction")


class SoapRawResponse(BaseModel):
    """Resposta da execução do envelope SOAP."""
    status_code: int = Field(200, examples=[200])
    response_xml: str = Field(..., description="XML retornado pelo servidor SOAP Spyne")
    content_type: str = Field("text/xml; charset=utf-8", examples=["text/xml; charset=utf-8"])


class SecurityStatusSchema(BaseModel):
    """Esquema para demonstração de autenticação bem-sucedida."""
    autenticado: bool = Field(True, examples=[True])
    mensagem: str = Field(..., examples=["Autenticação realizada com sucesso!"])
    token_utilizado: str = Field(..., examples=["soap-secret-key-2026"])
    ip_origem: str = Field(..., examples=["127.0.0.1"])


# ============================================================================
# Endpoints RESTful
# ============================================================================

@router.get(
    "/status",
    response_model=StatusServicoSchema,
    summary="Status Operacional e Recursos de Segurança",
    description="Retorna o status de saúde da aplicação, protocolos ativos e recursos de segurança habilitados.",
)
def obter_status():
    return StatusServicoSchema(
        servico=APP_NAME,
        versao=APP_VERSION,
        status="OPERACIONAL",
        protocolos=["SOAP 1.1 (WSDL em /soap?wsdl)", "REST (OpenAPI/Swagger em /docs)"],
        seguranca={
            "autenticacao": "API Key / Bearer Token ('X-API-Key' / 'Authorization')",
            "rate_limiting": "Ativo (60 req/min por IP)",
            "security_headers": "Ativo (nosniff, DENY, XSS-Protection, Referrer-Policy)",
            "sanitizacao_xxe": "Ativo (LXML + sanitização de entrada)",
        },
    )


@router.get(
    "/cep/{cep}",
    response_model=EnderecoSchema,
    summary="Consultar Endereço por CEP",
    description=(
        "Pesquisa informações completas de um endereço a partir de seu CEP (8 dígitos). "
        "Requer envio de API Key válida para autenticação."
    ),
    responses={
        200: {"description": "Endereço encontrado com sucesso."},
        400: {"description": "CEP com formato inválido."},
        401: {"description": "Não autorizado - API Key ausente ou inválida."},
        404: {"description": "CEP não localizado na base de dados."},
    },
)
def consultar_endereco_por_cep(
    cep: str,
    api_key: str = Depends(require_api_key),
):
    cep_sanitizado = sanitize_input(cep)
    if not validar_formato_cep(cep_sanitizado):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O CEP informado '{cep}' é inválido. Ele deve conter exatamente 8 dígitos numéricos.",
        )

    dados = consultar_viacep(cep_sanitizado)
    if not dados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"O CEP '{cep}' não foi encontrado na base de dados.",
        )

    return EnderecoSchema(
        cep=dados.get("cep", ""),
        logradouro=dados.get("logradouro", ""),
        complemento=dados.get("complemento", ""),
        bairro=dados.get("bairro", ""),
        localidade=dados.get("localidade", ""),
        uf=dados.get("uf", ""),
        ibge=dados.get("ibge", ""),
        gia=dados.get("gia", ""),
        ddd=dados.get("ddd", ""),
        siafi=dados.get("siafi", ""),
        sucesso=True,
        mensagem="CEP localizado com sucesso.",
    )


@router.get(
    "/cep/validar/{cep}",
    response_model=ValidacaoSchema,
    summary="Validar Formato de CEP",
    description="Valida se uma sequência de caracteres corresponde a um CEP válido de 8 dígitos.",
)
def validar_cep_endpoint(cep: str):
    cep_sanitizado = sanitize_input(cep)
    valido = validar_formato_cep(cep_sanitizado)
    cep_formatado = formatar_cep(cep_sanitizado) if valido else ""
    mensagem = (
        "Formato válido de 8 dígitos numéricos."
        if valido
        else "Formato inválido. O CEP deve conter exatamente 8 dígitos numéricos."
    )
    return ValidacaoSchema(
        cep=cep_sanitizado,
        valido=valido,
        cep_formatado=cep_formatado,
        mensagem=mensagem,
    )


@router.get(
    "/cep/buscar/enderecos",
    response_model=List[EnderecoSchema],
    summary="Buscar Endereços por Logradouro",
    description="Pesquisa lista de endereços filtrando por UF (Estado), Cidade e Trecho do Logradouro (Rua/Avenida).",
    responses={
        200: {"description": "Lista de endereços encontrados."},
        400: {"description": "Parâmetros obrigatórios ausentes ou inválidos."},
    },
)
def buscar_por_logradouro_endpoint(
    uf: str = Query(..., min_length=2, max_length=2, description="Sigla do Estado com 2 letras (ex: 'SP', 'RS')"),
    cidade: str = Query(..., min_length=3, description="Nome do município (ex: 'São Paulo', 'Porto Alegre')"),
    logradouro: str = Query(..., min_length=3, description="Trecho do logradouro (ex: 'Domingos', 'Paulista')"),
    api_key: str = Depends(require_api_key),
):
    uf_clean = sanitize_input(uf).upper()
    cidade_clean = sanitize_input(cidade)
    logradouro_clean = sanitize_input(logradouro)

    resultados = buscar_viacep_por_logradouro(uf_clean, cidade_clean, logradouro_clean)
    retorno = []
    for item in resultados:
        retorno.append(
            EnderecoSchema(
                cep=item.get("cep", ""),
                logradouro=item.get("logradouro", ""),
                complemento=item.get("complemento", ""),
                bairro=item.get("bairro", ""),
                localidade=item.get("localidade", ""),
                uf=item.get("uf", ""),
                ibge=item.get("ibge", ""),
                gia=item.get("gia", ""),
                ddd=item.get("ddd", ""),
                siafi=item.get("siafi", ""),
                sucesso=True,
                mensagem="Endereço localizado com sucesso.",
            )
        )
    return retorno


@router.get(
    "/security/verify",
    response_model=SecurityStatusSchema,
    summary="Verificar Autenticação e Segurança",
    description="Endpoint de teste para evidência de segurança. Retorna 200 OK se autenticado com sucesso.",
    responses={
        200: {"description": "Autenticado com sucesso."},
        401: {"description": "Não autorizado - Chave ausente ou inválida."},
    },
)
def verificar_seguranca_auth(
    request: Request,
    api_key: str = Depends(require_api_key),
):
    client_ip = request.client.host if request.client else "127.0.0.1"
    return SecurityStatusSchema(
        autenticado=True,
        mensagem="Autenticação com API Key validada com sucesso! Acesso concedido aos recursos protegidos.",
        token_utilizado=api_key,
        ip_origem=client_ip,
    )


def processar_soap_raw_envio(body: SoapRawRequest, client: Optional[httpx.Client] = None) -> SoapRawResponse:
    """Função utilitária para envio do envelope SOAP para o serviço Spyne."""
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": body.soap_action or "consultar_cep",
    }
    try:
        if client is not None:
            response = client.post("http://127.0.0.1:8000/soap", content=body.xml_envelope, headers=headers)
            return SoapRawResponse(
                status_code=response.status_code,
                response_xml=response.text,
                content_type=response.headers.get("content-type", "text/xml"),
            )

        with httpx.Client(timeout=10.0) as default_client:
            response = default_client.post("http://127.0.0.1:8000/soap", content=body.xml_envelope, headers=headers)
            return SoapRawResponse(
                status_code=response.status_code,
                response_xml=response.text,
                content_type=response.headers.get("content-type", "text/xml"),
            )
    except Exception as e:
        return SoapRawResponse(
            status_code=500,
            response_xml=f"<error>Falha ao processar requisição SOAP: {str(e)}</error>",
            content_type="text/xml",
        )


@router.post(
    "/soap/raw",
    response_model=SoapRawResponse,
    summary="Testador / Ponte SOAP Raw XML",
    description="Permite o envio direto de um envelope XML SOAP 1.1 para o serviço Spyne e retorna o XML de resposta.",
)
def executar_soap_raw(body: SoapRawRequest):
    return processar_soap_raw_envio(body)

