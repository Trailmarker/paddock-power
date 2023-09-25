# -*- coding: utf-8 -*-
from functools import cached_property

from ...models import Glitch
from ...utils import PADDOCK_POWER_EPSG, qgsDebug
from ...layers.fields.schema import Schema


class FieldMap(list):

    def __init__(self, importLayer, targetLayer):
        """Create a FieldMap."""
        super().__init__()

        self.importLayer = importLayer
        self.targetLayer = targetLayer

        self.initMappings()

    @cached_property
    def importQgsFields(self):
        """Return the import layer's field names as a QgsFields object."""
        return self.importLayer.fields()

    @cached_property
    def targetFields(self):
        """Return the target schema's field names as a list."""
        return self.targetLayer.getSchema().targetFields

    @cached_property
    def targetQgsFields(self):
        """Return the target schema's field names as a list."""
        return Schema.toQgsFields(self.targetFields)

    def __repr__(self):
        """Return a string representation of the FieldMap."""
        return f"{type(self).__name__}({super().__repr__()})"

    def initMappings(self):
        """Set up the default field mappings based on the import and target fields."""
        self.clear()
        for targetField in self.targetFields:
            default = None
            for importField in self.importQgsFields:
                if targetField.name().upper() == importField.name().upper():
                    default = (importField, targetField)
            if not default and targetField.required():
                default = (None, targetField)
            if default:
                self.append(default)

    @property
    def nextUnmappedTargetField(self):
        """Return the next unmapped target field, if any."""
        mapped = [targetField for (_, targetField) in self]
        return next((targetField for targetField in self.targetFields if targetField not in mapped), None)

    def getImportField(self, targetField):
        """Return the import field, if any, that maps to the given target field."""

        for (importField, field) in self:
            if field.name() == targetField.name():
                return importField
        return None

    def update(self, index, importFieldName, targetFieldName):
        """Update the mapping for the given target Field."""
        importField = self.importQgsFields.field(importFieldName) if importFieldName else None
        targetField = self.targetLayer.getSchema().field(targetFieldName)

        if index == len(self):
            self.append((importField, targetField))
        else:
            self[index] = (importField, targetField)

    def mapFeature(self, feature, targetFeature):
        """Map a QgsFeature to another QgsFeature via this FieldMap."""

        # No longer necessary to manually reproject, because the QgsFeatureRequest
        # used to get the import features already handles the destination coordinate system
        targetFeature.setGeometry(feature.geometry())

        # Suck the mapped import fields into the target feature fields
        for targetField in targetFeature.getSchema().targetFields:
            importField = self.getImportField(targetField)

            try:
                if importField:
                    importValue = feature.attribute(importField.name())
                    if importValue is not None:
                        targetFeature.setAttribute(targetField.name(), importValue)
                elif targetField.required():
                    raise Glitch(
                        f"{self}.mapFeature(): no configured import field maps to required field '{targetField.name()}'")
            except BaseException:
                qgsDebug(f"Failed to import {importField.name()} to {targetField.name()}")
                raise

        return targetFeature
