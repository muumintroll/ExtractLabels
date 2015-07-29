#!/usr/bin/env python

import urllib, json

URL_TEMPLATE = "http://crowdcrafting.org/api/project?limit=%s&offset=%s"
LIMIT = 100

OVERALL_DATA = []
for offset in range(100):
	print "Offset :: ",len(OVERALL_DATA)," LIMIT ::",LIMIT
	response = urllib.urlopen(URL_TEMPLATE % (LIMIT, len(OVERALL_DATA)))

	data = json.loads(response.read())
	for d in data:
		OVERALL_DATA.append(d)

	print "Number of results = ", len(data)
	f = open("project_list/"+str(offset)+".json", "w")
	f.write(json.dumps(data))

	f = open("project_list/overall.json","w")
	f.write(json.dumps(OVERALL_DATA))

	if len(data) == 0:
		break

print "Data Collected. Compiling all results into a single json"

f = open("project_list/overall.json", "r")
data = json.loads(f.read())

projects = {}

for d in data:
	projects[d['short_name']] = d

f = open("PROJECTS.json", "w")
f.write(json.dumps(projects))