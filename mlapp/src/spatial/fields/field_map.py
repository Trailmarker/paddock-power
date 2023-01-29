# -*- coding: utf-8 -*-
from functools import cached_property
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeature, QgsGeometry, QgsProject

from ...models.glitch import Glitch
from ...utils import PADDOCK_POWER_EPSG

class FieldMap(dict):

    def __init__(self, importLayer, targetLayer, *args, **kwargs):
        """Create a FieldMap."""

        self.importLayer = importLayer
        self.targetLayer = targetLayer
        self.update(*args, **kwargs)

    @cached_property
    def importFieldNames(self):
        """Return the import layer's field names as a list."""
        return [f.name() for f in self.importLayer.fields()]
    
    @cached_property
    def targetFieldNames(self):
        """Return the target schema's field names as a list."""
        return [f.name() for f in self.targetLayer.getSchema()]

    def __setitem__(self, __key, __value) -> None:
        """Set the mapping for the given Field."""
        if not isinstance(__key, str) or __key not in self.importFieldNames:
            raise Glitch(f"Invalid FieldMap key, must be a field name from the import layer")
        
        if not isinstance(__value, str) or __value not in self.targetFieldNames:
            raise Glitch(f"Invalid FieldMap value, must be a field name from the target schema")

        return super().__setitem__(__key, __value)

    def __getitem__(self, __key) -> object:
        """Get the mapping for the given Field."""
        if not isinstance(__key, str) or __key not in self.importFieldNames:
            raise Glitch(f"Invalid FieldMap key, must be a field name from the import layer")
        
        return super().__getitem__(__key)

    def __repr__(self):
        """Return a string representation of the FieldMap."""
        return f"{type(self).__name__}({super().__repr__()})"

    def update(self, *args, **kwargs):
        """Update the FieldMap."""
        for k, v in dict(*args, **kwargs).items():
            self[k] = v
            
    def mapFeature(self, feature, targetFeature):
        """Map a QgsFeature to another QgsFeature via this FieldMap."""
       
        # Transform the imported geometry, if applicable
        if feature.hasGeometry():
            # Copy incoming
            destGeom = QgsGeometry(feature.geometry())        
            sourceCrs = self.importLayer.crs()
            destCrs = QgsCoordinateReferenceSystem(f"epsg:{PADDOCK_POWER_EPSG}")
            tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())
            # Stateful
            destGeom.transform(tr)
            targetFeature.setGeometry(destGeom)
                
        for field in feature.fields():
            if field.name() in self:
                targetFeature.setAttribute(self[field.name()], feature.attribute(field.name()))
        
        return targetFeature
