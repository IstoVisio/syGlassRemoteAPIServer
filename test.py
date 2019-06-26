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


project = {
	"requestID": "hi_12344",
	"user": "hi",
	"time" : 111,
	"timestamp" : 222,
	"body_list" : [12,34,56]
	}


converted_to_json = json.dumps(project)
print(converted_to_json)
url_to_write_to = "http://127.0.0.1:8000/request/"
requests.post(url_to_write_to, json=json.loads(converted_to_json))