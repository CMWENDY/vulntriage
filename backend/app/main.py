from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title="VulnTriage AI", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}

