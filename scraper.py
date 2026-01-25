import requests
from bs4 import BeautifulSoup
import logging

def buscar_titulo(url_alvo):
    """
    Tenta acessar um site e retornar o título da página.
    Simula um navegador real para evitar bloqueio básico (403 Forbidden).
    """
    # Cabeçalhos: Mentimos para o servidor que somos um Chrome no Windows.
    # Sem isso, 90% dos sites bloqueiam o script imediatamente.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        logging.info(f"Conectando ao alvo: {url_alvo}...")
        
        # O REQUEST (O aperto de mão)
        resposta = requests.get(url_alvo, headers=headers, timeout=5)
        
        # Verificação de Status (200 = OK, 404 = Não achou, 403 = Bloqueado)
        if resposta.status_code == 200:
            # O PARSE (A Cirurgia)
            soup = BeautifulSoup(resposta.content, 'html.parser')
            titulo = soup.title.string.strip() if soup.title else "Sem Título"
            return f"Sucesso! Título capturado: '{titulo}'"
        else:
            return f"Falha. O servidor respondeu com código: {resposta.status_code}"

    except Exception as e:
        return f"Erro de conexão: {e}"
        