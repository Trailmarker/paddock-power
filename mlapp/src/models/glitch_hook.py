# -*- coding: utf-8 -*-
import sys

from qgis.PyQt.QtCore import QObject, pyqtSignal

from ..utils import qgsDebug
from .glitch import Glitch


class GlitchHook(QObject):
    __GLITCH_HOOK_WRAPPER = "__glitchHookWrapper"

    caughtGlitch = pyqtSignal(Glitch)
    pluginUnloading = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.pluginUnloading.connect(GlitchHook.__restoreSystemExceptionHook)
        self.__setupGlitchHook()
        self.caughtGlitch.connect(Glitch.popup)

    @staticmethod
    def __restoreSystemExceptionHook():
        if hasattr(sys.excepthook, GlitchHook.__GLITCH_HOOK_WRAPPER):
            qgsDebug("GlitchHook: restoring original system exception hook.")
            sys.excepthook = getattr(sys.excepthook, GlitchHook.__GLITCH_HOOK_WRAPPER)

    # Override Glitch type exceptions application-wide
    def __setupGlitchHook(self):
        if hasattr(sys.excepthook, GlitchHook.__GLITCH_HOOK_WRAPPER):
            qgsDebug("GlitchHook: Glitch hook already set.")
            return

        exceptHook = sys.excepthook
        qgsDebug("GlitchHook: setting up Glitch hook.")

        def glitchHookWrapper(exceptionType, e, traceback):
            if isinstance(e, Glitch):
                self.caughtGlitch.emit(e)
                return
            else:
                exceptHook(exceptionType, e, traceback)

        setattr(glitchHookWrapper, GlitchHook.__GLITCH_HOOK_WRAPPER, sys.excepthook)
        sys.excepthook = glitchHookWrapper
