# RAG OpenWebUI — Context7 Verified Configuration

Stack Docker: OpenWebUI + Ollama BGE-M3 + Brave Search + Crawl4AI + Tika.

## Quick Start

```bash
git clone https://github.com/jiehoes/rag-openwebui.git && cd rag-openwebui
cp .env.example .env                        # isi BRAVE_API_KEY
docker compose up -d                        # start semua
docker compose exec ollama ollama pull bge-m3  # download embedding
```

Buka http://localhost:9627

## Services

| Service | Port | Image |
|---------|------|-------|
| open-webui | 9627 | `ghcr.io/open-webui/open-webui:main` |
| mcpo | 8000 | `ghcr.io/open-webui/mcpo:main` |
| tika | 9998 | `apache/tika:latest` |
| crawl4ai | 11235 | `unclecode/crawl4ai:latest` |
| ollama | 11434 | `ollama/ollama:latest` |

## Environment Variables (Context7 Verified)

| Variable | Value | Doc Ref |
|----------|-------|---------|
| `OLLAMA_BASE_URLS` | `http://ollama:11434` | [Quick Start](https://docs.openwebui.com/getting-started/quick-start) |
| `RAG_EMBEDDING_ENGINE` | `ollama` | [Performance](https://docs.openwebui.com/troubleshooting/performance) |
| `RAG_EMBEDDING_MODEL` | `bge-m3:latest` | [Env Config](https://docs.openwebui.com/reference/env-configuration) |
| `RAG_RERANKING_MODEL` | `BAAI/bge-reranker-v2-m3` | [Env Config](https://docs.openwebui.com/reference/env-configuration) |
| `EXTERNAL_WEB_LOADER_URL` | `http://crawl4ai:11235/crawl` | [Env Config](https://docs.openwebui.com/reference/env-configuration) |

## Konfigurasi OpenWebUI

Setelah startup, tambahkan di Admin Panel:

| Setting | Value |
|---------|-------|
| LLM Provider | OpenAI-compatible → `https://api.deepseek.com/v1` |
| LLM Model | `deepseek-v4-pro` |
| Function Calling | Native |
| Web Search Engine | brave |

## Troubleshooting

```bash
docker compose ps                    # status
docker compose logs open-webui       # log
docker compose down -v               # reset total
```
