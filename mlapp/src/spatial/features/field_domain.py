# -*- coding: utf-8 -*-
from enum import Enum


class FieldDomain(Enum):
    def __format__(self, _):
        return str(self)

    def __str__(self):
        return self.value
