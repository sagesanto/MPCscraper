#just get rid of some unnecessary stuff
#assume directory "bulletins" with downloaded bulletins
# "M.P.E.C. " apppears at the beginning of the content that we're actually interested in. let's get rid of everything before that
from bs4 import BeautifulSoup as bs
import urllib
from urllib.request import urlopen
import re, sys, os, fileinput


#i really need to make a util library...
# recursively gather a list of the paths of the files in our subdirectories
def expandPath(workingDir, returner):
    if not os.path.isdir(workingDir):  # we're a file. append ourselves and return!
        returner.append(workingDir)
        return returner
    else: #call our nodes
        for item in os.listdir(workingDir):
            returner = expandPath(workingDir + "/" + item, returner)
        return returner

dir = "../src/bulletins2"
dirList = list(filter(lambda p: ".txt" in p, expandPath(dir, [])))
for filename in dirList:
    with open(filename,'r') as f:
        print(filename)
        start = False
        with open(filename,'r') as f:
            lines = f.readlines()
            f.close()
        with open(filename,'w') as f:
            for line in lines:
                if "M.P.E.C" in line:
                    start = True
                if start:
                    f.write(line)
            f.close()
print("Finished!")

