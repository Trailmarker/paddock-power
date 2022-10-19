# -*- coding: utf-8 -*-
from os import path
import sqlite3

from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.core import QgsVectorLayer

# -*- coding: utf-8 -*-
from ..spatial.features.boundary import Boundary
from ..spatial.features.waterpoint import Waterpoint
from ..spatial.features.pipeline import Pipeline
from ..spatial.features.fence import Fence
from ..spatial.features.paddock import Paddock
from ..spatial.features.land_system import LandSystem
from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.feature_layer_source_type import FeatureLayerSourceType
from ..utils import resolveGeoPackageFile
from .milestone import Milestone
from .glitch import Glitch


class Project(QObject):
    PROJECT_BASE_DATA_GROUP = "Base Data"

    PADDOCK_POWER_FEATURE_TYPES = (
        Boundary, Waterpoint, Pipeline, Fence, Paddock, LandSystem)

    # emit this signal when paddocks are updated
    milestonesUpdated = pyqtSignal(dict)
    milestoneChanged = pyqtSignal(Milestone)

    def __init__(self, gpkgFile=None):
        super().__init__()
        self.milestones = {}
        self.milestone = None

        self.elevationLayer = None

        if gpkgFile is None:
            self.gpkgFile = resolveGeoPackageFile()

        if gpkgFile is not None:
            self.gpkgFile = gpkgFile

        self.isLoaded = False

    def validateMilestoneName(self, milestoneName):
        """Validate a Milestone name."""
        if not milestoneName:
            raise Glitch(
                "Project.getMilestone: Milestone name is empty.")

        if milestoneName not in self.milestones:
            raise Glitch(
                f"Project.getMilestone: Milestone '{milestoneName}' does not exist.")

    def getMilestone(self, milestoneName):
        """Get a milestone by name."""
        self.validateMilestoneName(milestoneName)

        return self.milestones[milestoneName]

    def setMilestone(self, milestoneName):
        """Set the current milestone."""
        self.validateMilestoneName(milestoneName)

        if self.milestone is not None:
            self.milestone.disconnectAll()

        self.milestone = self.milestones[milestoneName]

        # Set the current milestone's layer group visible, and hide others
        for milestone in self.milestones.values():
            milestone.setVisible(milestone.milestoneName == milestoneName)

        self.milestoneChanged.emit(self.milestone)
        return self.milestone

    def addMilestone(self, milestoneName):
        """Add a new milestone to the project."""
        milestone = Milestone(milestoneName, self.gpkgFile, self.elevationLayer)
        milestone.create()

        self.milestones[milestoneName] = milestone
        milestone.addToMap()
        self.milestonesUpdated.emit(self.milestones)
        return milestone

    def addMilestoneFromExisting(self, milestoneName, existingMilestoneName):
        """Add a milestone copied from an existing milestone."""
        existingMilestone = self.getMilestone(existingMilestoneName)

        addedMilestone = self.addMilestone(milestoneName)
        existingMilestone.copyTo(addedMilestone)

    def deleteMilestone(self, milestoneName):
        """Delete a milestone from the project."""
        self.validateMilestoneName(milestoneName)

        if not self.gpkgFile:
            raise Glitch(
                "Project.deleteMilestone: Project has no GeoPackage file yet.")

        milestone = self.milestones.pop(milestoneName, None)
        milestone.removeFromMap()
        milestone.deleteFromGeoPackage()

        # Deleting the current Milestone
        if self.milestone is not None and self.milestone.milestoneName == milestoneName:
            self.milestone = None
            self.milestoneChanged.emit(self.milestone)

        self.milestonesUpdated.emit(self.milestones)

    def load(self, forceLoad=False):
        """Load this project from its GeoPackage."""
        assert(self.gpkgFile is not None)

        if not self.isLoaded or forceLoad:
            # We go to a loaded state if the GeoPackage file does not exist
            if not path.exists(self.gpkgFile):
                self.isLoaded = True
                return

            elevationLayerName = Project.findElevationLayer(self.gpkgFile)
            if elevationLayerName is not None:
                self.elevationLayer = ElevationLayer(elevationLayerName, self.gpkgFile)

            milestoneNames = Project.findMilestones(self.gpkgFile)
            milestoneNames.sort()

            self.milestones = {}
            self.milestone = None

            for milestoneName in milestoneNames:
                milestone = Milestone(milestoneName, self.gpkgFile, self.elevationLayer)
                self.milestones[milestoneName] = milestone
                milestone.load()

            self.isLoaded = True
            self.milestonesUpdated.emit(self.milestones)

        if self.milestone is None:
            self.setMilestone(list(self.milestones.keys())[0])

    def addToMap(self):
        """Add the project to the map."""
        # Remove first to keep order sane
        self.removeFromMap()

        milestoneNames = sorted(self.milestones.keys())

        for milestoneName in milestoneNames:
            self.milestones[milestoneName].addToMap()

        # baseDataGroup = QgsProject.instance().layerTreeRoot().findGroup(Project.PROJECT_BASE_DATA_GROUP)
        # self.elevationLayer.addToMap(baseDataGroup)

    def removeFromMap(self):
        """Remove the project from the map."""
        milestoneNames = sorted(self.milestones.keys())

        for milestoneName in milestoneNames:
            self.milestones[milestoneName].removeFromMap()

    @classmethod
    def findMilestones(cls, gpkgFile):
        """Find the milestones in a project GeoPackage."""
        def rchop(s, suffix):
            if suffix and s.endswith(suffix):
                return s[:-len(suffix)]
            return s

        layers = QgsVectorLayer(path=gpkgFile, providerLib="ogr")
        if not layers.isValid():
            raise Glitch(
                f"Project.findMilestones: error loading Paddock Power GeoPackage at {gpkgFile}")

        layerNames = [l.split('!!::!!')[1]
                      for l in layers.dataProvider().subLayers()]
        featureTypeNames = [
            ft.__name__ for ft in Project.PADDOCK_POWER_FEATURE_TYPES]

        milestones = set()
        for layerName in layerNames:
            match = next(
                (t for t in featureTypeNames if layerName.endswith(t + 's')), None)
            if match is not None:
                milestones.add(rchop(layerName, match + 's').strip())
            match = next(
                (t for t in featureTypeNames if layerName.endswith(t)), None)
            if match is not None:
                milestones.add(rchop(layerName, match).strip())

        return list(milestones)

    @classmethod
    def findElevationLayer(cls, gpkgFile):
        """Find the elevation layer in a project GeoPackage."""
        db = sqlite3.connect(gpkgFile)
        cursor = db.cursor()
        cursor.execute(
            "SELECT table_name, data_type FROM gpkg_contents WHERE data_type = '2d-gridded-coverage'")
        grids = cursor.fetchall()

        if len(grids) == 0:
            return None
        elif len(grids) == 1:
            return grids[0][0]
        else:
            raise Glitch(
                f"Project.findElevationLayer: multiple elevation layers found in {gpkgFile}")
