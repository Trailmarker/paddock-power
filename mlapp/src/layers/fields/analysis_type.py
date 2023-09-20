# -*- coding: utf-8 -*-
from .field_domain import FieldDomain


class AnalysisType(FieldDomain):
    Default = "Default"
    IgnoreFence = "Ignore Fence"
    ExcludePaddock = "Exclude Paddock"

    def toColour(self):
        """Get the colour associated with this status."""
        if self == AnalysisType.Default:
            return (255, 255, 255)
        elif self == AnalysisType.IgnoreFence:
            return (150, 150, 150, 100)
        elif self == AnalysisType.ExcludePaddock:
            return (255, 0, 0, 100)
        else:
            raise NotImplementedError("Unknown AnalysisType value")

    def toForegroundColour(self):
        """Get the foreground colour associated with this status."""
        if self == AnalysisType.Default:
            return (0, 0, 0)
        elif self == AnalysisType.IgnoreFence:
            return (0, 0, 0)
        elif self == AnalysisType.ExcludePaddock:
            return (255, 255, 255)
        else:
            raise NotImplementedError("Unknown AnalysisType value")
