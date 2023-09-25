# -*- coding: utf-8 -*-
from abc import abstractclassmethod, abstractmethod

from .layer import Layer


class MapLayer(Layer):

    @abstractclassmethod
    def defaultName(cls):
        """Return the default name for this layer."""
        pass

    @abstractclassmethod
    def defaultStyle(cls):
        """Return the default style for this layer."""
        pass

    @abstractclassmethod
    def detectAllOfType(cls):
        """Detect if any layers of the same type are already in the map, and if so, remove them. Use with care."""
        pass

    @abstractclassmethod
    def removeAllOfType(cls):
        """Detect if any layers of the same type are already in the map, and if so, remove them. Use with care."""
        pass

    def findItem(self):
        """Find the item for this layer in the layer stack."""
        pass

    @abstractmethod
    def findGroup(self, name=None):
        """Find the group for this layer in the map."""
        pass

    @abstractmethod
    def addInBackground(self):
        """Add this layer to the map in the background."""
        pass

    @abstractmethod
    def addToMap(self, group=None):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        pass

    @abstractmethod
    def removeFromMap(self, group):
        """Remove the layer from the map in the target group, if it is there."""
        pass

    @abstractmethod
    def setVisible(self, group, visible):
        """Set the layer's visibility."""
        pass

    @abstractmethod
    def applyNamedStyle(self, styleName):
        """Apply a style to the layer."""
        pass
