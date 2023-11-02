from typing import List
from fastapi import FastAPI, HTTPException
from models.ItemPayload import ItemPayload
from prisma.models import Item
from helper.prismaClient import prisma

app = FastAPI()


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


# Route to add a item
@app.post("/items/{name}/{quantity}")
async def add_item(name: str, quantity: int) -> dict[str, Item]:
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")
    # if item already exists, we'll just add the quantity.
    # get all item names

    item = await prisma.item.create(data={"name": name, "quantity": quantity})

    return {"item": item}


# Route to list a specific item by ID
@app.get("/items/{item_id}")
async def list_item(item_id: int) -> dict[str, Item]:
    item: Item | None = await prisma.item.find_unique(where={"id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found.")
    return {"item": item}


# Route to list all items
@app.get("/items")
async def list_items() -> dict[str, List[Item]]:
    itemList: List[Item] = await prisma.item.find_many()
    return {"items": itemList}


# Route to delete a specific item by ID
@app.delete("/items/{item_id}")
async def delete_item(item_id: int) -> dict[str, str]:
    item: Item | None = await prisma.item.delete(where={"id": item_id})

    return {"result": "Item deleted."}


# Route to remove some quantity of a specific item by ID
@app.delete("/items/{item_id}/{quantity}")
async def remove_quantity(item_id: int, quantity: int) -> dict[str, str]:
    item: Item | None = await prisma.item.find_unique(where={"id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found.")
    # if quantity to be removed is higher or equal to item's quantity, delete the item
    if item.quantity <= quantity:
        item: Item | None = await prisma.item.delete(where={"id": item_id})
        return {"result": "Item deleted."}
    else:
        item: Item | None = await prisma.item.update(
            where={"id": item_id}, data={"quantity": item.quantity - quantity}
        )
    return {"result": f"{quantity} items removed."}
