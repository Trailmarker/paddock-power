# -*- coding: utf-8 -*-
from abc import abstractmethod
from .feature import Feature


class StatusFeature(Feature):

    @abstractmethod
    def planFeature(self):
        """Plan a Feature."""
        pass

    @abstractmethod
    def undoPlanFeature(self):
        """Undo planning a Feature."""
        pass

    @abstractmethod
    def buildFeature(self):
        """Build a Feature."""
        pass

    @abstractmethod
    def undoBuildFeature(self):
        """Undo Building a Feature."""
        pass

    @abstractmethod
    def supersedeFeature(self):
        """Supersede a Feature."""
        pass

    @abstractmethod
    def undoSupersedeFeature(self):
        """Undo superseding a Feature."""
        pass

    @abstractmethod
    def trashFeature(self):
        """Trash a Feature."""
        pass

    @abstractmethod
    def archiveFeature(self):
        """Archive a Feature."""
        pass
