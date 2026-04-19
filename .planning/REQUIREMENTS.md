# Requirements: ORION — Milestone 2 (Sprint 2 + Sprint 3 + UX)

**Defined:** 2026-04-18
**Core Value:** ORION deve ser o assistente de voz pessoal mais capaz do desktop — controlando o PC, vendo a tela e dispositivos inteligentes em tempo real sem fricção.

## v1 Requirements

### PC Control — Acesso ao Sistema de Arquivos

- [ ] **PCSYS-01**: ORION pode listar conteúdo de um diretório (list_directory)
- [ ] **PCSYS-02**: ORION pode ler conteúdo de arquivos texto/código (read_file)
- [ ] **PCSYS-03**: ORION pode abrir arquivos com o app padrão do SO (open_file) — cross-platform Linux/Mac/Windows
- [ ] **PCSYS-04**: ORION pode abrir o browser padrão do usuário com uma URL (open_browser)

### PC Control — Controle do Sistema Operacional

- [ ] **PCOS-01**: ORION pode abrir aplicativos por nome (open_app)
- [ ] **PCOS-02**: ORION pode mover, copiar e deletar arquivos (move_file, copy_file, delete_file)
- [ ] **PCOS-03**: ORION pode controlar o volume do sistema (set_volume) — cross-platform
- [ ] **PCOS-04**: ORION pode listar processos em execução com uso de CPU/memória (list_processes)
- [ ] **PCOS-05**: ORION pode encerrar um processo por PID (kill_process)

### Security — Electron

- [ ] **SEC-01**: Electron usa contextIsolation: true com preload.js + contextBridge — elimina exposição do Node.js ao renderer
- [ ] **SEC-02**: Todas as APIs Electron expostas ao renderer passam por contextBridge com lista explícita (minimize, maximize, close, send, on)
- [ ] **SEC-03**: IPC existente (window controls, backend events) continua funcionando após migração para contextBridge

### Security — Backend

- [ ] **SEC-04**: audio_loop refatorado de singleton global para gerenciamento por sessão com cleanup adequado em desconexão/reconexão
- [ ] **SEC-05**: Multi-cliente: nova sessão WebSocket cria instância de audio_loop própria sem interferência

### UX — Status e Feedback

- [ ] **UX-01**: Barra de status (TopAudioBar) exibe indicadores semafóricos (verde/amarelo/vermelho) para: backend, modelo ativo, câmera, impressora, gestos
- [ ] **UX-02**: Indicadores de status são atualizados em tempo real via eventos do backend (WebSocket)
- [ ] **UX-03**: Layout modular persiste posições e tamanhos dos painéis no localStorage e é restaurado no mount

### UX — Interação

- [ ] **UX-04**: Push to Talk com atalho global configurável (padrão: Space) via Electron globalShortcut — funciona com janela em segundo plano

## v2 Requirements

### PC Control

- **PCOS-06**: ORION pode fazer screenshot sob demanda como tool (take_screenshot para análise pelo Gemini)
- **PCOS-07**: Controle de mouse/teclado via pyautogui para automações avançadas

### Inteligência

- **INT-01**: VAD neural com Silero — substitui threshold RMS manual por detecção de voz mais precisa
- **INT-02**: Memória vetorial com ChromaDB para busca semântica em conversas anteriores
- **INT-03**: Perfis de personalidade configuráveis via JSON — system prompt externalizado

### Features Novas

- **FEAT-01**: Painel de projetos com tree-view e preview de arquivos gerados (STL)
- **FEAT-02**: Execução de código Python pelo ORION em sandbox (subprocesso isolado, timeout 30s)
- **FEAT-03**: Notificações proativas e alarmes via scheduler assíncrono
- **FEAT-04**: Export CAD para múltiplos formatos (STEP, DXF, GLTF além de STL)
- **FEAT-05**: Drag & drop de arquivos para análise/contexto

### Integrações

- **INT-04**: Controle de lâmpadas Elgin Smart via protocolo Tuya (tinytuya)
- **INT-05**: Home Assistant REST API
- **INT-06**: Spotify Web API para controle de mídia
- **INT-07**: Google Calendar / Gmail via OAuth2

## Out of Scope

| Feature | Reason |
|---------|--------|
| Modo agente autônomo | Alta complexidade (fase 5), depende de estabilidade primeiro |
| Electron Builder / empacotamento | Útil mas não bloqueia funcionalidade atual |
| Refatoração completa do App.jsx | ~1700 linhas — refatoração parcial OK, rewrite completo não agora |
| GitHub integration | Alta complexidade, fase 6 |
| Instalador automático (install.sh) | Conveniente mas não crítico para o dev — v2 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PCSYS-01 | Phase 1 | Pending |
| PCSYS-02 | Phase 1 | Pending |
| PCSYS-03 | Phase 1 | Pending |
| PCSYS-04 | Phase 1 | Pending |
| PCOS-01 | Phase 1 | Pending |
| PCOS-02 | Phase 1 | Pending |
| PCOS-03 | Phase 1 | Pending |
| PCOS-04 | Phase 1 | Pending |
| PCOS-05 | Phase 1 | Pending |
| SEC-01 | Phase 2 | Pending |
| SEC-02 | Phase 2 | Pending |
| SEC-03 | Phase 2 | Pending |
| SEC-04 | Phase 2 | Pending |
| SEC-05 | Phase 2 | Pending |
| UX-01 | Phase 3 | Pending |
| UX-02 | Phase 3 | Pending |
| UX-03 | Phase 3 | Pending |
| UX-04 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-18*
*Last updated: 2026-04-18 after initial definition*
