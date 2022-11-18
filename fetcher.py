# format for bulletins between 01-99: https://www.minorplanetcenter.net/mpec/K[LAST TWO DIGITS OF YEAR]/K[LAST TWO DIGITS OF YEAR][THREE CHAR BULLETIN CODE].html
# example for bulletin 2021-T62: https://www.minorplanetcenter.net/mpec/K21/K21T62.html
# Each letter runs up to some number (?) before ticking over to the next, but the urls over 100 are different.
#format for bulletins 100+: [Letter][A/B/C/D/E...][last digit]
# A0 = 100, B2 = 112, C9 = 129, etc

# this script downloads and cleans every MPEC bulletin in a specified date range.

from bs4 import BeautifulSoup as bs
import urllib
from urllib.request import urlopen
import re
import sys
import os
import fileinput
import pandas as pd
import random
import time

failures = []
# check and see if a bulletin exists at a given URL. if it does, return the cleaned text. otherwise, return ''
def tryUrl(url):
    global failures
    count = 0
    while True:
        try:
            page = urlopen(url)
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")
            soup = bs(html, 'html.parser')
            clean = (soup.get_text().replace('\n\n\n', ''))
            return clean
        except urllib.error.HTTPError as e:
            if e.code == 404: # this just means we reached the end of a given series
                return ''

            print("HTTP EXCEPTION WITH " + url + ": " + e.code)
            time.sleep(1) #check if disconnected, retry twice
            count += 1
            if count >= 3:
                failures.append(url)
                return ''
        except Exception as e: #check if disconnected, retry twice
            print("EXCEPTION WITH " + url + ": " + e)
            time.sleep(1)
            count += 1
            if count >= 3:
                failures.append(url)
                return ''


# record in a dataFrame the first non-working extension in a given letter in a given year is
def recordLimit(year, c, ext, dataFrame):
    print("Found limit for " + c + ": " + ext)
    dataFrame.loc[len(dataFrame.index)] = [year, c, ext]
    return dataFrame


def dirtyWork(year, c, ext, limitsDf, path,obsDf):
    time.sleep((random.randint(1, 10))/100) #no ddos please and thank you
    url = "https://www.minorplanetcenter.net/mpec/K" + year + "/K" + year + ext + ".html"
    text = tryUrl(url)
    if text == '':
        print("Found limit: " + year + " " + ext)
        limitsDf = recordLimit(year, c, ext, limitsDf) # these aren't currently being reassigned out of this scope
        return False
    else: #this bulletin exists
        orbitUpdates = re.search("DAILY ORBIT", text) # check and see if this is a daily orbit update
        if orbitUpdates is not None:
            path += "/dailyBulletins"
        else: #these are mutually exclusive, as far as im concerned
            observations = re.search("Observer details:(?s).*Orbital elements:", text) # check and see if provided observer code is in the bulletin's observer section, if an observer section exists
            if observations is not None:
                if re.search(obsCode, observations.group()) is not None:
                    obsDf.loc[len(obsDf.index)] = [url]
                    path += "/autoTMO"

        fullpath = path + "/" + year
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)
        with open(fullpath + "/" + ext + ".txt", 'w') as f:
            try:
                f.write(text)
                f.close()
            except:
                print("!!! Write failed on " + url + " !!!")
        return True

# there's some redundant code here that's pretty painful

# get observer code and start and end year
if(len(sys.argv) < 4):
    raise Exception("usage: fetcher.py [observatory code (three alphanumeric characters, all caps)] [last two digits of start year (2000 onward)] [last two digits of end year (2000 onward)]")
obsCode = sys.argv[1]
startYear = sys.argv[2]
endYear = sys.argv[3]


# setup
path = "../src/bulletins2" #changed to 2 because im running it again -_-
if not os.path.exists(path):
    os.mkdir(path)
    os.mkdir(path+"/autoTMO")
    os.mkdir(path+"/dailyBulletins")

obsDf = pd.DataFrame(columns=['URL'])
limitsDf = pd.DataFrame(columns=['Year','Letter','Max'])
years = []
for i in range(int(startYear)-1,int(endYear)):
    years.append(i+1) # god i hope this works it makes sense in my head (range excludes the last year, includes the first
print(years)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWWXYZ"

# loop over each year and fetch each bulletin (which may or may not exist) corresponding to an extension code
for year in years:
    cont = True
    year = str(year)
    os.mkdir(path+"/"+year)
    for c in alphabet:
        cont = True
        for i in range(99):
            ext = c+str(i+1).zfill(2)
            if not dirtyWork(year,c,ext,limitsDf,path,obsDf):
                cont = False
                break
        if cont:
            for e in alphabet: # now start looking for bulletins numbered over 99
                for i in range(9):
                    ext = c + e + str(i)
                    if not dirtyWork(year, c, ext, limitsDf,path,obsDf):
                        cont = False
                        break
                if not cont:
                    break
print("Failures: ",failures)
obsDf.to_csv(path + "/urlsContainingObsCode.csv", index=False)
limitsDf.to_csv(path + "/maxIndex.csv", index=False)
print("All done!")
