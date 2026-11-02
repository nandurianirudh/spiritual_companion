"""FastAPI app. Thin wrapper only — no Panchangam/ritual logic lives here.
Each ritual gets one router under `routers/`, mounted at `/v1`; the web UI
(and any future client) talks to these routes."""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from saarathi.api.routers import achamanam, pranayamam, pravara, sankalpam

API_PREFIX = "/v1"

# Origins allowed to call the API from a browser. Vite dev server by default;
# override with SAARATHI_CORS_ORIGINS="https://app.example.com,https://..." in prod.
DEFAULT_CORS_ORIGINS = ("http://localhost:5173", "http://127.0.0.1:5173")

app = FastAPI(
    title="saarathi",
    description="Telugu Panchangam-driven Sankalpam generator.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        o.strip()
        for o in os.environ.get("SAARATHI_CORS_ORIGINS", ",".join(DEFAULT_CORS_ORIGINS)).split(",")
        if o.strip()
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])


@app.get("/health", response_model=HealthResponse, summary="Liveness check")
def health() -> dict:
    return {"status": "ok"}


for _module in (sankalpam, pravara, achamanam, pranayamam):
    app.include_router(_module.router, prefix=API_PREFIX)
