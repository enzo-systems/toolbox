# 🛠️ ToolBox - Ecossistema de Agentes Autônomos

### 📂 Visão Geral e Arquitetura
Este repositório foi reestruturado para operar através de **Agentes Especializados**. Cada diretório representa um domínio de competência técnica, integrando automação modular sob uma arquitetura de níveis.

* **Agentes de Dados:** Inteligência de busca, scraping e coleta de dados.
* **Agentes de Monitor:** Integridade de redes, latência e diagnóstico de sistemas.
* **Agentes de Visao:** Processamento de imagem, higienização e privacidade.
* **Agentes de Voz:** Síntese vocal e inteligência auditiva.
* **Infraestrutura:** Gestão de logs, configurações centralizadas e automação bash.

---

### 🛰️ /Agentes_Dados
> Coleta e processamento de notícias e oportunidades (Scraping/RSS).

- **[career_hunter.py](./Agentes_Dados/career_hunter.py)**: (2026-01-08) | *NÍVEL 2: Agente de Monitoramento de Mercado FUNÇÃO: Rastreia e filtra oportunidades de carreira em portais especializados. CONCEITOS: Web Crawling, BeautifulSoup4, Automação de Busca, Persistência de Dados.*
- **[cotacao_dolar.py](./Agentes_Dados/cotacao_dolar.py)**: (2026-01-08) | *NÍVEL 2: Agente Financeiro Autônomo FUNÇÃO: Captura cotações em tempo real via API e gera séries históricas. CONCEITOS: Integração de APIs REST, Configuração Centralizada, Persistência CSV.*
- **[global_news_sniper.py](./Agentes_Dados/global_news_sniper.py)**: (2026-01-08) | *NÍVEL 2: Agente de Inteligência de Dados FUNÇÃO: Coleta e processa notícias internacionais via RSS (Feedparser). CONCEITOS: RSS Parsing, Normalização de Dados, Persistência Estruturada.*
- **[news_sniper.py](./Agentes_Dados/news_sniper.py)**: (2026-01-08) | *NÍVEL 2: Agente de Extração de Dados FUNÇÃO: Coleta notícias de fontes globais via Web Scraping. CONCEITOS: BeautifulSoup, requests, persistência em JSON.*

### 🖥️ /Agentes_Monitor
> Monitoramento de integridade web e diagnóstico de hardware/OS.

- **[sentinela.py](./Agentes_Monitor/sentinela.py)**: (2026-01-08) | *NÍVEL 2: Sentinela de Infraestrutura FUNÇÃO: Vigia a conectividade e gerencia a rotatividade de logs do sistema. CONCEITOS: I/O de Sistema, RotatingFileHandler, Daemonize Simulation.*
- **[ssl_hunter.py](./Agentes_Monitor/ssl_hunter.py)**: (2026-01-08) | *NÍVEL 2: Auditor de Criptografia e Redes FUNÇÃO: Varredura e validação de certificados SSL/TLS em domínios externos. CONCEITOS: pyOpenSSL, Protocolos de Segurança, Persistência de Auditoria.*
- **[system_expert.py](./Agentes_Monitor/system_expert.py)**: (2026-01-08) | *NÍVEL 1: Agente de Diagnóstico de Infraestrutura FUNÇÃO: Analisa comandos Linux e gera documentação formatada para comunidades. CONCEITOS: Shell Integration, Log Parsing, Integração com API TLDR.*
- **[watchdog_sentinela.py](./Agentes_Monitor/watchdog_sentinela.py)**: (2026-01-08) | *NÍVEL 2: Watchdog (Supervisor de Resiliência) FUNÇÃO: Valida o heartbeat do Sentinela e dispara alertas visuais no Fedora. CONCEITOS: Auditoria de Heartbeat, Notificação de Sistema (GNOME), Resiliência.*
- **[web_monitor.py](./Agentes_Monitor/web_monitor.py)**: (2026-01-08) | *NÍVEL 2: Agente de Integridade de Redes FUNÇÃO: Monitora disponibilidade e latência de serviços web críticos. CONCEITOS: Socket Programming, HTTP Status Monitoring, Tempo de Resposta.*

### 👁️ /Agentes_Visao
> Processamento de imagens, filtros e remoção de metadados.

- **[vision_processor.py](./Agentes_Visao/vision_processor.py)**: (2026-01-08) | *NÍVEL 3: Processador de Visão Computacional FUNÇÃO: Higienização e formatação de fotos de perfil (LinkedIn Style). CONCEITOS: Pillow, Máscara Alpha, Organização de Data/output_images.*

### 🎙️ /Agentes_Voz
> Conversão de texto em fala (TTS) e inteligência auditiva.

- **[voice_synthesizer.py](./Agentes_Voz/voice_synthesizer.py)**: (2026-01-08) | *NÍVEL 4: Sintetizador de Inteligência Auditiva FUNÇÃO: Processamento de áudio e síntese vocal para interfaces. CONCEITOS: DSP (Digital Signal Processing), TTS (Text-to-Speech), Waveform.*

### 📜 /Scripts
> Utilitários de manutenção, backup e automação de infraestrutura.

- **[backup_toolbox.sh](./Scripts/backup_toolbox.sh)**: (2026-01-07) | *NÍVEL 1: Automação de Infraestrutura*

### ⚙️ /Config
> Cérebro do projeto (Settings, caminhos absolutos e variáveis).

- **[settings.py](./Config/settings.py)**: (2026-01-08) | *NÍVEL 1: Gestor de Ambiente e Caminhos (Versão Agentes V2) FUNÇÃO: Centraliza a inteligência de diretórios e separação por tipo de dado. CONCEITOS: Abstração de Caminhos, Configuração Centralizada, Higiene de Dados.*

### 📊 /Data
> Repositório central de entrada (input) e saída (output) de dados.

- *Pasta estruturada.*

### 📝 /Logs
> Registro de atividades e rastreabilidade de processos.

- *Pasta estruturada.*

### 📦 /Assets
> Recursos estáticos e arquivos fixos do sistema.

- *Pasta estruturada.*

---
### 🛠️ Stack Tecnológico
- **Linguagem:** Python 3.x / Bash
- **OS:** Linux (Fedora / Debian / Ubuntu)
- **Libs Principais:** `requests`, `BeautifulSoup4`, `Pillow (PIL)`, `gTTS`, `logging`.
- **Arquitetura:** Centralização de Caminhos via `Pathlib`, Persistência em JSON/CSV e Pipeline I/O.
