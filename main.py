from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

event_queue = asyncio.Queue()

from fastapi.responses import JSONResponse

@app.post("/search")
async def search_endpoint(request: Request):
    query = await request.json()
    results = {
        "results": [
            {
                "id": "result-1",
                "title": f"Результат по запросу: {query.get('query', '')}",
                "url": "https://example.com"
            }
        ]
    }
    return JSONResponse(content={
        "content": [
            {
                "type": "text",
                "text": json.dumps(results, ensure_ascii=False)
            }
        ]
    })

@app.post("/fetch")
async def fetch_endpoint(request: Request):
    body = await request.json()
    ids = body.get("ids", [])
    documents = {
        "id": ids[0],
        "title": "Документ",
        "text": f"Контент документа с ID: {ids[0]}",
        "url": "https://example.com"
    }
    return JSONResponse(content={
        "content": [
            {
                "type": "text",
                "text": json.dumps(documents, ensure_ascii=False)
            }
        ]
    })

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
    
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
