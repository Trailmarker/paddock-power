# -*- coding: utf-8 -*-
from abc import ABC, abstractclassmethod, abstractmethod

class Feature(ABC):

    @abstractclassmethod
    def displayName(cls):
        """Return the display name of the Feature."""
        pass

    @abstractclassmethod
    def focusOnSelect(self):
        """Return True if the app should focus on this type of Feature when selected."""
        pass

    @abstractmethod
    def clearFid(self):
        """Nullify the PersistedFeature's id as a prelude to saving it."""
        pass

    @property
    @abstractmethod
    def GEOMETRY(self):
        """Return the Feature's geometry."""
        return self.geometry()

    @property
    @abstractmethod
    def NAME(self):
        return self.TITLE

    @property
    @abstractmethod
    def TITLE(self):
        return f"{self.displayName()} {self.FID}"

    @property
    @abstractmethod
    def isInfrastructure(self):
        """Return True if the Feature is infrastructure."""
        pass

    @abstractmethod
    def hasField(self, fieldName):
        """Return True if the Feature's Schema has a Field with the supplied name."""
        pass

    @property
    @abstractmethod
    def hasArea(self):
        """Return True if the Feature has an area."""
        pass

    @property
    @abstractmethod
    def hasElevation(self):
        """Return True if the Feature has an elevation."""
        pass

    @property
    @abstractmethod
    def hasFid(self):
        """Return True if the Feature has a fid."""
        pass

    @property
    @abstractmethod
    def hasLength(self):
        """Return True if the Feature has a length."""
        pass

    @property
    @abstractmethod
    def hasLongitude(self):
        """Return True if the Feature has a longitude."""
        pass

    @property
    @abstractmethod
    def hasLatitude(self):
        """Return True if the Feature has a latitude."""
        pass

    @property
    @abstractmethod
    def hasPerimeter(self):
        """Return True if the Feature has a perimeter."""
        pass

    @property
    @abstractmethod
    def hasTimeframe(self):
        """Return True if this layer has a """
        pass

    @property
    @abstractmethod
    def hasStatus(self):
        """Return True if this layer has a status."""
        pass

    @abstractmethod
    def matchTimeframe(self, timeframe):
        """Return True if this feature's timeframe or status matches the supplied timeframe."""
        pass

    @abstractmethod
    def selectFeature(self):
        """Select the Feature."""
        pass

    @abstractmethod
    def zoomFeature(self):
        """Zoom to the Feature."""
        pass
