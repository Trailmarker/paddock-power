# -*- coding: utf-8 -*-
from ...layers.fields import PaddockLandTypeSchema, Timeframe
from ..details import PaddockLandTypeDetails, PaddockLandTypeDetailsEdit
from .feature_table import FeatureTable
from .feature_table_action import FeatureTableAction


# PaddockLandTypesTableSchema = Schema([AreaTitle,
#                                           # PaddockName,
#                                           LandTypeName,
#                                           ConditionTypeField,
#                                           WateredArea,
#                                           # EstimatedCapacityPerArea,
#                                           # PotentialCapacityPerArea,
#                                           EstimatedCapacity,
#                                           PotentialCapacity])


class PaddockLandTypesTable(FeatureTable):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(PaddockLandTypeSchema, PaddockLandTypeDetails, PaddockLandTypeDetailsEdit, parent)

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature, FeatureTableAction.editFeature]
    

class CurrentPaddockLandTypesTable(PaddockLandTypesTable):
    """A popup table view for collections of PaddockLandTypes
    in the Current timeframe only."""

    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def timeframe(self):
        return Timeframe.Current
    
    def onTimeframeChanged(self, timeframe):
        pass



class FuturePaddockLandTypesTable(PaddockLandTypesTable):
    """A popup table view for collections of PaddockLandTypes
    in the Future timeframe only."""

    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def timeframe(self):
        return Timeframe.Future
    
    def onTimeframeChanged(self, timeframe):
        pass

