# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, abstractproperty

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtGui import QIcon

from qgis.gui import QgsAttributeTableModel, QgsAttributeTableFilterModel

from ....models import QtAbstractMeta, WorkspaceMixin
from ....utils import PLUGIN_FOLDER


class FeatureTableActionModel(QObject, WorkspaceMixin, ABC, metaclass=QtAbstractMeta):

    _lockedIcon = QIcon(f':/plugins/{PLUGIN_FOLDER}/images/locked.png')

    def __init__(self):
        QObject.__init__(self)
        WorkspaceMixin.__init__(self)

    @abstractmethod
    def doAction(self, index):
        """Perform the action associated with the given index."""
        pass

    def getFeature(self, index):
        """The feature associated with the current index."""
        model = index.model()
        # Beware: the call signatures of rowToId are different for
        # QgsAttributeTableModel and QgsAttributeTableFilterModel
        if isinstance(model, QgsAttributeTableFilterModel):
            # TODO check this
            fid = model.rowToId(index)
        elif isinstance(model, QgsAttributeTableModel):
            fid = model.rowToId(index.row())

        return model.layer().getFeature(fid)

    @abstractproperty
    def featureTableAction(self):
        """The feature table action."""
        pass

    @property
    def isValid(self):
        """Whether the action is validly configurad."""
        return True

    @abstractmethod
    def icon(self, index):
        """The icon to paint for the action."""
        pass

    @property
    def lockedIcon(self):
        """The default 'locked' icon for locked actions."""
        return self._lockedIcon

    @property
    def locked(self):
        """Whether the action is locked."""
        return False

    @abstractmethod
    def description(self, index):
        """The description of the action, given the matching column."""
        pass

    def toolTip(self, index):
        """The tooltip of the action, given the matching column."""
        return self.description(index)
