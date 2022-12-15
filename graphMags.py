
import matplotlib.colors as mcolors, matplotlib.pyplot as plt, math, re, sys, os, fileinput, shutil, random, numpy as np
import pandas as pd
# from pandas_profiling import ProfileReport
from datetime import datetime

show = False
useColors = False
graphs = []
plots = []
graphPath = "graphs/decemberMags" + str(datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S")) + '/'
#initialize colors
if useColors:
    colors = [line.replace("\n",'') for line in open("colors.txt")]

class GraphObj:
    def __init__(self,name,dataframe,xAxis="Date",yAxis="Diagonal Residual",path=graphPath):
        self.name, self.dataframe, self.xAxis, self.yAxis, self.path = name, dataframe, xAxis, yAxis, path
    def graph(self):
        global graphPath
        df = self.dataframe
        codes = list(df["Obs Code"].unique())
        #move TMO to the back so it hopefully gets graphed over everything else:
        if "654" in codes:
            codes.remove("654")
            codes.append("654")
        colorDict = createLegend(codes)
        fig, ax = plt.subplots()
        for code in codes:
            mark = 'x' if code=="654" else 'o'
            markerSize = 9 if code=="654" else 1
            tempDf = df.loc[df["Obs Code"]==code]
            ax.scatter(tempDf[self.xAxis],tempDf[self.yAxis],c=colorDict[code],label=code, s=markerSize, marker=mark)
            if code=="654":
                z = np.polyfit(tempDf[self.xAxis], tempDf[self.yAxis], 2)
                p = np.poly1d(z)
                plt.plot(sorted(tempDf[self.xAxis].values.tolist()), (p(sorted(tempDf[self.xAxis].values.tolist()))), "r-o",markersize=1)
        # ax.legend(loc='upper center', ncol=5, fancybox=True, shadow=True)
        plt.title(self.name+" "+self.yAxis)
        plt.xlabel(self.xAxis)
        plt.ylabel(self.yAxis)
        plt.ylim(-0.1,2.5)
        plt.xticks()
        plt.tight_layout()
        plt.savefig(self.path + self.name +" "+self.yAxis +".png")
        if show:
            plt.show()
        plt.clf()

def createLegend(keys):
    global useColors
    # for gradient
    if useColors:
        global colors
        return {keys[i]: colors[i] for i in range(len(keys))}
    # monochromatic except TMO
    colors = ["#0606A0"]*len(keys)
    dict = {keys[i]: colors[i] for i in range(len(keys))}
    dict["654"] = "#FFAB00"
    return dict

os.mkdir(graphPath)

data = pd.read_csv("diagonalMagsTMO_Bulletins.csv")
current = (data.loc[data['Date'].str.contains('2022')])

for file in os.listdir("obsCodesToPlot"):
    #read in line numbers, if Obs Code in [list]
    codes = {}
    with open("obsCodesToPlot/"+file,'r') as f:
        for line in f:
            line = line.replace('\n','')
            split = line.split(", ")
            codes[split[0]] = split[1]
    currentDf = current.loc[current["Obs Code"].isin(codes)]
    # profile = ProfileReport(currentDf, title="Profile of 2022 Observations by Top Follow Ups from Bulletins that Include TMO")
    # profile.to_file("report"+file.replace('.txt','') + ".html")
    currentDf.to_csv("csvs/"+file.replace('.txt','')+".csv")
    graphs.append(GraphObj(file[:-4], currentDf,xAxis="Magnitude",yAxis="Diagonal Residual"))

for graph in graphs:
    graph.graph()

os.startfile(os.path.normpath(graphPath))