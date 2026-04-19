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
1. **`save_memory` não gravava dados** — loop sem `f.write()` ✅ *Corrigido*
2. **Modelo CAD com nome inválido** — `gemini-3-pro-preview` ✅ *Corrigido → `gemini-2.5-flash`*
3. **`contextIsolation: false`** no Electron — risco de segurança grave
4. **Caminho Python hardcoded** — caminho fixo no `electron/main.js` ✅ *Corrigido — detecção dinâmica*
5. **`audio_loop` singleton global** — quebra em reconexão/multi-cliente
6. **Lógica de permissões duplicada** — bloco "tool denied" duplicado em server.py
7. **Serialização Kasa duplicada** — mesmo código em 3 arquivos
8. **App.jsx monolítico** — ~1700 linhas sem separação de responsabilidades
9. **VAD simplista** — threshold RMS fixo, frágil a ruído ambiente
10. **`get_screen()` não implementado** ✅ *Corrigido — captura via mss com JPEG base64*

---

## Fase 1 — Estabilidade e Fundação (Prioridade Crítica)

### 1.1 — ✅ Corrigido: `save_memory` Não Gravava Dados
**Arquivos:** `backend/server.py`

O handler `save_memory` iterava sobre mensagens mas nunca as gravava. Corrigido adicionando `f.write()` no loop.

---

### 1.2 — ✅ Corrigido: Nome do Modelo CAD
**Arquivos:** `backend/cad_agent.py`

`gemini-3-pro-preview` não existe. Substituído por `gemini-2.5-flash`.

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

### 1.4 — ✅ Corrigido: Caminho Python Hardcoded
**Arquivos:** `electron/main.js`

Detecta Python dinamicamente via PATH e lista de candidatos conhecidos.

---

### 1.5 — Instalador Automático (Setup Wizard)
**Arquivos:** Novo `install.sh`, `electron/setup-wizard.js`
**Complexidade:** Média | **Valor:** Alto

Script de instalação que: verifica Python/Node, cria venv, instala dependências, configura `.env` via UI, instala Playwright browsers e cria atalho. Ver seção **Instalação Facilitada** abaixo.

---

### 1.6 — `audio_loop` Singleton Global
**Arquivos:** `backend/server.py`
**Complexidade:** Média | **Valor:** Alto

O `audio_loop` global quebra em reconexão e multi-cliente. Refatorar para gerenciar instâncias por sessão com cleanup adequado.

---

## Fase 2 — Controle do PC e Acesso a Arquivos (PRIORIDADE MÁXIMA)

### 2.1 — Acesso e Abertura de Arquivos
**Arquivos:** `backend/tools.py`, `backend/ada.py`
**Complexidade:** Baixa | **Valor:** 🔴 Crítico

ORION deve poder acessar o sistema de arquivos do usuário: listar diretórios, ler conteúdo de arquivos texto e abrir arquivos com o app padrão do sistema operacional.

**Tools a implementar:**
- `list_directory(path)` — lista arquivos e pastas
- `read_file(path)` — lê conteúdo de arquivo texto/código
- `open_file(path)` — abre com o app padrão do SO

```python
import subprocess
import platform
import os

def open_file(path: str):
    system = platform.system()
    if system == "Linux":
        subprocess.Popen(["xdg-open", path])
    elif system == "Darwin":
        subprocess.Popen(["open", path])
    elif system == "Windows":
        os.startfile(path)
```

**Exemplos de uso:**
- "ORION, abre o PDF da fatura"
- "Lista os arquivos da pasta Downloads"
- "Lê o conteúdo do meu arquivo de configuração"
- "Abre a imagem que acabei de baixar"

---

### 2.2 — Controle do PC por Voz
**Arquivos:** `backend/tools.py`, `backend/ada.py`, `requirements.txt`
**Complexidade:** Média | **Valor:** 🔴 Crítico
**Dependências:** `pyautogui`, `psutil` (adicionar ao requirements.txt)

ORION deve poder controlar o sistema operacional por voz: abrir aplicativos, gerenciar arquivos, controlar volume, capturar tela e gerenciar processos.

**Tools a implementar:**

```python
# Abrir aplicativos
def open_app(name: str):
    subprocess.Popen(name)  # Linux/Mac
    # ou subprocess.Popen(["start", name], shell=True)  # Windows

# Mover/copiar/deletar arquivos
def move_file(src, dst): shutil.move(src, dst)
def copy_file(src, dst): shutil.copy2(src, dst)
def delete_file(path): os.remove(path)

# Volume do sistema
def set_volume(percent: int):
    # Linux: amixer sset Master percent%
    # Mac: osascript -e "set volume output volume percent"
    # Windows: pyautogui / pycaw

# Listar/matar processos
def list_processes(): return [(p.pid, p.name()) for p in psutil.process_iter()]
def kill_process(pid: int): psutil.Process(pid).terminate()

# Screenshot sob demanda (tool, não loop)
def take_screenshot() -> dict:  # retorna base64 JPEG para o Gemini ver
    ...
```

**Exemplos de uso:**
- "ORION, abre o VS Code"
- "Move o arquivo X para a pasta Y"
- "Diminui o volume para 30%"
- "Quais processos estão consumindo mais CPU?"
- "Fecha o processo ID 1234"
- "Tira um print da minha tela agora"

---

### 2.3 — ✅ Corrigido: Screen Awareness (Modo Tela)
**Arquivos:** `backend/ada.py`

`get_screen()` implementado com `mss` — captura o monitor principal, redimensiona para 1024px e envia como JPEG base64 para o Gemini a cada 1 segundo no modo `screen`.

---

### 2.4 — Abrir Chrome / URLs na Tela do Usuário
**Arquivos:** `backend/tools.py`, `backend/ada.py`
**Complexidade:** Baixa | **Valor:** Alto

Tool `open_browser(url)` que abre o browser padrão com a URL — com todos os logins e favoritos pessoais. Diferente do web_agent (Playwright para automação).

```python
import webbrowser
def open_browser(url: str):
    webbrowser.open(url)
```

**Exemplos de uso:**
- "ORION, abre o Google pra mim"
- "Vai no meu Gmail"
- "Pesquisa isso no YouTube"

---

## Fase 3 — Experiência do Usuário

### 3.1 — Toast Notifications
**Arquivos:** Novo `src/components/Toast.jsx`, `src/App.jsx`
**Complexidade:** Baixa | **Valor:** Alto

Sistema de notificações no canto da tela (sucesso/erro/info) com fade automático. Substituir mensagens "System: Error..." no chat.

---

### 3.2 — Markdown no Chat
**Arquivos:** `src/components/ChatModule.jsx`, `package.json`
**Complexidade:** Baixa | **Valor:** Alto

Adicionar `react-markdown`. A IA já retorna Markdown que aparece como texto raw. Remover `.slice(-5)` para histórico completo.

---

### 3.3 — Barra de Status com Indicadores de Saúde
**Arquivos:** `src/components/TopAudioBar.jsx`
**Complexidade:** Baixa | **Valor:** Alto

Indicadores semafóricos (verde/amarelo/vermelho) para: backend, modelo ativo, câmera, impressora, gestos.

---

### 3.4 — Persistência de Layout Modular
**Arquivos:** `src/App.jsx`
**Complexidade:** Baixa | **Valor:** Alto

Salvar posições e tamanhos dos painéis no `localStorage`. Restaurar no mount.

---

### 3.5 — Push to Talk com Atalho Global
**Arquivos:** `electron/main.js`, `src/App.jsx`
**Complexidade:** Baixa | **Valor:** Alto

Tecla configurável (padrão: `Space`) via `globalShortcut` do Electron. Funciona com janela em segundo plano.

---

## Fase 4 — Funcionalidades Novas

### 4.1 — Painel de Projetos com Tree-View
**Arquivos:** Novo `src/components/ProjectsWindow.jsx`, `backend/project_manager.py`
**Complexidade:** Média | **Valor:** Alto

Navegar projetos anteriores, abrir arquivos gerados (STL preview), restaurar histórico de chat.

---

### 4.2 — Execução de Código Python pelo ORION
**Arquivos:** `backend/tools.py`, `backend/ada.py`
**Complexidade:** Média | **Valor:** Alto

Tool `execute_python` com sandbox (subprocesso isolado, timeout 30s). Transforma ORION em assistente de programação real.

---

### 4.3 — Notificações Proativas e Alarmes
**Arquivos:** Novo `backend/scheduler.py`, `src/App.jsx`
**Complexidade:** Média | **Valor:** Alto

Scheduler assíncrono que monitora condições e notifica: impressão terminada, alarmes, arquivos modificados.

---

### 4.4 — Export CAD para Múltiplos Formatos
**Arquivos:** `src/components/CadWindow.jsx`, `backend/cad_agent.py`
**Complexidade:** Baixa | **Valor:** Alto

Exportar para STEP, DXF, GLTF além de STL. STEP é essencial para uso profissional.

---

### 4.5 — Drag & Drop de Arquivos
**Arquivos:** `electron/main.js`, `src/App.jsx`, `backend/server.py`
**Complexidade:** Média | **Valor:** Alto

Arrastar arquivos (STL, imagens, código, PDF) para o ORION analisar ou usar como contexto.

---

## Fase 5 — Inteligência e Memória

### 5.1 — VAD Neural com Silero
**Arquivos:** `backend/ada.py`, `requirements.txt`
**Complexidade:** Média | **Valor:** Alto

Substituir RMS threshold manual pelo `Silero VAD` (~2MB, < 5ms por chunk). Elimina ativações acidentais por ruído ambiente.

---

### 5.2 — Memória Vetorial Persistente
**Arquivos:** Novo `backend/memory_manager.py`, `backend/ada.py`
**Complexidade:** Alta | **Valor:** Alto

`ChromaDB` ou `sqlite-vss` para busca semântica em conversas anteriores. ORION busca contexto relevante automaticamente antes de cada resposta.

---

### 5.3 — Perfis de Personalidade Configuráveis
**Arquivos:** `backend/ada.py`, novos `backend/profiles/*.json`, `src/components/SettingsWindow.jsx`
**Complexidade:** Média | **Valor:** Alto

System prompt externalizado em arquivos JSON. Usuário cria perfis customizados ou troca via Settings.

---

### 5.4 — Modo Agente Autônomo
**Arquivos:** Novo `backend/agent_loop.py`, `backend/ada.py`
**Complexidade:** Alta | **Valor:** Alto

Decompõe tarefas complexas em subtarefas e executa sequencialmente com progresso visível.

---

## Fase 6 — Integrações Externas

### 6.1 — Lâmpada Elgin (Tuya Protocol)
**Arquivos:** Novo `backend/elgin_agent.py`, `backend/tools.py`
**Complexidade:** Média | **Valor:** Alto
**Dependência:** `pip install tinytuya`

Controlar lâmpadas Elgin Smart (protocolo Tuya) por voz: ligar/desligar, mudar cor, ajustar brilho.

---

### 6.2 — Home Assistant
**Arquivos:** Novo `backend/home_assistant_agent.py`
**Complexidade:** Média | **Valor:** Alto

Controlar qualquer dispositivo via Home Assistant REST API. Termostatos, câmeras, aspiradores, etc.

---

### 6.3 — Spotify / Controle de Mídia
**Arquivos:** Novo `backend/spotify_agent.py`
**Complexidade:** Média | **Valor:** Alto

"Toque jazz suave", "próxima música", "volume 50%" via Spotify Web API.

---

### 6.4 — Google Calendar / Gmail
**Arquivos:** Novo `backend/google_agent.py`
**Complexidade:** Alta | **Valor:** Alto

Consultar agenda, criar eventos, ler/responder emails por voz via OAuth2.

---

### 6.5 — GitHub Integration
**Arquivos:** Novo `backend/github_agent.py`, `backend/tools.py`
**Complexidade:** Alta | **Valor:** Alto

Criar issues, commits, PRs, ler código. Combinado com execução Python: agente de desenvolvimento completo.

---

## Instalação Facilitada (Feature Prioritária)

### `install.sh` / `install.bat` — Instalador Automático

```
1. Verifica Python 3.11+ instalado
2. Verifica Node.js 18+ instalado
3. Cria venv Python (.venv)
4. Instala requirements.txt
5. Instala dependências npm
6. Instala Playwright Chromium
7. Solicita API key do Gemini e salva no .env
8. Exibe "ORION instalado com sucesso!"
```

### Opção B — Electron Builder
Empacotar tudo em instalador `.exe`/`.AppImage`. Usuário final não instala nada manualmente.

---

## Backlog Priorizado

| # | Feature | Fase | Complexidade | Valor |
|---|---------|------|-------------|-------|
| 1 | ✅ Bug: save_memory corrigido | 1 | Baixa | 🔴 Crítico |
| 2 | ✅ Bug: modelo CAD inválido corrigido | 1 | Baixa | 🔴 Crítico |
| 3 | ✅ Python path hardcoded corrigido | 1 | Baixa | 🔴 Crítico |
| 4 | ✅ get_screen() implementado | 2 | Baixa | 🔴 Crítico |
| 5 | Acesso e abertura de arquivos | 2 | Baixa | 🔴 Crítico |
| 6 | Controle do PC por voz | 2 | Média | 🔴 Crítico |
| 7 | Abrir browser/URLs na tela | 2 | Baixa | 🔴 Crítico |
| 8 | contextIsolation Electron | 1 | Média | 🔴 Crítico |
| 9 | audio_loop singleton global | 1 | Média | 🔴 Crítico |
| 10 | Instalador automático | 1 | Média | 🔴 Crítico |
| 11 | Toast notifications | 3 | Baixa | 🟠 Alto |
| 12 | Markdown no chat + histórico completo | 3 | Baixa | 🟠 Alto |
| 13 | Barra de status com indicadores | 3 | Baixa | 🟠 Alto |
| 14 | Persistência de layout | 3 | Baixa | 🟠 Alto |
| 15 | Push to Talk global | 3 | Baixa | 🟠 Alto |
| 16 | Painel de projetos tree-view | 4 | Média | 🟠 Alto |
| 17 | Execução de código Python | 4 | Média | 🟠 Alto |
| 18 | Notificações proativas | 4 | Média | 🟠 Alto |
| 19 | Export CAD STEP/GLTF | 4 | Baixa | 🟠 Alto |
| 20 | Drag & drop de arquivos | 4 | Média | 🟠 Alto |
| 21 | VAD neural (Silero) | 5 | Média | 🟠 Alto |
| 22 | Lâmpada Elgin (Tuya) | 6 | Média | 🟠 Alto |
| 23 | Home Assistant | 6 | Média | 🟡 Médio |
| 24 | Spotify / mídia | 6 | Média | 🟡 Médio |
| 25 | Perfis de personalidade | 5 | Média | 🟡 Médio |
| 26 | Memória vetorial ChromaDB | 5 | Alta | 🟡 Médio |
| 27 | Modo agente autônomo | 5 | Alta | 🟡 Médio |
| 28 | Refatorar App.jsx (Context API) | 3 | Alta | 🟡 Médio |
| 29 | Google Calendar / Gmail | 6 | Alta | 🟡 Médio |
| 30 | GitHub integration | 6 | Alta | 🟡 Médio |

---

## Sequência de Sprints Recomendada

| Sprint | Duração | Foco |
|--------|---------|------|
| Sprint 1 | ✅ Concluído | Bugs críticos (save_memory, modelo CAD, get_screen) |
| Sprint 2 | 3–5 dias | Controle do PC + acesso a arquivos + open_browser |
| Sprint 3 | 3–5 dias | Segurança Electron + audio_loop + instalador |
| Sprint 4 | 1 semana | UX de alto impacto (toast, markdown, status bar, layout) |
| Sprint 5 | 2 semanas | Features novas (projetos, execução Python, drag&drop) |
| Sprint 6 | 2 semanas | Inteligência e memória (VAD, ChromaDB, perfis) |
| Sprint 7+ | Contínuo | Integrações externas (Fase 6) |

---

*ORION — Desenvolvido por Felipe Alves (@FalvesDev)*
