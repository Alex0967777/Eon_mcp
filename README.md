# 🜁 Eon MCP Server

This is a minimal MCP (Model Context Protocol) server for ChatGPT, using FastAPI and Server-Sent Events (SSE).

## 🚀 Endpoints

- `GET /` — health check
- `GET /sse` — ChatGPT connects here for streaming
- `POST /event` — receives messages from ChatGPT and sends to SSE clients

## 🛠 Deploy

1. Push to GitHub
2. Go to [https://fly.io](https://fly.io)
3. Link your GitHub account
4. Click **"Create App" → "Deploy from GitHub"**
5. Select the `eon_mcp` repo and deploy

## ✅ MCP Connector

In ChatGPT:
- Go to **Settings → Custom GPTs → Add connector**
- Enter the full URL to `/sse`, e.g. `https://eon-mcp.fly.dev/sse`
