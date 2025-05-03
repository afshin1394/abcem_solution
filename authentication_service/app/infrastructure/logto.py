import asyncio

from fastapi import FastAPI

from app.core.config import settings

app = FastAPI()

# Configuration
logto_endpoint = settings.logto_endpoint
token_endpoint = settings.logto_token_endpoint
application_id = settings.logto_app_id
application_secret = settings.logto_app_secret

# Helper function to fetch access token
import httpx
from base64 import b64encode
from fastapi import HTTPException


# Helper function to fetch access token
async def fetch_access_token():
    try:
        # Prepare headers with basic authentication
        auth_header = f"Basic {b64encode(f'{application_id}:{application_secret}'.encode()).decode()}"
        print(f"token_endpoint {token_endpoint}",flush=True)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": auth_header,
        }

        # Prepare request body
        payload = {
            "grant_type": "client_credentials",
        }

        # Make asynchronous POST request
        async with httpx.AsyncClient() as client:
            response = await client.post(token_endpoint, headers=headers, data=payload)
            print(f"response {response}")
        # Check for errors
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        # Return response as JSON
        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
