# -*- coding: utf-8 -*-
from enum import Enum

from qgis.PyQt.QtGui import QColor

class FeatureStatus(Enum):
    """Allowed statuses for a Paddock Power feature."""
    Drafted = "Drafted"
    Planned = "Planned"
    Existing = "Existing"
    PlannedSuperseded = "Superseded (was Planned)"
    ExistingSuperseded = "Superseded (was Existing)"
    Archived = "Archived"
    Undefined = "Undefined"

    def toColour(self):
        """Get the colour associated with this status."""
        if self in [FeatureStatus.Undefined, FeatureStatus.Drafted]:
            return (250, 218, 221)
        elif self == FeatureStatus.Planned:
            return (215, 195, 163)
        elif self == FeatureStatus.Existing:
            return (215, 195, 163)
        elif self == FeatureStatus.PlannedSuperseded:
            return (147, 151, 153)
        elif self == FeatureStatus.ExistingSuperseded:
            return (147, 151, 153)
        elif self == FeatureStatus.Archived:
            raise NotImplementedError("Archived status not implemented")
        
        else:
            raise NotImplementedError("Unknown status not implemented")

    def toForegroundColour(self):
        """Get the foreground colour associated with this status."""
        if self in [FeatureStatus.Undefined, FeatureStatus.Drafted]:
            return (0 ,0, 0)
        elif self == FeatureStatus.Planned:
            return (255, 255, 255)
        elif self == FeatureStatus.Existing:
            return (0, 0, 0)
        elif self == FeatureStatus.PlannedSuperseded:
            return (0 ,0, 0)
        elif self == FeatureStatus.ExistingSuperseded:
            return (0, 0, 0)
        elif self == FeatureStatus.Archived:
            raise NotImplementedError("Archived status not implemented")
        else:
            raise NotImplementedError("Unknown status not implemented")

def toCssColour(r, g, b):
    return (f"rgb({r},{g},{b})")

def toHexColour(r, g, b):
    """Get the colour associated with this status."""
    return (f"#{r:X}{g:X}{b:X}")

def toQColor(r, g, b):
    """Get the colour associated with this status."""
    return QColor(r, g, b)

    