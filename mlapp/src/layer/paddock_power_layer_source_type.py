# -*- coding: utf-8 -*-

from enum import Enum


class PaddockPowerLayerSourceType(Enum):
    """Disambiguate between sources for a Paddock Power layer."""
    File = 1,
    Memory = 2
