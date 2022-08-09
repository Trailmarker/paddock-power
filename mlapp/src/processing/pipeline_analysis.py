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


class PipelineAnalysis(QgsProcessingAlgorithm):
    PIPE = 'PIPE'
    DEM = 'DEM'
    OUTPUT = 'OUTPUT'
    MinMax = 'MinMax'
 
    def __init__(self):
        super().__init__()
 
    def name(self):
        return "Pipeline Analysis"
 
    def displayName(self):
        return "Pipeline Analysis"
        
    def icon(self):
        return QIcon(":/plugins/mlapp/images/pipeline.png")
 
    def createInstance(self):
        return type(self)()
   
    def initAlgorithm(self, config=None):
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.PIPE,
                'New Pipeline',
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
                'Pipeline Analysis'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterVectorDestination (
                self.MinMax,
                'Pipeline Minimum & Maximum Elevation Coordinates'
            )
        )
         
    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(17, model_feedback)
        outputFile = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        minMaxFile = self.parameterAsOutputLayer(parameters, self.MinMax, context)
        outputs = {}

       
#------------------------------------------------------------------------------------------------------------------------------------
# Line Analysis
#------------------------------------------------------------------------------------------------------------------------------------            
      

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
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', alg_params, context=context, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Reproject layer
        alg_params = {
            'INPUT': parameters['PIPE'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Explode lines
        alg_params = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExplodeLines'] = processing.run('native:explodelines', alg_params, context=context, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '$id', 'length': 0, 'name': 'ID', 'precision': 0, 'type': 2}, 
            {'expression': ' round(angle_at_vertex( $geometry,0),6)', 'length': 10, 'name': 'Bearing (°)', 'precision': 3, 'type': 6}, 
            {'expression': 'round(x(transform(start_point($geometry),\'EPSG:7845\', \'EPSG:4326\')), 6)', 'length': 10, 'name': 'Start Coordinates Long', 'precision': 3, 'type': 6}, 
            {'expression': 'round(y(transform(start_point($geometry), \'EPSG:7845\', \'EPSG:4326\')), 6)', 'length': 10, 'name': 'Start Coordinates Lat', 'precision': 3, 'type': 6}, 
            {'expression': 'round(x(transform(end_point($geometry ), \'EPSG:7845\', \'EPSG:4326\')), 6)', 'length': 10, 'name': 'End Coordinates Long', 'precision': 3, 'type': 6}, 
            {'expression': 'round(y(transform(end_point($geometry ), \'EPSG:7845\', \'EPSG:4326\')), 6)', 'length': 10, 'name': 'End Coordinates Lat', 'precision': 3, 'type': 6}, 
            {'expression': '$length', 'length': 10, 'name': 'LengthM', 'precision': 2, 'type': 6}, 
            {'expression': '$length / 1000', 'length': 10, 'name': 'LengthKM', 'precision': 2, 'type': 6}],
            'INPUT': outputs['ExplodeLines']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFields'] = processing.run('qgis:refactorfields', alg_params, context=context, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Splitting Pipeline
        alg_params = {
            'INPUT': outputs['RefactorFields']['OUTPUT'],
            'INTERVAL': 30,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SplittingPipeline'] = processing.run('native:densifygeometriesgivenaninterval', alg_params, context=context, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Extract Elevation
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['SplittingPipeline']['OUTPUT'],
            'NODATA': 0,
            'RASTER': outputs['WarpReproject']['OUTPUT'],
            'SCALE': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractElevation'] = processing.run('native:setzfromraster', alg_params, context=context, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Explode lines
        alg_params = {
            'INPUT': outputs['ExtractElevation']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExplodeLines'] = processing.run('native:explodelines', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(7)
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
        outputs['Calculate3dLines'] = processing.run('qgis:fieldcalculator', alg_params, context=context, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}
            
        # Calculate Minimum Elevation
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'MinimumElev',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 1,
            'FORMULA': 'if (minimum(z(start_point($geometry)), "ID") < minimum(z(end_point($geometry)), "ID"), minimum(z(start_point($geometry))), minimum(z(end_point($geometry))))',
            'INPUT': outputs['Calculate3dLines']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MinElev'] = processing.run('qgis:fieldcalculator', alg_params, context=context, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Calculate Maximum Elevation
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'MaximumElev',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 1,
            'FORMULA': 'if (maximum(z(start_point($geometry)), "ID") < maximum(z(end_point($geometry)), "ID"), maximum(z(start_point($geometry))), maximum(z(end_point($geometry))))',
            'INPUT': outputs['MinElev']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MaxElev'] = processing.run('qgis:fieldcalculator', alg_params, context=context, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Sum Distance
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'TotalDistanceM',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 0,
            'FORMULA': 'sum( Distance , ID )',
            'INPUT': outputs['MaxElev']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SumDistance'] = processing.run('qgis:fieldcalculator', alg_params, context=context, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}


        # Joining Lines
        alg_params = {
            'FIELD': ['ID'],
            'INPUT': outputs['SumDistance']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoiningLines'] = processing.run('native:dissolve', alg_params, context=context, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}
            
        # Sort by ID
        
        alg_params = {
            'INPUT': outputs['JoiningLines']['OUTPUT'],
            'EXPRESSION': 'ID',
            'ASCENDING':True,
            'NULLS_FIRST':False,
            'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
          }
          
        outputs['SortFields'] = processing.run("native:orderbyexpression", alg_params, context=context, is_child_algorithm=True)
        
        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}
            
        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'expression': 'ID', 'length': 0, 'name': 'ID', 'precision': 0, 'type': 2}, 
            {'expression': '"Bearing (°)"', 'length': 10, 'name': 'Bearing (°)', 'precision': 3, 'type': 6}, 
            {'expression': '"Start Coordinates Long"', 'length': 10, 'name': 'Start Coordinates Long', 'precision': 3, 'type': 6}, 
            {'expression': '"Start Coordinates Lat"', 'length': 10, 'name': 'Start Coordinates Lat', 'precision': 3, 'type': 6}, 
            {'expression': '"End Coordinates Long"', 'length': 10, 'name': 'End Coordinates Long', 'precision': 3, 'type': 6}, 
            {'expression': '"End Coordinates Lat"', 'length': 10, 'name': 'End Coordinates Lat', 'precision': 3, 'type': 6}, 
            {'expression': 'round(LengthM,2)', 'length': 10, 'name': 'Distance as crow flies (m)', 'precision': 2, 'type': 6}, 
            {'expression': 'round(LengthKM,2)', 'length': 10, 'name': 'Distance as crow flies (km)', 'precision': 2, 'type': 6}, 
            #{'expression': '"Distance"', 'length': 10, 'name': 'Distance', 'precision': 2, 'type': 6}, 
            {'expression': 'round(TotalDistanceM,2)', 'length': 10, 'name': 'Distance inc. terrain (m)', 'precision': 2, 'type': 6}, 
            {'expression': 'round(TotalDistanceM / 1000,2)', 'length': 10, 'name': 'Distance inc. terrain (km)', 'precision': 2, 'type': 6}, 
            {'expression': 'abs(round( "TotalDistanceM" -  "LengthM" ,2))', 'length': 10, 'name': 'Difference (m)', 'precision': 2, 'type': 6}, 
            {'expression': 'round(MinimumElev,1)', 'length': 0, 'name': 'Minimum Elevation', 'precision': 0, 'type': 6},
            {'expression': 'round(MaximumElev,1)', 'length': 0, 'name': 'Maximum Elevation', 'precision': 0, 'type': 6}],
            'INPUT': outputs['SortFields']['OUTPUT'],
            'OUTPUT': outputFile
        }
        pipeline_analysis = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}
          
#------------------------------------------------------------------------------------------------------------------------------------
# Extract minimum and maximum elevations from proposed line
#------------------------------------------------------------------------------------------------------------------------------------            
        
        # Extract verticies from lines
        
        alg_params = {
             'INPUT': outputs['ExplodeLines']['OUTPUT'],
             'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractVertices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}
        
        # delete duplicate verticies
        alg_params = {
             'INPUT': outputs['ExtractVertices']['OUTPUT'],
             'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeleteDuplicateVertices'] = processing.run('qgis:deleteduplicategeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}
            
        # Add geometry attributes to verticies
        alg_params = {
            'INPUT': outputs['DeleteDuplicateVertices']['OUTPUT'], 
            'CALC_METHOD': 0, 
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddGeometryAtt'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}
            
        # Extract Minimum Elevation verticies
        alg_params = {
            'EXPRESSION': '\"zcoord\" = minimum( \"zcoord\", \"ID\")',
            'INPUT': outputs['AddGeometryAtt']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractMinimumElevation'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}
            
        # Extract Maximum Elevation verticies
        alg_params = {
            'EXPRESSION': '\"zcoord\" = maximum( \"zcoord\", \"ID\")',
            'INPUT': outputs['AddGeometryAtt']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractMaximumElevation'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}            
        
        # Merge  Minimum and Maximum points
        alg_params = {
            'LAYERS': [outputs['ExtractMinimumElevation']['OUTPUT'], outputs['ExtractMaximumElevation']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeMinMax'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {} 
            
        # Refactor fields
        alg_params = {
             'FIELDS_MAPPING': [{'expression': 'ID', 'length': 0, 'name': 'Line ID', 'precision': 0, 'type': 2},
             {'expression':  'round(x( transform($geometry, \'EPSG:7845\', \'EPSG:4326\') ),6)', 'length' : 0, 'name': 'Longitude', 'precision': 0, 'type': 6},
             {'expression':  'round(y( transform($geometry, \'EPSG:7845\', \'EPSG:4326\') ),6)', 'length' : 0, 'name': 'Latitude', 'precision': 0, 'type': 6},
             {'expression':  'round(zcoord,1)', 'length' : 0, 'name': 'Elevation (m)', 'precision': 0, 'type': 6},
             {'expression':  'if (z($geometry) = minimum( "zcoord" , "ID" ), \'Minimum Elevation\', \'Maximum Elevation\')', 'length' : 0, 'name': 'Minimum or Maximum', 'precision': 0, 'type': 10}],
             'INPUT': outputs['MergeMinMax']['OUTPUT'],
             'OUTPUT': minMaxFile
        }
             
        MinMaxMerge = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
 



        
        results = {self.OUTPUT : pipeline_analysis, self.MinMax : MinMaxMerge}
        return results
