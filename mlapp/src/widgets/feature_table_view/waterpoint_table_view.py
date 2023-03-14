# -*- coding: utf-8 -*-
from ...layers.fields import WaterpointSchema
from ...layers.fields.fields import *
from ..waterpoint_details import WaterpointDetailsEdit
from .feature_table_action.feature_table_action import FeatureTableAction
from .feature_table_view import FeatureTableView

# WaterpointTableViewSchema = Schema([DefaultTitle,
#                                     WaterpointTypeField,
#                                     Status,
#                                     NearGrazingRadius,
#                                     FarGrazingRadius,
#                                     Longitude,
#                                     Latitude,
#                                     Elevation])


class WaterpointTableView(FeatureTableView):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(WaterpointSchema, None, WaterpointDetailsEdit, parent)
        self.featureLayer = self.workspace.waterpointLayer

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature, FeatureTableAction.editFeature,
                FeatureTableAction.undoTrashFeature, FeatureTableAction.planBuildFeature]
