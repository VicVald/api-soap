"""
Módulo de Integração com a API REST do ViaCEP.

Fornece funções utilitárias para sanitização, validação de formato
e realização de requisições HTTP à API pública do ViaCEP.
"""

import re
from typing import Any, Dict, List, Optional
import httpx

# URL Base para comunicação com os endpoints da API ViaCEP
VIACEP_BASE_URL: str = "https://viacep.com.br/ws"


def limpar_cep(cep: str) -> str:
    """
    Remove caracteres não numéricos de uma string de CEP.

    Args:
        cep (str): String do CEP com ou sem formatação (ex: '01001-000' ou '01.001-000').

    Returns:
        str: String contendo apenas os dígitos numéricos (ex: '01001000').

    Examples:
        >>> limpar_cep("01001-000")
        '01001000'
    """
    if not cep:
        return ""
    # Substitui qualquer caractere que NÃO seja um dígito (0-9) por vazio
    return re.sub(r"\D", "", cep)


def validar_formato_cep(cep: str) -> bool:
    """
    Verifica se a string informada possui o formato válido de CEP (exatamente 8 dígitos numéricos).

    Args:
        cep (str): String a ser validada.

    Returns:
        bool: True se possuir exatamente 8 dígitos numéricos, False caso contrário.
    """
    cep_limpo = limpar_cep(cep)
    return len(cep_limpo) == 8 and cep_limpo.isdigit()


def formatar_cep(cep: str) -> str:
    """
    Aplica a máscara padrão de CEP (00000-000) a uma string de 8 dígitos numéricos.

    Args:
        cep (str): String de CEP (com ou sem máscara).

    Returns:
        str: CEP formatado no padrão '00000-000' ou o valor original se for inválido.
    """
    cep_limpo = limpar_cep(cep)
    if len(cep_limpo) == 8:
        return f"{cep_limpo[:5]}-{cep_limpo[5:]}"
    return cep


def consultar_viacep(cep: str) -> Optional[Dict[str, Any]]:
    """
    Realiza uma requisição HTTP à API do ViaCEP para obter os dados de um CEP específico.

    Args:
        cep (str): Código de Endereçamento Postal a ser pesquisado.

    Returns:
        Optional[Dict[str, Any]]: Dicionário contendo os dados do endereço se encontrado,
                                  ou None caso ocorra erro ou o CEP seja inexistente.
    """
    cep_limpo = limpar_cep(cep)
    
    # Valida antecipadamente a quantidade de dígitos para evitar requisições desnecessárias
    if not validar_formato_cep(cep_limpo):
        return None

    url = f"{VIACEP_BASE_URL}/{cep_limpo}/json/"
    try:
        # Define um timeout máximo de 10 segundos para a requisição externa
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            if response.status_code == 200:
                data = response.json()
                # A API do ViaCEP retorna {"erro": "true"} quando o CEP não é localizado
                if data.get("erro") is True or data.get("erro") == "true":
                    return None
                return data
    except Exception as e:
        # Registra a exceção no console caso haja falha de conexão ou rede
        print(f"[-] Erro de conexão ao consultar ViaCEP: {e}")
        
    return None


def buscar_viacep_por_logradouro(uf: str, cidade: str, logradouro: str) -> List[Dict[str, Any]]:
    """
    Pesquisa no ViaCEP a lista de endereços que correspondem aos critérios de Estado, Cidade e Logradouro.

    Args:
        uf (str): Sigla da Unidade Federativa com 2 caracteres (ex: 'SP').
        cidade (str): Nome da cidade (ex: 'São Paulo').
        logradouro (str): Nome ou trecho da rua (mínimo de 3 caracteres).

    Returns:
        List[Dict[str, Any]]: Lista de dicionários com os endereços localizados.
    """
    if not uf or not cidade or not logradouro:
        return []

    # Sanitização e remoção de espaços em branco nas bordas
    uf_clean = uf.strip().upper()
    cidade_clean = cidade.strip()
    logradouro_clean = logradouro.strip()

    # Validação dos parâmetros mínimos exigidos pelo ViaCEP
    if len(uf_clean) != 2 or len(logradouro_clean) < 3:
        return []

    url = f"{VIACEP_BASE_URL}/{uf_clean}/{cidade_clean}/{logradouro_clean}/json/"
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return data
    except Exception as e:
        print(f"[-] Erro de conexão ao buscar logradouro no ViaCEP: {e}")

    return []
