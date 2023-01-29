# -*- coding: utf-8 -*-
from qgis.core import QgsMapLayer

from ..condition_table import ConditionTable

class AbstractLayerMixin:
    @classmethod
    def detectAndRemoveAllOfType(cls):
        """Detect if any layers of the same type are already in the map, and if so, remove them. Use with care."""
        pass
    
    def __init__(self):
        super().__init__()
        
        assert isinstance(self, QgsMapLayer) or isinstance(self, ConditionTable)

    def findGroup(self, name=None):
        """Find the group for this layer in the map."""
        return None

    def addInBackground(self):
        """Add this layer to the map in the background."""
        pass
    
    def addToMap(self, group=None):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        pass

    def removeFromMap(self, group):
        """Remove the layer from the map in the target group, if it is there."""
        pass

    def setVisible(self, group, visible):
        """Set the layer's visibility."""
        pass
    
    def applyNamedStyle(self, styleName):
        """Apply a style to the layer."""
        pass