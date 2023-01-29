# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsFeature, QgsFields

from ...models.glitch import Glitch
from ..calculator import Calculator
from ..fields.names import FID
from ..layers.elevation_layer import ElevationLayer
from .feature import Feature

class PersistedFeature(Feature):

    def __init__(self, featureLayerType, existingFeature=None):
        """Create a new Feature."""

        self._featureUpserteds = []

        # This will be unused unless this is a LineFeature
        self._profile = None

        if not existingFeature:
            # Build an empty QgsFeature and wrap it up
            qgsFeature = QgsFeature(featureLayerType.getSchema().toQgsFields())

            # Need to call the superclass __init__ ASAP, otherwise PyQt complains
            super().__init__(featureLayerType, qgsFeature)

            for field in self.getSchema():
                field.setDefaultValue(self)

            # Clear FID
            self.clearId()

        elif isinstance(existingFeature, QgsFeature):
            # Repeat the constructor for an empty Feature
            # Build an empty QgsFeature and wrap it up
            fields = QgsFields()
            for field in self.getSchema():
                fields.append(field)
            qgsFeature = QgsFeature(fields)

            # Need to call the superclass __init__ ASAP, otherwise PyQt complains
            super().__init__(featureLayerType, existingFeature)

            # Incoming Feature must have compatible schema
            missingFields, _ = self.getSchema().checkFields(existingFeature.fields())
            if missingFields:
                raise Glitch(f"{self.__class__.__name__}.__init__: incoming Feature has missing fields: {missingFields}")

            for field in self.getSchema():
                field.setDefaultValue(self)

            # Set all attributes and geometry from the incoming Feature
            self.setAttributes(existingFeature.attributes())
            self.setGeometry(existingFeature.geometry())

            # Clear FID so that it will be created on upsert
            self.clearId()

        elif existingFeature is not None:
            # What?
            raise Glitch(
                f"{self.typeName}.__init__: unexpected type {type(existingFeature).__name__} for provided existing feature data (should be a Feature subclass or QgsFeature)")

    @property
    def FID(self):
        """Return the PersistedFeature's fid."""
        return self.id()

    @FID.setter
    def FID(self, fid):
        """Set or the PersistedFeature's id."""
        if self.hasFid:
            self.setAttribute(FID, fid)
        self.setId(fid)

    def clearId(self):
        """Set or the PersistedFeature's id."""
        self.FID = -1
        
    @property
    def ATTRIBUTES(self):
        """Return the PersistedFeature's attributes."""
        return self.attributes()

    @ATTRIBUTES.setter
    def GEOMETRY(self, attrs):
        """Set the PersistedFeature's geometry."""
        self.setAttributes(attrs)

    @property
    def GEOMETRY(self):
        """Return the PersistedFeature's geometry."""
        return self.geometry()

    @GEOMETRY.setter
    def GEOMETRY(self, g):
        """Set the PersistedFeature's geometry."""
        self.setGeometry(g)



    def recalculate(self):
        """Recalculate the length of this Pipeline."""
        self._profile = Calculator.calculateProfile(self.GEOMETRY, self.elevationLayer)
        length = round(self._profile.maximumDistance / 1000, 2)
        self.LENGTH = length



    def recalculate(self):
        """Recalculate everything that can be recalculated based on the Feature schema."""
        
        if self.GEOMETRY:
            if self.hasArea:
                self.AREA = round(Calculator.calculateArea(self.GEOMETRY) / 1000000, 2)
            if self.hasPerimeter:
                self.PERIMETER = round(Calculator.calculatePerimeter(self.GEOMETRY) / 1000, 2)
            if self.hasLongitude or self.hasLatitude:
                (longitude, latitude) = Calculator.calculateLongitudeAndLatitudeAtPoint(self.GEOMETRY)
                if self.hasLongitude:
                    self.LONGITUDE = longitude
                if self.hasLatitude:
                    self.LATITUDE = latitude
            if self.hasElevation or self.hasProfile:
                elevationLayer = self.depend(ElevationLayer)
                if self.hasElevation:
                    self.ELEVATION = Calculator.calculateElevationAtPoint(self.GEOMETRY, elevationLayer)
                if self.hasLength:
                    self._profile = Calculator.calculateProfile(self.GEOMETRY, elevationLayer)
                    length = round(self._profile.maximumDistance / 1000, 2)
                    self.LENGTH = length
     

    def toProviderFeature(self):
        """Map the PersistedFeature's fields to the provider's fields."""
        # Copy ourselves
        qgsFeature = QgsFeature(self)

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

        # assert self.featureLayer.isEditable()

        # # TODO inefficient
        self.recalculate()

        if (self.FID >= 0):
            self.featureLayer.updateFeature(self)
            self.featureUpserted()
            return self.FID
        else:
            # We use the dataProvider to upsert, because we can get the new FID back this way
            qf = self.toProviderFeature()

            ((success, [newQf])) = self.featureLayer.dataProvider().addFeatures([qf])

            if success:
                self.FID = newQf.id()
            else:
                raise Glitch(f"{self}.upsert: failed with unknown error")

        self.featureUpserted()
        return self.FID

    def delete(self):
        """Delete the PersistedFeature from the PersistedFeatureLayer."""
        self.featureLayer.deleteFeature(self)
        
    @property
    def featureUpserted(self):
        def __callUpsertedHandlers():
            for func in self._featureUpserteds:
                func()
        return __callUpsertedHandlers
    
    @featureUpserted.setter
    def featureUpserted(self, featureUpserted):
        self._featureUpserteds.append(featureUpserted)

