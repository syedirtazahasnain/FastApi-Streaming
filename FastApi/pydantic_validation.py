from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name : str
    price : float
    is_offer: bool = False
    password: str = "test@123"

class ItemResponse(BaseModel):
    name : str
    price : float
    is_offer: bool = False
    
class FullItemResponse(BaseModel):
    message: str
    item: ItemResponse
    
@app.post("/items/", response_model=FullItemResponse)
def create_item(item: Item):
    print(item)
    
    # return item
    return {
            "message": "Item created successfully",
            "item": item
        }