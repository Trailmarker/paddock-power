# -*- coding: utf-8 -*-

from .dev import *
from .src.layers.fields.field_map import FieldMap


def layerByName(layerName):
    return next((l for l in QgsProject.instance().mapLayers().values() if l.name() == layerName), None)


def testImportKidmanLandTypes():
    kidmanLandTypes = layerByName("c_Kidman_30k_land_units")
    fieldMap = FieldMap(kidmanLandTypes, workspace().landTypeLayer)
    fieldMap["Land Type Name"] = "LAND_UNIT"
    workspace().landTypeLayer.importFeatures(kidmanLandTypes, fieldMap)


def testImportKidmanPaddocks():
    kidmanPaddocks = layerByName("b_Kidman_Paddocks")
    fieldMap = FieldMap(kidmanPaddocks, workspace().basePaddockLayer)
    fieldMap["Name"] = "Name"
    basePaddockLayer.importFeatures(kidmanPaddocks, fieldMap)


def testImportKidmanWaterpoints():
    kidmanWaterpoints = layerByName("a_Kidman_Waterpoints")
    fieldMap = FieldMap(kidmanWaterpoints, workspace().waterpointLayer)
    fieldMap["Name"] = "NAME"
    fieldMap["Waterpoint Type"] = "LAYER"
    waterpointLayer.importFeatures(kidmanWaterpoints, fieldMap)
