# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, QObject

from .project import Project
from .paddock_power_error import PaddockPowerError

class State(QObject):
    # emit this signal when paddocks are updated
    projectChanged = pyqtSignal()

    def __init__(self):
        super(State, self).__init__()

        self.project = None

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