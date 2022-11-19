import matplotlib.colors as mcolors, matplotlib.pyplot as plt, re, sys, os, fileinput, shutil
import pandas as pd

def expandPath(workingDir, returner):
    if not os.path.isdir(workingDir):  # we're a file. append ourselves and return!
        returner.append(workingDir)
        return returner
    else: #call our nodes
        for item in os.listdir(workingDir):
            returner = expandPath(workingDir + "/" + item, returner)
        return returner
dir = "../src/bulletins2/autoTMO"
dirList = list(filter(lambda p: ".txt" in p, expandPath(dir, [])))
names = []

for file in dirList:
    with open(file,'r') as f:
        strings = []
        for i in range(50):
            s = f.readline()
            strings.append(s)
            if("Observations:" in s):
                break

        for i in range(len(strings)-2):
            line = strings[len(strings)-1-i].lstrip()
            if(len(line) and line[0]=="2"):
                line = line[:12].rstrip()
                if (line.count(" ") == 1):
                    names.append(line+"\n")
                    break

with open("TMOnames.txt",'w') as f:
    f.writelines(names)
print("Finished successfully!")
