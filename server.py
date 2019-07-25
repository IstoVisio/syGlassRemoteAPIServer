from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
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

	output_dir = f"output\\{name}"
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)

	shutil.copy(emptyProject, f"output\\{name}\\{name}.syg")
	shutil.copy(emptyProjectMeta, f"output\\{name}\\{name}.sym")


def convertMeshes(path_map, name):
	print("Putting meshes into project")
	copyEmpty(name)
	projectPath = os.path.join(os.getcwd(), f"output\\{name}\\{name}.syg")
	print(projectPath)

	with syglass.get_project(projectPath) as project:
		all_objs = [obj for obj in obj_list for obj_list in path_map.values()]
		project.impl.ImportMeshOBJs("default", "\n".join(all_objs))

		while project.impl.GetMeshIOPercentage() != 100:
			print(f"Progress: {project.impl.GetMeshIOPercentage()}%")
			print(f"Current mesh: {project.impl.GetMeshIOName()}\n")
			time.sleep(2)

		project.impl.RandomizeMeshColors("default")
		mesh_colors = project.get_mesh_colors()

		for body_id, obj_list in path_map.items():
			project.create_label(body_id)
			first_mesh_color = mesh_colors[os.path.basename(obj_list[0])]

			for mesh_name in map(os.path.basename, obj_list):
				project.add_label_to_surface(body_id, mesh_name)
				project.set_surface_color(mesh_name, first_mesh_color)

		vl = syglass.pyglass.VolumeLibrary()
		vl.ReloadLibrary()
		entry = vl.CreateEntryFromPath(projectPath, name)
		vl.PutEntry(entry)


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

	meshPathMap = {}

	sv_map_base = f"http://{server}:{port}/api/node/{uuid}/segmentation_sv_meshes/tarfile/"
	
	for body_id in item.body_list:
		sv_map = sv_map_base + str(body_id)
		print(sv_map)
		print(f"Requesting meshes (Body id: {body_id}) from server")
		map_response = requests.get(sv_map)
		meshesPath = from_tarfile(map_response.content, body_id, name)
		meshPathMap[body_id] = meshesPath

	convertMeshes(meshPathMap, name)
	
	return item