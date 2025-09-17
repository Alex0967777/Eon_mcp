# 🜁 Eon MCP Server (v2)

FastAPI MCP server for ChatGPT.

## Endpoints
- GET `/` → health check
- GET `/sse` → ChatGPT SSE stream
- POST `/event` → receive message and push to stream

## Deploy on Fly.io
Uses `Dockerfile` with `EXPOSE 8080` and `fly.toml`.

## Run locally
```bash
docker build -t eon_mcp .
docker run -p 8080:8080 eon_mcp
```
