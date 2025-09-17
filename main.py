from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search")
async def search_endpoint(request: Request):
    body = await request.json()
    query = body.get("query", "")

    results = {
        "results": [
            {
                "id": "result-1",
                "title": "Test result",
                "description": f"Result for query: {query}",
                "url": "https://example.com"
            }
        ]
    }

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(results)
            }
        ]
    }

@app.post("/fetch")
async def fetch_endpoint(request: Request):
    body = await request.json()
    ids = body.get("ids", [])

    if not ids:
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({})
                }
            ]
        }

    doc = {
        "id": ids[0],
        "title": f"Document {ids[0]}",
        "text": f"Full content for document {ids[0]}",
        "url": "https://example.com"
    }

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(doc)
            }
        ]
    }

@app.get("/sse")
async def sse():
    return EventSourceResponse(hello_stream())

from sse_starlette.sse import EventSourceResponse
import asyncio

async def hello_stream():
    while True:
        yield {
            "event": "message",
            "data": json.dumps({"type": "hello", "message": "MCP server ready"})
        }
        await asyncio.sleep(10)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
