from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

app = FastAPI()

# Allow all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SSE queue
event_queue = asyncio.Queue()

@app.post("/search")
async def search_endpoint(request: Request):
    query = await request.json()
    results = {
        "results": [
            {
                "id": "result-1",
                "title": f"Результат по запросу: {query.get('query', '')}",
                "description": "Описание результата",
                "url": "https://example.com"
            }
        ]
    }
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(results, ensure_ascii=False)
            }
        ]
    }

@app.post("/fetch")
async def fetch_endpoint(request: Request):
    body = await request.json()
    ids = body.get("ids", [])

    documents = [
        {
            "id": doc_id,
            "title": f"Документ {doc_id}",
            "text": f"Контент документа с ID: {doc_id}",
            "url": "https://example.com"
        } for doc_id in ids
    ]

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(documents[0], ensure_ascii=False)  # Только первый документ, как требует MCP
            }
        ]
    }

@app.get("/sse")
async def sse():
    async def event_generator():
        yield f"retry: 10000\ndata: {{\"type\": \"hello\", \"message\": \"MCP server ready\"}}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
