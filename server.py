from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class meshRequest(BaseModel):
	requestID: str
	user: str
	time : int
	timestamp : int
	body_list : List[int] = []

class meshAndDVIDRequest(BaseModel):
	user: str
	time : str
	epoch : int
	body_list : List[int] = []
	dvid : str
	port : int
	uuid : str
	segmentation : str


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

@app.post("/dvidRequest/")
def update_item(item: meshAndDVIDRequest):
	print(item)
	#bodyIDsToMakeIntoMeshes = item.body_list
	#print(bodyIDsToMakeIntoMeshes);
	#make into meshes
	return item