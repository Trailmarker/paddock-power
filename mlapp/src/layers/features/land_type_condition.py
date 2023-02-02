# -*- coding: utf-8 -*-
from ...models import Glitch, WorkspaceMixin
from ..fields import ConditionType
from ..interfaces import IPersistedFeature


class LandTypeCondition(IPersistedFeature, WorkspaceMixin):
    """This is a sort of mock Feature for the LandTypeConditionTable."""

    def __init__(self,
                 *args):
        super().__init__()
        
        if not args:
            # Blank constructor
            self._conditionRecord = (-1, -1, ConditionType.A)
        elif len(args) == 1:
            # Copy constructor
            assert isinstance(args[0], LandTypeCondition)
            self._conditionRecord = tuple(*args)        
        elif len(args) == 3:
            # Constructor from values
            self._conditionRecord = tuple(args)
        else:
            raise Glitch(f"LandTypeCondition.__init__: unexpected number of arguments: {len(args)}")

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
        self.featureLayer.updateFeature(self)

    def delete(self):
        self.featureLayer.deleteFeature(self)

    def recalculate(self):
        pass
