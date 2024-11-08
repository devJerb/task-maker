from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(
    title="Simple API",
    description="A simple FastAPI application with two endpoints",
    version="1.0.0",
    docs_url="/"
)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


# In-memory storage
items = {}


@app.post(
    "/items/",
    response_model=Item,
    status_code=201,
    summary="Create a new item",
    description="Create a new item with the provided details",
)
async def create_item(item: Item):
    if item.name in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item.name] = item
    return item


@app.get(
    "/items/{item_name}",
    response_model=Item,
    summary="Get item by name",
    description="Retrieve an item's details by its name",
)
async def get_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_name]


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
