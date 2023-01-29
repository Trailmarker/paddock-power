# -*- coding: utf-8 -*-
from ..fields.schemas import MetricPaddockSchema
from ..layers.metric_paddock_land_types_popup_layer import MetricPaddockCurrentLandTypesPopupLayer, MetricPaddockFutureLandTypesPopupLayer
from ..layers.paddock_layer import PaddockLayer
from ..layers.paddock_land_types_layer import PaddockLandTypesLayer
from .feature_action import FeatureAction
from .status_feature import StatusFeature

from ..layers.mixins.popup_feature_mixin import PopupFeatureMixin


@MetricPaddockSchema.addSchema()
class MetricPaddock(StatusFeature, PopupFeatureMixin):

    def __init__(self, featureLayer, existingFeature=None):
        """Initialise a new Metric Paddock."""
        StatusFeature.__init__(self, featureLayer, existingFeature)
        PopupFeatureMixin.__init__(self)

    @property
    def TITLE(self):
        return f"{self.NAME} ({self.AREA:.2f} km²)"

    @property
    def paddockLayer(self):
        return self.workspaceLayer(PaddockLayer)

    @property
    def paddockLandTypesLayer(self):
        return self.workspaceLayer(PaddockLandTypesLayer)

    # Completing the required definition of PopupFeatureMixin above
    @property
    def popupLayerTypes(self):
        return [MetricPaddockCurrentLandTypesPopupLayer, MetricPaddockFutureLandTypesPopupLayer]

    # All workflow functions are deferred to the underlying Paddock for this MetricPaddock
    def getPaddock(self):
        """Get the Paddock that this Metric Paddock is associated with."""
        return self.paddockLayer.getFeature(self.paddock)

    @FeatureAction.draft.handler()
    def draftFeature(self, geometry, name):
        """Draft a Paddock."""
        return self.getPaddock().draftFeature(geometry, name)

    @FeatureAction.plan.handler()
    def planFeature(self, fence, crossedPaddock=None):
        return self.getPaddock().planFeature(fence, crossedPaddock)

    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        return self.getPaddock().undoPlanFeature()

    @FeatureAction.supersede.handler()
    def supersedeFeature(self, fence):
        return self.getPaddock().supersedeFeature(fence)

    @FeatureAction.undoSupersede.handler()
    def undoSupersedeFeature(self):
        return self.getPaddock().undoSupersedeFeature()
