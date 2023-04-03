# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Layer(ABC):
    """A generic layer - could be GIS or some other thing, like a SQLite table."""

    def __init__(self):
        self.workspace = None

    @abstractmethod
    def name(self):
        """Return the name of the layer."""
        pass

    @abstractmethod
    def id(self):
        """Return the id of the layer."""
        pass

    @classmethod
    def variableName(cls):
        """Return a variable name for this layer type, eg 'basePaddockLayer' or 'elevationLayer'."""
        # Just use the lower-cased class name
        return cls.__name__[:1].lower() + cls.__name__[1:]

    def connectWorkspace(self, workspace):
        self.workspace = workspace
        setattr(self.workspace, self.variableName(), self)
