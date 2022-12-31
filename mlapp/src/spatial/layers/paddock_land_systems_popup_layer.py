# -*- coding: utf-8 -*-
from ..features.paddock_land_system import PaddockLandSystem
from ..schemas.schemas import LAND_SYSTEM_NAME, PADDOCK, TIMEFRAME
from .derived_feature_layer import DerivedFeatureLayer


class PaddockLandSystemsPopupLayer(DerivedFeatureLayer):

    STYLE = "paddock_land_systems_popup"

    def parameteriseQuery(self, paddockId, timeframe):
        return f"""
select *
from "{{0}}"
where "{PADDOCK}" = {paddockId}
and "{TIMEFRAME}" = '{timeframe.name}'
order by "{LAND_SYSTEM_NAME}"
"""

    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return PaddockLandSystem

    def wrapFeature(self, feature):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return self.getFeatureType()(self.paddockLandSystemsLayer, self.conditionTable, feature)

    def __init__(self, project, layerName, paddock, paddockLandSystemsLayer, conditionTable):
        # Burn in the Paddock specific parameters first …
        query = self.parameteriseQuery(paddockId=paddock.id, timeframe=project.currentTimeframe)

        super().__init__(
            project,
            layerName,
            query,
            PaddockLandSystemsPopupLayer.STYLE,
            paddockLandSystemsLayer)

        self.paddockLandSystemsLayer = paddockLandSystemsLayer
        self.conditionTable = conditionTable
