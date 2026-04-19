# ORION — Claude Code Guide

## Project

ORION é um assistente de IA desktop (Electron + React + Python/FastAPI + Gemini Live API).
Ver: `.planning/PROJECT.md` para contexto completo.

## GSD Workflow

Este projeto usa GSD (Get Shit Done) para planejamento e execução.

**Planejamento atual:** `.planning/ROADMAP.md`
**Requirements:** `.planning/REQUIREMENTS.md`
**Estado:** `.planning/STATE.md`

### Antes de cada fase
```
/gsd-discuss-phase N   — coletar contexto
/gsd-plan-phase N      — criar plano detalhado
/gsd-execute-phase N   — executar o plano
```

### Fluxo YOLO (configurado)
- Auto-aprovar planos sem confirmação
- Parallelização ativada para planos independentes
- Verificação de qualidade ativada (plan_check + verifier)

## Stack

- **Frontend:** Electron + React 18 + Vite + Tailwind CSS
- **Backend:** Python 3.12 + FastAPI + WebSocket
- **AI:** Gemini Live API (`gemini-2.5-flash-native-audio-preview`)
- **Python env:** `.venv/` (detectado dinamicamente)

## Estrutura

```
src/          — React components + App.jsx
backend/      — FastAPI server + agents + tools
electron/     — Main process + preload (em breve)
.planning/    — GSD planning artifacts
```

## Comandos Comuns

```bash
npm run dev          # Inicia Electron + Vite dev server
cd backend && uvicorn server:app --reload  # Backend apenas
```

## Notas de Segurança

- `contextIsolation: false` atualmente — Phase 2 corrige isso
- Nunca hardcodar caminhos Python — usar detecção dinâmica
- Chave Gemini API em `.env` (não commitar)
