# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class FencelineProfileCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        figure = Figure(figsize=(width, height), dpi=dpi)        
        self.axes = figure.add_subplot(111)
        super(FencelineProfileCanvas, self).__init__(figure)
