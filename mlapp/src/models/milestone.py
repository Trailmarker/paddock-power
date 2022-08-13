# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, QObject

from ..utils import qgsDebug

class Milestone(QObject):
    # emit this signal when paddocks are updated
    paddocksUpdated = pyqtSignal()

    def __init__(self, milestoneGroup):
        super(Milestone, self).__init__()

        self.milestoneGroup = milestoneGroup
        self.paddockLayer = None
        self.paddockFeatures = []

        self.loadMilestoneName()
        self.loadPaddocks()

    def loadPaddocks(self):
        """Load the milestone paddocks from a detected paddock layer."""
        self.paddockFeatures = []
        paddockLayers = [l for l in self.milestoneGroup.findLayers() if 'Paddocks' in l.name()]
        if len(paddockLayers) == 0:
            print("No paddock layer found for milestone " + self.milestoneName)
        elif len(paddockLayers) > 1:
            print("Multiple paddock layers found for milestone " + self.milestoneName)
        else:
            self.paddockLayer = paddockLayers[0].layer()
            self.paddockFeatures = [f for f in self.paddockLayer.getFeatures()]

    def loadMilestoneName(self):
        """Refresh the milestone name from the group."""
        self.milestoneName = self.milestoneGroup.name()
        
    def dump(self,tag=""):
        qgsDebug(self.milestoneName, tag=tag)

        for f in self.paddockFeatures:
            qgsDebug(str(f['Paddock Name']), tag=tag)
