from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

event_queue = asyncio.Queue()

@app.get("/sse")
async def sse_endpoint():
    async def event_generator():
        yield f"retry: 10000\ndata: {json.dumps({'type': 'hello', 'message': 'MCP server ready'})}\n\n"
        while True:
            data = await event_queue.get()
            yield f"data: {json.dumps(data)}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/search")
async def search(request: Request):
    query = await request.json()
    search_results = {
        "results": [
            {
                "id": "result-1",
                "title": f"Результат по запросу: {query.get('query', '')}",
                "url": "https://example.com/doc1"
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
async def fetch(request: Request):
    body = await request.json()
    doc_id = body.get("ids", ["result-1"])[0]

    document = {
        "id": doc_id,
        "title": f"Документ {doc_id}",
        "text": f"Контент документа с ID: {doc_id}",
        "url": f"https://example.com/{doc_id}",
        "metadata": {}
    }

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(document, ensure_ascii=False)
            }
        ]
    }
