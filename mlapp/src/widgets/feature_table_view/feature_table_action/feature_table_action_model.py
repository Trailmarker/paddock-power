# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, abstractproperty

from qgis.PyQt.QtCore import QObject

from ....models import QtAbstractMeta


class FeatureTableActionModel(ABC, QObject, metaclass=QtAbstractMeta):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.feature = None

    @abstractmethod
    def doAction(self, index):
        """Perform the action associated with the given index."""
        pass

    def getFeature(self, index):
        """The feature associated with the current index."""
        fid = index.model().rowToId(index)

        # This value gets stored here so that we can use it again when the user clicks on the cell.
        self.feature = index.model().layer().getFeature(fid)
        return self.feature

    @abstractproperty
    def featureTableAction(self):
        """The feature table action."""
        pass

    @abstractmethod
    def icon(self, index):
        """The icon to paint for the action."""
        pass

    @abstractmethod
    def description(self, index):
        """The description of the action, given the matching column."""
        pass

    def toolTip(self, index):
        """The tooltip of the action, given the matching column."""
        return self.description(index)
