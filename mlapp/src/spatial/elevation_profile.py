# -*- coding: utf-8 -*-
class ElevationProfile:
    def __init__(self, *, maximumDistance, distances, elevations, minimumElevation, maximumElevation, meanElevation):
        self.maximumDistance = maximumDistance
        self.distances = distances
        self.elevations = elevations
        self.minimumElevation = minimumElevation
        self.maximumElevation = maximumElevation
        self.meanElevation = meanElevation
