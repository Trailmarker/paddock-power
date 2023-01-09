# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsDefaultValue, QgsFeature, QgsEditorWidgetSetup, QgsField

from ...models.glitch import Glitch
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

    def __makeRealGetter(self):
        """Make a getter for the value of a real-valued field. Should not be called directly."""
        def _getter(feature: QgsFeature):
            val = feature._qgsFeature[self.name()]
            if isinstance(val, QVariant):
                unboxedVal = val.value() if val.convert(QVariant.Double) else None
                if unboxedVal == "NULL":
                    return None
            else:
                return float(val)
        return _getter

    def __makeGetter(self):
        if self._domainType is not None:
            return self.__makeFieldDomainGetter()
        elif self.typeName() == "String":
            return lambda feature: str(feature._qgsFeature[self.name()])
        elif self.typeName() == "Real":
            return self.__makeRealGetter()
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
        setattr(cls, self._propertyName, property(self.__makeGetter(), self.__makeSetter()))

    def setupLayer(self, layer):
        """Set up this Field in a FeatureLayer."""
        fieldIndex = layer.fields().indexFromName(self.name())
        layer.setEditorWidgetSetup(fieldIndex, self.editorWidgetSetup())
        layer.setDefaultValueDefinition(fieldIndex, self.defaultValueDefinition())


class MeasureField(Field):
    def __init__(self, propertyName, name, dps=2, *args, **kwargs):
        super().__init__(propertyName=propertyName, name=name, type=QVariant.Double,
                         typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid, *args, **kwargs)

        self._dps = dps

    def setupLayer(self, layer):
        """Set up this Field in a FeatureLayer."""
        # Default setup
        super().setupLayer(layer)

        # Create a separate, rounded expression field and add that as an expression field
        roundedField = QgsField(f"Rounded {self.name()}", QVariant.Double)
        roundedField.setAlias(self.name())
        layer.addExpressionField(f"round(\"{self.name()}\", {self._dps})", roundedField)

        # Hide this 'raw' field from the attribute table
        config = layer.attributeTableConfig()
        columns = config.columns()
        matches = [c for c in columns if c.name == self.name()]
        if matches:
            column = matches[0]
            column.hidden = True
            config.setColumns(columns)
            layer.setAttributeTableConfig(config)


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
