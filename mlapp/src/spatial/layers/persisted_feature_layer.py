# -*- coding: utf-8 -*-
from os import path

from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsVectorLayer, QgsWkbTypes
import processing

from ...models.glitch import Glitch
from ...utils import PADDOCK_POWER_EPSG, PLUGIN_NAME, qgsDebug, qgsException, qgsInfo
from ..layers.feature_layer import FeatureLayer

QGSWKB_TYPES = dict([(getattr(QgsWkbTypes, v), v) for v, m in vars(
    QgsWkbTypes).items() if isinstance(getattr(QgsWkbTypes, v), QgsWkbTypes.Type)])


class PersistedFeatureLayer(FeatureLayer):

    def detectInGeoPackage(self, workspaceFile, layerName):
        """Detect a matching QgsVectorLayer in a GeoPackage."""
        try:
            layers = QgsVectorLayer(path=workspaceFile, providerLib="ogr")
            if not layers.isValid():
                # GeoPackage file does not yet exist
                return None

            layerNames = [l.split('!!::!!')[1]
                          for l in layers.dataProvider().subLayers()]

            if layerName in layerNames:
                gpkgUrl = f"{workspaceFile}|layername={layerName}"
                layer = QgsVectorLayer(path=gpkgUrl, baseName=layerName, providerLib="ogr")
                if layer.isValid():
                    return True
        except BaseException:
            pass

        return False

    def createInGeoPackage(self, workspaceFile, layerName):

        qgsDebug(f"{self.__class__.__name__}.createInGeoPackage(workspaceFile={workspaceFile}, layerName={layerName})")

        wkbType = self.getWkbType()
        schema = self.getSchema()

        assert layerName and wkbType and schema

        layerDefinition = f"{QGSWKB_TYPES[wkbType]}?crs=epsg:{PADDOCK_POWER_EPSG}"

        layer = QgsVectorLayer(path=layerDefinition, baseName=layerName, providerLib="memory")

        # Have to start editing to get schema updates to stick
        layer.startEditing()
        layer.dataProvider().addAttributes(schema)
        layer.commitChanges()

        # layer.startEditing()

        # for field in self.getSchema():
        #     field.setupLayer(layer)
        # layer.commitChanges()

        params = {
            'LAYERS': [layer],
            'OVERWRITE': not path.exists(workspaceFile),
            'SAVE_STYLES': False,
            'OUTPUT': workspaceFile
        }

        processing.run(
            'native:package', params)

    def deleteFromGeoPackage(self, workspaceFile, layerName):
        """Delete this FeatureLayer from the GeoPackage file."""

        #gpkgUrl = f"{workspaceFile}|layername={layerName}"

        processing.run("native:spatialiteexecutesql", {
            'DATABASE': workspaceFile,
            'SQL': 'drop table {0}'.format(layerName)
        })

    def __init__(self, featureType, workspaceFile, layerName, styleName=None):
        f"""Create a new {PLUGIN_NAME} vector layer."""

        assert featureType
        assert workspaceFile
        assert layerName

        # If not found, create
        if not self.detectInGeoPackage(workspaceFile, layerName):
            qgsInfo(f"{self.__class__.__name__} not found in {PLUGIN_NAME} GeoPackage, creating new …")
            self.createInGeoPackage(workspaceFile, layerName)
        else:
            qgsInfo(f"{self.__class__.__name__} found in {PLUGIN_NAME} GeoPackage, loading …")

        self.gpkgUrl = f"{workspaceFile}|layername={layerName}"

        super().__init__(featureType, self.gpkgUrl, layerName, "ogr", styleName=styleName)

        # TODO
        missingFields, extraFields = self.getSchema().checkFields(self.dataProvider().fields())

        if missingFields:
            # Start editing to to expand the schema
            qgsInfo(
                f"Expanding schema for {self.typeName} to include {str([f.name() for f in missingFields])} …")
            self.startEditing()
            self.dataProvider().addAttributes(missingFields)
            self.commitChanges()

        if extraFields:
            # Start editing to to cut down the schema
            qgsInfo(f"Reducing schema for {self.typeName} to remove {str([f.name() for f in extraFields])} …")
            self.startEditing()
            self.dataProvider().deleteAttributes([self.fields().indexFromName(f.name()) for f in extraFields])
            self.commitChanges()

        # Apply editor widgets and other Field-specific layer setup
        for field in self.getSchema():
            field.setupLayer(self)

    def addFeatures(self, features):
        """Add a batch of features to this layer."""
        for f in features:
            f.clearId()
            self.addFeature(f)

    def copyFeature(self, feature):
        """Copy a feature using the logic (eg dependent layers) of this layer."""
        if not isinstance(feature, self.featureType):
            raise Glitch(
                f"You can't use a {self.typeName} to copy an object that isn't a {self.featureType.__name__}")

        copyFeature = self.makeFeature()
        for f in feature.getSchema():
            copyFeature.setAttribute(f.name(), feature.attribute(f.name()))
        copyFeature.setGeometry(copyFeature.geometry())
        copyFeature.clearId()
        return copyFeature

    def makeFeature(self):
        """Make a new PersistedFeature in this layer."""
        return self.wrapFeature(None)

    # TODO

    def deleteFeature(self, feature):
        """Delete a PersistedFeature from the layer."""
        super().deleteFeature(feature.FID)
