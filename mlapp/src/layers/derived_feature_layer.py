# -*- coding: utf-8 -*-
from urllib.parse import quote

from .feature_layer import FeatureLayer
from .interfaces import IDerivedFeatureLayer, IPersistedLayer


class DerivedFeatureLayer(FeatureLayer, IDerivedFeatureLayer):

    def __init__(self, layerName, styleName, *dependentLayers):

        self.dependentLayers = dependentLayers
        virtualSource = self._makeDerivedFeatureLayerSource(*dependentLayers)

        super().__init__(virtualSource, layerName, "virtual", styleName)

        # Apply editor widgets and other Field-specific layer setup
        for field in self.getSchema():
            field.setupLayer(self)

    @property
    def persistedLayers(self):
        """Return the instances of Paddock Power PersistedLayers used to derive this layer."""
        return [f for f in self.dependentLayers if isinstance(f, IPersistedLayer)]

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
