# -*- coding: utf-8 -*-
from qgis.core import QgsFeature

from ...models.paddock_power_error import PaddockPowerError
from .paddock_list_base import PaddockListBase


class PaddockMiniList(PaddockListBase):
    def __init__(self, paddocks, parent=None):
        """Constructor."""
        super(PaddockListBase, self).__init__(parent)

        self.setPaddocks(paddocks)

    def getPaddocks(self):
        """Get the paddocks."""
        return self.paddocks

    def setPaddocks(self, paddocks):
        """Set the paddocks."""
        if paddocks is None or not all(isinstance(paddock, QgsFeature) for paddock in paddocks):
            raise PaddockPowerError(
                "PaddockMiniList.setPaddocks: paddocks must be a list of QgsFeature objects")
        self.paddocks = paddocks
        self.refreshUi()
