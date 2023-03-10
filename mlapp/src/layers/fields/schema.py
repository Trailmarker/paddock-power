# -*- coding: utf-8 -*-
from qgis.core import QgsFields

from .field import Field
from .names import FID


class Schema(list):
    def __init__(self, fields, wkbType=None):
        assert isinstance(fields, list)
        assert all(isinstance(f, Field) for f in fields)

        super().__init__(fields)
        self.wkbType = wkbType

    def hasField(self, field):
        return any(field == f.name() for f in self)

    def toQgsFields(self):
        fields = QgsFields()
        for f in self:
            fields.append(f)
        return fields

    def addSchema(self):
        def _addSchema(cls):
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

    def displayFieldNames(self):
        return [f.displayFieldName() for f in self]
