# -*- coding: utf-8 -*-
from .features import Waterpoint
from .popup_layer_source_mixin import PopupLayerSourceMixin
from .imported_feature_layer import ImportedFeatureLayer
from .waterpoint_popup_layer import WaterpointPopupLayer


class WaterpointLayer(ImportedFeatureLayer, PopupLayerSourceMixin):

    NAME = "Waterpoints"
    STYLE = "waterpoint"

    @property
    def popupLayerTypes(self):
        return [WaterpointPopupLayer]

    @property
    def relativeLayerPosition(self):
        """Makes the Paddock Land Types popups appear *over* the Paddock layer."""
        return 1

    @property
    def zoomPopupLayerOnLoad(self):
        """True for this becaus Waterpoints don't zoom nicely."""
        return True

    @classmethod
    def getFeatureType(cls):
        return Waterpoint

    def __init__(self,
                 workspaceFile,
                 elevationLayer):
        """Create or open a Waterpoint layer."""

        super().__init__(workspaceFile,
                         layerName=WaterpointLayer.NAME,
                         styleName=WaterpointLayer.STYLE)

        self.elevationLayer = elevationLayer
