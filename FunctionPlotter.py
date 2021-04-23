# ------------------ PySide2 - Qt Designer - Matplotlib ------------------
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT  as  NavigationToolbar)

from matplotlib.figure import Figure

import numpy  as  np
import re


# to make Matplotlib figure be embedded in the Pyside2 application
# ------------------ MplWidget ------------------
class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

    # ------------------ MainWidget ------------------


class MainWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        # open the qt_design file
        designer_file = QFile("FunctionPlotterDesign.ui")
        designer_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        loader.registerCustomWidget(MplWidget)
        self.ui = loader.load(designer_file, self)

        designer_file.close()
        # connect the button with the update_dragh method
        self.ui.pushButton_Draw.clicked.connect(self.update_graph)
        # set the gui's title
        self.setWindowTitle("Function Plotter")



        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui)
        self.setLayout(grid_layout)

    def update_graph(self):
        try:
            # take maximum number
            max = self.ui.lineEdit_Max.text()
            # take minimum number
            min = self.ui.lineEdit_Min.text()
            # generate the range of x
            x = np.linspace(int(min), int(max))
            # replace ^ with ** prameter by using sub() method from re lib
            text_input = self.ui.lineEdit.text()
            new_text_input = re.sub("\^", "**", text_input)

            # use eval() to convert the string from text form to equation form
            try:
                y = eval(new_text_input)

                # clear the error display
                self.ui.text_exp_function.setText(" ")
                self.ui.text_exp_max_min.setText(" ")
                # plot the function
                self.ui.MplWidget.canvas.axes.clear()
                self.ui.MplWidget.canvas.axes.plot(x, y)
                self.ui.MplWidget.canvas.draw()
            # show error in input function
            except:
                self.ui.MplWidget.canvas.axes.clear()
                self.ui.MplWidget.canvas.draw()
                self.ui.text_exp_function.setText("Check your input Function it must be f(x)")
                self.ui.text_exp_max_min.setText(" ")

        # show error in maximum or minimum value
        except:
            self.ui.MplWidget.canvas.axes.clear()
            self.ui.MplWidget.canvas.draw()
            self.ui.text_exp_max_min.setText("Check the max and min value of x it must be a number")
            self.ui.text_exp_function.setText(" ")





app = QApplication([])
window = MainWidget()
window.show()
app.exec_()