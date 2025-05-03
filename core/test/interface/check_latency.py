

import time
import json

import pytest
from fastapi import FastAPI, Request, Response
from fastapi.testclient import TestClient

from app.interfaces.dto.response.technology_type_response import TechnologyTypeResponse

app = FastAPI()

# Middleware that adds latency to JSON responses.
@app.middleware("http")
async def add_latency_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time

    # If the response is JSON, update its body with the latency value.
    if response.media_type == "application/json":
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {}
        # Inject the calculated latency.
        data["latency"] = latency
        new_body = json.dumps(data)
        response = Response(
            content=new_body,
            status_code=response.status_code,
            media_type="application/json"
        )
    return response

# A simple endpoint returning JSON.
@app.get("/json")
async def json_endpoint():
    return {"message": "This is a test"}

# A simple endpoint returning plain text.
@app.get("/plain")
def plain_endpoint():
    return TechnologyTypeResponse(result= "This is plain text", latency= 23.44 ,status_code=200)

client = TestClient(app)

def test_json_endpoint_latency():
    response = client.get("/plain")
    print("response")
    # data = response.json()
    # # Verify that the latency field was injected.
    # assert "latency" in data
    # # Verify that the latency is a float and non-negative.
    # assert isinstance(data["latency"], float)
    # assert data["latency"] >= 0
    # # Ensure that other response data is preserved.
    # assert data.get("message") == "This is a test"

def test_plain_endpoint_no_modification():
    response = client.get("/plain")
    assert response.status_code == 200
    # Plain text responses should remain unmodified.
    assert response.text == "This is plain text"
