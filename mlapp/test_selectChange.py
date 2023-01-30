
from .dev import *


def testSelectChange():
    f = first(derivedMetricPaddockLayer)

    paddocks = [f]

    for p in paddocks:
        assert isinstance(p, MetricPaddock)

        workspace().featureLayerSelected.emit(type(p.featureLayer), p, True)
        workspace().selectFeature(p)

    for p in paddocks:
        derivedMetricPaddockLayer.onSelectedFeatureChanged(type(p.featureLayer), p, True)
