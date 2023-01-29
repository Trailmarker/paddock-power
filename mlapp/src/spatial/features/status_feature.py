# -*- coding: utf-8 -*-
from ...models.qt_abstract_meta import QtAbstractMeta
from ..fields.names import TIMEFRAME
from ..fields.schemas import StatusFeatureSchema
from ..fields.timeframe import Timeframe
from .edits import Edits
from .feature_action import FeatureAction
from .feature_state_machine import FeatureStateMachine
from .persisted_feature import PersistedFeature


@StatusFeatureSchema.addSchema()
class StatusFeature(PersistedFeature, FeatureStateMachine, metaclass=QtAbstractMeta):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new AreaFeature."""
        PersistedFeature.__init__(self, featureLayer, existingFeature)
        FeatureStateMachine.__init__(self)

    def __repr__(self):
        """Return a string representation of the Feature."""
        return f"{self.__class__.__name__}(id={self.FID},name='{self.NAME}',status={self.status})"

    def __str__(self):
        """Convert the Feature to a string representation."""
        return repr(self)

    @property
    def TIMEFRAME(self):
        """Return the timeframe for the Feature."""
        if not self.hasTimeframe:
            return Timeframe.fromFeatureStatus(self.status)
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

    @FeatureAction.supersede.handler()
    def supersedeFeature(self):
        """Supersede a Feature."""
        return Edits.upsert(self)

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

