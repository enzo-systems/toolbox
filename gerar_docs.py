"""
ROBÔ: ARQUITETO DE DOCS
FUNÇÃO: Lê metadados do Git e Docstrings dos scripts para auto-gerar os READMEs.
STATUS: Ativo e integrado com extração de comentários.
"""

import os
import re
import subprocess

# --- Configurações ---
MAPA_MODULOS = {
    "Robos": {"root": r"### 🤖 /Robos", "sub": r"## 📜 Lista de Scripts"},
    "Imagens": {"root": r"### 🖼️ /Imagens", "sub": r"## 📜 Lista de Scripts"},
    "CloneVoz": {"root": r"### 🎙️ /CloneVoz", "sub": r"## 📜 Lista de Scripts"}
}

def extrair_docstring(filepath):
    """Lê a descrição inicial (docstring) de um arquivo .py."""
    if not filepath.endswith('.py'):
        return ""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            # Busca o texto entre as primeiras triplas aspas
            match = re.search(r'"""(.*?)"""', conteudo, re.DOTALL)
            if match:
                # Pega o texto, remove quebras de linha extras e limita o tamanho
                descricao = match.group(1).strip().replace('\n', ' ')
                return f" | *{descricao}*"
    except Exception:
        pass
    return ""

def get_git_info(filepath):
    """Pega a última mensagem de commit e a data de um arquivo."""
    try:
        # Formato: Mensagem (Data)
        cmd = ['git', 'log', '-1', '--format=%s (%cd)', '--date=short', filepath]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        return "Novo arquivo (Aguardando commit)"
    except Exception:
        return "Erro ao ler Git"

def gerar_lista_arquivos(pasta):
    """Gera a lista em Markdown com Status do Git + Descrição do Código."""
    linhas = []
    if os.path.exists(pasta):
        arquivos = sorted([f for f in os.listdir(pasta) if f.endswith('.py') or f.endswith('.json')])
        for arquivo in arquivos:
            caminho_completo = os.path.join(pasta, arquivo)
            
            git_info = get_git_info(caminho_completo)
            descricao = extrair_docstring(caminho_completo) # <--- NOVIDADE AQUI
            
            # Formato: - [arquivo](link): Mensagem Git | *Descrição do código*
            linhas.append(f"- **[{arquivo}](./{pasta}/{arquivo})**: {git_info}{descricao}")
    
    if not linhas:
        return ["- *Nenhum script encontrado.*"]
    return linhas

def atualizar_conteudo(texto_original, header_regex, nova_lista_linhas):
    """Substitui a lista abaixo do cabeçalho preservando a estrutura."""
    pattern = re.compile(f"({header_regex}.*?)(?=\n#|\\Z)", re.DOTALL)
    match = pattern.search(texto_original)
    if not match: return texto_original

    bloco_inteiro = match.group(1)
    divisao = re.search(r"(?=\n- )", bloco_inteiro)
    
    texto_intro = bloco_inteiro[:divisao.start()].strip() if divisao else bloco_inteiro.strip()
    novo_bloco = f"{texto_intro}\n" + "\n".join(nova_lista_linhas) + "\n"
    return texto_original.replace(bloco_inteiro, novo_bloco)

def main():
    # 1. Atualizar README Principal (Raiz)
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            conteudo_root = f.read()
        
        modificou_root = False
        for pasta, headers in MAPA_MODULOS.items():
            if os.path.exists(pasta):
                lista = gerar_lista_arquivos(pasta)
                novo_conteudo = atualizar_conteudo(conteudo_root, headers["root"], lista)
                if novo_conteudo != conteudo_root:
                    conteudo_root = novo_conteudo
                    modificou_root = True
        
        if modificou_root:
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(conteudo_root)
            print("✅ README.md (Raiz) atualizado com descrições.")

    # 2. Atualizar READMEs das Subpastas
    for pasta, headers in MAPA_MODULOS.items():
        sub_readme = os.path.join(pasta, 'README.md')
        if os.path.exists(sub_readme):
            with open(sub_readme, 'r', encoding='utf-8') as f:
                conteudo_sub = f.read()
            
            lista = gerar_lista_arquivos(pasta)
            lista_local = [l.replace(f"./{pasta}/", "") for l in lista]
            
            novo_conteudo_sub = atualizar_conteudo(conteudo_sub, headers["sub"], lista_local)
            with open(sub_readme, 'w', encoding='utf-8') as f:
                f.write(novo_conteudo_sub)
            print(f"✅ {sub_readme} atualizado.")

if __name__ == "__main__":
    main()