#!/usr/bin/env python3
"""
NÍVEL 3: Agente Navegador com Visão Computacional
FUNÇÃO: Localiza elementos na tela por imagem.
        Sincroniza visualmente a cada produto para não perder o passo.
DEPENDÊNCIAS: pip install opencv-python pyautogui pandas
"""
import pyautogui
import time
import pandas as pd
from pathlib import Path
import webbrowser

# --- Configurações ---
CONFIDENCE_LEVEL = 0.7 
pyautogui.PAUSE = 0.5

# Caminhos
CAMINHO_SCRIPT = Path(__file__).resolve().parent
ARQUIVO_CSV = CAMINHO_SCRIPT.parent / "Data" / "csv" / "produtos_automacao_formulario.csv"
PASTA_IMAGENS = CAMINHO_SCRIPT.parent / "Data" / "ui_assets"

# --- Função Visual ---
def esperar_e_clicar(nome_imagem, tempo_limite=20, offset_x=0, offset_y=0):
    caminho_img = str(PASTA_IMAGENS / nome_imagem)
    inicio = time.time()
    # print(f"Procurando: {nome_imagem}...") # Comentei para limpar o terminal
    
    while True:
        try:
            localizacao = pyautogui.locateCenterOnScreen(caminho_img, confidence=CONFIDENCE_LEVEL, grayscale=True)
            if localizacao:
                x, y = localizacao
                pyautogui.click(x + offset_x, y + offset_y)
                return True
        except pyautogui.ImageNotFoundException:
            pass 
        except Exception:
            pass

        if time.time() - inicio > tempo_limite:
            return False
        time.sleep(0.5)

# --- Início ---
print("Iniciando Agente Visual...")
site = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"

try:
    webbrowser.get('firefox').open(site)
except:
    webbrowser.open(site)

# Login
if esperar_e_clicar("campo_email_automatizar_visual.png", offset_y=35):
    pyautogui.write("hackeando_hashtag@gmail.com")    
    pyautogui.press("tab")
    pyautogui.write("senha_hacker")
    pyautogui.press("tab")
    pyautogui.press("enter")
else:
    print("❌ Erro: Login falhou (Imagem não encontrada)")
    exit()

# Dados
tabela = pd.read_csv(ARQUIVO_CSV)

# Cadastro (Loop Sincronizado)
for linha in tabela.index:
    
    # 1. SINCRONIZAÇÃO VISUAL
    # Tenta clicar no campo código. Se falhar visualmente, usa o TAB como emergência.
    if not esperar_e_clicar("campo_codigo_automatizar_visual.png", tempo_limite=3, offset_y=35):
        print(f"⚠️ Aviso: Sincronia visual perdida na linha {linha}. Tentando TAB.")
        pyautogui.press("tab")
    
    # Se o clique funcionou, o cursor JÁ está no lugar certo. E o TAB de emergência não ocorrerá.
    
    # 1. Código
    codigo = str(tabela.loc[linha, "codigo"])
    pyautogui.write(codigo)
    pyautogui.press("tab")
    
    # 2. Marca
    marca = str(tabela.loc[linha, "marca"])
    pyautogui.write(marca)
    pyautogui.press("tab")
    
    # 3. Tipo
    tipo = str(tabela.loc[linha, "tipo"])
    pyautogui.write(tipo)
    pyautogui.press("tab")
    
    # 4. Categoria
    categoria = str(tabela.loc[linha, "categoria"])
    pyautogui.write(categoria)
    pyautogui.press("tab")
    
    # 5. Preço (Com tratamento de Vírgula)
    preco = str(tabela.loc[linha, "preco_unitario"])
    preco = preco.replace(".", ",") 
    pyautogui.write(preco)
    pyautogui.press("tab")
    
    # 6. Custo (Com tratamento de Vírgula e Vazio)
    custo = str(tabela.loc[linha, "custo"])
    if custo == "nan": custo = "0"
    custo = custo.replace(".", ",")
    pyautogui.write(custo)
    pyautogui.press("tab")
    
    # 7. Obs
    obs = str(tabela.loc[linha, "obs"])
    if obs != "nan":
       pyautogui.write(obs)
    pyautogui.press("tab")
    
    # Enviar e Reiniciar
    pyautogui.press("enter")
    pyautogui.press("pgup")
    # Pequena pausa para a tela rolar antes de procurar a imagem de novo
    time.sleep(0.5)