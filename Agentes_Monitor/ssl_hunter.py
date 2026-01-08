#!/usr/bin/env python3 
"""
NÍVEL 2: Auditor de Criptografia e Redes
FUNÇÃO: Varredura e validação de certificados SSL/TLS em domínios externos.
CONCEITOS: pyOpenSSL, Protocolos de Segurança, Persistência de Auditoria.
"""

import sys
import ssl
import socket
import json
from datetime import datetime, timezone
from pathlib import Path

# --- BOOTSTRAP ---
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from Config.settings import DIRS
    ARQUIVO_RELATORIO = DIRS["DATA"] / "auditoria_ssl.json"
except ImportError:
    ARQUIVO_RELATORIO = Path(__file__).resolve().parent.parent / "Data" / "auditoria_ssl.json"

# Alvos de Auditoria
dominios = ["google.com", "python.org", "expired.badssl.com"]

def verificar_ssl(hostname):
    resultado = {"host": hostname, "status": "Erro", "dias_restantes": None, "timestamp": datetime.now().isoformat()}
    print(f"🔍 Analisando segurança: {hostname}")
    
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after = cert['notAfter']
                expiry_date = datetime.strptime(not_after, r'%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
                days_left = (expiry_date - datetime.now(timezone.utc)).days
                
                resultado["dias_restantes"] = days_left
                if days_left < 0:
                    resultado["status"] = "VENCIDO"
                    print(f"❌ {hostname}: Certificado EXPIRADO!")
                else:
                    resultado["status"] = "OK"
                    print(f"✅ {hostname}: Seguro ({days_left} dias)")
                    
    except Exception as e:
        resultado["status"] = f"Falha: {str(e)}"
        print(f"⚠️ {hostname}: Erro de conexão ou SSL.")
    
    return resultado

def salvar_auditoria(dados):
    historico = []
    if ARQUIVO_RELATORIO.exists():
        with open(ARQUIVO_RELATORIO, 'r') as f:
            try: historico = json.load(f)
            except: historico = []
    
    historico.append(dados)
    with open(ARQUIVO_RELATORIO, 'w') as f:
        json.dump(historico[-50:], f, indent=4) # Mantém as últimas 50 análises

if __name__ == "__main__":
    relatorio_final = []
    for site in dominios:
        res = verificar_ssl(site)
        relatorio_final.append(res)
    
    salvar_auditoria(relatorio_final)
    print(f"💾 Auditoria salva em: Data/{ARQUIVO_RELATORIO.name}")