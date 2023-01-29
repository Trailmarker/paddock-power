
from .dev import * 

def testUpdateOrder(*layers):
    
    layers = layers or workspace().layerDependencyGraph.loadOrder()
    
    return workspace().layerDependencyGraph.updateOrder(*layers)

def testUpdateOrderSameAsLoadOrderWhenAllLayersUpdated():
    
    updatedLayers = workspace().layerDependencyGraph.loadOrder()
    layers = workspace().layerDependencyGraph.updateOrder(*updatedLayers)
    
    assert len(layers) == len(updatedLayers)
    