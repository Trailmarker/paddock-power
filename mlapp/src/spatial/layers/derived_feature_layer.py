# -*- coding: utf-8 -*-
from urllib.parse import quote

from qgis.PyQt.QtCore import pyqtSlot

from ...utils import qgsDebug
from ..fields.names import FID
from .condition_table import ConditionTable
from .feature_layer import FeatureLayer
from .persisted_feature_layer import PersistedFeatureLayer


class DerivedFeatureLayer(FeatureLayer):

    def __init__(self, featureType, layerName, styleName, *dependentLayers):
        # qgsDebug(f"DerivedFeatureLayer.__init__({featureType}, {layerName}, {styleName}, {dependentLayers})")

        # This ends up getting initialised again in onWorkspaceConnectionChanged at the moment
        self.workspaceLayerentLayers = dependentLayers
        virtualSource = self._makeDerivedFeatureLayerSource(*dependentLayers)

        super().__init__(featureType, virtualSource, layerName, "virtual", styleName)

        # Apply editor widgets and other Field-specific layer setup
        for field in self.getSchema():
            field.setupLayer(self)

    @property
    def persistedDependentLayers(self):
        """Return the instances of Paddock Power PersistedFeatureLayers used to derive this layer."""
        return [f for f in self.workspaceLayerentLayers if isinstance(
            f, PersistedFeatureLayer) or isinstance(f, ConditionTable)]

    def names(self, *dependentLayers):
        """Get a batch of dependent layer names."""
        return [layer.name() for layer in dependentLayers]

    def prepareQuery(self, query, *dependentLayers):
        """Make the query parameter for a feature layer."""
        if not query:
            return None
        else:
            return query.format(*self.names(*dependentLayers))

    def _makeNonDerivedFeatureLayerParameter(self, featureLayer):
        """Make a layer clause for a feature layer."""
        return "layer=" + ":".join([
            "ogr",
            quote(featureLayer.gpkgUrl),
            quote(featureLayer.name()),
            "UTF-8"
        ])

    def _makeAllLayerParameters(self, *dependentLayers):
        """Make layer clauses for all underlying feature layers that aren't derived."""
        nonDerivedFeatureLayers = [l for l in dependentLayers if not isinstance(l, DerivedFeatureLayer)]
        return [self._makeNonDerivedFeatureLayerParameter(l) for l in nonDerivedFeatureLayers]

    def _makeDerivedFeatureLayerSource(self, *dependentLayers):
        """Make the overall initialisation string for a DerivedFeatureLayer."""
        return f"?{'&'.join(self._makeAllLayerParameters(*dependentLayers))}&query={quote(self.prepareQuery(None, *dependentLayers))}"
