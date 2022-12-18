# -*- coding: utf-8 -*-
from .edits import Edits
from .persisted_feature import PersistedFeature
from .feature_action import FeatureAction
from ..schemas.schemas import StatusFeatureSchema
from .feature_state_machine import FeatureStateMachine


@StatusFeatureSchema.addSchema()
class StatusFeature(PersistedFeature, FeatureStateMachine):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new AreaFeature."""
        PersistedFeature.__init__(self, featureLayer, existingFeature)
        FeatureStateMachine.__init__(self)

        self.featureUpdated.connect(lambda: self.stateChanged.emit(self))
        self.featureDeleted.connect(lambda: self.stateChanged.emit(self))

    def __repr__(self):
        """Return a string representation of the Feature."""
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}'), status={self.status})"

    def __str__(self):
        """Convert the Feature to a string representation."""
        return repr(self)

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
