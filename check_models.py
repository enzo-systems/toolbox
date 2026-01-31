from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

print("--- INTERROGANDO API DO GOOGLE ---")
print("Listando modelos disponíveis para sua conta:")

try:
    # Pega a lista crua do servidor
    for m in client.models.list():
        # Filtra apenas os que geram texto (Gemini)
        if "generateContent" in m.supported_actions:
            print(f"ID: {m.name} | Display: {m.display_name}")
except Exception as e:
    print(f"Erro ao listar: {e}")

print("----------------------------------")