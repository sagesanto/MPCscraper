import re, sys, os, fileinput, shutil
import pandas as pd
from random import shuffle

dateDict = ["Jan","Feb", "Mar", "Apr", "May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def is_sorted(data):
    return all(a <= b for a, b in zip(data, data[1:]))

def bogosort(data):
    while not is_sorted(data):
        shuffle(data)
    return data

def regExSearch(start,end,string):
    returner = re.search(start+"(?s).*?"+end, string)
    if returner:
        return returner.group()
    else:
        return None

def datefinder(text):
    date = regExSearch("Issued ",",",text)
    if date is None:
        print("Oops, couldn't find a date!")
        print(text)
        return ''
    dateComps = date.split(' ')[1:]
    month=str(dateDict.index(dateComps[1][:3])+1)
    date = month+"/"+dateComps[2][:-1]+"/"+dateComps[0]
    return date

def residuals(lines):
    residual = regExSearch("(?<=Residuals in seconds of arc\n)","(?=\n(\n| ))", lines)  # check and see if provided observer code is in the bulletin's observer section, if an observer section exists
    if not residual:
        return None
    residual = (residual.replace("(", " ")).replace(")", " ")
    resLines = residual.split('\n')
    obs = []
    for l in resLines:
        mid = l.split("    ")
        for s in mid:
            sl = s.split(" ")
            obs.append([i for i in sl if i])
    try:
        interDf = pd.DataFrame(obs, columns = ['Date', 'Code', 'Res RA','Res Dec'])
        interDf['Res RA'], interDf['Res Dec'] = interDf['Res RA'].apply(lambda x: float(x[:-1])), interDf['Res Dec'].apply(lambda x: float(x[:-1]))
        returner = ((interDf.to_numpy()).tolist())
        return returner
        # return [interDf['Code'],interDf['Res RA'], interDf['Res Dec']]
        # tmo, other = interDf.loc[interDf['Code']=="654"], interDf.loc[interDf['Code']!=654] #horrible
        # tmoAvRA, tmoAvDec = tmo['Res RA'].mean(), tmo['Res Dec'].mean()
        # otherAvRA, otherAvDec = other['Res RA'].mean(), other['Res Dec'].mean()
        # return [tmoAvRA, tmoAvDec, otherAvRA, otherAvDec]
    except Exception as e:
        print(e)
        return []

#the data we have right now is gathered from reading across a three-column row. sort it into being in the original vertical order
def reorderDataframe(dataframe):
    newDf = pd.DataFrame(columns=dataframe.columns.values.tolist())
    for i in range(3):
        for j in range(int(len(dataframe.index) / 3)):
            if ((3 * j + i) <= len(dataframe.index) - 1):
                newDf.loc[len(newDf.index)] = dataframe.iloc[3 * j + i]
    return newDf

#this is just another (perhaps more readable) way to do what reorderDataframe does
def reorderBySort(dataframe):
    excess = 3 - (len(dataframe.index) % 3)
    length = int(len(dataframe.index) / 3) + 1
    list = []
    for i in range(length):
        for j in range(3):
            list.append(i + j * length + 1)
    for n in range(excess):
        list.remove(max(list))
    dataframe['Num'] = list
    return dataframe.sort_values(by='Num')


# recursively gather a list of the paths of the files in our subdirectories
def expandPath(workingDir, returner):
    if not os.path.isdir(workingDir):  # we're a file. append ourselves and return!
        returner.append(workingDir)
        return returner
    else: #call our nodes
        for item in os.listdir(workingDir):
            returner = expandPath(workingDir + "/" + item, returner)
        return returner

df = pd.DataFrame(columns=['Date','Bulletin', 'Obs Code', 'Residual RA', 'Residual Dec'])

dir = "../src/useBulletins/autoTMO/22"
dirList = list(filter(lambda p: ".txt" in p, expandPath(dir, [])))
for file in dirList:
    with open(file,'r') as f:
        lines = f.read() #whole text
    text = [i for i in lines.split('\n') if i!='\n'] #text as lines
    date = datefinder(text[0])
    num = text[0][9:18] # cringe hardcode
    toInsert = [date,num]
    res = residuals(lines)
    if res:
        for list in res:
            try:
                df.loc[len(df.index)] = (toInsert+list[1:])
            except Exception as e:
                print("Failed to insert ", toInsert+list, ", got ", e)
        print("Completed " + file)
    else:
        print("Oops - no residuals for " + file)
print(df)
df.to_csv("../src/revisedTMO_Bulletins.csv", index=False)
# except Exception as e:
#     df.to_csv("../src/stats.csv", index=False)
#     print("Oops! Exception! Saving df. Exception: ",e)

# xargs -a file_list.txt mv -t /path/to/dest


