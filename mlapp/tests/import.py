# -*- coding: utf-8 -*-

from ..dev import *
from ..src.layers.fields.field_map import FieldMap
from ..src.layers.fields import *


def layerByName(layerName):
    return next((l for l in QgsProject.instance().mapLayers().values() if l.name() == layerName), None)


def testImportKidmanLandTypes():
    kidmanLandTypes = layerByName("c_Kidman_30k_land_units")
    fieldMap = FieldMap(kidmanLandTypes, workspace().landTypeLayer)
    fieldMap["Land Type Name"] = "LAND_UNIT"
    imports = workspace().landTypeLayer.importFeatures(kidmanLandTypes, fieldMap)
    imports.persist()


def testImportKidmanPaddocks():
    kidmanPaddocks = layerByName("b_Kidman_Paddocks")
    fieldMap = FieldMap(kidmanPaddocks, workspace().basePaddockLayer)
    fieldMap["Name"] = "Name"
    imports = basePaddockLayer.importFeatures(kidmanPaddocks, fieldMap)
    imports.persist()


def testImportKidmanWaterpoints():
    kidmanWaterpoints = layerByName("a_Kidman_Waterpoints")
    fieldMap = FieldMap(kidmanWaterpoints, workspace().waterpointLayer)
    fieldMap["Name"] = "NAME"
    fieldMap["Waterpoint Type"] = "LAYER"
    imports = waterpointLayer.importFeatures(kidmanWaterpoints, fieldMap)
    imports.persist()


def testImportKidman():
    testImportKidmanLandTypes()
    testImportKidmanPaddocks()
    testImportKidmanWaterpoints()


def testImportMathisonLandTypes():
    kidmanLandTypes = layerByName("Land Systems")
    fieldMap = FieldMap(kidmanLandTypes, workspace().landTypeLayer)
    fieldMap["Land Type Name"] = "Land System"
    fieldMap[OPTIMAL_CAPACITY_PER_AREA] = "AE/km²"
    imports = workspace().landTypeLayer.importFeatures(kidmanLandTypes, fieldMap)
    imports.persist()


def testImportMathisonPaddocks():
    kidmanPaddocks = layerByName("Current Paddocks")
    fieldMap = FieldMap(kidmanPaddocks, workspace().basePaddockLayer)
    fieldMap["Name"] = "Paddock Name"
    imports = basePaddockLayer.importFeatures(kidmanPaddocks, fieldMap)
    imports.persist()


def testImportMathisonWaterpoints():
    kidmanWaterpoints = layerByName("Current Waterpoints")
    fieldMap = FieldMap(kidmanWaterpoints, workspace().waterpointLayer)
    fieldMap["Name"] = "Waterpoint Name"
    fieldMap["Waterpoint Type"] = "Waterpoint Type"
    imports = waterpointLayer.importFeatures(kidmanWaterpoints, fieldMap)
    imports.persist()


def testImportMathison():
    testImportMathisonLandTypes()
    testImportMathisonPaddocks()
    testImportMathisonWaterpoints()
