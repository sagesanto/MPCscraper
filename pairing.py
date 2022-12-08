import matplotlib.colors as mcolors, matplotlib.pyplot as plt, math, re, sys, os, fileinput, shutil, random
import pandas as pd
from datetime import datetime

raw = pd.read_csv("revisedTMO_Bulletins.csv")

raw['Diagonal Residual'] = (raw["Residual RA"]**2+raw["Residual Dec"]**2)**(1/2)

print(raw)
raw.to_csv("diagonalRevisedTMO_Bulletins.csv")
# def sortOut(row,dataFrame):
#     date = row["Date"]
#     print(date)
#     return true
#
# raw.loc[lambda row: sortOut(row,raw)]
# twentyTwo = raw.loc[[raw['Date'].str.contains('2022')]]
# twentyTwo.to_csv("2022_Observations.csv")