# -*- coding: utf-8 -*-
from ...models.paddock_power_error import PaddockPowerError
from ...spatial.features.paddock import Paddock
from .paddock_list_base import PaddockListBase


class PaddockMiniList(PaddockListBase):
    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)
        self.paddocks = []

    def getPaddocks(self):
        """Get the paddocks."""
        return self.paddocks

    def setPaddocks(self, paddocks):
        """Set the paddocks."""
        if paddocks is None:
            self.paddocks = []
            return

        if not all(isinstance(paddock, Paddock) for paddock in paddocks):
            raise PaddockPowerError(
                "PaddockMiniList.setPaddocks: paddocks must be a list of Paddock objects")
        self.paddocks = paddocks
        self.refreshUi()
