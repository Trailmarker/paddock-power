# -*- coding: utf-8 -*-
from .field_domain import FieldDomain


class WaterpointType(FieldDomain):
    Bore = "Bore"
    Dam = "Dam"
    Trough = "Trough"
    TurkeyNest = "Turkey Nest"
    WaterTank = "Water Tank"
    Waterhole = "Waterhole"

    def givesWater(self):
        return self.name in [t.name for t in [WaterpointType.Dam, WaterpointType.Trough, WaterpointType.Waterhole]]

    @classmethod
    def givesWaterSql(cls, term):
        """Return a SQL expression that will return True if the Waterpoint Type gives water."""
        return f"{term} in ('{WaterpointType.Dam.name}', '{WaterpointType.Trough.name}', '{WaterpointType.Waterhole.name}')"
