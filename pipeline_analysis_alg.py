import os
import inspect
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterFeatureSource
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
from PyQt5.QtGui import QIcon
import processing


class PipelineAnalysis(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('elevation', 'Elevation', defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSource('newfences', 'New Fences', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('PipelineAnalysis', 'Pipeline Analysis', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(12, model_feedback)
        results = {}
        outputs = {}

        # Reproject layer
        alg_params = {
            'INPUT': parameters['newfences'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '$id', 'length': 0, 'name': 'fid', 'precision': 0, 'type': 2}, {'expression': 'round($length,1)', 'length': 0, 'name': 'LengthM', 'precision': 1, 'type': 6}, {'expression': 'round($length / 1000,1)', 'length': 0, 'name': 'LengthKM', 'precision': 1, 'type': 6}],
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFields'] = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Warp (reproject)
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': parameters['elevation'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Densify by interval
        alg_params = {
            'INPUT': outputs['RefactorFields']['OUTPUT'],
            'INTERVAL': 30,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DensifyByInterval'] = processing.run('qgis:densifygeometriesgivenaninterval', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Drape (set z-value from raster)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['DensifyByInterval']['OUTPUT'],
            'NODATA': 0,
            'RASTER': outputs['WarpReproject']['OUTPUT'],
            'SCALE': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DrapeSetZvalueFromRaster'] = processing.run('native:setzfromraster', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Explode lines
        alg_params = {
            'INPUT': outputs['DrapeSetZvalueFromRaster']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExplodeLines'] = processing.run('native:explodelines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Calculate 3d lines
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Distance',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 0,
            'FORMULA': 'sqrt((x( end_point($geometry )) - x(start_point($geometry )))^2 + (y( end_point($geometry )) - y(start_point($geometry )))^2 + (z( end_point($geometry )) - z(start_point($geometry )))^2)',
            'INPUT': outputs['ExplodeLines']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Calculate3dLines'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'MinElev',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 1,
            'FORMULA': 'minimum( z( start_point(  $geometry )))',
            'INPUT': outputs['Calculate3dLines']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'MaxElev',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 1,
            'FORMULA': 'maximum( z( start_point(  $geometry )))',
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Sum Distance
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'TotalDistanceM',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 0,
            'FORMULA': 'sum( \"Distance\" , \"fid\" )',
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SumDistance'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Dissolve
        alg_params = {
            'FIELD': 'fid',
            'INPUT': outputs['SumDistance']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Dissolve'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'expression': 'LengthM', 'length': 0, 'name': 'LengthM', 'precision': 1, 'type': 0}, {'expression': 'LengthKM', 'length': 0, 'name': 'LengthKM', 'precision': 1, 'type': 6}, {'expression': 'round(TotalDistanceM / 1000,1)', 'length': 0, 'name': 'TotalDistanceKM', 'precision': 1, 'type': 6}, {'expression': 'abs(round( "TotalDistanceM" -  "LengthM" ,1))', 'length': 0, 'name': 'DifferenceM', 'precision': 1, 'type': 0}, {'expression': 'MinElev', 'length': 0, 'name': 'MinElev', 'precision': 0, 'type': 2}, {'expression': 'MaxElev', 'length': 0, 'name': 'MaxElev', 'precision': 0, 'type': 2}],
            'INPUT': outputs['Dissolve']['OUTPUT'],
            'OUTPUT': parameters['PipelineAnalysis']
        }
        outputs['RefactorFields'] = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['PipelineAnalysis'] = outputs['RefactorFields']['OUTPUT']
        return results

    def name(self):
        return 'Pipeline Analysis'

    def displayName(self):
        return 'Pipeline Analysis'
        
    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'icons/fenceline.png'))) # icon for the Paddock Power Tools Group in Toolbox
        return icon

    def group(self):
        return 'Line Tools'

    def groupId(self):
        return 'Line Tools'

    def createInstance(self):
        return PipelineAnalysis()
