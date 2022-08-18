# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.core import QgsVectorLayer

from ..layer.paddock_power_vector_layer import PaddockPowerVectorLayerType
from .milestone import Milestone
from .paddock_power_error import PaddockPowerError
from ..utils import resolveGeoPackageFile


class Project(QObject):
    # emit this signal when paddocks are updated
    milestonesUpdated = pyqtSignal()
    currentMilestoneChanged = pyqtSignal()

    def __init__(self, gpkgFile=None):
        super(Project, self).__init__()
        self.milestones = {}
        self.currentMilestone = None

        if gpkgFile is None:
            self.gpkgFile = resolveGeoPackageFile()

        if gpkgFile is not None:
            self.gpkgFile = gpkgFile

        self.isLoaded = False

    def getMilestone(self, milestoneName):
        """Get a milestone by name."""
        if not milestoneName:
            raise PaddockPowerError(
                "Project.getMilestone: milestone name is empty.")

        if milestoneName not in self.milestones:
            raise PaddockPowerError(
                f"Project.getMilestone: milestone '{milestoneName}' does not exist.")

        return self.milestones[milestoneName]

    def setMilestone(self, milestoneName):
        """Set the current milestone."""
        if not milestoneName:
            raise PaddockPowerError(
                "Project.setMilestone: milestone name is empty.")

        if milestoneName not in self.milestones:
            raise PaddockPowerError(
                f"Project.setMilestone: milestone '{milestoneName}' does not exist.")

        self.currentMilestone = self.milestones[milestoneName]
        self.currentMilestoneChanged.emit()
        return self.currentMilestone

    def addMilestone(self, milestoneName):
        """Add a new milestone to the project."""
        if not milestoneName:
            raise PaddockPowerError(
                "Project.addMilestone: milestone name is empty.")

        if milestoneName in self.milestones:
            raise PaddockPowerError(
                f"Project.addMilestone: milestone '{milestoneName}' already exists.")

        milestone = Milestone(milestoneName, self.gpkgFile)
        milestone.create()
        self.milestones[milestoneName] = milestone
        self.milestonesUpdated.emit()
        return milestone

    def deleteMilestone(self, milestoneName):
        """Delete a milestone from the project."""
        if not milestoneName:
            raise PaddockPowerError(
                "Project.deleteMilestone: milestone name is empty.")

        if milestoneName not in self.milestones:
            raise PaddockPowerError(
                f"Project.deleteMilestone: milestone '{milestoneName}' does not exist.")

        milestone = self.milestones.pop(milestoneName, None)
        milestone.removeFromMap()
        milestone.deleteFromGeoPackage()

    def load(self):
        """Load this project from its GeoPackage."""
        assert(self.gpkgFile is not None)

        milestoneNames = Project.findMilestones(self.gpkgFile)

        for milestoneName in milestoneNames:
            milestone = Milestone(milestoneName, self.gpkgFile)
            self.milestones[milestoneName] = milestone
            milestone.load()

        self.isLoaded = True

    def addToMap(self):
        """Add the project to the map."""
        milestoneNames = sorted(self.milestones.keys())

        for milestoneName in milestoneNames:
            self.milestones[milestoneName].removeFromMap()
            self.milestones[milestoneName].addToMap()

    @classmethod
    def findMilestones(cls, gpkgFile):
        """Find the milestones in a project GeoPackage."""
        def rchop(s, suffix):
            if suffix and s.endswith(suffix):
                return s[:-len(suffix)]
            return s

        layers = QgsVectorLayer(path=gpkgFile, providerLib="ogr")
        if not layers.isValid():
            raise PaddockPowerError(
                f"Project.findMilestones: error loading Paddock Power GeoPackage at {gpkgFile}")

        layerNames = [l.split('!!::!!')[1]
                      for l in layers.dataProvider().subLayers()]
        layerTypeNames = [el.name for el in PaddockPowerVectorLayerType]

        milestones = set()
        for layerName in layerNames:
            match = next(
                (t for t in layerTypeNames if layerName.endswith(t + 's')), None)
            if match is not None:
                milestones.add(rchop(layerName, match + 's').strip())
            match = next(
                (t for t in layerTypeNames if layerName.endswith(t)), None)
            if match is not None:
                milestones.add(rchop(layerName, match).strip())

        return list(milestones)
