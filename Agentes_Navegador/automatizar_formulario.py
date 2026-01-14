#!/usr/bin/env python3
"""
NÍVEL 2: Agente Navegador Autônomo
FUNÇÃO: Simula um usuário acessando um site e preenchendo formulários 
        Auxiliado por posicao_cursor_tela.py e Data/csv/produtos_automacao_formulario.csv  
CONCEITOS: Automação de Tarefas e Bots | Acesso a Informações de Arquivo CSV.
"""
import pyautogui
import time
import pandas as pd
from pathlib import Path
import webbrowser

# ---Lógica da Programação---
pyautogui.PAUSE = 0.5 

# Passo1: Entrar no sistema da empresa
site = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"

# Tenta abrir o Firefox especificamente, se falhar, abre o padrão
try:
    print("Tentando abrir Firefox...")
    webbrowser.get('firefox').open(site)
except webbrowser.Error:
    print("Firefox não encontrado, usando navegador padrão...")
    webbrowser.open(site)

# Passo2: Fazer Login
# Aumentamos para 6s para garantir que a INTERNET carregou o site
# Se sua internet oscilar, talvez precise de mais tempo.
time.sleep(6) 

# Clica no campo de e-mail
pyautogui.click(x=417, y=436)
pyautogui.write("hackeando_hashtag@gmail.com")
pyautogui.press("tab")
pyautogui.write("senha_hacker")
pyautogui.press("tab")
pyautogui.press("enter")

# Passo3: Abrir a base de dados
time.sleep(4) # Pausa para carregar a próxima página após o login
CAMINHO_SCRIPT = Path(__file__).resolve().parent 
ARQUIVO_CSV = CAMINHO_SCRIPT.parent / "Data" / "csv" / "produtos_automacao_formulario.csv"
tabela = pd.read_csv(ARQUIVO_CSV) 

# Passo4: Cadastrar Produto
for linha in tabela.index:    
    # Clique inicial para garantir o foco
    pyautogui.click(x=439, y=320)
    
    # codigo   
    codigo = str(tabela.loc[linha, "codigo"])
    pyautogui.write(codigo)
    pyautogui.press("tab")
    
    # marca    
    marca = str(tabela.loc[linha, "marca"])
    pyautogui.write(marca)
    pyautogui.press("tab")
    
    # tipo    
    tipo = str(tabela.loc[linha, "tipo"])
    pyautogui.write(tipo)
    pyautogui.press("tab")
    
    # categoria    
    categoria = str(tabela.loc[linha, "categoria"])
    pyautogui.write(categoria)
    pyautogui.press("tab")
    
    # preço unitário    
    preco = str(tabela.loc[linha, "preco_unitario"])
    pyautogui.write(preco)
    pyautogui.press("tab")
    
    # custo    
    custo = str(tabela.loc[linha, "custo"])
    pyautogui.write(custo)
    pyautogui.press("tab")
    
    # obs    
    obs = str(tabela.loc[linha, "obs"])
    if obs != "nan": 
       pyautogui.write(obs)
    pyautogui.press("tab")
    
    # Enviar
    pyautogui.press("enter") 
    
    # Rolar para cima para o próximo loop
    pyautogui.press("pgup")