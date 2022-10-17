# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant, pyqtSignal

from qgis.core import QgsFeatureRequest, QgsProject, QgsVectorLayer, QgsWkbTypes

from ...models.paddock_power_error import PaddockPowerError
from ...utils import resolveStylePath, qgsDebug
from ..features.feature import Feature
from .feature_layer_source_type import FeatureLayerSourceType

# Couple of lookup dictionaries (locally useful only)
QVARIANT_TYPES = dict([(getattr(QVariant, v), v) for v, m in vars(
    QVariant).items() if isinstance(getattr(QVariant, v), QVariant.Type)])

QGSWKB_TYPES = dict([(getattr(QgsWkbTypes, v), v) for v, m in vars(
    QgsWkbTypes).items() if isinstance(getattr(QgsWkbTypes, v), QgsWkbTypes.Type)])

# Paddock Power data is held in the GDA2020 coordinate system
PADDOCK_POWER_EPSG = 7845


class FeatureLayer(QgsVectorLayer):
    featureStateChanged = pyqtSignal(Feature)

    def __init__(self, featureType=Feature, sourceType=FeatureLayerSourceType.Memory, layerName=None,
                 gpkgFile=None, styleName=None):
        """Create a new Paddock Power vector layer."""

        self.featureType = featureType
        self.wrapFeature = lambda existingFeature: featureType(self, existingFeature)

        wkbType = featureType.getWkbType()
        schema = featureType.getSchema()

        if sourceType == FeatureLayerSourceType.Memory:
            assert(layerName is not None)
            assert(wkbType is not None)
            assert(schema is not None)

            layerDefinition = f"{QGSWKB_TYPES[wkbType]}?crs=epsg:{PADDOCK_POWER_EPSG}"

            super().__init__(path=layerDefinition, baseName=layerName, providerLib="memory")

            # Have to start editing to get schema updates to stick
            self.startEditing()
            self.dataProvider().addAttributes(schema)
            self.commitChanges()

        elif sourceType == FeatureLayerSourceType.File:
            assert(layerName is not None)
            assert(gpkgFile is not None)

            gpkgUrl = f"{gpkgFile}|layername={layerName}"

            super().__init__(path=gpkgUrl, baseName=layerName, providerLib="ogr")

        # Optionally apply a style to the layer
        if styleName is not None:
            stylePath = resolveStylePath(styleName)
            self.loadNamedStyle(stylePath)

        # Apply editor widgets
        for field in schema:
            fieldIndex = self.fields().indexFromName(field.name())
            self.setEditorWidgetSetup(fieldIndex, field.editorWidgetSetup())
            self.setDefaultValueDefinition(fieldIndex, field.defaultValueDefinition())

    def featureType(self):
        """Get the Paddock Power layer type."""
        return self.featureType

    def copyTo(self, otherLayer):
        """Copy all features in this layer to another layer."""
        if otherLayer is None:
            raise PaddockPowerError(
                "VectorLayer.copyTo: the target layer is not present")

        if self.featureType() != otherLayer.getLayerType():
            raise PaddockPowerError(
                f"Cannot copy features from {self.featureType().name} to {otherLayer.getLayerType().name}")

        otherLayer.startEditing()
        otherLayer.dataProvider().addFeatures(self.getFeatures())
        otherLayer.commitChanges()

    def addToMap(self, group):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        if group is None:
            raise PaddockPowerError(
                "VectorLayer.addToMap: the layer group is not present")

        node = group.findLayer(self.id())
        if node is None:
            group.addLayer(self)

    def _unwrapQgsFeature(self, feature):
        """Unwrap a Feature into a QgsFeature."""
        if not isinstance(feature, self.featureType):
            raise PaddockPowerError(
                f"VectorLayer.__unwrapQgsFeature: the feature is not a {self.featureType.__name__}")
        return feature._qgsFeature

    def _wrapQgsFeatures(self, qgsFeatures):
        """Adapt the features in this layer."""
        for feature in qgsFeatures:
            feature = self.wrapFeature(feature)
            yield feature

    def makeFeature(self, existingFeature=None):
        """Make a new Feature in this layer."""
        return self.wrapFeature(existingFeature)

    def copyFeature(self, feature):
        """Copy a Feature from this layer to the clipboard."""
        if not isinstance(feature, self.featureType):
            raise PaddockPowerError(
                "{self.__class__.__name__}.copyFeature: the incoming feature is not a {self.featureType.__name__}")

        qgsFeature = self._unwrapQgsFeature(feature)
        copyFeature = self.makeFeature()
        copyQgsFeature = self._unwrapQgsFeature(copyFeature)
        copyQgsFeature.setAttributes(qgsFeature.attributes())
        copyQgsFeature.setGeometry(qgsFeature.geometry())
        copyFeature.setId()
        return copyFeature

    def addFeature(self, feature):
        """Add a feature to the layer."""
        feature.setId()
        super().addFeature(self._unwrapQgsFeature(feature))

    def updateFeature(self, feature):
        """Add a feature to the layer."""
        super().updateFeature(self._unwrapQgsFeature(feature))

    def deleteFeature(self, feature):
        """Delete a feature from the layer."""
        super().deleteFeature(feature.id())

    def getFeatures(self, request=None):
        """Get the features in this layer."""
        if request is None:
            return self._wrapQgsFeatures(super().getFeatures())

        if not isinstance(request, QgsFeatureRequest):
            raise PaddockPowerError(
                "VectorLayer.getFeatures: the request is not a QgsRequest")

        return self._wrapQgsFeatures(super().getFeatures(request))

    def getFeaturesByStatus(self, *statuses, request=None):
        """Get the features in this layer filtered by one or more FeatureStatus values."""
        if not statuses:
            return self.getFeatures(request)
        return [f for f in self.getFeatures(request) if f.status in statuses]

    def whileEditing(self, func):
        """Run a function with the layer in edit mode."""
        isEditing = self.isEditable()

        try:
            if not isEditing:
                qgsDebug(f"{self.__class__.__name__}.whileEditing: starting an instant edit session")
                self.startEditing()
                func()
                self.commitChanges()
                qgsDebug(f"{self.__class__.__name__}.whileEditing: closing instant edit session")
            else:
                func()
        except Exception as e:
            self.rollBack()
            raise PaddockPowerError(
                f"VectorLayer.whileEditing: an exception occurred {str(e)}")
        finally:
            newIsEditing = self.isEditable()
            if isEditing and not newIsEditing:
                self.startEditing()
            else: 
                self.rollBack()

    def featureCount(self):
        """Get the number of Features in the layer."""
        return len([f for f in self.getFeatures()])

    def instantAddFeature(self, feature):
        """Start editing, add a Feature and commt the changes."""
        self.whileEditing(lambda: self.addFeature(feature))

    def instantUpdateFeature(self, feature):
        """Start editing, update a Feature and commt the changes."""
        self.whileEditing(lambda: self.updateFeature(feature))


# Helper functions - used to convert QgsField objects to code in the console as below
def dumpQgsFieldConstructorStatement(field):
    """Print a QgsField constructor statement for the given QgsField object."""
    return f"Field(propertyName="", name=\"{field.name()}\", type=QVariant.{QVARIANT_TYPES[field.type()]}, typeName=\"{field.typeName()}\", len={field.length()}, prec={field.precision()}, comment=\"{field.comment()}\", subType=QVariant.{QVARIANT_TYPES[field.subType()]})"


def dumpQgsFields(fields):
    """Print a list of QgsField constructor statements for the given QgsFields object."""
    for field in fields.toList():
        print(dumpQgsFieldConstructorStatement(field), ",")


def dumpLayerFieldsByName(layerName):
    """Match a map layer by name and dump all its fields as above."""
    project = QgsProject.instance()
    layer = project.mapLayersByName(layerName)[0]
    dumpQgsFields(layer.fields())
