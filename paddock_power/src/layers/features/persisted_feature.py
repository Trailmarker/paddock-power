# -*- coding: utf-8 -*-
from qgis.core import QgsFeature

from ...models import Glitch
from ..calculator import Calculator
from ..interfaces import IPersistedFeature
from .feature import Feature


class PersistedFeature(Feature, IPersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Feature."""

        super().__init__(featureLayer, existingFeature)

    @property
    def GEOMETRY(self):
        """Return the PersistedFeature's geometry."""
        return self.geometry()

    @GEOMETRY.setter
    def GEOMETRY(self, g):
        """Set the PersistedFeature's geometry."""
        self.setGeometry(g)

    def recalculateELevation(self):
        """Recalculate the PersistedFeature's elevation, if applicable."""
        if self.GEOMETRY and self.hasElevation:
            elevationLayer = self.featureLayer.workspace.elevationLayer
            if elevationLayer and elevationLayer.isValid():
                self.ELEVATION = Calculator.calculateElevationAtPoint(self.GEOMETRY, elevationLayer)

    def recalculateElevationProfile(self):
        """Recalculate the PersistedFeature's elevation profile, if applicable."""
        if self.GEOMETRY and self.hasLength:
            elevationLayer = self.featureLayer.workspace.elevationLayer
            if elevationLayer and elevationLayer.isValid():
                self._profile = Calculator.calculateProfile(self.GEOMETRY, elevationLayer)
                length = round(self._profile.maximumDistance / 1000, 2)
                self.LENGTH = length

    def recalculate(self):
        """Recalculate everything that can be recalculated based on the Feature schema."""

        if self.hasName:
            if not self.NAME or self.NAME == "NULL":
                self.NAME = f"{self.displayName()} {self.FID}"

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

        self.recalculateELevation()
        self.recalculateElevationProfile()

    def __toProviderFeature(self):
        """Map the PersistedFeature's fields to the provider's fields."""
        # Copy ourselves
        clonedFeature = QgsFeature(self)

        attributesWithProviderIndices = [
            (providerIndex,
             clonedFeature.attribute(index)) for (
                index,
                field) in enumerate(
                clonedFeature.fields()) for (
                providerIndex,
                providerField) in enumerate(
                    self.featureLayer.dataProvider().fields()) if providerField.name() == field.name()]

        # Sort the matched attributes
        attributesWithProviderIndices.sort(key=lambda x: x[0])

        providerAttributes = [v for (_, v) in attributesWithProviderIndices]

        clonedFeature.setFields(self.featureLayer.dataProvider().fields())
        clonedFeature.setAttributes(providerAttributes)
        return clonedFeature

    def upsert(self):
        """Add or update the PersistedFeature in the PersistedFeatureLayer."""

        if (self.FID >= 0):
            self.featureLayer.updateFeature(self)
            return self.FID
        else:
            # We use the dataProvider to upsert, because we can get the new FID back this way
            qf = self.__toProviderFeature()

            ((success, [newQf])) = self.featureLayer.dataProvider().addFeatures([qf])

            if success:
                if not newQf.isValid():
                    raise Glitch(f"{self}.upsert: new feature is not valid")
                if newQf.id() <= 0:
                    raise Glitch(f"{self}.upsert: new feature has invalid FID")

                # On first insert, we calculate the stuff - including a default NAME
                self.FID = newQf.id()
                self.recalculate()
                self.featureLayer.updateFeature(self)
                return self.FID
            else:
                raise Glitch(f"{self}.upsert: failed with unknown error")

    def delete(self):
        """Delete the PersistedFeature from the PersistedFeatureLayer."""
        self.featureLayer.deleteFeature(self)
