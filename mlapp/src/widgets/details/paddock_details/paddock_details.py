# -*- coding: utf-8 -*-

from ..details import Details


class PaddockDetails(Details):

    def __init__(self, paddock, parent=None):
        """Constructor."""
        super().__init__(parent)

        self._model = paddock
        self.refreshUi()

    @property
    def descriptors(self):
        return [
            (lambda m: m.AREA, "Area (km²)", "{0:.2f}"),
            (lambda m: m.WATERED_AREA, "Watered (km²)", "{0:.2f}"),
            (lambda m: m.PERIMETER, "Perimeter (km)", "{0:.1f}"),
            (lambda m: m.ESTIMATED_CAPACITY, "Estimated capacity (AE)", "{0:.0f}"),
            (lambda m: m.POTENTIAL_CAPACITY, "Potential capacity (AE)", "{0:.0f}"),
            (lambda m: m.ESTIMATED_CAPACITY_PER_AREA, "Watered carrying capacity (AE/km²)", "{0:.1f}"),
        ]
