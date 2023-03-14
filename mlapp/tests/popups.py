# -*- coding: utf-8 -*-

from ..dev import *


def testPaddocks():
    p = first(paddockLayer)

    assert isinstance(p, Paddock)

    q = first(paddockLayer.getFeaturesInCurrentTimeframe())

    paddockLayer.selectFeature(q)

    # p.addPopupLayer(PaddockCurrentLandTypesPopupLayer)
    # p.addPopupLayer(PaddockFutureLandTypesPopupLayer)

    # p.removePopupLayer(PaddockCurrentLandTypesPopupLayer)
    # p.removePopupLayer(PaddockFutureLandTypesPopupLayer)

    # for layerType in p.popupLayerTypes:
    #     p.addPopupLayer(layerType)


def testWaterpoints():
    w = first(waterpointLayer)

    assert isinstance(w, Waterpoint)

    w.addPopupLayer(WaterpointPopupLayer)
