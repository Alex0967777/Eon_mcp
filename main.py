from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

# Simple CORS for ChatGPT connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
