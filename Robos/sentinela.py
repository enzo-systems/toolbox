import time
import socket
import logging
from datetime import datetime

# --- CONFIGURAÇÃO DO ARQUITETO ---
# Aqui definimos que o "diário" será salvo num arquivo chamado sentinela.log
# level=logging.INFO significa que queremos registrar informações gerais e erros.
logging.basicConfig(
    filename='sentinela.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def checar_conexao():
    """Tenta conectar ao DNS do Google (8.8.8.8) na porta 53.
    É mais rápido e silencioso que um ping."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

print("🛡️  Sentinela iniciado. Rodando em background...")
print("📝  Verifique o arquivo 'sentinela.log' para o histórico.")

# --- O LOOP INFINITO (DAEMON) ---
while True:
    if checar_conexao():
        # Em vez de print, usamos logging.info
        logging.info("STATUS: ONLINE - A rede está operante.")
    else:
        # Se cair, logamos como WARNING (Aviso)
        logging.warning("ALERTA: OFFLINE - Conexão perdida!")
    
    # O Arquiteto define o ritmo. 
    # Dorme por 60 segundos para não gastar CPU à toa.
    time.sleep(60)
