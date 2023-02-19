# -*- coding: utf-8 -*-
from re import finditer

from ...models import Glitch, WorkspaceMixin
from ..fields import PADDOCK, LAND_TYPE, CONDITION_TYPE, ConditionType
from ..interfaces import IPersistedFeature


class LandTypeCondition(IPersistedFeature, WorkspaceMixin):
    """This is a sort of mock Feature for the LandTypeConditionTable."""

    @classmethod
    def displayName(cls):
        """Return the display name of the Feature."""
        matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', cls.__name__)
        return " ".join(m.group(0) for m in matches)

    @classmethod
    def focusOnSelect(self):
        """Return True if the app should focus on this type of Feature when selected."""
        return False

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
        return self.workspace.landTypeConditionTable

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

    @property
    def GEOMETRY(self):
        """Return the Feature's geometry."""
        return None

    @property
    def NAME(self):
        return self.TITLE

    @property
    def TITLE(self):
        return f"{self.displayName()} ({self.PADDOCK} {self.LAND_TYPE} {self.CONDITION_TYPE})"

    @property
    def isInfrastructure(self):
        """Return True if the Feature is infrastructure."""
        return False

    def hasField(self, fieldName):
        """Return True if the Feature's Schema has a Field with the supplied name."""
        return fieldName in [PADDOCK, LAND_TYPE, CONDITION_TYPE]

    @property
    def hasArea(self):
        """Return True if the Feature has an area."""
        return False

    @property
    def hasElevation(self):
        """Return True if the Feature has an elevation."""
        return False

    @property
    def hasFid(self):
        """Return True if the Feature has a fid."""
        return False

    @property
    def hasLength(self):
        """Return True if the Feature has a length."""
        return False

    @property
    def hasLongitude(self):
        """Return True if the Feature has a longitude."""
        return False

    @property
    def hasLatitude(self):
        """Return True if the Feature has a latitude."""
        return False

    @property
    def hasPerimeter(self):
        """Return True if the Feature has a perimeter."""
        return False

    @property
    def hasTimeframe(self):
        """Return True if this layer has a timeframe."""
        return False

    @property
    def hasStatus(self):
        """Return True if this layer has a status."""
        return False

    def matchTimeframe(self, timeframe):
        """Return True if this feature's timeframe or status matches the supplied timeframe."""
        return True

    def selectFeature(self):
        """Select the Feature."""
        pass

    def zoomFeature(self):
        """Zoom to the Feature."""
        pass
