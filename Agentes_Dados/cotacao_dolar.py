#!/usr/bin/env python3
"""
NÍVEL 2: Agente Financeiro Autônomo
FUNÇÃO: Captura cotações em tempo real via API e gera séries históricas.
CONCEITOS: Integração de APIs REST, Configuração Centralizada, Persistência CSV.
"""

import sys
import requests
import csv
from datetime import datetime
from pathlib import Path

# --- BOOTSTRAP: CONEXÃO COM O SETTINGS ---
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from Config.settings import CAMBIO_CONFIG, DIRS
except ImportError:
    print("❌ Erro: Não foi possível localizar Config/settings.py")
    sys.exit(1)

def buscar_cotacao():
    try:
        response = requests.get(CAMBIO_CONFIG["url_api"], timeout=10)
        response.raise_for_status()
        data = response.json()
        par = list(data.keys())[0]
        return data[par]['bid']
    except Exception as e:
        print(f"⚠️ Falha na coleta: {e}")
        return None

def salvar_dados(valor):
    if not valor: return
    
    # Garantimos que o arquivo seja salvo dentro de Data/
    arquivo = DIRS["DATA"] / "cotacao_dolar.csv"
    header = ['Data_Hora', 'Valor_BRL']
    existe = arquivo.exists()
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(arquivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(header)
        writer.writerow([agora, valor])
    
    print(f"✅ Registro arquivado em: Data/{arquivo.name} | Valor: R$ {valor}")

if __name__ == "__main__":
    cotacao = buscar_cotacao()
    salvar_dados(cotacao)