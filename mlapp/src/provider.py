# -*- coding: utf-8 -*-
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .processing.fenceline_analysis import FencelineAnalysis
from .processing.pipeline_analysis import PipelineAnalysis
from .processing.split_paddock import SplitPaddock
from .processing.waterpoint_buffers import WaterpointBuffers

from .processing.create_project import CreateProject
#from .processing.add_empty_project import AddEmptyProject
from .processing.add_project_from_existing import AddProjectFromExisting
from .processing.delete_project import DeleteProject


class Provider(QgsProcessingProvider):
    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        # self.addAlgorithm(FencelineAnalysis())
        # self.addAlgorithm(PipelineAnalysis())
        # self.addAlgorithm(SplitPaddock())
        # self.addAlgorithm(WaterpointBuffers())
        # self.addAlgorithm(CreateProject())
        # self.addAlgorithm(AddEmptyProject())
        # self.addAlgorithm(AddProjectFromExisting())
        #self.addAlgorithm(DeleteProject())
        pass

    def id(self):
        return 'Paddock Power'

    def name(self):
        return self.tr('Paddock Power')

    def icon(self):
        return QIcon(":/plugins/mlapp/images/paddock.png")

    def longName(self):
        return self.name()
