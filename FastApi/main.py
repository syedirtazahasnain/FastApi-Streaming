from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "1World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
     return {
          "item_id is": item_id,
            "query_param is": query_param
     }