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
            'SAVE_STYLES': False,
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
        self.milestoneGroup.addLayer(self.waterpointLayer)
        self.milestoneGroup.addLayer(self.boundaryLayer)
        self.milestoneGroup.addLayer(self.pipelineLayer)
        self.milestoneGroup.addLayer(self.fenceLayer)
        self.milestoneGroup.addLayer(self.paddockLayer)

