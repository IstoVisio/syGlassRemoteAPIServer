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

import syglass
DRACO_DEC_PATH = "C:\\Users\\smithc\\AppData\\Local\\Continuum\\miniconda3\\Library\\bin\\draco_decoder.exe"

def from_tarfile(path_or_bytes, body_id, name):
	tf = tarfile.TarFile(fileobj=io.BytesIO(path_or_bytes))
	members = sorted(tf.getmembers(), key=lambda m: m.name)

	meshpathlist = []
	new_path = 'C:\\VR_meshes\\{body_id}'
		
	if not os.path.exists(new_path):
		os.makedirs(new_path)

	for member in members:
		ext = os.path.splitext(member.name)[1]
		
		# Skip non-mesh files and empty files
		if ext not in ('.drc', '.obj') or member.size == 0:
			print(f"Skipping invalid file {member}.")
			continue
		
		file_path = new_path + "\\" + member.name
		buf = tf.extractfile(member).read()

		with open(file_path, "wb") as ff:
			ff.write(buf)
		
		# Convert any drc we accepted to obj
		if ext == '.drc':
			obj_path = file_path[:-3] + "obj"

			# add subprocess to convert draco to obj cmd: draco_decoder
			subprocess.run([
				DRACO_DEC_PATH,
				"-i",
				file_path,
				"-o",
				obj_path,
			])
			file_path = obj_path

		meshpathlist.append(file_path)

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
def update_dvid_item(item: meshAndDVIDRequest):
	print(item)

	server = item.dvid
	uuid = item.uuid
	port = item.port
	segmentation = item.segmentation
	body_length = len(item.body_list)

	name = f"Bodies{body_length}_{item.user.strip()}_{item.time}"

	meshPathList = []
	bodyList = []
	sv_map_base = f"http://{server}:{port}/api/node/{uuid}/segmentation_sv_meshes/tarfile/"
	
	for body_id in item.body_list:
		sv_map = sv_map_base + str(body_id)
		print(sv_map)
		print(f"Requesting meshes (Body id: {body_id}) from server")
		map_response = requests.get(sv_map)
		newMeshPathList = from_tarfile(map_response.content, bodyID, name)
		tempBodyList = [bodyID] * len(newMeshPathList)
		meshPathList = meshPathList + newMeshPathList
		bodyList = bodyList + tempBodyList
	addMeshes(meshPathList, name, bodyList)
	
	return item