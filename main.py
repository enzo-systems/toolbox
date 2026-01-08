#!/usr/bin/env python3 
"""
ORQUESTRADOR: main.py
FUNÇÃO: Ponto de entrada da ToolBox. Gerencia documentação e integridade do sistema.
STATUS: Operacional - Arquitetura por Domínios
"""

import os
import re
import subprocess
from pathlib import Path

# --- 1. MANIFESTO DO PROJETO (VISÃO POR AGENTES) ---
MANIFESTO = """# 🛠️ ToolBox - Ecossistema de Agentes Autônomos

### 📂 Visão Geral e Arquitetura
Este repositório foi reestruturado para operar através de **Agentes Especializados**. Cada diretório representa um domínio de competência técnica, integrando automação modular sob uma arquitetura de níveis.

* **Agentes de Dados:** Inteligência de busca, scraping e coleta de dados.
* **Agentes de Monitor:** Integridade de redes, latência e diagnóstico de sistemas.
* **Agentes de Visao:** Processamento de imagem, higienização e privacidade.
* **Agentes de Voz:** Síntese vocal e inteligência auditiva.
* **Infraestrutura:** Gestão de logs, configurações centralizadas e automação bash.

---
"""

# --- 2. NOVAS DEFINIÇÕES POR DOMÍNIO ---
DEFINICOES = {
    "Agentes_Dados": "Coleta e processamento de notícias e oportunidades (Scraping/RSS).",
    "Agentes_Monitor": "Monitoramento de integridade web e diagnóstico de hardware/OS.",
    "Agentes_Visao": "Processamento de imagens, filtros e remoção de metadados.",
    "Agentes_Voz": "Conversão de texto em fala (TTS) e inteligência auditiva.",
    "Scripts": "Utilitários de manutenção, backup e automação de infraestrutura.",
    "Config": "Cérebro do projeto (Settings, caminhos absolutos e variáveis).",
    "Data": "Repositório central de entrada (input) e saída (output) de dados.",
    "Logs": "Registro de atividades e rastreabilidade de processos.",
    "Assets": "Recursos estáticos e arquivos fixos do sistema."
}

MAPA_MODULOS = {
    "Agentes_Dados": "### 🛰️ /Agentes_Dados",
    "Agentes_Monitor": "### 🖥️ /Agentes_Monitor",
    "Agentes_Visao": "### 👁️ /Agentes_Visao",
    "Agentes_Voz": "### 🎙️ /Agentes_Voz",
    "Scripts": "### 📜 /Scripts",
    "Config": "### ⚙️ /Config",
    "Data": "### 📊 /Data",
    "Logs": "### 📝 /Logs",
    "Assets": "### 📦 /Assets"
}

STACK_TECNOLOGICO = """
---
### 🛠️ Stack Tecnológico
- **Linguagem:** Python 3.x / Bash
- **OS:** Linux (Fedora / Debian / Ubuntu)
- **Libs Principais:** `requests`, `BeautifulSoup4`, `Pillow (PIL)`, `gTTS`, `logging`.
- **Arquitetura:** Centralização de Caminhos via `Pathlib`, Persistência em JSON/CSV e Pipeline I/O.
"""

# --- 3. LÓGICA DE EXTRAÇÃO E AUDITORIA ---

def extrair_docstring(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            if filepath.endswith('.py'):
                match = re.search(r'"""(.*?)"""', conteudo, re.DOTALL)
                if match: return f" | *{match.group(1).strip().replace('\n', ' ')}*"
            elif filepath.endswith('.sh'):
                for l in conteudo.split('\n'):
                    if l.startswith('#') and '!' not in l and len(l.strip()) > 5:
                        return f" | *{l.replace('#', '').strip()}*"
    except: pass
    return ""

def get_git_info(filepath):
    try:
        cmd = ['git', 'log', '-1', '--format=%s (%cd)', '--date=short', filepath]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip() if result.stdout.strip() else "Aguardando commit"
    except: return "Novo"

def gerar_lista_arquivos(pasta, link_relativo=True):
    if not os.path.exists(pasta): return []
    extensoes = ('.py', '.sh', '.json', '.yml')
    arquivos = sorted([f for f in os.listdir(pasta) if f.endswith(extensoes) and f != 'README.md'])
    
    linhas = []
    for arq in arquivos:
        caminho = os.path.join(pasta, arq)
        git_info = get_git_info(caminho)
        desc = extrair_docstring(caminho)
        prefixo = f"./{pasta}/" if not link_relativo else "./"
        linhas.append(f"- **[{arq}]({prefixo}{arq})**: {git_info}{desc}")
    return linhas if linhas else ["- *Pasta estruturada.*"]

# --- 4. EXECUÇÃO DO ORQUESTRADOR ---

def main():
    print(f"🚀 Iniciando Orquestrador ToolBox em: {os.getcwd()}")
    
    conteudo_raiz = MANIFESTO

    for pasta, header in MAPA_MODULOS.items():
        if os.path.exists(pasta):
            conteudo_raiz += f"\n{header}\n> {DEFINICOES[pasta]}\n\n"
            conteudo_raiz += "\n".join(gerar_lista_arquivos(pasta, False)) + "\n"

    conteudo_raiz += STACK_TECNOLOGICO

    # Salva o README principal na raiz
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(conteudo_raiz)
    
    # Atualiza Sub-Readmes para navegação interna
    for pasta in DEFINICOES.keys():
        if os.path.exists(pasta):
            with open(os.path.join(pasta, "README.md"), 'w', encoding='utf-8') as f:
                f.write(f"# 📁 /{pasta}\n\n> {DEFINICOES[pasta]}\n\n## 📜 Arquivos\n")
                f.write("\n".join(gerar_lista_arquivos(pasta, True)))

    print("✅ Auditoria Concluída! README.md e sub-diretórios sincronizados com a Nova Arquitetura.")

if __name__ == "__main__":
    main()