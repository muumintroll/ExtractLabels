#!/usr/bin/env python
import json

f = open("project_list/overall.json", "r")
data = json.loads(f.read())

projects = {}

for d in data:
	projects[d['short_name']] = d

f = open("PROJECTS.json", "w")
f.write(json.dumps(projects))