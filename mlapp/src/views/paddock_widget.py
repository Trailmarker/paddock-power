# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import QVBoxLayout, QWidget

from ..models.workspace_mixin import WorkspaceMixin
#from .feature_attribute_table_view import FeatureAttributeTableView
from .feature_list_view import FeatureListView
class PaddockWidget(QWidget, WorkspaceMixin):

    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)

        # self.paddockView = FeatureAttributeTableView(self)
       
        self.paddockView = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.plugin.workspaceReady.connect(self.onWorkspaceReady)
        
        
    def onWorkspaceReady(self):
        if not self.paddockView:
            self.paddockView = FeatureListView(self.workspace.paddockLayer, self)
            self.layout.addWidget(self.paddockView)
        

     