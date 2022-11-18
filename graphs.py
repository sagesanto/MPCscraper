import matplotlib.colors as mcolors, matplotlib.pyplot as plt, re, sys, os, fileinput, shutil
import pandas as pd
from datetime import datetime

graphs = []
graphPath = "graphs/" + str(datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M")) + '/'
os.mkdir(graphPath)
os.mkdir(graphPath+"/barCharts")

class GraphObj:
    global graphPath
    def __init__(self,name,dataframe,xAxis="Date",yAxis="Diagonal Residual",path=graphPath):
        self.name, self.dataframe, self.xAxis, self.yAxis, self.path = name, dataframe, xAxis, yAxis, path
    def graph(self):
        df = self.dataframe
        tmoDf = (df.loc[(df["Obs Code"] == "654") | (df["Obs Code"] == 654)])
        other = (df.loc[(df["Obs Code"] != "654") | (df["Obs Code"] != 654)])  # this sucks
        plt.scatter(other[self.xAxis], other[self.yAxis], c='tab:blue')
        plt.scatter(tmoDf[self.xAxis], tmoDf[self.yAxis], c='tab:orange')
        plt.title(self.name)
        plt.xlabel(self.xAxis)
        plt.ylabel(self.yAxis)
        plt.xticks([])
        plt.savefig(self.path + self.name + ".png")
        plt.clf()


#read in the file
data = pd.read_csv("data3.csv")

current = (data.loc[data['Date'].str.contains('2022')])
tmoCurrent = (current.loc[(current["Obs Code"]=="654")])

alltimeGraph = GraphObj("Alltime Observations",data)
currentGraph = GraphObj("2022 Observations",current)
alltimeTMOGraph = GraphObj("Alltime TMO", (data.loc[(data["Obs Code"]=="654")]))
tmo2022Graph = GraphObj("TMO 2022", (current.loc[(current["Obs Code"]=="654")]))

#graph the manual graphs
graphs = [alltimeGraph, currentGraph, alltimeTMOGraph, tmo2022Graph]

def plotMedians(codes,graphTitle):
    global graphPath
    medDf = pd.DataFrame(columns=["Obs Code", "Name", "Median Diagonal Error"])
    for code in codes.keys():
        df = current.loc[current["Obs Code"]==code]
        lis = [code, codes[code],df["Diagonal Residual"].median()]
        medDf.loc[len(medDf.index)] = lis
    medDf = medDf.sort_values('Median Diagonal Error')
    plt.bar(medDf['Name'],medDf["Median Diagonal Error"])
    plt.title(graphTitle)
    plt.ylabel("Median Diagonal Error (arcseconds)")
    plt.xticks(fontsize=5, rotation=270)
    plt.savefig(graphPath+"/barCharts/"+graphTitle+".png")
    plt.clf()

for file in os.listdir("obsCodesToPlot"):
    #read in line numbers, if Obs Code in [list]
    codes = {}
    with open("obsCodesToPlot/"+file,'r') as f:
        for line in f:
            line = line.replace('\n','')
            split = line.split(", ")
            codes[split[0]] = split[1]
    currentDf = current.loc[current["Obs Code"].isin(codes)]
    plotMedians(codes,file[:-4])
    graphs.append(GraphObj(file[:-4], currentDf))

for graph in graphs:
    graph.graph()
