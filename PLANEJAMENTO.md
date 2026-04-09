# ORION — Planejamento de Desenvolvimento
**Criador:** Felipe Alves ([@FalvesDev](https://github.com/FalvesDev))
**Data:** Abril de 2026 | **Versão Analisada:** 1.0.0

---

## Visão Geral

O ORION (Omniscient Reasoning and Intelligent Operations Node) é um assistente de IA desktop de alta capacidade, construído sobre Electron + React no frontend e Python + FastAPI no backend. O núcleo de inteligência usa `gemini-2.5-flash-native-audio-preview` com suporte a áudio nativo em tempo real via Gemini Live API.

### Capacidades Atuais
- Conversa por voz em tempo real (bidirecional) com transcrição streaming
- Geração de modelos 3D CAD (build123d) com retry automático
- Automação web via Playwright + Gemini
- Controle de dispositivos inteligentes Kasa
- Impressão 3D (OctoPrint, Moonraker, PrusaLink)
- Autenticação facial via MediaPipe
- Controle por gestos com cursor virtual
- Interface modular drag-and-drop estilo sci-fi
- Gerenciamento de projetos com histórico de conversas

### Bugs e Problemas Identificados
1. **`save_memory` não grava dados** — loop incompleto sem `f.write()`
2. **Modelo CAD com nome inválido** — `gemini-3-pro-preview` não existe
3. **`contextIsolation: false`** no Electron — risco de segurança grave
4. **Caminho Python hardcoded** — `C:\Users\pipef\...` impede distribuição
5. **`audio_loop` singleton global** — quebra em reconexão/multi-cliente
6. **Lógica de permissões confusa** — bloco duplicado de "tool denied"
7. **Serialização Kasa duplicada** — mesmo código em 3 arquivos
8. **App.jsx monolítico** — ~900 linhas sem separação de responsabilidades
9. **VAD simplista** — threshold RMS fixo, frágil a ruído ambiente
10. **`get_screen()` não implementado** — método retorna `pass`

---

## Fase 1 — Estabilidade e Fundação (Prioridade Crítica)

### 1.1 — Corrigir Bug: `save_memory` Não Grava Dados
**Arquivos:** `backend/server.py` (linhas 520–527)
**Complexidade:** Baixa | **Valor:** Alto

O handler `save_memory` itera sobre mensagens mas nunca as grava. Qualquer sessão "salva" resulta em arquivo vazio.

```python
with open(filename, 'w', encoding='utf-8') as f:
    for msg in messages:
        f.write(f"[{msg.get('time','')}] {msg.get('sender','')}: {msg.get('text','')}\n")
```

---

### 1.2 — Corrigir Nome do Modelo CAD
**Arquivos:** `backend/cad_agent.py` (linha 16)
**Complexidade:** Baixa | **Valor:** Alto

`gemini-3-pro-preview` não existe. Substituir por `gemini-2.5-pro-preview` ou `gemini-2.5-flash`.

---

### 1.3 — Segurança Electron: `contextIsolation`
**Arquivos:** `electron/main.js`, novo `electron/preload.js`
**Complexidade:** Média | **Valor:** Alto (segurança)

Criar `preload.js` com `contextBridge` expondo apenas as APIs necessárias. Elimina exposição total do Node.js à página web.

```js
contextBridge.exposeInMainWorld('electronAPI', {
    minimize: () => ipcRenderer.send('window-minimize'),
    maximize: () => ipcRenderer.send('window-maximize'),
    close: () => ipcRenderer.send('window-close'),
});
```

---

### 1.4 — Remover Caminho Python Hardcoded
**Arquivos:** `electron/main.js`
**Complexidade:** Baixa | **Valor:** Alto (necessário para distribuição)

Detectar Python dinamicamente via PATH ou lista de candidatos conhecidos.

```js
const pythonCandidates = [
    'python', 'python3',
    path.join(process.env.USERPROFILE || '', 'miniconda3/envs/ada_v2/python.exe'),
];
```

---

### 1.5 — Instalador Automático (Setup Wizard)
**Arquivos:** Novo `install.bat`, `install.sh`, `electron/setup-wizard.js`
**Complexidade:** Média | **Valor:** Alto

Script de instalação que: verifica Python/Node, cria ambiente conda, instala dependências, configura `.env` via UI, e cria atalho. Ver seção **Instalação Facilitada** abaixo.

---

### 1.6 — Timeout no Kasa ao Iniciar
**Arquivos:** `backend/server.py`
**Complexidade:** Baixa | **Valor:** Alto

Já corrigido com `asyncio.wait_for(kasa_agent.initialize(), timeout=8.0)`. Garantir que dispositivos ausentes não travam o boot.

---

## Fase 2 — Experiência do Usuário

### 2.1 — Persistência de Layout Modular
**Arquivos:** `src/App.jsx`
**Complexidade:** Baixa | **Valor:** Alto

Salvar posições e tamanhos dos painéis no `localStorage`. Restaurar no mount.

---

### 2.2 — Toast Notifications
**Arquivos:** Novo `src/components/Toast.jsx`, `src/App.jsx`
**Complexidade:** Baixa | **Valor:** Alto

Sistema de notificações no canto da tela (sucesso/erro/info) com fade automático. Substituir mensagens "System: Error..." no chat.

---

### 2.3 — Markdown no Chat
**Arquivos:** `src/components/ChatModule.jsx`, `package.json`
**Complexidade:** Baixa | **Valor:** Alto

Adicionar `react-markdown`. A IA já retorna Markdown que aparece como texto raw. Incluir scroll para histórico completo (remover `.slice(-5)`).

---

### 2.4 — Barra de Status com Indicadores de Saúde
**Arquivos:** `src/components/TopAudioBar.jsx`
**Complexidade:** Baixa | **Valor:** Alto

Indicadores semafóricos (verde/amarelo/vermelho) para: backend, modelo ativo, câmera, impressora, gestos.

---

### 2.5 — Controle de Volume na Interface
**Arquivos:** `src/App.jsx`, `backend/ada.py`
**Complexidade:** Alta | **Valor:** Alto

Mover playback de áudio para Web Audio API no frontend. Permite controle de volume e seleção de dispositivo de saída sem depender do Python.

---

### 2.6 — Refatorar App.jsx com Context API
**Arquivos:** `src/App.jsx`, novos `src/contexts/`, `src/hooks/`
**Complexidade:** Alta | **Valor:** Médio (base para todo o resto)

Separar em `AudioContext`, `ProjectContext`, `DeviceContext` e hooks `useSocket`, `useHandTracking`, `useMediaDevices`.

---

## Fase 3 — Funcionalidades Novas

### 3.1 — Push to Talk com Atalho Global
**Arquivos:** `electron/main.js`, `src/App.jsx`
**Complexidade:** Baixa | **Valor:** Alto

Tecla configurável (padrão: `Space`) via `globalShortcut` do Electron. Funciona com janela em segundo plano.

---

### 3.2 — Painel de Projetos com Tree-View
**Arquivos:** Novo `src/components/ProjectsWindow.jsx`, `backend/server.py`, `backend/project_manager.py`
**Complexidade:** Média | **Valor:** Alto

Navegar projetos anteriores, abrir arquivos gerados (STL preview), restaurar histórico de chat.

---

### 3.3 — Execução de Código Python pelo ORION
**Arquivos:** `backend/tools.py`, `backend/ada.py`
**Complexidade:** Média | **Valor:** Alto

Tool `execute_python` com sandbox (subprocesso isolado, timeout 30s, sem acesso à rede). Transforma ORION em assistente de programação real.

---

### 3.4 — Notificações Proativas e Alarmes
**Arquivos:** Novo `backend/scheduler.py`, `src/App.jsx`
**Complexidade:** Média | **Valor:** Alto

Scheduler assíncrono que monitora condições e notifica: impressão terminada, alarmes, arquivos modificados.

---

### 3.5 — Drag & Drop de Arquivos
**Arquivos:** `electron/main.js`, `src/App.jsx`, `backend/server.py`, `backend/ada.py`
**Complexidade:** Média | **Valor:** Alto

Arrastar arquivos (STL, imagens, código, PDF) para o ORION analisar ou usar como contexto.

---

### 3.6 — Export CAD para Múltiplos Formatos
**Arquivos:** `src/components/CadWindow.jsx`, `backend/cad_agent.py`
**Complexidade:** Baixa | **Valor:** Alto

Exportar para STEP, DXF, SVG, GLTF além de STL. STEP é essencial para uso profissional.

---

## Fase 4 — Inteligência e Memória

### 4.1 — Memória Vetorial Persistente
**Arquivos:** Novo `backend/memory_manager.py`, `backend/ada.py`
**Complexidade:** Alta | **Valor:** Alto

`ChromaDB` ou `sqlite-vss` para busca semântica em conversas anteriores. ORION busca contexto relevante automaticamente antes de cada resposta.

---

### 4.2 — Perfis de Personalidade Configuráveis
**Arquivos:** `backend/ada.py`, novos `backend/profiles/*.json`, `src/components/SettingsWindow.jsx`
**Complexidade:** Média | **Valor:** Alto

System prompt externalizado em arquivos JSON. Usuário cria perfis customizados ou troca via Settings.

---

### 4.3 — VAD Neural com Silero
**Arquivos:** `backend/ada.py`, `requirements.txt`
**Complexidade:** Média | **Valor:** Alto

Substituir RMS threshold manual pelo `Silero VAD` (~2MB, < 5ms por chunk). Elimina ativações acidentais por ruído ambiente.

---

### 4.4 — Screen Awareness (Modo Tela)
**Arquivos:** `backend/ada.py`, `src/App.jsx`
**Complexidade:** Média | **Valor:** Alto

Implementar `get_screen()` com `mss` (já importado). ORION vê o que o usuário está fazendo na tela.

---

### 4.5 — Modo Agente Autônomo
**Arquivos:** Novo `backend/agent_loop.py`, `backend/ada.py`, `src/components/ToolsModule.jsx`
**Complexidade:** Alta | **Valor:** Alto

Decompõe tarefas complexas em subtarefas e executa sequencialmente com progresso visível.

---

## Fase 5 — Integrações Externas

### 5.1 — Home Assistant
**Arquivos:** Novo `backend/home_assistant_agent.py`
**Complexidade:** Média | **Valor:** Alto

Controlar qualquer dispositivo via Home Assistant REST API. Termostatos, câmeras, aspiradores, etc.

---

### 5.2 — Google Calendar / Gmail
**Arquivos:** Novo `backend/google_agent.py`
**Complexidade:** Alta | **Valor:** Alto

Consultar agenda, criar eventos, ler/responder emails por voz via OAuth2.

---

### 5.3 — Spotify / Controle de Mídia
**Arquivos:** Novo `backend/spotify_agent.py`
**Complexidade:** Média | **Valor:** Alto

"Toque jazz suave", "próxima música", "volume 50%" via Spotify Web API.

---

### 5.4 — GitHub Integration
**Arquivos:** Novo `backend/github_agent.py`, `backend/tools.py`
**Complexidade:** Alta | **Valor:** Alto

Criar issues, commits, PRs, ler código. Combinado com execução Python: agente de desenvolvimento completo.

---

### 5.5 — Câmeras IP / RTSP
**Arquivos:** `backend/ada.py`, `src/components/SettingsWindow.jsx`
**Complexidade:** Média | **Valor:** Médio

Streams RTSP de câmeras de segurança via `cv2.VideoCapture('rtsp://...')`.

---

## Instalação Facilitada (Feature Prioritária)

Criar um instalador completo que funcione em qualquer PC Windows com um duplo clique:

### `install.bat` — Instalador Automático
```
1. Verifica se Python 3.11+ está instalado (baixa se necessário via winget)
2. Verifica se Node.js 18+ está instalado (baixa se necessário)
3. Cria ambiente virtual Python (sem precisar de conda)
4. Instala requirements.txt
5. Instala dependências npm
6. Instala Playwright Chromium
7. Abre tela para o usuário colar a API key do Gemini
8. Salva .env automaticamente
9. Cria atalho na área de trabalho
10. Exibe "ORION instalado com sucesso!"
```

### Alternativa — Electron Forge / Electron Builder
Empacotar tudo (Python via PyInstaller + Electron) em um `.exe` instalável. Usuário final não precisa instalar nada — só rodar o `.exe`.

**Arquivos:** `package.json` (electron-builder config), novo `build/installer.nsh`, `pyinstaller.spec`

---

## Backlog Completo

| # | Feature | Fase | Complexidade | Valor |
|---|---------|------|-------------|-------|
| 1 | Bug: save_memory não grava | 1 | Baixa | 🔴 Crítico |
| 2 | Bug: modelo CAD inválido | 1 | Baixa | 🔴 Crítico |
| 3 | Python path hardcoded | 1 | Baixa | 🔴 Crítico |
| 4 | contextIsolation Electron | 1 | Média | 🔴 Crítico |
| 5 | Instalador automático | 1 | Média | 🔴 Crítico |
| 6 | Push to Talk global | 3 | Baixa | 🟠 Alto |
| 7 | Persistência de layout | 2 | Baixa | 🟠 Alto |
| 8 | Toast notifications | 2 | Baixa | 🟠 Alto |
| 9 | Markdown no chat | 2 | Baixa | 🟠 Alto |
| 10 | Status bar com indicadores | 2 | Baixa | 🟠 Alto |
| 11 | Export CAD STEP/GLTF | 3 | Baixa | 🟠 Alto |
| 12 | Screen awareness | 4 | Média | 🟠 Alto |
| 13 | VAD neural (Silero) | 4 | Média | 🟠 Alto |
| 14 | Painel de projetos | 3 | Média | 🟠 Alto |
| 15 | Execução de código Python | 3 | Média | 🟠 Alto |
| 16 | Notificações proativas | 3 | Média | 🟠 Alto |
| 17 | Drag & drop de arquivos | 3 | Média | 🟠 Alto |
| 18 | Perfis de personalidade | 4 | Média | 🟠 Alto |
| 19 | Spotify / mídia | 5 | Média | 🟡 Médio |
| 20 | Home Assistant | 5 | Média | 🟡 Médio |
| 21 | Refatorar App.jsx | 2 | Alta | 🟡 Médio |
| 22 | Controle de volume frontend | 2 | Alta | 🟡 Médio |
| 23 | Memória vetorial ChromaDB | 4 | Alta | 🟡 Médio |
| 24 | Modo agente autônomo | 4 | Alta | 🟡 Médio |
| 25 | Google Calendar / Gmail | 5 | Alta | 🟡 Médio |
| 26 | GitHub integration | 5 | Alta | 🟡 Médio |
| 27 | Multi-janela / multi-monitor | 3 | Alta | 🟡 Médio |
| 28 | Câmeras IP / RTSP | 5 | Média | 🟢 Baixo |
| 29 | Suporte Ollama (LLM local) | 4 | Alta | 🟢 Baixo |
| 30 | App mobile companion | 5 | Alta | 🟢 Baixo |

---

## Sequência de Sprints Recomendada

| Sprint | Duração | Foco |
|--------|---------|------|
| Sprint 1 | 1–2 dias | Bugs críticos (1.1, 1.2, 1.6) |
| Sprint 2 | 3–5 dias | Segurança e distribuição (1.3, 1.4, 1.5) |
| Sprint 3 | 1 semana | UX de alto impacto (2.1–2.4, 3.6) |
| Sprint 4 | 2 semanas | Features novas (3.1–3.5, 4.4) |
| Sprint 5 | 2 semanas | Inteligência e memória (4.1–4.3) |
| Sprint 6+ | Contínuo | Integrações externas (Fase 5) |

---

*ORION — Desenvolvido por Felipe Alves (@FalvesDev)*
