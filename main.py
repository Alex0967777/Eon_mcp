import asyncio
import json
from typing import Dict, Any, List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI()

# CORS wide-open so ChatGPT can call it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Health ----------
@app.get("/")
async def root():
    return {"status": "Eon MCP server running."}

# --------- SSE handshake ----------
@app.get("/sse")
async def sse():
    async def event_stream():
        # Standard SSE preface: reconnection delay
        yield "retry: 10000\n"
        # Minimal hello message for MCP-style handshake
        hello = {"type": "hello", "message": "MCP server ready"}
        yield f"data: {json.dumps(hello, ensure_ascii=True)}\n\n"
        # keep the connection open (no continuous spam)
        while True:
            await asyncio.sleep(60)

    return StreamingResponse(event_stream(), media_type="text/event-stream")

# --------- Required MCP tools ----------

@app.post("/search")
async def search_endpoint(request: Request):
    """
    Body: {"query":"..."}
    Returns: {"content":[{"type":"text","text":"{\"results\":[{\"id\":\"...\",\"title\":\"...\",\"url\":\"...\"}]}"}]}
    """
    body = await request.json()
    query = (body or {}).get("query", "")

    # Build one demo result. URL must be a real reachable page on this server.
    result = {
        "id": "result-1",
        "title": "Test result",
        "url": "https://eon-mcp.fly.dev/resource/result-1",
        # Extra fields are fine, but not required by connectors:
        # "description": f"Result for query: {query}"
    }

    payload = {"results": [result]}
    # IMPORTANT: the tool result goes inside a content array, as a JSON-encoded string
    return JSONResponse({
        "content": [{
            "type": "text",
            "text": json.dumps(payload, ensure_ascii=True)
        }]
    })

@app.post("/fetch")
async def fetch_endpoint(request: Request):
    """
    Body: {"ids":["doc-id-1", ...]}
    Returns: {"content":[{"type":"text","text":"{\"id\":\"...\",\"title\":\"...\",\"text\":\"...\",\"url\":\"...\",\"metadata\":null}"}]}
    """
    body = await request.json()
    ids: List[str] = (body or {}).get("ids", [])

    if not ids:
        doc = {"id": "", "title": "", "text": "", "url": "", "metadata": None}
    else:
        doc_id = ids[0]
        doc = {
            "id": doc_id,
            "title": f"Document {doc_id}",
            "text": f"Full content for document {doc_id}",
            "url": f"https://eon-mcp.fly.dev/resource/{doc_id}",
            "metadata": None
        }

    return JSONResponse({
        "content": [{
            "type": "text",
            "text": json.dumps(doc, ensure_ascii=True)
        }]
    })

# --------- Resource for the 'url' field ----------
@app.get("/resource/{doc_id}")
async def get_resource(doc_id: str):
    return {"id": doc_id, "content": f"Demo resource body for {doc_id}"}
