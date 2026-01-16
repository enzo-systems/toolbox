#!/usr/bin/env python3
import requests

# A URL suspeita (Padrão desse desafio)
URL_ALVO = "https://dlp.hashtagtreinamentos.com/python/intensivao/cadastrar"

print(f"🎯 Mirando em: {URL_ALVO}")

payload = {
    "codigo": "TESTE_KERNEL",
    "marca": "ToolBox",
    "tipo": "Software",
    "categoria": "Hacker",
    "preco_unitario": "100,00",
    "custo": "50,00",
    "obs": "Teste de injeção via Python"
}

try:
    # Dispara o POST
    response = requests.post(URL_ALVO, data=payload)
    
    print(f"\n📡 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCESSO! A porta está aberta.")
        print("   O servidor aceitou os dados. Você pode rodar o bot_http_hacker.py agora.")
    elif response.status_code == 405:
        print("❌ 405 - Método não permitido (URL errada).")
    elif response.status_code == 500:
        print("⚠️ 500 - Erro no Servidor (Talvez os nomes dos campos estejam errados).")
    else:
        print(f"⚠️ Resposta inesperada: {response.text[:100]}")

except Exception as e:
    print(f"❌ Erro de conexão: {e}")