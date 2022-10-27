# -*- coding: utf-8 -*-
from urllib.parse import quote

from .feature_layer import FeatureLayer


class DerivedLayer(FeatureLayer):

    @staticmethod
    def formatLayerClause(featureLayer):
        return "layer=" + ":".join([
            "ogr",
            quote(featureLayer._gpkgUrl),
            quote(featureLayer.name()),
            "UTF-8"
        ])

    @staticmethod
    def makeQueryClause(queryFormatSpec, *featureLayers):
        return queryFormatSpec.format(*(layer.name() for layer in featureLayers))

    def __init__(self, layerName, queryFormatSpec, styleName=None, *featureLayers):
        layerClauses = map(DerivedLayer.formatLayerClause, featureLayers)
        queryClause = DerivedLayer.makeQueryClause(queryFormatSpec, *featureLayers)

        init = f"?{'&'.join(layerClauses)}&query={quote(queryClause)}"

        super().__init__(init, layerName, "virtual", styleName=styleName)
