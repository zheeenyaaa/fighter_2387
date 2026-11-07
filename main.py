from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import routers


app = FastAPI()
app.include_router(routers.router)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.get("/health")
async def health():
    return {
        "status": "UP",
        "components": {
            "api": {"status": "UP", "details": {"application": "fighter-api"}}
        },
    }


@app.get("/info")
async def info():
    return {
        "build": {"name": "fighter-api", "version": "local"},
        "developers": [
            "Zakrenichny Evgeny",
            "Zazulya Ilya",
            "Ishutin Oleg",
        ],
    }
