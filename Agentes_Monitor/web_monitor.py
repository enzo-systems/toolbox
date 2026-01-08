#!/usr/bin/env python3
"""
NÍVEL 2: Agente de Integridade de Redes
FUNÇÃO: Monitora disponibilidade e latência de serviços web críticos.
CONCEITOS: Socket Programming, HTTP Status Monitoring, Tempo de Resposta.
"""

import sys
import requests
import json
import time
from pathlib import Path
from datetime import datetime

# --- BOOTSTRAP: CONEXÃO COM O SETTINGS ---
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from Config.settings import DIRS, LOGGING_CONF
    # Definimos onde salvar os resultados da inspeção
    ARQUIVO_DATA = DIRS["DATA"] / "web_monitor_results.json"
    ARQUIVO_LOG = DIRS["LOGS"] / "web_monitor.log"
except ImportError:
    ARQUIVO_DATA = BASE_DIR / "Data" / "web_monitor_results.json"
    ARQUIVO_LOG = BASE_DIR / "Logs" / "web_monitor.log"
    ARQUIVO_DATA.parent.mkdir(parents=True, exist_ok=True)
    ARQUIVO_LOG.parent.mkdir(parents=True, exist_ok=True)

def explorar_site(url):
    # O Disfarce (User-Agent) atualizado
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    inicio = time.time()
    resultado = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": url,
        "status": None,
        "latencia_ms": 0,
        "bytes": 0,
        "sucesso": False
    }

    try:
        print(f"🛰️  Tentando acessar: {url}")
        
        # Requisição com Timeout (Regra sênior para evitar scripts zumbis)
        response = requests.get(url, headers=headers, timeout=10)
        resultado["latencia_ms"] = round((time.time() - inicio) * 1000, 2)
        resultado["status"] = response.status_code
        resultado["bytes"] = len(response.text)

        if response.status_code == 200:
            print(f"✅ Conexão estabelecida! ({resultado['latencia_ms']}ms)")
            resultado["sucesso"] = True
        else:
            print(f"⚠️ Servidor retornou código: {response.status_code}")

    except Exception as e:
        erro_msg = f"❌ Erro na missão: {e}"
        print(erro_msg)
        # Log de erro sênior
        with open(ARQUIVO_LOG, 'a', encoding='utf-8') as f:
            f.write(f"{resultado['timestamp']} - {url} - {erro_msg}\n")
    
    return resultado

def salvar_inspecao(dados):
    """Persistência de dados para análise futura."""
    historico = []
    if ARQUIVO_DATA.exists():
        try:
            with open(ARQUIVO_DATA, 'r', encoding='utf-8') as f:
                historico = json.load(f)
        except:
            historico = []

    historico.append(dados)
    
    # Mantém apenas as últimas 100 inspeções para não inflar o JSON
    with open(ARQUIVO_DATA, 'w', encoding='utf-8') as f:
        json.dump(historico[-100:], f, indent=4, ensure_ascii=False)
    print(f"💾 Resultado arquivado em: {ARQUIVO_DATA}")

if __name__ == "__main__":
    # Alvo vindo da sua versão original
    alvo = "https://pt.wikipedia.org/wiki/Python"
    relatorio = explorar_site(alvo)
    salvar_inspecao(relatorio)