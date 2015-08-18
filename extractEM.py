#!/usr/bin/env python
#!/usr/bin/python
import json, os, types
import numpy as np
import csv
#import pandas as pd
import zipfile
import types
import sys
#
# This script gathers labels from json files.
# Assumes dictionary structure in info.
#

# Variables given by user are initialized
filename=""
labelfields=[]#"classification"
stopping_criteria=0.01
root=""
output_file="output"

# Handle command line arguments.
i=0
previous_input=""
if len(sys.argv)==2:
        if i>0:
            filename=sys.argv[1]
else:
    for arg in sys.argv:
        if i>0:
            if previous_input=="-f":
                filename=arg
            elif previous_input=="-r":
                root=arg
            elif previous_input=="-sc":
                stopping_criteria=float(arg)
            elif previous_input=="-lf":
                labelfields.append(arg)
            elif previous_input=="-o":
                output_file=arg
        i+=1
        previous_input=arg
# If filename is not given as a command line argument ask for it.        
if len(filename)==0:        
    filename=raw_input("Please give a filename for a file to be processed \n")
    
# Open file.
filename=os.path.join(root, filename)
file=open(filename, "r")

# Read json file.
data = json.loads(file.read())
file.close()

if len(data) > 1: # If file contains something.
    
# This is necessary only if not given by input.
# Gather all labelfields.    
    if len(labelfields)==0:
        answer=data[0]
        labelfields=answer["info"].keys()
        labelfield=labelfields[1]
        print labelfield
    
# This is necessary only if not given by input.
# Gather all unique task ids, user ids and labelvalues.
    task_ids=set()
    labelvalues=set()
    userids=set()
    # Gather all of the unique labels.
    for answer in data:
        # Checks that the labelfield is present in this data.
        if labelfield in answer["info"].keys():
            labelvalues.add(answer["info"][labelfield])
            task_ids.add(answer["task_id"])
            userids.add(answer["user_id"])

    # Convert set to list for keeping track of indexes.
    task_ids=list(task_ids)
    labelvalues=list(labelvalues)
    userids=list(userids)
    
    #############################################################################################################
    #
    # Algorithm starts here.
    # 
    
    # Necessary to keep track of which index is equivalent to which value.
    nbr_labelvalues=len(labelvalues)
    nbr_task_ids=len(task_ids)
    nbr_users=len(userids)
    
    # Initiate matrices and tensors necessary in algorithm.
    n=np.zeros(shape=[nbr_task_ids, nbr_labelvalues,nbr_users], dtype=int)
    p=np.zeros(shape=[nbr_labelvalues],dtype=float)
    pi=np.zeros(shape=[nbr_labelvalues,nbr_labelvalues,nbr_users], dtype=float)
    T=np.zeros(shape=[nbr_task_ids, nbr_labelvalues], dtype=float)
    T_old=T.copy()
    
    
    # Create n matrix.
    for answer in data:
        if labelfield in answer["info"].keys():
            n[task_ids.index(answer["task_id"]), labelvalues.index(answer["info"][labelfield]), userids.index(answer["user_id"])]+=1
       
    # Calculate initial T matrix.
    count_per_label_and_task=np.ndarray.sum(n,axis=2)
    count_per_label=np.ndarray.sum(count_per_label_and_task,axis=1)
    for i in xrange(0, nbr_task_ids):
        if count_per_label[i]!=0:
            T[i,:]=count_per_label_and_task[i,:]/count_per_label[i]
    #--------------------------------------------------------------------------------------------------------------
    # Loop stats here.
    while np.linalg.norm(T_old-T)>stopping_criteria:
        T_old=T.copy()
        
        # Update p and pi matrices.
        for j in xrange(0, nbr_labelvalues):
            tmp2=T[:,j]
            p[j]=sum(tmp2)/nbr_task_ids
            for k in xrange(0,nbr_users):
                for l in xrange(0, nbr_labelvalues):
                    tmp=T[:,j]*n[:,l,k]
                    pi[j,l,k]=sum(tmp)
                normalizer=sum(pi[j,:,k])
                # Normalize pi matrix
                if normalizer!=0:
                    pi[j,:,k]=pi[j,:,k]/normalizer

        # Update T matrix.
        for i in xrange(0, nbr_task_ids):
            normalizer=0
            for j in xrange(0, nbr_labelvalues):
                T[i,j]=1
                for l in xrange(0, nbr_labelvalues):
                    for k in xrange(0,nbr_users ):
                        T[i,j]=T[i,j]*(pi[j,l,k]**n[i,l,k])*p[j]
                        normalizer=normalizer+T[i,j]
            # Normalize T matrix           
            if normalizer!=0:
                T[i,:]=T[i,:]/normalizer
                
                
        print T
        for k in xrange(0,nbr_users):
            print pi[:,:,k]
        print np.linalg.norm(T_old-T)
        
print T