# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsCategorizedSymbolRenderer

from ...utils import PLUGIN_NAME
from ..schemas.feature_status import FeatureStatus
from .persisted_feature_layer import PersistedFeatureLayer


class StatusFeatureLayer(PersistedFeatureLayer):

    displayFilterChanged = pyqtSignal(list)

    def __init__(self, gpkgFile, layerName, styleName=None):
        f"""Create a new {PLUGIN_NAME} vector layer with status management."""
        super().__init__(gpkgFile=gpkgFile, layerName=layerName, styleName=styleName)
        self._displayFilter = [FeatureStatus.Drafted, FeatureStatus.Built, FeatureStatus.Planned]
        self._applyDisplayFilter(self.displayFilter)
        self.writeCustomSymbology.connect(self._refreshDisplayFilterFromRenderer)

    @property
    def displayFilter(self):
        """The display layer for this layer."""
        return self._displayFilter

    @displayFilter.setter
    def displayFilter(self, filter):
        """Set the display filter for this layer."""
        if self._displayFilter != filter:
            self._displayFilter = filter
            self.displayFilterChanged.emit(self.displayFilter)
            self._applyDisplayFilter(filter)

    def _applyDisplayFilter(self, filter):
        """Toggle the display of a renderer category."""
        renderer = self.renderer()
        if isinstance(renderer, QgsCategorizedSymbolRenderer) and renderer.classAttribute() == 'Status':
            displayed = [status.name for status in filter]
            categories = renderer.categories()
            for category in categories:
                category.setRenderState(category.value() in displayed)
            self.setRenderer(QgsCategorizedSymbolRenderer('Status', categories))
            self.triggerRepaint()

    def _refreshDisplayFilterFromRenderer(self):
        """Refresh the display filter from the renderer."""
        # qgsDebug("FeatureLayer._refreshDisplayFilterFromRenderer")
        renderer = self.renderer()
        if isinstance(renderer, QgsCategorizedSymbolRenderer) and renderer.classAttribute() == 'Status':
            values = [category.value() for category in renderer.categories() if category.renderState()]
            statuses = [status for status in FeatureStatus if status.match(*values)]
            self.displayFilter = statuses

    def getFeaturesByStatus(self, *statuses, request=None):
        """Get the features in this layer filtered by one or more FeatureStatus values."""
        if not statuses:
            return self.getFeatures(request)
        return [f for f in self.getFeatures(request) if f.status.match(*statuses)]
