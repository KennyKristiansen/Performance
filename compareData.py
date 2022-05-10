"""class creation"""

import enum
import json

import matplotlib.pyplot as plt


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

        # load labels from json file
        with open("labels.json", "r") as data:
            self.func_description = json.load(data)
        self.__parsedata__()

    def __parsedata__(self):
        """parse through data and extracts label and datapoint lists"""
        for data in self.data:
            self.fig1, self.ax1 = plt.subplots(**self.subPlotKwargs)
            self.labels, self.dataPoints = [*zip(*data[0].items())]
            self.boxplot = plt.boxplot(self.dataPoints, **self.plotKwargs)

    def getmedians(self):
        """create list of median values from boxplot"""
        median: list = []
        for line in self.boxplot["medians"]:
            # get position data for median line
            x, y = line.get_xydata()[1]
            plt.text(
                x - 0.75, y, "%.2f" % y, verticalalignment="center", fontsize=6
            )  # plot median information text onto plot
            # overlay median value
            median.append(float(y))
        self.medians.append(median)

    def editlabels(self):
        commentedLabels: list = []
        for i, _ in enumerate(self.labels):
            commentedLabels.append(self.labels[i] + ". " + self.func_description[i])
        commentedLabels = tuple(commentedLabels)
        plt.xticks(range(1, len(self.labels) + 1), labels=commentedLabels)

    def plot(self) -> None:
        """control plot config flow"""
        self.getmedians()
        self.editlabels()

        # define plot
        plt.grid(True, which="both", axis="x", linewidth=1, linestyle="--")
        plt.ylabel("Cycle time [ms]")
        plt.xlabel("Function")
        plt.title("Scantime for 10 x functioncall")
        self.fig1.autofmt_xdate()

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

    def infolabel(self, points, labels):
        baselinePoint = points[0]
        labelPercentage = []

        for i, label in enumerate(labels):
            datapoint = float(points[i])
            percentage = f"{(((datapoint/baselinePoint) * 100) - 100):.1f}"
            difference = f"{(datapoint - baselinePoint):.2f}"
            labelPercentage.append(f"{label} = {difference}")
        labelPercentage = tuple(labelPercentage)
        return labelPercentage

    def plot(self, labels, data) -> None:
        for points in data:
            fig1, ax1 = plt.subplots(**self.subPlotKwargs)
            # set baseline as first dataset
            self.plotKwargs["bottom"] = points[0]
            markerline, stemlines, baseline = plt.stem(points, **self.plotKwargs)

            labelPercentage = self.infolabel(points, labels)

            # define plotspecific layout functions
            plt.xticks(range(0, len(labels)), labelPercentage)
            plt.grid(True, which="both", axis="x", linewidth=0.5, linestyle="--")
            plt.grid(True, which="both", axis="y", linewidth=1, linestyle="--")

            # labeling
            plt.ylabel("Cycle time [ms]")
            plt.xlabel("Function and percentage timereduction")
            plt.legend(["baseline"], loc="best")

            # formatting
            plt.margins(x=0.008, y=0.1)
            fig1.autofmt_xdate()
            plt.tight_layout(pad=1, w_pad=1, h_pad=2)
            plt.show()


class Compare:
    def __init__(self, dataset1: list, dataset2: list) -> list:
        self.compare(dataset1, dataset2)

    def compare(dataset_1, dataset_2):
        difference = []
        difference.append([y - x for (x, y) in zip(dataset_1[0], dataset_2[0])])
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

    comparedData = Compare.compare(medians, medians1)

    stemplot = StemPlot()
    stemplot.plot(labels, comparedData)
