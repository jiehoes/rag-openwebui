"""
Crawl4AI REST Server
POST /crawl  — Crawl URL, return markdown
GET  /health — Health check
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import asyncio
from crawl4ai import AsyncWebCrawler

PORT = 11235


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def do_POST(self):
        if self.path != "/crawl":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        url = body.get("url", "")

        async def crawl():
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url)
                return result.markdown or result.html or ""

        try:
            content = asyncio.run(crawl())
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"content": content, "url": url}).encode()
            )
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": str(e)}).encode()
            )


if __name__ == "__main__":
    print(f"Crawl4AI Server running on 0.0.0.0:{PORT}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
