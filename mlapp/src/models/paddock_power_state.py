# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot, QObject

from .milestone import Milestone
from .paddock_power_error import PaddockPowerError
from .project import Project
from .singleton import Singleton
from ..utils import resolveGeoPackageFile, qgsDebug

class PaddockPowerState(QObject, metaclass=Singleton):
    projectChanged = pyqtSignal(Project)
    milestoneChanged = pyqtSignal(Milestone)
    milestonesUpdated = pyqtSignal(dict)

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
                qgsDebug("PaddockPowerState.detectProject: exception occurred while detecting project.")
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
        qgsDebug(f"PaddockPowerState.onProjectChanged: project changed to {str(project)}")
        if self.project is not None:
            self.project.milestoneChanged.connect(lambda m: self.milestoneChanged.emit(m))
            self.project.milestonesUpdated.connect(lambda ms: self.milestonesUpdated.emit(ms))
    
    @pyqtSlot()
    def onMilestoneChanged(self, milestone):
        qgsDebug(f"PaddockPowerState.onMilestoneChanged: milestone changed to {str(milestone)}")
        """Handle a change in the current Paddock Power milestone."""
        if self.project.milestone is not None:
            # eg handle change in selected Paddock or Fence
            pass

    @pyqtSlot()
    def onMilestonesUpdated(self, milestones):
        """Handle a change to the current collection of Paddock Power milestones."""
        qgsDebug(f"PaddockPowerState.onMilestonesUpdated: milestones changed to {str(milestones)}")
        pass


def connectPaddockPowerStateListener(state, listener):
    """Connect a listener to the Paddock Power state."""
    if listener is not None:
        if hasattr(listener, "onProjectChanged") and callable(listener.onProjectChanged):
            state.projectChanged.connect(lambda p: listener.onProjectChanged(p))
        else:
            raise PaddockPowerError("PaddockPowerState.listen: listener has no onProjectChanged method.")
        if hasattr(listener, "onMilestoneChanged") and callable(listener.onMilestoneChanged):
            state.milestoneChanged.connect(lambda m: listener.onMilestoneChanged(m))
        else:
            raise PaddockPowerError("PaddockPowerState.listen: listener has no onMilestoneChanged method.")
        if hasattr(listener, "onMilestonesUpdated") and callable(listener.onMilestonesUpdated):
            state.milestonesUpdated.connect(lambda ms: listener.onMilestonesUpdated(ms))
        else:
            raise PaddockPowerError("PaddockPowerState.listen: listener has no onMilestonesUpdated method.")