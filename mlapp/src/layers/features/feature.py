# -*- coding: utf-8 -*-
from functools import cached_property
from re import finditer

from qgis.core import QgsFeature, QgsRectangle, QgsVectorLayer

from ...models import Glitch, QtAbstractMeta
from ..fields import AREA, ELEVATION, FID, LENGTH, LONGITUDE, LATITUDE, NAME, STATUS, PERIMETER, TIMEFRAME, Timeframe
from ..interfaces import IFeature


class Feature(QgsFeature, IFeature, metaclass=QtAbstractMeta):

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
            if not existingFeature.isValid():
                raise Glitch(
                    f"{type(self).__name__}.__init__: existingFeature.isValid() == False: {existingFeature}, experimenting with strictnesss about validity")

            # Incoming Feature must have compatible schema
            missingFields, _ = self.getSchema().checkFields(existingFeature.fields())
            if missingFields:
                raise Glitch(f"{type(self).__name__}.__init__: incoming Feature has missing fields: {missingFields}")

            QgsFeature.__init__(self, existingFeature)
            self.setAttributes(existingFeature.attributes())
            self.setGeometry(existingFeature.geometry())

        elif existingFeature is not None:
            # What?
            raise Glitch(
                f"{type(self).__name__}.__init__: unexpected type {type(existingFeature).__name__} (should be a QgsFeature)")

    def __repr__(self):
        """Return a string representation of the Feature."""
        attrs = [f"{f}={self.attribute(f)}" for f in [FID, STATUS, TIMEFRAME] if self.hasField(f)]
        return f"{type(self).__name__}({', '.join(attrs)})"

    def __str__(self):
        """Convert the Feature to a string representation."""
        return repr(self)

    def clearFid(self):
        """Nullify the PersistedFeature's id as a prelude to saving it."""
        self.FID = -1
        self.setId(-1)

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
        return self.hasField(FID) and self.attribute(FID) > 0

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
    def hasName(self):
        """Return True if the Feature has a latitude."""
        return self.hasField(NAME)

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

    def matchStatus(self, status):
        """Return True if this feature's status matches the supplied status."""
        if self.hasStatus:
            return self.STATUS.name == status.name
        else:
            return False

    def matchTimeframe(self, timeframe):
        """Return True if this feature's timeframe or status matches the supplied timeframe."""
        if self.hasTimeframe:
            # TIMEFRAME gets precedence if it is defined
            return timeframe.matchTimeframe(self.TIMEFRAME)
        elif self.hasStatus:
            return timeframe.matchFeatureStatus(self.STATUS)
        else:
            return False

    @classmethod
    def focusOnSelect(self):
        """Return True if the app should focus on this type of Feature when selected."""
        return True

    def selectFeature(self):
        """Select the Feature."""
        # qgsDebug(f"{self.__class__.__name__}.selectFeature({self}), self.FID={self.FID}, self.id()={self.id()}")
        self.featureLayer.selectByIds([self.id()], QgsVectorLayer.SetSelection)

    def zoomFeature(self):
        """Zoom to the Feature."""
        iface = self.featureLayer and self.featureLayer.workspace and self.featureLayer.workspace.iface
        if self.GEOMETRY and iface:
            featureExtent = QgsRectangle(self.GEOMETRY.boundingBox())
            featureExtent.scale(1.5)  # Expand by 50%
            iface.mapCanvas().setExtent(featureExtent)
            iface.mapCanvas().refresh()
