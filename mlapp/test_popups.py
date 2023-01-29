
from .src.spatial.features.metric_paddock import MetricPaddock
from .src.spatial.layers.metric_paddock_land_types_popup_layer import MetricPaddockCurrentLandTypesPopupLayer, MetricPaddockFutureLandTypesPopupLayer
from .dev import * 

def testPopups():
    p = first(derivedMetricPaddockLayer)

    assert isinstance(p, MetricPaddock)

    p.addPopupLayer(MetricPaddockCurrentLandTypesPopupLayer)
    p.addPopupLayer(MetricPaddockFutureLandTypesPopupLayer)
    
    p.removePopupLayer(MetricPaddockCurrentLandTypesPopupLayer)
    p.removePopupLayer(MetricPaddockFutureLandTypesPopupLayer)
    
    for layerType in p.popupLayerTypes:
        p.addPopupLayer(layerType)
        
    
