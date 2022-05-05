'''class creation'''
import json
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.ticker import (MultipleLocator)
from numpy import diff


class BoxPlot():
    '''Parse and plot information from imported JSON file'''
    
    def __init__(self, data):
        self.data = data
        self.plotKwargs = {}
        self.plotKwargs['meanline'] = True
        self.plotKwargs['showmeans'] = True
        self.plotKwargs['bootstrap'] = 5000
        self.plotKwargs['widths'] = 0.75

        self.subPlotKwargs = {}
        self.subPlotKwargs['sharey'] = True
        self.subPlotKwargs['sharex'] = True
        self.subPlotKwargs['figsize'] = (15, 5)

        # Optional definitions

        self.medians: list = []
        self.labels: list = []
        self.ax1 = plt.axis
        self.fig1 = plt.figure

        self.func_description = ['None',  # 0
                    'Call conv block',  # 1
                    'A(int) --> B',  # 2
                    "A --> B",
                    "A --> B(OUT)",  # 4
                    "A-->B(Length)",
                    "A+A-->B",
                    "A",
                    "A(int)-->B(joining)",
                    "A--->B+A-->(B+B)",  # 9
                    "A(slat)-->B",
                    "A-->B(A-->pos,pos->B)",
                    "A-->B(A-->B,B>pos,pos->B)",
                    "A-->B(A-->B,centering)",
                    "A--->B(A-->centering-->B)",  # 14
                    "Conv_man_ctrl_2",
                    "A-->B(AGV)",
                    "A-->B(disjoining,length)",
                    "A-->B(joining)",
                    "A-->B(Length,pos)",  # 19
                    "A(int)-->B-->B",
                    "A-->B(pos,int)()",
                    "Centering()",
                    "Man ctrl 1",
                    "Conv data copy",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""]  # 63

        self.__parsedata__()

    def __parsedata__(self):
        for data in self.data:
            self.fig1, self.ax1 = plt.subplots(**self.subPlotKwargs)
            self.labels, self.dataPoints = [*zip(*data[0].items())]

    def plot(self) -> None:

        self.boxplot = plt.boxplot(self.dataPoints, **self.plotKwargs)

        # create list of median values
        median: list = []
        for line in self.boxplot['medians']:
            # get position data for median line
            x, y = line.get_xydata()[1]
            plt.text(x-0.75, y, '%.1f' % y, verticalalignment='center', fontsize=7)      # plot median information text onto plot
            # overlay median value
            median.append(float(y))
        self.medians.append(median)
        plt.show()



class StemPlot():
    '''Plot medians from boxplot on a stemplot'''

    def __init__(self):
        # init data and plot design
        self.plotKwargs = {}
        self.plotKwargs['linefmt'] = 'grey'  # vertical linestyle and color
        self.plotKwargs['bottom'] = '0'  # baseline

        # define plot arguments
        self.subPlotKwargs = {}
        self.subPlotKwargs['sharey'] = True
        self.subPlotKwargs['sharex'] = True
        self.subPlotKwargs['figsize'] = (15, 5)

    def plot(self, labels, data) -> None:
        for points in data:
            fig1, ax1 = plt.subplots(**self.subPlotKwargs)
            # set baseline as first dataset
            self.plotKwargs['bottom'] = points[-1]
            markerline, stemlines, baseline = plt.stem(
                points, **self.plotKwargs)

            # calculate performanceboost for labeling
            labelPercentage= []
            baselinePoint = points[-1]
            for i in range(len(labels)):
                datapoint = points[i]
                percentage = f'{(((datapoint/baselinePoint) * 100) - 100):.1f}'
                labelPercentage.append(f'{labels[i]} = {percentage}%')
            labelPercentage = tuple(labelPercentage)

            # define plotspecific layout functions
            plt.margins(x=0.008, y=0.1)
            plt.xticks(range(0, len(labels)), labelPercentage)
            plt.grid(True, which='both', axis='x',
                     linewidth=0.5, linestyle='--')
            plt.grid(True, which='both', axis='y', linewidth=1, linestyle='--')
            plt.ylabel('Cycle time [ms]')
            plt.xlabel('Function and percentage timereduction')
            plt.legend(['baseline'], loc='best')
            fig1.autofmt_xdate()
            plt.tight_layout(pad=1, w_pad=1, h_pad=2)
            plt.show()


class comparison():
    def __init__(self, dataset1 :list, dataset2 :list) -> None:
        self.dataset1 = dataset1
        self.dataset2 = dataset2
    
    def compare(self):
        difference = []
        difference.append([x - y for (x,y) in zip(self.dataset1[0], self.dataset2[0])])
        print(difference)
        return difference
        



class CSVParser():
    def __init__(self, fileList):
        self.fileList: list = fileList
        self.data: list = []

        self.parserKwargs = {}
        self.parse()

    def parse(self) -> None:
        for file in self.fileList:
            try:
                with open(str(file), 'r') as data:
                    fileData = json.load(data)
                    self.data.append(fileData)
            except FileNotFoundError as e:
                print(e)
                exit()


if __name__ == '__main__':
    fileList: list = ['basis.json']
    parser = CSVParser(fileList)
    parser1 = CSVParser(['changed.json'])

    boxplot = BoxPlot(parser.data)
    boxplot.plot()
    boxplot1 = BoxPlot(parser1.data)
    boxplot1.plot()


    labels = boxplot.labels
    medians = boxplot.medians
    
    labels1 = boxplot1.labels
    medians1 = boxplot1.medians

    compare = comparison(medians, medians1)
    comparedData = compare.compare()
    
    stemplot = StemPlot()
    stemplot.plot(labels, comparedData)