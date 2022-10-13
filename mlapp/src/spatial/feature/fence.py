# -*- coding: utf-8 -*-
from qgis.core import (QgsFeature, QgsField, QgsFields,
                       QgsGeometry, QgsLineString, QgsPoint)
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature

from ...models.paddock_power_error import PaddockPowerError
from ...utils import qgsDebug
from ..calculator import Calculator
from .feature import Feature
from .feature_status import FeatureStatus
from .line_feature import LineFeature
from .paddock import asPaddock


class Fence(LineFeature):
    BUILD_ORDER, LENGTH, STATUS = ["Build Order",
                                   LineFeature.LENGTH,
                                   Feature.STATUS]

    SCHEMA = [
        QgsField(name=BUILD_ORDER, type=QVariant.LongLong, typeName="Integer64",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=LENGTH, type=QVariant.Double, typeName="Real",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=STATUS, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def __init__(self):
        super().__init__()

        # Cache the length profile
        self.profile = None

    def fenceBuildOrder(self):
        return self[Fence.BUILD_ORDER]

    def setFenceBuildOrder(self, buildOrder):
        self.setAttribute(Fence.BUILD_ORDER, buildOrder)

    def getProfile(self):
        return self.profile

    def recalculate(self, elevationLayer=None):
        """Recalculate the length of this Fence."""
        self.profile = Calculator.calculateProfile(self.geometry(), elevationLayer)
        length = round(self.profile.maximumDistance, 2)
        self.setAttribute(Fence.LENGTH, length)

    def planFence(self, paddockLayer):
        """Return a tuple consisting of a normalised fence geometry, a list of superseded paddocks 'fully crossed' by the cropped fence geometry,
           and a list of planned paddocks resulting from splitting the paddocks using the cropped fence geometry."""

        fenceLine = self.geometry()

        intersects = [p for p in paddockLayer.getFeatures(
        ) if fenceLine.intersects(p.geometry())]

        # Find the existing paddocks crossed by the fence line that will be superseded
        supersededPaddocks = []
        for paddock in intersects:
            polygon = paddock.geometry().asMultiPolygon()
            boundaryLine = QgsGeometry.fromMultiPolylineXY(polygon[0])
            intersection = boundaryLine.intersection(fenceLine)
            if intersection.isMultipart():
                # Deep copy the crossed paddocks
                supersededPaddocks.append(asPaddock(QgsFeature(paddock)))

        # Crop the fence line to these superseded paddocks - no loose ends
        allExisting = QgsGeometry.unaryUnion(
            f.geometry() for f in supersededPaddocks)
        normalisedFenceLine = fenceLine.intersection(allExisting)

        if normalisedFenceLine.isEmpty():
            return fenceLine, [], []

        # If this leaves the fence line multipart, reduce it to a single part
        if normalisedFenceLine.isMultipart():
            normalisedFenceLine = normalisedFenceLine.combine()

        if normalisedFenceLine.isMultipart():
            raise PaddockPowerError(
                "Fence.analyseFence: fence line is still multipart")

        # Set this fence's geometry to the normalised output
        self.setGeometry(normalisedFenceLine)

        splitLine = QgsLineString(
            [QgsPoint(p.x(), p.y()) for p in normalisedFenceLine.asPolyline()])

        # Use editing mode temporarily to derive the split paddocks
        paddockLayer.startEditing()
        paddockLayer.splitFeatures(splitLine, False, False)

        plannedPaddocks = []
        for crossedPaddock in supersededPaddocks:
            # This paddock would be superseded by the split
            crossedPaddock.setStatus(FeatureStatus.Superseded)
            paddockLayer.updatePaddock(crossedPaddock)

            crossedPaddockName = crossedPaddock.paddockName()

            # Deep copy the split paddocks
            splitPaddocks = [asPaddock(QgsFeature(p)) for p in paddockLayer.getFeatures(
            ) if p['Paddock Name'] == crossedPaddockName]

            for i, splitPaddock in enumerate(splitPaddocks):
                splitPaddock.setPaddockName(
                    crossedPaddockName + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i])
                splitPaddock.setStatus(FeatureStatus.Planned)
                splitPaddock.recalculate()
                # paddockLayer.updatePaddock(splitPaddock)
                plannedPaddocks.append(splitPaddock)

        # roll back all these edits
        paddockLayer.commitChanges()

        return (normalisedFenceLine, supersededPaddocks, plannedPaddocks)

FenceFeature = type('FenceFeature', (Fence, QgsFeature), {})

def asFence(feature):
    """Return a Fence object from a QgsFeature."""
    if not isinstance(feature, QgsFeature):
        qgsDebug(f"feature: {str(feature)}")
        qgsDebug(f"feature.__class__.__name__: {feature.__class__.__name__}")
        raise PaddockPowerError("asFence: feature is not a QgsFeature")
    if not isinstance(feature, Fence):
        feature.__class__ = FenceFeature
    if not hasattr(feature, 'profile'):
        setattr(feature, 'profile', None)
    return feature

def makeFence():
    """Return a new and empty Fence object."""
    fields = QgsFields()
    for field in Fence.SCHEMA:
        fields.append(field)

    feature = QgsFeature(fields)
    return asFence(feature)
