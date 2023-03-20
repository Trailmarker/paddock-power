# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon

from ..utils import PLUGIN_FOLDER

from .features import Waterpoint
from .popup_layer_source_mixin import PopupLayerSourceMixin
from .importable_feature_layer import ImportableFeatureLayer
from .waterpoint_buffer_popup_layer import WaterpointBufferPopupLayer


class WaterpointLayer(ImportableFeatureLayer, PopupLayerSourceMixin):

    LAYER_NAME = "Waterpoints"
    STYLE = "waterpoint"

    @classmethod
    def getFeatureType(cls):
        return Waterpoint

    def __init__(self,
                 workspaceFile,
                 *dependentLayers):
        """Create or open a Waterpoint layer."""
        ImportableFeatureLayer.__init__(self, workspaceFile,
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
    
    @classmethod    
    def icon(cls):
        """The icon to paint to represent this layer."""
        return QIcon(f":/plugins/{PLUGIN_FOLDER}/images/waterpoint.png")
