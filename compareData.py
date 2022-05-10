"""class creation"""

import json

import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


class BoxPlot:
    """Parse and plot information from imported JSON file"""

    def __init__(self, data):
        self.data = data
        self.plotKwargs = {}
        self.plotKwargs["meanline"] = True
        self.plotKwargs["showmeans"] = True
        self.plotKwargs["bootstrap"] = 5000
        self.plotKwargs["widths"] = 0.75
        self.plotKwargs["vert"] = True  # default = True

        self.subPlotKwargs = {}
        self.subPlotKwargs["sharey"] = True
        self.subPlotKwargs["sharex"] = True
        self.subPlotKwargs["figsize"] = (15, 5)

        # Optional definitions

        self.medians: list = []
        self.labels: list = []
        self.ax1 = plt.axis
        self.fig1 = plt.figure

        self.func_description = [
            "None",  # 0
            "A(int) --> B",  # 1
            "A --> B",  # 2
            "A --> B(OUT)",  # 3
            "A-->B(Length)",
            "A+A-->B",
            "A",
            "A(int)-->B(joining)",
            "A--->B+A-->(B+B)",  # 8
            "",
            "A(slat)-->B",
            "A-->B(A-->pos,pos->B)",
            "A-->B(A-->B,B>pos,pos->B)",
            "A-->B(A-->B,centering)",
            "A--->B(A-->centering-->B)",  # 14
            "A-->B AGV",
            "A-->B(AGV)",
            "A-->B(disjoining,length)",
            "A-->B(joining)",
            "",  # 19
            "",
            "A-->B(pos,int)()",
            "Centering",  # 22
            "Man ctrl 1",
            "Man ctrl 2",
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
            "",
        ]

        self.__parsedata__()

    def __parsedata__(self):
        for data in self.data:
            self.fig1, self.ax1 = plt.subplots(**self.subPlotKwargs)
            self.labels, self.dataPoints = [*zip(*data[0].items())]

    def plot(self) -> None:

        self.boxplot = plt.boxplot(self.dataPoints, **self.plotKwargs)

        labelCommented = []
        for i in range(len(self.labels)):
            labelCommented.append(self.labels[i] + ". " + self.func_description[i])
        labelCommented = tuple(labelCommented)
        plt.xticks(range(1, len(self.labels) + 1), labelCommented)

        # create list of median values
        median: list = []
        for line in self.boxplot["medians"]:
            # get position data for median line
            x, y = line.get_xydata()[1]
            plt.text(
                x - 0.75, y, "%.2f" % y, verticalalignment="center", fontsize=7
            )  # plot median information text onto plot
            # overlay median value
            median.append(float(y))
        self.medians.append(median)
        self.fig1.autofmt_xdate()

        plt.grid(True, which="both", axis="x", linewidth=1, linestyle="--")
        plt.ylabel("Cycle time [ms]")
        plt.xlabel("Function")
        plt.title("Scantime for 10 x functioncall")
        plt.show()


class StemPlot:
    """Plot medians from boxplot on a stemplot"""

    def __init__(self):
        # init data and plot design
        self.plotKwargs = {}
        self.plotKwargs["linefmt"] = "grey"  # vertical linestyle and color
        self.plotKwargs["bottom"] = "0"  # baseline

        # define plot arguments
        self.subPlotKwargs = {}
        self.subPlotKwargs["sharey"] = True
        self.subPlotKwargs["sharex"] = True
        self.subPlotKwargs["figsize"] = (15, 5)

    def plot(self, labels, data) -> None:
        for points in data:
            fig1, ax1 = plt.subplots(**self.subPlotKwargs)
            # set baseline as first dataset
            self.plotKwargs["bottom"] = points[0]
            markerline, stemlines, baseline = plt.stem(points, **self.plotKwargs)

            # calculate performanceboost for labeling
            labelPercentage = []
            baselinePoint = points[0]
            for i in range(len(labels)):
                datapoint = points[i]
                percentage = f"{(((datapoint/baselinePoint) * 100) - 100):.1f}"
                difference = f"{(datapoint - baselinePoint):.2f}"
                labelPercentage.append(f"{labels[i]} = {difference}")
            labelPercentage = tuple(labelPercentage)

            # define plotspecific layout functions
            plt.margins(x=0.008, y=0.1)
            plt.xticks(range(0, len(labels)), labelPercentage)
            plt.grid(True, which="both", axis="x", linewidth=0.5, linestyle="--")
            plt.grid(True, which="both", axis="y", linewidth=1, linestyle="--")
            plt.ylabel("Cycle time [ms]")
            plt.xlabel("Function and percentage timereduction")
            plt.legend(["baseline"], loc="best")
            fig1.autofmt_xdate()
            plt.tight_layout(pad=1, w_pad=1, h_pad=2)
            plt.show()


class comparison:
    def __init__(self, dataset1: list, dataset2: list) -> None:
        self.dataset1 = dataset1
        self.dataset2 = dataset2

    def compare(self):
        difference = []
        difference.append([y - x for (x, y) in zip(self.dataset1[0], self.dataset2[0])])
        return difference


class CSVParser:
    def __init__(self, fileList):
        self.fileList: list = fileList
        self.data: list = []

        self.parserKwargs = {}
        self.parse()

    def parse(self) -> None:
        for file in self.fileList:
            try:
                with open(str(file), "r") as data:
                    fileData = json.load(data)
                    self.data.append(fileData)
            except FileNotFoundError as e:
                print(e)
                exit()


if __name__ == "__main__":
    fileList: list = ["basis_conveyor.json"]
    parser = CSVParser(fileList)
    parser1 = CSVParser(["changed_conveyor.json"])

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
