# -*- coding: utf-8 -*-
import base64
import os

from qgis.PyQt.QtCore import (Qt, QSize, QByteArray, QBuffer, QIODevice, QTimer,
                                pyqtSignal)
from qgis.PyQt.QtWidgets import (qApp, QDialog, QFileDialog, QMessageBox, QStyle, QLabel,
                                 QComboBox, QLineEdit, QRadioButton, QPushButton,
                                 QGridLayout, QVBoxLayout, QHBoxLayout)
from qgis.PyQt.QtGui import QIcon, QColor, QPageLayout, QPageSize, QImage
from qgis.PyQt.QtPrintSupport import QPrintPreviewDialog, QPrinter
from qgis.PyQt.QtWebKitWidgets import QWebView

from qgis.core import (Qgis, QgsMapSettings, QgsMapRendererParallelJob, QgsRasterLayer,
                        QgsCoordinateReferenceSystem, QgsTask, QgsApplication)

from .report_utils import ReportUtils


class PdfReportDialog(QDialog):
    def __init__(self):
        super(PdfReportDialog, self).__init__()

        self.utils = ReportUtils()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        self.setWindowTitle('Paddock Development Report')
        self.setMinimumWidth(1100)
        self.setMinimumHeight(800)
        self.setGeometry(QStyle.alignedRect(
            Qt.LeftToRight,
            Qt.AlignCenter,
            self.size(),
            qApp.desktop().availableGeometry()))

        self.paddocksLabel = QLabel('Developed Paddocks:', self)
        self.paddocksComboBox = QComboBox(self)
        self.titleLabel = QLabel('Development Title:', self)
        self.titleEdit = QLineEdit('Proposed Development Option', self)
        self.reportOptionLabel = QLabel('Report Template:', self)
        self.basicReportRadioButton = QRadioButton('Basic Report', self)
        self.basicReportRadioButton.setChecked(True)
        self.advancedReportRadioButton = QRadioButton('Advanced Report', self)
        self.advancedReportRadioButton.toggled.connect(self.radioButtonToggled)
        self.basemapLabel = QLabel('Basemap:')
        self.basemapComboBox = QComboBox(self)
        self.basemapComboBox.setMinimumWidth(200)
        self.basemapComboBox.addItems(['Bing Virtual Earth', 'Esri Satellite', 'Google Satellite', 'Esri Topo World', 'No Basemap'])
        self.basemapComboBox.setEnabled(False)
        self.previewButton = QPushButton('Preview', self)
        self.previewButton.setToolTip('Show Selected Report Preview')

        self.populateComboBox()

        self.previewButton.clicked.connect(self.setStandbyHtml)
        self.widget_layout = QGridLayout()
        self.widget_layout.addWidget(self.paddocksLabel, 0, 0, 1, 1)
        self.widget_layout.addWidget(self.paddocksComboBox, 0, 1, 1, 4)
        self.widget_layout.addWidget(self.titleLabel, 1, 0, 1, 1)
        self.widget_layout.addWidget(self.titleEdit, 1, 1, 1, 4)
        self.control_layout = QHBoxLayout()
        self.control_layout.addWidget(self.reportOptionLabel)
        self.control_layout.addWidget(self.basicReportRadioButton)
        self.control_layout.addWidget(self.advancedReportRadioButton)
        self.control_layout.addWidget(self.basemapLabel, alignment=Qt.AlignRight)
        self.control_layout.addWidget(self.basemapComboBox, alignment=Qt.AlignLeft)
        self.control_layout.addWidget(self.previewButton)
        self.view = QWebView(self)
        self.master_layout = QVBoxLayout(self)
        self.master_layout.addLayout(self.widget_layout)
        self.master_layout.addLayout(self.control_layout)
        self.master_layout.addWidget(self.view)
        self.export_button = QPushButton(QIcon(":images/themes/default/mActionSaveAsPDF.svg"), '', self)
        self.export_button.setFixedSize(QSize(50, 50))
        self.export_button.setIconSize(QSize(45, 45))
        self.export_button.setToolTip('Export Report to PDF')
        self.export_button.clicked.connect(self.exportToPdf)
        self.print_button = QPushButton(QIcon(":images/themes/default/mActionFilePrint.svg"), '', self)
        self.print_button.setFixedSize(QSize(50, 50))
        self.print_button.setIconSize(QSize(45, 45))
        self.print_button.setToolTip('Print Report')

        self.print_button.clicked.connect(self.previewReportPrinter)

        self.button_group_layout = QHBoxLayout(self)
        self.button_group_layout.addStretch()
        self.button_group_layout.addWidget(self.print_button)
        self.button_group_layout.addWidget(self.export_button)
        self.button_group_layout.addStretch()
        self.master_layout.addLayout(self.button_group_layout)
        self.setDefaultHtml()
        self.msgBox = QMessageBox()
        
        self.render_task = None
        

    def populateComboBox(self):
        self.paddocksComboBox.clear()
        developed_paddocks = self.utils.getDevelopedPaddocks()
        if developed_paddocks:
            self.paddocksComboBox.addItems(developed_paddocks)
            if not self.paddocksComboBox.isEnabled():
                self.paddocksComboBox.setEnabled(True)
            self.manageWidgets(True)
        else:
            self.paddocksComboBox.setCurrentText('No Developed Paddocks')
            if self.paddocksComboBox.isEnabled():
                self.paddocksComboBox.setEnabled(False)
            self.manageWidgets(False)
            
    def radioButtonToggled(self, is_checked):
        if is_checked:
            if not self.basemapComboBox.isEnabled():
                self.basemapComboBox.setEnabled(True)
        else:
            if self.basemapComboBox.isEnabled():
                self.basemapComboBox.setEnabled(False)

    def manageWidgets(self, bool_val):
        self.titleEdit.setEnabled(bool_val)
        self.basicReportRadioButton.setEnabled(bool_val)
        self.advancedReportRadioButton.setEnabled(bool_val)
        self.previewButton.setEnabled(bool_val)

    def setDefaultHtml(self):
        html_text = "<html>"
        html_text += "<body>"
        html_text += f"<img src='file:///{self.current_dir}/pdk-img.jpg' alt='Paddock Image' style='width: 100%; opacity: 0.2;'/>"
        html_text += "</body>"
        html_text += "</html>"
        self.view.setHtml(html_text)
        
    def setStandbyHtml(self):
        # Show 'Generating preview...' screen while maps are rendering in background thread.
        # Creating a new preview will cancel the current task and cause it to gracefully fail.
        standby_html = "<html>"
        standby_html += "<body>"
        standby_html += "<h1>"
        standby_html += "Generating preview..."
        standby_html += "</h1>"
        standby_html += "</body>"
        standby_html += "</html>"
        standby_html += "<style>"
        standby_html += "body {display: flex; align-items: center; justify-content: center; font-family: Arial, sans-serif; background-color: #D3D3D3;}"
        standby_html += "</style>"
        self.view.setHtml(standby_html)
        
        QTimer.singleShot(250, self.showPreview)

##### **************METHODS TO GENERATE HTML CONTENT**********************#####

    def basicReportHtml(self, paddock_name, development_name):
        html_text = "<html>"
        html_text += "<body>"
        html_text += "<div id='report-1-heading'>"
        html_text += "<h1>"
        html_text += "Paddock Power Investment Calculator Data"
        html_text += "</h1>"
        html_text += "</div>"
        current_pdk_details = self.utils.paddockDetails(paddock_name, 'Current')
        if not current_pdk_details:
            return None
        html_text += "<div id='info-panel'>"
        html_text += "<div id='current-info'>"
        html_text += "<h2>Current Situation</h2>"
        html_text += "<hr>"
        html_text += f"<h3>{paddock_name}</h3>"
        html_text += f"<p>Total paddock area (km²) = {round(current_pdk_details[0]/1000000, 1)}</p>"
        html_text += f"<p>Recommended carrying capacity (AE/yr) = {round(current_pdk_details[1])}</p>"
        html_text += f"<p>Number of water points = {current_pdk_details[2]}</p>"
        html_text += f"<p>3km Watered Area (km² and %) = {round(current_pdk_details[3]/1000000, 1)} | {round(current_pdk_details[4], 1)}</p>"
        html_text += f"<p>5km Watered Area (km² and %) = {round(current_pdk_details[5]/1000000, 1)} | {round(current_pdk_details[6], 1)}</p>"
        html_text += f"<p>Minimum length of fencing (km) = {round(current_pdk_details[7]/1000, 1)}</p>"
        html_text += "</div>"
        html_text += "<div id='proposed-development-info'>"
        html_text += "<h2>Proposed Development Option</h2>"
        html_text += "<hr>"
        if development_name != "Proposed Development Option":
            html_text += f"<h3>{development_name}</h3>"

        pdks = [ft for ft in self.utils.pdk_lyr.getFeatures() if ft['Name'] == paddock_name]
        if pdks:
            pdk = pdks[0]
            pdk_geom = pdk.geometry()
            planned_pdks = [
                p for p in self.utils.pdk_lyr.getFeatures()
                if p['Status'] == 'Planned' and p.geometry().intersection(pdk_geom).area() > 10]
            if planned_pdks:
                # The original paddock has been split, so we need to return details for each new paddock
                all_3km_watered_areas = []
                all_5km_watered_areas = []
                all_ccs = []  # Not used?
                all_potential_ccs = []  # Not used?
                total_required_fencing = self.utils.paddockPlannedFence(pdk_geom)
                for pp in sorted(planned_pdks, key=lambda x: x['Name']):
                    pp_geom = pp.geometry()
                    pp_name = pp['Name']
                    pp_area = pp.geometry().area()  # m2
                    pp_cc = pp['AE']
                    pp_potential_cc = pp['Potential AE']
                    pp_no_wpts = self.utils.futureNumWaterPoints(pp_geom)
                    pp_3km_watered_area = self.utils.plannedWateredArea(pp_geom, 3000)
                    all_3km_watered_areas.append(pp_3km_watered_area)
                    pp_3km_watered_pcnt = (pp_3km_watered_area / pp_area) * 100
                    pp_5km_watered_area = self.utils.plannedWateredArea(pp_geom, 5000)
                    all_5km_watered_areas.append(pp_5km_watered_area)
                    pp_5km_watered_pcnt = (pp_5km_watered_area / pp_area) * 100
                    html_text += f"<h3>{pp_name} (planned)</h3>"
                    html_text += f"<p>Total paddock area (km²) = {round(pp_area/1000000, 1)}</p>"
                    html_text += f"<p>Recommended carrying capacity (AE/yr) = {round(pp_cc)}</p>"
                    html_text += f"<p>Potential carrying capacity (AE/yr) = {round(pp_potential_cc)}</p>"
                    html_text += f"<p>Number of water points = {pp_no_wpts}</p>"
                    html_text += f"<p>3km Watered Area (km² and %) = {round(pp_3km_watered_area/1000000, 1)} | {round(pp_3km_watered_pcnt, 1)}</p>"
                    html_text += f"<p>5km Watered Area (km² and %) = {round(pp_5km_watered_area/1000000, 1)} | {round(pp_5km_watered_pcnt, 1)}</p></br>"
                html_text += "<h3>Planned paddocks</h3>"
                html_text += "<div id='totals'>"
                html_text += f"<p>Total 3km watered area = {round(sum(all_3km_watered_areas)/1000000, 1)}km²</p>"
                html_text += f"<p>Total 5km watered area = {round(sum(all_5km_watered_areas)/1000000, 1)}km²</p>"
                html_text += f"<p>Additional fencing required = {round(total_required_fencing/1000, 1)}km</p>"
                html_text += "</div>"

            else:
                # Paddock has not been split, so we just get the additional waterpoints, watered area etc.
                future_paddock_details = self.utils.paddockDetails(paddock_name, 'Future')
                if not future_paddock_details:
                    return
                fp_area = future_paddock_details[0]
                future_cc = future_paddock_details[1]
                fp_no_wpts = future_paddock_details[2]
                fp_3km_watered_area = future_paddock_details[3]
                fp_3km_watered_pcnt = future_paddock_details[4]
                fp_5km_watered_area = future_paddock_details[5]
                fp_5km_watered_pcnt = future_paddock_details[6]
                future_fence_length = future_paddock_details[7]
                html_text += f"<h3>{paddock_name} (planned)</h3>"
                html_text += f"<p>Total paddock area (km²) = {round(fp_area/1000000, 1)}</p>"
                html_text += f"<p>Recommended carrying capacity (AE/yr) = {round(future_cc)}</p>"
                html_text += f"<p>Number of water points = {fp_no_wpts}</p>"
                html_text += f"<p>3km Watered Area (km² and %) = {round(fp_3km_watered_area/1000000, 1)} | {round(fp_3km_watered_pcnt, 1)}</p>"
                html_text += f"<p>5km Watered Area (km² and %) = {round(fp_5km_watered_area/1000000, 1)} | {round(fp_5km_watered_pcnt, 1)}</p>"
                html_text += f"<p>Minimum length of fencing (km) = {round(future_fence_length/1000)}</p>"
            html_text += "</div>"
            html_text += "</div>"  # Closing tag for info-panel div
            html_text += "</body>"
            html_text += "</html>"
            html_text += "<style>"
            html_text += "body {font-family: Arial, sans-serif; background-color: #fcf5e1;}"
            html_text += "#info-panel {margin-left: 50px;}"
            html_text += "#report-1-heading {text-align: center; margin-top: 50px; margin-bottom:50px;}"
            html_text += "</style>"
            return html_text
        return None

    def advancedReportTableHtml(self, paddock_name):
        # Current
        current_pdk_details = self.utils.paddockDetails(paddock_name, 'Current')
        current_area = round(current_pdk_details[0] / 1000000, 1)
        current_recommended_cc = round(current_pdk_details[1])
        current_avg_AE = 'TODO'
        current_num_wpts = current_pdk_details[2]
        if current_num_wpts > 0:
            current_avg_AE_per_wpt = round(current_recommended_cc / current_num_wpts)
        else:
            current_avg_AE_per_wpt = 0
        current_wa_3km = round(current_pdk_details[3] / 1000000, 1)
        current_wa_3km_pcnt = round(current_pdk_details[4], 1)
        current_wa_3km_info = f'{current_wa_3km} km² | {current_wa_3km_pcnt}%'
        current_wa_5km = round(current_pdk_details[5] / 1000000, 1)
        current_wa_5km_pcnt = round(current_pdk_details[6], 1)
        current_wa_5km_info = f'{current_wa_5km} km² | {current_wa_5km_pcnt}%'
        current_wa_stocking_rate = 'TODO'
        current_fencing = round(current_pdk_details[7] / 1000, 1)
        current_pipeline = round(current_pdk_details[9] / 1000, 1)

        # Future
        pdks = [ft for ft in self.utils.pdk_lyr.getFeatures() if ft['Name'] == paddock_name]
        if pdks:
            pdk = pdks[0]
            pdk_geom = pdk.geometry()
            planned_pdks = [
                p for p in self.utils.pdk_lyr.getFeatures()
                if p['Status'] == 'Planned' and p.geometry().intersection(pdk_geom).area() > 10]
            if planned_pdks:
                # The original paddock has been split, so we need to sum & return details for each new paddock
                all_areas = []
                all_ccs = []
                all_wpts = []
                all_3km_wa = []
                all_5km_wa = []
                for pp in sorted(planned_pdks, key=lambda x: x['Name']):
                    pp_name = pp['Name']
                    pp_geom = pp.geometry()
                    all_areas.append(pp_geom.area())
                    all_ccs.append(pp['AE'])
                    all_wpts.append(self.utils.futureNumWaterPoints(pp_geom))
                    all_3km_wa.append(self.utils.plannedWateredArea(pp_geom, 3000))
                    all_5km_wa.append(self.utils.plannedWateredArea(pp_geom, 5000))

                future_area = round(sum(all_areas) / 1000000, 1)
                future_recommended_cc = round(sum(all_ccs), 1)
                future_num_wpts = sum(all_wpts)
                future_avg_AE_per_wpt = round(future_recommended_cc / future_num_wpts, 1)
                future_wa_3km = round(sum(all_3km_wa) / 1000000, 1)
                future_wa_3km_pcnt = round((future_wa_3km / future_area) * 100, 1)
                future_wa_3km_info = f'{future_wa_3km} km² | {future_wa_3km_pcnt}%'
                future_wa_5km = round(sum(all_5km_wa) / 1000000, 1)
                future_wa_5km_pcnt = round((future_wa_5km / future_area) * 100, 1)
                future_wa_5km_info = f'{future_wa_5km} km² | {future_wa_5km_pcnt}%'
            else:
                # Paddock has not been split, so we just get the additional waterpoints, watered area etc.
                future_pdk_details = self.utils.paddockDetails(paddock_name, 'Future')
                if not future_pdk_details:
                    return
                future_area = round(future_pdk_details[0] / 1000000, 1)
                future_recommended_cc = round(future_pdk_details[1])
                future_num_wpts = future_pdk_details[2]
                future_avg_AE_per_wpt = round(future_recommended_cc / future_num_wpts)
                future_wa_3km = round(future_pdk_details[3] / 1000000, 1)
                future_wa_3km_pcnt = round(future_pdk_details[4], 1)
                future_wa_3km_info = f'{future_wa_3km} km² | {future_wa_3km_pcnt}%'
                future_wa_5km = round(future_pdk_details[5] / 1000000, 1)
                future_wa_5km_pcnt = round(future_pdk_details[6], 1)
                future_wa_5km_info = f'{future_wa_5km} km² | {future_wa_5km_pcnt}%'
                future_wa_stocking_rate = 'TODO'
            # planned_fencing = round(current_pdk_details[8]/1000, 3)
            total_future_fencing = round((current_pdk_details[7] + current_pdk_details[8]) / 1000, 1)
            planned_fencing = round(total_future_fencing - current_fencing, 1)
            current_pipeline = round(current_pdk_details[9] / 1000, 1)  # Only Built Pipelines
            future_pipeline = round(current_pdk_details[10] / 1000, 1)  # Only Planned Pipelines
            total_future_pipeline = round(current_pipeline + future_pipeline, 1)

        # Differences
        area_diff = round(future_area - current_area, 1)
        area_sign = self.utils.sign(current_area, future_area)
        cc_diff = round(future_recommended_cc - current_recommended_cc)
        cc_sign = self.utils.sign(current_recommended_cc, future_recommended_cc)
        wpt_diff = future_num_wpts - current_num_wpts
        wpt_sign = self.utils.sign(current_num_wpts, future_num_wpts)
        avg_AE_per_wpt_diff = round(future_avg_AE_per_wpt - current_avg_AE_per_wpt)
        avg_AE_per_wpt_sign = self.utils.sign(current_avg_AE_per_wpt, future_avg_AE_per_wpt)
        wa_3km_diff = round(future_wa_3km - current_wa_3km, 1)
        wa_3km_pcnt_diff = round(future_wa_3km_pcnt - current_wa_3km_pcnt, 1)
        wa_3km_diff_info = f'{wa_3km_diff} km² | {wa_3km_pcnt_diff}%'
        wa_3km_sign = self.utils.sign(current_wa_3km, future_wa_3km)
        wa_5km_diff = round(future_wa_5km - current_wa_5km)
        wa_5km_pcnt_diff = round(future_wa_5km_pcnt - current_wa_5km_pcnt, 1)
        wa_5km_diff_info = f'{wa_5km_diff} km² | {wa_5km_pcnt_diff}%'
        wa_5km_sign = self.utils.sign(current_wa_5km, future_wa_5km)

        html_text = "<table>"
        html_text += "<tr><th>Paddock Development Proposal</th><th>Current</th><th>Proposed</th><th>Difference +/-</th></tr>"
        html_text += f"<tr><td>Total paddock area</td><td>{current_area} km²</td><td>{future_area} km²</td><td>{area_sign}{area_diff} km²</td></tr>"
        html_text += f"<tr><td>Recommended carrying capacity</td><td>{current_recommended_cc} AE/yr</td><td>{future_recommended_cc} AE/yr</td><td>{cc_sign}{cc_diff} AE/yr</td></tr>"
        # html_text+=f"<tr><td>Average adult equivalents carried now and planned for proposed development</td><td>{current_avg_AE}</td><td>B</td><td>C</td></tr>"
        html_text += f"<tr><td>Number of water points in paddock</td><td>{current_num_wpts}</td><td>{future_num_wpts}</td><td>{wpt_sign}{wpt_diff}</td></tr>"
        html_text += f"<tr><td>Average number of AE/water point</td><td>{current_avg_AE_per_wpt}</td><td>{future_avg_AE_per_wpt}</td><td>{avg_AE_per_wpt_sign}{avg_AE_per_wpt_diff}</td></tr>"
        html_text += f"<tr><td>3km watered area</td><td>{current_wa_3km_info}</td><td>{future_wa_3km_info}</td><td>{wa_3km_sign}{wa_3km_diff_info}</td></tr>"
        html_text += f"<tr><td>5km watered area</td><td>{current_wa_5km_info}</td><td>{future_wa_5km_info}</td><td>{wa_5km_sign}{wa_5km_diff_info}</td></tr>"
        # html_text+=f"<tr><td>Watered area stocking rate</td><td>{current_wa_stocking_rate} AE/km²</td><td>B</td><td>C</td></tr>"
        html_text += f"<tr><td>Minimum length of fencing (including terrain)</td><td>{current_fencing} km</td><td>{total_future_fencing} km</td><td>{self.utils.sign(current_fencing, total_future_fencing)}{planned_fencing} km</td></tr>"
        html_text += f"<tr><td>Minimum length of pipeline (including terrain)</td><td>{current_pipeline} km</td><td>{total_future_pipeline} km</td><td>{self.utils.sign(current_pipeline, total_future_pipeline)}{future_pipeline} km</td></tr>"
        html_text += "</table>"
        html_text += "</body></html>"
        return html_text

##############################################################################

    def showPreview(self):
        ##### BASIC REPORT TEMPLATE#####
        development_name = self.titleEdit.text()
        paddock_name = self.paddocksComboBox.currentText()
        if self.basicReportRadioButton.isChecked():
            if self.render_task and self.render_task.alive:
                self.render_task.cancel()
            basic_html = self.basicReportHtml(paddock_name, development_name)
            self.view.setHtml(basic_html)
        ##### ADVANCED REPORT TEMPLATE#####
        elif self.advancedReportRadioButton.isChecked():
            basemap = self.basemapComboBox.currentText()
            if basemap == 'No Basemap':
                basemap_lyr = None
            else:
                basemap_lyr = self.utils.basemapLayer(basemap)
            #############################################################
            # Create image tag for current layers
            current_layers = self.utils.currentMapLayers(paddock_name, basemap)
            current_layer_names = [l.name() for l in current_layers]
            current_layers_ordered = []

            if 'Waterpoints' in current_layer_names:
                wpt_lyr_index = current_layer_names.index('Waterpoints')
                current_layers_ordered.append(current_layers[wpt_lyr_index])
            if 'Pipelines' in current_layer_names:
                pipe_lyr_index = current_layer_names.index('Pipelines')
                current_layers_ordered.append(current_layers[pipe_lyr_index])
            if 'Watered Areas' in current_layer_names:
                wa_lyr_index = current_layer_names.index('Watered Areas')
                current_layers_ordered.append(current_layers[wa_lyr_index])
            if 'Paddocks' in current_layer_names:
                pdk_lyr_index = current_layer_names.index('Paddocks')
                if not basemap_lyr:
                    ls_lyr = self.utils.landTypesLayer(current_layers[pdk_lyr_index])
                    if ls_lyr:
                        current_layers_ordered.append(ls_lyr)
                current_layers_ordered.append(current_layers[pdk_lyr_index])
            if basemap_lyr:
                current_layers_ordered.append(basemap_lyr)

            current_extent = current_layers[pdk_lyr_index].extent()
#***************************************************************************
            # Create image tag for future layers
            future_layers = self.utils.futureMapLayers(paddock_name, basemap)
            future_layer_names = [l.name() for l in future_layers]
            future_layers_ordered = []

            if 'Waterpoints' in future_layer_names:
                wpt_lyr_index = future_layer_names.index('Waterpoints')
                future_layers_ordered.append(future_layers[wpt_lyr_index])
            if 'Pipelines' in future_layer_names:
                pipe_lyr_index = future_layer_names.index('Pipelines')
                future_layers_ordered.append(future_layers[pipe_lyr_index])
            if 'Watered Areas' in future_layer_names:
                wa_lyr_index = future_layer_names.index('Watered Areas')
                future_layers_ordered.append(future_layers[wa_lyr_index])
            if 'Paddocks' in future_layer_names:
                pdk_lyr_index = future_layer_names.index('Paddocks')
                if not basemap_lyr:
                    ls_lyr = self.utils.landTypesLayer(future_layers[pdk_lyr_index])
                    if ls_lyr:
                        future_layers_ordered.append(ls_lyr)
                future_layers_ordered.append(future_layers[pdk_lyr_index])
            if basemap_lyr:
                future_layers_ordered.append(basemap_lyr)
            future_extent = future_layers[pdk_lyr_index].extent()
#*****************************************
            ########SET UP TASK TO CREATE RENDERED CANVAS IMAGES##########>>>
            if basemap == 'No Basemap':
                task_desc = 'Rendering maps without basemap...'
            else:
                task_desc = f'Rendering maps with {basemap} basemap'
            if self.render_task and self.render_task.alive:
                self.render_task.cancel()
            self.render_task = RenderTask(task_desc,
                                current_layers_ordered,
                                current_extent,
                                future_layers_ordered,
                                future_extent)
            self.render_task.map_images.connect(lambda images: self.setAdvancedHtml(images, paddock_name, basemap))
            self.render_task.taskCompleted.connect(self.resetTask)
            self.render_task.taskTerminated.connect(self.resetTask)
            QgsApplication.taskManager().addTask(self.render_task)

    def resetTask(self):
        self.render_task = None
        
    def setAdvancedHtml(self, map_images, paddock_name, basemap=None):
        advanced_html = "<html>"
        advanced_html += "<body>"
        advanced_html += "<h1>"
        advanced_html += "Paddock Power Investment Calculator Data"
        advanced_html += "</h1><br>"
        advanced_html += self.advancedReportTableHtml(paddock_name)

        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        map_images[0].save(buffer, "PNG")
        img_tag1 = "<img src='data:image/png;base64,{}' width='420' height='420'>".format(base64.b64encode(
            byte_array).decode())
            
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        map_images[1].save(buffer, "PNG")
        img_tag2 = "<img src='data:image/png;base64,{}' width='420' height='420'>".format(base64.b64encode(
            byte_array).decode())
            
        advanced_html += "<div id='image-div'>"
        advanced_html += "<div id='current-map-img'>"
        advanced_html += "<h3>Current</h3>"
        advanced_html += img_tag1
        advanced_html += "</div>"  # Closing tag for current-map-img div
        advanced_html += "<div id='planned-map-img'>"
        advanced_html += "<h3>Planned</h3>"
        advanced_html += img_tag2
        advanced_html += "</div>"  # Closing tag for planned-map-img div
        advanced_html += "</div>"  # Closing tag for image-div
        if basemap and basemap != 'No Basemap':
            attribution_txt = self.utils.basemapAttribution(basemap)
            advanced_html += f"<p id=attribution-txt>{attribution_txt}</p>"
            advanced_html += f"<img src='file:///{self.current_dir}/legend-img-basemap.png' alt='Legend' width='750'/>"
        else:
            advanced_html += f"<img src='file:///{self.current_dir}/legend-img-no-basemap.png' alt='Legend' width='750'/>"
        advanced_html += "</body>"
        advanced_html += "</html>"
        advanced_html += "<style>"
        advanced_html += "h1, h3 {font-family: Arial, sans-serif;}"
        advanced_html += "img {border: 3px solid #555; margin: 5px;}"
        advanced_html += "table, th, tr, td"
        advanced_html += "{border: 1px solid black;"
        advanced_html += "border-collapse: collapse;"
        advanced_html += "padding: 5px; font-family: Arial, sans-serif;}"
        advanced_html += "th {background-color: #bfd9c4;}"
        advanced_html += "td {background-color: #ffffff;}"
        advanced_html += "table {margin-left: auto; margin-right: auto; margin-bottom: 50px;}"
        advanced_html += "body {padding-top: 50; background-color: #fcf5e1; text-align: center;}"
        advanced_html += "#image-div {display: flex; justify-content: center;}"
        advanced_html += "#attribution-txt {font-family: Arial, sans-serif; font-size: 12}"
        advanced_html += "</style>"
        self.view.setHtml(advanced_html)
        
########################################################################################

    def exportToPdf(self):
        save_file_name = QFileDialog.getSaveFileName(
            self, 'Save to PDF', 'Paddock Power Report.pdf', 'PDF File (*.pdf)')
        if save_file_name[0]:
            pdf_path = save_file_name[0]
            printer = QPrinter()
            page_layout = QPageLayout()
            page_layout.setPageSize(QPageSize(QPageSize.A4))
            page_layout.setOrientation(QPageLayout.Portrait)
            printer.setPageLayout(page_layout)
            printer.setOrientation(QPrinter.Portrait)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(pdf_path)
            self.view.print_(printer)
            self.msgBox.setText(f'PDF exported to: {pdf_path}')
            self.msgBox.exec_()

    def previewReportPrinter(self):
        preview_dialog = QPrintPreviewDialog()
        preview_dialog.paintRequested.connect(self.view.print_)
        preview_dialog.exec_()

###############QGSTASK TO CREATE RENDERED CANVAS IMAGES################################

class RenderTask(QgsTask):
    map_images = pyqtSignal(list)
    
    def __init__(self, desc, current_layers, current_extent, future_layers, future_extent):
        self.desc = desc
        QgsTask.__init__(self, self.desc, QgsTask.CanCancel)
        self.current_layers = current_layers
        self.current_extent = current_extent
        self.future_layers = future_layers
        self.future_extent = future_extent
        self.images = []
        self.utils = ReportUtils()
        # We want to check for network request errors and cancel the task if received
        self.msg_log = QgsApplication.messageLog()
        self.msg_log.messageReceived.connect(self.errorChecker)
        
        self.alive = True
        
        self.taskCompleted.connect(self.killed)
        self.taskTerminated.connect(self.killed)
        
    def killed(self):
        self.alive = False
                
    def run(self):
        # Render Current map image
        longest_dim = max([self.current_extent.width(), self.current_extent.height()])
        grow_factor = longest_dim / 30
        self.current_extent.grow(grow_factor)
        self.current_extent.setYMinimum(self.current_extent.yMinimum() - (longest_dim) / 8)
        scale_bar_lyr = self.utils.scaleBarLayer(self.current_extent)
        self.current_layers.insert(0, scale_bar_lyr)
        settings = QgsMapSettings()
        settings.setDestinationCrs(QgsCoordinateReferenceSystem('EPSG:7845'))
        settings.setOutputDpi(350)
        settings.setLayers(self.current_layers)
        settings.setExtent(self.current_extent)
        settings.setBackgroundColor(QColor(255, 255, 255))
        settings.setOutputSize(QSize(1200, 1200))
        render = QgsMapRendererParallelJob(settings)
        # Start the rendering
        render.start()
        render.waitForFinished()
        current_img = render.renderedImage()
        self.images.append(current_img)
        if self.isCanceled():
            self.alive = False
            return False
            
        # Render Future map image
        longest_dim = max([self.future_extent.width(), self.future_extent.height()])
        grow_factor = longest_dim / 30
        self.future_extent.grow(grow_factor)
        self.future_extent.setYMinimum(self.future_extent.yMinimum() - (longest_dim) / 8)
        scale_bar_lyr = self.utils.scaleBarLayer(self.future_extent)
        self.future_layers.insert(0, scale_bar_lyr)
        settings = QgsMapSettings()
        settings.setDestinationCrs(QgsCoordinateReferenceSystem('EPSG:7845'))
        settings.setOutputDpi(350)
        settings.setLayers(self.future_layers)
        settings.setExtent(self.future_extent)
        settings.setBackgroundColor(QColor(255, 255, 255))
        settings.setOutputSize(QSize(1200, 1200))
        render = QgsMapRendererParallelJob(settings)
        # Start the rendering
        render.start()
        render.waitForFinished()
        future_img = render.renderedImage()
        self.images.append(future_img)
        if self.isCanceled():
            self.alive = False
            return False
        return True
        
    def finished(self, result):
        if result:
            self.map_images.emit(self.images)
        
    def errorChecker(self, msg, tag, level):
        '''Cancel task if network error logged (and task has not already been canceled)
        e.g. by user generating a new preview which cancels the current task'''
        if not self.alive:
            return
        if 'Network request' in msg and tag == 'Network' and level == Qgis.Warning:
            self.cancel()
                    
########################################################################################