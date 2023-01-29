# -*- coding: utf-8 -*-
from functools import cached_property
from os import path
import sqlite3

from qgis.core import QgsRasterLayer

from ...models.glitch import Glitch
from ...utils import PLUGIN_NAME
from .mixins.layer_mixin import LayerMixin
from .mixins.workspace_connection_mixin import WorkspaceConnectionMixin


class ElevationLayer(QgsRasterLayer, WorkspaceConnectionMixin, LayerMixin):

    NAME = "Elevation Mapping"
    STYLE = "elevation"

    @staticmethod
    def _rasterGpkgUrl(workspaceFile, layerName):
        """Return a URL for a raster layer in a GeoPackage file."""
        # different from QgsVectorLayer GeoPackage URL format!
        return f"GPKG:{workspaceFile}:{layerName}"

    @classmethod
    def detectInGeoPackage(_, workspaceFile):
        """Find an elevation layer in a workspace GeoPackage."""
        try:
            if not path.exists(workspaceFile):
                return None

            db = sqlite3.connect(workspaceFile)
            cursor = db.cursor()
            cursor.execute(
                "SELECT table_name, data_type FROM gpkg_contents WHERE data_type = '2d-gridded-coverage'")
            grids = cursor.fetchall()

            if len(grids) == 0:
                return None
            elif len(grids) == 1:
                return grids[0][0]
            else:
                raise Glitch(
                    f"{PLUGIN_NAME} found multiple possible elevation layers in {workspaceFile}")
        except BaseException:
            return None

    def __init__(self, workspaceFile, layerName=None, *args, **kwargs):
        """Create a new elevation layer."""

        self._workspace = None

        # Route changes to this layer *through* the Paddock Power
        # workspace so other objects can respond
        self._blockWorkspaceConnnection = False

        layerName = layerName or ElevationLayer.NAME

        styleName = kwargs.pop("styleName", ElevationLayer.STYLE)

        # Note ths URL format is different from QgsVectorLayer!
        rasterUrl = ElevationLayer._rasterGpkgUrl(workspaceFile, layerName)
        super().__init__(rasterUrl, baseName=layerName)

        self.applyNamedStyle(styleName)

        self.addInBackground()

    @cached_property
    def typeName(self):
        """Return the FeatureLayer's type name."""
        return type(self).__name__

    def __repr__(self):
        """Return a string representation of the Field."""
        return f"{self.typeName}(name={self.name()})"

    def __str__(self):
        """Convert the Field to a string representation."""
        return repr(self)
