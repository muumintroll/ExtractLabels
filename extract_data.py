#!/usr/bin/env python

import json, os, zipfile, types
count=0;
for root, dirs, files in os.walk("./output/", topdown=False):
    for name in files:
        filename=os.path.join(root, name)
        if len(filename.split("/"))==4 and filename.split("/")[-1]=="task_run.zip":
            projectname=filename.split("/")[-2]
            file=open(filename, "r")
            # Try unzipping.
            try:
                zip = zipfile.ZipFile(file)
                target_dir = "tmp"
                for name in zip.namelist():
                    # Max size limit for unzipped file. Change this if you like. My computer cannot unzip very big files.
                    if file.tell()<131072:
                        zip.extract(name, target_dir)
                        f = open(target_dir+"/"+name, "r")
                        data = json.loads(f.read())
                        # Checks if the json file contains something.
                        if len(data) > 1:
                            # Creates a file with the labels of the users.
                            answerfile=open(os.path.join("labels",name), "w")
                            count=count+1 #Counts number of files with data.
                            print "File nbr %d , and name %s",count,name
                            # Goes through each worker's answer.
                            for answer in data:
                                # The worker's answer always seemed to be saved as a value for the info key.
                                label=answer["info"]
                                try:
                                    answerfile.write(label+" \n")
                                except TypeError:
                                    #The answer is saved as a hierarchy.
                                    try:
                                        for key in label.keys():
                                            try:
                                                answerfile.write(key+" "+label[key]+"\n")
                                            except TypeError:
                                                # Numbers as values.
                                                answerfile.write(key+" "+str(label[key])+"\n")
                                            except UnicodeEncodeError:
                                                print "Not unicode key."
                                                print label
                                    #The answer is saved as a list.
                                    except AttributeError:
                                        for subanswer in label:
                                            try:
                                                for key in subanswer.keys():
                                                    try:
                                                        answerfile.write(key+" "+subanswer[key]+"\n")
                                                    except TypeError:
                                                        # Numbers as values.
                                                        answerfile.write(key+" "+str(subanswer[key])+"\n")
                                                    except UnicodeEncodeError:
                                                        print "Not unicode subanswer."
                                                        print subanswer
                                            except AttributeError:
                                                try:
                                                    answerfile.write(subanswer)
                                                except UnicodeEncodeError:
                                                    print "Not unicode subanswer."
                                                    print subanswer
                                                except TypeError:
                                                    try:
                                                        for subsubanswer in subanswer:
                                                            print type(subsubanswer)
                                                            answerfile.write(subsubanswer)
                                                    except TypeError:
                                                        print "Type of subanswer is not a hierarcy or a word"
                                                    except UnicodeEncodeError:
                                                        print "Not unicode subsubanswer."
                                                        print subsubanswer
                                                    
                                # Not unicode label.
                                except UnicodeEncodeError:
                                    print "Not unicode label."
                                    print label
                                    break
                            answerfile.close()
            except zipfile.BadZipfile:
                count=count+0




