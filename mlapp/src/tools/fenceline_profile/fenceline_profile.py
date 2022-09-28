# -*- coding: utf-8 -*-
from math import hypot

from shapely.wkb import loads
from shapely.wkt import dumps

from qgis.core import QgsCoordinateReferenceSystem, QgsDistanceArea, QgsGeometry, QgsPoint, QgsPointXY, QgsProject, QgsRaster

from qgis.PyQt.QtCore import QObject

from ...layer.elevation_layer import ElevationLayer
from ...models.milestone import PaddockPowerError
from ...utils import qgsDebug


class FencelineProfile(QObject):
    def __init__(self, fenceline, elevationLayer):

        super(FencelineProfile, self).__init__()

        if not isinstance(fenceline, QgsGeometry):
            raise PaddockPowerError(
                "FencelineData.__init__: fenceline is not a QgsGeometry.")

        if not isinstance(elevationLayer, ElevationLayer):
            raise PaddockPowerError(
                "FencelineData.__init__: elevationLayer is not an ElevationLayer.")

        self.fenceline = fenceline
        self.elevationLayer = elevationLayer

        self.analyseFenceline()

    def analyseFenceline(self):
        """Update the fenceline data."""

        # Get points along line at the granularity of the project elevation layer, using Shapely
        fencelineLength = self.fenceline.length()
        shapelyFenceline = loads(bytes(self.fenceline.asWkb()))

        elevationLayerCellSize = self.elevationLayer.rasterUnitsPerPixelX()

        currentDistanceAlongFenceline = elevationLayerCellSize
        pointsAlongFenceline = []

        while currentDistanceAlongFenceline < fencelineLength:
            shapelyPoint = shapelyFenceline.interpolate(
                currentDistanceAlongFenceline)
            point = QgsGeometry.fromWkt(dumps(shapelyPoint)).asPoint()
            pointsAlongFenceline.append(point)
            currentDistanceAlongFenceline = currentDistanceAlongFenceline + elevationLayerCellSize

        # Add Z values to points along line
        dataProvider = self.elevationLayer.dataProvider()

        pointsWithZ = [QgsPoint(point.x(), point.y(), dataProvider.identify(
            point, QgsRaster.IdentifyFormatValue).results()[1]) for point in pointsAlongFenceline]

        # Calculate distances along line using the GDA2020 ellipsoid
        pointPairs = zip(pointsWithZ, pointsWithZ[1:])
        calculator = QgsDistanceArea()

        calculator.setSourceCrs(QgsCoordinateReferenceSystem(
            'EPSG:7845'), QgsProject.instance().transformContext())
        # See QgsCoordinateReferenceSystem('EPSG:7844').ellipsoidAcronym()
        calculator.setEllipsoid('EPSG:7019')

        cumulativeDistances = [0.0]

        for p1, p2 in pointPairs:
            if p1 is None or p2 is None:
                break

            # Calculate the ellipsoidal ground distance
            groundDistance = calculator.measureLine(
                QgsPointXY(p1.x(), p1.y()), QgsPointXY(p2.x(), p2.y()))

            # Elevation variation
            elevationVariation = p2.z() - p1.z()

            # Pythagoras
            cumulativeDistances.append(
                cumulativeDistances[-1] + hypot(groundDistance, elevationVariation))

        # Store the profile data
        self.distances = cumulativeDistances
        self.elevations = [point.z() for point in pointsWithZ]

        qgsDebug(str(self.distances))
        qgsDebug(str(self.elevations))

        self.minimumElevation = round(min(self.elevations), 1)
        self.maximumElevation = round(max(self.elevations), 1)
        self.meanElevation = round(
            sum(self.elevations) / len(self.elevations), 1)

        self.maximumDistance = self.distances[-1]
