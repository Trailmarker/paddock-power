# -*- coding: utf-8 -*-
from .field_domain import FieldDomain


class WaterpointType(FieldDomain):
    Bore = "Bore"
    Dam = "Dam"
    Trough = "Trough"
    TurkeyNest = "Turkey Nest"
    WaterTank = "Water Tank"
    Waterhole = "Waterhole"

    @classmethod
    def givesWater(cls, term):
        """Return a SQL expression that will return True if the Waterpoint Type gives water."""
        return f"{term} in ('{cls.Bore}', '{WaterpointType.Dam.name}', '{WaterpointType.Trough.name}', '{WaterpointType.Waterhole.name}')"
