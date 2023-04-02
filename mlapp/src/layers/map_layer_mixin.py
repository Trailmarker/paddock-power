# -*- coding: utf-8 -*-
from qgis.core import QgsMapLayer, QgsProject

from ..utils import PLUGIN_NAME, qgsInfo, resolveStylePath
from .interfaces import IDerivedFeatureLayer, IMapLayer, IPersistedFeatureLayer


class MapLayerMixin(IMapLayer):

    @classmethod
    def defaultName(cls):
        """Return the default name for this layer."""
        return cls.LAYER_NAME

    @classmethod
    def defaultStyle(cls):
        """Return the default style for this layer."""
        return cls.STYLE

    @classmethod
    def detectAllOfType(cls, workspaceFile=None):
        """Detect if any layers of the same type are already in the map, and if so, remove them. Use with care."""
        allLayers = QgsProject.instance().mapLayers().values()

        # Match by type
        matches = list(set([l.id() for l in allLayers if type(l).__name__ == cls.__name__]))

        # Match by source for persisted layers
        if workspaceFile and issubclass(cls, IPersistedFeatureLayer):
            sameSource = [l.id() for l in allLayers if l.source() == cls.workspaceUrl(workspaceFile)]

            matches = list(set(matches + sameSource))

        # Match by provider and name for derived layers
        if issubclass(cls, IDerivedFeatureLayer):
            sameProviderAndName = [l.id() for l in allLayers if l.providerType() ==
                                   "virtual" and l.name() == cls.defaultName()]

            matches = list(set(matches + sameProviderAndName))

        return matches

    @classmethod
    def removeAllOfType(cls, workspaceFile=None):
        matches = cls.detectAllOfType(workspaceFile)

        for layerId in matches:
            qgsInfo(f"{PLUGIN_NAME} Cleaning up {layerId} …")
            QgsProject.instance().removeMapLayer(layerId)

    def __init__(self):
        super().__init__()
        self._tasks = []
        self._taskIds = []

        assert isinstance(self, QgsMapLayer)

    def findGroup(self, name=None):
        """Find the group for this layer in the layer stack."""
        return QgsProject.instance().layerTreeRoot().findGroup(name) if name else None

    def findItem(self):
        """Find the item for this layer in the layer stack."""
        return QgsProject.instance().layerTreeRoot().findLayer(self)

    def addInBackground(self):
        """Add this layer to the map in the background."""
        qgsInfo(f"Adding layer {self.name()} in background …")
        QgsProject.instance().addMapLayer(self, False)

    def addToMap(self, group=None):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        group = group or self.findGroup() or QgsProject.instance().layerTreeRoot()
        group.addLayer(self)

    def removeFromMap(self, group):
        """Remove the layer from the map in the target group, if it is there."""
        group = group or self.findGroup() or QgsProject.instance().layerTreeRoot()
        node = group.findLayer(self.id())
        if node:
            group.removeChildNode(node)

    def setVisible(self, group, visible):
        """Set the layer's visibility."""
        group = group or self.findGroup() or QgsProject.instance().layerTreeRoot()
        node = group.findLayer(self.id())
        if node:
            node.setItemVisibilityChecked(visible)

    def applyNamedStyle(self, styleName):
        """Apply a style to the layer."""
        # Optionally apply a style to the layer
        if styleName:
            stylePath = resolveStylePath(styleName)
            self.loadNamedStyle(stylePath)
        self.triggerRepaint(True)

    def zoomLayer(self):
        """Zoom to this layer."""
        iface = self.workspace.iface
        canvas = iface.mapCanvas()
        canvas.setExtent(self.extent())
        canvas.refresh()
