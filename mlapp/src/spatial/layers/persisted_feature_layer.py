# -*- coding: utf-8 -*-
from abc import abstractmethod
from os import path

from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject, QgsVectorLayer, QgsWkbTypes
import processing

from ...models.glitch import Glitch
from ...utils import PADDOCK_POWER_EPSG, PLUGIN_NAME, qgsInfo
from ..features.persisted_feature import Feature
from ..layers.feature_layer import FeatureLayer

QGSWKB_TYPES = dict([(getattr(QgsWkbTypes, v), v) for v, m in vars(
    QgsWkbTypes).items() if isinstance(getattr(QgsWkbTypes, v), QgsWkbTypes.Type)])


class PersistedFeatureLayer(FeatureLayer):

    featuresPersisted = pyqtSignal(list)

    @abstractmethod
    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        pass

    def detectInGeoPackage(self, gpkgFile, layerName):
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

    def createInGeoPackage(self, gpkgFile, layerName):
        featureType = self.getFeatureType()
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

    def deleteFromGeoPackage(self, gpkgFile, layerName):
        """Delete this FeatureLayer from the GeoPackage file."""

        #gpkgUrl = f"{gpkgFile}|layername={layerName}"

        processing.run("native:spatialiteexecutesql", {
            'DATABASE': gpkgFile,
            'SQL': 'drop table {0}'.format(layerName)
        })

    def __init__(self, project, gpkgFile, layerName, styleName=None):
        f"""Create a new {PLUGIN_NAME} vector layer."""

        # If not found, create
        if not self.detectInGeoPackage(gpkgFile, layerName):
            qgsInfo(f"{self.__class__.__name__} not found in {PLUGIN_NAME} GeoPackage. Creating new, stand by …")
            self.createInGeoPackage(gpkgFile, layerName)

        self._gpkgUrl = f"{gpkgFile}|layername={layerName}"
        super().__init__(project, path=self._gpkgUrl, baseName=layerName, providerLib="ogr", styleName=styleName)

        missingFields, extraFields = self.getFeatureType().checkSchema(self.dataProvider().fields())

        if missingFields:
            # Start editing to to expand the schema
            qgsInfo(
                f"Expanding schema for {self.__class__.__name__} to include {str([f.name() for f in missingFields])} …")
            self.startEditing()
            self.dataProvider().addAttributes(missingFields)
            self.commitChanges()

        if extraFields:
            # Start editing to to cut down the schema
            qgsInfo(f"Reducing schema for {self.__class__.__name__} to remove {str([f.name() for f in extraFields])} …")
            self.startEditing()
            self.dataProvider().deleteAttributes([self.fields().indexFromName(f.name()) for f in extraFields])
            self.commitChanges()

        # Apply editor widgets and other Field-specific layer setup
        for field in self.getFeatureType().getSchema():
            field.setupLayer(self)

        self.detectAndRemove()
        QgsProject.instance().addMapLayer(self, False)

    def addFeatures(self, features):
        """Add a batch of features to this layer."""
        for f in features:
            f.clearId()
            self.addFeature(f)

    def copyFeature(self, feature):
        """Copy a feature using the logic (eg dependent layers) of this layer."""
        if not isinstance(feature, self.getFeatureType()):
            raise Glitch(
                "You can't use a {self.__class__.__name__} to copy an object that isn't a {self.getFeatureType().__name__}")

        qgsFeature = self._unwrapQgsFeature(feature)
        copyFeature = self.makeFeature()
        copyQgsFeature = self._unwrapQgsFeature(copyFeature)
        for f in qgsFeature.fields():
            copyQgsFeature.setAttribute(f.name(), qgsFeature.attribute(f.name()))
        copyQgsFeature.setGeometry(qgsFeature.geometry())
        copyFeature.clearId()
        return copyFeature

    def makeFeature(self):
        """Make a new PersistedFeature in this layer."""
        return self.wrapFeature(None)

    def addFeature(self, feature):
        """Add a PersistedFeature to the layer."""
        super().addFeature(self._unwrapQgsFeature(feature))

    def updateFeature(self, feature):
        """Update a PersistedFeature in the layer."""
        super().updateFeature(self._unwrapQgsFeature(feature))

    def deleteFeature(self, feature):
        """Delete a PersistedFeature from the layer."""
        super().deleteFeature(feature.id)


# Helper functions - used to convert QgsField objects to code in the console as below

# QVARIANT_TYPES = dict([(getattr(QVariant, v), v) for v, m in vars(
#     QVariant).items() if isinstance(getattr(QVariant, v), QVariant.Type)])

# def dumpQgsFieldConstructorStatement(field):
#     """Print a QgsField constructor statement for the given QgsField object."""
# return f"Field(propertyName="", name=\"{field.name()}\",
# type=QVariant.{QVARIANT_TYPES[field.type()]},
# typeName=\"{field.typeName()}\", len={field.length()},
# prec={field.precision()}, comment=\"{field.comment()}\",
# subType=QVariant.{QVARIANT_TYPES[field.subType()]})"


# def dumpQgsFields(fields):
#     """Print a list of QgsField constructor statements for the given QgsFields object."""
#     for field in fields.toList():
#         print(dumpQgsFieldConstructorStatement(field), ",")


# def dumpLayerFieldsByName(layerName):
#     """Match a map layer by name and dump all its fields as above."""
#     project = QgsProject.instance()
#     layer = project.mapLayersByName(layerName)[0]
#     dumpQgsFields(layer.fields())
