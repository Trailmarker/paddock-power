# -*- coding: utf-8 -*-
from ...models import StateMachineMixin
from ..fields import TIMEFRAME, Timeframe, StatusFeatureSchema
from .edits import Edits
from .feature_action import FeatureAction
from .feature_state_machine import FeatureStateMachine
from .interfaces import IStatusFeature
from .persisted_feature import PersistedFeature


@StatusFeatureSchema.addSchema()
class StatusFeature(IStatusFeature, PersistedFeature, StateMachineMixin):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new AreaFeature."""
        PersistedFeature.__init__(self, featureLayer, existingFeature)

        self._machine = FeatureStateMachine(self)

    def __repr__(self):
        """Return a string representation of the Feature."""
        return f"{self.__class__.__name__}(id()={self.id()},FID={self.FID},name='{self.NAME}',status={self.STATUS})"

    def __str__(self):
        """Convert the Feature to a string representation."""
        return repr(self)

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

    @Edits.persistFeatures
    @FeatureAction.plan.handler()
    def planFeature(self):
        """Plan a Feature."""

        return Edits.upsert(self)

    @Edits.persistFeatures
    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        """Undo planning a Feature."""
        return Edits.upsert(self)

    @Edits.persistFeatures
    @FeatureAction.build.handler()
    def buildFeature(self):
        """Build a Feature."""
        return Edits.upsert(self)

    @Edits.persistFeatures
    @FeatureAction.undoBuild.handler()
    def undoBuildFeature(self):
        """Undo Building a Feature."""
        return Edits.upsert(self)

    @Edits.persistFeatures
    @FeatureAction.supersede.handler()
    def supersedeFeature(self):
        """Supersede a Feature."""
        return Edits.upsert(self)

    @Edits.persistFeatures
    @FeatureAction.undoSupersede.handler()
    def undoSupersedeFeature(self):
        """Undo superseding a Feature."""
        return Edits.upsert(self)

    @Edits.persistFeatures
    @FeatureAction.trash.handler()
    def trashFeature(self):
        """Trash a Feature."""
        return Edits.delete(self)

    @Edits.persistFeatures
    @FeatureAction.archive.handler()
    def archiveFeature(self):
        """Archive a Feature."""
        return Edits.upsert(self)
