from sql_model import SqlModel , Field
from typing import Optional
from contextlib import asynccontextmanager

class Item(SqlModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    price: Optional[float] = None
    is_offer: bool = False
    
from sql_model import create_engine, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SqlModel.metadata.create_all(engine)
    
from fastapi import FastAPI
app = FastAPI()

@aysnccontextmanager
async