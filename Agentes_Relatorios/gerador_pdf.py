#!/usr/bin/env python3
"""
AGENTE DE RELATÓRIOS
Função: Gerar documentação estratégica e relatórios em PDF.
"""
from fpdf import FPDF
from pathlib import Path

# --- CONFIGURAÇÃO DE CAMINHOS ---
# Define a raiz do projeto baseando-se na localização deste script
BASE_DIR = Path(__file__).resolve().parent.parent
DIR_PDF = BASE_DIR / "Data" / "pdf"

# Garante que a pasta Data/pdf existe
DIR_PDF.mkdir(parents=True, exist_ok=True)

class PDF(FPDF):
    def header(self):
        # Fonte Arial Bold 14
        self.set_font('Arial', 'B', 14)
        # Título
        self.cell(0, 10, 'Plano Estratégico: Python Impressionador (Debian Edition)', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, num, label):
        # Fonte Arial 12
        self.set_font('Arial', 'B', 12)
        # Cor de fundo cinza claro
        self.set_fill_color(230, 230, 230)
        # Título do capítulo
        self.cell(0, 6, f'{num} : {label}', 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        # Fonte Arial 11
        self.set_font('Arial', '', 11)
        # Imprime o corpo do texto justificado
        self.multi_cell(0, 6, body)
        self.ln()

# Instanciação do objeto PDF
pdf = PDF()
pdf.set_title("Plano Estratégico Debian")
pdf.add_page()

# --- CONTEÚDO DO TEXTO ---

# Introdução
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 6, 'Veredito: Sim, o curso vai "turbinar" sua recolocação.', 0, 1)
pdf.ln(2)
pdf.set_font('Arial', '', 11)
texto_intro = (
    "O Diferencial: Você usará o curso como um repositório de lógica de negócios e projetos, "
    "mas executará tudo com ferramentas superiores (Debian/Terminal/VSCodium). "
    "Enquanto outros alunos clicam em menus, você estará automatizando via linha de comando."
)
pdf.multi_cell(0, 6, texto_intro)
pdf.ln(5)

# Capítulo 1
pdf.chapter_title('1', 'O Filtro Técnico: Adaptando a Ementa ao Seu "Chão de Fábrica"')
texto_cap1 = (
    "O curso foi desenhado para Windows e VS Code padrão. Sua vantagem competitiva está em "
    "traduzir isso para um ambiente de alta performance e zero bloatware.\n\n"
    "A. Ambiente de Desenvolvimento (VSCodium + Terminal)\n"
    "- O Curso Ensina: Instalar VS Code e extensões proprietárias, usar menus para criar pastas.\n"
    "- Sua Realidade (VSCodium): Experiência 99% idêntica, sem telemetria. "
    "Ação: Eu ajudarei a achar alternativas Open Source para extensões Microsoft.\n"
    "- Sua Realidade (Terminal): Agilidade via comando (mkdir, touch) em vez de menus lentos.\n"
    "- Gerenciamento: Ignore o Anaconda (bloatware). Usaremos 'python3 -m venv' ou 'poetry'.\n\n"
    "B. O 'Elefante na Sala': Excel e Power BI\n"
    "- O Curso Ensina: Controle de Excel instalado e Power BI Desktop.\n"
    "- Sua Realidade (Debian): Você não tem esses softwares pesados.\n"
    "- Solução Excel: Usaremos 'pandas' e 'openpyxl' para manipular arquivos (.xlsx) via script, "
    "o que é mais rápido que abrir o software.\n"
    "- Solução Power BI: Pivotaremos para Streamlit (Módulo 35) ou Django (Módulo 41). "
    "Dashboards via navegador, ideais para SaaS.\n\n"
    "C. Interface Gráfica (GUI)\n"
    "- O Curso Ensina: Tkinter (Desktop).\n"
    "- Solução: Pule o Tkinter para evitar dependências pesadas do X11. Foque 100% em Web (Django/Flask/Streamlit)."
)
pdf.chapter_body(texto_cap1)

# Capítulo 2
pdf.chapter_title('2', 'O Caminho do Dinheiro Rápido (Roteiro de Estudos)')
texto_cap2 = (
    "Para rentabilizar rápido, focaremos em produtos 'invisíveis' (scripts backend) e automação headless.\n\n"
    "Fase 1: A Base Sólida (Módulos 1-16)\n"
    "- Foco: Sintaxe moderna e Lógica.\n"
    "- Ferramenta: VSCodium + Terminal.\n"
    "- Objetivo: Reaquecer músculos de programação (f-strings, List Comprehensions).\n\n"
    "Fase 2: A Mina de Ouro - Automação e Dados (Módulos 28-30, 32, 39)\n"
    "- O que Vender: Bots de monitoramento e extração de dados.\n"
    "- Web Scraping: Robôs 'headless' (sem interface) consumindo mínima RAM em VPS Linux.\n"
    "- APIs: Scripts de integração (ex: Web -> Google Sheets).\n\n"
    "Fase 3: O Produto Final - SaaS e Web (Módulos 35, 36, 41)\n"
    "- O que Vender: Dashboards interativos e Sistemas Web.\n"
    "- Streamlit: Substitui o Power BI com Python puro.\n"
    "- Deploy: Transição natural do Debian local para servidores Linux (Render/Railway)."
)
pdf.chapter_body(texto_cap2)

# Capítulo 3
pdf.chapter_title('3', 'O Papel do Gemini: Seu Copiloto Linux')
texto_cap3 = (
    "O curso é gravado em Windows. Eu serei a ponte que traduz tudo para o Debian.\n\n"
    "- Tradução de Caminhos: Corrigo 'C:\\Users' para '/home/user' usando pathlib.\n"
    "- Drivers: Comandos exatos para configurar chromedriver/geckodriver no Linux.\n"
    "- Ambiente Limpo: Guia para ambientes virtuais (venv) isolados.\n"
    "- Adaptação: Recomendação de alternativas CLI ou Open Source para ferramentas Windows."
)
pdf.chapter_body(texto_cap3)

# Rodapé/Conclusão
pdf.ln(5)
pdf.set_font('Arial', 'I', 11)
pdf.multi_cell(0, 6, "Resumo da Ação: Compre o curso pelos projetos e pela lógica. Use o VSCodium e o Debian para executar com superioridade técnica.")

# --- SALVAMENTO FINAL ---
nome_arquivo = "Plano_Estrategico_Debian.pdf"
caminho_final = DIR_PDF / nome_arquivo

try:
    # str(caminho_final) converte o objeto Path para string que o fpdf entende
    pdf.output(str(caminho_final))
    print(f"✅ PDF gerado com sucesso!")
    print(f"📂 Local: {caminho_final}")
except Exception as e:
    print(f"❌ Erro ao gerar PDF: {e}")