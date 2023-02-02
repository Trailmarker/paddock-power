# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from ...layers.features import Edits
from ...models import WorkspaceMixin

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'metric_paddock_details_edit_base.ui')))


class MetricPaddockDetailsEdit(QWidget, FORM_CLASS, WorkspaceMixin):

    def __init__(self, metricPaddock, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)

        self.metricPaddock = metricPaddock
        self.paddock = None
        self.getPaddock()

    @property
    def paddockLayer(self):
        """Get the FeatureLayer."""
        return self.workspace.paddockLayer

    def getPaddock(self):
        self.paddock = self.metricPaddock.getPaddock()
        self.nameLineEdit.setText(self.paddock.NAME)

    def saveFeature(self):
        """Save the Paddock Details."""
        self.paddock.NAME = self.nameLineEdit.text()
        return Edits.upsert(self.paddock)
