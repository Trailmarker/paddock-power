# -*- coding: utf-8 -*-
from abc import abstractmethod

from .layer import Layer


class PersistedLayer(Layer):

    @abstractmethod
    def readOnly(self):
        """Return True if this layer is read-only, False otherwise."""
        pass

    @abstractmethod
    def setReadOnly(self, readOnly):
        """Set this layer to read-only or not."""
        pass

    @abstractmethod
    def isEditable(self):
        """Return True if this layer is currently editable, False otherwise."""
        pass

    @abstractmethod
    def startEditing(self):
        """Start an edit session on this layer."""
        pass

    @abstractmethod
    def commitChanges(self):
        """Commit changes to this layer."""
        pass

    @abstractmethod
    def rollBack(self):
        """Roll back changes to this layer."""
        pass

    @abstractmethod
    def copyFeature(self, feature):
        """Copy a feature using the logic (eg dependent layers) of this layer."""
        pass

    @abstractmethod
    def makeFeature(self):
        """Make a new, empty and default-valued feature in this layer."""
        pass

    @abstractmethod
    def addFeature(self, feature):
        """Add a feature to this layer."""
        pass

    @abstractmethod
    def updateFeature(self, feature):
        """Update a feature in this layer."""
        pass

    @abstractmethod
    def deleteFeature(self, feature):
        """Delete a feature from the layer."""
        pass

    @abstractmethod
    def addFeatures(self, features):
        """Add a batch of features to this layer."""
        pass

    @abstractmethod
    def recalculateFeatures(self, raiseErrorIfTaskHasBeenCancelled=lambda: None):
        """Recalculate features in this layer."""
        pass
