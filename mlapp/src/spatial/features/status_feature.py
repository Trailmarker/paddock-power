# -*- coding: utf-8 -*-
from .edits import Edits
from .feature import Feature
from .feature_action import FeatureAction
from .schemas import StatusFeatureSchema
from .feature_state_machine import FeatureStateMachine

@StatusFeatureSchema.addSchema()
class StatusFeature(Feature, FeatureStateMachine):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new AreaFeature."""
        super().__init__(featureLayer, existingFeature)
        self.featureUpdated.connect(lambda: self.stateChanged.emit(self))
        self.featureDeleted.connect(lambda: self.stateChanged.emit(self))

    def __repr__(self):
        """Return a string representation of the Feature."""
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}'), status={self.status})"

    def __str__(self):
        """Convert the Feature to a string representation."""
        return repr(self)

    @Edits.persistEdits
    @FeatureAction.trash.handler()
    def trashFeature(self):
        """Trash a Draft Feature."""
        return Edits.delete(self)
