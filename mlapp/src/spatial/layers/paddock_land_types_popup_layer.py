# -*- coding: utf-8 -*-
from ..features.paddock_land_type import PaddockLandType
from ..fields.schemas import LAND_TYPE_NAME, PADDOCK, TIMEFRAME
from .derived_feature_layer import DerivedFeatureLayer


class PaddockLandTypesPopupLayer(DerivedFeatureLayer):

    STYLE = "paddock_land_types_popup"

    def parameteriseQuery(self, paddockId, timeframe):
        return f"""
select *
from "{{0}}"
where "{PADDOCK}" = {paddockId}
and "{TIMEFRAME}" = '{timeframe.name}'
order by "{LAND_TYPE_NAME}"
"""

    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return PaddockLandType

    def wrapFeature(self, feature):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return self.getFeatureType()(self.paddockLandTypesLayer, self.conditionTable, feature)

    def __init__(self, project, layerName, paddock, paddockLandTypesLayer, conditionTable):
        # Burn in the Paddock specific parameters first …
        query = self.parameteriseQuery(paddockId=paddock.id, timeframe=project.currentTimeframe)

        super().__init__(
            project,
            layerName,
            query,
            PaddockLandTypesPopupLayer.STYLE,
            paddockLandTypesLayer)

        self.paddockLandTypesLayer = paddockLandTypesLayer
        self.conditionTable = conditionTable
