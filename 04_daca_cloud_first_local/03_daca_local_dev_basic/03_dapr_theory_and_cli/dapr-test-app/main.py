from fastapi import FastAPI, HTTPException
import httpx
import os

app = FastAPI()
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
STATE_URL = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/state/statestore"

@app.get("/")
async def root():
    return {"message": "Hello from Dapr Test App!"}

@app.post("/save-state")
async def save_state(key: str, value: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(STATE_URL, json=[{"key": key, "value": value}])
            response.raise_for_status()
            return {"status": "State saved successfully"}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-state/{key}")
async def get_state(key: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{STATE_URL}/{key}")
            response.raise_for_status()
            return {"key": key, "value": response.json()}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=404, detail="State not found")