#!/usr/bin/env python3
"""
NÍVEL 2: Career Hunter
STATUS: Corrigido com Debug de Caminhos Absolutos.
"""

import sys
import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

# --- BOOTSTRAP ---
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from Config.settings import DIRS
    ARQUIVO_SAIDA = DIRS["JSON"] / "vagas_encontradas.json"
except ImportError:
    ARQUIVO_SAIDA = BASE_DIR / "Data" / "json" / "vagas_encontradas.json"

ARQUIVO_SAIDA.parent.mkdir(parents=True, exist_ok=True)

def buscar_vagas():
    url = "https://www.python.org/jobs/"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    print(f"📁 [DEBUG] Banco de Vagas: {ARQUIVO_SAIDA}")
    print(f"👔 [Career Hunter] Monitorando: {url}")
    
    try:
        resposta = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resposta.text, 'html.parser')
        vagas_html = soup.find_all('h2', class_='listing-company')
        
        achados = []
        termos = ["brazil", "remote", "latam", "south america"]
        
        print(f"🔎 Analisando {len(vagas_html)} ofertas...")
        
        for item in vagas_html:
            texto = item.get_text(strip=True)
            if any(t in texto.lower() for t in termos):
                link = "https://www.python.org" + item.find('a')['href'] if item.find('a') else "N/A"
                print(f"   🎯 OPORTUNIDADE: {texto}")
                achados.append({
                    "data": datetime.now().strftime("%Y-%m-%d"),
                    "vaga": texto,
                    "link": link
                })
        return achados

    except Exception as e:
        print(f"❌ Erro: {e}")
        return []

def salvar_resultados(novas):
    if not novas:
        print("💤 Nada encontrado hoje.")
        return

    dados_db = []
    if ARQUIVO_SAIDA.exists():
        with open(ARQUIVO_SAIDA, 'r', encoding='utf-8') as f:
            try: dados_db = json.load(f)
            except: dados_db = []

    links_db = {item['link'] for item in dados_db}
    
    reais = [v for v in novas if v['link'] not in links_db]
    
    if not reais:
        print(f"🔄 Todas as {len(novas)} vagas encontradas já existem em:\n   📄 {ARQUIVO_SAIDA}")
        return

    dados_db.extend(reais)
    with open(ARQUIVO_SAIDA, 'w', encoding='utf-8') as f:
        json.dump(dados_db[-200:], f, indent=4, ensure_ascii=False)
        
    print(f"✅ {len(reais)} novas vagas salvas em:\n   📄 {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    vagas = buscar_vagas()
    salvar_resultados(vagas)