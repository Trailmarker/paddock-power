# -*- coding: utf-8 -*-
from math import hypot, isnan, isinf

from shapely.wkb import loads
from shapely.wkt import dumps

from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsDistanceArea, QgsGeometry, QgsPoint, QgsPointXY, QgsProject, QgsRaster

from ..utils import PLUGIN_NAME
from ..models import Glitch
from .elevation_profile import ElevationProfile


def makeDistanceAreaCalculator():
    """Return a QgsDistanceArea object with the correct settings for the workspace."""
    calculator = QgsDistanceArea()
    calculator.setSourceCrs(QgsCoordinateReferenceSystem(
        'EPSG:7845'), QgsProject.instance().transformContext())
    # See QgsCoordinateReferenceSystem('EPSG:7844').ellipsoidAcronym()
    calculator.setEllipsoid('EPSG:7019')
    return calculator


class Calculator:
    MINIMUM_PLANAR_AREA_M2 = 10.0  # 10 m² is the smallest analytic area we care about
    QGIS_CALCULATOR = makeDistanceAreaCalculator()

    @staticmethod
    def calculateElevationAtPoint(point, elevationLayer=None):
        if elevationLayer is None:
            return 0.0

        if not isinstance(point, QgsGeometry):
            raise Glitch(
                "Calculator.calculateElevationAtPoint: point is not a QgsGeometry.")

        try:
            pointXY = point.asPoint()
            dataProvider = elevationLayer.dataProvider()
            return dataProvider.identify(pointXY, QgsRaster.IdentifyFormatValue).results()[1]
        except Exception:
            return 0.0

    @staticmethod
    def calculateLongitudeAndLatitudeAtPoint(point):
        if not isinstance(point, QgsGeometry):
            raise Glitch(
                "Calculator.calculateCoordinatesAtPoint: point is not a QgsGeometry.")

        copy = QgsGeometry(point)

        destCrs = QgsCoordinateReferenceSystem('EPSG:7844')
        sourceCrs = QgsCoordinateReferenceSystem('EPSG:7845')
        transform = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())
        copy.transform(transform)

        outputPoint = copy.asPoint()
        return (outputPoint.x(), outputPoint.y())

    @staticmethod
    def calculateProfile(line, elevationLayer=None):
        """Calculate the length of a line."""

        if not isinstance(line, QgsGeometry):
            raise Glitch(
                "Calculator.calculateLength: line is not a QgsGeometry.")

        if line.isMultipart():
            raise Glitch(
                f"Calculator.calculateArea: {PLUGIN_NAME} should not be used with multi-part linestrings.")

        calculator = Calculator.QGIS_CALCULATOR

        calculator.setSourceCrs(QgsCoordinateReferenceSystem(
            'EPSG:7845'), QgsProject.instance().transformContext())
        # See QgsCoordinateReferenceSystem('EPSG:7844').ellipsoidAcronym()
        calculator.setEllipsoid('EPSG:7019')

        distances = [0.0]
        elevations = []

        if elevationLayer is None:
            calculator = QgsDistanceArea()
            points = line.asPolyline()

            # Calculate distances along line using the GDA2020 ellipsoid
            pointPairs = zip(points, points[1:])

            for p1, p2 in pointPairs:
                if p1 is None or p2 is None:
                    break

                # Calculate the ellipsoidal ground distance
                groundDistance = calculator.measureLine(p1, p2)
                distances.append(distances[-1] + groundDistance)

            elevations = [0.0 for point in points]

        else:
            # Get points along line at the granularity of the workspace elevation layer, using Shapely
            lineLength = line.length()
            shapelyLine = loads(
                bytes(line.asWkb()))

            elevationLayerCellSize = elevationLayer.rasterUnitsPerPixelX()

            currentDistanceAlongLine = elevationLayerCellSize
            pointsAlongLine = []

            while currentDistanceAlongLine < lineLength:
                shapelyPoint = shapelyLine.interpolate(
                    currentDistanceAlongLine)
                point = QgsGeometry.fromWkt(dumps(shapelyPoint)).asPoint()
                pointsAlongLine.append(point)
                currentDistanceAlongLine = currentDistanceAlongLine + elevationLayerCellSize

            # Add Z values to points along line
            dataProvider = elevationLayer.dataProvider()

            pointsWithZ = []
            for point in pointsAlongLine:
                elevation = 0.0
                try:
                    pointXY = point.asPoint()
                    dataProvider = elevationLayer.dataProvider()
                    elevation = dataProvider.identify(pointXY, QgsRaster.IdentifyFormatValue).results()[1]
                except Exception:
                    pass
                pointsWithZ.append(QgsPoint(point.x(), point.y(), elevation))

            # Calculate distances along line using the GDA2020 ellipsoid
            pointPairs = zip(pointsWithZ, pointsWithZ[1:])

            for p1, p2 in pointPairs:
                if p1 is None or p2 is None:
                    break

                # Calculate the ellipsoidal ground distance
                groundDistance = calculator.measureLine(
                    QgsPointXY(p1.x(), p1.y()), QgsPointXY(p2.x(), p2.y()))

                # Elevation variation
                elevationVariation = p2.z() - p1.z()

                # Pythagoras
                distances.append(
                    distances[-1] + hypot(groundDistance, elevationVariation))

            elevations = [point.z() for point in pointsWithZ]

        # Clean up bad values (caused eg by points outside the elevation layer)
        elevations = [(z if not isnan(z) and not isinf(z) else 0.0) for z in elevations]

        minimumElevation = round(min(elevations), 1)
        maximumElevation = round(max(elevations), 1)
        meanElevation = round(
            sum(elevations) / len(elevations), 1)

        maximumDistance = distances[-1]

        return ElevationProfile(maximumDistance=maximumDistance,
                                distances=distances,
                                elevations=elevations,
                                minimumElevation=minimumElevation,
                                maximumElevation=maximumElevation,
                                meanElevation=meanElevation)

    @staticmethod
    def calculateArea(polygon):
        """Calculate the area of a polygon."""

        if not isinstance(polygon, QgsGeometry):
            raise Glitch(
                "Calculator.calculateArea: polygon is not a QgsGeometry.")

        return polygon.area()
        # calculator = Calculator.QGIS_CALCULATOR
        # return calculator.measureArea(polygon)

    @staticmethod
    def calculatePerimeter(polygon, elevationLayer=None):
        """Calculate the perimeter of a polygon."""

        if not isinstance(polygon, QgsGeometry):
            raise Glitch(
                "Calculator.calculatePerimeter: polygon is not a QgsGeometry.")

        calculator = Calculator.QGIS_CALCULATOR
        return calculator.measurePerimeter(polygon)
