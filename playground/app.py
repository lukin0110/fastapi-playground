"""FastAPI Playground.

Run locally

    uvicorn playground.app:app

"""
from typing import Any, Dict

from fastapi import FastAPI

from . import users

app = FastAPI(title="Playground")


@app.get("/")
def index() -> Dict[str, Any]:
    """Hello World."""
    return {"message": "Hello World"}


app.include_router(users.router, prefix="/users", tags=["Users"])
