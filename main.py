
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import routers
from config import settings
from db_depends import lifespan

app = FastAPI(lifespan = lifespan)
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
        "environment": settings.app_env,
        "feature_flag": settings.feature_flag,
        "build": {"name": "fighter-api", "version": "local"},
        "developers": [
            "Zakrenichny Evgeny",
            "Zazulya Ilya",
            "Ishutin Oleg",
        ],
    }
