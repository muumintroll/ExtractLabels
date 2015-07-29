#!/usr/bin/env python
#!/usr/bin/python
import json, os, types
import numpy as np
import csv
#import pandas as pd
import zipfile
import types

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
            # Put all ansers in a dictionary.
            taskids=set()
            labelvalues=set()
            # Gather all of the unique labels.
            for answer in data:
                labelvalues.add(answer["info"][labelfield])
                task_ids.add(answer["task_id"])
            # Convert set to list for keeping track of indexes.
            task_ids=list(task_ids)
            labelvalues=list(labelvalues)
            n=np.zeros(shape=[len(task_ids), len(labelvalues)], dtype=int)
            # Create n matrix.
            for answer in data:
                n[task_ids.index(answer["task_id"]), labelvalues.index(answer["info"][labelfield])]+=1
            # Calculate T matrix.
            T=n.copy()
            count_per_task=np.sum(n,axis=1)
            for i in xrange(0, len(task_ids)):
                T[i,:]=T[i,:]/count_per_task[i]
            
                
            
                        
    #for uid in dictionary.keys()
                 
            
    except zipfile.BadZipfile:
        print "'Info' does not contain key-value pairs in file"
            # Checks if the json file contains something.
except zipfile.BadZipfile:
    print "Data format incorrect, cannot be opened with a jsonreader (should be dark skies) "    



                    
            
            
