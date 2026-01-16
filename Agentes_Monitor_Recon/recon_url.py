#!/usr/bin/env python3
import requests
import re

URL_ALVO = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"

print(f"🕵️  Sondando o alvo: {URL_ALVO}")

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(URL_ALVO, headers=headers)
    html = response.text
    
    # Busca via Regex (Hacker leve, sem instalar BeautifulSoup)
    # Procura por <form ... action="ALGO">
    match_action = re.search(r'<form[^>]*action=["\'](.*?)["\']', html)
    
    if match_action:
        endpoint = match_action.group(1)
        print(f"\n🚨 [ALVO ENCONTRADO] O formulário envia dados para: {endpoint}")
        
        # Se o endpoint for relativo (ex: /login/auth), monta a URL completa
        if not endpoint.startswith("http"):
            print(f"   👉 URL Completa para POST: https://dlp.hashtagtreinamentos.com{endpoint}")
        else:
            print(f"   👉 URL Completa para POST: {endpoint}")
            
    else:
        print("\n⚠️ Não achei o atributo 'action' explícito no form.")
        print("   Isso indica que o envio pode ser via JavaScript (Ajax).")
        print("   Nesse caso, a única saída é usar o F12 (Network Tab).")

except Exception as e:
    print(f"❌ Erro de conexão: {e}")