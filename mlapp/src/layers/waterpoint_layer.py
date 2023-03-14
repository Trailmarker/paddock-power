# -*- coding: utf-8 -*-
from .features import Waterpoint
from .popup_layer_source_mixin import PopupLayerSourceMixin
from .imported_feature_layer import ImportedFeatureLayer
from .waterpoint_buffer_popup_layer import WaterpointBufferPopupLayer


class WaterpointLayer(ImportedFeatureLayer, PopupLayerSourceMixin):

    LAYER_NAME = "Waterpoints"
    STYLE = "waterpoint"

    @classmethod
    def getFeatureType(cls):
        return Waterpoint

    def __init__(self,
                 workspaceFile,
                 *dependentLayers):
        """Create or open a Waterpoint layer."""
        ImportedFeatureLayer.__init__(self, workspaceFile,
                                      layerName=WaterpointLayer.defaultName(),
                                      styleName=WaterpointLayer.defaultStyle())
        PopupLayerSourceMixin.__init__(self)
        self.connectPopups()

    @property
    def hasPopups(self):
        return True

    @property
    def popupLayerTypes(self):
        return [WaterpointBufferPopupLayer]

    @property
    def relativeLayerPosition(self):
        """Makes the Paddock Land Types popups appear *over* the Paddock layer."""
        return 1

    @property
    def zoomPopupLayerOnLoad(self):
        """True for this becaus Waterpoints don't zoom nicely."""
        return True
