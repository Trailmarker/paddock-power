# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsProject, QgsVectorLayer, QgsWkbTypes
from qgis.PyQt.QtCore import QVariant

from ...models.paddock_power_error import PaddockPowerError
from ...utils import qgsDebug, resolveStylePath
from ..feature.feature import Feature
from .paddock_power_layer_source_type import PaddockPowerLayerSourceType

# Couple of lookup dictionaries (locally useful only)
QVARIANT_TYPES = dict([(getattr(QVariant, v), v) for v, m in vars(
    QVariant).items() if type(getattr(QVariant, v)) == QVariant.Type])

QGSWKB_TYPES = dict([(getattr(QgsWkbTypes, v), v) for v, m in vars(
    QgsWkbTypes).items() if type(getattr(QgsWkbTypes, v)) == QgsWkbTypes.Type])

# Paddock Power data is held in the GDA2020 coordinate system
PADDOCK_POWER_EPSG = 7845


class PaddockPowerVectorLayer(QgsVectorLayer):
    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None,
                 wkbType=None, schema=None, gpkgFile=None, styleName=None):
        """Create a new Paddock Power vector layer."""

        # By default, we don't adapt the features
        self.featureAdapter = None

        if sourceType == PaddockPowerLayerSourceType.Memory:
            assert(layerName is not None)
            assert(wkbType is not None)
            assert(schema is not None)

            layerDefinition = f"{QGSWKB_TYPES[wkbType]}?crs=epsg:{PADDOCK_POWER_EPSG}"

            super(PaddockPowerVectorLayer, self).__init__(
                path=layerDefinition, baseName=layerName, providerLib="memory")

            # Have to start editing to get schema updates to stick
            self.startEditing()
            self.dataProvider().addAttributes(schema)
            self.commitChanges()

        elif sourceType == PaddockPowerLayerSourceType.File:
            assert(layerName is not None)
            assert(gpkgFile is not None)

            gpkgUrl = f"{gpkgFile}|layername={layerName}"

            super(PaddockPowerVectorLayer, self).__init__(
                path=gpkgUrl, baseName=layerName, providerLib="ogr")

        # Optionally apply a style to the layer
        if styleName is not None:
            stylePath = resolveStylePath(styleName)
            self.loadNamedStyle(stylePath)

    def getLayerType(self):
        """Get the Paddock Power layer type."""
        pass

    def copyTo(self, otherLayer):
        """Copy all features in this layer to another layer."""
        if otherLayer is None:
            raise PaddockPowerError(
                "PaddockPowerVectorLayer.copyTo: the target layer is not present")

        if self.getLayerType() != otherLayer.getLayerType():
            raise PaddockPowerError(
                f"Cannot copy features from {self.getLayerType().name} to {otherLayer.getLayerType().name}")

        otherLayer.startEditing()
        otherLayer.dataProvider().addFeatures(self.getFeatures())
        otherLayer.commitChanges()

    def addToMap(self, group):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        if group is None:
            raise PaddockPowerError(
                "PaddockPowerVectorLayer.addToMap: the layer group is not present")

        node = group.findLayer(self.id())
        if node is None:
            group.addLayer(self)

    def addFeature(self, feature):
        """Add a feature to the layer."""
        if not isinstance(feature, Feature):
            raise PaddockPowerError(
                "PaddockPowerVectorLayer.addFeature: the feature is not a Feature")

        for field in feature.fields():
            qgsDebug(f"addFeature: field.name() {field.name()}")
            
            if field.name() not in self.fields().names():
                raise PaddockPowerError(
                    f"Cannot add feature to {self.name()}: field {field.name()} is not present")
            
        feature.clearId()
        super().addFeature(feature)

    def setFeatureAdapter(self, featureAdapter):
        """Set the QgsFeature mixin for this layer."""
        self.featureAdapter = featureAdapter

    def adaptFeatures(self, features):
        """Adapt the features in this layer."""
        if self.featureAdapter is not None:
            for feature in features:
                feature = self.featureAdapter(feature)
                yield feature
        else:
            return features

    def getFeatures(self, request=None):
        """Get the features in this layer."""
        if request is None:
            return self.adaptFeatures(super().getFeatures())

        if not isinstance(request, QgsFeatureRequest):
            raise PaddockPowerError(
                "PaddockPowerVectorLayer.getFeatures: the request is not a QgsRequest")

        return self.adaptFeatures(super().getFeatures(request))

    def getFeaturesByStatus(self, *statuses, request=None):
        """Get the features in this layer filtered by one or more FeatureStatus values."""
        return [f for f in self.getFeatures(request) if f.status() in statuses]

    def whileEditing(self, func):
        """Run a function with the layer in edit mode."""
        isEditing = self.isEditable()

        try:
            if not isEditing:
                self.startEditing()
                func()
                self.commitChanges()
            else:
                func()
                self.commitChanges()
                self.startEditing()
        except Exception as e:
            self.rollBack()
            raise PaddockPowerError(
                f"PaddockPowerVectorLayer.whileEditing: an exception occurred {str(e)}")
        finally:
            newIsEditing = self.isEditable()
            if isEditing and not newIsEditing:
                self.startEditing()

    def instantAddFeature(self, feature):
        """Start editing, add a Feature and commt the changes."""
        self.whileEditing(lambda: self.addFeature(feature))

    def instantUpdateFeature(self, feature):
        """Start editing, update a Feature and commt the changes."""
        self.whileEditing(lambda: self.updateFeature(feature))


# Helper functions - used to convert QgsField objects to code in the console as below
def dumpQgsFieldConstructorStatement(field):
    """Print a QgsField constructor statement for the given QgsField object."""
    return f"QgsField(name=\"{field.name()}\", type=QVariant.{QVARIANT_TYPES[field.type()]}, typeName=\"{field.typeName()}\", len={field.length()}, prec={field.precision()}, comment=\"{field.comment()}\", subType=QVariant.{QVARIANT_TYPES[field.subType()]})"


def dumpQgsFields(fields):
    """Print a list of QgsField constructor statements for the given QgsFields object."""
    for field in fields.toList():
        print(dumpQgsFieldConstructorStatement(field), ",")


def dumpLayerFieldsByName(layerName):
    """Match a map layer by name and dump all its fields as above."""
    project = QgsProject.instance()
    layer = project.mapLayersByName(layerName)[0]
    dumpQgsFields(layer.fields())


