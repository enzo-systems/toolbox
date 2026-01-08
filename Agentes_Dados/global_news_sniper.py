#!/usr/bin/env python3
"""
NÍVEL 2: Agente de Inteligência de Dados (Global Sniper)
FUNÇÃO: Coleta e processa notícias internacionais via RSS (Feedparser).
CONCEITOS: RSS Parsing, Normalização de Dados, Persistência JSON.
"""

import sys
import json
import time
import feedparser  # pip install feedparser
from pathlib import Path
from urllib.parse import quote 

# --- BOOTSTRAP: CONEXÃO COM O SETTINGS ---
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from Config.settings import DIRS
    # CORREÇÃO SÊNIOR: Salvamos na pasta específica de JSON
    ARQUIVO_MEMORIA = DIRS["JSON"] / "global_news_memory.json"
except ImportError:
    # Fallback seguro
    ARQUIVO_MEMORIA = BASE_DIR / "Data" / "json" / "global_news_memory.json"

# Garante que o diretório pai exista (caso rode isolado fora do main)
ARQUIVO_MEMORIA.parent.mkdir(parents=True, exist_ok=True)

# --- CONFIGURAÇÃO ---
TERMOS_ALVO = ["Inteligência Artificial", "Linux", "Python", "Cibersegurança"]

def carregar_memoria():
    if ARQUIVO_MEMORIA.exists():
        try:
            with open(ARQUIVO_MEMORIA, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Memória corrompida ou vazia ({e}). Iniciando nova.")
            return []
    return []

def salvar_memoria(lista_vistos):
    try:
        with open(ARQUIVO_MEMORIA, 'w', encoding='utf-8') as f:
            # Mantendo os últimos 500 para controle de duplicatas
            json.dump(lista_vistos[-500:], f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Erro ao salvar memória: {e}")

def buscar_google_news():
    print(f"🌍 [Global Sniper] Iniciando Varredura via Feedparser...")
    
    memoria = carregar_memoria()
    novas_descobertas = []

    for termo in TERMOS_ALVO:
        termo_safe = quote(termo)
        print(f"   📡 Sintonizando: [{termo}]...")
        
        # Google News RSS (Brasil)
        url = f"https://news.google.com/rss/search?q={termo_safe}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        
        try:
            feed = feedparser.parse(url)
            
            if feed.bozo: # feedparser flag para XML malformado
                 print(f"      ⚠️ Aviso: XML instável para {termo}")

            contador_termo = 0
            for entry in feed.entries:
                if contador_termo >= 3: 
                    break 
                
                titulo = entry.title
                link = entry.link
                
                if link not in memoria:
                    print(f"      🔥 ALVO: {titulo[:60]}...")
                    memoria.append(link)
                    novas_descobertas.append({
                        "titulo": titulo, 
                        "link": link, 
                        "data": entry.get('published', 'N/A')
                    })
                    contador_termo += 1
        except Exception as e:
            print(f"      ❌ Erro ao ler feed: {e}")
        
        time.sleep(1) # Rate Limiting

    if novas_descobertas:
        salvar_memoria(memoria)
        print(f"✅ Missão cumprida. {len(novas_descobertas)} novos registros em {ARQUIVO_MEMORIA.name}.")
    else:
        print("💤 Sem novidades no radar global.")

if __name__ == "__main__":
    buscar_google_news()