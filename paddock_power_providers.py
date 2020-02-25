import os
import inspect
from PyQt5.QtGui import QIcon

from qgis.core import QgsProcessingProvider
from .split_paddock_alg import SplitPaddocksWithNewFence
from .pipeline_analysis_alg import PipelineAnalysis
from .fenceline_analysis_alg import FencelineAnalysis
from .waterpoint_analysis_alg import WaterpointBuffers

class PaddockPowerProviders(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)
        
    def unload(self):
        pass
        
    def loadAlgorithms(self):
        self.addAlgorithm(SplitPaddocksWithNewFence())
        self.addAlgorithm(PipelineAnalysis())
        self.addAlgorithm(FencelineAnalysis())
        self.addAlgorithm(WaterpointBuffers())
        
    def id(self):
        return 'paddock_power'
        
    def name(self):
        return self.tr('Paddock Power Tools')
        
    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'icons/ntg-primary-cmyk.png'))) # icon for the Paddock Power Tools Group in Toolbox
        return icon
        
    def longName(self):
        return self.name()
        
    