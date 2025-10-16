from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AppRequest(BaseModel):
    instance: str

class TokenRequest(BaseModel):
    instance: str
    client_id: str
    client_secret: str
    redirect_uri: str
    grant_type: str
    code: str
    scope: str

@app.post("/api/proxy/apps")
async def create_app(request: AppRequest):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://{request.instance}/api/v1/apps",
                json={
                    "client_name": "RETTO",
                    "redirect_uris": "urn:ietf:wg:oauth:2.0:oob",
                    "scopes": "read write follow",
                    "website": "https://retto.app"
                }
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/proxy/token")
async def get_token(request: TokenRequest):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://{request.instance}/oauth/token",
                data={
                    "client_id": request.client_id,
                    "client_secret": request.client_secret,
                    "redirect_uri": request.redirect_uri,
                    "grant_type": request.grant_type,
                    "code": request.code,
                    "scope": request.scope
                }
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/proxy/timeline/{instance}")
async def get_timeline(instance: str, endpoint: str = "home", limit: int = 20):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://{instance}/api/v1/timelines/{endpoint}?limit={limit}"
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)