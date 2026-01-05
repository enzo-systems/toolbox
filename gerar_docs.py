import os
import re
import subprocess

# --- Configurações ---
# Define onde procurar no README Principal (root) e no README da Subpasta (sub)
MAPA_MODULOS = {
    "Robos": {"root": r"### 🤖 /Robos", "sub": r"## 📜 Lista de Scripts"},
    "Imagens": {"root": r"### 🖼️ /Imagens", "sub": r"## 📜 Lista de Scripts"},
    "CloneVoz": {"root": r"### 🎙️ /CloneVoz", "sub": r"## 📜 Lista de Scripts"}
}

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
    """Gera a lista em Markdown com os status do Git."""
    linhas = []
    if os.path.exists(pasta):
        # Filtra apenas .py e .json
        arquivos = sorted([f for f in os.listdir(pasta) if f.endswith('.py') or f.endswith('.json')])
        for arquivo in arquivos:
            caminho_completo = os.path.join(pasta, arquivo)
            info = get_git_info(caminho_completo)
            # Cria o link: [arquivo](./Pasta/arquivo)
            linhas.append(f"- **[{arquivo}](./{pasta}/{arquivo})**: {info}")
    
    if not linhas:
        return ["- *Nenhum script encontrado.*"]
    return linhas

def atualizar_conteudo(texto_original, header_regex, nova_lista_linhas):
    """Substitui apenas a lista abaixo do cabeçalho específico."""
    # Encontra do cabeçalho até o próximo título (#) ou fim do arquivo
    pattern = re.compile(f"({header_regex}.*?)(?=\n#|\\Z)", re.DOTALL)
    match = pattern.search(texto_original)
    
    if not match:
        return texto_original

    bloco_inteiro = match.group(1)
    
    # Tenta achar onde começa a lista antiga para preservar o texto de introdução
    divisao = re.search(r"(?=\n- )", bloco_inteiro)
    
    if divisao:
        texto_intro = bloco_inteiro[:divisao.start()].strip()
    else:
        texto_intro = bloco_inteiro.strip()

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
            print("✅ README.md (Raiz) atualizado.")

    # 2. Atualizar READMEs das Subpastas
    for pasta, headers in MAPA_MODULOS.items():
        sub_readme = os.path.join(pasta, 'README.md')
        if os.path.exists(sub_readme):
            with open(sub_readme, 'r', encoding='utf-8') as f:
                conteudo_sub = f.read()
            
            # Gera lista e ajusta links para serem locais (remove ./Pasta/)
            lista = gerar_lista_arquivos(pasta)
            lista_local = [l.replace(f"./{pasta}/", "") for l in lista]
            
            novo_conteudo_sub = atualizar_conteudo(conteudo_sub, headers["sub"], lista_local)
            
            with open(sub_readme, 'w', encoding='utf-8') as f:
                f.write(novo_conteudo_sub)
            print(f"✅ {sub_readme} atualizado.")

if __name__ == "__main__":
    main()
