# RAG OpenWebUI — Context7 Verified Configuration

Stack Docker: OpenWebUI + Ollama BGE-M3 + Brave Search MCP + Crawl4AI + Tika + Open Terminal.

## Quick Start

```bash
git clone https://github.com/jiehoes/rag-openwebui.git && cd rag-openwebui
cp .env.example .env                        # isi BRAVE_API_KEY
docker compose up -d                        # start semua
docker compose exec ollama ollama pull bge-m3
```

Buka http://localhost:9627 → **Sign up** (admin).

## Services

| Service | Port | Image |
|---------|------|-------|
| open-webui | 9627 | `ghcr.io/open-webui/open-webui:main` |
| mcpo | — | `ghcr.io/open-webui/mcpo:main` (hot-reload) |
| tika | — | `apache/tika:3.3.0.0-full` (OCR + healthcheck) |
| crawl4ai | — | `unclecode/crawl4ai:latest` |
| open-terminal | — | `ghcr.io/open-webui/open-terminal:0.11.34` |
| ollama | 11434 | `ollama/ollama:latest` (GPU reserved) |

## Environment Variables (Context7 Verified)

| Variable | Value | Source |
|----------|-------|--------|
| `OLLAMA_BASE_URLS` | `http://ollama:11434` | Official |
| `RAG_EMBEDDING_ENGINE` | `ollama` | Official |
| `RAG_EMBEDDING_MODEL` | `bge-m3:latest` | Official |
| `RAG_RERANKING_MODEL` | `BAAI/bge-reranker-v2-m3` | Official |
| `ENABLE_RAG_HYBRID_SEARCH` | `True` | Official |
| `RAG_SYSTEM_CONTEXT` | `true` | Official |
| `CONTENT_EXTRACTION_ENGINE` | `tika` | Official |
| `TIKA_SERVER_URL` | `http://tika:9998` | Official |
| `EXTERNAL_WEB_LOADER_URL` | `http://crawl4ai:11235/crawl` | Official |

## Optional: Karakeep

```bash
docker compose -f docker-compose.karakeep.yml up -d
# Bookmark manager → http://localhost:3000
```

## Troubleshooting

```bash
docker compose ps                    # status
docker compose logs open-webui       # log
docker compose down -v               # reset total
```
