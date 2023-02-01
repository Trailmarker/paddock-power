# -*- coding: utf-8 -*-
from ...models import WorkspaceMixin
from .interfaces import IPersistedFeature


class LandTypeCondition(IPersistedFeature, WorkspaceMixin):
    """This is a sort of mock Feature for the ConditionTable."""

    def __init__(self,
                 *args):
        super().__init__()
        self._conditionRecord = args

    @property
    def featureLayer(self):
        return self.workspace.conditionTable

    @property
    def PADDOCK(self):
        return self._conditionRecord[0]

    @PADDOCK.setter
    def PADDOCK(self, val):
        self._conditionRecord[0] = val

    @property
    def LAND_TYPE(self):
        return self._conditionRecord[1]

    @LAND_TYPE.setter
    def LAND_TYPE(self, val):
        self._conditionRecord[1] = val

    @property
    def CONDITION_TYPE(self):
        return self._conditionRecord[2]

    @CONDITION_TYPE.setter
    def CONDITION_TYPE(self, val):
        self._conditionRecord[2] = val

    def upsert(self):
        self.featureLayer.upsertFeature(self)

    def delete(self):
        self.featureLayer.deleteFeature(self)

    def recalculate(self):
        pass
