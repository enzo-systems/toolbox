#!/usr/bin/env python3 
"""
ORQUESTRADOR: main.py
FUNÇÃO: Ponto de entrada da ToolBox. Gerencia documentação e integridade do sistema.
STATUS: Operacional - Auditoria Profunda & Stack Sênior
"""

import os
import re
import subprocess
from pathlib import Path

# --- 1. MANIFESTO DO PROJETO ---
MANIFESTO = """# 🛠️ ToolBox - Ecossistema de Agentes Autônomos

### 📂 Visão Geral e Arquitetura
Este repositório opera através de **Agentes Especializados** e uma infraestrutura de dados organizada por tipos e domínios.

* **Agentes de Dados:** Inteligência de busca, scraping e coleta de dados.
* **Agentes de Monitor:** Integridade de redes, latência e diagnóstico de sistemas.
* **Agentes de Visao:** Processamento de imagem, higienização e privacidade.
* **Agentes de Voz:** Síntese vocal e inteligência auditiva.
* **Infraestrutura:** Gestão de logs, configurações e persistência de dados.

---
"""

# --- 2. STACK TECNOLÓGICO DETALHADO ---
STACK_TECNOLOGICO = """
---
### 🛠️ Stack Tecnológico e Engenharia
- **Core Executivo:** Python 3.x & Bash Scripting (Automação de Infraestrutura).
- **Domínios de Inteligência:**
    - `Requests` & `BeautifulSoup4`: Engenharia de extração e consumo de APIs REST.
    - `Pillow (PIL)`: Pipeline de processamento de imagem e manipulação de metadados.
    - `gTTS`: Síntese de voz e processamento de fluxos de áudio.
- **Resiliência e Monitoramento:**
    - `Socket`: Diagnósticos de conectividade em baixo nível (TCP/UDP).
    - `Logging (RotatingFileHandler)`: Gestão de logs cíclicos com controle de volumetria.
    - `Subprocess`: Orquestração de comandos do sistema operacional (Fedora/Linux).
- **Arquitetura de Dados:**
    - **Persistência Estruturada:** Armazenamento em CSV (Séries temporais) e JSON (Status/Auditoria).
    - **Estratégia de I/O:** Separação rigorosa entre `input_` (Matéria-prima) e `output_` (Processados).
    - **Portabilidade:** Gestão de caminhos absolutos via `Pathlib` para integridade entre ambientes.
"""

# --- 3. DEFINIÇÕES POR DOMÍNIO ---
DEFINICOES = {
    "Agentes_Dados": "Coleta e processamento de notícias e oportunidades (Scraping/RSS).",
    "Agentes_Monitor": "Monitoramento de integridade web e diagnóstico de hardware/OS.",
    "Agentes_Visao": "Processamento de imagens, filtros e remoção de metadados.",
    "Agentes_Voz": "Conversão de texto em fala (TTS) e inteligência auditiva.",
    "Scripts": "Utilitários de manutenção, backup e automação de infraestrutura.",
    "Config": "Cérebro do projeto (Settings, caminhos absolutos e variáveis).",
    "Data": "Repositório central organizado por subpastas (csv, json, images, audio).",
    "Logs": "Registro de atividades, histórico de erros e auditoria.",
    "Assets": "Recursos estáticos, modelos e arquivos fixos do sistema."
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

# --- 4. LÓGICA DE EXTRAÇÃO E AUDITORIA ---

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
        return result.stdout.strip() if result.stdout.strip() else "Novo"
    except: return "Novo"

def gerar_lista_arquivos(pasta, link_relativo=True):
    if not os.path.exists(pasta): return []
    
    # Extensões permitidas (Ampliadas para incluir dados e logs)
    ext_codigo = ('.py', '.sh')
    ext_dados = ('.json', '.csv', '.log', '.jpg', '.png', '.mp3', '.webp')
    extensoes = ext_codigo + ext_dados
    
    arquivos_encontrados = []
    
    # Busca recursiva para capturar subpastas (importante para Data/)
    for root, dirs, files in os.walk(pasta):
        for f in files:
            if f.endswith(extensoes) and f != 'README.md':
                caminho_completo = os.path.join(root, f)
                arquivos_encontrados.append(caminho_completo)

    arquivos_encontrados.sort()
    
    linhas = []
    for caminho in arquivos_encontrados:
        # Nome exibido será relativo à pasta (ex: json/status.json)
        nome_exibicao = os.path.relpath(caminho, pasta)
        git_info = get_git_info(caminho)
        desc = extrair_docstring(caminho) if caminho.endswith(ext_codigo) else ""
        
        prefixo = f"./{pasta}/" if not link_relativo else "./"
        link = f"{prefixo}{nome_exibicao}"
        
        linhas.append(f"- **[{nome_exibicao}]({link})**: {git_info}{desc}")
        
    return linhas if linhas else ["- *Aguardando geração de dados ou scripts.*"]

# --- 5. EXECUÇÃO DO ORQUESTRADOR ---

def main():
    print(f"🚀 Iniciando Auditoria Deep Scan em: {os.getcwd()}")
    
    conteudo_raiz = MANIFESTO

    for pasta, header in MAPA_MODULOS.items():
        if os.path.exists(pasta):
            print(f"📁 Mapeando: {pasta}...")
            conteudo_raiz += f"\n{header}\n> {DEFINICOES[pasta]}\n\n"
            conteudo_raiz += "\n".join(gerar_lista_arquivos(pasta, False)) + "\n"

    # Adiciona o Stack Tecnológico Detalhado ao final
    conteudo_raiz += STACK_TECNOLOGICO

    # Salva o README principal
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(conteudo_raiz)
    
    # Atualiza Sub-Readmes para navegação interna
    for pasta in DEFINICOES.keys():
        if os.path.exists(pasta):
            with open(os.path.join(pasta, "README.md"), 'w', encoding='utf-8') as f:
                f.write(f"# 📁 /{pasta}\n\n> {DEFINICOES[pasta]}\n\n## 📜 Conteúdo Detectado\n")
                f.write("\n".join(gerar_lista_arquivos(pasta, True)))

    print("✅ Sucesso! README.md agora reflete a Engenharia e Arquitetura completa.")

if __name__ == "__main__":
    main()