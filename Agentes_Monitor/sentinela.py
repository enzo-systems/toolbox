#!/usr/bin/env python3
"""
NÍVEL 2: Sentinela de Infraestrutura
FUNÇÃO: Vigia a conectividade e gerencia a rotatividade de logs do sistema.
CONCEITOS: I/O de Sistema, RotatingFileHandler, Daemonize Simulation.
"""

import sys
import time
import socket
import logging
import json
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime

# --- BOOTSTRAP: CONEXÃO COM O SETTINGS ---
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from Config.settings import DIRS
    CAMINHO_LOG = DIRS["LOGS"] / "sentinela.log"
    STATUS_JSON = DIRS["JSON"] / "sentinela_status.json"
except ImportError:
    CAMINHO_LOG = Path("Logs/sentinela.log")
    STATUS_JSON = Path("Data/json/sentinela_status.json")

# --- 1. CONFIGURAÇÃO DE LOG ROTATIVO (PADRÃO SÊNIOR) ---
log_handler = RotatingFileHandler(
    CAMINHO_LOG, 
    maxBytes=2*1024*1024, # Reduzi para 2MB para ser mais ágil
    backupCount=3,
    encoding='utf-8'
)

logging.basicConfig(
    handlers=[log_handler],
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def checar_conexao():
    """Verifica conectividade via Socket TCP na porta 53 (DNS)."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def atualizar_status_visual(online):
    """Atualiza um JSON para que o main.py saiba o estado da rede sem ler logs."""
    status = {
        "ultimo_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rede_online": online,
        "agente": "Sentinela"
    }
    with open(STATUS_JSON, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=4)

if __name__ == "__main__":
    print(f"🛡️  Sentinela iniciado. Log: {CAMINHO_LOG.name}")
    print("🚦 Monitorando rede... (Pressione Ctrl+C para parar)")

    try:
        while True:
            online = checar_conexao()
            
            if online:
                logging.info("STATUS: ONLINE - Conectividade estabelecida.")
            else:
                logging.warning("ALERTA: OFFLINE - Falha de conexão detectada!")
            
            atualizar_status_visual(online)
            
            # O Arquiteto define o intervalo (60 segundos)
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n🛑 Sentinela desativado pelo usuário.")
        logging.info("Sentinela encerrado manualmente.")