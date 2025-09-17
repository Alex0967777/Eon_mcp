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

@app.post("/search")
async def search_endpoint(request: Request):
    query = await request.json()
    # Можешь здесь сделать что угодно: запрос к БД, апишке и т.д.
    # Сейчас просто тестовый ответ
    return {
        "results": [
            {
                "id": "result-1",
                "title": f"Результат по запросу: {query.get('query', '')}",
                "description": "Описание результата",
            }
        ]
    }

@app.post("/fetch")
async def fetch_endpoint(request: Request):
    body = await request.json()
    ids = body.get("ids", [])
    # Возвращаем "документы" по ID (заглушка)
    return {
        "documents": [
            {
                "id": id_,
                "content": f"Контент документа с ID: {id_}"
            }
            for id_ in ids
        ]
    }
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
