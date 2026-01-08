# 🛠️ ToolBox - Ecossistema de Agentes Autônomos

### 📂 Visão Geral
Este repositório é uma **Caixa de Ferramentas Modular**. Cada pasta contém agentes especializados que funcionam de forma independente.
Use este README como um **Índice Dinâmico** para encontrar a ferramenta certa para sua tarefa.

---

### 🛰️ /Agentes_Dados
> Coleta de dados, Scraping e Processamento de RSS.

- 🐍 **[career_hunter.py](./Agentes_Dados/career_hunter.py)** (2026-01-08) | *NÍVEL 2: Career Hunter STATUS: Corrigido com Debug de Caminhos Absolutos.*
- 🐍 **[cotacao_dolar.py](./Agentes_Dados/cotacao_dolar.py)** (2026-01-08) | *NÍVEL 2: Agente Financeiro Autônomo FUNÇÃO: Captura cotações em tempo real via API e gera séries históricas. CONCEITOS: Integração de APIs REST, Configuração Centralizada, Persistência CSV.*
- 🐍 **[global_news_sniper.py](./Agentes_Dados/global_news_sniper.py)** (2026-01-08) | *NÍVEL 2: Agente de Inteligência de Dados (Global Sniper) FUNÇÃO: Coleta e processa notícias internacionais via RSS (Feedparser). CONCEITOS: RSS Parsing, Normalização de Dados, Persistência JSON.*
- 🐍 **[news_sniper.py](./Agentes_Dados/news_sniper.py)** (2026-01-08) | *NÍVEL 2: Agente de Extração de Dados (News Sniper) STATUS: Corrigido com Debug de Caminhos Absolutos.*

### 👁️ /Agentes_Visao
> Computer Vision: Análise, filtros e manipulação de imagens.

- 🐍 **[vision_processor.py](./Agentes_Visao/vision_processor.py)** (2026-01-08) | *NÍVEL 3: Processador de Visão Computacional (Vision Processor) FUNÇÃO: Higienização e formatação de fotos de perfil (LinkedIn Style) em lote. CONCEITOS: Pillow, Pipeline de I/O, Processamento em Batch.*

### 🎙️ /Agentes_Voz
> Síntese de Voz (TTS) e Clonagem de Áudio (XTTS).

- 🐍 **[voice_synthesizer.py](./Agentes_Voz/voice_synthesizer.py)** (2026-01-08) | *NÍVEL 4: Sintetizador de Inteligência Auditiva (Voice Cloner) FUNÇÃO: Processamento de áudio e síntese vocal (TTS) com auto-conversão de formatos. CONCEITOS: DSP, Wrappers de FFmpeg, Pipeline de Áudio Automatizado.*

### 🖥️ /Agentes_Monitor
> Monitoramento de sistema, rede e hardware.

- 🐍 **[sentinela.py](./Agentes_Monitor/sentinela.py)** (2026-01-08) | *NÍVEL 2: Sentinela de Infraestrutura FUNÇÃO: Vigia a conectividade e gerencia a rotatividade de logs do sistema. CONCEITOS: I/O de Sistema, RotatingFileHandler, Daemonize Simulation.*
- 🐍 **[ssl_hunter.py](./Agentes_Monitor/ssl_hunter.py)** (2026-01-08) | *NÍVEL 2: Auditor de Criptografia e Redes FUNÇÃO: Varredura e validação de certificados SSL/TLS em domínios externos. CONCEITOS: pyOpenSSL, Protocolos de Segurança, Persistência de Auditoria.*
- 🐍 **[system_expert.py](./Agentes_Monitor/system_expert.py)** (2026-01-08) | *NÍVEL 1: Agente de Diagnóstico de Infraestrutura FUNÇÃO: Analisa comandos Linux e gera documentação formatada para comunidades. CONCEITOS: Shell Integration, Log Parsing, Integração com API TLDR.*
- 🐍 **[watchdog_sentinela.py](./Agentes_Monitor/watchdog_sentinela.py)** (2026-01-08) | *NÍVEL 2: Watchdog (Supervisor de Resiliência) FUNÇÃO: Valida o heartbeat do Sentinela e dispara alertas visuais no Fedora. CONCEITOS: Auditoria de Heartbeat, Notificação de Sistema (GNOME), Resiliência.*
- 🐍 **[web_monitor.py](./Agentes_Monitor/web_monitor.py)** (2026-01-08) | *NÍVEL 2: Agente de Integridade de Redes FUNÇÃO: Monitora disponibilidade e latência de serviços web críticos. CONCEITOS: Socket Programming, HTTP Status Monitoring, Tempo de Resposta.*

### 📜 /Scripts
> Automação de infraestrutura e manutenção do OS.

- 🐚 **[backup_toolbox.sh](./Scripts/backup_toolbox.sh)** (2026-01-07) | *NÍVEL 1: Automação de Infraestrutura*

### 📊 /Data
> Repositório de Arquivos (Inputs e Outputs).

- ⚙️ **[json/auditoria_ssl.json](./Data/json/auditoria_ssl.json)** (2026-01-08)
- ⚙️ **[json/global_news_memory.json](./Data/json/global_news_memory.json)** (2026-01-08)
- ⚙️ **[json/memoria_world.json](./Data/json/memoria_world.json)** (2026-01-08)
- ⚙️ **[json/news_sniper_memory.json](./Data/json/news_sniper_memory.json)** (2026-01-08)
- ⚙️ **[json/sentinela_status.json](./Data/json/sentinela_status.json)** (2026-01-08)
- ⚙️ **[json/vagas_encontradas.json](./Data/json/vagas_encontradas.json)** (2026-01-08)
- ⚙️ **[json/web_monitor_results.json](./Data/json/web_monitor_results.json)** (2026-01-08)
- 📂 **[output_audio/ (Estrutura)](./Data/output_audio)**  | *Diretório de Saída (Conteúdo gerado ignorado pelo Git)*
- 📂 **[output_images/ (Estrutura)](./Data/output_images)**  | *Diretório de Saída (Conteúdo gerado ignorado pelo Git)*
- 📄 **[csv/cotacao_dolar.csv](./Data/csv/cotacao_dolar.csv)** (2026-01-08)
- 📄 **[input_audio/referencia.m4a](./Data/input_audio/referencia.m4a)** (2026-01-08)
- 📄 **[input_audio/roteiro.txt](./Data/input_audio/roteiro.txt)** (2026-01-08)
- 🔊 **[input_audio/referencia.wav](./Data/input_audio/referencia.wav)** (Novo/Local)
- 🔊 **[output_audio/audio_clonado_final.wav](./Data/output_audio/audio_clonado_final.wav)** (Novo/Local)
- 🖼️ **[input_images/minha_foto.jpg](./Data/input_images/minha_foto.jpg)** (Novo/Local)
- 🖼️ **[output_images/perfil_minha_foto.png](./Data/output_images/perfil_minha_foto.png)** (Novo/Local)

### 📝 /Logs
> Histórico de execução e auditoria.

- 📂 **[/ (Estrutura)](./Logs/)**  | *Diretório de Saída (Conteúdo gerado ignorado pelo Git)*

---
### 🛠️ Engenharia e Stack
- **Linguagem:** Python 3.10+
- **Documentação:** Gerada automaticamente via `main.py`.
- **Estrutura:**
    - `Agentes_*`: Módulos funcionais independentes.
    - `Data`: Armazenamento de inputs (matéria-prima) e outputs (resultados).
