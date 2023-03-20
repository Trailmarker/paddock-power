# -*- coding: utf-8 -*-

from ..dev import *
from ..src.layers.fields.field_map import FieldMap
from ..src.layers.fields import *


def layerByName(layerName):
    return next((l for l in QgsProject.instance().mapLayers().values() if l.name() == layerName), None)


def testImportKidmanLandTypes():
    kidmanLandTypes = layerByName("c_Kidman_30k_land_units")
    fieldMap = FieldMap(kidmanLandTypes, workspace().landTypeLayer)
    fieldMap.update(0, "LAND_UNIT", "Land Type Name")
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
    mathsionLandTypes = layerByName("Land Systems")
    fieldMap = FieldMap(mathsionLandTypes, workspace().landTypeLayer)
    fieldMap.update(0, "Land System", "Land Type Name")
    fieldMap.update(1, "AE/km²", OPTIMAL_CAPACITY_PER_AREA)
    imports = workspace().landTypeLayer.importFeatures(mathsionLandTypes, fieldMap)
    imports.persist()


def testImportMathisonPaddocks():
    mathisonPaddocks = layerByName("Supplied Paddocks")
    fieldMap = FieldMap(mathisonPaddocks, workspace().basePaddockLayer)
    fieldMap.update(0, "Paddock Name", "Name")
    imports = basePaddockLayer.importFeatures(mathisonPaddocks, fieldMap)
    imports.persist()


def testImportMathisonWaterpoints():
    mathisonWaterpoints = layerByName("Supplied Waterpoints")
    fieldMap = FieldMap(mathisonWaterpoints, workspace().waterpointLayer)
    fieldMap.update(0, "Waterpoint Name", "Name")
    fieldMap.update(1, "Waterpoint Type", "Waterpoint Type")
    imports = waterpointLayer.importFeatures(mathisonWaterpoints, fieldMap)
    imports.persist()


def testImportMathison():
    testImportMathisonLandTypes()
    testImportMathisonPaddocks()
    testImportMathisonWaterpoints()
