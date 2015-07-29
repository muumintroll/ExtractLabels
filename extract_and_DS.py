#!/usr/bin/env python
#!/usr/bin/python
import json, os, types
import csv
import pandas as pd
import zipfile

# This method gathers labels from json files.
# Assumes dictionary in info

filename=raw_input("Write a filename \n")
file=open(filename, "r")
#labelfield=raw_input("Write the key of the label you are interested in \n")
labelfield="classification"
try:
    data = json.loads(file.read())
    file.close()
    try:
        if len(data) > 1:
        # Create file for labels.
            dictionary={}
            task_ids=set()
            # Put all ansers in a dictionary
            no_uid_counter=-1
            for answer in data:
                task_ids.update(answer["task_id"])
                key=answer["user_id"]
                # No user id
                if key is None:
                    key=no_uid_counter
                    no_uid_counter=no_uid_counter-1
                # An object with this user id has not been added previously
                if dictionary.get(key) is None:
                    dictionary[key]={answer["task_id"]:[answer["info"]]}
                else:
                    # An object with this user id and task id has not been added previously
                    if dictionary.get(key).get(answer["task_id"]) is None:
                        dictionary.get(key).update({answer["task_id"]:[answer["info"]]})
                    else:
                        dictionary.get(key).get(answer["task_id"]).append(answer["info"])
            labels=set()
            sum=0
            # Gather all of the labels to the same place
            for dic in dictionary.values():
                labels.add(val[labelfield] for list in dic.values() for val in list)
                
                ## Estimation of T's
            T={}
            for task_id in task_ids:
                T[task_id]={}
                for label in labels:
                    T.get(task_id).update({label:})
                        
    #for uid in dictionary.keys()
                 
            
    except zipfile.BadZipfile:
        print "'Info' does not contain key-value pairs in file"
            # Checks if the json file contains something.
except zipfile.BadZipfile:
    print "Data format incorrect, cannot be opened with a jsonreader (should be dark skies) "    



                    
            
            
