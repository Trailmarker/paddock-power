# -*- coding: utf-8 -*-
from enum import Enum


class FieldDomain(Enum):
    def __format__(self, _):
        return str(self)

    def __str__(self):
        return self.value

    def toColour(self):
        """Get the theme colour associated with this domain value."""
        return (255, 255, 255)

    def toForegroundColour(self):
        """Get the pen colour associated with this domain value."""
        return (0, 0, 0)
