# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsFeature, QgsFields

from ...models.glitch import Glitch
from .feature import Feature
from ..schemas.schemas import PersistedFeatureSchema


@PersistedFeatureSchema.addSchema()
class PersistedFeature(Feature):
    featureUpdated = pyqtSignal()
    featureDeleted = pyqtSignal()
    featureSelected = pyqtSignal()

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Feature."""
        
        if not existingFeature:
            # Build an empty QgsFeature and wrap it up
            fields = QgsFields()
            for field in self.getSchema():
                fields.append(field)
            qgsFeature = QgsFeature(fields)
            for field in self.getSchema():
                field.setDefaultValue(self)
            super().__init__(featureLayer, qgsFeature)
            self.clearId()

        elif isinstance(existingFeature, Feature):
            # Copy constructor for Feature and subclasses

            # Incoming Feature must have compatible schema
            missingFields, _ = self.checkSchema(existingFeature.getSchema())
            if missingFields:
                raise Glitch(f"{self.__class__.__name__}.__init__: incoming Feature has missing fields: {missingFields}")

            # First create an empty Feature with the correct schema
            self.__init__(featureLayer, None)

            # Then set all attributes and geometry
            self._qgsFeature.setAttributes(existingFeature._qgsFeature.attributes())
            self._qgsFeature.setGeometry(existingFeature._qgsFeature.geometry())

            # Clear FID so that it will be created on upsert
            self.clearId()

        elif isinstance(existingFeature, QgsFeature):
            super().__init__(featureLayer, existingFeature)

        elif existingFeature is not None:
            # What?
            raise Glitch(
                f"{self.__class__.__name__}.__init__: unexpected type {existingFeature.__class__.__name__} for provided existing feature data (should be a Feature subclass or QgsFeature)")

    def upsert(self):
        """Add or update the Feature in the FeatureLayer."""
        # TODO inefficient
        self.recalculate()

        if (self.id >= 0):
            self.featureLayer.updateFeature(self)
        else:
            self.featureLayer.addFeature(self)
        self.featureUpdated.emit()

    def delete(self):
        """Delete the Feature from the FeatureLayer."""
        self.featureLayer.deleteFeature(self)
        self.featureDeleted.emit()

    @property
    def id(self):
        """Return the Feature's fid."""
        return self._qgsFeature.id()

    @id.setter
    def id(self, fid):
        """Set or the Feature's id."""
        self._qgsFeature.setId(fid)

    def clearId(self):
        """Set or the Feature's id."""
        self.id = -1
        self._qgsFeature.setAttribute('fid', self.id)

    @property
    def geometry(self):
        """Return the Feature's geometry."""
        return self._qgsFeature.geometry()

    @geometry.setter
    def geometry(self, g):
        """Set the Feature's geometry."""
        self._qgsFeature.setGeometry(g)

    def recalculate(self):
        """Recalculate derived data about the Feature."""
        pass

    @property
    def isInfrastructure(self):
        """Return True if the Feature is infrastructure."""
        return False

