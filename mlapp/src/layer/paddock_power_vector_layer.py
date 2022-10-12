# -*- coding: utf-8 -*-

from enum import Enum
from qgis.core import QgsProject, QgsVectorLayer, QgsWkbTypes
from qgis.PyQt.QtCore import QVariant

from .paddock_power_layer_source_type import PaddockPowerLayerSourceType
from ..models.paddock_power_error import PaddockPowerError
from ..utils import resolveStylePath

# Couple of lookup dictionaries (locally useful only)
QVARIANT_TYPES = dict([(getattr(QVariant, v), v) for v, m in vars(
    QVariant).items() if type(getattr(QVariant, v)) == QVariant.Type])

QGSWKB_TYPES = dict([(getattr(QgsWkbTypes, v), v) for v, m in vars(
    QgsWkbTypes).items() if type(getattr(QgsWkbTypes, v)) == QgsWkbTypes.Type])

# Paddock Power data is held in the GDA2020 coordinate system
PADDOCK_POWER_EPSG = 7845


class PaddockPowerVectorLayerType(Enum):
    """Enumeration of the types of Paddock Power vector layers."""
    # Note the order of this enumeration can be used to sort map layers for display purposes
    Boundary = 1
    Waterpoint = 2
    Pipeline = 3
    Fence = 4
    Paddock = 5
    LandSystems = 6

    @classmethod
    def guessLayerType(cls, layerName):
        """Guess the type of a Paddock Power vector layer based on the layerName."""
        layerTypeNames = [e.name for e in PaddockPowerVectorLayerType]
        return next(t for t in layerTypeNames if t in layerName)


class PaddockPowerVectorLayer(QgsVectorLayer):
    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None,
                 wkbType=None, schema=None, gpkgFile=None, styleName=None):
        """Create a new Paddock Power vector layer."""

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

# Also: layer.wkbType() is the storage for the "real" WKB geometry type
# By observation:
# * paddocks, boundary, watered areas and land systems are QgsWkbTypes.MultiPolygon
# * fences and pipelines are QgsWkbTypes.LineString
# * water points are QgsWkbTypes.Point
