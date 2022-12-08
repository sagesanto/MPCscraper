import matplotlib.colors as mcolors, matplotlib.pyplot as plt, math, re, sys, os, fileinput, shutil, random
import pandas as pd
from datetime import datetime


graphs = []
graphPath = "graphs/" + str(datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S")) + '/'
#initialize colors
# colors = [line.replace("\n",'') for line in open("colors.txt")]
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
        # ax.legend(loc='upper center', ncol=5, fancybox=True, shadow=True)
        plt.title(self.name)
        plt.xlabel(self.xAxis)
        plt.ylabel(self.yAxis)
        plt.xticks([])
        plt.tight_layout()
        plt.savefig(self.path + self.name + ".png")
        plt.clf()

def createLegend(keys):
# for gradient
#     global colors
#     return {keys[i]: colors[i] for i in range(len(keys))}
#for tmo only
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

#read in the file
os.mkdir(graphPath)
os.mkdir(graphPath+"/barCharts")


repeats = []
with open("repeatBulList.txt",'r') as f:
    for line in f:
        line = line.replace('\n', '')
        repeats.append(line)

data = pd.read_csv("diagonalTMO_Bulletins.csv")
current = (data.loc[data['Date'].str.contains('2022')])
# print("data has\n",(data.nunique()))
# print("\n\n\n",data["Bulletin"].value_counts())

#filter out orbit updates from the main dataset

#have not quite filtered out all revisions - 2018-T13 - NEED TO CONVERT FROM T130 to TD0 or whatever when searching in the repeatBuls - watch out for truncation, maybe use date?


# print("Median for all time before trim:",str(data["Diagonal Residual"].median()),"mean:",str(data["Diagonal Residual"].mean()))



# current = data[~data["Bulletin"].isin(repeats)]
# orbitUpdate = data[data["Bulletin"].isin(repeats)]
# print(orbitUpdate)
# print("orbitUpdate has\n",(orbitUpdate.nunique()))
# print("\n\n\n",orbitUpdate["Bulletin"].value_counts())
# print(current)
# print("\n\n\n",orbitUpdate["Bulletin"].value_counts())
# orbUpObsPerBull = orbitUpdate["Bulletin"].value_counts()
# plt.bar(x=orbUpObsPerBull.index,height=orbUpObsPerBull)
# plt.title("Observations Per Bulletin: Revisions")
# plt.xticks([])
# plt.show()
# plt.clf()
# plt.close()
# print("Median for all time after trim: ",str(current["Diagonal Residual"].median()),"mean:",str(current["Diagonal Residual"].mean()))
# exit()
# tmoCurrent = (current.loc[(current["Obs Code"]=="654")])
# orbUpObsPerBull = current["Bulletin"].value_counts()
# print("\n\nCurrent:\n",orbUpObsPerBull)
# plt.bar(x=orbUpObsPerBull.index,height=orbUpObsPerBull)
# plt.title("Observations Per Bulletin: Non-Revisions")
# plt.xticks([])
# plt.show()
# plt.clf()
# plt.close()

#2018-T13 from 10/10/18 (really 18T1D0, mislabeled) has close to 2000 observations (2015 TB145 is a PHA) - it's not crazy that there's close to 165,000 revisions updates
#create mask

# orbitUpdate2022 = orbitUpdate.loc[orbitUpdate['Date'].str.contains('2022')]
obsWithTMOalltimeGraph = GraphObj("Alltime Observations on TMO Bulletins",data)
obsWithTMO2022 = GraphObj("2022 Observations on TMO Bulletins", current)
#
graphs = [obsWithTMOalltimeGraph,obsWithTMO2022]


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
