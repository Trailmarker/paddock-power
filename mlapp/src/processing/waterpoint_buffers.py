#
#   To do:
#   
#   Output into groups
#   Add to existing datasets
#   Run on selected paddocks automatically and check if no paddocks selected
#   Check if layers are in correct CRS and if not then reproject

import os
import inspect
from qgis.core import   (QgsProcessing,
                        QgsProcessingAlgorithm, 
                        QgsProcessingParameterFeatureSource, 
                        QgsProcessingParameterVectorDestination,
                        QgsProcessingMultiStepFeedback,
                        QgsProcessingParameterNumber,
                        QgsCoordinateReferenceSystem,
                        QgsExpression)
from PyQt5.QtGui import QIcon
import processing


class WaterpointBuffers(QgsProcessingAlgorithm):
    BUFFERDISTANCE = 'BUFFERDISTANCE'
    CURRENTWATER = 'CURRENTWATER'
    NEWWATER = 'NEWWATER'
    LANDUNIT = 'LANDUNIT'
    PADDOCK = 'PADDOCK'
    CWAREA = 'CWAREA'
    NWAREA = 'NWAREA'
    CWLAREA = 'CWLAREA'
    NWLAREA = 'NWLAREA'
    OUTPUT = 'OUTPUT'
 
    def __init__(self):
        super().__init__()
 
    def name(self):
        return "Waterpoint Buffers"
 
    def displayName(self):
        return "Waterpoint Buffers"
        
    def icon(self):
        return QIcon(":/plugins/mlapp/images/buffer.png")
        
    # def group(self):
    #     return 'Waterpoint Tools'
    
    # def groupId(self):
    #     return 'Waterpoint Tools'
 
    def createInstance(self):
        return type(self)()
   
    def initAlgorithm(self, config=None):
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.BUFFERDISTANCE,
                'Buffer Distance (km)',
                type=QgsProcessingParameterNumber.Integer,
                minValue=0,
                maxValue=10,
                defaultValue=3
            )
        )    
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.PADDOCK,
                'Selected Paddock',
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.CURRENTWATER,
                'Current Waterpoints',
                [QgsProcessing.TypeVectorPoint]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.NEWWATER,
                'Proposed Waters',
                [QgsProcessing.TypeVectorPoint]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.LANDUNIT,
                'Land Unit/Systems Mapping',
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterVectorDestination (
                self.CWAREA,
                'Current Watered Area Buffers'
            )
        )
    
        self.addParameter(
            QgsProcessingParameterVectorDestination (
                self.NWAREA,
                'Proposed Watered Area Buffers'
            )
        )
      
        self.addParameter(
            QgsProcessingParameterVectorDestination (
                self.CWLAREA,
                'Current Land Unit/System Watered Areas'
            )
        ) 
        
        self.addParameter(
            QgsProcessingParameterVectorDestination (
                self.NWLAREA,
                'Proposed Land Unit/System Watered Areas'
            )
        )
    

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(26, model_feedback)
        buffer_distance_km = (self.parameterAsInt(parameters, self.BUFFERDISTANCE, context))
        buffer_distance = (self.parameterAsInt(parameters, self.BUFFERDISTANCE, context)) * 1000 # convert entered value to metres
        current_buffer = self.parameterAsOutputLayer(parameters, self.CWAREA, context)
        new_buffer = self.parameterAsOutputLayer(parameters, self.NWAREA, context)
        current_land_buffer = self.parameterAsOutputLayer(parameters, self.CWLAREA, context)
        new_land_buffer = self.parameterAsOutputLayer(parameters, self.NWLAREA, context)
        results = {}
        outputs = {}
        
        # Reproject Current Waters. Shouldn't be needed if already in correct projection, maybe check projection first?
        alg_params = {
            'INPUT': parameters['CURRENTWATER'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectCurrentWaters'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
            
        # Delete unneeded fields
        alg_params = {
            'INPUT': outputs['ReprojectCurrentWaters']['OUTPUT'],
            'COLUMN': ['fid',
            'Waterpoint Name', 
            'Waterpoint Reference',
            'Waterpoint Bore Yield (l/sec)',
            'Waterpoint Date Commisioned',
            'Waterpoint Date Decommisioned',
            'Waterpoint Status',
            'Waterpoint Start Month',
            'Waterpoint End Month',
            'Waterpoint Longitude',
            'Waterpoint Latitude',
            'Waterpoint Elevation',
            'Waterpoint Bore Report',
            'Date Edited'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeletedCurrentWaters'] = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
            
        # Reproject Paddocks. Shouldn't be needed if already in correct projection, maybe check projection first?
        alg_params = {
            'INPUT': parameters['PADDOCK'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectPaddocks'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
        
          
        # Extract by expression for Current Waters
        alg_params = {
            'EXPRESSION': ' \"Waterpoint Type\"  =  \'Trough\' OR  \"Waterpoint Type\" = \'Waterhole\' OR  \"Waterpoint Type\" = \'Turkey Nest\'',
            'INPUT': outputs['DeletedCurrentWaters']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpressionCurrentWaters'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Extract by location using selected paddock for current waters
        alg_params = {
            'INPUT': outputs['ExtractByExpressionCurrentWaters']['OUTPUT'],
            'INTERSECT': outputs['ReprojectPaddocks']['OUTPUT'],
            'PREDICATE': [0],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByLocationCurrentWaters'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Create buffer for current waters
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': buffer_distance,
            'END_CAP_STYLE': 0,
            'INPUT': outputs['ExtractByLocationCurrentWaters']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 25,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CurrentBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Intersection Current
        alg_params = {
            'INPUT': outputs['CurrentBuffer']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectPaddocks']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionCurrent'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST Current
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Buffer Distance (km)',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': buffer_distance_km,
            'INPUT': outputs['IntersectionCurrent']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}
            
        # Calc CURR_WAREA
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Current Watered Area (km²)',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001,1)',
            'INPUT': outputs['AddWa_dist']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcCurrentArea'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}
            
        # Calc Percent Watered
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Current Watered Area (%)',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(\"Current Watered Area (km²)\" / \"Paddock Area (km²)\" * 100,1)',
            'INPUT': outputs['CalcCurrentArea']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcPercentageCurrent'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Delete unneeded fields
        alg_params = {
            'INPUT': outputs['CalcPercentageCurrent']['OUTPUT'],
            'COLUMN': ['Waterpoint Type','Paddock Date Commisioned','Paddock Date Decommisioned','Paddock Status','Date Edited', 'Paddock Perimeter (km)'],
            'OUTPUT': current_buffer
        }
        current_buffers = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
      
        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}




#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Reproject Proposed Waters. Shouldn't be needed if already in correct projection, maybe check projection first?
        alg_params = {
            'INPUT': parameters['NEWWATER'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectNewWaters'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}
            
        # Delete unneeded fields
        alg_params = {
            'INPUT': outputs['ReprojectNewWaters']['OUTPUT'],
            'COLUMN': ['fid',
            'Waterpoint Name',
            'Waterpoint Reference',
            'Waterpoint Bore Yield (l/sec)',
            'Waterpoint Date Commisioned',
            'Waterpoint Date Decommisioned',
            'Waterpoint Status',
            'Waterpoint Start Month',
            'Waterpoint End Month',
            'Date Edited',
            'Waterpoint Longitude',
            'Waterpoint Latitude',
            'Waterpoint Elevation',
            'Waterpoint Bore Report'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeletedNewWaters'] = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            
        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}
           
        # Extract by expression New Waters
        alg_params = {
            'EXPRESSION': ' \"Waterpoint Type\"  =  \'Trough\' OR  \"Waterpoint Type\" = \'Waterhole\' OR  \"Waterpoint Type\" = \'Turkey Nest\'',
            'INPUT': outputs['DeletedNewWaters']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpressionNewWaters'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Extract by location New Waters
        alg_params = {
            'INPUT': outputs['ExtractByExpressionNewWaters']['OUTPUT'],
            'INTERSECT': outputs['ReprojectPaddocks']['OUTPUT'],
            'PREDICATE': [0],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByLocationNewWaters'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}
            
        # Merge Current Watered Areas
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'LAYERS': [outputs['ExtractByLocationNewWaters']['OUTPUT'],outputs['ExtractByLocationCurrentWaters']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeWaters'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # New Buffer
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': buffer_distance,
            'END_CAP_STYLE': 0,
            'INPUT': outputs['MergeWaters']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 25,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['NewBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Intersection Current
        alg_params = {
            'INPUT': outputs['NewBuffer']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectPaddocks']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionNew'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST Current
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Buffer Distance (km)',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': buffer_distance_km,
            'INPUT': outputs['IntersectionNew']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist_New'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}
            
        # Calc CURR_WAREA
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Proposed Watered Area (km²)',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001,2)',
            'INPUT': outputs['AddWa_dist_New']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcNewArea'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

         # Calc Percent Watered
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Proposed Watered Area (%)',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(\"Proposed Watered Area (km²)\" / \"Paddock Area (km²)\" * 100,1)',
            'INPUT': outputs['CalcNewArea']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcPercentageProposed'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}
        
        # Delete unneeded fields
        alg_params = {
            'INPUT': outputs['CalcPercentageProposed']['OUTPUT'],
            'COLUMN': ['Waterpoint Type','Paddock Date Commisioned','Paddock Date Decommisioned','Paddock Status','Date Edited', 'Paddock Perimeter (km)', 'layer', 'path'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeletedWatersNew'] = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
      
        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}
            
        # Join current watered area attribute to proposed watered area buffer
        
        alg_params = {
            'INPUT': outputs['DeletedWatersNew']['OUTPUT'],
            'FIELD': 'Buffer Distance (km)',
            'INPUT_2': current_buffer,
            'FIELD_2': 'Buffer Distance (km)',
            'FIELDS_TO_COPY': ['Current Watered Area (km²)', 'Current Watered Area (%)'],
            'METHOD': 1,
            'DISCARD_NONMATCHING': False,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinedWaters'] = processing.run("native:joinattributestable", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}
 
        alg_params = {
            
            'FIELDS_MAPPING':[{'expression': '"Paddock Name"', 'length': 0, 'name': 'Paddock Name', 'precision': 0, 'type': 10},
            {'expression': '"Paddock Area (km²)"', 'length': 0, 'name': 'Paddock Area (km²)', 'precision': 0, 'type': 6},
            {'expression': '"Buffer Distance (km)"', 'length': 0, 'name': 'Buffer Distance (km)', 'precision': 0, 'type': 2},
            {'expression': '"Current Watered Area (km²)"', 'length': 0, 'name': 'Current Watered Area (km²)', 'precision': 0, 'type': 6},
            {'expression': '"Current Watered Area (%)"', 'length': 0, 'name': 'Current Watered Area (%)', 'precision': 0, 'type': 6},
            {'expression': '"Proposed Watered Area (km²)"', 'length': 0, 'name': 'Proposed Watered Area (km²)', 'precision': 0, 'type': 6},
            {'expression': '"Proposed Watered Area (%)"', 'length': 0, 'name': 'Proposed Watered Area (%)', 'precision': 0, 'type': 6},
            {'expression': ' round("Proposed Watered Area (km²)" / "Current Watered Area (km²)" ,2 )', 'length': 0, 'name': 'Proposed Watered Area Difference (km²)', 'precision': 0, 'type': 6}],
            'INPUT': outputs['JoinedWaters']['OUTPUT'],
            'OUTPUT':new_buffer
         }

        new_buffers = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}
            
            
            
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Reproject Land Units / Systems. Shouldn't be needed if already in correct projection, maybe check projection first?
        alg_params = {
            'INPUT': parameters['LANDUNIT'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLandUnit'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}
            

        # Intersection Current
        alg_params = {
            'INPUT': outputs['ReprojectPaddocks']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectLandUnit']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CurrentLandInt'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        #current_land_buffers = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}
 
        # Delete unneeded fields
        alg_params = {
            'INPUT': outputs['CurrentLandInt']['OUTPUT'],
            'COLUMN': ['Paddock Name', 'Paddock Area (km²)', 'Paddock Perimeter (km)', 'Date Edited', 'Paddock Status', 'Paddock Date Commisioned','Paddock Date Decommisioned'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CurrentLandIntDel'] = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
      
        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}
            
        # Calculate LU/LS Area
        alg_params = {
            'INPUT': outputs['CurrentLandIntDel']['OUTPUT'],
            'FIELD_NAME':'Paddock Land Unit/Land System Area (km²)',
            'FIELD_TYPE':0,
            'FIELD_LENGTH':10,
            'FIELD_PRECISION':3,
            'NEW_FIELD': False,
            'FORMULA':'round(area( $geometry ) * 0.000001,1)',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateLSLUPDK'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
                
        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}
            
        # Intersection Current
        alg_params = {
            'INPUT': current_buffer,
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['CalculateLSLUPDK']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CurrentLandInt'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        #current_land_buffers = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}
            

        alg_params = {

            'INPUT':outputs['CurrentLandInt']['OUTPUT'],
            'FIELDS_MAPPING':[{'expression': '"Paddock Name"', 'length': 0, 'name': 'Paddock Name', 'precision': 0, 'type': 10},
            {'expression': '"Paddock Area (km²)"', 'length': 0, 'name': 'Paddock Area (km²)', 'precision': 0, 'type': 6},
            {'expression': '"Buffer Distance (km)"', 'length': 0, 'name': 'Buffer Distance (km)', 'precision': 0, 'type': 2},
            {'expression': '"Current Watered Area (km²)"', 'length': 0, 'name': 'Current Watered Area (km²)', 'precision': 0, 'type': 6},
            {'expression': '"Current Watered Area (%)"', 'length': 0, 'name': 'Current Watered Area (%)', 'precision': 0, 'type': 6},
            {'expression': '"Land System"', 'length': 50, 'name': 'Land System', 'precision': 0, 'type': 10},
            {'expression': '"Map Unit"', 'length': 10, 'name': 'Map Unit', 'precision': 0, 'type': 10},
            {'expression': '"Original Land System"', 'length': 50, 'name': 'Original Land System', 'precision': 0, 'type': 10},
            {'expression': '"Original Map Unit"', 'length': 10, 'name': 'Original Map Unit', 'precision': 0, 'type': 10},
            {'expression': '"Landscape Class"', 'length': 50, 'name': 'Landscape Class', 'precision': 0, 'type': 10},
            {'expression': '"Class Description"', 'length': 254, 'name': 'Class Description', 'precision': 0, 'type': 10},
            {'expression': '"Erosion Risk"', 'length': 100, 'name': 'Erosion Risk', 'precision': 0, 'type': 10},
            {'expression': '"AE/km²"', 'length': 0, 'name': 'AE/km²', 'precision': 0, 'type': 6},
            {'expression': '"Paddock Land Unit/Land System Area (km²)"', 'length': 0, 'name': 'Paddock Land Unit/Land System Area (km²)', 'precision': 0, 'type': 6},
            {'expression': 'round(area( $geometry ) * 0.000001,1)', 'length': 0, 'name': 'Current Land Unit/Land System Area (km²)', 'precision': 0, 'type': 6},
            {'expression': 'round( round(area( $geometry ) * 0.000001,1) / "Current Watered Area (km²)" * 100, 1)', 'length': 0, 'name': 'Current Land Unit/Land System Area (%)', 'precision': 0, 'type': 6},
            {'expression': 'round( "AE/km²" * round(area( $geometry ) * 0.000001,1) ,1)', 'length': 0, 'name': 'Current AE in A Condition', 'precision': 0, 'type': 6},
            {'expression': 'round(( ("AE/km²"  * .75)* round(area( $geometry ) * 0.000001,1) ),1)', 'length': 0, 'name': 'Current AE in B Condition', 'precision': 0, 'type': 6},
            {'expression': 'round(( ("AE/km²"  * .5)* round(area( $geometry ) * 0.000001,1) ),1)', 'length': 0, 'name': 'Current AE in C Condition', 'precision': 0, 'type': 6},
            {'expression': '0', 'length': 0, 'name': 'Current AE in D Condition', 'precision': 0, 'type': 6}],
            'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
        }
        
        outputs['RefactorCurrentLUDiff'] = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
           
        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}
            
        # Delete unneeded fields
        alg_params = {
            'INPUT': outputs['RefactorCurrentLUDiff']['OUTPUT'],
            'COLUMN': ['fid',
            'fid_2', 'fid_2_2', 'Land Unit/Land System Area (km²)'],
            'OUTPUT': current_land_buffer
        }
        current_land_buffers = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
      
        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Intersection Proposed
        alg_params = {
            'INPUT':new_buffer,
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['CalculateLSLUPDK']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['NewLandInt'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
                
        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}
            
        # Calculate LU/LS Area
        alg_params = {
            'INPUT': outputs['NewLandInt']['OUTPUT'],
            'FIELD_NAME':'Proposed Land Unit/Land System Area (km²)',
            'FIELD_TYPE':0,
            'FIELD_LENGTH':10,
            'FIELD_PRECISION':3,
            'NEW_FIELD': True,
            'FORMULA':'round(area( $geometry ) * 0.000001,1)',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateLSLUNew'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
                
        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}
        
        # Delete unneeded fields
        alg_params = {
            'INPUT': outputs['CalculateLSLUNew']['OUTPUT'],
            'COLUMN': ['fid',
            'layer',
            'path',
            'fid_2',
            'fid_2_2'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeletedWatersNewLULS'] = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
      
        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}
            
        # Join current watered area attribute to proposed watered area buffer
        
        alg_params = {
            'INPUT': outputs['DeletedWatersNewLULS']['OUTPUT'],
            'FIELD': 'Paddock Land Unit/Land System Area (km²)',
            'INPUT_2': current_land_buffer,
            'FIELD_2': 'Paddock Land Unit/Land System Area (km²)',
            'FIELDS_TO_COPY': ['Current Land Unit/Land System Area (km²)', 'Current AE in A Condition', 'Current AE in B Condition', 'Current AE in C Condition', 'Current AE in D Condition'],
            'METHOD': 1,
            'DISCARD_NONMATCHING': False,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinedLandUnits'] = processing.run("native:joinattributestable", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}
            
         # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Current Land Unit/Land System Area (km²)',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 0,
            'FORMULA': 'if( \"Current Land Unit/Land System Area (km²)\" IS NULL, 0,\"Current Land Unit/Land System Area (km²)\" )',
            'INPUT': outputs['JoinedLandUnits']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCurrentLU'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)    
        
        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}
            
        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Land Unit/Land System Watered Area Difference (km²)',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 0,
            'FORMULA': 'round( \"Proposed Land Unit/Land System Area (km²)\" - \"Current Land Unit/Land System Area (km²)\" ,1)',
            'INPUT': outputs['FieldCalculatorCurrentLU']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCurrentLUDiff'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True) 

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}
            
        alg_params = {
            'INPUT': outputs['FieldCalculatorCurrentLUDiff']['OUTPUT'],
            'FIELDS_MAPPING':[{'expression': '"Paddock Name"', 'length': 0, 'name': 'Paddock Name', 'precision': 0, 'type': 10}, 
            {'expression': '"Paddock Area (km²)"', 'length': 0, 'name': 'Paddock Area (km²)', 'precision': 0, 'type': 6}, 
            {'expression': '"Buffer Distance (km)"', 'length': 0, 'name': 'Buffer Distance (km)', 'precision': 0, 'type': 2}, 
            {'expression': '"Current Watered Area (km²)"', 'length': 0, 'name': 'Current Watered Area (km²)', 'precision': 0, 'type': 6}, 
            {'expression': '"Current Watered Area (%)"', 'length': 0, 'name': 'Current Watered Area (%)', 'precision': 0, 'type': 6}, 
            {'expression': '"Proposed Watered Area (km²)"', 'length': 0, 'name': 'Proposed Watered Area (km²)', 'precision': 0, 'type': 6}, 
            {'expression': '"Proposed Watered Area (%)"', 'length': 0, 'name': 'Proposed Watered Area (%)', 'precision': 0, 'type': 6}, 
            {'expression': '"Proposed Watered Area Difference (km²)"', 'length': 0, 'name': 'Proposed Watered Area Difference (km²)', 'precision': 0, 'type': 6}, 
            {'expression': '"Land System"', 'length': 50, 'name': 'Land System', 'precision': 0, 'type': 10}, 
            {'expression': '"Map Unit"', 'length': 10, 'name': 'Map Unit', 'precision': 0, 'type': 10}, 
            {'expression': '"Original Land System"', 'length': 50, 'name': 'Original Land System', 'precision': 0, 'type': 10}, 
            {'expression': '"Original Map Unit"', 'length': 10, 'name': 'Original Map Unit', 'precision': 0, 'type': 10}, 
            {'expression': '"Landscape Class"', 'length': 50, 'name': 'Landscape Class', 'precision': 0, 'type': 10}, 
            {'expression': '"Class Description"', 'length': 254, 'name': 'Class Description', 'precision': 0, 'type': 10}, 
            {'expression': '"Erosion Risk"', 'length': 100, 'name': 'Erosion Risk', 'precision': 0, 'type': 10}, 
            {'expression': '"AE/km²"', 'length': 0, 'name': 'AE/km²', 'precision': 0, 'type': 6}, 
            {'expression': '"Paddock Land Unit/Land System Area (km²)"', 'length': 0, 'name': 'Paddock Land Unit/Land System Area (km²)', 'precision': 0, 'type': 6}, 
            {'expression': '"Current Land Unit/Land System Area (km²)"', 'length': 0, 'name': 'Current Land Unit/Land System Area (km²)', 'precision': 0, 'type': 6}, 
            {'expression': 'round( "Current Land Unit/Land System Area (km²)" / "Current Watered Area (km²)" *100,1)', 'length': 0, 'name': 'Current Land Unit/Land System Area (%)', 'precision': 0, 'type': 6}, 
            {'expression': '"Proposed Land Unit/Land System Area (km²)"', 'length': 0, 'name': 'Proposed Land Unit/Land System Area (km²)', 'precision': 0, 'type': 6}, 
            {'expression': 'round("Proposed Land Unit/Land System Area (km²)" / "Proposed Watered Area (km²)" * 100,1)', 'length': 0, 'name': 'Proposed Land Unit/Land System Area (%)', 'precision': 0, 'type': 6}, 
            {'expression': '"Land Unit/Land System Watered Area Difference (km²)"', 'length': 0, 'name': 'Land Unit/Land System Watered Area Difference (km²)', 'precision': 0, 'type': 6}, 
            {'expression': '"Current AE in A Condition"', 'length': 0, 'name': 'Current AE in A Condition', 'precision': 0, 'type': 6}, 
            {'expression': '"Current AE in B Condition"', 'length': 0, 'name': 'Current AE in B Condition', 'precision': 0, 'type': 6},
            {'expression': '"Current AE in C Condition"', 'length': 0, 'name': 'Current AE in C Condition', 'precision': 0, 'type': 6},
            {'expression': '"Current AE in D Condition"', 'length': 0, 'name': 'Current AE in  D Condition', 'precision': 0, 'type': 6},
            {'expression': ' round("AE/km²" *  "Proposed Land Unit/Land System Area (km²)" ,1)', 'length': 0, 'name': 'Proposed AE in A Condition', 'precision': 0, 'type': 6},
            {'expression': ' round(("AE/km²" * 0.75) *  "Proposed Land Unit/Land System Area (km²)" ,1)', 'length': 0, 'name': 'Proposed AE in B Condition', 'precision': 0, 'type': 6},
            {'expression': ' round(("AE/km²" * 0.5) *  "Proposed Land Unit/Land System Area (km²)" ,1)', 'length': 0, 'name': 'Proposed AE in C Condition', 'precision': 0, 'type': 6},
            {'expression': '0', 'length': 0, 'name': 'Proposed AE in D Condition', 'precision': 0, 'type': 6}],
            'OUTPUT': new_land_buffer
        }
        new_land_buffers = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            
        return {self.NWAREA : new_buffers, self.CWAREA : current_buffers, self.CWLAREA: current_land_buffers, self.NWLAREA : new_land_buffers}
        