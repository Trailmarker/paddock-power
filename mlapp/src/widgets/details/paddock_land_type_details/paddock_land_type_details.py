# -*- coding: utf-8 -*-
from ..details import Details


class PaddockLandTypeDetails(Details):

    def __init__(self, paddockLandType, parent=None):
        """Constructor."""
        super().__init__(parent)

        self._model = paddockLandType
        self.refreshUi()

    @property
    def descriptors(self):
        return [
            (lambda m: [m.LAND_TYPE_NAME], "Land type name", "{0}"),
            (lambda m: [m.CONDITION_TYPE.value], "Condition", "{0}"),
            (lambda m: [m.AREA, m.WATERED_AREA], "Area (km²)", "{0:.2f} ({1:.2f}💧)"),
            (lambda m: [m.ESTIMATED_CAPACITY, m.POTENTIAL_CAPACITY], "Estimated capacity (AE)", "{0:.0f} ({1:.0f}📈)")
            # (lambda m: [m.ESTIMATED_CAPACITY_PER_AREA], "Watered carrying capacity (AE/km²)", "{0:.1f}"),
        ]

