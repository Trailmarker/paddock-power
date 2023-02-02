# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Layer(ABC):
    """A generic layer - could be GIS or some other thing, like a SQLite table."""

    @abstractmethod
    def name(self):
        """Return the name of the layer."""
        pass

    @abstractmethod
    def id(self):
        """Return the id of the layer."""
        pass
