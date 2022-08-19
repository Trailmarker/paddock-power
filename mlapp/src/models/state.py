# -*- coding: utf-8 -*-
from pydoc import resolve
from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.core import QgsProject

from .project import Project
from .paddock_power_error import PaddockPowerError
from ..utils import resolveGeoPackageFile

class State(QObject):
    # emit this signal when paddocks are updated
    projectChanged = pyqtSignal()

    def __init__(self):
        super(State, self).__init__()

        self.project = None

    def detectProject(self):
        """Detect a Paddock Power project in the current QGIS project."""
        if self.project is None:
            try:
                gpkgFile = resolveGeoPackageFile()
                if gpkgFile is not None:
                    milestones = Project.findMilestones(gpkgFile)
                    if milestones:
                        project = Project(gpkgFile)
                        self.setProject(project)
            except Exception:
                pass            

    def setProject(self, project):
        """Set the current milestone."""
        if not isinstance(project, Project):
            raise PaddockPowerError("State.setProject: project is not a Project.")

        if self.project is not None:
            self.project.removeFromMap()

        self.project = project
        self.project.load()
        self.project.addToMap()

        self.projectChanged.emit()

# Singleton behaviour
__STATE__ = State()

def getState():
    """Get the current state."""
    return __STATE__

def getProject():
    """Get the current project."""
    return __STATE__.project

def getMilestone():
    """Get the current milestone."""
    project = getProject()
    if project is not None:
        return project.currentMilestone

def detectProject():
    """Detect and load any current project."""
    __STATE__.detectProject()

def setProject(project):
    """Set the current project."""
    __STATE__.setProject(project)