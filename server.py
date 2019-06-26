from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import tarfile
import os
import subprocess
import requests
import io

def from_tarfile(path_or_bytes):
        tf = tarfile.TarFile(fileobj=io.BytesIO(path_or_bytes))
        
        # As a convenience, we sort the members by name before loading them.
        # This ensures that tarball storage order doesn't affect vertex order.
        members = sorted(tf.getmembers(), key=lambda m: m.name)

        meshes = {}
        for member in members:
            ext = member.name[-4:]
            # Skip non-mesh files and empty files
            if ext in ('.drc', '.obj', '.ngmesh') and member.size > 0:
            	buf = tf.extractfile(member).read()
            	if len(buf) == 0:
            		continue
            	with open(member.name, "wb") as ff:
            		ff.write(buf)
            	#add subprocess to convert draco to obj cmd: draco_decoder
            	#if len(buf)
            	subprocess.call(draco_decoder)


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

	server = item.dvid
	uuid = item.uuid
	instance = 'segmentation_sv_meshes'
	body_id = item.body_list
	port = item.port
	segmentation = item.segmentation
	#replace fetch_tarfile with below 2 lines
	for bodyID in body_id:
		sv_map = "http://"+str(server)+":"+str(port)+"/api/node/"+str(uuid)+"/"+str(segmentation)+"/supervoxels/"+str(bodyID)
		print(sv_map)
		map_response = requests.get(sv_map)
		from_tarfile(map_response.content)
		new_path = 'C:\\VR_meshes\\'+ bodyID
		if not os.path.exists(new_path):
			os.makedirs(new_path)

	
	return item