"""
Módulo de definição do Serviço SOAP de CEP (Spyne Service).

Este módulo define a estrutura da API SOAP 1.1 para consulta, validação
e busca de CEPs utilizando a biblioteca Spyne sob o protocolo WSDL.
Executa de forma 100% nativa em Python 3.11+.
"""

from spyne import Application, Array, Boolean, ComplexModel, ServiceBase, Unicode, rpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

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
    
    Attributes:
        cep (Unicode): Código de Endereçamento Postal formatado (ex: '01001-000').
        logradouro (Unicode): Nome da rua, avenida ou praça.
        complemento (Unicode): Informações adicionais de complemento do endereço.
        bairro (Unicode): Nome do bairro.
        localidade (Unicode): Nome da cidade/município.
        uf (Unicode): Sigla da Unidade Federativa / Estado (ex: 'SP').
        ibge (Unicode): Código IBGE do município.
        gia (Unicode): Código GIA da cidade.
        ddd (Unicode): Código DDD do telefone da região.
        siafi (Unicode): Código SIAFI do município.
        sucesso (Boolean): Indica se a consulta obteve sucesso.
        mensagem (Unicode): Mensagem explicativa ou de status da operação.
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

    Attributes:
        valido (Boolean): True se o CEP contiver 8 dígitos numéricos válidos.
        mensagem (Unicode): Descrição legível sobre o resultado da validação.
        cep_formatado (Unicode): CEP formatado com máscara (ex: '01001-000') se válido.
    """
    __namespace__ = "api.soap.cep"
    
    valido = Boolean
    mensagem = Unicode
    cep_formatado = Unicode


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
            cep (str): CEP a ser consultado (pode conter pontuação ou apenas números).

        Returns:
            EnderecoResponse: Objeto contendo os dados do endereço localizado ou mensagem de erro.
        """
        # Valida se o CEP foi informado na requisição SOAP
        if not cep or not cep.strip():
            return EnderecoResponse(
                sucesso=False,
                mensagem="O parâmetro CEP é de preenchimento obrigatório."
            )

        # Realiza a requisição ao serviço do ViaCEP
        dados = consultar_viacep(cep)
        
        # Caso o CEP não seja localizado ou seja inválido
        if not dados:
            return EnderecoResponse(
                sucesso=False,
                mensagem=f"O CEP '{cep}' não foi localizado ou possui formato inválido."
            )

        # Retorna a resposta com os dados mapeados para o tipo de retorno SOAP
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
            mensagem="CEP encontrado com sucesso."
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
        if not cep or not cep.strip():
            return ResultadoValidacao(
                valido=False,
                mensagem="O parâmetro CEP não foi informado.",
                cep_formatado=""
            )

        # Executa a checagem de formato numérico de 8 dígitos
        valido = validar_formato_cep(cep)
        
        if valido:
            return ResultadoValidacao(
                valido=True,
                mensagem="CEP possui formato válido.",
                cep_formatado=formatar_cep(cep)
            )
        else:
            return ResultadoValidacao(
                valido=False,
                mensagem="CEP inválido. O CEP deve conter exatamente 8 dígitos numéricos.",
                cep_formatado=""
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

        # Consulta os dados correspondentes no ViaCEP
        resultados_viacep = buscar_viacep_por_logradouro(uf, cidade, logradouro)
        lista_enderecos = []

        # Itera sobre os resultados convertendo cada dict retornado no modelo EnderecoResponse
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
                    mensagem="Endereço localizado."
                )
            )

        return lista_enderecos


# Definição da Aplicação Spyne SOAP 1.1 com gerador WSDL
app_spyne = Application(
    services=[CepService],
    tns="api.soap.cep",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

# Empacotamento WSGI para ser montado em servidores web Python (como FastAPI ou Uvicorn)
wsgi_soap_app = WsgiApplication(app_spyne)
