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


#project = {"user": "timedRunSingle", "time": "2019-06-27_083132", "epoch": 1561638692, "body_list": ['1563440956', '2221053439', '887105351', '1039072544', '1420906080', '607925257'], "dvid": "emdata2", "port": "7900", "uuid": "3b29", "segmentation": "segmentation"}  
project = {"user": "labelTEST2", "time": "2019-06-27_083132", "epoch": 1561638692, "body_list": ['1039072544'], "dvid": "emdata2", "port": "7900", "uuid": "3b29", "segmentation": "segmentation"}  
converted_to_json = json.dumps(project)
print(converted_to_json)
url_to_write_to = "http://10.200.255.16:8000/dvidRequest/"
requests.post(url_to_write_to, json=json.loads(converted_to_json))
