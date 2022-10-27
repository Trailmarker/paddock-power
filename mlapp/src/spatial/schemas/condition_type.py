# -*- coding: utf-8 -*-
from .field_domain import FieldDomain


class ConditionType(FieldDomain):
    """Allowed conditions for a Land Type, Paddock and Water Buffer combination."""
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    def toColour(self):
        """Get the colour associated with this status."""
        if self == ConditionType.A:
            return (35, 139, 69)
        elif self == ConditionType.B:
            return (65, 171, 93)
        elif self == ConditionType.C:
            return (116, 196, 118)
        elif self == ConditionType.D:
            return (161, 217, 155)
        else:
            raise NotImplementedError("Unknown ConditionType value")

    def toForegroundColour(self):
        """Get the foreground colour associated with this status."""
        if self == ConditionType.A:
            return (255, 255, 255)
        elif self == ConditionType.B:
            return (255, 255, 255)
        elif self == ConditionType.C:
            return (0, 0, 0)
        elif self == ConditionType.D:
            return (0, 0, 0)
        else:
            raise NotImplementedError("Unknown ConditionType value")
