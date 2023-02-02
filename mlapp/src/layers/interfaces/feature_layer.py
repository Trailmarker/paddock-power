# -*- coding: utf-8 -*-
from abc import abstractclassmethod
from .map_layer import MapLayer


class FeatureLayer(MapLayer):
    @abstractclassmethod
    def getFeatureType(cls):
        """Return the Feature type for this layer."""
        pass

    @classmethod
    def getSchema(cls):
        """Return the Schema for this layer."""
        return cls.getFeatureType().getSchema()

    @classmethod
    def getWkbType(cls):
        """Return the WKB type for this layer."""
        return cls.getSchema().wkbType

    @classmethod
    def focusOnSelect(self):
        """Return True if this layer should be focused when a feature is selected."""
        return self.getFeatureType().focusOnSelect()

