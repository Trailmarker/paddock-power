# -*- coding: utf-8 -*-
from urllib.parse import quote

from qgis.core import QgsProject, QgsVectorLayer

from ...models.glitch import Glitch
from ...utils import resolveStylePath


class DerivedLayer(QgsVectorLayer):

    def __init__(self, layerName, featureLayer, query, styleName=None):
        layerClause = ":".join([
            "ogr",
            quote(featureLayer._gpkgUrl),
            quote(featureLayer.name()),
            "UTF-8"
        ])

        queryClause = query.format(layer=featureLayer.name())

        init = f"?layer={layerClause}&query={quote(queryClause)}"

        super().__init__(init, layerName, "virtual")

        # Optionally apply a style to the layer
        if styleName is not None:
            stylePath = resolveStylePath(styleName)
            self.loadNamedStyle(stylePath)

        self.detectAndRemove()
        QgsProject.instance().addMapLayer(self, False)

    def detectAndRemove(self):
        """Detect if a layer is already in the map, and if so, return it."""

        layers = [l for l in QgsProject.instance().mapLayers().values()]
        for layer in layers:
            if layer.source() == self.source():
                QgsProject.instance().removeMapLayer(layer.id())

    def addToMap(self, group):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        if group is None:
            raise Glitch(
                "DerivedLayer.addToMap: the layer group is not present")

        group.addLayer(self)
