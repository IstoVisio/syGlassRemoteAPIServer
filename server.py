from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import ntpath
import tarfile
import os
import subprocess
import requests
import io
import shutil
import time

import pyglass


def from_tarfile(path_or_bytes, bodyID, name):
	tf = tarfile.TarFile(fileobj=io.BytesIO(path_or_bytes))
	members = sorted(tf.getmembers(), key=lambda m: m.name)

	meshpathlist = []
	new_path = 'C:\\VR_meshes\\'+ str(bodyID)
	if not os.path.exists(new_path):
		os.makedirs(new_path)
	for member in members:
		ext = member.name[-4:]
		# Skip non-mesh files and empty files
		if ext in ('.drc', '.obj', '.ngmesh') and member.size > 0:
			buf = tf.extractfile(member).read()
			#if len(buf) == 0:
			#	continue
			with open(new_path + "\\" + member.name, "wb") as ff:
				ff.write(buf)
			#add subprocess to convert draco to obj cmd: draco_decoder
			#if len(buf)
			s = "C:\\Users\\smithc\\AppData\\Local\\Continuum\\miniconda3\\Library\\bin\\draco_decoder.exe -i " + new_path + "\\" + member.name + " -o " + new_path + "\\" + member.name[:-3] + "obj"
			#print(s)
			FNULL = open(os.devnull, 'w')
			subprocess.call(s, stdout=FNULL, stderr=subprocess.STDOUT)
			meshpathlist.append(new_path + "\\" + member.name[:-3] + "obj")
	return meshpathlist

def copyEmpty(name):
	emptyProject = "emptyProject\\emptyProject.syg"
	emptyProjectMeta = "emptyProject\\emptyProject.sym"
	if not os.path.exists("output\\" + name):
		os.mkdir("output\\" + name)
	shutil.copy(emptyProject, "output/" + name + "/" + name + ".syg")
	shutil.copy(emptyProjectMeta, "output/" + name + "/" + name + ".sym")

def addMeshes(path, name, bodyList):
	copyEmpty(name)
	print(path)
	projectPath = os.path.join(os.getcwd(), "output\\" + name + "\\" + name + ".syg")
	print(projectPath)
	project = pyglass.OpenProject(pyglass.path(projectPath))
	l = path
	project.ImportMeshOBJs("default", "\n".join(l))
	for each in bodyList:
		project.CreateTag("default", str(each))
	while project.GetMeshIOPercentage() != 100:
		print("Progress: " + str(project.GetMeshIOPercentage()) + "%")
		print("Current mesh: "  + project.GetMeshIOName() + "\n")
		time.sleep(2)
	for ii, id in enumerate(bodyList):
		nameMesh = ntpath.basename(path[ii])
		project.AddTagToMesh("default", str(id), nameMesh)
	
	vl = pyglass.VolumeLibrary()
	vl.ReloadLibrary()
	entry = vl.CreateEntryFromPath(projectPath, name)
	vl.PutEntry(entry)
	project.RandomizeMeshColors()
	
	print("Project Ready!")


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

	name = "Bodies" + str(len(item.body_list)).strip() + "_" + item.user.strip() + "_" + item.time

	meshPathList = []
	bodyList = []

	for bodyID in body_id:
		sv_map = "http://"+str(server)+":"+str(port)+"/api/node/"+str(uuid)+"/segmentation_sv_meshes/tarfile/"+str(bodyID)
		print(sv_map)
		map_response = requests.get(sv_map)
		newMeshPathList = from_tarfile(map_response.content, bodyID, name)
		tempBodyList = [bodyID] * len(newMeshPathList)
		meshPathList = meshPathList + newMeshPathList
		bodyList = bodyList + tempBodyList
		
	addMeshes(meshPathList, name, bodyList)

	
	return item