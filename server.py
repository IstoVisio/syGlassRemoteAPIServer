from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import tarfile
import os
import subprocess
import requests
import io

import pyglass

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
        	s = ['draco_decoder']
        	subprocess.call(draco_decoder)

def copyEmpty(name):
	emptyProject = "emptyProject\\emptyProject.syg"
	emptyProjectMeta = "emptyProject\\emptyProject.sym"
	if not os.path.exists("output/" + name):
		os.mkdir("output/" + name)
	shutil.copy(emptyProject, "output/" + name + "/" + name + ".syg")
	shutil.copy(emptyProjectMeta, "output/" + name + "/" + name + ".sym")

def convertMeshes(path):
	name = ntpath.basename(path)
	copyEmpty(name)
	projectPath = os.path.join(os.getcwd(), "output\\" + name + "\\" + name + ".syg")
	print(projectPath)
	project = pyglass.OpenProject(pyglass.path(projectPath))
	l = glob.glob(path + "\\*.obj")
	project.ImportMeshOBJs("default", "\n".join(l))
	while project.GetMeshIOPercentage() != 100:
		print("Progress: " + str(project.GetMeshIOPercentage()) + "%")
		print("Current mesh: "  + project.GetMeshIOName() + "\n")
		time.sleep(2)
	vl = pyglass.VolumeLibrary()
	vl.ReloadLibrary()
	entry = vl.CreateEntryFromPath(projectPath, name)
	vl.PutEntry(entry)
	project.RandomizeMeshColors()


# ------------------------------------------------------ #

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

	name = "Body#:" + str(len(item.body_list)) + "_" + item.user + "_" + item.time

	for bodyID in body_id:
		sv_map = "http://"+str(server)+":"+str(port)+"/api/node/"+str(uuid)+"/"+str(segmentation)+"/supervoxels/"+str(bodyID)
		print(sv_map)
		map_response = requests.get(sv_map)
		print(map_response.content)
		supervoxels = map_response.content.decode('UTF-8')
		supervoxels = supervoxels[1:-1].split(',')
		supervoxels = [int(x) for x in supervoxels]
		for each in supervoxels:
			#get all the supervoxels 
		new_path = 'C:\\VR_meshes\\'+ bodyID
		if not os.path.exists(new_path):
			os.makedirs(new_path)

	
	return item