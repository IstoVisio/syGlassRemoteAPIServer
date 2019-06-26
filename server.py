from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import syglass

app = FastAPI()

class meshRequest(BaseModel):
	requestID: str
	user: str
	time : int
	timestamp : int
	body_list : List[int] = []

@app.get("/")
def read_root():
	return {"Welcome to the syGlass Remote Server! Let's see what we can do!"}


@app.post("/request/")
def update_item(item: meshRequest):
	print(item)
	#bodyIDsToMakeIntoMeshes = item.body_list
	#print(bodyIDsToMakeIntoMeshes);
	#make into meshes
	return item