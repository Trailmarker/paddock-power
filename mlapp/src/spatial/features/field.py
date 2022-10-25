# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsDefaultValue, QgsFeature, QgsEditorWidgetSetup, QgsField

from ...models.glitch import Glitch
from ...utils import qgsDebug
from .field_domain import FieldDomain


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

        if self._defaultValue is not None:
            qgsDebug(f"Setting default value for field: {self.name()}, {self._defaultValue}")

        if self._domainType is not None:
            self.setEditorWidgetSetup(Field.__fieldDomainToEditorWidgetSetup(self._domainType))
        else:
            self.setEditorWidgetSetup(QgsEditorWidgetSetup())
        if self._defaultValue is not None:
            if self._defaultValue == "NULL":
                self.setDefaultValueDefinition(QgsDefaultValue("NULL"))
            elif isinstance(self._defaultValue, FieldDomain):
                self.setDefaultValueDefinition(QgsDefaultValue(f"'{self._defaultValue.name}'"))
            elif self._defaultValue is str:
                self.setDefaultValueDefinition(QgsDefaultValue(f"'{self._defaultValue}'"))
            else:
                self.setDefaultValueDefinition(QgsDefaultValue(str(self._defaultValue)))
        else:
            self.setDefaultValueDefinition(QgsDefaultValue())

    @staticmethod
    def __fieldDomainToEditorWidgetSetup(domainType):
        """Get the editor widget setup for an enum type."""

        mappings = [{format(domainItem): domainItem.name} for domainItem in domainType]
        config = {
            'map': mappings,
        }
        return QgsEditorWidgetSetup('ValueMap', config)

    def __makeFieldDomainGetter(self):
        """Make a getter for the value of a domain-valued field. Should not be called directly."""
        def _getter(feature: QgsFeature):
            try:
                return self._domainType[str(feature._qgsFeature[self.name()])]
            except BaseException:
                if self._defaultValue is not None and isinstance(self._defaultValue, self._domainType):
                    feature._qgsFeature.setAttribute(self.name(), self._defaultValue.name)
                return self._defaultValue
        return _getter

    def __makeFieldDomainSetter(self):
        """Make a setter for the value of a domain-valued field. Should not be called directly."""
        def _setter(feature: QgsFeature, domainValue):
            if not isinstance(domainValue, self._domainType):
                raise Glitch(f"{domainValue} must be a {self._domainType.__name__}")
            feature._qgsFeature.setAttribute(self.name(), domainValue.name)
        return _setter

    def __makeGetter(self):
        if self._domainType is not None:
            return self.__makeFieldDomainGetter()
        elif self.typeName() == "String":
            return lambda feature: str(feature._qgsFeature[self.name()])
        else:
            return lambda feature: feature._qgsFeature[self.name()]

    def __makeSetter(self):
        if self._domainType is not None:
            return self.__makeFieldDomainSetter()
        else:
            return lambda feature, value: feature._qgsFeature.setAttribute(self.name(), value)

    def setDefaultValue(self, feature):
        """Set the default value of a field on a feature."""
        if self._defaultValue:
            self.__makeSetter()(feature, self._defaultValue)

    def addFieldProperty(self, cls):
        """Add a Python property to a Feature class for this Field."""
        # getterName = f"_{self._propertyName}"
        # setterName = f"_set{self._propertyName.capitalize()}"

        # setattr(cls, getterName, self.__makeGetter())
        # setattr(cls, setterName, self.__makeSetter())
        setattr(cls, self._propertyName, property(self.__makeGetter(), self.__makeSetter()))


class MeasureField(Field):
    def __init__(self, propertyName, name, *args, **kwargs):
        super().__init__(propertyName=propertyName, name=name, type=QVariant.Double,
                         typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid, *args, **kwargs)


class StringField(Field):
    def __init__(self, propertyName, name, *args, **kwargs):
        super().__init__(propertyName=propertyName, name=name, type=QVariant.String, typeName="String",
                         len=0, prec=0, comment="", subType=QVariant.Invalid, *args, **kwargs)


class IdField(Field):
    def __init__(self, propertyName, name, *args, **kwargs):
        super().__init__(propertyName=propertyName, name=name, type=QVariant.LongLong, typeName="Integer64",
                         len=0, prec=0, comment="", subType=QVariant.Invalid, *args, **kwargs)


class DomainField(Field):
    def __init__(self, propertyName, name, domainType, *args, **kwargs):
        super().__init__(propertyName=propertyName, name=name, type=QVariant.String, typeName="String",
                         len=0, prec=0, comment="", subType=QVariant.Invalid, domainType=domainType, *args, **kwargs)
