# -*- coding: utf-8 -*-

from shapely.ops import split

from qgis.core import QgsGeometry

from ..dev import *

# import sqlite3
# conn = sqlite3.connect('C:/Users/tom.lynch/dev/trm/paddock-power-data/Kidman-0.38/Kidman.gpkg')
# conn.enable_load_extension(True)
# conn.execute("select load_extension('mod_spatialite')")

# for row in conn.execute("SELECT ST_AsText(MakePoint(11.5, 42.5, 4326))"):
#     print(row)

from shapely.geometry import shape


def getFence(fid):
    return next(f for f in workspace().fenceLayer.getFeatures() if f.FID == fid)


def getPropertyGeometry(glitchBuffer=1.0):
    """Get the property geometry for this Fence."""
    # Get the whole area around the property
    # We are only interested in Paddocks that are going to be there if we Plan this Fence (so Future, not Current)
    # We use the PaddockLayer because it is the reference for Paddock timeframe data
    currentPaddocks = workspace().paddockLayer.getFeaturesByTimeframe(Timeframe.Future)

    # Get the whole current Paddock area - note the buffering here to reduce glitches
    return QgsGeometry.unaryUnion(p.GEOMETRY.buffer(glitchBuffer, 10) for p in currentPaddocks)
    # return property.buffer(-glitchBuffer, 10)


def getPropertyNeighbourhood():
    """Get the property neighbourhood around this Fence."""
    # Get the whole area around the property
    propertyGeometry = getPropertyGeometry()

    if not propertyGeometry or propertyGeometry.isEmpty():
        return None
    propertyExtent = propertyGeometry.boundingBox()
    propertyExtent.scale(1.5)  # Expand by 50%
    return QgsGeometry.fromRect(propertyExtent)


def getNotPropertyGeometry(glitchBuffer=1.0):
    """Get the not property geometry for this Fence."""
    # Get the whole area around the property
    propertyNeighbourhood = getPropertyNeighbourhood()
    propertyGeometry = getPropertyGeometry(glitchBuffer=glitchBuffer)

    # Get a representation of everything that's not in the property
    notPropertyGeometry = propertyNeighbourhood.difference(propertyGeometry)
    return notPropertyGeometry.buffer(2 * glitchBuffer, 10)


def getCrossedPaddocks(fence):
    fenceLine = getFence(fence.FID).GEOMETRY
    paddockLayer = workspace().paddockLayer

    # We are only interested in Paddocks that are going to be there if we Plan this Fence (so Future, not Current)
    candidatePaddocks = paddockLayer.getFeaturesByTimeframe(Timeframe.Future)

    intersects = [p for p in candidatePaddocks if fenceLine.intersects(p.GEOMETRY)]

    # # Crop the fence line to the property
    # propertyBoundary = getPropertyGeometry(glitchBuffer=1.0)
    crossedPaddocks = []

    for paddock in intersects:
        polygon = paddock.GEOMETRY.asMultiPolygon()
        boundaryLine = QgsGeometry.fromMultiPolylineXY(polygon[0])
        intersection = boundaryLine.intersection(fenceLine)
        if intersection.isMultipart():
            crossedPaddocks.append(paddock)

    allCrossed = QgsGeometry.unaryUnion(p.GEOMETRY for p in crossedPaddocks)
    allCrossedBuffered = allCrossed.buffer(1.0, 10)
    fenceLine = fenceLine.intersection(allCrossedBuffered)

    if not crossedPaddocks:
        return [], []
    else:
        return [fenceLine], crossedPaddocks


def getCrossedBasePaddocks(fence):
    """Same as getCrossedPaddocks but returns the crossed Base Paddock features."""
    fenceLines, crossedPaddocks = getCrossedPaddocks(fence)
    return fenceLines, [p.getBasePaddock() for p in crossedPaddocks]


def getNewBasePaddocks(fence):
    """Get the Base Paddocks that will be newly enclosed by this Fence, and the normalised outer fence lines."""

    fenceLine = fence.GEOMETRY

    if not fenceLine or fenceLine.isEmpty():
        return [], []

    notProperty = getNotPropertyGeometry(glitchBuffer=1.0)

    if notProperty.isEmpty():
        raise BaseException(f"{PLUGIN_NAME} can't find the property boundary, is there any paddock data?")

    if fenceLine.isEmpty():
        return [], []

    notProperty = notProperty.asGeometryCollection() if notProperty.isMultipart() else [notProperty] 

    _, *propertyBoundaries = [QgsGeometry.fromMultiPolylineXY(p.asPolygon()) for p in notProperty]


    # Straightforward case where we have a single new fence line enclosing things
    if fenceLine.isMultipart():
        fenceLine = fenceLine.asGeometryCollection()[0]

    newBasePaddocks = []

    for interiorRing in propertyBoundaries:

        intersection = interiorRing.intersection(fenceLine)

        if (not intersection.isEmpty()) and intersection.isMultipart():
            # We crossed the not-property boundary more than once, so we are enclosing land
            blade = shape(fenceLine.__geo_interface__)

            # qgsDebug("getNewPaddocks: splitGeometry in progress …")
            notProperty = shape(getNotPropertyGeometry().__geo_interface__)
            splits = split(notProperty, blade)

            # The first result is always the piece of notProperty that is carved out? TODO check this
            if splits:
                paddockGeometry = notProperty.difference(splits[0])
                newBasePaddock = workspace().basePaddockLayer.makeFeature()
                newBasePaddock.draftFeature(QgsGeometry.fromWkt(paddockGeometry.wkt), f"Fence New")
                newBasePaddocks.append(newBasePaddock)

    # notPropertyGeometry = self.getNotPropertyGeometry(glitchBuffer=1.0)
    # fenceLine = fenceLine.intersection(notPropertyGeometry)

    if not newBasePaddocks or not fenceLine:
        return [], []
    else:
        return [fenceLine], newBasePaddocks


def planFenceLine(fence):
    edits = Edits()

    _, crossedBasePaddocks = getCrossedBasePaddocks(fence)

    fenceLine = fence.GEOMETRY
    blade = shape(fenceLine.__geo_interface__)

    for crossedBasePaddock in crossedBasePaddocks:
        # See discussion here
        # https://gis.stackexchange.com/questions/232771/splitting-polygon-by-linestring-in-geodjango
        crossedPaddockGeometry = shape(crossedBasePaddock.GEOMETRY.__geo_interface__)
        splits = split(crossedPaddockGeometry, blade)

        for i, splitPaddockGeometry in enumerate(splits):
            splitPaddock = workspace().basePaddockLayer.makeFeature()

            splitPaddock.draftFeature(
                QgsGeometry.fromWkt(splitPaddockGeometry.wkt),
                crossedBasePaddock.NAME + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i])

            splitPaddock.recalculate()
            edits.editBefore(splitPaddock.planFeature(fence, crossedBasePaddock))

    _, newBasePaddocks = getNewBasePaddocks(fence)

    for newBasePaddock in newBasePaddocks:
        edits.editBefore(newBasePaddock.planFeature(fence))

    for crossedBasePaddock in crossedBasePaddocks:
        edits.editBefore(crossedBasePaddock.supersedeFeature(fence))

    return Edits.upsert(fence).editAfter(edits)
