"""Launched with `poetry run start` at root level"""
import uvicorn  # type: ignore


def start() -> None:
    """Run uvicorn."""
    uvicorn.run("playground.app:app", host="0.0.0.0", port=8000, reload=True)
