# -*- coding: utf-8 -*-
from urllib.parse import quote

from qgis.core import QgsFeatureRequest

from ..utils import qgsDebug, qgsError
from .features.edits import Edits
from .feature_layer import FeatureLayer
from .interfaces import IDerivedFeatureLayer, IPersistedLayer


class DerivedFeatureLayer(FeatureLayer, IDerivedFeatureLayer):

    @classmethod
    def keyClause(cls, edits, layer, fieldName):
        fids = edits.layerFids(layer)
        return (f'"{fieldName}" in ({",".join([str(fid) for fid in fids])})' if fids else "")

    @classmethod
    def allKeyClauses(cls, edits, *args):
        keyClauses = [cls.keyClause(edits, layer, fieldName) for (layer, fieldName) in zip(*([iter(args)] * 2))]
        keyClauses = [clause for clause in keyClauses if clause]
        if not keyClauses:
            return ""
        return " or ".join(keyClauses)

    @classmethod
    def andAllKeyClauses(cls, edits, *args):
        allKeyClauses = cls.allKeyClauses(edits, *args)
        return f"and ({allKeyClauses})" if allKeyClauses else ""

    @classmethod
    def prepareRederiveFeaturesRequest(cls, edits, *args):
        """Return a QgsFeatureRequest to figure out which featurs to rederive based on some edits."""
        orClauses = cls.allKeyClauses(edits, *args)
        qgsDebug(f"DerivedFeatureLayer.getRederiveFeaturesRequest({edits}, {args}): orClauses: {orClauses}")

        return QgsFeatureRequest().setFilterExpression(orClauses)
        # return QgsFeatureRequest().setNoAttributes().setFlags(
        #     QgsFeatureRequest.NoGeometry).setFilterExpression(orClauses)


    def getRederiveFeaturesRequest(self, edits):
        """Given a layer, remove the features within it that depend on some edits."""
        return None

    def __init__(self, layerName, styleName, dependentLayers, edits=None):

        self.dependentLayers = dependentLayers
        self.edits = edits or Edits()
        virtualSource = self._makeDerivedFeatureLayerSource(dependentLayers)

        super().__init__(virtualSource, layerName, "virtual", styleName)

        if not self.isValid():
            # No exception raised here because it will interrupt lots of other things
            qgsError(f"{self}.__init__(…): not self.isValid(), check the layer source: {virtualSource}")
            self.setName(f"Invalid {self.name()}!")
            self.addToMap()

        # Apply editor widgets and other Field-specific layer setup
        # for field in self.getSchema():
        #     field.setupLayer(self)

    @property
    def persistedLayers(self):
        """Return the instances of Paddock Power PersistedLayers used to derive this layer."""
        return [f for f in self.dependentLayers if isinstance(f, IPersistedLayer)]

    def names(self, dependentLayers):
        """Get a batch of dependent layer names."""
        return [layer.name() for layer in dependentLayers]

    def prepareQuery(self, query, dependentLayers):
        """Make the query parameter for a feature layer."""
        if not query:
            return None
        else:
            return query.format(*self.names(dependentLayers))

    def _makeNonDerivedFeatureLayerParameter(self, featureLayer):
        """Make a layer clause for a feature layer."""
        return "layer=" + ":".join([
            "ogr",
            quote(featureLayer.gpkgUrl),
            quote(featureLayer.name()),
            "UTF-8"
        ])

    def _makeAllLayerParameters(self, dependentLayers):
        """Make layer clauses for all underlying feature layers that aren't derived."""
        nonDerivedFeatureLayers = [l for l in dependentLayers if not isinstance(l, DerivedFeatureLayer)]
        return [self._makeNonDerivedFeatureLayerParameter(l) for l in nonDerivedFeatureLayers]

    def _makeDerivedFeatureLayerSource(self, dependentLayers):
        """Make the overall initialisation string for a DerivedFeatureLayer."""
        return f"?{'&'.join(self._makeAllLayerParameters(dependentLayers))}&query={quote(self.prepareQuery(None, dependentLayers))}"
