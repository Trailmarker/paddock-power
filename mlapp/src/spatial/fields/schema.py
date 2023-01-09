# -*- coding: utf-8 -*-
class Schema(list):
    def __init__(self, fieldList, wkbType=None):
        super().__init__(fieldList)
        self._wkbType = wkbType

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

