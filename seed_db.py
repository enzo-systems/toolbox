import sqlite3
import os

DB_PATH = "data/chat_history.db"

# A Memória Primordial (Resumo Contextual)
MEMORIA_INICIAL = [
    
    # aqui você pode inserir manualmente suas informações no banco de dados
    
]

def semear_banco():
    print(f"💀 Conectando ao Banco: {DB_PATH}...")
    
    if not os.path.exists("data"):
        os.makedirs("data")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Garante que a tabela existe (caso rode antes do app.py)
    c.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_content ON mensagens(content)')

    # 2. Inserção
    print("⚡ Injetando Memória Primordial...")
    for role, content in MEMORIA_INICIAL:
        c.execute('INSERT INTO mensagens (role, content) VALUES (?, ?)', (role, content))
    
    conn.commit()
    conn.close()
    print("✅ Sucesso. O Cérebro agora possui contexto.")

if __name__ == "__main__":
    semear_banco()
