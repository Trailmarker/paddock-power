# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject
from re import finditer

from qgis.core import QgsFeature, QgsFields, QgsRectangle
from qgis.utils import iface

from ...models.glitch import Glitch
from .edits import Edits
from .feature_action import FeatureAction
from .feature_state_machine import FeatureStateMachine
from .schemas import FeatureSchema


@FeatureSchema.addSchema()
class Feature(QObject, FeatureStateMachine):
    # featurePersisted = pyqtSignal(int)
    # featureUpdated = pyqtSignal(int)

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
    def checkSchema(cls, fieldsToCheck):
        """Check that an incoming schema contains this Feature's schema. Checks field names only."""
        return [field for field in cls.getSchema() if field.name() not in [f.name() for f in fieldsToCheck]]

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Feature."""
        super().__init__()

        if not existingFeature:
            # Build an empty QgsFeature and wrap it up
            fields = QgsFields()
            for field in self.getSchema():
                fields.append(field)
            self._qgsFeature = QgsFeature(fields)
            self.clearId()

        elif isinstance(existingFeature, Feature):
            # Copy constructor for Feature and subclasses

            # Incoming Feature must have compatible schema
            missingFields = self.checkSchema(existingFeature.getSchema())
            if missingFields:
                raise Glitch(f"{self.__class__.name__}: incoming Feature has missing fields: {missingFields}")

            # First create an empty Feature with the correct schema
            self.__init__(featureLayer)

            # Then set all attributes and geometry
            self._qgsFeature.setAttributes(existingFeature._qgsFeature.attributes())
            self._qgsFeature.setGeometry(existingFeature._qgsFeature.geometry())

            # Clear FID so that it will be created on upsert
            self.clearId()
            return

        elif isinstance(existingFeature, QgsFeature):
            # Incoming QgsFeature must have the correct schema
            missingFields = self.checkSchema(existingFeature.fields().toList())
            if missingFields:
                raise Glitch(f"{self.__class__.name__} incoming QgsFeature has missing fields: {missingFields}")

            self._qgsFeature = existingFeature

        elif existingFeature is not None:
            # What?
            raise Glitch(
                f"Feature.__init__: unexpected type {existingFeature.__class__.__name__} for provided existing feature data (should be a Feature subclass or QgsFeature)")

        self.featureLayer = featureLayer

    def __repr__(self):
        """Return a string representation of the Feature."""
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}', status={self.status})"

    def __str__(self):
        """Convert the Feature to a string representation."""
        return repr(self)

    def upsert(self):
        """Add or update the Feature in the FeatureLayer."""
        # TODO inefficient
        self.recalculate()
        
        if (self.id >= 0):
            self.featureLayer.updateFeature(self)
        else:
            self.featureLayer.addFeature(self)

    def delete(self):
        """Delete the Feature from the FeatureLayer."""
        self.featureLayer.deleteFeature(self)

    def zoomToFeature(self):
        """Zoom to the Feature."""
        featureExtent = QgsRectangle(self.geometry.boundingBox())
        featureExtent.scale(1.5)  # Expand by 50%
        iface.mapCanvas().setExtent(featureExtent)
        iface.mapCanvas().refresh()

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

    @property
    def title(self):
        """Return the Feature's title."""
        f"{self.name}"


    @Edits.persistEdits
    @FeatureAction.trash.handler()
    def trashFeature(self):
        """Trash a Draft Feature."""
        return Edits.delete(self)
