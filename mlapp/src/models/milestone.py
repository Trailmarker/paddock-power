# -*- coding: utf-8 -*-
from os import path

import processing

from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.core import QgsProject

from ..data.paddock_power_vector_layer import PaddockPowerVectorLayerSourceType, PaddockPowerVectorLayerType
from ..data.boundary_layer import BoundaryLayer
from ..data.waterpoint_layer import WaterpointLayer
from ..data.pipeline_layer import PipelineLayer
from ..data.fence_layer import FenceLayer
from ..data.paddock_layer import PaddockLayer

from ..utils import qgsDebug


class Milestone(QObject):
    # emit this signal when paddocks are updated
    paddocksUpdated = pyqtSignal()

    def __init__(self, milestoneName, gpkgFile):
        super(Milestone, self).__init__()

        self.milestoneName = milestoneName
        self.gpkgFile = gpkgFile
        self.isLoaded = False
    

    def create(self):
        """Create this milestone in its GeoPackage."""
        # Create paddocks, pipeline, fence, waterpoints, boundary layers
        boundary = BoundaryLayer(layerName=f"{self.milestoneName} Boundary")
        waterpoint = WaterpointLayer(layerName=f"{self.milestoneName} Waterpoints")
        pipeline = PipelineLayer(layerName=f"{self.milestoneName} Pipeline")
        fence = FenceLayer(layerName=f"{self.milestoneName} Fence")
        paddock = PaddockLayer(layerName=f"{self.milestoneName} Paddocks")

        # The 'Layers' parameter of the Package Layers tool ('native:package')
        # Note this is sensitive to order
        layers = [boundary, waterpoint, pipeline, fence, paddock]

        qgsDebug(f"layers: {str(layers)}")
        qgsDebug(f"gpkgName: {self.gpkgFile}")

        # Add milestone to GeoPackage using the Package Layers tool
        params = {
            'LAYERS': layers,
            #'OUTPUT': parameters['ProjectName'],
            'OVERWRITE': not path.exists(self.gpkgFile),
            'SAVE_STYLES': True,
            'OUTPUT': self.gpkgFile
        }

        processing.run(
            'native:package', params)

        # Load the required layers for this milestone from the source
        self.load()


    def load(self):
        """Load this milestone its GeoPackage."""
        boundaryLayerName = f"{self.milestoneName} Boundary"
        self.boundaryLayer = BoundaryLayer(sourceType=PaddockPowerVectorLayerSourceType.File,
                                           layerName=boundaryLayerName, gpkgFile=self.gpkgFile)
        waterpointLayerName = f"{self.milestoneName} Waterpoints"
        self.waterpointLayer = WaterpointLayer(sourceType=PaddockPowerVectorLayerSourceType.File,
                                               layerName=waterpointLayerName, gpkgFile=self.gpkgFile)
        pipelineLayerName = f"{self.milestoneName} Pipeline"
        self.pipelineLayer = PipelineLayer(sourceType=PaddockPowerVectorLayerSourceType.File,
                                           layerName=pipelineLayerName, gpkgFile=self.gpkgFile)
        fenceLayerName = f"{self.milestoneName} Fence"
        self.fenceLayer = FenceLayer(sourceType=PaddockPowerVectorLayerSourceType.File,
                                    layerName=fenceLayerName, gpkgFile=self.gpkgFile)
        paddockLayerName = f"{self.milestoneName} Paddocks"
        self.paddockLayer = PaddockLayer(sourceType=PaddockPowerVectorLayerSourceType.File,
                                         layerName=paddockLayerName, gpkgFile=self.gpkgFile)

        self.isLoaded = True


    def addToMap(self):
        """Add this milestone to the current map view."""
        self.milestoneGroup = QgsProject.instance().layerTreeRoot().addGroup(self.milestoneName)
        self.milestoneGroup.addLayer(self.boundaryLayer)
        self.milestoneGroup.addLayer(self.waterpointLayer)
        self.milestoneGroup.addLayer(self.pipelineLayer)
        self.milestoneGroup.addLayer(self.fenceLayer)
        self.milestoneGroup.addLayer(self.paddockLayer)


    # def guessLayerType(cls, layerName):
    #     """Guess the type of a Paddock Power vector layer based on the layerName."""
    #     layerTypeNames = [e.name for e in PaddockPowerVectorLayerType]
    #     return next(t for t in layerTypeNames if t in layerName)


    # def loadPaddocks(self):
    #     """Load the milestone paddocks from a detected paddock layer."""
    #     self.paddockFeatures = []
    #     paddockLayers = [
    #         l for l in self.milestoneGroup.findLayers() if 'Paddocks' in l.name()]
    #     if len(paddockLayers) == 0:
    #         print("No paddock layer found for milestone " + self.milestoneName)
    #     elif len(paddockLayers) > 1:
    #         print("Multiple paddock layers found for milestone " + self.milestoneName)
    #     else:
    #         self.paddockLayer = paddockLayers[0].layer()
    #         self.paddockFeatures = [f for f in self.paddockLayer.getFeatures()]

    # def loadMilestoneName(self):
    #     """Refresh the milestone name from the group."""
    #     self.milestoneName = self.milestoneGroup.name()

    # def dump(self, tag=""):
    #     qgsDebug(self.milestoneName, tag=tag)

    #     for f in self.paddockFeatures:
    #         qgsDebug(str(f['Paddock Name']), tag=tag)
