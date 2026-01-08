#!/usr/bin/env python3
"""
NÍVEL 2: Watchdog (Supervisor de Resiliência)
FUNÇÃO: Valida o heartbeat do Sentinela e dispara alertas visuais no Fedora.
CONCEITOS: Auditoria de Heartbeat, Notificação de Sistema (GNOME), Resiliência.
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# --- BOOTSTRAP: CONEXÃO COM O SETTINGS ---
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from Config.settings import DIRS
    STATUS_SENTINELA = DIRS["JSON"] / "sentinela_status.json"
    LOG_SISTEMA = DIRS["LOGS"] / "system_toolbox.log"
except ImportError:
    STATUS_SENTINELA = Path("Data/json/sentinela_status.json")
    LOG_SISTEMA = Path("Logs/system_toolbox.log")

def enviar_notificacao_fedora(mensagem):
    """Sua ideia original: Alerta visual no GNOME/Fedora."""
    try:
        subprocess.run(['notify-send', '-u', 'critical', '🚨 ToolBox Watchdog', mensagem])
    except: pass

def auditar_sistema():
    print("🐕 [Watchdog] Checando batimentos do Sentinela...")
    
    if not STATUS_SENTINELA.exists():
        msg = "Sentinela NUNCA foi iniciado!"
        registrar_e_notificar(msg)
        return

    try:
        with open(STATUS_SENTINELA, 'r', encoding='utf-8') as f:
            status = json.load(f)
        
        ultimo_check = datetime.strptime(status["ultimo_check"], "%Y-%m-%d %H:%M:%S")
        atraso = (datetime.now() - ultimo_check).total_seconds()

        # Se o Sentinela não der sinal de vida por mais de 3 minutos
        if atraso > 180:
            msg = f"Sentinela travado! Último sinal há {int(atraso)}s."
            registrar_e_notificar(msg)
        else:
            print(f"✅ Sistema Saudável. (Atraso: {int(atraso)}s)")

    except Exception as e:
        registrar_e_notificar(f"Erro na auditoria: {e}")

def registrar_e_notificar(msg):
    print(f"⚠️ {msg}")
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Escreve no Log Central
    with open(LOG_SISTEMA, 'a', encoding='utf-8') as f:
        f.write(f"{agora} - [WATCHDOG] - {msg}\n")
    # Envia o Popup no seu Fedora
    enviar_notificacao_fedora(msg)

if __name__ == "__main__":
    auditar_sistema()