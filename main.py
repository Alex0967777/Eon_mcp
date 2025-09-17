# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse, PlainTextResponse
from typing import Any, Dict, AsyncGenerator
import asyncio
import json
import os

app = FastAPI(title="Eon MCP")

def ok(id_: Any, result: Dict[str, Any]):
    return {"jsonrpc": "2.0","id": id_,"result": result}

def err(id_: Any, code: int, message: str, data: Dict[str, Any] | None = None):
    return {"jsonrpc":"2.0","id":id_,"error":{"code":code,"message":message,**({"data":data} if data else {})}}

MOCK_DOCS = {
    "result-1": {"id":"result-1","title":"Document result-1","text":"Full content for document result-1","url":"https://eon-mcp.fly.dev/resource/result-1"}
}

@app.get("/")
def health():
    return {"status": "Eon MCP server running."}

@app.post("/mcp")
async def mcp_rpc(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(err(None, -32700, "Parse error"), status_code=400)
    if isinstance(body, list):
        results = [await handle_rpc(envelope) for envelope in body]
        return JSONResponse(results)
    else:
        result = await handle_rpc(body)
        if result is None:
            return PlainTextResponse("", status_code=204)
        return JSONResponse(result)

async def handle_rpc(msg: Dict[str, Any] | None):
    if not isinstance(msg, dict):
        return err(None, -32600, "Invalid Request")
    rpc_id = msg.get("id")
    method = msg.get("method")
    params = msg.get("params") or {}
    if not method:
        return err(rpc_id, -32600, "Invalid Request: no method")
    if method == "initialize":
        protocol_version = params.get("protocolVersion") or os.getenv("MCP_PROTOCOL_VERSION", "2024-11-05")
        server_info = {"name":"Eon MCP","version":os.getenv("MCP_SERVER_VERSION","0.1.0")}
        capabilities = {"tools": {}}
        instructions = "Welcome to Eon MCP. Available tools: search(query: string), fetch(id: string)."
        return ok(rpc_id, {"protocolVersion":protocol_version,"serverInfo":server_info,"capabilities":capabilities,"instructions":instructions})
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        tools = [
            {"name":"search","description":"Toy search across mock corpus.","inputSchema":{"type":"object","properties":{"query":{"type":"string","description":"Search query"}},"required":["query"],"additionalProperties":False}},
            {"name":"fetch","description":"Fetch a document by id from mock corpus.","inputSchema":{"type":"object","properties":{"id":{"type":"string","description":"Document id"}},"required":["id"],"additionalProperties":False}},
        ]
        return ok(rpc_id, {"tools": tools})
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        if name == "search":
            q = (args.get("query") or "").strip()
            results = []
            if q:
                r = MOCK_DOCS["result-1"]
                results.append({"id":r["id"],"title":"Test result","description":f"Result for query: {q}","url":r["url"]})
            return ok(rpc_id, {"content":[{"type":"text","text":json.dumps({"results":results},ensure_ascii=False)}]})
        elif name == "fetch":
            doc_id = (args.get("id") or "").strip()
            doc = MOCK_DOCS.get(doc_id)
            if not doc:
                return err(rpc_id,-32004,f"Not found: {doc_id}")
            return ok(rpc_id, {"content":[{"type":"text","text":json.dumps(doc,ensure_ascii=False)}]})
        else:
            return err(rpc_id,-32601,f"Unknown tool: {name}")
    if method == "ping":
        return ok(rpc_id, {"pong": True})
    return err(rpc_id, -32601, f"Method not found: {method}")

@app.get("/mcp")
async def mcp_events():
    async def event_stream():
        while True:
            payload = json.dumps({"method":"notifications/heartbeat","params":{"ts":asyncio.get_event_loop().time()}})
            yield f"event: message\ndata: {payload}\n\n".encode("utf-8")
            await asyncio.sleep(15)
    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT","8080")))
