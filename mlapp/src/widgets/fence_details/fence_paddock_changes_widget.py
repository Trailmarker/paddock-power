# # -*- coding: utf-8 -*-
# from ast import If
# import os

# from qgis.PyQt import uic
# from qgis.PyQt.QtCore import pyqtSignal
# from qgis.PyQt.QtGui import QIcon
# from qgis.PyQt.QtWidgets import QWidget

# from ...views.paddock_view.paddock_table_model import PaddockTableModel
# from ...utils import guiConfirm, qgsDebug

# FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
#     os.path.dirname(__file__), 'infrastructure_existing_new_paddocks_base.ui')))


# class FencePaddockChangesWidget(QWidget, FORM_CLASS):

#     closingPlugin = pyqtSignal()
#     refreshUiNeeded = pyqtSignal()

#     def __init__(self, paddockLayer, fence, parent=None):
#         """Constructor."""
#         super(QWidget, self).__init__(parent)

#         self.setupUi(self)

#         self.refreshUiNeeded.connect(self.render)
        
#         self.paddockLayer = paddockLayer

#         self.render()

#     def refreshUi(self):
#         """Show the Paddock View."""

#         if not self.existingPaddocks:
#             self.existingPaddocksTableView.setModel(PaddockTableModel(None))
#         else:
#             self.existingPaddocksTableView.setModel(PaddockTableModel(self.paddockLayer, self.existingPaddocks))

#         if not self.newPaddocks:
#            self.newPaddocksTableView.setModel(PaddockTableModel(None))
#         else:
#             self.newPaddocksTableView.setModel(PaddockTableModel(self.paddockLayer, self.newPaddocks))

#     def setFeatures(self, existingFeatures, newFeatures):
#         self.existingPaddocks = existingFeatures
#         self.newPaddocks = newFeatures
#         self.refreshUiNeeded.emit()

