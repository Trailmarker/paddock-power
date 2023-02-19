# -*- coding: utf-8 -*-
from ..models import Glitch
from ..utils import randomString
from .derived_feature_layer import DerivedFeatureLayer


class PopupFeatureLayer(DerivedFeatureLayer):

    @classmethod
    def defaultName(cls):
        return f"{cls.__name__}{randomString()}"

    def __init__(self, feature, *args):
        if not feature:
            raise Glitch(f"{type(self).__name__}.__init__({feature}, {args}): not feature")

        DerivedFeatureLayer.__init__(self, *args)
        self.popupFeature = feature
