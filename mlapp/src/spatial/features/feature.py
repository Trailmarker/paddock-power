# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject, pyqtSlot
from re import finditer

from qgis.core import QgsFeature, QgsProject, QgsRectangle, QgsVectorLayer

from ...models.glitch import Glitch
from ..schemas.schemas import FID, STATUS, TIMEFRAME, FeatureSchema
from ..schemas.timeframe import Timeframe


@FeatureSchema.addSchema()
class Feature(QObject):

    @classmethod
    def displayName(cls):
        """Return the display name of the Feature."""
        matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', cls.__name__)
        return " ".join(m.group(0) for m in matches)

    @classmethod
    def getWkbType(cls):
        """Return the Feature's wkbType."""
        raise NotImplementedError("Feature.getWkbType: must be implemented in subclass")

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return True

    @classmethod
    def checkSchema(cls, fieldsToCheck):
        """Check that an incoming schema contains this Feature's schema. Checks field names only."""
        missing = [field for field in cls.getSchema() if field.name() not in [f.name() for f in fieldsToCheck]]
        extra = [field for field in fieldsToCheck if field.name() not in [f.name() for f in cls.getSchema()]]
        return missing, extra

    def __init__(self, featureLayer, existingFeature):
        """Create a new Feature."""
        super().__init__()

        if isinstance(existingFeature, QgsFeature):
            # Incoming QgsFeature must have the correct schema
            missingFields, _ = self.checkSchema(existingFeature.fields().toList())
            if missingFields:
                raise Glitch(f"{self.__class__.__name__}.__init__ incoming QgsFeature has missing fields: {missingFields}")

            self._qgsFeature = existingFeature

        elif existingFeature is not None:
            # What?
            raise Glitch(
                f"{self.__class__.__name__}.__init__: unexpected type {existingFeature.__class__.__name__} for provided existing feature data (should be a Feature subclass or QgsFeature)")

        self._featureLayerId = featureLayer.id()

    def __repr__(self):
        """Return a string representation of the Feature."""
        return f"{self.__class__.__name__}(id={self.id})"

    def __str__(self):
        """Convert the Feature to a string representation."""
        return repr(self)

    @property
    def featureLayer(self):
        """Return the FeatureLayer that contains this Feature."""
        return QgsProject.instance().mapLayer(self._featureLayerId)

    @property
    def id(self):
        """Return the Feature's fid."""
        return self._qgsFeature.id()

    @property
    def geometry(self):
        """Return the Feature's geometry."""
        return self._qgsFeature.geometry()

    @property
    def name(self):
        return self.title

    @property
    def title(self):
        return f"{self.displayName()} {self.id}"

    @property
    def isInfrastructure(self):
        """Return True if the Feature is infrastructure."""
        return False

    @property
    def hasTimeframe(self):
        """Return True if this layer has a """
        return TIMEFRAME in [field.name() for field in type(self).getSchema()]

    @property
    def hasStatus(self):
        return STATUS in [field.name() for field in type(self).getSchema()]

    def matchTimeframe(self, timeframe):
        """Return True if this feature's timeframe or status matches the supplied timeframe."""
        if self.hasTimeframe:
            return Timeframe[self.timeframe.name] == Timeframe[timeframe.name]
        elif self.hasStatus:
            return timeframe.matchFeatureStatus(self.status)
        else:
            return False

    @pyqtSlot()
    def selectFeature(self):
        """Select the Feature."""
        self.featureLayer.selectByIds([self.id], QgsVectorLayer.SetSelection)

    def zoomFeature(self):
        """Zoom to the Feature."""
        iface = self.featureLayer.getPaddockPowerProject().iface
        if self.geometry and iface:
            featureExtent = QgsRectangle(self.geometry.boundingBox())
            featureExtent.scale(1.5)  # Expand by 50%
            iface.mapCanvas().setExtent(featureExtent)
            iface.mapCanvas().refresh()

    def onSelectFeature(self):
        """Called when the Feature is selected."""
        self.zoomFeature()

    def onDeselectFeature(self):
        """Called when the Feature is selected."""
        pass
