#!/usr/bin/python

"""
In this example, we create a simple
window in PyQt5.

Author: Kenny Kristiansen
Company: Lachenmeier
"""

import sys

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('untitled.ui', self) # Load the .ui file
        self.show() # Show the GUI

app = QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application
