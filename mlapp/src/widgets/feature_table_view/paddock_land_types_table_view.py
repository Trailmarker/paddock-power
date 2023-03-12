# -*- coding: utf-8 -*-
from ...layers.fields import *
from ...layers.paddock_land_types_popup_layer import PaddockCurrentLandTypesPopupLayer, PaddockFutureLandTypesPopupLayer
from ..paddock_land_type_details import PaddockLandTypeDetails, PaddockLandTypeDetailsEdit
from .feature_table_action import FeatureTableAction
from .popup_table_view import PopupTableView


PaddockLandTypesTableViewSchema = Schema([AreaTitle,
                                          # PaddockName,
                                          LandTypeName,
                                          ConditionTypeField,
                                          WateredArea,
                                          # EstimatedCapacityPerArea,
                                          # PotentialCapacityPerArea,
                                          EstimatedCapacity,
                                          PotentialCapacity])


class PaddockLandTypesTableView(PopupTableView):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(PaddockLandTypesTableViewSchema, PaddockLandTypeDetails, PaddockLandTypeDetailsEdit, parent)

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature, FeatureTableAction.editFeature]
    

class CurrentPaddockLandTypesTableView(PaddockLandTypesTableView):
    """A popup table view for collections of PaddockLandTypes
    in the Current timeframe only."""

    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def popupLayerType(self):
        return PaddockCurrentLandTypesPopupLayer

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
    def popupLayerType(self):
        return PaddockFutureLandTypesPopupLayer

    @property
    def timeframe(self):
        return Timeframe.Future
    
    def onTimeframeChanged(self, timeframe):
        pass

