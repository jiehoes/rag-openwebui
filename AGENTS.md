# RAG OpenWebUI — Instruksi Inisialisasi Teknis (IIT)

Stack Docker untuk Retrieval-Augmented Generation (RAG) dengan OpenWebUI, BGE-M3 embedding, Brave Search MCP, Crawl4AI, dan Apache Tika.

## Arsitektur

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Compose Stack                  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  open-webui (:3000)          ghcr.io/open-webui  │   │
│  │  ├── DeepSeek v4-pro (LLM, API)                  │   │
│  │  ├── BGE-M3 (embedding, via Ollama :11434)       │   │
│  │  ├── BGE-Reranker-v2-M3 (sentence-transformers)  │   │
│  │  └── Brave Search MCP Tool                       │   │
│  └──────────┬───────────────────────────────────────┘   │
│             │                                           │
│  ┌──────────┴──────┐ ┌──────────┐ ┌──────────────────┐  │
│  │ mcpo (:8000)    │ │tika      │ │ crawl4ai (:11235)│  │
│  │ Brave→REST proxy│ │(:9998)   │ │ Web loader       │  │
│  └─────────────────┘ └──────────┘ └──────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  ollama (:11434)             ollama/ollama        │   │
│  │  └── bge-m3:latest (1024d embedding)             │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Clone
git clone https://github.com/jiehoes/rag-openwebui.git
cd rag-openwebui

# Setup
cp .env.example .env
# Isi BRAVE_API_KEY di .env

# Start stack
docker compose up -d

# Pull BGE-M3 embedding model
docker compose exec ollama ollama pull bge-m3

# Open
open http://localhost:3000
```

## Services

| Service | Port | Image | Fungsi |
|---------|------|-------|--------|
| open-webui | 3000 | `ghcr.io/open-webui/open-webui:main` | AI Chat + RAG |
| mcpo | 8000 | `ghcr.io/open-webui/mcpo:main` | Brave Search MCP → REST |
| tika | 9998 | `apache/tika:latest` | Document parser |
| crawl4ai | 11235 | `Dockerfile.crawl4ai` | Web crawler |
| ollama | 11434 | `ollama/ollama:latest` | Embedding server |

## Konfigurasi OpenWebUI

Setelah startup, konfigurasi via Admin Panel atau langsung DB:

### Embedding (RAG)
```
Engine:     Ollama
Model:      bge-m3:latest
Base URL:   http://ollama:11434
```

### Web Loader
```
Engine:     external
URL:        http://crawl4ai:11235/crawl
API Key:    none
```

### Web Search
```
Engine:     brave
API Key:    (dari .env BRAVE_API_KEY)
```

### Model LLM
```
Provider:   OpenAI-compatible
Base URL:   https://api.deepseek.com/v1
Model:      deepseek-v4-pro
Function Calling: Native
```

## Struktur File

```
rag-openwebui/
├── docker-compose.yml      # Stack orchestrator
├── Dockerfile.crawl4ai     # Crawl4AI custom image
├── server.py               # Crawl4AI REST wrapper
├── mcpo-config.json        # MCPO Brave Search config
├── .env.example            # Environment template
├── .gitignore
├── AGENTS.md               # This file
└── README.md               # Full documentation
```

## Catatan Penting

1. **BGE-M3 download pertama kali** — `ollama pull bge-m3` (~1.2 GB, 5-10 menit). Setelah itu tersimpan di volume `ollama-data`.

2. **GPU opsional** — `docker-compose.yml` sudah include GPU reservation. Tanpa GPU, Ollama jalan di CPU (lebih lambat).

3. **MCPO perlu Brave API key** — dapatkan di https://brave.com/search/api/. Set di `.env`.

4. **OpenWebUI DB** — tersimpan di volume `open-webui-data`. Backup dengan `docker compose cp open-webui:/app/backend/data/webui.db .`.

5. **Crawl4AI build pertama** — `docker compose build crawl4ai` (~5 menit, download Playwright + Chromium).

6. **Custom Domain** — untuk production, set `WEBUI_URL` di environment dan gunakan reverse proxy (nginx/Caddy).

## Troubleshooting

```bash
# Cek semua service
docker compose ps

# Log spesifik
docker compose logs open-webui
docker compose logs ollama

# Restart satu service
docker compose restart open-webui

# Reset total
docker compose down -v   # Hapus semua + volume!
docker compose up -d     # Start fresh
```
