import matplotlib.colors as mcolors, matplotlib.pyplot as plt, math, re, sys, os, fileinput, shutil, random
import pandas as pd
from datetime import datetime


graphs = []
graphPath = "graphs/" + str(datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S")) + '/'


class GraphObj:
    global graphPath
    def __init__(self,name,dataframe,xAxis="Date",yAxis="Diagonal Residual",path=graphPath):
        self.name, self.dataframe, self.xAxis, self.yAxis, self.path = name, dataframe, xAxis, yAxis, path
    def graph(self):
        df = self.dataframe
        codes = list(df["Obs Code"].unique())
        colorDict = createLegend(codes)
        fig, ax = plt.subplots()

        for code in codes:
            tempDf = df.loc[df["Obs Code"]==code]
            ax.scatter(tempDf[self.xAxis],tempDf[self.yAxis],c=colorDict[code],label=code)
        ax.legend(loc='upper center', ncol=5, fancybox=True, shadow=True)
        plt.title(self.name)
        plt.xlabel(self.xAxis)
        plt.ylabel(self.yAxis)
        plt.xticks([])
        plt.tight_layout()
        plt.savefig(self.path + self.name + ".png")
        plt.clf()

def createLegend(keys):
    colors = mcolors.XKCD_COLORS
    colors = list(colors.values())
    random.shuffle(colors)
    colors = colors[:len(keys)]
    return {keys[i]: colors[i] for i in range(len(keys))}

def plotMedians(codes,graphTitle):
    global graphPath
    medDf = pd.DataFrame(columns=["Obs Code", "Name", "Median Diagonal Error"])
    for code in codes.keys():
        df = current.loc[current["Obs Code"]==code]
        lis = [code, codes[code],df["Diagonal Residual"].median()]
        medDf.loc[len(medDf.index)] = lis
    medDf = medDf.sort_values('Median Diagonal Error')
    if graphTitle == "Maunakea":
        print(medDf)
    fig,ax = plt.subplots()
    codes = list(medDf["Obs Code"].unique())
    colorDict = createLegend(codes)
    fig, ax = plt.subplots()
    for code in codes:
        tempDf = medDf.loc[medDf["Obs Code"] == code]
        bar = ax.bar(tempDf["Name"], tempDf["Median Diagonal Error"], color=colorDict[code])
        ax.bar_label(bar, size=5, labels=['{:g}'.format(float('{:.2g}'.format(i))) for i in tempDf["Median Diagonal Error"]])
    plt.title(graphTitle)
    plt.ylabel("Median Diagonal Error (arcseconds)")
    plt.xticks(fontsize=5, rotation=270)
    x,y = medDf['Name'].values.tolist(), medDf["Median Diagonal Error"].values.tolist()

    # for index in range(len(bar)):
    #     ax.text(x[index], y[index], roundToN(y[index],2), size=4)
    plt.savefig(graphPath+"/barCharts/"+graphTitle+".png")
    plt.clf()

#2018-A27 is an example of a repeat

#read in the file
os.mkdir(graphPath)
os.mkdir(graphPath+"/barCharts")


data = pd.read_csv("data3.csv")
current = (data.loc[data['Date'].str.contains('2022')])
tmoCurrent = (current.loc[(current["Obs Code"]=="654")])

alltimeGraph = GraphObj("Alltime Observations",data)
currentGraph = GraphObj("2022 Observations",current)
alltimeTMOGraph = GraphObj("Alltime TMO", (data.loc[(data["Obs Code"]=="654")]))
tmo2022Graph = GraphObj("TMO 2022", (current.loc[(current["Obs Code"]=="654")]))

#graph the manual graphs
graphs = [alltimeGraph, currentGraph, alltimeTMOGraph, tmo2022Graph]



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
