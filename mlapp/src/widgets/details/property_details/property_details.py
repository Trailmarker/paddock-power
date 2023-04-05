# -*- coding: utf-8 -*-

from ..details import Details


class PropertyDetails(Details):

    def __init__(self, property, parent=None):
        """Constructor."""
        super().__init__(parent)

        self._model = property
        self.refreshUi()

    @property
    def descriptors(self):
        return [
            (lambda m: [m.AREA, m.WATERED_AREA], "Area (km²)", "{0:.2f} ({1:.2f}💧)"),
            (lambda m: [m.PERIMETER], "Perimeter (km)", "{0:.1f}"),
            (lambda m: [m.ESTIMATED_CAPACITY, m.POTENTIAL_CAPACITY], "Estimated capacity (AE)", "{0:.0f} ({1:.0f}📈)")
        ]
