import streamlit as st
from google import genai
import asyncio
import os
import sqlite3
import re
from dotenv import load_dotenv

# Carrega variáveis de ambiente (.env)
load_dotenv()

# --- 0. CONSTANTES & CONFIGURAÇÃO ---
DB_PATH = "data/chat_history.db"
MODELO_ALVO = "gemini-3-flash-preview"

# PERSONA PRINCIPAL
SYSTEM_PROMPT = """
REGRA MESTRA: Roleplay como "Co-Processador Lógico" (Backend Builder).
AMBIENTE: Debian Linux (Minimalista) + Python Localhost (4GB RAM) + SQLite.
IDIOMA: PORTUGUÊS (BRASIL) TÉCNICO OBRIGATÓRIO.

### 1. PERFIL DO OPERADOR (HUMANWARE: ENZO)
- **Role:** Auditor Técnico / Arquiteto (41 anos).
- **Cognitivo:** TDAH (Fluxo Acelerado -> Exige Single Thread/Passo-a-Passo).
- **Safety:** Evitar redundância (Ruído Cognitivo). Foco em lógica crua.

### 2. AMBIENTE DE EXECUÇÃO (MACHINE: DELL 3442)
- **Hardware:** Intel Haswell | 4GB RAM (Crítico) | SSD 120GB.
- **Stack:** GNU/Debian 13 (Trixie) | VSCodium | Python 3.13 (AsyncIO).
- **Persistência:** SQLite Nativo (Zero ORM).
- **Restrição:** Localhost Only. Zero Cloud Paga.

### 3. ARQUITETURA LÓGICA (TOOLBOX V4)
- **Interface:** Streamlit (Web Local).
- **Modos:**
  A. **Conversacional:** Single Thread (Planejamento).
  B. **Cluster:** Multi-Thread (Coder + Auditor + Optimizer).
- **Memória (RAG):** Contexto injetado via busca SQL por palavras-chave (Indexação em Disco).

### 4. DIRETRIZES IMUTÁVEIS (KERNEL DRIVERS)
1. ATOMICIDADE: Um passo por vez. Aguarde "OK".
2. BAIXO NÍVEL: Explique impacto em RAM (Stack/Heap) e Disco.
3. PERSONALIDADE: Zero Fluff. Angst/Realismo. Verdade técnica.
4. SINTAXE: O usuário define a lógica, o sistema gera o código pronto.
"""

st.set_page_config(page_title="ToolBox SQL v4.3", page_icon="💀", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #d4d4d4; }
    code { color: #50fa7b; font-family: 'Consolas', monospace; }
    .stSidebar { background-color: #000; border-right: 1px solid #333; }
    .stStatus { border: 1px solid #bd93f9; }
</style>
""", unsafe_allow_html=True)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("🔑 API Key:", type="password")

# --- 1. CAMADA DE PERSISTÊNCIA (SQLITE) ---
def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_content ON mensagens(content)')
    conn.commit()
    conn.close()

def salvar_mensagem(role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO mensagens (role, content) VALUES (?, ?)', (role, content))
    conn.commit()
    conn.close()

def carregar_historico_recente(limite):
    """
    Query Otimizada:
    SELECT ... LIMIT N
    O Kernel do SQLite lê apenas os últimos N blocos do disco.
    O Browser recebe apenas N objetos JSON.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT role, content FROM mensagens ORDER BY id DESC LIMIT ?', (limite,))
    rows = c.fetchall()
    conn.close()
    return rows[::-1] 

def buscar_contexto_sql(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    palavras = list(set(re.findall(r'\w+', query.lower())) - {'o','a','e','de','que','para','com','um','uma'})
    
    if not palavras:
        conn.close()
        return None

    query_sql = "SELECT content FROM mensagens WHERE role = 'user' AND (" + " OR ".join(["content LIKE ?"] * len(palavras)) + ")"
    params = [f"%{p}%" for p in palavras]
    
    c.execute(query_sql + " ORDER BY id DESC LIMIT 3", params)
    rows = c.fetchall()
    conn.close()
    
    return "\n---\n".join([r[0] for r in rows]) if rows else None

init_db()

# --- 2. LÓGICA DE AGENTES (ASYNC) ---

async def chat_conversacional(api_key, query, contexto_rag):
    client = genai.Client(api_key=api_key)    
    # Injeção da Restrição Negativa Local
    restricao = "ALERTA DE MODO: ESTAMOS NO MODO CONVERSACIONAL. PROIBIDO GERAR CÓDIGO. FOQUE NA LÓGICA E ARQUITETURA."    
    prompt_final = f"{SYSTEM_PROMPT}\n\nCTX SQL:\n{contexto_rag}\n\n{restricao}\n\nUSER (AUDITOR): {query}"    
    response = await client.aio.models.generate_content(model=MODELO_ALVO, contents=prompt_final)
    return response.text

async def worker_agente(client, nome, role, query, contexto_rag):
    prompt_worker = f"""
    ROLE: {role}
    CONTEXTO RECUPERADO: {contexto_rag}
    TAREFA DO USUÁRIO: {query}
    DIRETRIZES RÍGIDAS:
    1. IDIOMA: PORTUGUÊS (BRASIL) TÉCNICO OBRIGATÓRIO.
    2. CONCISÃO: Responda em no máximo 2 parágrafos ou código direto.
    3. FOCO: Baixo Nível (Kernel, Hardware, Memory Management).
    4. ZERO FLUFF.
    """
    try:
        response = await client.aio.models.generate_content(model=MODELO_ALVO, contents=prompt_worker)
        return nome, response.text
    except Exception as e:
        return nome, f"ERRO NO WORKER: {e}"

async def chat_cluster(api_key, query, contexto_rag):
    client = genai.Client(api_key=api_key)
    t1 = worker_agente(client, "CODER", "Gerador de Código Python/Bash (Zero libs externas).", query, contexto_rag)
    t2 = worker_agente(client, "AUDITOR", "Analista de Segurança, Kernel Linux e Syscalls.", query, contexto_rag)
    t3 = worker_agente(client, "OPTIMIZER", "Engenheiro de Performance (Big-O, RAM, Disk I/O).", query, contexto_rag)
    return await asyncio.gather(t1, t2, t3)

# --- 3. INTERFACE VISUAL (FRONTEND) ---
with st.sidebar:
    st.header(f"🎛️ Kernel: {MODELO_ALVO}")
    modo_operacao = st.radio("Fluxo:", ["💬 Conversacional", "⚡ Cluster (3 Agentes)"])
    
    st.divider()
    
    # --- CONTROLE DE PAGINAÇÃO (SLIDER) ---
    # Isso resolve o problema dos 30GB na tela.
    # O padrão é 30 msg. Máximo 100.
    limit_msgs = st.slider("Janela de Mensagens (RAM)", 5, 100, 30, help="Define quantas mensagens antigas são carregadas do disco.")
    
    st.divider()
    if st.button("🧨 Drop Database (Reset Total)"):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            init_db()
            st.rerun()

st.title(f"💀 ToolBox: {modo_operacao}")

# Renderiza o histórico (Limitado pelo Slider)
historico = carregar_historico_recente(limit_msgs)
for msg in historico:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. LOOP DE EXECUÇÃO ---
if prompt := st.chat_input("Input do Arquiteto..."):
    if not api_key:
        st.warning("⚠ API Key não detectada.")
        st.stop()

    salvar_mensagem("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    contexto_rag = buscar_contexto_sql(prompt)
    if contexto_rag:
        with st.expander("🗄️ SQL RAG: Memória Ativada", expanded=False):
            st.code(contexto_rag, language="sql")

    with st.chat_message("assistant"):
        if modo_operacao == "💬 Conversacional":
            with st.spinner("Single Thread Processing..."):
                resposta = asyncio.run(chat_conversacional(api_key, prompt, contexto_rag))
                st.markdown(resposta)
                salvar_mensagem("assistant", resposta)

        elif modo_operacao == "⚡ Cluster (3 Agentes)":
            st.status("Forking Processes (3 Threads)...", expanded=True)
            resultados = asyncio.run(chat_cluster(api_key, prompt, contexto_rag))
            
            texto_final = "### 🧠 Relatório do Cluster\n"
            cols = st.columns(3)
            for i, (nome, r) in enumerate(resultados):
                cols[i].markdown(f"**{nome}**")
                cols[i].caption(r[:100] + "...")
                texto_final += f"\n---\n#### 🤖 {nome}\n{r}\n"
            
            st.markdown(texto_final)
            salvar_mensagem("assistant", texto_final)