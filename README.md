# RAG OpenWebUI

Setup Retrieval-Augmented Generation (RAG) di OpenWebUI dengan BGE-M3 embedding, BGE-Reranker, Crawl4AI web loader, Brave Search MCP, dan Apache Tika document parser.

## Arsitektur

```
┌─────────────────────────────────────────────────────────┐
│                   wslc Container Stack                   │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  OpenWebUI (:3000)                               │   │
│  │  ├── DeepSeek v4-pro (LLM)                       │   │
│  │  ├── BGE-M3 (Embedding, via Ollama)              │   │
│  │  ├── BGE-Reranker-v2-M3 (via sentence-transform) │   │
│  │  └── Brave Search MCP Tool                       │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────────┐ ┌──────────┐ ┌──────────┐            │
│  │ MCPO (:8000) │ │Tika(:9998│ │Crawl4AI  │            │
│  │ Brave Search │ │ Doc Parse│ │(:11235)  │            │
│  └──────────────┘ └──────────┘ └──────────┘            │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Ollama (Windows, :11434)                        │   │
│  │  └── bge-m3:latest (1024d embedding)             │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Layanan

| Service | Port | Container | Fungsi |
|---------|------|-----------|--------|
| OpenWebUI | 3000 | wslc | AI Chat + RAG |
| MCPO | 8000 | wslc | Brave Search MCP proxy |
| Tika | 9998 | wslc | Document parser |
| Crawl4AI | 11235 | wslc | Web crawler/loader |
| Ollama | 11434 | Windows | BGE-M3 embedding |

## Konfigurasi OpenWebUI

### Embedding
- **Engine**: Ollama
- **Model**: `bge-m3:latest`
- **Dimensi**: 1024

### Reranker
- **Engine**: sentence-transformers
- **Model**: `BAAI/bge-reranker-v2-m3`

### Web Search
- **Engine**: brave
- **Web Loader**: external → `http://crawl4ai:11235/crawl`

### Model
- **LLM**: DeepSeek v4-pro (via OpenAI-compatible API)
- **Function Calling**: Native

## Setup

### Prasyarat
- Windows 10/11 dengan WSL2
- [wslc](https://github.com/nousresearch/wslc) (WSL Container CLI)
- [Ollama](https://ollama.com) (Windows)

### Install

```bash
# Pull images & create containers
wslc pull ghcr.io/open-webui/open-webui:main
wslc pull ghcr.io/open-webui/mcpo:main
wslc pull apache/tika:latest

# Run containers
wslc run -d --name open-webui -p 3000:8080 \
  -v open-webui-data:/app/backend/data \
  ghcr.io/open-webui/open-webui:main

wslc run -d --name mcpo -p 8000:8000 \
  -v mcpo-config:/app/config \
  ghcr.io/open-webui/mcpo:main

wslc run -d --name tika -p 9998:9998 apache/tika:latest

wslc run -d --name crawl4ai -p 11235:11235 \
  ubuntu:latest bash -c '
    apt-get update && apt-get install -y python3 python3-pip &&
    pip3 install crawl4ai --break-system-packages &&
    crawl4ai-setup &&
    python3 -c "...server wrapper..."
  '
```

### Ollama

```bash
# Download BGE-M3
ollama pull bge-m3

# Auto-start via registry
powershell -Command "New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'Ollama' -Value '...\ollama.exe serve' -Force"
```

### Konfigurasi DB

```sql
-- Embedding via Ollama
UPDATE config SET value='"ollama"' WHERE key='rag.embedding_engine';
UPDATE config SET value='"bge-m3:latest"' WHERE key='rag.embedding_model';

-- Reranker via sentence-transformers
UPDATE config SET value='""' WHERE key='rag.reranking_engine';
UPDATE config SET value='"BAAI/bge-reranker-v2-m3"' WHERE key='rag.reranking_model';

-- Web loader
UPDATE config SET value='"http://crawl4ai:11235/crawl"' WHERE key='web.loader.external_web_loader_url';
UPDATE config SET value='"none"' WHERE key='web.loader.external_web_loader_api_key';

-- Ollama URL
UPDATE config SET value='["http://host.docker.internal:11434"]' WHERE key='ollama.base_urls';
```

## Lisensi

MIT
