# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsFeature, QgsFields

from ...models.glitch import Glitch
from ...utils import qgsDebug, qgsInfo
from .feature import Feature
from ..fields.schemas import PersistedFeatureSchema


@PersistedFeatureSchema.addSchema()
class PersistedFeature(Feature):

    featureUpserted = pyqtSignal()
    featureDeleted = pyqtSignal()
    featureSelected = pyqtSignal()

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Feature."""

        if not existingFeature:
            # Build an empty QgsFeature and wrap it up
            fields = QgsFields()
            for field in featureLayer.fields():
                fields.append(field)
            qgsFeature = QgsFeature(fields)

            # Need to call the superclass __init__ ASAP, otherwise PyQt complains
            super().__init__(featureLayer, qgsFeature)

            for field in self.getSchema():
                field.setDefaultValue(self)

            # Clear FID
            self.clearId()

        elif isinstance(existingFeature, Feature):
            # Repeat the constructor for an empty Feature
            # Build an empty QgsFeature and wrap it up
            fields = QgsFields()
            for field in self.getSchema():
                fields.append(field)
            qgsFeature = QgsFeature(fields)

            # Need to call the superclass __init__ ASAP, otherwise PyQt complains
            super().__init__(featureLayer, qgsFeature)

            # Incoming Feature must have compatible schema
            missingFields, _ = self.checkSchema(existingFeature.getSchema())
            if missingFields:
                raise Glitch(f"{self.__class__.__name__}.__init__: incoming Feature has missing fields: {missingFields}")

            for field in self.getSchema():
                field.setDefaultValue(self)

            # Set all attributes and geometry from the incoming Feature
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

    @property
    def id(self):
        """Return the PersistedFeature's fid."""
        return self._qgsFeature.id()

    @id.setter
    def id(self, fid):
        """Set or the PersistedFeature's id."""
        self._qgsFeature.setId(fid)

    def clearId(self):
        """Set or the PersistedFeature's id."""
        self.id = -1
        self._qgsFeature.setAttribute('fid', self.id)

    @property
    def geometry(self):
        """Return the PersistedFeature's geometry."""
        return self._qgsFeature.geometry()

    @geometry.setter
    def geometry(self, g):
        """Set the PersistedFeature's geometry."""
        self._qgsFeature.setGeometry(g)

    @property
    def isInfrastructure(self):
        """Return True if the PersistedFeature is infrastructure."""
        return False

    def recalculate(self):
        """Recalculate derived data about the PersistedFeature."""
        pass

    def toProviderFeature(self):
        """Map the PersistedFeature's fields to the provider's fields."""
        qgsFeature = QgsFeature(self._qgsFeature)

        attributesWithProviderIndices = [
            (providerIndex,
             qgsFeature.attribute(index)) for (
                index,
                field) in enumerate(
                qgsFeature.fields()) for (
                providerIndex,
                providerField) in enumerate(
                    self.featureLayer.dataProvider().fields()) if providerField.name() == field.name()]

        # Sort the matched attributes
        attributesWithProviderIndices.sort(key=lambda x: x[0])

        providerAttributes = [v for (_, v) in attributesWithProviderIndices]

        qgsFeature.setFields(self.featureLayer.dataProvider().fields())
        qgsFeature.setAttributes(providerAttributes)
        return qgsFeature

    def upsert(self):
        """Add or update the PersistedFeature in the PersistedFeatureLayer."""
        
        assert(self.featureLayer.isEditable())
        
        # # TODO inefficient
        # self.recalculate()

        if (self.id >= 0):
            self.featureLayer.updateFeature(self)
            self.featureUpserted.emit()
            return self.id
        else:
            # We use the dataProvider to upsert, because we can get the new FID back this way
            qf = self.toProviderFeature()

            ((success, [newQf])) = self.featureLayer.dataProvider().addFeatures([qf])

            if success:
                self.id = newQf.id()
            else:
                raise Glitch(f"{self}.upsert: failed with unknown error")

        self.featureUpserted.emit()
        return self.id

    def delete(self):
        """Delete the PersistedFeature from the PersistedFeatureLayer."""
        self.featureLayer.deleteFeature(self)
        self.featureDeleted.emit()
