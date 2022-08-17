# -*- coding: utf-8 -*-

from enum import Enum
from pathlib import Path
from qgis.core import QgsProject, QgsVectorLayer, QgsWkbTypes
from qgis.PyQt.QtCore import QVariant

from ..utils import resolveStylePath

# Couple of lookup dictionaries (locally useful only)
QVARIANT_TYPES = dict([(getattr(QVariant, v), v) for v, m in vars(
    QVariant).items() if type(getattr(QVariant, v)) == QVariant.Type])

QGSWKB_TYPES = dict([(getattr(QgsWkbTypes, v), v) for v, m in vars(
    QgsWkbTypes).items() if type(getattr(QgsWkbTypes, v)) == QgsWkbTypes.Type])

# Paddock Power data is held in the GDA2020 coordinate system
PADDOCK_POWER_EPSG = 7845


class PaddockPowerVectorLayerSourceType(Enum):
    """Disambiguate between sources for a Paddock Power vector layer."""
    File = 1,
    Memory = 2


class PaddockPowerVectorLayerType(Enum):
    """Enumeration of the types of Paddock Power vector layers."""
    # Note the order of this enumeration can be used to sort map layers for display purposes
    Boundary = 1,
    Waterpoint = 2,
    Pipeline = 3,
    Fence = 4,
    Paddock = 5,
    LandSystems = 6

    @classmethod
    def guessLayerType(cls, layerName):
        """Guess the type of a Paddock Power vector layer based on the layerName."""
        layerTypeNames = [e.name for e in PaddockPowerVectorLayerType]
        return next(t for t in layerTypeNames if t in layerName)


class PaddockPowerVectorLayer(QgsVectorLayer):
    def __init__(self, sourceType=PaddockPowerVectorLayerSourceType.Memory, layerName=None,
                 wkbType=None, schema=None, gpkgUrl=None, styleName=None):
        """Create a new Paddock Power vector layer."""

        if sourceType == PaddockPowerVectorLayerSourceType.Memory:
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

        elif sourceType == PaddockPowerVectorLayerSourceType.File:
            assert(gpkgUrl is not None)

            super(PaddockPowerVectorLayer, self).__init__(
                path=gpkgUrl, baseName=None, providerLib="ogr")

        # Optionally apply a style to the layer
        if styleName is not None:
            stylePath = resolveStylePath(styleName)
            self.loadNamedStyle(stylePath)



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
