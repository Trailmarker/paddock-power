# -*- coding: utf-8 -*-
import sip  # type: ignore

from qgis.PyQt.QtCore import QSize
from qgis.PyQt.QtWidgets import QGroupBox, QSizePolicy, QVBoxLayout

from ...layers.popup_layer_consumer_mixin import PopupLayerConsumerMixin
from ...models import WorkspaceMixin


class FeatureTableGroupBox(WorkspaceMixin, PopupLayerConsumerMixin, QGroupBox):

    def __init__(self, parent=None):
        WorkspaceMixin.__init__(self)
        PopupLayerConsumerMixin.__init__(self)
        QGroupBox.__init__(self, parent)

        # Keep a top margin of 1, everything else is 0
        # TODO do this with a stylesheet
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 1, 0, 0)
        self.setLayout(self.verticalLayout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._featureTableFactory = None
        self._featureTable = None
        self._popupLayerTypes = []

        # Not visible until the feature layer is set
        self.setVisible(False)

    @property
    def featureTableFactory(self):
        """Return the FeatureTable factory (usually just a FeatureTable specialisation) used to create the FeatureTables of this group box."""
        return self._featureTableFactory

    @featureTableFactory.setter
    def featureTableFactory(self, featureTableFactory):
        """Set the FeatureTable factory."""
        self._featureTableFactory = featureTableFactory
        self._featureTable = self.featureTableFactory(self) if self._featureTableFactory else None
        self.layout().addWidget(self.featureTable)

    @property
    def featureTable(self):
        """Safely retrieve the underlying FeatureTable object, if any."""
        return self._featureTable if not sip.isdeleted(self._featureTable) else None

    @property
    def featureLayer(self):
        """Return the feature layer for the feature table, if we have one, or None."""
        return self.featureTable.featureLayer if self.featureTable else None

    def removeFeatureTable(self):
        """Remove any current FeatureTable from the widget."""
        if self.featureTable:
            self.layout().removeWidget(self.featureTable)
            self.featureTable.deleteLater()

    @featureLayer.setter
    def featureLayer(self, featureLayer):
        """Create a new FeatureTable and set its feature layer, if we have a configured FeatureTable factory, or clear everything."""
        self.removeFeatureTable()

        showTable = bool(featureLayer) and bool(self.featureTableFactory) and featureLayer.featureCount() > 0
        if showTable:
            self._featureTable = self.featureTableFactory(self)
            self.featureTable.featureLayer = featureLayer
            self.layout().addWidget(self.featureTable)

        # Becomes visible when the feature layer is set
        self.setVisible(showTable)

        if featureLayer:
            self.setTitle(featureLayer.name())

    def sizeHint(self):
        """Return the size hint for the widget."""
        if not self.featureTableFactory:
            return super().sizeHint()
        elif self.featureTable:
            # Pump for our QGroupBox margins
            hint = self.featureTable.sizeHint()
            return QSize(hint.width() + 10, hint.height() + 20)
        else:
            return super().sizeHint()

    # Implement PopupLayerConsumerMixin

    @property
    def popupLayerTypes(self):
        """Return the popup layer types that this widget can handle."""
        return self._popupLayerTypes

    @popupLayerTypes.setter
    def popupLayerTypes(self, popupLayerTypes):
        """Set the popup layer types that this widget can handle."""
        self._popupLayerTypes = popupLayerTypes

    def onPopupLayerAdded(self, layerId):
        """Handle a new layer from the popup layer source (if any)."""
        featureLayer = self.workspace.mapLayer(layerId)
        if type(featureLayer) not in self.popupLayerTypes:
            return
        self.featureLayer = featureLayer

    def onPopupLayerRemoved(self):
        """Override in subclass to handle popup layer removed."""
        self.featureLayer = None
