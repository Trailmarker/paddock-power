# -*- coding: utf-8 -*-
from ...utils import PLUGIN_NAME
from .feature_status import FeatureStatus
from .field_domain import FieldDomain
from .names import TIMEFRAME


class Timeframe(FieldDomain):
    f"""The two available timeframes for a {PLUGIN_NAME} workspace."""
    Current = "Current"
    Future = "Future"
    Undefined = "Undefined"

    def toColour(self):
        """Get the colour associated with this status."""
        if Timeframe[self.name] == Timeframe.Current:
            return (215, 195, 163)
        elif Timeframe[self.name] == Timeframe.Future:
            return (163, 195, 215, 100)
        elif Timeframe[self.name] == Timeframe.Undefined:
            raise NotImplementedError("Undefined status not implemented")

    def toForegroundColour(self):
        """Get the foreground colour associated with this status."""
        if Timeframe[self.name] == Timeframe.Current:
            return (0, 0, 0)
        elif Timeframe[self.name] == Timeframe.Future:
            return (255, 255, 255)
        elif Timeframe[self.name] == Timeframe.Undefined:
            raise NotImplementedError("Undefined status not implemented")

    def getFilterExpression(self):
        return f"\"{TIMEFRAME}\"='{self.name}'"

    def matchingFeatureStatuses(self):
        """Return all Feature Statuses that correspond to this Timeframe."""
        if Timeframe[self.name] == Timeframe.Current:
            return [FeatureStatus.Built, FeatureStatus.BuiltSuperseded, FeatureStatus.PlannedSuperseded,
                    FeatureStatus.BuiltArchived, FeatureStatus.PlannedArchived]
        elif Timeframe[self.name] == Timeframe.Future:
            return [FeatureStatus.Drafted, FeatureStatus.Built, FeatureStatus.Planned]
        elif Timeframe[self.name] == Timeframe.Undefined:
            return [FeatureStatus.PlannedSuperseded, FeatureStatus.PlannedArchived, FeatureStatus.Undefined]

    def matchFeatureStatus(self, featureStatus):
        """Check if a Feature Status corresponds to this Timeframe."""
        return bool([fs for fs in self.matchingFeatureStatuses()
                     if FeatureStatus[featureStatus.name] == FeatureStatus[fs.name]])

    def matchTimeframe(self, timeframe):
        """Check if a Timeframe corresponds to this Timeframe."""
        return (Timeframe[self.name] == Timeframe[timeframe.name])

    def includesStatus(self, statusTerm):
        """Return a SQLite IN clause matching a Feature Status term against this Timeframe."""
        matchTerms = ", ".join([f"'{status.name}'" for status in self.matchingFeatureStatuses()])
        return f"{statusTerm} in ({matchTerms})"

    def includesStatuses(self, *statusTerms):
        """Return a SQLite IN … AND … IN … compound clause matching several interacting Feature Status terms against this Timeframe."""
        includesStatusTerms = " and ".join([self.includesStatus(statusTerm) for statusTerm in statusTerms])
        return f"({includesStatusTerms})"

    def timeframeIncludesStatuses(self, timeframeTerm, *statusTerms):
        """Return a SQLite IN clause matching a Timeframe term against this Timeframe."""
        return f"({timeframeTerm} = '{self.name}') and {self.includesStatuses(*statusTerms)}"

        # matchTerms = ", ".join([f"'{timeframe.name}'" for timeframe in Timeframe.matchingTimeframes(self)])
        # return f"{timeframeTerm} in ({matchTerms})"

    @classmethod
    def timeframesIncludeStatuses(cls, timeframeTerm, *statusTerms):
        """Return a SQLite IN … AND … IN … compound clause matching several interacting Feature Status terms against a Timeframe term."""
        allTimeframeIncludeStatusesTerms = " or ".join(
            [timeframe.timeframeIncludesStatuses(timeframeTerm, *statusTerms) for timeframe in cls])
        return f"({allTimeframeIncludeStatusesTerms})"

    @classmethod
    def matchingTimeframes(cls, featureStatus):
        """Return all Timeframes that correspond to a Feature Status."""
        return [timeframe for timeframe in cls if timeframe.matchFeatureStatus(featureStatus)]

    @classmethod
    def statusIncludesTimeframes(cls, statusTerm, *timeframeTerms):
        """Return a SQLite IN … OR … IN … compound clause matching several interacting Timeframe terms against a Feature Status term."""
        allStatusIncludeTimeframesTerms = " or ".join([
            f"({statusTerm} = '{status.name}') and {Timeframe.matchingTimeframes(status)}"
            for status in FeatureStatus])
        return f"({allStatusIncludeTimeframesTerms})"
