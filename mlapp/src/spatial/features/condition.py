# -*- coding: utf-8 -*-
from .field_domain import FieldDomain


class Condition(FieldDomain):
    """Allowed conditions for a Land Type, Paddock and Water Buffer combination."""
    A = "A"
    B = "B"
    C = "C"
    D = "D"
