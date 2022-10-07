# -*- coding: utf-8 -*-
from qgis.core import QgsFeature, QgsField, QgsFields, QgsGeometry, QgsLineString, QgsPoint, QgsWkbTypes
from qgis.PyQt.QtCore import QVariant

from .paddock_power_vector_layer import (PaddockPowerVectorLayer,
                                         PaddockPowerLayerSourceType,
                                         PaddockPowerVectorLayerType)


class PaddockLayer(PaddockPowerVectorLayer):

    SCHEMA = [
        QgsField(name="Paddock Name", type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Paddock Area (km²)", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Paddock Perimeter (km)", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
    ]

    STYLE = "paddock"

    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Paddock layer."""

        super(PaddockLayer, self).__init__(sourceType,
                                           layerName,
                                           QgsWkbTypes.MultiPolygon,
                                           self.SCHEMA,
                                           gpkgFile,
                                           styleName=self.STYLE)

    def getLayerType(self):
        """Return the Paddock Power layer type."""
        return PaddockPowerVectorLayerType.Paddock

    def crossedPaddocks(self, splitLine):
        """Return a tuple, a list of paddocks 'fully crossed' by a splitting line and a crop of the
           splitting line to the crossed paddocks."""
        intersects = [p for p in self.getFeatures(
        ) if splitLine.intersects(p.geometry())]
        crossed = []
        for paddock in intersects:
            polygon = paddock.geometry().asMultiPolygon()
            boundaryLine = QgsGeometry.fromMultiPolylineXY(polygon[0])
            intersection = boundaryLine.intersection(splitLine)
            if intersection.isMultipart():
                crossed.append(paddock)

        allCrossed = QgsGeometry.unaryUnion(f.geometry() for f in crossed)
        cropped = splitLine.intersection(allCrossed)

        return (crossed, cropped)

    def splitPaddocks(self, fenceLine):
        """Split paddocks by a line and update the layer."""
        crossedPaddocks, _ = self.crossedPaddocks(fenceLine)

        self.startEditing()

        crossedPaddockNames = [crossedPaddock['Paddock Name']
                               for crossedPaddock in crossedPaddocks]

        # Split all the relevant features—this should split every element in crossed
        fixedSplitLine = QgsLineString(
            [QgsPoint(p.x(), p.y()) for p in fenceLine.asPolyline()])

        self.splitFeatures(fixedSplitLine, False, False)

        for crossedPaddockName in crossedPaddockNames:
            splitPaddocks = [p for p in self.getFeatures(
            ) if p['Paddock Name'] == crossedPaddockName]

            for i, splitPaddock in enumerate(splitPaddocks):
                splitPaddock.setAttribute(
                    "Paddock Name", crossedPaddockName + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i])
                self.updateFeature(splitPaddock)

        self.commitChanges()

    # def splitPaddocks(self, splitLine):
    #     """Split paddocks 'fully crossed' by a line and update the layer."""
    #     crossed = self.crossedPaddocks(splitLine)

    #     self.startEditing()

    #     for paddock in crossed:
    #         paddockName = paddock.attribute("Paddock Name")

    #         # TODO splitGeometry is not working as expected / is deprecated
    #         result, splitGeometries, _ = paddock.geometry().splitGeometry(splitLine.asPolyline(), False)

    #         if result == QgsGeometry.OperationResult.Success:
    #             for i, geometry in enumerate(splitGeometries):
    #                 feature = QgsFeature(self.fields())
    #                 feature.setAttributes(paddock.attributes())
    #                 feature.setAttribute("Paddock Name", paddockName + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i])
    #                 feature.setAttribute("fid", 0)
    #                 feature.setGeometry(geometry)

    #                 self.addFeature(feature)

    #             self.deleteFeature(paddock.id())

    #     self.commitChanges()
