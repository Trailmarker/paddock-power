# -*- coding: utf-8 -*-
from os import path

from qgis.core import QgsVectorLayer, QgsWkbTypes
import processing

from ..models import Glitch
from ..utils import PADDOCK_POWER_EPSG, PLUGIN_NAME, qgsInfo
from .features import Edits
from .feature_layer import FeatureLayer
from .interfaces import IPersistedFeatureLayer

QGSWKB_TYPES = dict([(getattr(QgsWkbTypes, v), v) for v, m in vars(
    QgsWkbTypes).items() if isinstance(getattr(QgsWkbTypes, v), QgsWkbTypes.Type)])


class PersistedFeatureLayer(FeatureLayer, IPersistedFeatureLayer):

    def detectInStore(self, workspaceFile, layerName):
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

    def createInStore(self, workspaceFile, layerName):

        wkbType = self.getWkbType()
        schema = self.getSchema()

        assert layerName and wkbType and schema

        layerDefinition = f"{QGSWKB_TYPES[wkbType]}?crs=epsg:{PADDOCK_POWER_EPSG}"

        layer = QgsVectorLayer(path=layerDefinition, baseName=layerName, providerLib="memory")

        # Have to start editing to get schema updates to stick
        layer.startEditing()
        layer.dataProvider().addAttributes(schema)
        layer.commitChanges()

        params = {
            'LAYERS': [layer],
            'OVERWRITE': not path.exists(workspaceFile),
            'SAVE_STYLES': False,
            'OUTPUT': workspaceFile
        }

        processing.run(
            'native:package', params)
        
        # options = QgsVectorFileWriter.SaveVectorOptions()
        # options.driverName = "GPKG"
        # options.fileEncoding = 'cp1251'
        # options.layerName = layerName

        # fileWriter = QgsVectorFileWriter.create(
        #     fileName=workspaceFile,
        #     fields=schema.toQgsFields(),
        #     geometryType=wkbType,
        #     srs=QgsCoordinateReferenceSystem(f"EPSG:{PADDOCK_POWER_EPSG}"),
        #     transformContext=QgsProject.instance().transformContext(),
        #     options=options)
        # del fileWriter 

    def deleteFromStore(self, workspaceFile, layerName):
        """Delete this FeatureLayer from the GeoPackage file."""

        # gpkgUrl = f"{workspaceFile}|layername={layerName}"

        processing.run("native:spatialiteexecutesql", {
            'DATABASE': workspaceFile,
            'SQL': 'drop table {0}'.format(layerName)
        })

    def __init__(self, workspaceFile, layerName, styleName=None):
        f"""Create a new {PLUGIN_NAME} vector layer."""

        assert workspaceFile
        assert layerName

        self._taskId = None
        self._task = None

        # If not found, create
        if not self.detectInStore(workspaceFile, layerName):
            qgsInfo(f"{layerName} not found in {PLUGIN_NAME} GeoPackage, creating new …")
            self.createInStore(workspaceFile, layerName)

        self.gpkgUrl = f"{workspaceFile}|layername={layerName}"

        super().__init__(self.gpkgUrl, layerName, "ogr", styleName=styleName)

        # TODO
        missingFields, extraFields = self.getSchema().checkFields(self.dataProvider().fields())

        if missingFields:
            # Start editing to to expand the schema
            qgsInfo(
                f"Expanding schema for {type(self).__name__} to include {str([f.name() for f in missingFields])} …")
            self.startEditing()
            self.dataProvider().addAttributes(missingFields)
            self.commitChanges()

        if extraFields:
            # Start editing to to cut down the schema
            qgsInfo(f"Reducing schema for {type(self).__name__} to remove {str([f.name() for f in extraFields])} …")
            self.startEditing()
            self.dataProvider().deleteAttributes([self.fields().indexFromName(f.name()) for f in extraFields])
            self.commitChanges()

        # Apply editor widgets and other Field-specific layer setup
        for field in self.getSchema():
            field.setupLayer(self)

        self.addInBackground()

    def addFeatures(self, features):
        """Add a batch of features to this layer."""
        for f in features:
            self.addFeature(f)

    def copyFeature(self, feature):
        """Copy a feature using the logic (eg dependent layers) of this layer."""
        if not self.getSchema().containsSchema(feature.getSchema()):
            raise Glitch(
                f"{type(self).__name__}.copyFeature({feature}): {type(self).__name__}.getSchema().containsSchema({type(feature).__name__}.getSchema()) is False")
        copy = self.wrapFeature(feature)
        copy.FID = -1
        return copy

    def makeFeature(self):
        """Make a new PersistedFeature in this layer."""
        return self.wrapFeature(None)

    def deleteFeature(self, feature):
        """Delete a PersistedFeature from the layer."""
        super().deleteFeature(feature.FID)

    def recalculateFeatures(self, raiseErrorIfTaskHasBeenCancelled=lambda: None):
        """Recalculate features in this layer."""
        edits = Edits()

        qgsInfo(f"Recalculating {self.name()} …")

        for feature in self.getFeatures():
            raiseErrorIfTaskHasBeenCancelled()
            feature.recalculate()
            edits.editBefore(Edits.upsert(feature))

        return edits
