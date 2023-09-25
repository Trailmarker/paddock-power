# # -*- coding: utf-8 -*-

# from .dev import *
# from paddock_power.src.layers.waterpoint_layer import WaterpointLayer


# def testSelectChange():
#     f = first(paddockLayer)

#     paddocks = [f]

#     for p in paddocks:
#         assert isinstance(p, Paddock)

#         workspace().featureLayerSelected.emit(type(p.featureLayer), p, True)
#         workspace().selectFeature(p)

#     for p in paddocks:
#         paddockLayer.onSelectedFeatureChanged(type(p.featureLayer), p, True)


# waterpointList = plugin().pluginDockWidget.waterpointTab.waterpointList


# def testListSelection():
#     f = first(waterpointLayer)

#     workspace().selectFeature(f)

#     assert waterpointList.itemWidget(waterpointList._selectedItem).feature.FID == f.FID
#     assert waterpointList._selectedFeature.FID == f.FID
#     waterpointList.changeSelection(WaterpointLayer)
