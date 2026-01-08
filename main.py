#!/usr/bin/env python3 
"""
ORQUESTRADOR: main.py
FUNÇÃO: Gerador de Documentação Viva (Living Documentation).
DESCRIÇÃO: Varre a estrutura do projeto e atualiza todos os README.md automaticamente.
STATUS: Operacional - Modo Bibliotecário (Com suporte a pastas de Output)
"""

import os
import re
import subprocess
from pathlib import Path

# --- CONFIGURAÇÕES DE IGNORAR ---
# Apenas lixo de sistema e controle de versão. Pastas de output agora SÃO PERMITIDAS.
DIRS_IGNORADOS = {'.venv', '__pycache__', '.git', '.idea', '.vscode'}

# --- 1. MANIFESTO DO PROJETO ---
MANIFESTO = """# 🛠️ ToolBox - Ecossistema de Agentes Autônomos

### 📂 Visão Geral
Este repositório é uma **Caixa de Ferramentas Modular**. Cada pasta contém agentes especializados que funcionam de forma independente.
Use este README como um **Índice Dinâmico** para encontrar a ferramenta certa para sua tarefa.

---
"""

# --- 2. STACK TECNOLÓGICO ---
STACK_TECNOLOGICO = """
---
### 🛠️ Engenharia e Stack
- **Linguagem:** Python 3.10+
- **Documentação:** Gerada automaticamente via `main.py`.
- **Estrutura:**
    - `Agentes_*`: Módulos funcionais independentes.
    - `Data`: Armazenamento de inputs (matéria-prima) e outputs (resultados).
"""

# --- 3. DEFINIÇÕES ---
DEFINICOES = {
    "Agentes_Dados": "Coleta de dados, Scraping e Processamento de RSS.",
    "Agentes_Visao": "Computer Vision: Análise, filtros e manipulação de imagens.",
    "Agentes_Voz": "Síntese de Voz (TTS) e Clonagem de Áudio (XTTS).",
    "Agentes_Monitor": "Monitoramento de sistema, rede e hardware.",
    "Scripts": "Automação de infraestrutura e manutenção do OS.",
    "Data": "Repositório de Arquivos (Inputs e Outputs).",
    "Logs": "Histórico de execução e auditoria."
}

MAPA_MODULOS = {
    "Agentes_Dados": "### 🛰️ /Agentes_Dados",
    "Agentes_Visao": "### 👁️ /Agentes_Visao",
    "Agentes_Voz": "### 🎙️ /Agentes_Voz",
    "Agentes_Monitor": "### 🖥️ /Agentes_Monitor",
    "Scripts": "### 📜 /Scripts",
    "Data": "### 📊 /Data",
    "Logs": "### 📝 /Logs"
}

# --- 4. FUNÇÕES DE EXTRAÇÃO ---

def extrair_docstring(filepath):
    """Lê o cabeçalho do arquivo para explicar o que ele faz."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            if filepath.endswith('.py'):
                match = re.search(r'"""(.*?)"""', conteudo, re.DOTALL)
                if match: return f" | *{match.group(1).strip().replace(chr(10), ' ')}*"
            elif filepath.endswith('.sh'):
                comentarios = []
                for l in conteudo.split('\n'):
                    if l.startswith('#') and '!' not in l:
                        comentarios.append(l.replace('#', '').strip())
                if comentarios: return f" | *{' '.join(comentarios[:1])}*"
    except: pass
    return ""

def get_git_info(filepath):
    """Pega a data da última modificação real no Git."""
    try:
        cmd = ['git', 'log', '-1', '--format=%cd', '--date=short', filepath]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return f"({result.stdout.strip()})" if result.stdout.strip() else "(Novo/Local)"
    except: return "(Local)"

def gerar_lista_arquivos(pasta_raiz, link_relativo=True):
    linhas = []
    
    # Varredura
    for root, dirs, files in os.walk(pasta_raiz):
        # Filtra pastas ignoradas
        dirs[:] = [d for d in dirs if d not in DIRS_IGNORADOS]
        
        for f in files:
            # Regra de Ouro: Ignora ocultos, EXCETO .gitkeep
            if f.startswith('.') and f != '.gitkeep': continue 
            if f == 'README.md': continue
            
            caminho_completo = os.path.join(root, f)
            nome_exibicao = os.path.relpath(caminho_completo, pasta_raiz)
            
            # Definição de Ícones e Descrições
            icone = "📄"
            info_git = get_git_info(caminho_completo)
            desc = extrair_docstring(caminho_completo)
            
            if f == '.gitkeep':
                icone = "📂"
                # Remove o nome .gitkeep da exibição para ficar mais limpo, mostra a pasta
                pasta_pai = os.path.dirname(nome_exibicao)
                nome_exibicao = f"{pasta_pai}/ (Estrutura)"
                desc = " | *Diretório de Saída (Conteúdo gerado ignorado pelo Git)*"
            elif f.endswith('.py'): icone = "🐍"
            elif f.endswith('.sh'): icone = "🐚"
            elif f.endswith(('.wav', '.mp3')): icone = "🔊"
            elif f.endswith(('.jpg', '.png')): icone = "🖼️"
            elif f.endswith('.json'): icone = "⚙️"
            
            # Cria o link Markdown
            prefixo = f"./{pasta_raiz}/" if not link_relativo else "./"
            # Se for gitkeep, o link aponta para a pasta onde ele está
            link = f"{prefixo}{os.path.dirname(os.path.relpath(caminho_completo, pasta_raiz))}" if f == '.gitkeep' else f"{prefixo}{nome_exibicao}"
            
            # Formatação da linha
            if f == '.gitkeep':
                 linhas.append(f"- {icone} **[{nome_exibicao}]({link})** {desc}")
            else:
                 linhas.append(f"- {icone} **[{nome_exibicao}]({link})** {info_git}{desc}")

    return sorted(linhas) if linhas else ["- *Pasta vazia.*"]

# --- 5. EXECUÇÃO ---

def main():
    print(f"📚 Iniciando Bibliotecário ToolBox em: {os.getcwd()}")
    
    # 1. Gera o README.md Principal (Raiz)
    conteudo_raiz = MANIFESTO
    
    for pasta, header in MAPA_MODULOS.items():
        if os.path.exists(pasta):
            print(f"   - Indexando: {pasta}...")
            conteudo_raiz += f"\n{header}\n> {DEFINICOES.get(pasta, '')}\n\n"
            conteudo_raiz += "\n".join(gerar_lista_arquivos(pasta, link_relativo=False)) + "\n"
            
    conteudo_raiz += STACK_TECNOLOGICO
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(conteudo_raiz)
    
    # 2. Gera os READMEs Internos (Dentro de cada pasta)
    for pasta in DEFINICOES.keys():
        if os.path.exists(pasta):
            with open(os.path.join(pasta, "README.md"), 'w', encoding='utf-8') as f:
                f.write(f"# 📁 Módulo: {pasta}\n\n> {DEFINICOES[pasta]}\n\n## 🧰 Estrutura e Ferramentas\n")
                f.write("\n".join(gerar_lista_arquivos(pasta, link_relativo=True)))

    print("✅ Documentação Viva atualizada (Outputs incluídos)!")

if __name__ == "__main__":
    main()