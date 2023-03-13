# -*- coding: utf-8 -*-
from enum import Enum


class FeatureTableAction(Enum):
    """Up to the first five visible columns of the FeatureTableModel are action columns as follows. Not all apply
       to all features, for example only Fences and Pipelines will have a 'viewFeatureProfile' action."""
    selectFeature = 0
    viewFeatureDetails = 1
    editFeature = 2
    undoTrashFeature = 3
    planBuildFeature = 4
    viewFeatureProfile = 5
