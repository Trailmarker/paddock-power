# -*- coding: utf-8 -*-
from .field_domain import FieldDomain


class WaterpointType(FieldDomain):
    Bore = "Bore"
    Dam = "Dam"
    Trough = "Trough"
    Tank = "Tank"
    TurkeyNest = "Turkey Nest"
    WaterTank = "Water Tank"
    Waterhole = "Waterhole"


class WaterpointBufferType(FieldDomain):
    Near = "Near Buffer"
    Far = "Far Buffer"
