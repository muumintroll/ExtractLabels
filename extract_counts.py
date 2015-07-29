#!/usr/bin/env python
#!/usr/bin/python
import json, os, types
import csv
import pandas as pd
from pandas.io.json import json_normalize

# This method gathers counts of labels from json files.
#

count=0
for root, dirs, files in os.walk("./tmp/", topdown=False):
    for name in files:
        filename=os.path.join(root, name)
        shortname=filename.split("/")[-1]
        file=open(filename, "r")
        try:
            data = json.loads(file.read())
            # Checks if the json file contains something.
            try:
                if len(data) > 1:
                    # Collect data from 'info' into labels.
                    labels = []
                    for answer in data:
                        labels.append(answer["info"])
                
                    # Count labels
                    #frame=json_normalize(data)
                    #print frame
                    frame=pd.read_json(json.dumps(labels))
                    counts=frame.count()
                    #try:
                        #counts= frame["info"].value_counts()
                        #print counts
                    #except KeyError:
                        #print "Fel"
                
                    # Create file for labels.
                    labelsfilename=os.path.join("./counts/", shortname[0:-5]+'.csv')
                    labelsfile=open(labelsfilename,"w")
                    csvwriter = csv.writer(labelsfile)
                        
                    # Create container for labels and values.
                    labelvalues=[]
                    values=[]
                        
                    # Iterate over labels and counts putting them in different conatiners.
                    iterator=counts.iteritems()
                    for i in iterator:
                        labelvalues.append(i[0])
                        values.append(i[1])
                    
                    # Write to csv file 
                    csvwriter.writerow(labelvalues)
                    csvwriter.writerow(values)
                    labelsfile.close()
                    print "Done with ",shortname
           
            except ValueError:
                print "Objects passed were None "+shortname
                count+=1
        except ValueError:
            print "Data format incorrect "+shortname
            count+=1

print "Number of unzipped json files not processed"+ str(count)

                    
            
            
