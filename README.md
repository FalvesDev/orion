# ORION — Omniscient Reasoning and Intelligent Operations Node

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/React-18.2-61DAFB?logo=react" alt="React">
  <img src="https://img.shields.io/badge/Electron-28-47848F?logo=electron" alt="Electron">
  <img src="https://img.shields.io/badge/Google%20Gemini-2.5%20Native%20Audio-4285F4?logo=google" alt="Gemini">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

<p align="center">
  <strong>Um assistente de IA avançado para desktop — rápido, composto, e inegavelmente vivo.</strong><br>
  <em>Desenvolvido por <a href="https://github.com/FalvesDev">Felipe Alves</a></em>
</p>

---

ORION é um assistente pessoal de IA de alto desempenho rodando localmente como aplicativo desktop. Combina voz em tempo real via Google Gemini 2.5, geração de modelos CAD 3D, automação web, controle de dispositivos inteligentes e rastreamento de gestos — tudo em uma interface estilo sci-fi.

> **Origem:** ORION é uma evolução do projeto A.D.A, criado originalmente por [Nazir Louis](https://github.com/nazirlouis/ada_v2). Esta versão foi completamente reformulada com nova personalidade, novas funcionalidades e arquitetura aprimorada.

---

## Capacidades

| Funcionalidade | Descrição | Tecnologia |
|---|---|---|
| **Voz em Tempo Real** | Conversa bidirecional com baixa latência e interrupt handling | Gemini 2.5 Native Audio |
| **CAD 3D Paramétrico** | Gera modelos 3D editáveis por comando de voz | `build123d` → STL |
| **Impressão 3D** | Fatiamento e envio sem fio para impressoras | OrcaSlicer + Moonraker/OctoPrint |
| **Interface por Gestos** | Controle de janelas com rastreamento de mãos | MediaPipe Hand Tracking |
| **Autenticação Facial** | Login biométrico local e seguro | MediaPipe Face Landmarker |
| **Agente Web** | Automação autônoma do navegador | Playwright + Chromium |
| **Casa Inteligente** | Controle por voz de dispositivos Kasa | `python-kasa` |
| **Memória de Projetos** | Contexto persistente entre sessões | JSON file-based storage |

---

## Arquitetura

```
┌─────────────────────────────────────────┐
│          Frontend (Electron + React)     │
│  React UI · Three.js · MediaPipe        │
│  Socket.IO Client                       │
└──────────────┬──────────────────────────┘
               │ WebSocket
┌──────────────▼──────────────────────────┐
│          Backend (Python 3.11)           │
│  server.py  →  FastAPI + Socket.IO       │
│  ada.py     →  Gemini Live API           │
│  web_agent  →  Playwright Browser        │
│  cad_agent  →  build123d CAD             │
│  kasa_agent →  Smart Home                │
│  printer    →  3D Printing               │
└─────────────────────────────────────────┘
```

---

## Instalação

### Pré-requisitos

- **Python 3.11** via [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- **Node.js 18+** via [nodejs.org](https://nodejs.org/)
- **Git** via [git-scm.com](https://git-scm.com/)
- Chave de API do **Google Gemini** via [aistudio.google.com](https://aistudio.google.com/app/apikey)

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/FalvesDev/orion.git
cd orion
```

**2. Crie o ambiente Python**
```bash
conda create -n ada_v2 python=3.11 -y
conda activate ada_v2
pip install -r requirements.txt
playwright install chromium
```

**3. Instale as dependências do frontend**
```bash
npm install
```

**4. Configure a API key**

Crie um arquivo `.env` na raiz do projeto:
```
GEMINI_API_KEY=sua_chave_aqui
```
> Nunca commite o arquivo `.env`. Ele já está no `.gitignore`.

**5. Execute**
```bash
conda activate ada_v2
npm run dev
```

---

## Configuração (`settings.json`)

O arquivo `backend/settings.json` é criado automaticamente na primeira execução. Principais opções:

| Chave | Tipo | Descrição |
|---|---|---|
| `face_auth_enabled` | `bool` | Exige reconhecimento facial para desbloquear o assistente |
| `tool_permissions.generate_cad` | `bool` | Requer confirmação antes de gerar modelos 3D |
| `tool_permissions.run_web_agent` | `bool` | Requer confirmação antes de abrir o agente web |
| `tool_permissions.write_file` | `bool` | Requer confirmação antes de escrever arquivos em disco |
| `kasa_devices` | `list` | Lista de dispositivos Kasa com IP, nome e apelido |

---

## Autenticação Facial (opcional)

1. Tire uma foto clara do seu rosto.
2. Renomeie para `reference.jpg`.
3. Coloque o arquivo em `backend/reference.jpg`.
4. No `settings.json`, mude `face_auth_enabled` para `true`.

---

## Impressora 3D (opcional)

ORION suporta **Klipper/Moonraker**, **OctoPrint** e **PrusaLink**.

1. Instale o [OrcaSlicer](https://github.com/SoftFever/OrcaSlicer) e execute uma vez.
2. Certifique-se que a impressora e o PC estão na mesma rede Wi-Fi.
3. O ORION detecta impressoras automaticamente via mDNS.
4. Para conexão manual, adicione o IP em **Settings → Printers**.

---

## Gestos Suportados

| Gesto | Ação |
|---|---|
| Pinça | Confirmar / clicar |
| Palma aberta | Soltar janela |
| Punho fechado | Segurar e arrastar janela |

---

## Estrutura do Projeto

```
orion/
├── backend/                    # Servidor Python e lógica de IA
│   ├── ada.py                  # Integração com Gemini Live API
│   ├── server.py               # FastAPI + Socket.IO
│   ├── cad_agent.py            # Geração de modelos CAD
│   ├── printer_agent.py        # Descoberta e fatiamento 3D
│   ├── web_agent.py            # Automação com Playwright
│   ├── kasa_agent.py           # Controle de casa inteligente
│   ├── authenticator.py        # Autenticação facial
│   ├── project_manager.py      # Gerenciamento de projetos
│   └── tools.py                # Definição de ferramentas para o Gemini
├── src/                        # Frontend React
│   ├── App.jsx                 # Componente principal
│   ├── components/             # Componentes de UI
│   └── index.css               # Estilos globais
├── electron/                   # Processo principal Electron
│   └── main.js                 # Janelas e IPC
├── .env                        # Chaves de API (crie este arquivo!)
├── requirements.txt            # Dependências Python
├── package.json                # Dependências Node.js
├── PLANEJAMENTO.md             # Roadmap completo de desenvolvimento
└── README.md                   # Este arquivo
```

---

## Roadmap

O desenvolvimento futuro do ORION está documentado em detalhes no [PLANEJAMENTO.md](PLANEJAMENTO.md). Resumo das fases:

| Fase | Foco | Status |
|---|---|---|
| **Fase 1** | Estabilidade — bugs críticos, segurança Electron, instalador | Planejado |
| **Fase 2** | UX — persistência de layout, toast notifications, markdown no chat | Planejado |
| **Fase 3** | Novas features — push-to-talk, painel de projetos, abrir Chrome, execução de código | Planejado |
| **Fase 4** | Inteligência — memória vetorial, VAD neural, screen awareness, modo agente autônomo | Planejado |
| **Fase 5** | Integrações — Home Assistant, Google Calendar, Spotify, GitHub, lâmpadas Tuya | Planejado |

---

## Solução de Problemas

**`GEMINI_API_KEY` não encontrada**
- Verifique se o `.env` está na raiz do projeto (não dentro de `backend/`).
- Formato correto: `GEMINI_API_KEY=sua_chave` (sem aspas, sem espaços).

**Erro de conexão WebSocket (1011)**
- Problema temporário da API Gemini. Clique em reconectar ou aguarde alguns segundos.

**Camera sem permissão (macOS)**
- Vá em **Preferências do Sistema → Privacidade → Câmera** e autorize o terminal.

**App não abre / ERR_CONNECTION_REFUSED**
- Certifique-se de usar `npm run dev` (não `npx electron .` diretamente), pois ele inicia o Vite e o Electron juntos.

---

## Segurança

| Aspecto | Implementação |
|---|---|
| Chaves de API | Armazenadas em `.env`, nunca commitadas |
| Dados faciais | Processados localmente, nunca enviados |
| Confirmação de ferramentas | Ações destrutivas requerem aprovação do usuário |
| Sem armazenamento em nuvem | Todos os dados de projeto ficam no seu computador |

---

## Licença

Este projeto está licenciado sob a **MIT License** — veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## Créditos

- **Felipe Alves ([@FalvesDev](https://github.com/FalvesDev))** — Criador e mantenedor do ORION
- **Nazir Louis ([@nazirlouis](https://github.com/nazirlouis))** — Criador do projeto original A.D.A, base sobre a qual o ORION foi construído
- **[Google Gemini](https://deepmind.google/technologies/gemini/)** — API de áudio nativo em tempo real
- **[build123d](https://github.com/gumyr/build123d)** — Biblioteca CAD paramétrica moderna
- **[MediaPipe](https://developers.google.com/mediapipe)** — Rastreamento de mãos, gestos e autenticação facial
- **[Playwright](https://playwright.dev/)** — Automação de navegador confiável

---

<p align="center">
  <strong>ORION — Desenvolvido por <a href="https://github.com/FalvesDev">Felipe Alves</a></strong><br>
  <em>Inteligência. Voz. Controle. Tudo em um.</em>
</p>
