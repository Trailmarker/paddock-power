# -*- coding: utf-8 -*-
from ...utils import PLUGIN_NAME
from .feature_status import FeatureStatus
from .field_domain import FieldDomain


class Timeframe(FieldDomain):
    f"""The two available timeframes for a {PLUGIN_NAME} project."""
    Current = "Current"
    Future = "Future"
    Historical = "Historical"
    Undefined = "Undefined"
    Drafted = "Drafted"

    def toColour(self):
        """Get the colour associated with this status."""
        if Timeframe[self.name] == Timeframe.Current:
            return (215, 195, 163)
        elif Timeframe[self.name] == Timeframe.Future:
            return (163, 195, 215, 100)
        elif Timeframe[self.name] == Timeframe.Historical:
            raise NotImplementedError("Historical status not implemented")
        elif Timeframe[self.name] == Timeframe.Undefined:
            raise NotImplementedError("Undefined status not implemented")
        elif Timeframe[self.name] == Timeframe.Drafted:
            return (250, 218, 221, 100)

    def toForegroundColour(self):
        """Get the foreground colour associated with this status."""
        if Timeframe[self.name] == Timeframe.Current:
            return (0, 0, 0)
        elif Timeframe[self.name] == Timeframe.Future:
            return (255, 255, 255)
        elif Timeframe[self.name] == Timeframe.Historical:
            raise NotImplementedError("Historical status not implemented")
        elif Timeframe[self.name] == Timeframe.Undefined:
            raise NotImplementedError("Undefined status not implemented")
        elif Timeframe[self.name] == Timeframe.Drafted:
            return (0, 0, 0)

    def matchFeatureStatus(self, featureStatus):
        if Timeframe[self.name] == Timeframe.Current:
            return FeatureStatus[featureStatus.name] in [FeatureStatus.Built, FeatureStatus.BuiltSuperseded]
        elif Timeframe[self.name] == Timeframe.Future:
            return FeatureStatus[featureStatus.name] in [FeatureStatus.Built, FeatureStatus.Planned]
        elif Timeframe[self.name] == Timeframe.Historical:
            return FeatureStatus[featureStatus.name] in [FeatureStatus.Archived]
        elif Timeframe[self.name] == Timeframe.Undefined:
            return FeatureStatus[featureStatus.name] in [FeatureStatus.PlannedSuperseded, FeatureStatus.Undefined]
        elif Timeframe[self.name] == Timeframe.Drafted:
            return FeatureStatus[featureStatus.name] in [FeatureStatus.Drafted]
