# -*- coding: utf-8 -*-
from os import path

from qgis.PyQt.QtCore import QVariant, pyqtSignal

from qgis.core import QgsCategorizedSymbolRenderer, QgsFeatureRequest, QgsProject, QgsVectorLayer, QgsWkbTypes
import processing

from ...models.glitch import Glitch
from ...utils import resolveStylePath, qgsDebug
from ..features.feature import Feature
from ..features.feature_status import FeatureStatus

# Couple of lookup dictionaries (locally useful only)
QVARIANT_TYPES = dict([(getattr(QVariant, v), v) for v, m in vars(
    QVariant).items() if isinstance(getattr(QVariant, v), QVariant.Type)])

QGSWKB_TYPES = dict([(getattr(QgsWkbTypes, v), v) for v, m in vars(
    QgsWkbTypes).items() if isinstance(getattr(QgsWkbTypes, v), QgsWkbTypes.Type)])

# Paddock Power data is held in the GDA2020 coordinate system
PADDOCK_POWER_EPSG = 7845


class FeatureLayer(QgsVectorLayer):

    displayFilterChanged = pyqtSignal(list)

    @classmethod
    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return Feature

    @classmethod
    def detectAndRemove(cls, gpkgFile, layerName):
        """Detect if a layer is already in the map, and if so, return it."""
        gpkgUrl = f"{gpkgFile}|layername={layerName}"

        layers = [l for l in QgsProject.instance().mapLayers().values()]
        for layer in layers:
            if layer.source() == gpkgUrl:
                QgsProject.instance().removeMapLayer(layer.id())

    @classmethod
    def detectInGeoPackage(cls, gpkgFile, layerName):
        """Detect a matching QgsVectorLayer in a GeoPackage."""
        try:
            layers = QgsVectorLayer(path=gpkgFile, providerLib="ogr")
            if not layers.isValid():
                # GeoPackage file does not yet exist
                return None

            layerNames = [l.split('!!::!!')[1]
                          for l in layers.dataProvider().subLayers()]

            if layerName in layerNames:
                gpkgUrl = f"{gpkgFile}|layername={layerName}"
                layer = QgsVectorLayer(path=gpkgUrl, baseName=layerName, providerLib="ogr")
                if layer.isValid():
                    return True
        except BaseException:
            pass

        return False

    @classmethod
    def createInGeoPackage(cls, gpkgFile, layerName):
        featureType = cls.getFeatureType()
        wkbType = featureType.getWkbType()
        schema = featureType.getSchema()

        assert(layerName is not None)
        assert(wkbType is not None)
        assert(schema is not None)

        layerDefinition = f"{QGSWKB_TYPES[wkbType]}?crs=epsg:{PADDOCK_POWER_EPSG}"

        layer = QgsVectorLayer(path=layerDefinition, baseName=layerName, providerLib="memory")

        # Have to start editing to get schema updates to stick
        layer.startEditing()
        layer.dataProvider().addAttributes(schema)
        layer.commitChanges()

        params = {
            'LAYERS': [layer],
            'OVERWRITE': not path.exists(gpkgFile),
            'SAVE_STYLES': False,
            'OUTPUT': gpkgFile
        }

        processing.run(
            'native:package', params)

    def deleteFromGeoPackage(cls, gpkgFile, layerName):
        """Delete this FeatureLayer from the GeoPackage file."""

        #gpkgUrl = f"{gpkgFile}|layername={layerName}"

        processing.run("native:spatialiteexecutesql", {
            'DATABASE': gpkgFile,
            'SQL': 'drop table {0}'.format(layerName)
        })

    def __init__(self, gpkgFile, layerName, styleName=None):
        """Create a new Paddock Power vector layer."""

        # If not found, create
        if not self.detectInGeoPackage(gpkgFile, layerName):
            qgsDebug(f"{self.__class__.__name__} not found in Paddock Power GeoPackage. Creating new, stand by …")
            self.createInGeoPackage(gpkgFile, layerName)

        self._gpkgUrl = f"{gpkgFile}|layername={layerName}"
        super().__init__(path=self._gpkgUrl, baseName=layerName, providerLib="ogr")

        # Optionally apply a style to the layer
        if styleName is not None:
            stylePath = resolveStylePath(styleName)
            self.loadNamedStyle(stylePath)

        # Apply editor widgets
        schema = self.getFeatureType().getSchema()

        for field in schema:
            fieldIndex = self.fields().indexFromName(field.name())
            self.setEditorWidgetSetup(fieldIndex, field.editorWidgetSetup())
            self.setDefaultValueDefinition(fieldIndex, field.defaultValueDefinition())

        self.detectAndRemove(gpkgFile, layerName)

        QgsProject.instance().addMapLayer(self, False)

        self._displayFilter = [FeatureStatus.Drafted, FeatureStatus.Built, FeatureStatus.Planned]
        self._applyDisplayFilter(self.displayFilter)
        self.writeCustomSymbology.connect(self._refreshDisplayFilterFromRenderer)

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, feature)

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
        # qgsDebug("FeatureLayer._refreshDisplayFilterFromRenderer")
        renderer = self.renderer()
        if isinstance(renderer, QgsCategorizedSymbolRenderer) and renderer.classAttribute() == 'Status':
            values = [category.value() for category in renderer.categories() if category.renderState()]
            statuses = [status for status in FeatureStatus if status.match(*values)]
            self.displayFilter = statuses

    def copyTo(self, otherLayer):
        """Copy all features in this layer to another layer."""
        if otherLayer is None:
            raise Glitch(
                "FeatureLayer.copyTo: the target layer is not present")

        if self.getFeatureType() != otherLayer.getFeatureType():
            raise Glitch(
                f"Cannot copy features from {self.getFeatureType().displayName()} to {otherLayer.getFeatureType().displayName()}")

        otherLayer.startEditing()
        otherLayer.dataProvider().addFeatures(self.getFeatures())
        otherLayer.commitChanges()

    def addToMap(self, group):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        if group is None:
            raise Glitch(
                "FeatureLayer.addToMap: the layer group is not present")

        group.addLayer(self)

    def removeFromMap(self, group):
        node = group.findLayer(self.id())
        if node:
            group.removeChildNode(node)

    def _unwrapQgsFeature(self, feature):
        """Unwrap a Feature into a QgsFeature."""
        if not isinstance(feature, self.getFeatureType()):
            raise Glitch(
                f"FeatureLayer.__unwrapQgsFeature: the feature is not a {self.getFeatureType().__name__}")
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
        if not isinstance(feature, self.getFeatureType()):
            raise Glitch(
                "You can't use a {self.__class__.__name__} to copy an object that isn't a {self.getFeatureType().__name__}")

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

    def getFeatureById(self, id):
        """Get a feature by its ID."""
        qgsFeature = super().getFeature(id)

        if qgsFeature is not None:
            feature = self.wrapFeature(qgsFeature)
            return feature if feature.status.match(*self.displayFilter) else None

    def getFeatures(self, request=None):
        """Get the features in this layer."""
        if request is None:
            return self._wrapQgsFeatures(super().getFeatures())

        if not isinstance(request, QgsFeatureRequest):
            raise Glitch(
                "FeatureLayer.getFeatures: the request is not a QgsRequest")

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
