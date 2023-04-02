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

    def connectWorkspace(self, workspace):
        self.workspace = workspace
        
        # Convenience attributes, eg workspace.paddockLayer = self
        # TODO this is a bit of hack that can cause various issues
        typeName = type(self).__name__
        attrName = typeName[:1].lower() + typeName[1:]
        setattr(self.workspace, attrName, self)
