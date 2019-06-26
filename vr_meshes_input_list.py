# import sys
#from neuclease.dvid import *
#from vol2mesh import Mesh

from multiprocessing import Process

import json

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from time import gmtime, strftime, sleep
import time

import requests

#-----------------------------------------------------------------------------------------------------

#def make_meshes(bodyID):
	#print(bodyID)
	## tar_bytes = fetch_tarfile(*master_meshes, 1137499592)
	#tar_bytes = fetch_tarfile(*master_meshes, bodyID)
#
	#mesh = Mesh.from_tarfile(tar_bytes)
#
	#mesh.simplify(0.1)
#
	## mesh.serialize('/groups/flyem/data/neacee_data/VR_meshes_03-03-2019/'+bodyID+'-decimated.obj')
	#mesh.serialize('/groups/flyem/data/neacee_data/VR_meshes_06-26-2019/'+bodyID+'-decimated.obj')


def timestamp_to_epoch(timestamp):
    timestamp_format = '%Y-%m-%d %H:%M:%S'
    epoch = int(time.mktime(time.strptime(timestamp, timestamp_format)))
    return epoch

#-----------------------------------------------------------------------------------------------------

if __name__ == '__main__':

	body_list = []
	procs = []

	#-- GUI Things --
	#-- Create instance --
	win = tk.Tk()

	#-- add title--
	win.title("Generate VR Mesh")

	# -- server --
	ttk.Label(win, text="DVID Server:").grid(column=0, row=0)
	server = tk.StringVar()
	server_chosen = ttk.Combobox(win, width=12, textvariable=server)
	server_chosen['values'] = ("emdata1", "emdata2", "emdata3", "emdata4")
	server_chosen.grid(column=0, row=1)
	server_chosen.current(3)

	# -- port --
	ttk.Label(win, text="DVID Port:").grid(column=1, row=0)
	port = tk.StringVar()
	port_chosen = ttk.Combobox(win, width=12, textvariable=port)
	port_chosen['values'] = (7900, 8400, 8700, 8900)
	port_chosen.grid(column=1, row=1)
	port_chosen.current(3)

	ttk.Label(win, text="UUID:").grid(column=2, row=0)
	uuid = tk.StringVar()
	uuid_chosen = ttk.Combobox(win, width=12, textvariable=uuid)
	uuid_chosen['values'] = ("a21a")
	uuid_chosen.grid(column=2, row=1)
	uuid_chosen.current(0)

	#-- segmentation --
	ttk.Label(win, text="Segmentation:").grid(column=3, row=0)
	segmentation = tk.StringVar()
	segmentation_chosen = ttk.Combobox(win, width=12, textvariable=segmentation)
	segmentation_chosen['values'] = ("segmentation", "segmentation1")
	segmentation_chosen.grid(column=3, row=1)
	segmentation_chosen.current(0)

	# #-- bodyID --
	# ttk.Label(win, text="BodyID").grid(column=4, row=0)
	# input_bodyID = tk.StringVar()
	# input_bodyID_entered = tk.Entry(win, width=15, textvariable=input_bodyID)
	# input_bodyID_entered.grid(column=4, row=1, columnspan=1)


	#-- todo action --
	ttk.Label(win, text="Body List File").grid(column=0, row=3)
	input_file = tk.StringVar(value =" ")
	input_file_entered = ttk.Entry(win, width=60, textvariable=input_file)
	input_file_entered.grid(column=0, row=4, columnspan=4)

	#-- Add text box Entry form --
	tk.Label(win, text="Username").grid(column=0, row=6)
	user = tk.StringVar(value=" ")
	user_entered = tk.Entry(win, width=60, textvariable=user)
	user_entered.grid(column=0, row=7, columnspan=4)

	#-- adding a button --
	action = ttk.Button(win, text="Submit", command=win.quit)
	action.grid(column=2, row=8)

	# win.configure(background='blue')

	#-- start gui --
	win.mainloop()
	#-- End GUI Things --
	#-----------------------------------------------------------------------------------------

	now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	epoch = timestamp_to_epoch(now_time)

	#-- reads file with bodyIDs, appends to list --

	body_list = input_file.get().strip().split(" ")

	print(body_list)


	#class meshAndDVIDRequest(BaseModel):
	#requestID: str
	#user: str
	#time : str
	#epoch : int
	#body_list : List[int] = []
	#dvid : str
	#port : int
	#uuid : str
	#segmentation : strftime

	project = {
		"user": user.get(),
		"time" : now_time,
		"epoch" : epoch,
		"body_list" : body_list,
		"dvid" : server.get(),
		"port" : port.get(),
		"uuid" : uuid.get(),
		"segmentation" : segmentation.get()

	}

converted_to_json = json.dumps(project)
print(converted_to_json)
url_to_write_to = "http://127.0.0.1:8000/dvidRequest/"
requests.post(url_to_write_to, json=json.loads(converted_to_json))


	# -- multiprocess --
	#for body in body_list:
		#proc = Process(target=make_meshes, args=(body,))
		#procs.append(proc)
		#proc.start()
#
	#for proc in procs:
		#proc.join()