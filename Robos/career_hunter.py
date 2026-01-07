#!/usr/bin/env python3
"""
NÍVEL 2: Agente de Monitoramento de Mercado
FUNÇÃO: Rastreia e filtra oportunidades de carreira em portais especializados.
CONCEITOS: Web Crawling, BeautifulSoup4, Automação de Busca, Persistência de Dados.
"""

import sys
import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

# --- BOOTSTRAP: CONEXÃO COM O SETTINGS ---
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from Config.settings import DIRS
    ARQUIVO_SAIDA = DIRS["DATA"] / "vagas_encontradas.json"
except ImportError:
    ARQUIVO_SAIDA = BASE_DIR / "Data" / "vagas_encontradas.json"
    ARQUIVO_SAIDA.parent.mkdir(parents=True, exist_ok=True)

def buscar_vagas():
    url = "https://www.python.org/jobs/"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    print(f"--> Monitorando: {url}")
    
    try:
        resposta = requests.get(url, headers=headers, timeout=15)
        resposta.raise_for_status()
        
        soup = BeautifulSoup(resposta.text, 'html.parser')
        vagas_html = soup.find_all('h2', class_='listing-company')
        
        achados = []
        termos_filtro = ["brazil", "remote", "latam", "south america"]
        
        print("\n--- ANALISANDO OPORTUNIDADES ---\n")
        
        for item in vagas_html:
            texto_vaga = item.get_text(strip=True)
            texto_lower = texto_vaga.lower()
            
            # Inteligência de Filtragem
            if any(termo in texto_lower for termo in termos_filtro):
                link = "https://www.python.org" + item.find('a')['href'] if item.find('a') else "N/A"
                
                print(f"[ALVO ENCONTRADO] {texto_vaga}")
                
                achados.append({
                    "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "vaga": texto_vaga,
                    "link": link
                })
        
        return achados

    except Exception as e:
        print(f"❌ Erro ao acessar o portal: {e}")
        return []

def salvar_resultados(vagas):
    if not vagas:
        print("💤 Nenhuma vaga no perfil encontrada hoje.")
        return

    # Carregar dados existentes para não sobrescrever, mas sim acumular (Opcional)
    dados_totais = []
    if ARQUIVO_SAIDA.exists():
        try:
            with open(ARQUIVO_SAIDA, 'r', encoding='utf-8') as f:
                dados_totais = json.load(f)
        except:
            dados_totais = []

    dados_totais.extend(vagas)

    with open(ARQUIVO_SAIDA, 'w', encoding='utf-8') as f:
        json.dump(dados_totais, f, indent=4, ensure_ascii=False)
        
    print(f"\n✅ Missão cumprida. {len(vagas)} alvos salvos em: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    lista_vagas = buscar_vagas()
    salvar_resultados(lista_vagas)