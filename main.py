# format for bulletins between 01-99: https://www.minorplanetcenter.net/mpec/K[LAST TWO DIGITS OF YEAR]/K[LAST TWO DIGITS OF YEAR][THREE CHAR BULLETIN CODE].html
# example for bulletin 2021-T62: https://www.minorplanetcenter.net/mpec/K21/K21T62.html
# Each letter ruins up to some number (?) before ticking over to the next, but the urls over 100 are different.
#format for bulletins between 100-150: [Letter][A/B/C/D/E][last digit]
# A0 = 100, B2 = 112, C9 = 129, etc
# potential flow: (gather all bulletins -> run parse on each of gathered bulletins) / repeat(gather a bulletin -> run parse)  -> generate stats
# or: repeat(gather->parse->small stats report) and then leave compilation of those stats reports more open ended
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import re, sys, os, fileinput
import pandas as pd
# This opens, reads, cleans, and saves a webpage:
# url = "https://www.minorplanetcenter.net/mpec/K21/K21T62.html"
# page = urlopen(url)
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")
# soup = bs(html, 'html.parser')
# clean = (soup.get_text().replace('\n\n\n',''))
# with open("decodedhtml.txt",'w') as f:
#     f.write(clean)
#     f.close()



# with open("decodedhtml.txt", 'r') as f: #temporary to avoid spamming mpc while testing
#     html = f.read()
# soup = bs(html, 'html.parser')
# clean = (soup.get_text().replace('\n\n\n',''))
# print(clean)
# print("*****\n\n\n\n\n")
# observations = re.search("Observer details:(?s).*Orbital elements:",clean)
# print(("654" in observations.group()))
