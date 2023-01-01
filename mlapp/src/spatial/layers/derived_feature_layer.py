# -*- coding: utf-8 -*-
from urllib.parse import quote

from qgis.core import QgsProject

from .condition_table import ConditionTable
from .feature_layer import FeatureLayer
from .persisted_feature_layer import PersistedFeatureLayer


class DerivedFeatureLayer(FeatureLayer):

    def __init__(self, project, layerName, queryFormatSpec, styleName=None, *featureLayers):
        # We don't need a layer clause for any DerivedFeatureLayers

        self._featureLayers = list(featureLayers)
        self._queryFormatSpec = queryFormatSpec

        init = self._makeDerivedFeatureLayerSource()

        super().__init__(project, init, layerName, "virtual", styleName=styleName)

        # Apply editor widgets and other Field-specific layer setup
        for field in self.getFeatureType().getSchema():
            field.setupLayer(self)

        self.detectAndRemove()
        QgsProject.instance().addMapLayer(self, False)

    @property
    def featureLayers(self):
        """Return the feature layers that are used to derive this layer."""
        return self._featureLayers

    @property
    def persistedFeatureLayers(self):
        """Return the instances of Paddock Power PersistedFeatureLayers used to derive this layer."""
        return [f for f in self.featureLayers if isinstance(f, PersistedFeatureLayer) or isinstance(f, ConditionTable)]

    @property
    def nonDerivedFeatureLayers(self):
        """Return the feature layers that are used to derive this layer."""
        return [f for f in self.featureLayers if not isinstance(f, DerivedFeatureLayer)]

    def detectAndRemove(self):
        """Detect if a DerivedFeatureLayer is already in the map, and if so, remove it."""
        layers = [l for l in QgsProject.instance().mapLayers().values()]
        for layer in layers:
            if layer.name() == self.name() and layer.providerType() == "virtual":
                QgsProject.instance().removeMapLayer(layer.id())

    def _makeNonDerivedFeatureLayerParameter(self, featureLayer):
        """Make a layer clause for a feature layer."""
        return "layer=" + ":".join([
            "ogr",
            quote(featureLayer._gpkgUrl),
            quote(featureLayer.name()),
            "UTF-8"
        ])

    def _makeAllLayerParameters(self):
        """Make layer clauses for all feature layers."""
        return [self._makeNonDerivedFeatureLayerParameter(f) for f in self.nonDerivedFeatureLayers]

    def _makeQueryParameter(self):
        """Make the query parameter for a feature layer."""
        return self._queryFormatSpec.format(*(layer.name() for layer in self.featureLayers))

    def _makeDerivedFeatureLayerSource(self):
        """Make the overall initialisation string for a DerivedFeatureLayer."""
        return f"?{'&'.join(self._makeAllLayerParameters())}&query={quote(self._makeQueryParameter())}"
