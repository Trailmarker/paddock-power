# -*- coding: utf-8 -*-
from enum import Enum

from qgis.core import QgsDefaultValue, QgsFeature, QgsEditorWidgetSetup, QgsField

from ...models.glitch import Glitch


class Field(QgsField):

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], Field):
            self._propertyName = args[0]._propertyName
            self._domainType = args[0]._domainType
            self._defaultValue = args[0]._defaultValue
        else:
            # Pop off the extra args
            self._propertyName = kwargs.pop("propertyName", None)
            self._domainType = kwargs.pop('domainType', None)
            self._defaultValue = kwargs.pop('defaultValue', None)

        super().__init__(*args, **kwargs)

        if self._domainType is not None:
            self.setEditorWidgetSetup(Field.enumToEditorWidgetSetup(self._domainType))
        else:
            self.setEditorWidgetSetup(QgsEditorWidgetSetup())
        if self._defaultValue is not None:
            if self._defaultValue == "NULL":
                self.setDefaultValueDefinition(QgsDefaultValue("NULL"))
            elif isinstance(self._defaultValue, Enum):
                self.setDefaultValueDefinition(QgsDefaultValue(f"'{self._defaultValue.name}'"))
            elif self._defaultValue is str:
                self.setDefaultValueDefinition(QgsDefaultValue(f"'{self._defaultValue}'"))
            else:
                self.setDefaultValueDefinition(QgsDefaultValue(str(self._defaultValue)))
        else:
            self.setDefaultValueDefinition(QgsDefaultValue())

    @staticmethod
    def enumToEditorWidgetSetup(enumType):
        """Get the editor widget setup for an enum type."""

        mappings = [{enumType.value: enumType.name} for enumType in enumType]
        config = {
            'map': mappings,
        }

        return QgsEditorWidgetSetup('ValueMap', config)

    def _makeDomainvValuedFieldGetter(self):
        """Make a gette for the value of a domain-valued field. Should not be called directly."""
        def _getter(feature: QgsFeature):
            try:
                return self._domainType(str(feature._qgsFeature[self.name()]))
            except BaseException:
                if self._defaultValue is not None and isinstance(self._defaultValue, self._domainType):
                    feature._qgsFeature.setAttribute(self.name(), self._defaultValue.name)
                return self._defaultValue
        return _getter

    def _makeDomainValuedFieldSetter(self):
        """Set the value of a domain-valued field. Should not be called directly."""
        def _setter(feature: QgsFeature, domainValue):
            if not isinstance(domainValue, self._domainType):
                raise Glitch(f"{domainValue} must be a {self._domainType.__name__}")
            feature._qgsFeature.setAttribute(self.name(), domainValue.name)
        return _setter

    def _makeGetter(self):
        if self._domainType is not None:
            return self._makeDomainvValuedFieldGetter()
        elif self.typeName() == "String":
            return lambda feature: str(feature._qgsFeature[self.name()])
        else:
            return lambda feature: feature._qgsFeature[self.name()]

    def _makeSetter(self):
        if self._domainType is not None:
            return self._makeDomainValuedFieldSetter()
        else:
            return lambda feature, value: feature._qgsFeature.setAttribute(self.name(), value)

    def addFieldProperty(self, cls):
        """Add a Python property to a Feature class for this Field."""
        getterName = f"_{self._propertyName}"
        setterName = f"_set{self._propertyName.capitalize()}"

        setattr(cls, getterName, self._makeGetter())
        setattr(cls, setterName, self._makeSetter())

        setattr(cls, self._propertyName, property(fget=getattr(cls, getterName), fset=getattr(cls, setterName)))
