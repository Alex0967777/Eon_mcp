from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Очередь для SSE
event_queue = asyncio.Queue()

@app.get("/")
async def root():
    return {"status": "Eon MCP server running."}

@app.get("/sse")
async def sse_endpoint():
    async def event_stream():
        yield "retry: 10000\n"
        yield f"data: {{\"type\": \"hello\", \"message\": \"Eon MCP stream connected.\"}}\n\n"
        while True:
            data = await event_queue.get()
            yield f"data: {data}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.post("/event")
async def receive_event(request: Request):
    data = await request.json()
    await event_queue.put(str(data))
    return JSONResponse({"status": "received", "echo": data})

@app.post("/search")
async def search_endpoint(request: Request):
    query = await request.json()
    search_results = {
        "results": [
            {
                "id": "result-1",
                "title": f"Результат по запросу: {query.get('query', '')}",
                "url": "https://example.com/result-1"
            }
        ]
    }
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(search_results, ensure_ascii=False)
            }
        ]
    }

@app.post("/fetch")
async def fetch_endpoint(request: Request):
    body = await request.json()
    ids = body.get("ids", [])
    if not ids:
        return JSONResponse(status_code=400, content={"error": "No IDs provided"})

    result_id = ids[0]
    document = {
        "id": result_id,
        "title": f"Документ {result_id}",
        "text": f"Контент документа с ID: {result_id}",
        "url": f"https://example.com/docs/{result_id}",
        "metadata": {"source": "eon-mcp"}
    }

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(document, ensure_ascii=False)
            }
        ]
    }
