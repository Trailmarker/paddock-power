# -*- coding: utf-8 -*-

from ..details import Details


class WaterpointDetails(Details):

    def __init__(self, waterpoint, parent=None):
        """Constructor."""
        super().__init__(parent)

        self._model = waterpoint
        self.refreshUi()

    @property
    def descriptors(self):
        return [
            (lambda m: [m.NEAR_GRAZING_RADIUS], "Near Grazing Radius (m)", "{0:0f}"),
            (lambda m: [m.FAR_GRAZING_RADIUS], "Far Grazing Radius (m)", "{0:0f}"),
            (lambda m: [m.WATERPOINT_TYPE], "Waterpoint Type", "{0}"),
            (lambda m: [m.ACTIVE], "Active", "{0}")
        ]