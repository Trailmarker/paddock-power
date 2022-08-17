# -*- coding: utf-8 -*-
from os import path

import processing
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterString)
from qgis.PyQt.QtGui import QIcon

from ..utils import qgsDebug
from .boundary_layer import BoundaryLayer
from .fence_layer import FenceLayer
from .paddock_layer import PaddockLayer
from .pipeline_layer import PipelineLayer
from .waterpoint_layer import WaterpointLayer


class AddMilestone(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(
            'PaddockPowerProjectFile', 'Paddock Power Project File', fileFilter="QGS Project Files (*.qgz *.qgs)"))
        self.addParameter(QgsProcessingParameterString(
            'MilestoneName', 'Milestone Name', multiLine=False, defaultValue='New Milestone'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        milestoneName = parameters['MilestoneName']

        gpkgName = f"{path.splitext(parameters['PaddockPowerProjectFile'])[0]}.gpkg"

        qgsDebug(f"gpkgName: {gpkgName}")
        qgsDebug(f"milestoneName: {milestoneName}")
        qgsDebug(f"parameters: {str(parameters)}")

        # Create paddocks, pipeline, fence, waterpoints, boundary layers
        boundary = BoundaryLayer(layerName=f"{milestoneName} Boundary")
        waterpoint = WaterpointLayer(layerName=f"{milestoneName} Waterpoints")
        pipeline = PipelineLayer(layerName=f"{milestoneName} Pipeline")
        fence = FenceLayer(layerName=f"{milestoneName} Fence")
        paddock = PaddockLayer(layerName=f"{milestoneName} Paddocks")
        
        # The 'Layers' parameter of the Package Layers tool ('native:package')
        # Note this is sensitive to order
        layers = [boundary, waterpoint, pipeline, fence, paddock]

        # Add milestone to project
        alg_params = {
            'LAYERS': layers,
            #'OUTPUT': parameters['ProjectName'],
            'OVERWRITE': not path.exists(gpkgName),
            'SAVE_STYLES': True,
            'OUTPUT': gpkgName
        }
        outputs['AddMilestone'] = processing.run(
            'native:package', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'PaddockPowerAddMilestone'

    def displayName(self):
        return 'Add Milestone to Paddock Power Project'

    def icon(self):
        return QIcon(":/plugins/mlapp/images/fenceline.png")

    # def group(self):
    #     return ''

    # def groupId(self):
    #     return ''

    def createInstance(self):
        return AddMilestone()
