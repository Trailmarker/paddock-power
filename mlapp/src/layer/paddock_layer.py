# -*- coding: utf-8 -*-
from qgis.core import (QgsField, QgsGeometry, QgsLineString, QgsPoint,
                       QgsWkbTypes)
from qgis.PyQt.QtCore import QVariant

from .paddock_power_vector_layer import (PaddockPowerLayerSourceType,
                                         PaddockPowerVectorLayer,
                                         PaddockPowerVectorLayerType)


class PaddockLayer(PaddockPowerVectorLayer):

    SCHEMA = [
        QgsField(name="Paddock Name", type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Paddock Area (km²)", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Paddock Perimeter (km)", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Status", type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
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

    def whileEditing(self, func):
        """Run a function with the layer in edit mode."""
        isEditing = self.isEditable()

        if not isEditing:
            self.startEditing()
            func()
            self.commitChanges()
        else:
            func()
            self.commitChanges()
            self.startEditing()

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
                splitPaddock.setAttribute(
                    "Status", "New")
                self.updateFeature(splitPaddock)

        self.commitChanges()

    def updatePaddockFeature(self, paddockFeature):
        """Update a paddock feature."""
        self.whileEditing(lambda: self.updateFeature(paddockFeature))

    def updatePaddockFeature(self, paddockFeature, paddockName):
        """Update a paddock feature's name."""
        paddockFeature.setAttribute("Paddock Name", paddockName)
        self.updatePaddockFeature(paddockFeature)

        
