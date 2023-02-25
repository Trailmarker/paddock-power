# -*- coding: utf-8 -*-
from ...models import StateMachineMixin
from ..fields import TIMEFRAME, Timeframe, StatusFeatureSchema
from ..interfaces import IStatusFeature
from .edits import Edits
from .feature_action import FeatureAction
from .feature_state_machine import FeatureStateMachine


@StatusFeatureSchema.addSchema()
class StatusFeatureMixin(StateMachineMixin, IStatusFeature):

    def __init__(self):
        """Create a new AreaFeature."""
        StateMachineMixin.__init__(self)

        self._machine = FeatureStateMachine(self)

    @property
    def machine(self):
        return self._machine

    @property
    def TIMEFRAME(self):
        """Return the timeframe for the Feature."""
        if not self.hasTimeframe:
            return Timeframe.fromFeatureStatus(self.STATUS)
        else:
            return self.attribute(TIMEFRAME)

    @FeatureAction.plan.handleAndPersist()
    def planFeature(self):
        """Plan a Feature."""

        return Edits.upsert(self)

    @FeatureAction.undoPlan.handleAndPersist()
    def undoPlanFeature(self):
        """Undo planning a Feature."""
        return Edits.upsert(self)

    @FeatureAction.build.handleAndPersist()
    def buildFeature(self):
        """Build a Feature."""
        return Edits.upsert(self)

    @FeatureAction.undoBuild.handleAndPersist()
    def undoBuildFeature(self):
        """Undo Building a Feature."""
        return Edits.upsert(self)

    @FeatureAction.supersede.handleAndPersist()
    def supersedeFeature(self):
        """Supersede a Feature."""
        return Edits.upsert(self)

    @FeatureAction.undoSupersede.handleAndPersist()
    def undoSupersedeFeature(self):
        """Undo superseding a Feature."""
        return Edits.upsert(self)

    @FeatureAction.trash.handleAndPersist()
    def trashFeature(self):
        """Trash a Feature."""
        return Edits.delete(self)

    @FeatureAction.archive.handleAndPersist()
    def archiveFeature(self):
        """Archive a Feature."""
        return Edits.upsert(self)

    @FeatureAction.undoArchive.handleAndPersist()
    def undoArchiveFeature(self):
        """Archive a Feature."""
        return Edits.upsert(self)
