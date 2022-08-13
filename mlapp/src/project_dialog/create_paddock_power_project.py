# -*- coding: utf-8 -*-
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterMultipleLayers
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterDefinition
from PyQt5.QtGui import QIcon
import processing

class CreatePaddockPowerProject(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        param = QgsProcessingParameterMultipleLayers('Layers', 'Layers', layerType=QgsProcessing.TypeMapLayer, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterString('ProjectName', 'Project Name', multiLine=False, defaultValue='My Farm'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Create Paddock Power Project
        alg_params = {
            'LAYERS': parameters['Layers'],
            'OUTPUT': parameters['ProjectName'],
            'OVERWRITE': True,
            'SAVE_STYLES': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CreatePaddockPowerProject'] = processing.run('native:package', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
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
        return CreatePaddockPowerProject()
