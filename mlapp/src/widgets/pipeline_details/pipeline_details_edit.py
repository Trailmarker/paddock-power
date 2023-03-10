# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from ...layers.features import Edits
from ...models import WorkspaceMixin

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'pipeline_details_edit_base.ui')))


class PipelineDetailsEdit(QWidget, FORM_CLASS, WorkspaceMixin):

    def __init__(self, pipeline, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)

        self.pipeline = pipeline
        if self.pipeline:
            self.nameLineEdit.setText(self.pipeline.NAME)

    def saveFeature(self):
        """Save the Paddock Details."""
        self.pipeline.NAME = self.nameLineEdit.text()
        return Edits.upsert(self.pipeline)
