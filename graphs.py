import matplotlib.colors as mcolors, matplotlib.pyplot as plt, re, sys, os, fileinput, shutil
import pandas as pd
from datetime import datetime

graphs = []
graphPath = "/graphs/" + str(datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M")) + '/'
os.mkdir(graphPath)
os.mkdir(graphPath+"manual/") #idk if i can combine the previous line and this one


class GraphObj:
    def __init__(self,name,dataframe,xaxis="Date",yaxis="Diagonal Residual"):
        self.name, self.data, self.xAxis,self.yAxis= name,dataframe, xaxis,yaxis

#read in the file
df = pd.read_csv("data2.csv")

current = df["2022" in df["Date"]]
tmoCurrent = df[current["Obs Code"]==654]

alltimeGraph = GraphObj("Alltime Observations",df)
currentGraph = GraphObj("2022 Observations",current)
alltimeTMOGraph = GraphObj("Alltime TMO", df[df["Obs Code"]==654])
tmo2022Graph = GraphObj("TMO 2022", df[current["Obs Code"]==654])


#graph the manual graphs
for graph in [alltimeGraph,currentGraph,alltimeTMOGraph,tmo2022Graph]:
    tmoDf = df[graph.dataframe["Obs Code"]==654]
    other = df[graph.dataframe["Obs Code"]!=654] #this sucks
    plt.scatter(other[graph.xaxis], other[graph.yaxis], c='tab:blue')
    plt.scatter(tmoDf[graph.xaxis],tmoDf[graph.yaxis],c='tab:orange')
    plt.savefig(graphPath+"manual/"+graph.name+".png")

for file in os.list_dir("/obsCodesToPlot"):
    #read in line numbers, if Obs Code in [list]
    graphs.append(GraphObj(file[:-4], ))

