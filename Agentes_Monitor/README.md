# 📁 Módulo: Agentes_Monitor

> Monitoramento de sistema, rede e hardware.

## 🧰 Estrutura e Ferramentas
- 🐍 **[sentinela.py](./sentinela.py)** (2026-01-08) | *NÍVEL 2: Sentinela de Infraestrutura FUNÇÃO: Vigia a conectividade e gerencia a rotatividade de logs do sistema. CONCEITOS: I/O de Sistema, RotatingFileHandler, Daemonize Simulation.*
- 🐍 **[ssl_hunter.py](./ssl_hunter.py)** (2026-01-08) | *NÍVEL 2: Auditor de Criptografia e Redes FUNÇÃO: Varredura e validação de certificados SSL/TLS em domínios externos. CONCEITOS: pyOpenSSL, Protocolos de Segurança, Persistência de Auditoria.*
- 🐍 **[system_expert.py](./system_expert.py)** (2026-01-08) | *NÍVEL 1: Agente de Diagnóstico de Infraestrutura FUNÇÃO: Analisa comandos Linux e gera documentação formatada para comunidades. CONCEITOS: Shell Integration, Log Parsing, Integração com API TLDR.*
- 🐍 **[watchdog_sentinela.py](./watchdog_sentinela.py)** (2026-01-08) | *NÍVEL 2: Watchdog (Supervisor de Resiliência) FUNÇÃO: Valida o heartbeat do Sentinela e dispara alertas visuais no Fedora. CONCEITOS: Auditoria de Heartbeat, Notificação de Sistema (GNOME), Resiliência.*
- 🐍 **[web_monitor.py](./web_monitor.py)** (2026-01-08) | *NÍVEL 2: Agente de Integridade de Redes FUNÇÃO: Monitora disponibilidade e latência de serviços web críticos. CONCEITOS: Socket Programming, HTTP Status Monitoring, Tempo de Resposta.*