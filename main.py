from fastapi import FastAPI, Query
from enum import Enum
from pydantic import BaseModel
from typing import Annotated


class ModelName(str,Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Item(BaseModel):
    name: str
    description : str | None = None
    price: float 
    tax : float | None = None 

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}

'''@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id" : 3}
'''
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user}")
async def read_user(user_id : str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message":"Deep Learnin FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name" : model_name, "message":"Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/items/")
async def read_item(skip: int =0, limit: int = 10):
    return fake_items_db[skip : skip +limit]

'''@app.get("/items/{item_id}")
async def read_item(item_id: str , q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id" : item_id}
'''
# Multiple path and query parameters¶
'''
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
'''
# Required query parameters
'''
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id" : item_id, "needy": needy}
    return item
'''
#Mixed Req-Non Req parameters
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy : str, skip: int = 0, limit : int | None = None  
):
    item = {"itm_id" : item_id, "needy" : needy, "skip" : skip, "limit": limit}
    return item
##############################################
################ REQUEST BODY ################
##############################################

# Import Pydantic's BaseModel
'''
@app.post("/items/")
async def create_item(item: Item):
    return item
'''

# Using the Model
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax" : price_with_tax})
    return item_dict

# Query Parameters and String Validations¶
@app.get("/items")
async def read_item(q: str | None = None):
    results = {"items" : [{"items_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q })
    return results

#Additional Validation

@app.get("/items")
async def read_items(q: Annotated[str | None, Query(min_lenght=3, max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"},{"item_id": "Bar"}]}
    if q: 
        results.update({"q": q})
    return results


