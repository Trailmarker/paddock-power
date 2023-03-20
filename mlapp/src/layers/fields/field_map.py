# -*- coding: utf-8 -*-
from functools import cached_property
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFields, QgsGeometry, QgsProject

from ...utils import PADDOCK_POWER_EPSG


class FieldMap(list):

    def __init__(self, importLayer, targetLayer):
        """Create a FieldMap."""
        super().__init__()
        
        self.importLayer = importLayer
        self.targetLayer = targetLayer
        
        self.initMappings()

    @cached_property
    def importFields(self):
        """Return the import layer's field names as a list."""
        return self.importLayer.fields()

    @cached_property
    def targetFields(self):
        """Return the target schema's field names as a list."""
        return self.targetLayer.getSchema().toImportFields()

    def __repr__(self):
        """Return a string representation of the FieldMap."""
        return f"{type(self).__name__}({super().__repr__()})"

    def initMappings(self):
        """Set up the default field mappings based on the import and target fields."""
        self.clear()
        for targetField in self.targetFields():
            default = None
            for importField in self.importFields():
                if targetField.name().upper() == importField.name().upper():
                    default = (importField, targetField)
            if not default and targetField.required():
                default = (None, targetField)
            if default:
                self.append(default)

    @property
    def unmappedImportFields(self):
        """Return the import fields that are not mapped."""
        mapped = [importField for (importField, _) in self if importField is not None]     
        return QgsFields([f for f in self.importFields if f not in mapped])
   
    @property
    def unmappedTargetFields(self):
        """Return the target fields that are not mapped."""
        mapped = [targetField for (_, targetField) in self]     
        return QgsFields([f for f in self.targetFields if f not in mapped])
   
    def mapFieldsByName(self, importFieldName, targetFieldName):
        """Set the mapping for the given Field."""
        
        importField = self.importFields.field(importFieldName)
        targetField = self.targetFields.field(targetFieldName)
        
        if not importField or not targetField:
            return
        
        self.unmapField(targetField)        
        self.append((importField, targetField))
   
    def unmapField(self, targetField):
        """Remove the mapping for the given target Field."""
        (importMatch, targetMatch) = next(((i, t) for (i, t) in self if t == targetField), (None, None))
        if targetMatch:
            self.remove((importMatch, targetMatch))
        
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

        # Suck the mapped import fields into the target feature fields
        for targetField in targetFeature.getSchema():
            if targetField.name() in self:
                targetField.setValue(targetFeature, feature.attribute(self[targetField.name()]))

        return targetFeature
