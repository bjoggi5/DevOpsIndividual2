import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# used: https://fastapi.tiangolo.com/tutorial/body/
class ItemCreate(BaseModel):
    name: str
    description: str


app = FastAPI(
    title="FastAPI GitOps Starter",
    description="A starter template for learning GitOps with FastAPI",
    version="1.0.0",
    root_path=os.getenv("ROOT_PATH", "/GitOps-Starter"),
)


@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to FastAPI GitOps Starter!"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "fastapi-gitops-starter"},
    )


@app.get("/api/items")
async def list_items():
    """Example endpoint to list items."""
    return {
        "items": [
            {"id": 1, "name": "Item 1", "description": "First item"},
            {"id": 2, "name": "Item 2", "description": "Second item"},
            {"id": 3, "name": "Item 3", "description": "Third item"},
        ]
    }


@app.get("/api/items/{item_id}")
async def get_item(item_id: int):
    """Example endpoint to get a specific item by ID."""
    return {
        "id": item_id,
        "name": f"Item {item_id}",
        "description": f"This is item number {item_id}",
    }


@app.post("/api/items")
async def create_item(item: ItemCreate):
    """Create a new item."""
    return {
        "id": 999,
        "name": item.name,
        "description": item.description,
        "created": True,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
