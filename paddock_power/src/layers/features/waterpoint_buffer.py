# -*- coding: utf-8 -*-
from ..fields import WaterpointBufferSchema, FID, NAME, STATUS, TIMEFRAME, WATERPOINT_TYPE, GRAZING_RADIUS_TYPE
from .persisted_feature import PersistedFeature


@WaterpointBufferSchema.addSchema()
class WaterpointBuffer(PersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Waterpoint Buffer."""
        super().__init__(featureLayer, existingFeature)

    def __repr__(self):
        """Return a string representation of the Feature."""
        attrs = [
            f"{f}={self.attribute(f)}" for f in [
                FID,
                NAME,
                STATUS,
                TIMEFRAME,
                WATERPOINT_TYPE,
                GRAZING_RADIUS_TYPE] if self.hasField(f)]
        return f"{type(self).__name__}({', '.join(attrs)})"

    @classmethod
    def focusOnSelect(cls):
        """Return True if the app should focus on this type of Feature when selected."""
        return False
