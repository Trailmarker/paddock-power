# -*- coding: utf-8 -*-
from qgis.core import QgsMapLayer, QgsProject


from ....utils import resolveStylePath
from .abstract_layer_mixin import AbstractLayerMixin

class LayerMixin(AbstractLayerMixin):
    @classmethod
    def detectAndRemoveAllOfType(cls):
        """Detect if any layers of the same type are already in the map, and if so, remove them. Use with care."""
        layers = [l for l in QgsProject.instance().mapLayers().values() if type(l).__name__ == cls.__name__]
        for layer in layers:
            QgsProject.instance().removeMapLayer(layer.id())

    def __init__(self):
        super().__init__()
        
        assert isinstance(self, QgsMapLayer)

    def findGroup(self, name=None):
        """Find the group for this layer in the layer stack."""
        return QgsProject.instance().layerTreeRoot().findGroup(name) if name else None

    def findItem(self):
        """Find the item for this layer in the layer stack."""
        return QgsProject.instance().layerTreeRoot().findLayer(self)
            
    def addInBackground(self):
        """Add this layer to the map in the background."""
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
        self.triggerRepaint()

