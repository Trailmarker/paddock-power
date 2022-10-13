# -*- coding: utf-8 -*-

from enum import Enum


class PaddockPowerFeatureStatus(Enum):
    """Allowed statuses for a Paddock Power feature."""
    Planned = "Planned",
    Existing = "Existing",
    Superseded = "Superseded",
    Historical = "Historical"
