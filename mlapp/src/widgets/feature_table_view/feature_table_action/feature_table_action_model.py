# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, abstractproperty

from qgis.PyQt.QtCore import QObject

from ....models import QtAbstractMeta


class FeatureTableActionModel(QObject, ABC, metaclass=QtAbstractMeta):

    def __init__(self):
        QObject.__init__(self)

    @abstractmethod
    def doAction(self, index):
        """Perform the action associated with the given index."""
        pass

    def getFeature(self, index):
        """The feature associated with the current index."""
        fid = index.model().rowToId(index.row())
        return index.model().layer().getFeature(fid)

    @abstractproperty
    def featureTableAction(self):
        """The feature table action."""
        pass

    @classmethod
    def bumpCacheAfterAction(self):
        """Invalidate the cache after a call to doAction."""
        return False

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
