"""
Módulo de Definição do Serviço SOAP de CEP (Spyne Service).

Define o contrato WSDL, modelos de dados e operações RPC da API SOAP 1.1:
- consultar_cep
- validar_cep
- buscar_por_logradouro
- obter_status_servico

Compatível com Spyne e WSGI/ASGI via a2wsgi no Python 3.11.
"""

from datetime import datetime
from spyne import Application, Array, Boolean, ComplexModel, ServiceBase, Unicode, rpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from src.core.config import APP_NAME, APP_VERSION
from src.core.security import sanitize_input
from src.services.viacep_client import (
    buscar_viacep_por_logradouro,
    consultar_viacep,
    formatar_cep,
    validar_formato_cep,
)


class EnderecoResponse(ComplexModel):
    """
    Modelo de dados retornado nas consultas de CEP.

    Representa um endereço completo no padrão do protocolo SOAP / WSDL.
    """

    __namespace__ = "api.soap.cep"

    cep = Unicode
    logradouro = Unicode
    complemento = Unicode
    bairro = Unicode
    localidade = Unicode
    uf = Unicode
    ibge = Unicode
    gia = Unicode
    ddd = Unicode
    siafi = Unicode
    sucesso = Boolean
    mensagem = Unicode


class ResultadoValidacao(ComplexModel):
    """
    Modelo de dados retornado na validação de formato de CEP.
    """

    __namespace__ = "api.soap.cep"

    valido = Boolean
    mensagem = Unicode
    cep_formatado = Unicode


class StatusServicoResponse(ComplexModel):
    """
    Modelo de status e integridade do serviço SOAP.
    """

    __namespace__ = "api.soap.cep"

    servico = Unicode
    versao = Unicode
    status = Unicode
    provedor = Unicode
    timestamp = Unicode


class CepService(ServiceBase):
    """
    Classe de Serviço SOAP contendo os métodos RPC expostos no contrato WSDL.
    """

    @rpc(Unicode, _returns=EnderecoResponse)
    def consultar_cep(ctx, cep: str) -> EnderecoResponse:
        """
        Consulta os dados detalhados de um CEP na base de dados (ViaCEP).

        Args:
            ctx: Contexto da requisição RPC do Spyne.
            cep (str): CEP a ser consultado (com ou sem máscara).

        Returns:
            EnderecoResponse: Objeto contendo os dados do endereço localizado ou mensagem de erro.
        """
        if not cep or not str(cep).strip():
            return EnderecoResponse(
                sucesso=False,
                mensagem="O parâmetro CEP é de preenchimento obrigatório.",
            )

        cep_sanitizado = sanitize_input(str(cep))
        dados = consultar_viacep(cep_sanitizado)

        if not dados:
            return EnderecoResponse(
                sucesso=False,
                mensagem=f"O CEP '{cep_sanitizado}' não foi localizado ou possui formato inválido.",
            )

        return EnderecoResponse(
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
            mensagem="CEP encontrado com sucesso.",
        )

    @rpc(Unicode, _returns=ResultadoValidacao)
    def validar_cep(ctx, cep: str) -> ResultadoValidacao:
        """
        Valida a estrutura de um CEP (verifica se possui 8 dígitos numéricos).

        Args:
            ctx: Contexto da requisição RPC do Spyne.
            cep (str): CEP a ser validado.

        Returns:
            ResultadoValidacao: Objeto indicando se o formato é válido e sua representação formatada.
        """
        if not cep or not str(cep).strip():
            return ResultadoValidacao(
                valido=False,
                mensagem="O parâmetro CEP não foi informado.",
                cep_formatado="",
            )

        cep_sanitizado = sanitize_input(str(cep))
        valido = validar_formato_cep(cep_sanitizado)

        if valido:
            return ResultadoValidacao(
                valido=True,
                mensagem="CEP possui formato válido de 8 dígitos.",
                cep_formatado=formatar_cep(cep_sanitizado),
            )
        else:
            return ResultadoValidacao(
                valido=False,
                mensagem="CEP inválido. O CEP deve conter exatamente 8 dígitos numéricos.",
                cep_formatado="",
            )

    @rpc(Unicode, Unicode, Unicode, _returns=Array(EnderecoResponse))
    def buscar_por_logradouro(ctx, uf: str, cidade: str, logradouro: str):
        """
        Busca uma lista de CEPs e endereços filtrados por Estado (UF), Cidade e Nome da Rua.

        Args:
            ctx: Contexto da requisição RPC do Spyne.
            uf (str): Sigla do Estado com 2 caracteres (ex: 'SP', 'RS').
            cidade (str): Nome da cidade (ex: 'São Paulo', 'Porto Alegre').
            logradouro (str): Nome ou trecho do nome do logradouro (mínimo de 3 caracteres).

        Returns:
            list[EnderecoResponse]: Lista de endereços encontrados correspondentes aos parâmetros.
        """
        if not uf or not cidade or not logradouro:
            return []

        uf_sanitizado = sanitize_input(str(uf))
        cidade_sanitizada = sanitize_input(str(cidade))
        logradouro_sanitizado = sanitize_input(str(logradouro))

        resultados_viacep = buscar_viacep_por_logradouro(
            uf_sanitizado, cidade_sanitizada, logradouro_sanitizado
        )
        lista_enderecos = []

        for item in resultados_viacep:
            lista_enderecos.append(
                EnderecoResponse(
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

        return lista_enderecos

    @rpc(_returns=StatusServicoResponse)
    def obter_status_servico(ctx) -> StatusServicoResponse:
        """
        Retorna as informações de integridade operacional do serviço SOAP.
        """
        return StatusServicoResponse(
            servico=APP_NAME,
            versao=APP_VERSION,
            status="OPERACIONAL",
            provedor="ViaCEP Integration Engine",
            timestamp=datetime.now().isoformat(),
        )


# Definição da Aplicação Spyne SOAP 1.1 com gerador WSDL
app_spyne = Application(
    services=[CepService],
    tns="api.soap.cep",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

# Empacotamento WSGI para ser montado em servidores ASGI via a2wsgi
wsgi_soap_app = WsgiApplication(app_spyne)
