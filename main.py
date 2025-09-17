from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/search")
async def search_endpoint(request: Request):
    body = await request.json()
    query = body.get("query", "")

    results = {
        "results": [
            {
                "id": "result-1",
                "title": f"Test result",
                "description": f"Result for query: {query}",
                "url": "https://eon-mcp.fly.dev/resource/result-1"
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
        "url": f"https://eon-mcp.fly.dev/resource/{ids[0]}"
    }

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(doc)
            }
        ]
    }
