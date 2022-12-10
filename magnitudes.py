import re, sys, os, fileinput, shutil
import pandas as pd
from random import shuffle

#also: hash to make unique id using info in column (make sure to write a reverser too)

def regExSearch(start,end,string):
    returner = re.search(start+"(?s).*?"+end, string)
    if returner:
        return returner.group()
    else:
        return None

def magnitudes(lines):
    mags = regExSearch("(?<=Observations:\n)", "(?=\n(\n| \n))", lines)
    magSplit = (mags.split("\n"))
    magClean = []
    for l in magSplit:
        mid = l.split("          ")
        magClean.extend(mid)
    magClean = magClean[1::2]
    print(magClean)
    magDf = pd.DataFrame(columns=['Magnitude','Obs Code'])
    for str in magClean:
        obsCode = str[-3:]
        mag = str[:5].strip(" ")
        mag = float(mag) if mag else None
        magDf.loc[len(magDf.index)] = [mag,obsCode]
    return magDf


with open("../MPCscraper/testBulletins/B09.txt", 'r') as f:
    lines = f.read()  # whole text
print(magnitudes(lines))

