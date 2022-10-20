# -*- coding: utf-8 -*-
from ...models.state_machine import StateMachineStatus


class FeatureStatus(StateMachineStatus):
    """Allowed statuses for a Paddock Power feature."""
    Drafted = "Drafted"
    Planned = "Planned"
    Built = "Built"
    PlannedSuperseded = "Superseded (was Planned)"
    BuiltSuperseded = "Superseded (was Built)"
    Archived = "Archived"
    Undefined = "Undefined"

    def toColour(self):
        """Get the colour associated with this status."""
        if self in [FeatureStatus.Undefined, FeatureStatus.Drafted]:
            return (250, 218, 221, 100)
        elif self == FeatureStatus.Planned:
            return (163, 195, 215, 100)
        elif self == FeatureStatus.Built:
            return (215, 195, 163)
        elif self == FeatureStatus.PlannedSuperseded:
            return (147, 151, 153, 100)
        elif self == FeatureStatus.BuiltSuperseded:
            return (147, 151, 153, 100)
        elif self == FeatureStatus.Archived:
            raise NotImplementedError("Archived status not implemented")
        else:
            raise NotImplementedError("Unknown status not implemented")

    def toForegroundColour(self):
        """Get the foreground colour associated with this status."""
        if self in [FeatureStatus.Undefined, FeatureStatus.Drafted]:
            return (0, 0, 0)
        elif self == FeatureStatus.Planned:
            return (255, 255, 255)
        elif self == FeatureStatus.Built:
            return (0, 0, 0)
        elif self == FeatureStatus.PlannedSuperseded:
            return (0, 0, 0)
        elif self == FeatureStatus.BuiltSuperseded:
            return (0, 0, 0)
        elif self == FeatureStatus.Archived:
            raise NotImplementedError("Archived status not implemented")
        else:
            raise NotImplementedError("Unknown status not implemented")
