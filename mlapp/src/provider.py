# -*- coding: utf-8 -*-
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .processing.algorithm import Algorithm
from .processing.fenceline_analysis import FencelineAnalysis
from .processing.pipeline_analysis import PipelineAnalysis
from .processing.split_paddock import SplitPaddock
from .processing.waterpoint_buffers import WaterpointBuffers

from .processing.create_project import CreateProject
from .processing.add_milestone import AddMilestone


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
        self.addAlgorithm(CreateProject())
        self.addAlgorithm(AddMilestone())

    def id(self):
        return 'Paddock Power'

    def name(self):
        return self.tr('Paddock Power')

    def icon(self):
        return QIcon(":/plugins/mlapp/images/icon.png")

    def longName(self):
        return self.name()
