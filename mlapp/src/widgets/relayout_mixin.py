# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

import sip  # type: ignore

from qgis.PyQt.QtCore import QTimer

from ..models import QtAbstractMeta


class RelayoutMixin(ABC, metaclass=QtAbstractMeta):
    """Mixin class to support re-laying out a widget after a resize event has finished.
       Must be mixed into a QWidget which uses the QtAbstractMeta metaclass."""

    # Time to wait before re-laying out the widget after a resize event
    RELAYOUT_DELAY = 100

    def __init__(self):
        # Set up a single shot timer to trigger re-laying out the widget
        self.relayoutTimer = QTimer()
        self.relayoutTimer.setSingleShot(True)
        self.relayoutTimer.setInterval(100)
        self.relayoutTimer.timeout.connect(lambda: self.__niceRelayout())

    def __niceRelayout(self):
        """Use SIP utility to check if the widget has been deleted before re-laying out,
           and disable visual updates during the re-layout to avoid flickering."""
        if not sip.isdeleted(self):
            self.relayout()

    @abstractmethod
    def relayout(self):
        """Re-lay out the widget after a resize event has finished."""
        pass

    def resizeEvent(self, event):
        """Keep bumping the single shot timer during resize events."""
        super().resizeEvent(event)

        # Re-start the timeout while we're resizing
        self.relayoutTimer.stop()
        self.relayoutTimer.start()
