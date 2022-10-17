# -*- coding: utf-8 -*-

from enum import Enum


class FeatureLayerSourceType(Enum):
    """Disambiguate between sources for a Paddock Power layer."""
    File = 1,
    Memory = 2
