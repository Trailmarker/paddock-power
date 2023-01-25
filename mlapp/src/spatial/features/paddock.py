# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject

from ...utils import qgsDebug
from ..layers.condition_table import ConditionTable
from ..layers.derived_metric_paddock_layer import DerivedMetricPaddockLayer
from ..layers.paddock_land_types_layer import PaddockLandTypesLayer
from ..layers.paddock_land_types_popup_layer import PaddockLandTypesPopupLayer
from ..fields.schemas import PaddockSchema
from .area_feature import AreaFeature
from .edits import Edits
from .feature_action import FeatureAction


@PaddockSchema.addSchema()
class Paddock(AreaFeature):

    popupLayerAdded = pyqtSignal(PaddockLandTypesPopupLayer)
    popupLayerRemoved = pyqtSignal()

    def __init__(self, featureLayer, conditionTable: ConditionTable, existingFeature=None):
        """Create a new Paddock."""
        super().__init__(featureLayer, existingFeature=existingFeature)

        self.conditionTable = conditionTable

        self._popupLayerId = None
        self.crossedPaddockId = None

    @property
    def title(self):
        return f"{self.name} ({self.featureArea:.2f} km²)"

    def upsert(self):
        """Upsert the Paddock and also upsert a Condition record if the Paddock has been split."""
        super().upsert()

        if self.crossedPaddockId:
            # qgsDebug(f"{self}.conditionTable.upsertSplit({self.id}, {self.crossedPaddockId})")
            self.conditionTable.upsertSplit(self.id, self.crossedPaddockId)

        self.featureUpserted.emit()
        return self.id

    @FeatureAction.draft.handler()
    def draftFeature(self, geometry, name):
        """Draft a Paddock."""
        self.name = name
        self.geometry = geometry
        return Edits.upsert(self)

    @FeatureAction.plan.handler()
    def planFeature(self, fence, crossedPaddock=None):
        self.buildFence = fence.buildOrder
        self.crossedPaddockId = crossedPaddock.id if crossedPaddock else None
        return Edits.upsert(self)

    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        self.buildFence = None
        return Edits.delete(self)

    @FeatureAction.supersede.handler()
    def supersedeFeature(self, fence):
        self.buildFence = fence.buildOrder
        return Edits.upsert(self)

    @FeatureAction.undoSupersede.handler()
    def undoSupersedeFeature(self):
        self.buildFence = None
        return Edits.upsert(self)
