# -*- coding: utf-8 -*-
from qgis.core import QgsCategorizedSymbolRenderer, QgsFillSymbol, QgsLineSymbol, QgsRendererCategory

from ...models.colors import toQgisRendererColour
from ..schemas.feature_status import FeatureStatus


def fill(colour, outline):
    return QgsFillSymbol.createSimple(
        {'color': toQgisRendererColour(*colour),
         'outline-color': toQgisRendererColour(*outline),
         'outline_style': 'solid'})


def line(colour, width):
    return QgsLineSymbol.createSimple({'color': toQgisRendererColour(*colour), 'width': str(width)})


def lineRendererCategory(status, colour, outline=None, enabled=True):
    return QgsRendererCategory(status.name, line(colour, 10), status.value, enabled)


def fillRendererCategory(status, colour, outline=None, enabled=True):
    return QgsRendererCategory(status.name, fill(colour, outline or colour), status.value, enabled)


def lineStatusCategoryRenderer(enabled=True):
    categories = [lineRendererCategory(status, status.toColour(),
                                       outline=(0, 0, 0), enabled=enabled)
                  for status in FeatureStatus if not status.match(FeatureStatus.Archived, FeatureStatus.Undefined)]
    return QgsCategorizedSymbolRenderer(attrName='Status', categories=categories)


def fillStatusCategoryRenderer(enabled=True):
    categories = [fillRendererCategory(status, status.toColour(),
                                       outline=(0, 0, 0), enabled=enabled)
                  for status in FeatureStatus if not status.match(FeatureStatus.Archived, FeatureStatus.Undefined)]
    return QgsCategorizedSymbolRenderer(attrName='Status', categories=categories)
