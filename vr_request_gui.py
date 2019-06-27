'''
neacee 03-26-2019
user create mesh request for VR project
simple gui

'''


import json
import requests
# import getpass
from datetime import datetime
from time import gmtime, strftime, sleep
import time
import tkinter as tk

#-----------------------------------------------------------------------------------------

def add_body_to_list():
	#-- get bodyID from entry, add to list --
	body = bodyID.get()
	request_list.append(body)
	print(body)
	return(request_list)

def get_request_data():
	#-- request_id = userame.epoch --
	if len(request_list) < 1:
		return(request_list)
	else:
		now_time = datetime.now().strftime('%Y-%m-%d_%H%M%S')
		epoch = timestamp_to_epoch(now_time)
		username = user.get()
		if username == "username":
			print("Username Required!!")
			return(username)
		else:
			request_id = username+"_"+str(epoch)
			print("Your VR body request list:")
			print(request_list)

			project = {
				"requestID": request_id,
				"user": username,
				"time" : epoch,
				"timestamp" : now_time,
				"body_list" : request_list
				}
			VR_project_request = {request_id: project}
			send_request(request_id, project)

def send_request(request_id, VR_project_request):
	# print(request_id)
	print("Your VR project request list: ")
	print(VR_project_request)
	#-- close gui opon request submit --
	#win.quit()

	# #-- write request to api --
	converted_to_json = json.dumps(VR_project_request)
	print(converted_to_json)
	url_to_write_to = "http://127.0.0.1:8000/request/"
	requests.post(url_to_write_to, json=json.loads(converted_to_json))

#-- convert timestamp to epoch for id --
def timestamp_to_epoch(timestamp):
    timestamp_format = '%Y-%m-%d %H:%M:%S'
    epoch = int(time.mktime(time.strptime(timestamp, timestamp_format)))
    return epoch


#------------------------------------------------------------------------------------

if __name__ == '__main__':

	request_list = []

	#-- Create instance --
	win = tk.Tk()
	#-- add title--
	win.title("VR Mesh Project Request")

	#-- Add text box Entry form --
	tk.Label(win, text="Username").grid(column=0, row=0)
	user = tk.StringVar(value="username")
	user_entered = tk.Entry(win, width=0, textvariable=user)
	user_entered.grid(column=0, row=1, columnspan=1)

	#-- Add text box Entry form --
	tk.Label(win, text="Add BodyID To List").grid(column=2, row=0)
	bodyID = tk.IntVar(value="bodyID")
	bodyID_entered = tk.Entry(win, width=20, textvariable=bodyID)
	bodyID_entered.grid(column=2, row=1, columnspan=1)

	btn = tk.Button(text = 'Add to List', command = add_body_to_list)
	btn.grid(column=2, row=6)

	#-- adding a button --
	action = tk.Button(win, text="Submit Request", command=get_request_data)
	action.grid(column=0, row=6)

	#-- adding a button --
	action = tk.Button(win, text="Quit", command=win.quit)
	action.grid(column=1, row=8)

	#-- start gui --
	win.mainloop()