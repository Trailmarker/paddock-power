from qgis.PyQt.QtGui import QFont, QColor

from qgis.core import (QgsProject, QgsFillSymbol, QgsSingleSymbolRenderer,
                        QgsPalLayerSettings, QgsTextFormat, QgsTextBufferSettings,
                        QgsVectorLayerSimpleLabeling, QgsSimpleMarkerSymbolLayer,
                        QgsFontMarkerSymbolLayer, QgsMarkerSymbol, QgsMarkerSymbol,
                        QgsCategorizedSymbolRenderer, QgsCategorizedSymbolRenderer,
                        QgsLineSymbol, QgsSingleSymbolRenderer, QgsSingleSymbolRenderer,
                        QgsMapSettings, QgsMapRendererParallelJob, QgsGeometry,
                        QgsFeatureRequest, QgsRendererCategory, QgsSimpleLineSymbolLayer,
                        QgsVectorLayer, QgsPoint, QgsFeature)

class reportUtils():
    
    def __init__(self):
        
        self.project = QgsProject.instance()
        
        self.pdk_lyr = self.project.mapLayersByName('Paddocks')[0]
        self.wpt_lyr = self.project.mapLayersByName('Waterpoints')[0]
        self.fence_lyr = self.project.mapLayersByName('Fences')[0]
        self.pipe_lyr = self.project.mapLayersByName('Pipelines')[0]
        self.wa_lyr = self.project.mapLayersByName('Watered Areas')[0]
        
        
    def getDevelopedPaddocks(self):
        developed_paddocks = []
        planned_waterpoints = [wp for wp in self.wpt_lyr.getFeatures() if wp['Status'] == 'Planned']
        for wpt in planned_waterpoints:
            paddock = [pdk for pdk in self.pdk_lyr.getFeatures() if wpt.geometry().within(pdk.geometry())][0]
            if not paddock['Name'] in developed_paddocks:
                developed_paddocks.append(paddock['Name'])
        planned_fences = [f for f in self.fence_lyr.getFeatures() if f['Status'] == 'Planned']
        for f in planned_fences:
            paddock = [pdk for pdk in self.pdk_lyr.getFeatures() if f.geometry().intersection(pdk.geometry()).length()>5][0]
            if not paddock['Name'] in developed_paddocks:
                developed_paddocks.append(paddock['Name'])
        planned_pipelines = [pl for pl in self.pipe_lyr.getFeatures() if pl['Status'] == 'Planned']
        for pl in planned_pipelines:
            paddock = [pdk for pdk in self.pdk_lyr.getFeatures() if pl.geometry().intersection(pdk.geometry()).length()>5][0]
            if not paddock['Name'] in developed_paddocks:
                developed_paddocks.append(paddock['Name'])
        return developed_paddocks
        
    
    def paddockRenderer(self):
        symbol = QgsFillSymbol.createSimple({'border_width_map_unit_scale': '3x:0,0,0,0,0,0',
                                            'color': '60,179,113,255',
                                            'joinstyle': 'bevel',
                                            'offset': '0,0',
                                            'offset_map_unit_scale': '3x:0,0,0,0,0,0',
                                            'offset_unit': 'MM',
                                            'outline_color': '35,35,35,178',
                                            'outline_style': 'solid',
                                            'outline_width': '0.4',
                                            'outline_width_unit': 'MM',
                                            'style': 'solid'})
        renderer = QgsSingleSymbolRenderer(symbol)
        return renderer
        
    def paddockLabels(self):
        settings = QgsPalLayerSettings()
        txt_format = QgsTextFormat()
        txt_format.setFont(QFont('Arial'))
        txt_format.setSize(10)
        txt_format.setColor(QColor('black'))
        txt_buffer = QgsTextBufferSettings()
        txt_buffer.setSize(0.8)
        txt_buffer.setEnabled(True)
        txt_format.setBuffer(txt_buffer)
        settings.setFormat(txt_format)
        settings.fieldName = """ title(concat("Name",'\n',round("Area (km²)",1),'km²'))"""
        settings.isExpression = True
        settings.drawLabels = True
        labels = QgsVectorLayerSimpleLabeling(settings)
        return labels

    def waterpointRenderer(self):
        fld_name = 'Waterpoint Type'
        categories = []
        base_simple_marker_symbol_layer = QgsSimpleMarkerSymbolLayer.create({'angle': '0', 'cap_style': 'square', 'color': '9,211,251,255', 'horizontal_anchor_point': '1', 'joinstyle': 'bevel', 'name': 'circle', 'offset': '0,0', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 'offset_unit': 'MM', 'outline_color': '35,35,35,0', 'outline_style': 'solid', 'outline_width': '0', 'outline_width_map_unit_scale': '3x:0,0,0,0,0,0', 'outline_width_unit': 'MM', 'scale_method': 'diameter', 'size': '5', 'size_map_unit_scale': '3x:0,0,0,0,0,0', 'size_unit': 'MM', 'vertical_anchor_point': '1'})
        base_font_marker_symbol_layer = QgsFontMarkerSymbolLayer.create({'angle': '0', 'chr': '', 'color': '0,0,0,255', 'font': 'Calibri', 'font_style': 'Bold', 'horizontal_anchor_point': '1', 'joinstyle': 'bevel', 'offset': '0,-1.59999999999999987', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 'offset_unit': 'Point', 'outline_color': '0,0,0,255', 'outline_width': '0', 'outline_width_map_unit_scale': '3x:0,0,0,0,0,0', 'outline_width_unit': 'Point', 'size': '8', 'size_map_unit_scale': '3x:0,0,0,0,0,0', 'size_unit': 'Point', 'vertical_anchor_point': '1'})
        ###
        value_map = {'Bore':'B', 'Dam':'D', 'Trough':'T', 'Turkey Nest':'TN', 'Water Tank':'WT', 'Waterhole':'WH',}
        for k, v in value_map.items():
            waterpoint_symbol = QgsMarkerSymbol()
            waterpoint_symbol.appendSymbolLayer(base_simple_marker_symbol_layer.clone())
            waterpoint_font_marker = base_font_marker_symbol_layer.clone()
            waterpoint_font_marker.setCharacter(v)
            waterpoint_symbol.appendSymbolLayer(waterpoint_font_marker)
            waterpoint_cat = QgsRendererCategory(k, waterpoint_symbol, k)
            categories.append(waterpoint_cat)
        renderer = QgsCategorizedSymbolRenderer(fld_name, categories)
        return renderer
        
    def pipelineRenderer(self):
        symbol_layer_1 = QgsSimpleLineSymbolLayer.create({'align_dash_pattern': '0',
                                                            'capstyle': 'round',
                                                            'customdash': '5;2',
                                                            'customdash_map_unit_scale': '3x:0,0,0,0,0,0',
                                                            'customdash_unit': 'MM',
                                                            'dash_pattern_offset': '0',
                                                            'dash_pattern_offset_map_unit_scale': '3x:0,0,0,0,0,0',
                                                            'dash_pattern_offset_unit': 'MM',
                                                            'draw_inside_polygon': '0',
                                                            'joinstyle': 'round',
                                                            'line_color': '0,0,0,255',
                                                            'line_style': 'solid',
                                                            'line_width': '2.06',
                                                            'line_width_unit': 'MM',
                                                            'offset': '0',
                                                            'offset_map_unit_scale': '3x:0,0,0,0,0,0',
                                                            'offset_unit': 'MM',
                                                            'ring_filter': '0',
                                                            'trim_distance_end': '0',
                                                            'trim_distance_end_map_unit_scale': '3x:0,0,0,0,0,0',
                                                            'trim_distance_end_unit': 'MM',
                                                            'trim_distance_start': '0',
                                                            'trim_distance_start_map_unit_scale': '3x:0,0,0,0,0,0',
                                                            'trim_distance_start_unit': 'MM',
                                                            'tweak_dash_pattern_on_corners': '0',
                                                            'use_custom_dash': '0',
                                                            'width_map_unit_scale': '3x:0,0,0,0,0,0'})
        symbol_layer_2 = QgsSimpleLineSymbolLayer.create({'align_dash_pattern': '0',
                                                            'capstyle': 'square',
                                                            'customdash': '5;3',
                                                            'customdash_map_unit_scale': '3x:0,0,0,0,0,0',
                                                            'customdash_unit': 'MM',
                                                            'dash_pattern_offset': '0',
                                                            'dash_pattern_offset_map_unit_scale': '3x:0,0,0,0,0,0',
                                                            'dash_pattern_offset_unit': 'MM',
                                                            'draw_inside_polygon': '0',
                                                            'joinstyle': 'round',
                                                            'line_color': '31,120,180,255',
                                                            'line_style': 'dash',
                                                            'line_width': '1.46',
                                                            'line_width_unit': 'MM',
                                                            'offset': '0',
                                                            'offset_map_unit_scale': '3x:0,0,0,0,0,0',
                                                            'offset_unit': 'MM',
                                                            'ring_filter': '0',
                                                            'trim_distance_end': '0',
                                                            'trim_distance_end_map_unit_scale': '3x:0,0,0,0,0,0',
                                                            'trim_distance_end_unit': 'MM',
                                                            'trim_distance_start': '0',
                                                            'trim_distance_start_map_unit_scale': '3x:0,0,0,0,0,0',
                                                            'trim_distance_start_unit': 'MM',
                                                            'tweak_dash_pattern_on_corners': '0',
                                                            'use_custom_dash': '1',
                                                            'width_map_unit_scale': '3x:0,0,0,0,0,0'})
        symbol = QgsLineSymbol()
        symbol.appendSymbolLayer(symbol_layer_1.clone())
        symbol.appendSymbolLayer(symbol_layer_2.clone())
        symbol.deleteSymbolLayer(0)
        renderer = QgsSingleSymbolRenderer(symbol)
        return renderer
                
    def scaleBarRenderer(self):
        symbol_layer = QgsSimpleLineSymbolLayer.create({'line_color': '0,0,0,255', 'line_style': 'solid', 'line_width': '0.35', 'line_width_unit': 'MM',})
        symbol = QgsLineSymbol()
        symbol.appendSymbolLayer(symbol_layer.clone())
        scale_bar_renderer = QgsSingleSymbolRenderer(symbol)
        return scale_bar_renderer
        
    def scaleBarLabels(self):
        settings = QgsPalLayerSettings()
        txt_format = QgsTextFormat()
        txt_format.setFont(QFont('Arial'))
        txt_format.setSize(10)
        txt_format.setColor(QColor('black'))
        settings.setFormat(txt_format)
        settings.fieldName = """concat(to_string(to_int($length/1000)), ' km')"""
        settings.isExpression = True
        settings.drawLabels = True
        settings.placement = QgsPalLayerSettings.Line
        labels = QgsVectorLayerSimpleLabeling(settings)
        return labels
        
    def scaleBarLayer(self, extent):
        scale_bar_layer = QgsVectorLayer('LineString?crs=epsg:3857', '', 'memory')
        canvas_width = extent.width()
        scale_bar_length = round(canvas_width/5, -3)
        bar_end_point = QgsPoint(extent.xMaximum()-(scale_bar_length/2), extent.yMinimum()+(scale_bar_length/2))
        bar_start_point = QgsPoint(bar_end_point.x()-scale_bar_length, bar_end_point.y())
        tick_start_point = QgsPoint(bar_start_point.x(), bar_start_point.y()+(extent.height()/50))
        tick_end_point = QgsPoint(bar_end_point.x(), bar_end_point.y()+(extent.height()/50))
        geom = QgsGeometry().fromPolyline([tick_start_point, bar_start_point, bar_end_point, tick_end_point])
        feat = QgsFeature()
        feat.setGeometry(geom)
        scale_bar_layer.dataProvider().addFeature(feat)
        scale_bar_layer.updateExtents()
        scale_bar_layer.setRenderer(self.scaleBarRenderer())
        scale_bar_layer.setLabeling(self.scaleBarLabels())
        scale_bar_layer.setLabelsEnabled(True)
        return scale_bar_layer
        

    def currentMapLayers(self, pdk_name):
        map_layers = []
        invalid_layer_names = []
        pdk_feats = [ft for ft in self.pdk_lyr.getFeatures() if ft['Name'] == pdk_name and ft['Timeframe'] == 'Current']
        if not pdk_feats:
            return False
        pdk_feat = pdk_feats[0]
        current_pdk_lyr = self.pdk_lyr.materialize(QgsFeatureRequest([pdk_feat.id()]))
        if current_pdk_lyr.isValid():
            current_pdk_lyr.setRenderer(self.paddockRenderer())
            current_pdk_lyr.setLabeling(self.paddockLabels())
            current_pdk_lyr.setLabelsEnabled(True)
            map_layers.append(current_pdk_lyr)
        else:
            invalid_layer_names.append(current_pdk_lyr.name())
        current_wa_feats = [ft for ft in self.wa_lyr.getFeatures() if ft['Paddock Name'] == pdk_name and ft['Timeframe'] == 'Current']
        if current_wa_feats:
            current_wa_lyr = self.wa_lyr.materialize(QgsFeatureRequest([f.id() for f in current_wa_feats]))
            if current_wa_lyr.isValid():
                renderer = self.wa_lyr.renderer().clone()
                renderer.setClassAttribute('Watered')
                current_wa_lyr.setRenderer(renderer)
                current_wa_lyr.triggerRepaint()
                map_layers.append(current_wa_lyr)
            else:
                invalid_layer_names.append(current_wa_lyr.name())
        built_pipeline_feats = [ft for ft in self.pipe_lyr.getFeatures() if ft['Status'] == 'Built' and ft.geometry().intersects(pdk_feat.geometry())]
        if built_pipeline_feats:
            built_pipeline_lyr = self.pipe_lyr.materialize(QgsFeatureRequest([f.id() for f in built_pipeline_feats]))
            if built_pipeline_lyr.isValid():
                built_pipeline_lyr.setRenderer(self.pipelineRenderer())
                map_layers.append(built_pipeline_lyr)
            else:
                invalid_layer_names.append(built_pipeline_lyr.name())
        pdk_wpt_feats = [ft for ft in self.wpt_lyr.getFeatures() if ft['Status'] == 'Built' and ft.geometry().intersects(pdk_feat.geometry())]
        if pdk_wpt_feats:
            current_wpt_lyr = self.wpt_lyr.materialize(QgsFeatureRequest([f.id() for f in pdk_wpt_feats]))
            if current_wpt_lyr.isValid():
                current_wpt_lyr.setRenderer(self.waterpointRenderer())
                map_layers.append(current_wpt_lyr)
            else:
                invalid_layer_names.append(self.wpt_lyr.name())
        return map_layers
        
        
    def futureMapLayers(self, pdk_name):
        map_layers = []
        invalid_layer_names = []
        # Get current paddock feature (for spatial retrieval of future features)
        current_pdk_feats = [ft for ft in self.pdk_lyr.getFeatures() if ft['Name'] == pdk_name and ft['Timeframe'] == 'Current']
        if not current_pdk_feats:
            return False
        current_pdk_feat = current_pdk_feats[0]
        current_pdk_geom = current_pdk_feat.geometry()
        
        future_pdk_ids = [ft.id() for ft in self.pdk_lyr.getFeatures() if ft['Timeframe'] == 'Future' and (ft.geometry().intersection(current_pdk_geom).area()>1)]
        # print(future_pdk_ids)
        if not future_pdk_ids:
            future_pdk_ids = [ft.id() for ft in current_pdk_feats]
        future_pdk_lyr = self.pdk_lyr.materialize(QgsFeatureRequest(future_pdk_ids))
        if future_pdk_lyr.isValid():
            future_pdk_lyr.setRenderer(self.paddockRenderer())
            future_pdk_lyr.setLabeling(self.paddockLabels())
            future_pdk_lyr.setLabelsEnabled(True)
            map_layers.append(future_pdk_lyr)
        else:
            invalid_layer_names.append(future_pdk_lyr.name())
            
        future_pdk_names = [ft['Name'] for ft in future_pdk_lyr.getFeatures()]
        future_wa_feats = [ft for ft in self.wa_lyr.getFeatures() if ft['Paddock Name'] in future_pdk_names and ft['Timeframe'] == 'Future']
        if future_wa_feats:
            future_wa_lyr = self.wa_lyr.materialize(QgsFeatureRequest([f.id() for f in future_wa_feats]))
            if future_wa_lyr.isValid():
                renderer = self.wa_lyr.renderer().clone()
                renderer.setClassAttribute('Watered')
                future_wa_lyr.setRenderer(renderer)
                future_wa_lyr.triggerRepaint()
                map_layers.append(future_wa_lyr)
            else:
                invalid_layer_names.append(future_wa_lyr.name())
        future_pipeline_feats = [ft for ft in self.pipe_lyr.getFeatures() if ft['Status'] in ['Planned', 'Built'] and ft.geometry().intersects(current_pdk_geom)]
        if future_pipeline_feats:
            future_pipeline_lyr = self.pipe_lyr.materialize(QgsFeatureRequest([f.id() for f in future_pipeline_feats]))
            if future_pipeline_lyr.isValid():
                future_pipeline_lyr.setRenderer(self.pipelineRenderer())
                map_layers.append(future_pipeline_lyr)
            else:
                invalid_layer_names.append(self.pipe_lyr.name())
        future_wpt_feats = [ft for ft in self.wpt_lyr.getFeatures() if ft['Status'] in ['Planned', 'Built'] and ft.geometry().intersects(current_pdk_geom)]
        if future_wpt_feats:
            future_wpt_lyr = self.wpt_lyr.materialize(QgsFeatureRequest([f.id() for f in future_wpt_feats]))
            if future_wpt_lyr.isValid():
                future_wpt_lyr.setRenderer(self.waterpointRenderer())
                map_layers.append(future_wpt_lyr)
            else:
                invalid_layer_names.append(future_wpt_lyr.name())
        return map_layers

    def paddockDetails(self, paddock_name, timeframe):
        pdks = [ft for ft in self.pdk_lyr.getFeatures() if ft['Name'] == paddock_name and ft['Timeframe'] == timeframe]
        if pdks:
            pdk = pdks[0]
            pdk_geom = pdk.geometry()
            pdk_area = pdk_geom.area()
            cc = pdk['AE']
            if timeframe == 'Current':
                num_wpts = self.currentNumWaterPoints(pdk_geom)
                wa_3km = self.currentWateredArea(pdk_geom, 3000)
                wa_5km = self.currentWateredArea(pdk_geom, 5000)
            elif timeframe == 'Future':
                num_wpts = self.futureNumWaterPoints(pdk_geom)
                wa_3km = self.plannedWateredArea(pdk_geom, 3000)
                wa_5km = self.plannedWateredArea(pdk_geom, 5000) 
            wa_3km_pcnt = (wa_3km/pdk_area)*100
            wa_5km_pcnt = (wa_5km/pdk_area)*100
            fence_length = pdk_geom.length()
            planned_fencing = self.paddockPlannedFence(pdk_geom)
            current_pipeline = self.paddockCurrentPipe(pdk_geom)
            planned_pipeline = self.paddockPlannedPipe(pdk_geom)

            return [pdk_area,
                    cc,
                    num_wpts,
                    wa_3km,
                    wa_3km_pcnt,
                    wa_5km,
                    wa_5km_pcnt,
                    fence_length,
                    planned_fencing,
                    current_pipeline,
                    planned_pipeline]

        return None

    def currentWateredArea(self, pdk_geom, buff_dist):
        pdk_wpt_buffers = [w.geometry().buffer(buff_dist, 25) for w in self.wpt_lyr.getFeatures() if w['Status'] == 'Built' and w.geometry().intersects(pdk_geom)]
        dissolved_wa = QgsGeometry.unaryUnion(pdk_wpt_buffers)
        wa_geom = dissolved_wa.intersection(pdk_geom)
        return wa_geom.area()
        
    def plannedWateredArea(self, pdk_geom, buff_dist):
        pdk_wpt_buffers = [w.geometry().buffer(buff_dist, 25) for w in self.wpt_lyr.getFeatures() if (w['Status'] == 'Built' or w['Status'] == 'Planned')and w.geometry().intersects(pdk_geom)]
        dissolved_wa = QgsGeometry.unaryUnion(pdk_wpt_buffers)
        wa_geom = dissolved_wa.intersection(pdk_geom)
        return wa_geom.area()
        
    def paddockPlannedFence(self, pdk_geom):
        planned_fences = [f for f in self.fence_lyr.getFeatures() if f['Status'] == 'Planned']
        intersecting_fence = [f.geometry().intersection(pdk_geom) for f in planned_fences]
        total_required_fencing = sum(i.length() for i in intersecting_fence)
        # Return planned fence length in meters
        return total_required_fencing
    
    def paddockCurrentPipe(self, pdk_geom):
        current_pipe = [f for f in self.pipe_lyr.getFeatures() if f['Status'] == 'Built']
        intersecting_pipe = [f.geometry().intersection(pdk_geom) for f in current_pipe]
        total_current_pipe = sum(i.length() for i in intersecting_pipe)
        # Return current pipe length in meters
        return total_current_pipe
    
    def paddockPlannedPipe(self, pdk_geom):
        planned_pipe = [f for f in self.pipe_lyr.getFeatures() if f['Status'] == 'Planned']
        intersecting_pipe = [f.geometry().intersection(pdk_geom) for f in planned_pipe]
        total_planned_pipe = sum(i.length() for i in intersecting_pipe)
        # Return planned pipe length in meters
        return total_planned_pipe
        
    def currentNumWaterPoints(self, pdk_geom):
        return len([w for w in self.wpt_lyr.getFeatures() if w['Status'] == 'Built' and w.geometry().intersects(pdk_geom)])
        
    def futureNumWaterPoints(self, pdk_geom):
        return len([w for w in self.wpt_lyr.getFeatures() if (w['Status'] == 'Built' or w['Status'] == 'Planned') and w.geometry().intersects(pdk_geom)])
    
    def sign(self, num1, num2):
        diff = num2-num1
        if diff <= 0:
            return ''
        if diff > 0:
            return '+'