from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select
from fastapi import FastAPI , Path, Body
from sqlalchemy.dialects.mysql import BIGINT, TEXT
from pydantic import BaseModel

# Define the model
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    price: Optional[float] = None
    is_offer: bool = False
    
class ItemDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: Optional[int] = Field(sa_type=BIGINT(unsigned=True))
    description: Optional[str] = Field(sa_type=TEXT)
    
class ItemDescriptionRequest(BaseModel):
    item_id: int
    description: str
    

# MySQL connection (sync driver)
# MYSQL_URL = "mysql+pymysql://root:password@localhost:3306/your_database"
MYSQL_URL = "mysql+pymysql://root:@localhost:3306/fastapi_db"
engine = create_engine(MYSQL_URL, echo=True)
app = FastAPI()

@app.delete("/drop-all")
def drop_all_tables():
    SQLModel.metadata.drop_all(engine)
    return {"message": "All tables dropped."}

# Create DB and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# FastAPI app

# Initialize DB on startup (sync way)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# POST /items   
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    
@app.post("/items/{item_id}/description", response_model=ItemDetail)
def create_item_description(
    # item_id: int = Path(...),
    # description: str = Body(...)
     item: ItemDescriptionRequest
):
    item_detail = ItemDetail(item_id=item.item_id, description=item.description)

    with Session(engine) as session:
        session.add(item_detail)
        session.commit()
        session.refresh(item_detail)
        return item_detail



# GET /items
@app.get("/items/", response_model=List[Item])
def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items
