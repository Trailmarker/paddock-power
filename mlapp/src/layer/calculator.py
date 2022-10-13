# -*- coding: utf-8 -*-
from math import hypot

from shapely.wkb import loads
from shapely.wkt import dumps

from qgis.core import QgsCoordinateReferenceSystem, QgsDistanceArea, QgsGeometry, QgsPoint, QgsPointXY, QgsProject, QgsRaster

from ..models.paddock_power_error import PaddockPowerError
from .profile import Profile

def makeDistanceAreaCalculator():
    """Return a QgsDistanceArea object with the correct settings for the project."""
    calculator = QgsDistanceArea()
    calculator.setSourceCrs(QgsCoordinateReferenceSystem(
        'EPSG:7845'), QgsProject.instance().transformContext())
    # See QgsCoordinateReferenceSystem('EPSG:7844').ellipsoidAcronym()
    calculator.setEllipsoid('EPSG:7019')
    return calculator

class Calculator:
    QGIS_CALCULATOR = makeDistanceAreaCalculator()
 
    @staticmethod
    def calculateProfile(line, elevationLayer=None):
        """Calculate the length of a line."""

        if not isinstance(line, QgsGeometry):
            raise PaddockPowerError(
                "Calculator.calculateLength: line is not a QgsGeometry.")

        if line.isMultipart():
            raise PaddockPowerError(
                "Calculator.calculateArea: Paddock Power should not be used with multi-part linestrings.")

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
            # Get points along line at the granularity of the project elevation layer, using Shapely
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

            pointsWithZ = [QgsPoint(point.x(), point.y(), dataProvider.identify(
                point, QgsRaster.IdentifyFormatValue).results()[1]) for point in pointsAlongLine]

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

        minimumElevation = round(min(elevations), 1)
        maximumElevation = round(max(elevations), 1)
        meanElevation = round(
            sum(elevations) / len(elevations), 1)

        maximumDistance = distances[-1]

        return Profile(maximumDistance = maximumDistance,
                                 distances = distances,
                                 elevations = elevations,
                                 minimumElevation = minimumElevation,
                                 maximumElevation = maximumElevation,
                                 meanElevation = meanElevation)

    @staticmethod
    def calculateArea(polygon):
        """Calculate the area of a polygon."""

        if not isinstance(polygon, QgsGeometry):
            raise PaddockPowerError(
                "Calculator.calculateArea: polygon is not a QgsGeometry.")

        # if polygon.isMultipart():
        #     raise PaddockPowerError(
        #         "Calculator.calculateArea: Paddock Power should not be used with multi-part polygons.")


        calculator = Calculator.QGIS_CALCULATOR

        return calculator.measureArea(polygon)

    @staticmethod
    def calculatePerimeter(polygon, elevationLayer=None):
        """Calculate the perimeter of a polygon."""

        if not isinstance(polygon, QgsGeometry):
            raise PaddockPowerError(
                "Calculator.calculatePerimeter: polygon is not a QgsGeometry.")

        # if polygon.isMultipart():
        #     raise PaddockPowerError(
        #         "Calculator.calculatePerimeter: Paddock Power should not be used with multi-part polygons.")

        calculator = Calculator.QGIS_CALCULATOR

        return calculator.measurePerimeter(polygon)
