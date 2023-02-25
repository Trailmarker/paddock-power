# -*- coding: utf-8 -*-
from qgis.gui import QgsFeatureListViewDelegate


class FeatureItemDelegate(QgsFeatureListViewDelegate):

    def __init__(self, editWidgetFactory, parent=None):
        """Constructor."""
        QgsFeatureListViewDelegate.__init__(self, parent)

        self._editWidgetFactory = editWidgetFactory

    def createEditor(self, parent, option, index):
        return self._editWidgetFactory()
