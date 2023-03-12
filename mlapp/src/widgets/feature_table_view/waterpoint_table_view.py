# -*- coding: utf-8 -*-
from mlapp.src.widgets.feature_table_view.feature_table_action.feature_table_action import FeatureTableAction
from ...layers.fields import Schema
from ...layers.fields.fields import *
from ..waterpoint_details import WaterpointDetailsEdit
from .feature_table_view import FeatureTableView

WaterpointTableViewSchema = Schema([DefaultTitle,
                                    WaterpointTypeField,
                                    Status,
                                    NearGrazingRadius,
                                    FarGrazingRadius,
                                    Longitude,
                                    Latitude,
                                    Elevation])


class WaterpointTableView(FeatureTableView):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(WaterpointTableViewSchema, WaterpointDetailsEdit, parent)
        self.featureLayer = self.workspace.waterpointLayer

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature, FeatureTableAction.editFeature,
                FeatureTableAction.undoTrashFeature, FeatureTableAction.planBuildFeature]
