# -*- coding: utf-8 -*-
import processing
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterString)

from ..utils import qgsDebug
from .boundary_layer import BoundaryLayer
from .fence_layer import FenceLayer
from .paddock_layer import PaddockLayer
from .pipeline_layer import PipelineLayer
from .waterpoint_layer import WaterpointLayer

class CreateProject(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString(
            'ProjectName', 'Project Name', multiLine=False, defaultValue='My Farm'))
        self.addParameter(QgsProcessingParameterString(
            'FirstMilestoneName', 'First Milestone Name', multiLine=False, defaultValue='Current'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        milestoneName = parameters['FirstMilestoneName']

        # Create paddocks, pipeline, fence, waterpoints, boundary layers
        boundary = BoundaryLayer(layerName=f"{milestoneName} Boundary")
        waterpoint = WaterpointLayer(layerName=f"{milestoneName} Waterpoints")
        pipeline = PipelineLayer(layerName=f"{milestoneName} Pipeline")
        fence = FenceLayer(layerName=f"{milestoneName} Fence")
        paddock = PaddockLayer(layerName=f"{milestoneName} Paddocks")
        
        # The 'Layers' parameter of the Package Layers tool ('native:package')
        # Note this is sensitive to order
        layers = [boundary, waterpoint, pipeline, fence, paddock]

        # Create Paddock Power Project
        alg_params = {
            'LAYERS': layers,
            #'OUTPUT': parameters['ProjectName'],
            'OVERWRITE': True,
            'SAVE_STYLES': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CreatePaddockPowerProject'] = processing.run(
            'native:package', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'Create Paddock Power Project'

    def displayName(self):
        return 'Create Paddock Power Project'

    def icon(self):
        return QIcon(":/plugins/mlapp/images/fenceline.png")

    # def group(self):
    #     return ''

    # def groupId(self):
    #     return ''

    def createInstance(self):
        return CreateProject()
