# -*- coding: utf-8 -*-
from ...layers.fields import PaddockLandTypeSchema, Timeframe
from ..paddock_land_type_details import PaddockLandTypeDetails, PaddockLandTypeDetailsEdit
from .feature_table_action import FeatureTableAction
from .feature_table_view import FeatureTableView


# PaddockLandTypesTableViewSchema = Schema([AreaTitle,
#                                           # PaddockName,
#                                           LandTypeName,
#                                           ConditionTypeField,
#                                           WateredArea,
#                                           # EstimatedCapacityPerArea,
#                                           # PotentialCapacityPerArea,
#                                           EstimatedCapacity,
#                                           PotentialCapacity])


class PaddockLandTypesTableView(FeatureTableView):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(PaddockLandTypeSchema, PaddockLandTypeDetails, PaddockLandTypeDetailsEdit, parent)

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature, FeatureTableAction.editFeature]
    

class CurrentPaddockLandTypesTableView(PaddockLandTypesTableView):
    """A popup table view for collections of PaddockLandTypes
    in the Current timeframe only."""

    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def timeframe(self):
        return Timeframe.Current
    
    def onTimeframeChanged(self, timeframe):
        pass



class FuturePaddockLandTypesTableView(PaddockLandTypesTableView):
    """A popup table view for collections of PaddockLandTypes
    in the Future timeframe only."""

    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def timeframe(self):
        return Timeframe.Future
    
    def onTimeframeChanged(self, timeframe):
        pass

