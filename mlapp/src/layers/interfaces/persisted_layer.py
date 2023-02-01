# -*- coding: utf-8 -*-
from abc import abstractmethod

from .layer import Layer


class PersistedLayer(Layer):

    @abstractmethod
    def analyseFeatures(self):
        pass
