# -*- coding: utf-8 -*-
from qgis.core import QgsFields

from ...models import Glitch
from ..interfaces import IFeature
from .field import Field
from .names import FID


class Schema(list):
    def __init__(self, fields, wkbType=None, hiddenFields=[]):
        assert isinstance(fields, list)
        assert all(isinstance(f, Field) for f in fields)

        super().__init__(fields)
        self.wkbType = wkbType
        self.hiddenFields = hiddenFields

    def field(self, fieldName):
        """Return the Field with the given name."""
        return next((f for f in self if f.name() == fieldName), None)

    def hasField(self, fieldName):
        """Check if this Schema has a Field with the given name."""
        return any(fieldName == f.name() for f in self)

    def toQgsFields(self):
        """Convert this Schema to a QgsFields object."""
        fields = QgsFields()
        for f in self:
            fields.append(f)
        return fields

    def toImportableFields(self):
        """Convert this Schema to a QgsFields object representing fields that can be imported."""
        return [f for f in self if f.importable()]

    def addSchema(self):
        """Return a decorator that implements getSchema and getWkbType classmethods for
           the decorated class based on this Schema."""
        def _addSchema(cls):
            if not issubclass(cls, IFeature):
                raise Glitch("Cannot add a Schema to class that does not implement IFeature")

            for field in self:
                if field._propertyName is not None and field.name() is not FID:
                    field.addFieldProperty(cls)
            setattr(cls, "getSchema", classmethod(lambda _: self))
            setattr(cls, "getWkbType", classmethod(lambda _: self.wkbType))
            return cls

        return _addSchema

    def checkFields(self, fields):
        """Check that the given Feature is compatible with this Schema."""
        missing = [field for field in self if field.name() not in [f.name() for f in fields]]
        extra = [field for field in fields if field.name() not in [f.name() for f in self]]
        return missing, extra

    def containsSchema(self, otherSchema):
        """Check that the given Feature is compatible with this Schema."""
        extra = [field for field in otherSchema if field.name() not in [f.name() for f in self]]
        return not bool(extra) and self.wkbType == otherSchema.wkbType

    def hiddenFieldNames(self):
        """Get all names of Fields that are hidden at either the Field or Schema level."""
        hiddenFieldNames = sum((f.hiddenFieldNames() for f in self), [])
        hiddenFieldNames += [f.displayFieldName() for f in self.hiddenFields]

        return hiddenFieldNames
