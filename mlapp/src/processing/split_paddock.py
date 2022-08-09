import os
import inspect
from qgis.core import   (QgsProcessing,
                        QgsProcessingAlgorithm, 
                        QgsProcessingParameterFeatureSource, 
                        QgsProcessingParameterVectorDestination,
                        QgsProcessingMultiStepFeedback,
                        QgsCoordinateReferenceSystem)
from PyQt5.QtGui import QIcon
import processing


class SplitPaddock(QgsProcessingAlgorithm):
    FENCE = 'FENCE'
    PADDOCK = 'PADDOCK'
    SPLIT_PADDOCK = 'SPLIT_PADDOCK'
 
    def __init__(self):
        super().__init__()
 
    def name(self):
        return "Split paddocks with new fence"
 
    def displayName(self):
        return "Split paddocks with new fence"
        
    def icon(self):
        return QIcon(":/plugins/mlapp/images/split.png")
        
    def createInstance(self):
        return type(self)()
   
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.FENCE,
                'New Fence',
                [QgsProcessing.TypeVectorLine]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.PADDOCK,
                'Paddocks to Split',
                [QgsProcessing.TypeVectorPolygon]
            )
        )
 
        self.addParameter(
            QgsProcessingParameterVectorDestination (
                self.SPLIT_PADDOCK,
                'Split Paddocks'
            )
        )
         
    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        outputFile = self.parameterAsOutputLayer(parameters, self.SPLIT_PADDOCK, context)
        outputs = {}

        # Reproject Paddock
        alg_params = {
            'INPUT': parameters['PADDOCK'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectPaddock'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        # Reproject lines
        alg_params = {
            'INPUT': parameters['FENCE'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectFence'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        # Extend lines
        alg_params = {
            'INPUT': outputs['ReprojectFence']['OUTPUT'],
            'START_DISTANCE':100,
            'END_DISTANCE':100,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtendedLine'] = processing.run("native:extendlines", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        # Split with lines
        alg_params = {
            'INPUT': outputs['ReprojectPaddock']['OUTPUT'],
            'LINES': outputs['ExtendedLine']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            #'OUTPUT': outputFile
        }
        outputs['SplitWithLines'] = processing.run('native:splitwithlines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        #split_paddocks = processing.run('native:splitwithlines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'FID',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': '$id',
            'INPUT': outputs['SplitWithLines']['OUTPUT'],
            'NEW_FIELD': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateFID'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)            
            
        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'PDK_AREAKM',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round($area * 0.000001,1)',
            'INPUT': outputs['CalculateFID']['OUTPUT'],
            'NEW_FIELD': False,
            'OUTPUT': outputFile
        }
        split_paddocks = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
         
        return {self.SPLIT_PADDOCK : split_paddocks}