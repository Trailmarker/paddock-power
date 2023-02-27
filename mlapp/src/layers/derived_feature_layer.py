# -*- coding: utf-8 -*-
from urllib.parse import quote

from qgis.core import QgsFeatureRequest

from ..utils import qgsDebug, qgsError
from .features import Edits
from .feature_layer import FeatureLayer
from .interfaces import IDerivedFeatureLayer, IPersistedLayer


class DerivedFeatureLayer(FeatureLayer, IDerivedFeatureLayer):

    def keyClause(self, changeset, dependentLayer, derivedKeyFieldName, dependentKeyFieldName):
        keyValues = changeset.layerKeyValues(dependentLayer, dependentKeyFieldName)
        return (f'{derivedKeyFieldName} in ({",".join([str(fid) for fid in keyValues])})' if keyValues else "")

    def allKeyClauses(self, changeset, *args):
        keyClauses = [self.keyClause(changeset, layer, derivedKeyFieldName, dependentKeyFieldName)
                      for (layer, derivedKeyFieldName, dependentKeyFieldName) in zip(*([iter(args)] * 3))]
        keyClauses = [clause for clause in keyClauses if clause]
        if not keyClauses:
            return ""
        return " or ".join(keyClauses)

    def andAllKeyClauses(self, changeset, *args):
        allKeyClauses = self.allKeyClauses(changeset, *args)
        return f"and ({allKeyClauses})" if allKeyClauses else ""

    def prepareRederiveFeaturesRequest(self, *args):
        """Return a QgsFeatureRequest to figure out which featurs to rederive based on some edits."""
        if not self.changeset:
            return None

        orClauses = self.allKeyClauses(self.changeset, *args)
        return QgsFeatureRequest().setFilterExpression(orClauses) if orClauses else None

        # return QgsFeatureRequest().setNoAttributes().setFlags(
        #     QgsFeatureRequest.NoGeometry).setFilterExpression(orClauses)

    def getRederiveFeaturesRequest(self):
        """Given a layer, remove the features within it that depend on some edits."""
        return None

    def __init__(self, layerName, styleName, dependentLayers, changeset=None):

        self.dependentLayers = dependentLayers
        self.changeset = changeset or Edits()
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
