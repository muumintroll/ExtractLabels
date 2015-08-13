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

# Read json file.
data = json.loads(file.read())
file.close()
if len(data) > 1:
# This is necessary only if not given by input.
# Gather all unique task ids, user ids and labelvalues.
    task_ids=set()
    labelvalues=set()
    userids=set()
    # Gather all of the unique labels.
    for answer in data:
        labelvalues.add(answer["info"][labelfield])
        task_ids.add(answer["task_id"])
        userids.add(answer["user_id"])
    # Convert set to list for keeping track of indexes.
    task_ids=list(task_ids)
    labelvalues=list(labelvalues)
    userids=list(userids)
    # This is necessary.
    nbr_labelvalues=len(labelvalues)
    nbr_task_ids=len(task_ids)
    nbr_users=len(userids)
    #Initiate vectors
    n=np.zeros(shape=[nbr_task_ids, nbr_labelvalues,nbr_users], dtype=int)
    p=np.zeros(shape=[nbr_labelvalues],dtype=float)
    pi=np.zeros(shape=[nbr_labelvalues,nbr_labelvalues,nbr_users], dtype=float)
    T=np.zeros(shape=[nbr_task_ids, nbr_labelvalues], dtype=float)
    T_old=T.copy()
    # Create n matrix.
    for answer in data:
        n[task_ids.index(answer["task_id"]), labelvalues.index(answer["info"][labelfield]), userids.index(answer["user_id"])]+=1
    # Calculate initial T matrix.
    count_per_label_and_task=np.ndarray.sum(n,axis=2)
    count_per_label=np.ndarray.sum(count_per_label_and_task,axis=1)
    for i in xrange(0, nbr_task_ids):
        if count_per_label[i]!=0:
            T[i,:]=count_per_label_and_task[i,:]/count_per_label[i]
    
    while np.linalg.norm(T_old-T)>0:
        T_old=T.copy()
        for j in xrange(0, nbr_labelvalues):
            tmp2=T[:,j]
            p[j]=sum(tmp2)/nbr_task_ids
            for k in xrange(0,nbr_users):
                for l in xrange(0, nbr_labelvalues):
                    tmp=T[:,j]*n[:,l,k]
                    pi[j,l,k]=sum(tmp)
                normalizer=sum(pi[j,:,k])
                if normalizer!=0:
                    pi[j,:,k]=pi[j,:,k]/normalizer


        for i in xrange(0, nbr_task_ids):
            normalizer=0
            for j in xrange(0, nbr_labelvalues):
                T[i,j]=p[j]
                for l in xrange(0, nbr_labelvalues):
                    for k in xrange(0,nbr_users ):
                        T[i,j]=T[i,j]*(pi[j,l,k]**n[i,l,k])
                        normalizer=normalizer+T[i,j]
            if normalizer!=0:
                T[i,:]=T[i,:]/normalizer

        print np.linalg.norm(T_old-T)
        
print T
                        
      
                        
    
    #for uid in dictionary.keys()