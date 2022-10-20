# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant, pyqtSignal

from qgis.core import QgsCategorizedSymbolRenderer, QgsFeatureRequest, QgsProject, QgsVectorLayer, QgsWkbTypes

from ...models.glitch import Glitch
from ...utils import resolveStylePath, qgsDebug
from ..features.feature import Feature
from ..features.feature_status import FeatureStatus
from .feature_layer_source_type import FeatureLayerSourceType

# Couple of lookup dictionaries (locally useful only)
QVARIANT_TYPES = dict([(getattr(QVariant, v), v) for v, m in vars(
    QVariant).items() if isinstance(getattr(QVariant, v), QVariant.Type)])

QGSWKB_TYPES = dict([(getattr(QgsWkbTypes, v), v) for v, m in vars(
    QgsWkbTypes).items() if isinstance(getattr(QgsWkbTypes, v), QgsWkbTypes.Type)])

# Paddock Power data is held in the GDA2020 coordinate system
PADDOCK_POWER_EPSG = 7845


class FeatureLayer(QgsVectorLayer):
    displayFilterChanged = pyqtSignal(list)

    def __new__(cls, *args, **kwargs):

        sourceType = kwargs.get('sourceType', None)
        gpkgFile = kwargs.get('gpkgFile', None)
        layerName = kwargs.get('layerName', None)

        if sourceType == FeatureLayerSourceType.Detect:
            gpkgUrl = f"{gpkgFile}|layername={layerName}"

            for layer in QgsProject.instance().mapLayers().values():

                if layer.source() == gpkgUrl:
                    qgsDebug(f"{cls.__name__}.__new__: Coercing existing QgsVectorLayer {layer.name()}")
                    QgsProject.instance().removeMapLayer(layer.id())
                    layer.setName(layerName)
                    layer.__class__ = cls
                    return layer

        return super().__new__(cls)

    def __new__(cls, *args, **kwargs):
        """Create a new FeatureLayer, or return an existing one if it already exists."""
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, featureType=Feature, sourceType=FeatureLayerSourceType.Memory, layerName=None,
                 gpkgFile=None, styleName=None):
        """Create a new Paddock Power vector layer."""

        self._featureType = featureType
        self.wrapFeature = lambda existingFeature: featureType(self, existingFeature)

        wkbType = featureType.getWkbType()
        schema = featureType.getSchema()

        # If we didn't get an already initialised FeatureLayer from the custom __new__ above …
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

        elif sourceType in [FeatureLayerSourceType.Detect, FeatureLayerSourceType.File]:
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

        self._displayFilter = [FeatureStatus.Drafted, FeatureStatus.Built, FeatureStatus.Planned]
        self._applyDisplayFilter(self._displayFilter)
        self.writeCustomSymbology.connect(self._refreshDisplayFilterFromRenderer)

    @property
    def featureType(self):
        """The Paddock Power Feature type for this layer."""
        return self._featureType

    @property
    def displayFilter(self):
        """The display layer for this layer."""
        return self._displayFilter

    @displayFilter.setter
    def displayFilter(self, filter):
        """Set the display filter for this layer."""
        if self._displayFilter != filter:
            self._displayFilter = filter
            self.displayFilterChanged.emit(self.displayFilter)
            self._applyDisplayFilter(filter)

    def _applyDisplayFilter(self, filter):
        """Toggle the display of a renderer category."""
        renderer = self.renderer()
        if isinstance(renderer, QgsCategorizedSymbolRenderer) and renderer.classAttribute() == 'Status':
            displayed = [status.name for status in filter]
            categories = renderer.categories()
            for category in categories:
                category.setRenderState(category.value() in displayed)
            self.setRenderer(QgsCategorizedSymbolRenderer('Status', categories))
            self.triggerRepaint()

    def _refreshDisplayFilterFromRenderer(self):
        """Refresh the display filter from the renderer."""
        qgsDebug("FeatureLayer._refreshDisplayFilterFromRenderer")
        renderer = self.renderer()
        if isinstance(renderer, QgsCategorizedSymbolRenderer) and renderer.classAttribute() == 'Status':
            values = [category.value() for category in renderer.categories() if category.renderState()]
            statuses = [status for status in FeatureStatus if status.match(*values)]
            self.displayFilter = statuses

    def copyTo(self, otherLayer):
        """Copy all features in this layer to another layer."""
        if otherLayer is None:
            raise Glitch(
                "VectorLayer.copyTo: the target layer is not present")

        if self.featureType != otherLayer.featureType:
            raise Glitch(
                f"Cannot copy features from {self.featureType.displayName()} to {otherLayer.featureType.displayName()}")

        otherLayer.startEditing()
        otherLayer.dataProvider().addFeatures(self.getFeatures())
        otherLayer.commitChanges()

    def addToMap(self, group):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        if group is None:
            raise Glitch(
                "VectorLayer.addToMap: the layer group is not present")

        node = group.findLayer(self.id())
        if node is None:
            group.addLayer(self)
            QgsProject.instance().addMapLayer(self, False)

    def _unwrapQgsFeature(self, feature):
        """Unwrap a Feature into a QgsFeature."""
        if not isinstance(feature, self.featureType):
            raise Glitch(
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
            raise Glitch(
                "{self.__class__.__name__}.copyFeature: the incoming feature is not a {self.featureType.__name__}")

        qgsFeature = self._unwrapQgsFeature(feature)
        copyFeature = self.makeFeature()
        copyQgsFeature = self._unwrapQgsFeature(copyFeature)
        copyQgsFeature.setAttributes(qgsFeature.attributes())
        copyQgsFeature.setGeometry(qgsFeature.geometry())
        copyFeature.clearId()
        return copyFeature

    def addFeature(self, feature):
        """Add a feature to the layer."""
        super().addFeature(self._unwrapQgsFeature(feature))

    def updateFeature(self, feature):
        """Add a feature to the layer."""
        super().updateFeature(self._unwrapQgsFeature(feature))

    def deleteFeature(self, feature):
        """Delete a feature from the layer."""
        super().deleteFeature(feature.id)

    def getFeatures(self, request=None):
        """Get the features in this layer."""
        if request is None:
            return self._wrapQgsFeatures(super().getFeatures())

        if not isinstance(request, QgsFeatureRequest):
            raise Glitch(
                "VectorLayer.getFeatures: the request is not a QgsRequest")

        return self._wrapQgsFeatures(super().getFeatures(request))

    def getFeaturesByStatus(self, *statuses, request=None):
        """Get the features in this layer filtered by one or more FeatureStatus values."""
        if not statuses:
            return self.getFeatures(request)
        return [f for f in self.getFeatures(request) if f.status.match(*statuses)]

    def featureCount(self):
        """Get the number of Features in the layer."""
        return len([f for f in self.getFeatures()])


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
