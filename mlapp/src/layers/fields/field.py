# -*- coding: utf-8 -*-
import re

from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsDefaultValue, QgsFeature, QgsEditorWidgetSetup, QgsField

from ...models import Glitch
from .field_domain import FieldDomain
from .names import FID


class Field(QgsField):

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], Field):
                # Copy constructor applied below in super().__init__
                self._propertyName = args[0]._propertyName
                self._domainType = args[0]._domainType
                self._defaultValue = args[0]._defaultValue
                self._required = args[0]._required
            elif isinstance(args[0], QgsField):
                # Construct from a 'raw' QgsField with a default _propertyName
                self._propertyName = re.sub('\\W|^(?=\\d)', '_', args[0].name())
                self._domainType = None
                self._defaultValue = None
                self._required = False
        else:
            # Pop off and apply the extra args for Field versus QgsField
            self._propertyName = kwargs.pop("propertyName", None)
            self._domainType = kwargs.pop('domainType', None)
            self._defaultValue = kwargs.pop('defaultValue', None)
            self._required = kwargs.pop('required', False)

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

    def __eq__(self, other):
        """Return True if the Field is equal to another Field, False otherwise."""
        if isinstance(other, Field):
            return self.name() == other.name()
        return False

    def __hash__(self):
        """Return a hash of the Field."""
        return hash(self.name())

    def __repr__(self):
        """Return a string representation of the Field."""
        return f"{self.__class__.__name__}(name={self.name()})"

    def __str__(self):
        """Convert the Field to a string representation."""
        return repr(self)

    @staticmethod
    def __fieldDomainToEditorWidgetSetup(domainType):
        """Get the editor widget setup for an enum type."""

        mappings = [{format(domainItem): domainItem.name} for domainItem in domainType]
        config = {
            'map': mappings,
        }
        return QgsEditorWidgetSetup('ValueMap', config)

    def __makeIdGetter(self):
        """Make a getter for the value of a FID field. Should not be called directly."""
        def _getter(feature: QgsFeature):
            fid = feature.id()
            if fid != feature.attribute(self.name()):
                feature.setAttribute(self.name(), fid)
            return fid
        return _getter

    def __makeIdSetter(self):
        """Make a setter for the value of a FID field. Should not be called directly."""
        def _setter(feature: QgsFeature, value):
            if value and value >= 0:
                feature.setId(value)
                feature.setAttribute(self.name(), value)
            else:
                feature.setId(-1)
                feature.setAttribute(self.name(), -1)
        return _setter

    def __makeFieldDomainGetter(self):
        """Make a getter for the value of a domain-valued field. Should not be called directly."""
        def _getter(feature: QgsFeature):
            try:
                return self._domainType[str(feature[self.name()])]
            except BaseException:
                if self._defaultValue is not None and isinstance(self._defaultValue, self._domainType):
                    feature.setAttribute(self.name(), self._defaultValue.name)
                return self._defaultValue
        return _getter

    def __makeFieldDomainSetter(self):
        """Make a setter for the value of a domain-valued field. Should not be called directly."""
        def _setter(feature: QgsFeature, domainValue):
            if isinstance(domainValue, self._domainType):
                feature.setAttribute(self.name(), domainValue.name)
            elif isinstance(domainValue, str):
                # Try a few ways to set the value
                try:
                    feature.setAttribute(self.name(), self._domainType[domainValue].name)
                except:
                    try:
                        feature.setAttribute(self.name(), self._domainType(domainValue).name)
                    except:
                        raise Glitch(f"Invalid value '{domainValue}' for field '{self.name()}'")
        return _setter

    def __makeRealGetter(self):
        """Make a getter for the value of a real-valued field. Should not be called directly."""
        def _getter(feature: QgsFeature):
            val = feature[self.name()]
            if isinstance(val, QVariant):
                if val.isNull():
                    return None
                unboxedVal = val.value() if val.convert(QVariant.Double) else None
                return float(unboxedVal)
            else:
                return float(val)
        return _getter

    def __makeStringGetter(self):
        """Make a getter for the value of a string-valued field. Handle 'NULL' correctly. Should not be called directly."""
        def _getter(feature: QgsFeature):
            val = feature[self.name()]
            if isinstance(val, QVariant):
                if val.isNull():
                    return None
            return str(val) if val else None
        return _getter

    def __makeGetter(self):
        if self.name() == FID:
            return self.__makeIdGetter()
        if self._domainType is not None:
            return self.__makeFieldDomainGetter()
        elif self.typeName() == "String":
            return self.__makeStringGetter()
        elif self.typeName() == "Real":
            return self.__makeRealGetter()
        else:
            return lambda feature: feature[self.name()]

    def __makeSetter(self):
        if self.name() == FID:
            return self.__makeIdSetter()
        if self._domainType is not None:
            return self.__makeFieldDomainSetter()
        else:
            return lambda feature, value: feature.setAttribute(self.name(), value)

    def getValue(self, feature):
        """Get the value of a Field on a Feature."""
        return self.__makeGetter()(feature)

    def setValue(self, feature, value):
        """Set the value of a Field on a Feature."""
        self.__makeSetter()(feature, value)

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


class CalculatedField(MeasureField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
