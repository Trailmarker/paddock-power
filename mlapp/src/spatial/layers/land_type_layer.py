# -*- coding: utf-8 -*-
from ..features.land_type import LandType
from ..fields.schemas import LandTypeSchema
from .imported_feature_layer import ImportedFeatureLayer


class LandTypeLayer(ImportedFeatureLayer):

    NAME = "Land Types"
    STYLE = "land_type"

    def __init__(self, workspaceFile):
        super().__init__(LandType,
                         workspaceFile,
                         layerName=LandTypeLayer.NAME,
                         styleName=LandTypeLayer.STYLE)

        self.setReadOnly(True)

    def getSchema(self):
        """Return the Schema for this layer."""
        return LandTypeSchema

    def getWkbType(self):
        """Return the WKB type for this layer."""
        return LandTypeSchema.wkbType
