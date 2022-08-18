# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.core import QgsProject, QgsVectorLayer

from ..layer.paddock_power_vector_layer import PaddockPowerVectorLayerType
from .milestone import Milestone
from ..utils import guiError, resolveGeoPackageFile, qgsDebug


class Project(QObject):
    # emit this signal when paddocks are updated
    milestonesUpdated = pyqtSignal()
    currentMilestoneChanged = pyqtSignal()

    milestones = {}
    currentMilestone = None

    def __init__(self, gpkgFile=None):
        super(Project, self).__init__()

        if gpkgFile is None:
            self.gpkgFile = resolveGeoPackageFile()

        if gpkgFile is not None:
            self.gpkgFile = gpkgFile

        self.isLoaded = False

    def setMilestoneByName(self, milestoneName):
        """Set the current milestone."""
        if milestoneName not in self.milestones:
            guiError(f"Milestone '{milestoneName}' does not exist.")
            return None

        self.currentMilestone = self.milestones[milestoneName]
        self.currentMilestoneChanged.emit()
        return self.currentMilestone

    def addMilestone(self, milestoneName):
        """Add a new milestone to the project."""
        if milestoneName in self.milestones:
            guiError(f"Milestone '{milestoneName}' already exists.")
            return None

        milestone = Milestone(milestoneName, self.gpkgFile)
        milestone.create()
        self.milestones[milestoneName] = milestone
        self.milestonesUpdated.emit()
        return milestone

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
        for milestone in self.milestones.values():
            milestone.addToMap()

    @classmethod
    def findMilestones(cls, gpkgName):
        """Find the milestones in a project GeoPackage."""
        def rchop(s, suffix):
            if suffix and s.endswith(suffix):
                return s[:-len(suffix)]
            return s

        layers = QgsVectorLayer(path=gpkgName, providerLib="ogr")
        if not layers.isValid():
            guiError(f"Error loading Paddock Power GeoPackage at {gpkgName}")

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
