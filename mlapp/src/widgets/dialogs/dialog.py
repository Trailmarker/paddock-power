# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from qgis.PyQt.QtWidgets import QDialog

from ...models import QtAbstractMeta, WorkspaceMixin
from ...utils import PLUGIN_NAME


class Dialog(ABC, WorkspaceMixin, QDialog, metaclass=QtAbstractMeta):
    f"""Base class for {PLUGIN_NAME} dialogs."""

    def __init__(self, parent=None):
        """Constructor."""
        WorkspaceMixin.__init__(self)
        QDialog.__init__(self, parent)

    @property
    @abstractmethod
    def dialogRole(self):
        pass

    def setWindowTitle(self, title):
        """Set the dialog's title using a standard format."""
        super().setWindowTitle(f"{PLUGIN_NAME} | {self.dialogRole}{(' — ' + title) if title else ''}")

    def showEvent(self, event):
        """Override the show event to also adjust the dialog layout."""
        self.adjustSize()
        self.resize(max(800, self.minimumWidth(), self.width()), self.height())
        super().showEvent(event)

    # def closeEvent(self, event):
    #     """Override the close event to also close the dialog."""
    #     self.reject()
    #     super().closeEvent(event)