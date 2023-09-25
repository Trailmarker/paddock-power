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

    def displayedFeatureStatuses(self):
        """Return all Feature Statuses that should be displayed in this Timeframe."""
        if Timeframe[self.name] == Timeframe.Current:
            return [FeatureStatus.Built, FeatureStatus.BuiltSuperseded, FeatureStatus.PlannedSuperseded]
        elif Timeframe[self.name] == Timeframe.Future:
            return [FeatureStatus.Drafted, FeatureStatus.Built, FeatureStatus.Planned]
        elif Timeframe[self.name] == Timeframe.Undefined:
            return []

    def displayFeatureStatus(self, featureStatus):
        """Check if a Feature Status corresponds to this Timeframe."""
        matches = [fs for fs in self.displayedFeatureStatuses()
                   if FeatureStatus[featureStatus.name] == FeatureStatus[fs.name]]
        return bool(matches)

    def matchTimeframe(self, timeframe):
        """Check if a Timeframe corresponds to this Timeframe."""
        return (Timeframe[self.name] == Timeframe[timeframe.name])

    def matchesStatus(self, statusTerm):
        """Return a SQLite IN clause logically matching a Feature Status term against this Timeframe."""
        matchTerms = ", ".join([f"'{status.name}'" for status in self.matchingFeatureStatuses()])
        return f"{statusTerm} in ({matchTerms})"

    def displaysStatus(self, statusTerm):
        """Return a SQLite IN clause matching a Feature Status term against this Timeframe for display purposes."""
        matchTerms = ", ".join([f"'{status.name}'" for status in self.displayedFeatureStatuses()])
        return f"{statusTerm} in ({matchTerms})"

    def matchesStatuses(self, *statusTerms):
        """Return a SQLite IN … AND … IN … compound clause logically matching several interacting Feature Status terms against this Timeframe."""
        includesStatusTerms = " and ".join([self.matchesStatus(statusTerm) for statusTerm in statusTerms])
        return f"({includesStatusTerms})"

    def displaysStatuses(self, *statusTerms):
        """Return a SQLite IN … AND … IN … compound clause matching several interacting Feature Status terms against this Timeframe for display purposes."""
        includesStatusTerms = " and ".join([self.displaysStatus(statusTerm) for statusTerm in statusTerms])
        return f"({includesStatusTerms})"

    def timeframeMatchesStatuses(self, timeframeTerm, *statusTerms):
        """Return a SQLite IN clause logically matching a Timeframe term against this Timeframe."""
        return f"({timeframeTerm} = '{self.name}') and {self.matchesStatuses(*statusTerms)}"

        # matchTerms = ", ".join([f"'{timeframe.name}'" for timeframe in Timeframe.matchingTimeframes(self)])
        # return f"{timeframeTerm} in ({matchTerms})"

    def timeframeDisplaysStatuses(self, timeframeTerm, *statusTerms):
        """Return a SQLite IN clause matching a Timeframe term against this Timeframe for display purposes."""
        return f"({timeframeTerm} = '{self.name}') and {self.displaysStatuses(*statusTerms)}"

    @classmethod
    def timeframesMatchStatuses(cls, timeframeTerm, *statusTerms):
        """Return a SQLite IN … AND … IN … compound clause logically matching several interacting Feature Status terms against a Timeframe term."""
        allTimeframeMatchesStatusesTerms = " or ".join(
            [timeframe.timeframeMatchesStatuses(timeframeTerm, *statusTerms) for timeframe in cls])
        return f"({allTimeframeMatchesStatusesTerms})"

    @classmethod
    def timeframesDisplayStatuses(cls, timeframeTerm, *statusTerms):
        """Return a SQLite IN … AND … IN … compound clause matching several interacting Feature Status terms against a Timeframe term for display purposes."""
        allTimeframeDisplaysStatusesTerms = " or ".join(
            [timeframe.timeframeDisplaysStatuses(timeframeTerm, *statusTerms) for timeframe in cls])
        return f"({allTimeframeDisplaysStatusesTerms})"

    # @classmethod
    # def matchingTimeframes(cls, featureStatus):
    #     """Return all Timeframes that correspond to a Feature Status."""
    #     return [timeframe for timeframe in cls if timeframe.matchFeatureStatus(featureStatus)]

    # @classmethod
    # def statusIncludesTimeframes(cls, statusTerm, *timeframeTerms):
    #     """Return a SQLite IN … OR … IN … compound clause matching several interacting Timeframe terms against a Feature Status term."""
    #     allStatusIncludeTimeframesTerms = " or ".join([
    #         f"({statusTerm} = '{status.name}') and {Timeframe.matchingTimeframes(status)}"
    #         for status in FeatureStatus])
    #     return f"({allStatusIncludeTimeframesTerms})"
