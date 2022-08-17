# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.core import QgsProject

from .milestone import Milestone
from ..utils import qgsDebug


class Project(QObject):
    # emit this signal when paddocks are updated
    milestonesUpdated = pyqtSignal()
    currentMilestoneChanged = pyqtSignal()

    def __init__(self):
        super(Project, self).__init__()

        self.milestones = []
        self.currentMilestone = None

        self.loadMilestones()

    def setMilestoneByName(self, milestoneName):
        """Set the current milestone."""
        self.currentMilestone = self.milestones[milestoneName]
        self.currentMilestoneChanged.emit()

    def loadMilestones(self):
        root = QgsProject.instance().layerTreeRoot()

        # Each milestone is a layer group with (for now) the word 'Infrastructure' in the name
        self.milestones = dict([(g.name(), Milestone(g))
                               for g in root.findGroups() if 'Infrastructure' in g.name()])
        self.milestonesUpdated.emit()

#        if len(self.milestones) > 1:
#            self.currentMilestone = self.milestones[1]

    def dump(self, tag=""):
        """Print to the QGIS message log."""

        qgsDebug("State", tag=tag)

        for m in self.milestones:
            m.dump()
