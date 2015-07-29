#!/usr/bin/env python

import json, requests, os

TASK_DOWNLOAD_TEMPLATE = "http://crowdcrafting.org/project/%s/tasks/export?type=task&format=json"
TASK_RUN_DOWNLOAD_TEMPLATE = "http://crowdcrafting.org/project/%s/tasks/export?type=task_run&format=json"

f = open("PROJECTS.json", "r")

projects = json.loads(f.read())

import requests
import time

def download_zip(project_short_name, _type):

	print "Attempting to download %s file for %s " % (_type, project_short_name )
	URL = ""
	FILENAME = "output/"+project_short_name+"/"+_type+".zip"

	if _type == "task":
		URL = TASK_DOWNLOAD_TEMPLATE % project_short_name
	if _type == "task_run":
		URL = TASK_RUN_DOWNLOAD_TEMPLATE % project_short_name

	res = requests.get(URL)
	if 'X-RateLimit-Remaining' in res.headers.keys() and int(res.headers['X-RateLimit-Remaining']) < 10:
		print "Sleeping for 5 minutes to comply with Pybossa ratelimiting......"
		time.sleep(300) # Sleep for 5 minutes
	else:
		if not os.path.exists(os.path.dirname(FILENAME)):
			os.makedirs(os.path.dirname(FILENAME))

		with open(FILENAME, "wb") as f:
			f.write(res.content)
		print "Successfully downloaded %s file for %s " % (_type, project_short_name )

FILE_COUNT = 1
for project_short_name in projects.keys():
	print "="*80
	print "FILE_COUNT : ",FILE_COUNT
	print "PROJECT_SHORT_NAME : ", project_short_name
	download_zip(project_short_name, "task")
	download_zip(project_short_name, "task_run")
	FILE_COUNT += 1