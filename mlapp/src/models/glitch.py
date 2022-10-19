# -*- coding: utf-8 -*-
from contextlib import contextmanager

from qgis.core import Qgis

from ..utils import guiError, qgsDebug


class Glitch(Exception):
    """Throw a Paddock Power business logic or consistency error."""

    def __init__(self, *args):
        """Create a new Glitch."""
        self.__glitches = []

        if not args:
            super().__init__()
            return

        arg = args[0]

        if isinstance(arg, str):
            super().__init__(arg)
            self.__addGlitch(arg)

        elif isinstance(arg, Glitch):
            super().__init__(arg)
            self.__glitches = arg.__glitches
            if len(args) >= 2 and isinstance(args[1], str):
                self.__addGlitch(args[1])

        elif isinstance(arg, BaseException):
            super().__init__(arg)
            if len(args) >= 2 and isinstance(args[1], str):
                self.__addGlitch(args[1])

    def __addGlitch(self, message):
        """Add a message to the glitch."""
        self.__glitches.append(message)
        self.message = str(self.__glitches)

    def show(self):
        """Display a GUI message for this glitch."""
        glitchMessages = [g for g in self.__glitches] or ["An unknown error occurred."]
        glitchMessages.reverse()
        guiError(glitchMessages)

    @staticmethod
    def popup(glitch):
        """Display a GUI message for this glitch."""
        glitch.show()

    @staticmethod
    @contextmanager
    def glitches(message=None):
        """Catch and report Glitches."""
        try:
            yield
        except Glitch as g:
            if message is not None:
                raise Glitch(g, message)
            else:
                raise
        except BaseException as e:
            raise Glitch(e, message)

    @staticmethod
    def glitchy(message=None):
        """Catch and report Glitches adding an optional extra message for context."""
        def makeGlitchy(func):
            def funcWithGlitches(*args, **kwargs):
                with Glitch.glitches(message):
                    return func(*args, **kwargs)
            return funcWithGlitches
        return makeGlitchy
