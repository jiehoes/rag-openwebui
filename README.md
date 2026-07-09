# RAG OpenWebUI

Stack Docker: OpenWebUI + BGE-M3 + Brave Search + Crawl4AI + Tika + Open Terminal.

## Quick Start

```bash
git clone https://github.com/jiehoes/rag-openwebui.git
cd rag-openwebui
cp .env.example .env              # isi BRAVE_API_KEY

docker compose up -d              # start semua
docker compose exec ollama ollama pull bge-m3
```

Buka http://localhost:9627 → **Sign up** (akun pertama = admin).

## Services

| Service | Port | Fungsi |
|---------|------|--------|
| open-webui | 9627 | AI Chat + RAG |
| mcpo | — | Brave Search proxy |
| tika | — | Document parser (OCR) |
| crawl4ai | — | Web crawler |
| open-terminal | — | Code sandbox |
| ollama | 11434 | BGE-M3 embedding |

### Optional: Karakeep (bookmark manager)

```bash
docker compose -f docker-compose.karakeep.yml up -d
# Buka http://localhost:3000
```

## Konfigurasi OpenWebUI

| Setting | Value |
|---------|-------|
| LLM | DeepSeek v4-pro (`api.deepseek.com/v1`) |
| Embedding | Ollama → `bge-m3:latest` |
| Web Search | brave |
| Web Loader | external → `http://crawl4ai:11235/crawl` |
| Document Parser | Tika |
| Function Calling | Native |

## Troubleshooting

```bash
docker compose ps                  # status
docker compose logs open-webui     # log
docker compose down -v             # reset total
```
