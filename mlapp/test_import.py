# -*- coding: utf-8 -*-

from .dev import *
from .src.layers.fields.field_map import FieldMap

# From QGIS having created a new project and loaded it empty

[landTypeLayer, basePaddockLayer, pipelineLayer, waterpointLayer] = [workspace().landTypeLayer, workspace().basePaddockLayer,
                                                                 workspace().pipelineLayer, workspace().waterpointLayer]

kidmanPaddocks = next((l for l in QgsProject.instance().mapLayers().values() if l.name() == "b_Kidman_Paddocks"), None)
kidmanLandTypes = next((l for l in QgsProject.instance().mapLayers().values()
                       if l.name() == "c_Kidman_30k_land_units"), None)
kidmanWaterpoints = next((l for l in QgsProject.instance().mapLayers().values()
                         if l.name() == "a_Kidman_Waterpoints"), None)

kidmanPaddockFieldMap = FieldMap(kidmanPaddocks, basePaddockLayer)
kidmanLandTypeFieldMap = FieldMap(kidmanLandTypes, landTypeLayer)
kidmanWaterpointFieldMap = FieldMap(kidmanWaterpoints, waterpointLayer)


def testImportKidmanLandTypes():
    kidmanLandTypeFieldMap["LAND_UNIT"] = "Land Type Name"
    landTypeLayer.importFeatures(kidmanLandTypes, kidmanLandTypeFieldMap)


def testImportKidmanPaddocks():
    kidmanPaddockFieldMap["Name"] = "Name"
    basePaddockLayer.importFeatures(kidmanPaddocks, kidmanPaddockFieldMap)


def testImportKidmanWaterpoints():
    kidmanWaterpointFieldMap["NAME"] = "Name"
    kidmanWaterpointFieldMap["LAYER"] = "Waterpoint Type"
    waterpointLayer.importFeatures(kidmanWaterpoints, kidmanWaterpointFieldMap)
