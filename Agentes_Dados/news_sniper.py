#!/usr/bin/env python3 
"""
NÍVEL 2: Agente de Extração de Dados (News Sniper)
STATUS: Corrigido com Debug de Caminhos Absolutos.
"""

import sys
import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path

# --- BOOTSTRAP ---
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from Config.settings import DIRS
    ARQUIVO_MEMORIA = DIRS["JSON"] / "news_sniper_memory.json"
except ImportError:
    ARQUIVO_MEMORIA = BASE_DIR / "Data" / "json" / "news_sniper_memory.json"

# Garante que a pasta existe
ARQUIVO_MEMORIA.parent.mkdir(parents=True, exist_ok=True)

URL_ALVO = "https://www.tabnews.com.br"
PALAVRAS_CHAVE = ["inteligência artificial", "linux", "python"]

def carregar_memoria():
    if ARQUIVO_MEMORIA.exists():
        try:
            with open(ARQUIVO_MEMORIA, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []
    return []

def salvar_memoria(lista_vistos):
    try:
        with open(ARQUIVO_MEMORIA, 'w', encoding='utf-8') as f:
            json.dump(lista_vistos, f, indent=4)
        return True
    except Exception as e:
        print(f"❌ Erro de permissão ao salvar em {ARQUIVO_MEMORIA}: {e}")
        return False

def caçar_noticias():
    print(f"📁 [DEBUG] Arquivo de Memória: {ARQUIVO_MEMORIA}")
    print(f"🕵️  [News Sniper] Varrendo TabNews...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'}

    try:
        response = requests.get(URL_ALVO, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    
    memoria = carregar_memoria()
    novas_descobertas = []
    
    print(f"🔎 Analisando {len(links)} links...")

    for link in links:
        titulo = link.get_text().strip()
        url_relativa = link.get('href')

        if not titulo or len(titulo) < 5 or not url_relativa: continue
            
        url_final = url_relativa if url_relativa.startswith('http') else f"{URL_ALVO}{url_relativa}"
        titulo_lower = titulo.lower()

        # Verifica Keywords
        encontrou = False
        match = ""
        for palavra in PALAVRAS_CHAVE:
            if palavra in titulo_lower:
                encontrou = True
                match = palavra
                break 
        
        if encontrou:
            if url_final not in memoria:
                print(f"   🎯 NOVO ALVO [{match.upper()}]: {titulo}")
                memoria.append(url_final)
                novas_descobertas.append(titulo)

    if novas_descobertas:
        salvar_memoria(memoria)
        print(f"✅ Sucesso! {len(novas_descobertas)} novos itens salvos em:\n   📄 {ARQUIVO_MEMORIA}")
    else:
        # Força a criação do arquivo mesmo se não achar nada, pra você ver que funciona
        if not ARQUIVO_MEMORIA.exists():
            salvar_memoria(memoria)
            print(f"⚠️ Nenhuma notícia nova, mas criei o arquivo de memória inicial.")
        print(f"💤 Sem novidades. (Verificado contra base em: {ARQUIVO_MEMORIA.name})")

if __name__ == "__main__":
    caçar_noticias()