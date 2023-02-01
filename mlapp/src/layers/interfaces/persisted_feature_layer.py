# -*- coding: utf-8 -*-
from .map_layer import MapLayer
from .persisted_layer import PersistedLayer


class PersistedFeatureLayer(MapLayer, PersistedLayer):
    pass
