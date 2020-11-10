import os
import inspect
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSource
from qgis.core import QgsProcessingParameterFeatureSink
from PyQt5.QtGui import QIcon
import processing


class SplitPaddocksWithNewFence(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource('newfence', 'New Fence', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSource('paddocktosplit', 'Paddock to split', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Split', 'Split', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Split with lines
        alg_params = {
            'INPUT': parameters['paddocktosplit'],
            'LINES': parameters['newfence'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SplitWithLines'] = processing.run('native:splitwithlines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'PDKAREAKM2',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 0,
            'FORMULA': 'round($area * 0.000001,1)',
            'INPUT': outputs['SplitWithLines']['OUTPUT'],
            'NEW_FIELD': False,
            'OUTPUT': parameters['Split']
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Split'] = outputs['FieldCalculator']['OUTPUT']
        return results

    def name(self):
        return 'Split paddocks with new fence'

    def displayName(self):
        return 'Split paddocks with new fence'
        
    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'icons/split.png'))) # icon for the Paddock Power Tools Group in Toolbox
        return icon

    def group(self):
        return 'Paddock Tools'

    def groupId(self):
        return 'Paddocks Tools'

    def createInstance(self):
        return SplitPaddocksWithNewFence()