# -*- coding: utf-8 -*-
from ...layers import PaddockCurrentLandTypesPopupLayer, PaddockFutureLandTypesPopupLayer
from ...models import WorkspaceMixin
from ..feature_table import PaddockTable, CurrentPaddockLandTypesTable, FuturePaddockLandTypesTable, PaddockLandTypesGroupBox, SplitFeatureTablesWidget


class PaddocksWidget(WorkspaceMixin, SplitFeatureTablesWidget):
    """A widget that shows three adjacent feature tables: Paddocks, Current Paddock Land Types, Future Paddock Land Types.
       Selecting items in the Paddock Table adds popup layers to MLA Paddock Power which are then tabulated in the Land Types Tables."""

    def __init__(self, parent=None):
        """Constructor."""
        WorkspaceMixin.__init__(self)
        SplitFeatureTablesWidget.__init__(self, parent)

        self.addFeatureTable("Paddocks", PaddockTable)

        currentPaddockLandTypesGroupBox = PaddockLandTypesGroupBox()
        currentPaddockLandTypesGroupBox.setTitle("Current Paddock Land Types")
        currentPaddockLandTypesGroupBox.featureTableFactory = CurrentPaddockLandTypesTable
        currentPaddockLandTypesGroupBox.popupLayerTypes = [PaddockCurrentLandTypesPopupLayer]
        currentPaddockLandTypesGroupBox.popupLayerSource = self.workspace.paddockLayer
        self.splitter.addWidget(currentPaddockLandTypesGroupBox)
        
        futurePaddockLandTypesGroupBox = PaddockLandTypesGroupBox()
        futurePaddockLandTypesGroupBox.setTitle("Future Paddock Land Types")
        futurePaddockLandTypesGroupBox.featureTableFactory = FuturePaddockLandTypesTable
        futurePaddockLandTypesGroupBox.popupLayerTypes = [PaddockFutureLandTypesPopupLayer]
        futurePaddockLandTypesGroupBox.popupLayerSource = self.workspace.paddockLayer
        self.splitter.addWidget(futurePaddockLandTypesGroupBox)
        
        self.relayout()

