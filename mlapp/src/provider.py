# -*- coding: utf-8 -*-
from qgis.core import QgsProcessingProvider
from PyQt5.QtGui import QIcon
from .processing.algorithm import Algorithm
from .processing.fenceline_analysis import FencelineAnalysis
from .processing.pipeline_analysis import PipelineAnalysis
from .processing.split_paddock import SplitPaddock
from .processing.waterpoint_buffers import WaterpointBuffers

class Provider(QgsProcessingProvider):
    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        self.addAlgorithm(Algorithm())
        self.addAlgorithm(FencelineAnalysis())
        self.addAlgorithm(PipelineAnalysis())
        self.addAlgorithm(SplitPaddock())
        self.addAlgorithm(WaterpointBuffers())

    def id(self):
        return 'Paddock Power'

    def name(self):
        return self.tr('Paddock Power')

    def icon(self):
        return QIcon(":/plugins/mlapp/images/ntg-primary-cmyk.png")

    def longName(self):
        return self.name()
