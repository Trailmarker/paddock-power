# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QState, QStateMachine, pyqtSignal

from ..feature_status import FeatureStatus


class FeatureStateMachine(QStateMachine):

    # State transitions
    plan = pyqtSignal()
    undoPlan = pyqtSignal()
    build = pyqtSignal()
    undoBuild = pyqtSignal()
    supersede = pyqtSignal()
    archive = pyqtSignal()

    def __init__(self, feature=None):
        """Initialise the state machine."""
        # Set up state machine
        super().__init__()

        self.draft = QState()
        self.planned = QState()
        self.existing = QState()
        self.superseded = QState()
        self.removed = QState()
        self.archived = QState()

        self.draft.addTransition(self.plan, self.planned)
        self.planned.addTransition(self.undoPlan, self.draft)
        self.planned.addTransition(self.build, self.existing)
        self.existing.addTransition(self.undoBuild, self.planned)

        self.existing.addTransition(self.supersede, self.superseded)

        self.draft.addTransition(self.archive, self.archived)
        self.planned.addTransition(self.archive, self.archived)
        self.existing.addTransition(self.archive, self.archived)
        self.superseded.addTransition(self.archive, self.archived)

        # Note that the self.setInitialState is not called, and the machine is not yet run …

        if feature is not None:
            self.connect(feature)

    def connect(self, feature):
        """Connect the state machine to a Feature."""
        if feature.status() != FeatureStatus.Unknown:
            self.setInitialState(feature.status())
        else:
            feature.setStatus(FeatureStatus.Draft)
            self.setInitialState(FeatureStatus.Draft)

        self.draft.entered.connect(feature.setStatus(FeatureStatus.Draft))
        self.planned.entered.connect(feature.setStatus(FeatureStatus.Planned))
        self.existing.entered.connect(feature.setStatus(FeatureStatus.Existing))
        self.superseded.entered.connect(feature.setStatus(FeatureStatus.Superseded))
        self.archived.entered.connect(feature.setStatus(FeatureStatus.Archived))
