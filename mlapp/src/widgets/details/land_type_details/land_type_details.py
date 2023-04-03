# -*- coding: utf-8 -*-

from ..details import Details


class LandTypeDetails(Details):

    def __init__(self, landType, parent=None):
        """Constructor."""
        super().__init__(parent)

        self._model = landType
        self.refreshUi()

    @property
    def descriptors(self):
        return [
            (lambda m: m.AREA, "Area (km²)", "{0:.2f}"),
            (lambda m: m.PERIMETER, "Perimeter (km)", "{0:.1f}"),
            (lambda m: m.OPTIMAL_CAPACITY_PER_AREA, "Best AE/km² (if Condition is 'A')", "{0:.1f}"),
        ]
