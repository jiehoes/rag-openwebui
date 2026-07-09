# RAG OpenWebUI

Stack Docker: OpenWebUI + BGE-M3 + Brave Search + Crawl4AI + Tika.

## Quick Start

```bash
git clone https://github.com/jiehoes/rag-openwebui.git
cd rag-openwebui
cp .env.example .env          # isi BRAVE_API_KEY

docker compose up -d          # start semua
docker compose exec ollama ollama pull bge-m3   # download embedding model
```

Buka http://localhost:3000

## Services

| Service | Port | Fungsi |
|---------|------|--------|
| open-webui | 3000 | AI Chat + RAG |
| mcpo | 8000 | Brave Search proxy |
| tika | 9998 | Document parser |
| crawl4ai | 11235 | Web crawler |
| ollama | 11434 | BGE-M3 embedding |

## Konfigurasi OpenWebUI

| Setting | Value |
|---------|-------|
| LLM | DeepSeek v4-pro (`api.deepseek.com/v1`) |
| Embedding | Ollama → `bge-m3:latest` |
| Web Search | brave |
| Web Loader | external → `http://crawl4ai:11235/crawl` |
| Function Calling | Native |

## Troubleshooting

```bash
docker compose ps              # status
docker compose logs open-webui # log
docker compose down -v         # reset total
```
