"""
NÍVEL 1: Gestor de Ambiente e Caminhos (Versão Agentes V2)
FUNÇÃO: Centraliza a inteligência de diretórios e separação por tipo de dado.
CONCEITOS: Abstração de Caminhos, Configuração Centralizada, Higiene de Dados.
"""

import os
from pathlib import Path

# Caminho Base do Projeto (Raiz da ToolBox)
BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Definição dos Novos Domínios de Agentes e Infraestrutura
DIRS = {
    # Domínios de Agentes (Lógica/Scripts)
    "AGENTES_DADOS": BASE_DIR / "Agentes_Dados",
    "AGENTES_MONITOR": BASE_DIR / "Agentes_Monitor",
    "AGENTES_VISAO": BASE_DIR / "Agentes_Visao",
    "AGENTES_VOZ": BASE_DIR / "Agentes_Voz",
    
    # Infraestrutura
    "CONFIG": BASE_DIR / "Config",
    "SCRIPTS": BASE_DIR / "Scripts",
    "LOGS": BASE_DIR / "Logs",
    "ASSETS": BASE_DIR / "Assets",
    
    # Repositório Central de Dados (Persistência Estruturada)
    "DATA": BASE_DIR / "Data",
    "JSON": BASE_DIR / "Data" / "json",
    "CSV": BASE_DIR / "Data" / "csv",
    
    # Pipelines de I/O de Mídia (Binários)
    "IN_IMAGES": BASE_DIR / "Data" / "input_images",
    "OUT_IMAGES": BASE_DIR / "Data" / "output_images",
    "IN_VOICE": BASE_DIR / "Data" / "input_audio",
    "OUT_VOICE": BASE_DIR / "Data" / "output_audio"
}

# 2. Automação de Infraestrutura: Garante que TODAS as pastas existam
for folder_path in DIRS.values():
    folder_path.mkdir(parents=True, exist_ok=True)

# 3. Configurações de Logs Globais
LOGGING_CONF = {
    "format": '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    "datefmt": '%Y-%m-%d %H:%M:%S',
    "arquivo_log": DIRS["LOGS"] / "system_toolbox.log"
}

# 4. Configurações de Câmbio (Agora apontando para a subpasta CSV)
CAMBIO_CONFIG = {
    "url_api": "https://economia.awesomeapi.com.br/last/USD-BRL",
    "arquivo_saida": DIRS["CSV"] / "cotacao_dolar.csv"
}