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
            
        # Reproject Paddocks
        alg_params = {
            'INPUT': parameters['PADDOCK'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectPaddocks'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
            
        # Reproject Land Units / Systems
        alg_params = {
            'INPUT': parameters['LANDUNIT'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLandUnit'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
            
        # Extract by expression Current Waters
        alg_params = {
            'EXPRESSION': ' \"Type\"  =  \'Trough\' OR  \"Type\" = \'Waterhole\' OR  \"Type\" = \'Turkey Nest\'',
            'INPUT': outputs['ReprojectCurrentWaters']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpressionCurrentWaters'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
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

        feedback.setCurrentStep(5)
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

        feedback.setCurrentStep(6)
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

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST 2km Current
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DIST',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '2',
            'INPUT': outputs['Intersection2kmCurrent']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist2km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}
            
        # Calc CURR_WAREA 2km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'CURR_WAREA',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001),3',
            'INPUT': outputs['AddWa_dist2km']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcCurr_warea2km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}
            
            
        # Intersection Current 2km LU
        alg_params = {
            'INPUT': outputs['CalcCurr_warea2km']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': parameters['ReprojectLandUnit'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionCurrent2kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
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

        feedback.setCurrentStep(11)
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

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST 3km Current
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DIST',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '3',
            'INPUT': outputs['Intersection3kmCurrent']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist3km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}
            
        # Calc CURR_WAREA 3km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'CURR_WAREA',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'area($geometry) * 0.000001',
            'INPUT': outputs['AddWa_dist3km']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcCurr_warea3km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}
            
            
        # Intersection Current 3km LU
        alg_params = {
            'INPUT': outputs['CalcCurr_warea3km']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': parameters['ReprojectLandUnit'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionCurrent3kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
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

        feedback.setCurrentStep(16)
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

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST 5km Current
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DIST',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '5',
            'INPUT': outputs['Intersection5kmCurrent']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist5km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}
            
            
        # Calc CURR_WAREA 5km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'CURR_WAREA',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'area($geometry) * 0.000001',
            'INPUT': outputs['AddWa_dist5km']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcCurr_warea5km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}
            
        # Intersection Current 5km LU
        alg_params = {
            'INPUT': outputs['CalcCurr_warea5km']['OUTPUT'],
            'INPUT_FIELDS': None,
            'OVERLAY': parameters['ReprojectLandUnit'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionCurrent5kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
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

        feedback.setCurrentStep(21)
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

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}
            
        # Add WA_DIST 8km Current
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'WA_DIST',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '8',
            'INPUT': outputs['Intersection8kmCurrent']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddWa_dist8km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}
            
        # Calc CURR_WAREA 8km
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'CURR_WAREA',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'round(area($geometry) * 0.000001),3',
            'INPUT': outputs['AddWa_dist8km']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalcCurr_warea8km'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}
            
        # Intersection Current 8km LU/LS
        alg_params = {
            'INPUT': outputs['CalcCurr_warea8km']['OUTPUT'],
            'INPUT_FIELDS': '',
            'OVERLAY': parameters['ReprojectLandUnit'],
            'OVERLAY_FIELDS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IntersectionCurrent8kmLu'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

            
        # Merge Current Watered Areas
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'LAYERS': [outputs['CalcCurr_warea2km']['OUTPUT'],outputs['CalcCurr_warea3km']['OUTPUT'],outputs['CalcCurr_warea5km']['OUTPUT'],outputs['CalcCurr_warea8km']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeCurrent'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}
            
        # Order Current Watered Areas from highest to lowest
        alg_params = {
            'ASCENDING': False,
            'EXPRESSION': 'WA_DIST',
            'INPUT': outputs['MergeCurrent']['OUTPUT'],
            'NULLS_FIRST': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['OrderByExpressionCurrent'] = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}
            
        # Refactor fields Current WA fields - Final Ouput for Current Watered Areas
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '"Name_2"', 'length': 80, 'name': 'PADDOCK', 'precision': 0, 'type': 10}, {'expression': '"PDKAREAKM2"', 'length': 0, 'name': 'PDKAREAKM2', 'precision': 1, 'type': 6}, {'expression': '"WA_DIST"', 'length': 10, 'name': 'WA_DISTKM', 'precision': 3, 'type': 2}, {'expression': '"CURR_WAREA"', 'length': 10, 'name': 'CURR_WAREAKM2', 'precision': 1, 'type': 6}],
            'INPUT': outputs['OrderByExpressionCurrent']['OUTPUT'],
            'OUTPUT': current_buffer
        }
        current_buffers = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}
            
        # Merge Current LU/LS Watered Areas
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['IntersectionCurrent2kmLu']['OUTPUT'],outputs['IntersectionCurrent3kmLu']['OUTPUT'],outputs['IntersectionCurrent5kmLu']['OUTPUT'],outputs['IntersectionCurrent8kmLu']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeCurrentLand'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}
            
        # Order Current LU/LS Watered Areas from highest to lowest
        alg_params = {
            'ASCENDING': False,
            'EXPRESSION': 'WA_DIST',
            'INPUT': outputs['MergeCurrentLand']['OUTPUT'],
            'NULLS_FIRST': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['OrderByExpressionLand'] = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}
            
        # Refactor fields Current LU/LS - Final Ouput for Current Watered Area LU/LS
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '"NAME_2"', 'length': 17, 'name': 'NAME', 'precision': 0, 'type': 10}, {'expression': '"PROPERTY"', 'length': 50, 'name': 'PROPERTY', 'precision': 0, 'type': 10}, {'expression': '"PDKAREAKM2"', 'length': 0, 'name': 'PDKAREAKM2', 'precision': 0, 'type': 6}, {'expression': '"WA_DIST"', 'length': 10, 'name': 'WA_DIST', 'precision': 3, 'type': 2}, {'expression': '"CURR_WAREA"', 'length': 10, 'name': 'CURR_WAREA', 'precision': 1, 'type': 6}, {'expression': '"SURVEY_NME"', 'length': 254, 'name': 'SURVEY_NME', 'precision': 0, 'type': 10}, {'expression': '"SURVEY_ID"', 'length': 5, 'name': 'SURVEY_ID', 'precision': 0, 'type': 10}, {'expression': '"LAND_UNIT"', 'length': 10, 'name': 'LAND_UNIT', 'precision': 0, 'type': 10}, {'expression': '"LF_CLASS"', 'length': 50, 'name': 'LF_CLASS', 'precision': 0, 'type': 10}, {'expression': '"SOIL_SYS"', 'length': 10, 'name': 'SOIL_SYS', 'precision': 0, 'type': 10}, {'expression': '"SOIL"', 'length': 50, 'name': 'SOIL', 'precision': 0, 'type': 10}, {'expression': '"VEG_SYS"', 'length': 15, 'name': 'VEG_SYS', 'precision': 0, 'type': 10}, {'expression': '"VEG_STRUC"', 'length': 50, 'name': 'VEG_STRUC', 'precision': 0, 'type': 10}, {'expression': '"SPECIES_1"', 'length': 50, 'name': 'SPECIES_1', 'precision': 0, 'type': 10}, {'expression': '"SPECIES_2"', 'length': 50, 'name': 'SPECIES_2', 'precision': 0, 'type': 10}, {'expression': '"SPECIES_3"', 'length': 50, 'name': 'SPECIES_3', 'precision': 0, 'type': 10}, {'expression': '"LF_DESC"', 'length': 254, 'name': 'LF_DESC', 'precision': 0, 'type': 10}, {'expression': '"SOIL_DESC"', 'length': 254, 'name': 'SOIL_DESC', 'precision': 0, 'type': 10}, {'expression': '"VEG_DESC"', 'length': 254, 'name': 'VEG_DESC', 'precision': 0, 'type': 10}, {'expression': 'area($geometry) * 0.000001', 'length': 0, 'name': 'LUAREAKM2', 'precision': 0, 'type': 6}],
            'INPUT': outputs['OrderByExpressionLand']['OUTPUT'],
            'OUTPUT': current_land_buffer
        }
        current_land_buffers = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
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
        
        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Merge Current and New WP
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:7845'),
            'LAYERS': [outputs['ExtractByLocationNewWaters']['OUTPUT'],outputs['ExtractByLocationCurrentWaters']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeCurrentAndNewWp'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Extract by expression New Waters
        alg_params = {
            'EXPRESSION': ' \"Type\"  =  \'Trough\' OR  \"Type\" = \'Waterhole\' OR  \"Type\" = \'Turkey Nest\' OR  \"Type\" = \'Dam\'',
            'INPUT': outputs['ReprojectNewWaters']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            #'OUTPUT': outputFile
        }
        outputs['ExtractByExpressionNewWaters'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        feedback.setCurrentStep(34)
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
            'FIELD_NAME': 'WA_DIST',
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
            'FIELD_NAME': 'NEW_WAREA',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 0,
            'FORMULA': 'area($geometry) * 0.000001',
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
            'OVERLAY': parameters['ReprojectLandUnit'],
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
            'FIELD_NAME': 'WA_DIST',
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
            'FIELD_NAME': 'NEW_WAREA',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 0,
            'FORMULA': 'area($geometry) * 0.000001',
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
            'OVERLAY': parameters['ReprojectLandUnit'],
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
            'FIELD_NAME': 'WA_DIST',
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
            'FIELD_NAME': 'NEW_WAREA',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'area($geometry) * 0.000001',
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
            'OVERLAY': parameters['ReprojectLandUnit'],
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
            'FIELD_NAME': 'WA_DIST',
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
            'FIELD_NAME': 'NEW_WAREA',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'area($geometry) * 0.000001',
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
            'OVERLAY': parameters['ReprojectLandUnit'],
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
            'LAYERS': [outputs['CalcNew_warea2km']['OUTPUT'],outputs['CalcNew_warea3km']['OUTPUT'],outputs['CalcNew_warea5km']['OUTPUT'],outputs['CalcNew_warea8km']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeNew'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(56)
        if feedback.isCanceled():
            return {}

        # Order New Watered areas highest to lowest
        alg_params = {
            'ASCENDING': False,
            'EXPRESSION': 'WA_DIST',
            'INPUT': outputs['MergeNew']['OUTPUT'],
            'NULLS_FIRST': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['OrderByExpressionNew'] = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(57)
        if feedback.isCanceled():
            return {}
            
        # Refactor fields New
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '"Name_2"', 'length': 80, 'name': 'PADDOCK', 'precision': 0, 'type': 10}, {'expression': '"PDKAREAKM2"', 'length': 0, 'name': 'PDKAREAKM2', 'precision': 1, 'type': 6}, {'expression': '"WA_DIST"', 'length': 10, 'name': 'WA_DISTKM', 'precision': 3, 'type': 2}, {'expression': '"NEW_WAREA"', 'length': 10, 'name': 'NEW_WAREAKM2', 'precision': 3, 'type': 6}],
            'INPUT': outputs['OrderByExpressionNew']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFieldsNew'] = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(58)
        if feedback.isCanceled():
            return {}
            
        # Merge vector layers
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['IntersectionNew2kmLu']['OUTPUT'],outputs['IntersectionNew5kmLu']['OUTPUT'],outputs['IntersectionNew3kmLu']['OUTPUT'],outputs['IntersectionNew8kmLu']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeNewLU'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(59)
        if feedback.isCanceled():
            return {}
            
        # Order New Watered LU/LS areas highest to lowest
        alg_params = {
            'ASCENDING': False,
            'EXPRESSION': 'WA_DIST',
            'INPUT': outputs['MergeNewLU']['OUTPUT'],
            'NULLS_FIRST': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['OrderNewLU'] = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(60)
        if feedback.isCanceled():
            return {}
            
        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '"NAME_2"', 'length': 17, 'name': 'NAME', 'precision': 0, 'type': 10}, {'expression': '"LAYER"', 'length': 7, 'name': 'LAYER', 'precision': 0, 'type': 10}, {'expression': '"PROPERTY"', 'length': 50, 'name': 'PROPERTY', 'precision': 0, 'type': 10}, {'expression': '"PDKAREAKM2"', 'length': 0, 'name': 'PDKAREAKM2', 'precision': 0, 'type': 6}, {'expression': '"WA_DIST"', 'length': 10, 'name': 'WA_DIST', 'precision': 3, 'type': 2}, {'expression': '"CURR_WAREA"', 'length': 10, 'name': 'CURR_WAREA', 'precision': 1, 'type': 6}, {'expression': '"SURVEY_NME"', 'length': 254, 'name': 'SURVEY_NME', 'precision': 0, 'type': 10}, {'expression': '"SURVEY_ID"', 'length': 5, 'name': 'SURVEY_ID', 'precision': 0, 'type': 10}, {'expression': '"LAND_UNIT"', 'length': 10, 'name': 'LAND_UNIT', 'precision': 0, 'type': 10}, {'expression': '"LF_CLASS"', 'length': 50, 'name': 'LF_CLASS', 'precision': 0, 'type': 10}, {'expression': '"SOIL_SYS"', 'length': 10, 'name': 'SOIL_SYS', 'precision': 0, 'type': 10}, {'expression': '"SOIL"', 'length': 50, 'name': 'SOIL', 'precision': 0, 'type': 10}, {'expression': '"VEG_SYS"', 'length': 15, 'name': 'VEG_SYS', 'precision': 0, 'type': 10}, {'expression': '"VEG_STRUC"', 'length': 50, 'name': 'VEG_STRUC', 'precision': 0, 'type': 10}, {'expression': '"SPECIES_1"', 'length': 50, 'name': 'SPECIES_1', 'precision': 0, 'type': 10}, {'expression': '"SPECIES_2"', 'length': 50, 'name': 'SPECIES_2', 'precision': 0, 'type': 10}, {'expression': '"SPECIES_3"', 'length': 50, 'name': 'SPECIES_3', 'precision': 0, 'type': 10}, {'expression': '"LF_DESC"', 'length': 254, 'name': 'LF_DESC', 'precision': 0, 'type': 10}, {'expression': '"SOIL_DESC"', 'length': 254, 'name': 'SOIL_DESC', 'precision': 0, 'type': 10}, {'expression': '"VEG_DESC"', 'length': 254, 'name': 'VEG_DESC', 'precision': 0, 'type': 10}, {'expression': 'round( area($geometry) * 0.000001,1)', 'length': 0, 'name': 'LUAREAKM2', 'precision': 0, 'type': 6}],
            'INPUT': outputs['OrderNewLU']['OUTPUT'],
            'OUTPUT': parameters['NWLAREA']
        }
        new_land_buffers = processing.run('qgis:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'WA_DISTKM',
            'FIELDS_TO_COPY': 'CURR_WAREAKM2',
            'FIELD_2': 'WA_DISTKM',
            'INPUT': outputs['RefactorFieldsNew']['OUTPUT'],
            'INPUT_2': current_buffer,
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(61)
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

        feedback.setCurrentStep(62)
        if feedback.isCanceled():
            return {}
        
        return {self.CWAREA : current_buffers, self.NWAREA : new_buffers, self.CWLAREA : current_land_buffers, self.NWLAREA : new_land_buffers}