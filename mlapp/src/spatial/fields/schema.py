# -*- coding: utf-8 -*-
from .field import Field


class Schema(list):
    def __init__(self, fields, wkbType=None):
        assert isinstance(fields, list)
        assert all(isinstance(f, Field) for f in fields)

        super().__init__(fields)
        self._wkbType = wkbType

    def hasField(self, field):
        return any(field == f.name for f in self)

    def addSchema(self):
        def _addSchema(cls):
            for field in self:
                if field._propertyName is not None:
                    field.addFieldProperty(cls)
                setattr(cls, "getSchema", classmethod(lambda _: self))
            if self._wkbType is not None:
                setattr(cls, "getWkbType", classmethod(lambda _: self._wkbType))
            return cls
        return _addSchema
