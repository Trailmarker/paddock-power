# -*- coding: utf-8 -*-
from qgis.core import (QgsFeature, QgsField, QgsGeometry, QgsLineString, QgsPoint,
                       QgsWkbTypes)
from qgis.PyQt.QtCore import QVariant

from .paddock import Paddock, makePaddock
from .paddock_power_vector_layer import (PaddockPowerLayerSourceType,
                                         PaddockPowerVectorLayer,
                                         PaddockPowerVectorLayerType)


class PaddockLayer(PaddockPowerVectorLayer):

    STYLE = "paddock"

    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Paddock layer."""

        super(PaddockLayer, self).__init__(sourceType,
                                           layerName,
                                           QgsWkbTypes.MultiPolygon,
                                           Paddock.SCHEMA,
                                           gpkgFile,
                                           styleName=self.STYLE)
        # Convert all QGIS features to Paddocks
        self.setFeatureAdapter(makePaddock)

    def getLayerType(self):
        """Return the Paddock Power layer type."""
        return PaddockPowerVectorLayerType.Paddock

    def planFenceLine(self, fenceLine):
        """Return a tuple consisting of a cropped fence geometry, a list of existing paddocks 'fully crossed' by the cropped fence geometry,
           and a list of planned paddocks resulting from splitting the paddocks using the cropped fence geometry."""

        intersects = [p for p in self.getFeatures(
        ) if fenceLine.intersects(p.geometry())]

        # Find the existing paddocks crossed by the fence line
        existingPaddocks = []
        for paddock in intersects:
            polygon = paddock.geometry().asMultiPolygon()
            boundaryLine = QgsGeometry.fromMultiPolylineXY(polygon[0])
            intersection = boundaryLine.intersection(fenceLine)
            if intersection.isMultipart():
                # Deep copy the crossed paddocks
                existingPaddocks.append(QgsFeature(paddock))

        # Crop the fence line to these existing paddocks - no loose ends
        allExisting = QgsGeometry.unaryUnion(
            f.geometry() for f in existingPaddocks)
        normalisedFenceLine = fenceLine.intersection(allExisting)

        fixedFenceLine = QgsLineString(
            [QgsPoint(p.x(), p.y()) for p in normalisedFenceLine.asPolyline()])

        # Use editing mode temporarily to derive the split paddocks
        self.startEditing()
        self.splitFeatures(fixedFenceLine, False, False)

        crossedPaddockNames = [crossedPaddock['Paddock Name']
                               for crossedPaddock in existingPaddocks]
        plannedPaddocks = []
        for crossedPaddockName in crossedPaddockNames:
            # Deep copy the split paddocks
            splitPaddocks = [QgsFeature(p) for p in self.getFeatures(
            ) if p['Paddock Name'] == crossedPaddockName]

            for i, splitPaddock in enumerate(splitPaddocks):
                splitPaddock.setAttribute(
                    "Paddock Name", crossedPaddockName + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i])
                splitPaddock.setAttribute(
                    "Status", "Planned")
                # self.updateFeature(splitPaddock)
            plannedPaddocks.append(splitPaddocks)

        # roll back all these edits
        self.rollBack()

        return (normalisedFenceLine, existingPaddocks, plannedPaddocks)

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
        crossedPaddocks, _ = self.planFence(fenceLine)

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

    def updatePaddock(self, paddockFeature):
        """Update a paddock feature."""
        self.whileEditing(lambda: self.updateFeature(paddockFeature))

    def updatePaddockName(self, paddockFeature, paddockName):
        """Update a paddock feature's name."""
        paddockFeature.setPaddockName(paddockName)
        self.updatePaddock(paddockFeature)
