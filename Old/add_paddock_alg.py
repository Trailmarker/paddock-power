import os
import inspect
from qgis.core import   (QgsProcessing,
                        QgsProcessingAlgorithm, 
                        QgsProcessingParameterFeatureSource, 
                        QgsProcessingParameterVectorDestination,
                        QgsProcessingParameterRasterLayer,
                        QgsCoordinateReferenceSystem,
                        QgsProcessingMultiStepFeedback)
from PyQt5.QtGui import QIcon
import processing


class AddPaddockLayer(QgsProcessingAlgorithm):
    FENCE = 'FENCE'
    DEM = 'DEM'
    OUTPUT = 'OUTPUT'
 
    def __init__(self):
        super().__init__()
 
    def name(self):
        return "Add a temporary paddock layer"
 
    def displayName(self):
        return "Add a temporary paddock layer"
        
    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'icons/fenceline.png'))) # icon for the Paddock Power Tools Group in Toolbox
        return icon
        
    def group(self):
        return 'New Layers'
    
    def groupId(self):
        return 'New Layers'
 
    def createInstance(self):
        return type(self)()
   
    def initAlgorithm(self, config=None):
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.FENCE,
                'New Fenceline',
                [QgsProcessing.TypeVectorLine]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.DEM,
                'Elevation Mapping'
            )
        )
 
        self.addParameter(
            QgsProcessingParameterVectorDestination (
                self.OUTPUT,
                'Fenceline Analysis'
            )
        )
         
    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        outputFile = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        outputs = {}

        # Warp (reproject)
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': parameters['DEM'],
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

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Reproject layer
        alg_params = {
            'INPUT': parameters['FENCE'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Explode lines
        alg_params = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExplodeLines'] = processing.run('native:explodelines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '$id', 'length': 0, 'name': 'ID', 'precision': 0, 'type': 2}, {'expression': ' angle_at_vertex( $geometry,0)', 'length': 10, 'name': 'Bearing', 'precision': 3, 'type': 6}, {'expression': 'x(start_point(  $geometry ))', 'length': 10, 'name': 'Start Coordinates Long', 'precision': 3, 'type': 6}, {'expression': 'y(start_point(  $geometry ))', 'length': 10, 'name': 'Start Coordinates Lat', 'precision': 3, 'type': 6}, {'expression': 'x(end_point(  $geometry ))', 'length': 10, 'name': 'End Coordinates Long', 'precision': 3, 'type': 6}, {'expression': 'y(end_point(  $geometry ))', 'length': 10, 'name': 'End Coordinates Y', 'precision': 3, 'type': 6}, {'expression': 'round($length,1)', 'length': 10, 'name': 'LengthM', 'precision': 2, 'type': 6}, {'expression': 'round($length,1)', 'length': 10, 'name': 'LengthKM', 'precision': 2, 'type': 6}],
            'INPUT': outputs['ExplodeLines']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFields'] = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Splitting fence line
        alg_params = {
            'INPUT': outputs['RefactorFields']['OUTPUT'],
            'LENGTH': 10,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SplittingFenceLine'] = processing.run('native:splitlinesbylength', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Extract elevation
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['SplittingFenceLine']['OUTPUT'],
            'NODATA': 0,
            'RASTER': outputs['WarpReproject']['OUTPUT'],
            'SCALE': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractElevation'] = processing.run('native:setzfromraster', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Calculate 3d lines
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Distance',
            'FIELD_PRECISION': 2,
            'FIELD_TYPE': 0,
            'FORMULA': 'sqrt($length^2 + (z(start_point($geometry)) - z(end_point($geometry)))^2)',
            'INPUT': outputs['ExtractElevation']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Calculate3dLines'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Sum lines
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'TotalDistanceM',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'sum( \"Distance\" ,  \"ID\" )',
            'INPUT': outputs['Calculate3dLines']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SumLines'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Joining Lines
        alg_params = {
            'FIELD': ['ID'],
            'INPUT': outputs['SumLines']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoiningLines'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Calculating total distance in km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'TotalDistanceKM',
            'FIELD_PRECISION': 2,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(TotalDistanceM / 1000,1)',
            'INPUT': outputs['JoiningLines']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatingTotalDistanceInKm'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Calculating difference
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'DifferenceM',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'round( \"TotalDistanceM\" -  \"LengthM\" ,1)',
            'INPUT': outputs['CalculatingTotalDistanceInKm']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatingDifference'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'expression': 'ID', 'length': 0, 'name': 'ID', 'precision': 0, 'type': 2},{'expression': '"Bearing"', 'length': 10, 'name': 'Bearing', 'precision': 3, 'type': 6}, {'expression': '"Start Coordinates Long"', 'length': 10, 'name': 'Start Coordinates Long', 'precision': 3, 'type': 6}, {'expression': '"Start Coordinates Lat"', 'length': 10, 'name': 'Start Coordinates Lat', 'precision': 3, 'type': 6}, {'expression': '"End Coordinates Long"', 'length': 10, 'name': 'End Coordinates Long', 'precision': 3, 'type': 6}, {'expression': '"End Coordinates Y"', 'length': 10, 'name': 'End Coordinates Y', 'precision': 3, 'type': 6}, {'expression': '"LengthM"', 'length': 10, 'name': 'LengthM', 'precision': 2, 'type': 6}, {'expression': '"LengthKM"', 'length': 10, 'name': 'LengthKM', 'precision': 2, 'type': 6}, {'expression': '"TotalDistanceM"', 'length': 10, 'name': 'TotalDistanceM', 'precision': 2, 'type': 6}, {'expression': '"TotalDistanceKM"', 'length': 10, 'name': 'TotalDistanceKM', 'precision': 2, 'type': 6}, {'expression': '"DifferenceM"', 'length': 10, 'name': 'DifferenceM', 'precision': 2, 'type': 6}],
            'INPUT': outputs['CalculatingDifference']['OUTPUT'],
            'OUTPUT': outputFile            
        }

        fenceline_analysis = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
         
        return {self.OUTPUT : fenceline_analysis}