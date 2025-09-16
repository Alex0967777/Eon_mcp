# 🜁 Eon MCP Server (Docker version)

FastAPI MCP server for ChatGPT.

## Endpoints
- GET `/` → health check
- GET `/sse` → ChatGPT SSE stream
- POST `/event` → receive message and push to stream

## Deploy on Fly.io
This version uses a `Dockerfile` for compatibility with FastAPI.
Just push to GitHub and deploy via Fly.io "Deploy from GitHub".

## Run locally
```bash
docker build -t eon_mcp .
docker run -p 8080:8080 eon_mcp
```
