# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class FeatureList(ABC):
    """A generic list of Features."""

    @abstractmethod
    def filterByName(self, filter):
        """Filter the Feature list by name."""
        pass

    @abstractmethod
    def listFeatures(self, request=None):
        """List the Features."""
        pass

    @abstractmethod
    def getFeature(self, fid):
        """Get a Feature by ID."""
        pass

    @abstractmethod
    def clear(self):
        """Clear the list."""
        pass

    @abstractmethod
    def sortFeatures(self, features):
        """Sort the Features."""
        pass

    @abstractmethod
    def deduplicateFeatures(self, features):
        """De-duplicate the Features. May be necessary to provide this for some FeatureLayerList subclasses."""
        pass

    @abstractmethod
    def addListItem(self, feature):
        """Add one item in the list specified a Feature."""
        pass

    @abstractmethod
    def refreshListItem(self, fid):
        """Refresh one item in the list specified by Feature ID."""
        pass

    @abstractmethod
    def refreshList(self):
        """Refresh the whole Feature List."""
        pass

    @abstractmethod
    def removeSelection(self):
        """Clear the selected Feature."""
        pass

    @abstractmethod
    def changeSelection(self, layerType):
        """Select a Feature from the specified layer type."""
        pass
