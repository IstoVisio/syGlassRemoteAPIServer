from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

class meshRequest(BaseModel):
	requestID: str
	user: str
	time : int
	timestamp : int
	body_list : List[int] = []

@app.get("/")
def read_root():
	return {"Welcome to the syGlass Remote Server! Let's see what we can do!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
	return {"item_id": item_id, "q": q}


@app.put("/request/")
def update_item(item: meshRequest):
	bodyIDsToMakeIntoMeshes = item.body_list
	print(bodyIDsToMakeIntoMeshes);
	#make into meshes
	return item