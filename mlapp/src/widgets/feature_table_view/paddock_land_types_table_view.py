# -*- coding: utf-8 -*-
from ...layers.fields import Schema
from ...layers.fields.fields import *
from ..paddock_land_type_details import PaddockLandTypeDetailsEdit
from .feature_table_view import FeatureTableView

PaddockLandTypesTableViewSchema = Schema([AreaTitle,
                                          PaddockName,
                                          LandTypeName,
                                          ConditionTypeField,
                                          WateredArea,
                                          EstimatedCapacityPerArea,
                                          PotentialCapacityPerArea,
                                          EstimatedCapacity,
                                          PotentialCapacity])


class PaddockLandTypesTableView(FeatureTableView):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(PaddockLandTypesTableViewSchema, PaddockLandTypeDetailsEdit, parent)
        self.featureLayer = self.workspace.paddockLayer
