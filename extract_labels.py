#!/usr/bin/env python
#!/usr/bin/python
import json, os, types
import csv
import pandas as pd
import zipfile

# This method gathers labels from json files.
# Assumes dictionary in info

countlabel=0 #Counts number of instances which did not have a dictionary
count=0 # Counts number of failed instances
for root, dirs, files in os.walk("./tmp/", topdown=False):
    for name in files:
        filename=os.path.join(root, name)
        shortname=filename.split("/")[-1]
        file=open(filename, "r")
        try:
            data = json.loads(file.read())
            print shortname
            try:
                if len(data) > 1:
                    # Create file for labels.
                    labelsfilename=os.path.join("./data/", shortname[0:-5]+'.csv')
                    labelsfile=open(labelsfilename,"w")
                    csvwriter = csv.writer(labelsfile)
                    itr=1 # Indicates that we are on answer 1 and we need to write label names.
                    # For each answer in the json file.
                    for answer in data:
                        #Add labelnames as the first row in csv file.
                        try:
                            # Assume dictionary
                            if itr:
                                labels=answer["info"]
                                labelnames=["user_id"]
                                # Go through all of the keys
                                for key in labels.keys():
                                    labelnames.append(key)
                                csvwriter.writerow(labelnames)
                            #Add labelnames as the first row in csv file.
                            labels=answer["info"]
                            labellist=[answer["user_id"]]
                            for key in labels.keys():
                                labellist.append(labels.get(key))
                            csvwriter.writerow(labellist)
                        except AttributeError:
                            # Assume simply labels 
                            if itr:
                                countlabel+=1
                                print "Not a dictionary but will try if string"+shortname
                                itr=0
                                csvwriter.writerow("user_id", "label")
                            labellist=[answer["user_id"],answer["info"]]
                            csvwriter.writerow(labellist)
                    labelsfile.close()
                    print "Done with ",shortname
                else:
                    print shortname, "is empty"
            except zipfile.BadZipfile:
                print "'Info' does not contain key-value pairs in file", shortname
                count+=1
            # Checks if the json file contains something.
        except ValueError:
            print "Data format incorrect, cannot be opened with a jsonreader (should be dark skies) "+shortname
            count+=1

print "Number of unzipped json files not processed"+ str(count)

                    
            
            
