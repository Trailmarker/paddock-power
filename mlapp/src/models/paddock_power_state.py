# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot, QObject

from qgis.core import QgsFeature

from .milestone import Milestone
from .paddock_power_error import PaddockPowerError
from .project import Project
from .singleton import Singleton
from ..utils import resolveGeoPackageFile, qgsDebug


class PaddockPowerState(QObject, metaclass=Singleton):
    milestoneChanged = pyqtSignal(Milestone)
    milestonesUpdated = pyqtSignal(dict)
    projectChanged = pyqtSignal(Project)
    selectedFenceChanged = pyqtSignal(QgsFeature)
    selectedPaddockChanged = pyqtSignal(QgsFeature)
    selectedPipelineChanged = pyqtSignal(QgsFeature)
    milestoneDataChanged = pyqtSignal()

    project = None

    def __init__(self):
        super().__init__()

    def detectProject(self):
        """Detect a Paddock Power project in the current QGIS project."""
        if self.project is None:
            try:
                gpkgFile = resolveGeoPackageFile()
                if gpkgFile is not None:
                    milestones = Project.findMilestones(gpkgFile)
                    if milestones:
                        qgsDebug(
                            f"PaddockPowerState.detectProject: detected project with {len(milestones)} milestones in {gpkgFile}")
                        project = Project(gpkgFile)
                        self.setProject(project)
                        return
            except Exception as e:
                qgsDebug(
                    "PaddockPowerState.detectProject: exception occurred while detecting project.")
                qgsDebug(str(e))
                pass
            qgsDebug("PaddockPowerState.detectProject: no project detected.")
        else:
            self.refreshProject()

    def refreshProject(self):
        """Refresh the current project."""
        if self.project is not None:
            self.project.load()
            self.project.addToMap()

    def getProject(self):
        """Get the current Project."""
        return self.project

    def getMilestone(self):
        """Get the current Milestone."""
        if self.project is not None:
            return self.project.milestone
        else:
            return None

    def getSelectedFence(self):
        """Get the selected Fence."""
        if self.project is not None and self.project.milestone is not None:
            return self.project.milestone.selectedFence

    def getSelectedPaddock(self):
        """Get the selected Paddock."""
        if self.project is not None and self.project.milestone is not None:
            return self.project.milestone.selectedPaddock

    def clearProject(self):
        """Clear the current Project, for example if the current QGIS project is closed."""
        if self.project is not None:
            self.project.removeFromMap()
            self.project = None
            self.projectChanged.emit(self.project)

    def setProject(self, project):
        """Set the current Project."""
        if not isinstance(project, Project):
            raise PaddockPowerError(
                "PaddockPowerState.setProject: project is not a Project.")

        if self.project is not None:
            self.project.removeFromMap()

        self.project = project
        self.refreshProject()
        self.projectChanged.emit(self.project)

    def setMilestone(self, milestone):
        """Set the current Project."""
        if not isinstance(milestone, Milestone):
            raise PaddockPowerError(
                "PaddockPowerState.setMilestone: milestone is not a Milestone.")

        if self.project is not None:
            self.project.setMilestone(milestone)
        else:
            raise PaddockPowerError(
                "PaddockPowerState.setMilestone: there is no current Project.")

    @pyqtSlot()
    def onProjectChanged(self, project):
        """Handle a change in the current Paddock Power project."""
        if self.project is not None:
            self.project.milestoneChanged.connect(
                lambda m: self.milestoneChanged.emit(m))
            self.project.milestonesUpdated.connect(
                lambda ms: self.milestonesUpdated.emit(ms))
            self.onMilestoneChanged(self.project.milestone)

    @pyqtSlot()
    def onMilestoneChanged(self, milestone):
        """Handle a change in the current Paddock Power milestone."""
        if self.project.milestone is not None:
            self.project.milestone.selectedFenceChanged.connect(
                lambda f: self.selectedFenceChanged.emit(f))
            self.project.milestone.selectedPaddockChanged.connect(
                lambda p: self.selectedPaddockChanged.emit(p))
            self.project.milestone.selectedPipelineChanged.connect(
                lambda p: self.selectedPipelineChanged.emit(p))
            self.project.milestone.milestoneDataChanged.connect(
                lambda: self.milestoneDataChanged.emit())


def connectPaddockPowerStateListener(state, listener):
    """Connect a listener to the Paddock Power state."""
    if listener is not None:
        if hasattr(listener, "onMilestoneChanged") and callable(listener.onMilestoneChanged):
            state.milestoneChanged.connect(
                lambda m: listener.onMilestoneChanged(m))
        if hasattr(listener, "onMilestonesUpdated") and callable(listener.onMilestonesUpdated):
            state.milestonesUpdated.connect(
                lambda ms: listener.onMilestonesUpdated(ms))
        if hasattr(listener, "onProjectChanged") and callable(listener.onProjectChanged):
            state.projectChanged.connect(
                lambda p: listener.onProjectChanged(p))
        if hasattr(listener, "onSelectedFenceChanged") and callable(listener.onSelectedFenceChanged):
            state.selectedFenceChanged.connect(
                lambda f: listener.onSelectedFenceChanged(f))
        if hasattr(listener, "onSelectedPaddockChanged") and callable(listener.onSelectedPaddockChanged):
            state.selectedPaddockChanged.connect(
                lambda p: listener.onSelectedPaddockChanged(p))
        if hasattr(listener, "onSelectedPipelineChanged") and callable(listener.onSelectedPipelineChanged):
            state.selectedPipelineChanged.connect(
                lambda p: listener.onSelectedPipelineChanged(p))
        if hasattr(listener, "onMilestoneDataChanged") and callable(listener.onMilestoneDataChanged):
            state.milestoneDataChanged.connect(
                lambda: listener.onMilestoneDataChanged())
