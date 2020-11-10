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


class WaterpointBuffers(QgsProcessingAlgorithm):
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
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'icons/buffer.png'))) # icon for the Paddock Power Tools Group in Toolbox
        return icon
        
    def group(self):
        return 'Waterpoint Tools'
    
    def groupId(self):
        return 'Waterpoint Tools'
 
    def createInstance(self):
        return type(self)()
   
    def initAlgorithm(self, config=None):
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
        feedback = QgsProcessingMultiStepFeedback(65, model_feedback)
        current_buffer = self.parameterAsOutputLayer(parameters, self.CWAREA, context)
        new_buffer = self.parameterAsOutputLayer(parameters, self.NWAREA, context)
        current_land_buffer = self.parameterAsOutputLayer(parameters, self.CWLAREA, context)
        new_land_buffer = self.parameterAsOutputLayer(parameters, self.NWLAREA, context)
        results = {}
        outputs = {}
        
        # Reproject Current Waters
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
            'COLUMN': ['WPT_NAME','WPT_COMMISIONED','WPT_DECOMISSIONED','WPT_ACTIVE','WPT_PROPOSED','FID'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeletedCurrentWaters'] = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            
        # Reproject Paddocks
        alg_params = {
            'INPUT': parameters['PADDOCK'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectPaddocks'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
            
        # Reproject Land Units / Systems
        alg_params = {
            'INPUT': parameters['LANDUNIT'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLandUnit'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
            
        # Extract by expression Current Waters
        alg_params = {
            'EXPRESSION': ' \"WPT_TYPE\"  =  \'Trough\' OR  \"WPT_TYPE\" = \'Waterhole\' OR  \"WPT_TYPE\" = \'Turkey Nest\'',
            'INPUT': outputs['DeletedCurrentWaters']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpressionCurrentWaters'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Extract by location Current Waters
        alg_params = {
            'INPUT': outputs['ExtractByExpressionCurrentWaters']['OUTPUT'],
            'INTERSECT': outputs['ReprojectPaddocks']['OUTPUT'],
            'PREDICATE': [0],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByLocationCurrentWaters'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Current 2km Buffer
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 2000,
            'END_CAP_STYLE': 0,
            'INPUT': outputs['ExtractByLocationCurrentWaters']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 25,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Current2kmBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Intersection 2km Current
        alg_params = {
            'INPUT': outputs['Current2kmBuffer']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectPaddocks']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Intersection2kmCurrent'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST 2km Current
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DISTKM',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '2',
            'INPUT': outputs['Intersection2kmCurrent']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist2km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}
            
        # Calc CURR_WAREA 2km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'CURR_WAREAKM2',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001,4)',
            'INPUT': outputs['AddWa_dist2km']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcCurr_warea2km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}
            
            
        # Intersection Current 2km LU
        alg_params = {
            'INPUT': outputs['CalcCurr_warea2km']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectLandUnit']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionCurrent2kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

            
        # Current 3km Buffer
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 3000,
            'END_CAP_STYLE': 0,
            'INPUT': outputs['ExtractByLocationCurrentWaters']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 25,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Current3kmBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}
            
        # Intersection 3km Current
        alg_params = {
            'INPUT': outputs['Current3kmBuffer']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectPaddocks']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Intersection3kmCurrent'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST 3km Current
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DISTKM',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '3',
            'INPUT': outputs['Intersection3kmCurrent']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist3km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}
            
        # Calc CURR_WAREA 3km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'CURR_WAREAKM2',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001,4)',
            'INPUT': outputs['AddWa_dist3km']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcCurr_warea3km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}
            
            
        # Intersection Current 3km LU
        alg_params = {
            'INPUT': outputs['CalcCurr_warea3km']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectLandUnit']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionCurrent3kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}
            
        # Current 5km Buffer
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 5000,
            'END_CAP_STYLE': 0,
            'INPUT': outputs['ExtractByLocationCurrentWaters']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 25,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Current5kmBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}
        
        # Intersection 5km Current
        alg_params = {
            'INPUT': outputs['Current5kmBuffer']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectPaddocks']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Intersection5kmCurrent'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST 5km Current
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DISTKM',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '5',
            'INPUT': outputs['Intersection5kmCurrent']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist5km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}
            
            
        # Calc CURR_WAREA 5km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'CURR_WAREAKM2',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001,4)',
            'INPUT': outputs['AddWa_dist5km']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcCurr_warea5km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}
            
        # Intersection Current 5km LU
        alg_params = {
            'INPUT': outputs['CalcCurr_warea5km']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectLandUnit']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionCurrent5kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}
            
        # Current 8km Buffer
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 8000,
            'END_CAP_STYLE': 0,
            'INPUT': outputs['ExtractByLocationCurrentWaters']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 25,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Current8kmBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}
            
        # Intersection 8km Current
        alg_params = {
            'INPUT': outputs['Current8kmBuffer']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectPaddocks']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Intersection8kmCurrent'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST 8km Current
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DISTKM',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '8',
            'INPUT': outputs['Intersection8kmCurrent']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist8km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}
            
        # Calc CURR_WAREA 8km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'CURR_WAREAKM2',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001,4)',
            'INPUT': outputs['AddWa_dist8km']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcCurr_warea8km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}
            
        # Intersection Current 8km LU/LS
        alg_params = {
            'INPUT': outputs['CalcCurr_warea8km']['OUTPUT'],
            'INPUT_FIELDS': '',
            'OVERLAY': outputs['ReprojectLandUnit']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionCurrent8kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

            
        # Merge Current Watered Areas
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'LAYERS': [outputs['CalcCurr_warea8km']['OUTPUT'],outputs['CalcCurr_warea5km']['OUTPUT'],outputs['CalcCurr_warea3km']['OUTPUT'],outputs['CalcCurr_warea2km']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeCurrent'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}
            
        # Order Current Watered Areas from highest to lowest
        alg_params = {
            'ASCENDING': False,
            'EXPRESSION': 'WA_DISTKM',
            'INPUT': outputs['MergeCurrent']['OUTPUT'],
            'NULLS_FIRST': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            #'OUTPUT': current_buffer
        }
        outputs['OrderByExpressionCurrent'] = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        #current_buffers = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}
        
        # Delete unneeded fields
        alg_params = {
            'INPUT': outputs['OrderByExpressionCurrent']['OUTPUT'],
            'COLUMN': ['WPT_NAME','WPT_TYPE','WPT_COMMISIONED','WPT_DECOMISSIONED','WPT_ACTIVE','WPT_PROPOSED','fid_2','layer','path','FID'],
            'OUTPUT': current_buffer
        }
        current_buffers = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
      
        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}
            
        # Merge Current LU/LS Watered Areas
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['IntersectionCurrent8kmLu']['OUTPUT'],outputs['IntersectionCurrent5kmLu']['OUTPUT'],outputs['IntersectionCurrent3kmLu']['OUTPUT'],outputs['IntersectionCurrent2kmLu']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeCurrentLand'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}
            
        # Order Current LU/LS Watered Areas from highest to lowest
        alg_params = {
            'ASCENDING': False,
            'EXPRESSION': 'WA_DISTKM',
            'INPUT': outputs['MergeCurrentLand']['OUTPUT'],
            'NULLS_FIRST': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            #'OUTPUT': current_land_buffer
        }
        outputs['OrderByExpressionLand'] = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        #current_land_buffers = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}
            
        # Calculate LU/LS Area
        alg_params = {
            'INPUT': outputs['OrderByExpressionLand']['OUTPUT'],
            'FIELD_NAME':'LU_LS_AREAKM',
            'FIELD_TYPE':0,
            'FIELD_LENGTH':10,
            'FIELD_PRECISION':3,
            'NEW_FIELD': False,
            'FORMULA':'round(area( $geometry ) * 0.000001,3)',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateLSLU'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        # Delete unneeded fields
        alg_params = {
            'INPUT': outputs['CalculateLSLU']['OUTPUT'],
            'COLUMN': ['WPT_NAME','WPT_TYPE','WPT_COMMISIONED','WPT_DECOMISSIONED','WPT_ACTIVE','WPT_PROPOSED','fid_2','layer','path','FID', 'fid_3'],
            'OUTPUT': current_land_buffer
        }
        current_land_buffers = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
      
        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}
            

#-------------------------------------------------------------------------------------------------------------------------------------------        

        # Reproject New Waters
        alg_params = {
            'INPUT': parameters['NEWWATER'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectNewWaters'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}
                 
        # Extract by expression New Waters
        alg_params = {
            'EXPRESSION': ' \"WPT_TYPE\"  =  \'Trough\' OR  \"WPT_TYPE\" = \'Waterhole\' OR  \"WPT_TYPE\" = \'Turkey Nest\' OR  \"WPT_TYPE\" = \'Dam\'',
            'INPUT': outputs['ReprojectNewWaters']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            #'OUTPUT': outputFile
        }
        outputs['ExtractByExpressionNewWaters'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)            
        
        feedback.setCurrentStep(33)
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

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Merge Current and New WP
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'LAYERS': [outputs['ExtractByLocationNewWaters']['OUTPUT'],outputs['ExtractByLocationCurrentWaters']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeCurrentAndNewWp'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # New 2km Buffer
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 2000,
            'END_CAP_STYLE': 0,
            'INPUT': outputs['MergeCurrentAndNewWp']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 25,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['New2kmBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Intersection 2km New
        alg_params = {
            'INPUT': outputs['New2kmBuffer']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectPaddocks']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Intersection2kmNew'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST 2km New
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DISTKM',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '2',
            'INPUT': outputs['Intersection2kmNew']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist2kmNew'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}
            
        # Calc NEW_WAREA 2km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'NEW_WAREAKM2',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001,4)',
            'INPUT': outputs['AddWa_dist2kmNew']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcNew_warea2km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}
            
        # Intersection New 2km LU
        alg_params = {
            'INPUT': outputs['CalcNew_warea2km']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectLandUnit']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionNew2kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # New 3km Buffer
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 3000,
            'END_CAP_STYLE': 0,
            'INPUT': outputs['MergeCurrentAndNewWp']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 25,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['New3kmBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}
            
        # Intersection 3km New
        alg_params = {
            'INPUT': outputs['New3kmBuffer']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectPaddocks']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Intersection3kmNew'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}        
            
        # Add WA_DIST 3km New
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DISTKM',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '3',
            'INPUT': outputs['Intersection3kmNew']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist3kmNew'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(43)
        if feedback.isCanceled():
            return {}
            
        # Calc NEW_WAREA 3km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'NEW_WAREAKM2',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001,4)',
            'INPUT': outputs['AddWa_dist3kmNew']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcNew_warea3km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}
            
        # Intersection New 3km LU
        alg_params = {
            'INPUT': outputs['CalcNew_warea3km']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectLandUnit']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionNew3kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(45)
        if feedback.isCanceled():
            return {}

        # New 5km Buffer
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 5000,
            'END_CAP_STYLE': 0,
            'INPUT': outputs['MergeCurrentAndNewWp']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 25,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['New5kmBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(46)
        if feedback.isCanceled():
            return {}
            
        # Intersection 5km New
        alg_params = {
            'INPUT': outputs['New5kmBuffer']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectPaddocks']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Intersection5kmNew'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(47)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST 5km New
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DISTKM',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '5',
            'INPUT': outputs['Intersection5kmNew']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist5kmNew'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(48)
        if feedback.isCanceled():
            return {}
                 
        # Calc NEW_WAREA 5km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'NEW_WAREAKM2',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001,4)',
            'INPUT': outputs['AddWa_dist5kmNew']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcNew_warea5km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(49)
        if feedback.isCanceled():
            return {}
            
            
        # Intersection New 5km LU
        alg_params = {
            'INPUT': outputs['CalcNew_warea5km']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectLandUnit']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionNew5kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(50)
        if feedback.isCanceled():
            return {}

        # New 8km Buffer
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 8000,
            'END_CAP_STYLE': 0,
            'INPUT': outputs['MergeCurrentAndNewWp']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 25,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['New8kmBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(51)
        if feedback.isCanceled():
            return {}


        # Intersection 8km New
        alg_params = {
            'INPUT': outputs['New8kmBuffer']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectPaddocks']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Intersection8kmNew'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(52)
        if feedback.isCanceled():
            return {}

        # Add WA_DIST 8km New
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DISTKM',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '8',
            'INPUT': outputs['Intersection8kmNew']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist8kmNew'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(53)
        if feedback.isCanceled():
            return {}

        # Calc NEW_WAREA 8km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'NEW_WAREAKM2',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001,4)',
            'INPUT': outputs['AddWa_dist8kmNew']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcNew_warea8km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(54)
        if feedback.isCanceled():
            return {}
            
        # Intersection New 8km LU
        alg_params = {
            'INPUT': outputs['CalcNew_warea8km']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': outputs['ReprojectLandUnit']['OUTPUT'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionNew8kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(55)
        if feedback.isCanceled():
            return {}      

        # Merge New Watered Area buffers
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'LAYERS': [outputs['CalcNew_warea8km']['OUTPUT'],outputs['CalcNew_warea5km']['OUTPUT'],outputs['CalcNew_warea3km']['OUTPUT'],outputs['CalcNew_warea2km']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeNew'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(56)
        if feedback.isCanceled():
            return {}

        # Order New Watered areas highest to lowest
        alg_params = {
            'ASCENDING': False,
            'EXPRESSION': 'WA_DISTKM',
            'INPUT': outputs['MergeNew']['OUTPUT'],
            'NULLS_FIRST': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['OrderByExpressionNew'] = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        
        feedback.setCurrentStep(57)
        if feedback.isCanceled():
            return {}
 
        # Delete unneeded fields
        alg_params = {
            'INPUT': outputs['OrderByExpressionNew']['OUTPUT'],
            'COLUMN': ['FID','WPT_NAME','WPT_TYPE','WPT_COMMISIONED','WPT_DECOMISSIONED','WPT_ACTIVE','WPT_PROPOSED','fid_2','layer','path','fid_3'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeleteFieldsNew'] = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
      
        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}           
           
        # Merge vector layers
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['IntersectionNew8kmLu']['OUTPUT'],outputs['IntersectionNew5kmLu']['OUTPUT'],outputs['IntersectionNew3kmLu']['OUTPUT'],outputs['IntersectionNew2kmLu']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeNewLU'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(58)
        if feedback.isCanceled():
            return {}
            
        # Order New Watered LU/LS areas highest to lowest
        alg_params = {
            'ASCENDING': False,
            'EXPRESSION': 'WA_DISTKM',
            'INPUT': outputs['MergeNewLU']['OUTPUT'],
            'NULLS_FIRST': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            #'OUTPUT': new_land_buffer
        }
        outputs['OrderNewLU'] = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        #new_land_buffers = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(59)
        if feedback.isCanceled():
            return {}
            
        # Calculate LU/LS Area New
        alg_params = {
            'INPUT': outputs['OrderNewLU']['OUTPUT'],
            'FIELD_NAME':'LU_LS_AREAKM',
            'FIELD_TYPE':0,
            'FIELD_LENGTH':10,
            'FIELD_PRECISION':3,
            'NEW_FIELD': False,
            'FORMULA':'round(area( $geometry ) * 0.000001,3)',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateLSLUNew'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        # Delete unneeded fields
        alg_params = {
            'INPUT': outputs['CalculateLSLUNew']['OUTPUT'],
            'COLUMN': ['WPT_NAME','WPT_TYPE','WPT_COMMISIONED','WPT_DECOMISSIONED','WPT_ACTIVE','WPT_PROPOSED','fid_2','layer','path','FID', 'fid_3'],
            'OUTPUT': new_land_buffer
        }
        new_land_buffers = processing.run("qgis:deletecolumn", alg_params, context=context, feedback=feedback, is_child_algorithm=True)
      
        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}           
           
        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'WA_DISTKM',
            'FIELDS_TO_COPY': 'CURR_WAREAKM2',
            'FIELD_2': 'WA_DISTKM',
            'INPUT': outputs['DeleteFieldsNew']['OUTPUT'],
            'INPUT_2': current_buffer,
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(60)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WAREA_DIFFKM2',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 0,
            'FORMULA': 'round( \"NEW_WAREAKM2\" - \"CURR_WAREAKM2\" ,1)',
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': new_buffer
        }
        new_buffers = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(61)
        if feedback.isCanceled():
            return {}
        
        #return {self.CWAREA : current_buffers, self.CWLAREA : current_land_buffers}
        return {self.CWAREA : current_buffers, self.NWAREA : new_buffers, self.CWLAREA : current_land_buffers, self.NWLAREA : new_land_buffers}
        