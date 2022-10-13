# -*- coding: utf-8 -*-
from enum import Enum


class FeatureStatus(Enum):
    """Allowed statuses for a Paddock Power feature."""
    Draft = "Draft"
    Planned = "Planned",
    Existing = "Existing",
    Superseded = "Superseded",
    Historical = "Historical",
    Unknown = "Unknown"
