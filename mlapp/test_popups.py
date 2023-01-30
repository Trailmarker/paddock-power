
from .dev import * 

def testMetricPaddocks():
    p = first(derivedMetricPaddockLayer)

    assert isinstance(p, MetricPaddock)

    q = first(derivedMetricPaddockLayer.getFeaturesInCurrentTimeframe())

    derivedMetricPaddockLayer.selectFeature(q)

    # p.addPopupLayer(MetricPaddockCurrentLandTypesPopupLayer)
    # p.addPopupLayer(MetricPaddockFutureLandTypesPopupLayer)
    
    # p.removePopupLayer(MetricPaddockCurrentLandTypesPopupLayer)
    # p.removePopupLayer(MetricPaddockFutureLandTypesPopupLayer)
    
    # for layerType in p.popupLayerTypes:
    #     p.addPopupLayer(layerType)
        
def testWaterpoints():
    w = first(waterpointLayer)
    
    assert isinstance(w, Waterpoint)
    
    w.addPopupLayer(WaterpointPopupLayer) 
        
    
