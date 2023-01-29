# -*- coding: utf-8 -*-
from functools import cached_property

from qgis.PyQt.QtCore import pyqtSlot
from re import finditer

from qgis.core import QgsFeature, QgsRectangle, QgsVectorLayer

from ...models.glitch import Glitch
from ...utils import qgsDebug
from ..fields.names import AREA, ELEVATION, FID, LENGTH, LONGITUDE, LATITUDE, STATUS, PERIMETER, TIMEFRAME
from ..fields.timeframe import Timeframe


class Feature(QgsFeature):

    @classmethod
    def displayName(cls):
        """Return the display name of the Feature."""
        matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', cls.__name__)
        return " ".join(m.group(0) for m in matches)

    def __init__(self, featureLayer, existingFeature):
        """Create a new Feature."""

        self.featureLayer = featureLayer
        
        # This will be unused unless this is a LineFeature
        self._profile = None

        if existingFeature is None:
            # Create a new feature
            QgsFeature.__init__(self, featureLayer.getSchema().toQgsFields())

            # Set defaults
            for field in self.getSchema():
                field.setDefaultValue(self)

            # Clear FID
            self.clearFid()

        if isinstance(existingFeature, QgsFeature):
            # Incoming Feature must have compatible schema
            missingFields, _ = self.getSchema().checkFields(existingFeature.fields())
            if missingFields:
                raise Glitch(f"{self.typeName}.__init__: incoming Feature has missing fields: {missingFields}")

            QgsFeature.__init__(self, existingFeature)
            self.setAttributes(existingFeature.attributes())
            self.setGeometry(existingFeature.geometry())

        elif existingFeature is not None:
            # What?
            raise Glitch(
                f"{self.typeName}.__init__: unexpected type {type(existingFeature).__name__} (should be a QgsFeature)")

    @cached_property
    def typeName(self):
        """Return the Feature's type name."""
        return type(self).__name__

    def __repr__(self):
        """Return a string representation of the Feature."""
        return f"{self.__class__.__name__}(id={self.FID})"

    def __str__(self):
        """Convert the Feature to a string representation."""
        return repr(self)

    def workspaceLayer(self, layerType):
        """Get a layer we depend on to work with by type."""
        return self.featureLayer.workspaceLayer(layerType)

    @property
    def FID(self):
        # Always keep ID consisted with FID attribute unless we are inserting
        if self.hasFID:
            fid, id = self.attribute(FID), self.id()
            if id <= 0 and fid > 0:
                self.setId(fid)
                return fid
            elif id > 0 and fid <= 0:
                self.setAttribute(FID, id)
                return id
        return self.id()

    @FID.setter
    def FID(self, fid):
        if self.hasFid:
            self.setAttribute(FID, fid)
        self.setId(fid)

    def clearFid(self):
        """Set or the PersistedFeature's id."""
        self.FID = -1

    @property
    def GEOMETRY(self):
        """Return the Feature's geometry."""
        return self.geometry()

    @property
    def NAME(self):
        return self.TITLE

    @property
    def TITLE(self):
        return f"{self.displayName()} {self.FID}"

    @property
    def isInfrastructure(self):
        """Return True if the Feature is infrastructure."""
        return False

    def hasField(self, fieldName):
        """Return True if the Feature's Schema has a Field with the supplied name."""
        return fieldName in [field.name() for field in self.getSchema()]

    @cached_property
    def hasArea(self):
        """Return True if the Feature has an area."""
        return self.hasField(AREA)

    @cached_property
    def hasElevation(self):
        """Return True if the Feature has an elevation."""
        return self.hasField(ELEVATION)

    @cached_property
    def hasFid(self):
        """Return True if the Feature has a fid."""
        return self.hasField(FID)

    @cached_property
    def hasLength(self):
        """Return True if the Feature has a length."""
        return self.hasField(LENGTH)

    @cached_property
    def hasLongitude(self):
        """Return True if the Feature has a longitude."""
        return self.hasField(LONGITUDE)

    @cached_property
    def hasLatitude(self):
        """Return True if the Feature has a latitude."""
        return self.hasField(LATITUDE)

    @cached_property
    def hasPerimeter(self):
        """Return True if the Feature has a perimeter."""
        return self.hasField(PERIMETER)

    @cached_property
    def hasTimeframe(self):
        """Return True if this layer has a """
        return self.hasField(TIMEFRAME)

    @cached_property
    def hasStatus(self):
        """Return True if this layer has a status."""
        return self.hasField(STATUS)

    def matchTimeframe(self, timeframe):
        """Return True if this feature's timeframe or status matches the supplied timeframe."""
        if self.hasTimeframe:
            return Timeframe[self.TIMEFRAME.name] == Timeframe[timeframe.name]
        elif self.hasStatus:
            return timeframe.matchFeatureStatus(self.STATUS)
        else:
            return False

    @classmethod
    def focusOnSelect(self):
        """Return True if the app should focus on this type of Feature when selected."""
        return True

    @pyqtSlot()
    def selectFeature(self):
        """Select the Feature."""
        qgsDebug(f"{self}.selectFeature(FID={self.FID})")
        self.featureLayer.selectByIds([self.id()], QgsVectorLayer.SetSelection)

    def zoomFeature(self):
        """Zoom to the Feature."""
        iface = self.featureLayer.getPaddockPowerProject().iface
        if self.GEOMETRY and iface:
            featureExtent = QgsRectangle(self.GEOMETRY.boundingBox())
            featureExtent.scale(1.5)  # Expand by 50%
            iface.mapCanvas().setExtent(featureExtent)
            iface.mapCanvas().refresh()

    def onSelectFeature(self):
        """Called when the Feature is selected."""
        self.zoomFeature()

    def onDeselectFeature(self):
        """Called when the Feature is selected."""
        pass
