# ORION — Omniscient Reasoning and Intelligent Operations Node

## What This Is

ORION é um assistente de IA desktop de alta capacidade construído sobre Electron + React + Vite no frontend e Python + FastAPI no backend. O núcleo de inteligência usa `gemini-2.5-flash-native-audio-preview` com suporte a áudio nativo em tempo real via Gemini Live API. É um projeto pessoal de Felipe Alves para automação desktop com voz, visão computacional e controle de dispositivos IoT.

## Core Value

ORION deve ser o assistente de voz pessoal mais capaz do desktop — ouvindo, vendo a tela, controlando o PC e dispositivos inteligentes, tudo em tempo real sem fricção.

## Requirements

### Validated

- ✓ Conversa por voz em tempo real bidirecional com streaming — existente
- ✓ Geração de modelos 3D CAD via build123d com retry automático — existente
- ✓ Automação web via Playwright + Gemini — existente
- ✓ Controle de dispositivos Kasa (smart home) — existente
- ✓ Impressão 3D (OctoPrint, Moonraker, PrusaLink) — existente
- ✓ Autenticação facial via MediaPipe — existente
- ✓ Controle por gestos com cursor virtual — existente
- ✓ Interface modular drag-and-drop sci-fi — existente
- ✓ Gerenciamento de projetos com histórico de conversas — existente
- ✓ Screen awareness (get_screen via mss + JPEG base64) — Sprint 1
- ✓ Toast notifications no frontend — Sprint 1
- ✓ Render Markdown no chat com histórico completo — Sprint 1

### Active

- [ ] **PC-01**: ORION pode listar, ler e abrir arquivos do sistema do usuário (list_directory, read_file, open_file)
- [ ] **PC-02**: ORION pode controlar o PC por voz (abrir apps, mover/copiar/deletar arquivos, controlar volume, gerenciar processos)
- [ ] **PC-03**: ORION pode abrir o browser padrão do usuário com uma URL (open_browser)
- [ ] **SEC-01**: Electron usa contextIsolation + contextBridge (preload.js) — elimina exposição total do Node.js
- [ ] **SEC-02**: audio_loop singleton global refatorado para gerenciamento por sessão com cleanup adequado
- [ ] **UX-01**: Barra de status com indicadores semafóricos (backend, modelo, câmera, impressora, gestos)
- [ ] **UX-02**: Persistência de layout modular no localStorage (posições e tamanhos dos painéis)
- [ ] **UX-03**: Push to Talk com atalho global configurável (padrão: Space) via globalShortcut Electron

### Out of Scope

- Memória vetorial ChromaDB — alta complexidade, fase 5, não é sprint atual
- Modo agente autônomo — fase 5, depende de estabilidade primeiro
- Integrações externas (Spotify, Google Calendar, GitHub) — fase 6, após estabilidade
- Electron Builder / empacotamento — útil mas não é prioridade agora
- VAD neural Silero — fase 5, melhoria de qualidade após estabilidade

## Context

- **Stack:** Electron + React 18 + Vite + Tailwind no frontend; Python 3.12 + FastAPI + WebSocket no backend; Gemini Live API para áudio nativo
- **Arquitetura:** App.jsx (~1700 linhas) monolítico — identificado como dívida técnica mas refatoração completa está fora do escopo atual
- **Python:** Detectado dinamicamente via PATH e lista de candidatos (`.venv/bin/python` preferido)
- **Sprint atual:** Sprint 2 (Controle do PC) + Sprint 3 (Segurança Electron + audio_loop)
- **Commits recentes:** Toast notifications + react-markdown já implementados

## Constraints

- **Tech Stack**: Python 3.12 + FastAPI + Electron — não trocar runtime
- **API**: Gemini Live API (`gemini-2.5-flash-native-audio-preview`) — chave configurada em `.env`
- **Plataforma**: Linux primário, mas tools de controle de PC devem ser cross-platform (Linux/Mac/Windows)
- **Segurança**: contextIsolation=false é risco grave conhecido — corrigir sem quebrar IPC existente

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Gemini Live API para áudio | Suporte nativo a áudio bidirecional em tempo real sem STT/TTS separados | ✓ Good |
| FastAPI + WebSocket | Streaming de áudio e eventos em tempo real com suporte assíncrono | ✓ Good |
| Electron + React + Vite | Desktop app com UI web — acesso nativo ao SO + ecossistema React | ✓ Good |
| App.jsx monolítico ~1700 linhas | Dívida técnica identificada — refatoração parcial planejada | ⚠️ Revisit |
| contextIsolation: false | Decisão inicial — risco de segurança grave, correção pendente | ⚠️ Revisit |

## Evolution

Este documento evolui em transições de fase e marcos de milestone.

**Após cada transição de fase:**
1. Requirements invalidados? → Mover para Out of Scope com motivo
2. Requirements validados? → Mover para Validated com referência de fase
3. Novos requirements emergiram? → Adicionar em Active
4. Decisões a registrar? → Adicionar em Key Decisions
5. "What This Is" ainda preciso? → Atualizar se derivou

**Após cada milestone:**
1. Revisão completa de todas as seções
2. Core Value check — ainda é a prioridade certa?
3. Auditar Out of Scope — motivos ainda válidos?
4. Atualizar Context com estado atual

---
*Last updated: 2026-04-18 after initialization*
