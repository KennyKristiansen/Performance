'''class creation'''
import json
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.ticker import (MultipleLocator)


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

        labelCommented = []
        for i in range(len(self.labels)):
            labelCommented.append(
                self.labels[i] + '. ' + self.func_description[i])
        labelCommented = tuple(labelCommented)

        # create list of median values
        median: list = []
        for line in self.boxplot['medians']:
            # get position data for median line
            x, y = line.get_xydata()[1]
            plt.text(x-0.75, y, '%.1f' % y, verticalalignment='center', fontsize=7)      # plot median information text onto plot
            # overlay median value
            median.append(float(y))
        self.medians.append(median)


        # define plotspecific layout functions
        plt.xticks(range(1, len(self.labels) + 1), labelCommented)
        plt.margins(x=0.008, y=0.1)
        self.ax1.set_xlim(0, self.ax1.get_xlim()[1])
        self.fig1.autofmt_xdate()
        self.ax1.legend(self.boxplot)
        plt.grid(True, which='both', axis='y', linewidth=1, linestyle='--')
        plt.grid(True, which='both', axis='x',
                     linewidth=0.5, linestyle='--')
        plt.ylabel('Cycle time [ms]')
        plt.xlabel('Function disabled')
        plt.tight_layout(pad=1, w_pad=1.0, h_pad=2)
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

    boxplot = BoxPlot(parser.data)
    boxplot.plot()

    labels = boxplot.labels
    medians = boxplot.medians

    stemplot = StemPlot()
    stemplot.plot(labels, medians)