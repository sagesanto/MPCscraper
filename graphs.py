import matplotlib.colors as mcolors, matplotlib.pyplot as plt, math, re, sys, os, fileinput, shutil, random, numpy as np
import pandas as pd
# from pandas_profiling import ProfileReport
from datetime import datetime

useColors = False
graphs = []
graphPath = "graphs/" + str(datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S")) + '/'
#initialize colors
if useColors:
    colors = [line.replace("\n",'') for line in open("colors.txt")]

class GraphObj:
    global graphPath
    def __init__(self,name,dataframe,xAxis="Date",yAxis="Diagonal Residual",path=graphPath):
        self.name, self.dataframe, self.xAxis, self.yAxis, self.path = name, dataframe, xAxis, yAxis, path
    def graph(self):
        df = self.dataframe
        codes = list(df["Obs Code"].unique())
        #move TMO to the back so it hopefully gets graphed over everything else
        if "654" in codes:
            codes.remove("654")
            codes.append("654")
        colorDict = createLegend(codes)
        fig, ax = plt.subplots()
        for code in codes:
            tempDf = df.loc[df["Obs Code"]==code]
            ax.scatter(tempDf[self.xAxis],tempDf[self.yAxis],c=colorDict[code],label=code)
        # ax.legend(loc='upper center', ncol=5, fancybox=True, shadow=True)
        plt.title(self.name)
        plt.xlabel(self.xAxis)
        plt.ylabel(self.yAxis)
        plt.xticks([])
        plt.tight_layout()
        plt.savefig(self.path + self.name + ".png")
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


def plotMedians(codes,graphTitle):
    global graphPath
    calcDf = pd.DataFrame(columns=["Obs Code", "Name", "Median Diagonal Error","Average Diagonal Error"])
    
    for code in codes.keys():
        df = current.loc[current["Obs Code"]==code]
        lis = [code, codes[code],df["Diagonal Residual"].median(),df["Diagonal Residual"].mean()]
        calcDf.loc[len(calcDf.index)] = lis
    for column in ["Median Diagonal Error","Average Diagonal Error"]:
        type = column.split(" ")[0]
        calcDf = calcDf.sort_values(column)
        fig,ax = plt.subplots()
        codes = list(calcDf["Obs Code"].unique())
        colorDict = createLegend(codes)
        fig.set_size_inches(18.5, 10.5)
        fig, ax = plt.subplots()
        for code in codes:
            tempDf = calcDf.loc[calcDf["Obs Code"] == code]
            bar = ax.bar(tempDf["Name"], tempDf[column], color=colorDict[code],label=code)
            ax.bar_label(bar, size=5, labels=['{:g}'.format(float('{:.2g}'.format(i))) for i in tempDf[column]])
        plt.title(graphTitle+ ", by " + type + " Error")
        plt.ylabel(column+" (arcseconds)")
        plt.xticks(fontsize=10, rotation=270)
        fig.subplots_adjust(bottom=0.3)
        x,y = calcDf['Name'].values.tolist(), calcDf[column].values.tolist()
        plt.savefig(graphPath+"/barCharts/"+graphTitle+type+".png", dpi=300)
        plt.clf()
        plt.close()

 repeats = []
#read in the file
os.mkdir(graphPath)
os.mkdir(graphPath+"/barCharts")

data = pd.read_csv("diagonalRevisedTMO_Bulletins.csv")
data = data[~data["Bulletin"].isin(repeats)]
current = (data.loc[data['Date'].str.contains('2022')])

print(data)


# orbitUpdate2022 = orbitUpdate.loc[orbitUpdate['Date'].str.contains('2022')]
# obsWithTMOalltimeGraph = GraphObj("Alltime Observations on TMO Bulletins",data)
obsWithTMO2022 = GraphObj("2022 Observations on TMO Bulletins", current)
#
graphs = [obsWithTMO2022]


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
    plotMedians(codes,file[:-4])
    graphs.append(GraphObj(file[:-4], currentDf))

for graph in graphs:
    graph.graph()

