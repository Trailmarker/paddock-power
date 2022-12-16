# -*- coding: utf-8 -*-
from ..calculator import Calculator
from ..features.watered_area import WateredArea
from ..schemas.schemas import FID, PADDOCK, PADDOCK_STATUS, STATUS, GRAZING_RADIUS_TYPE, WATERED_TYPE
from ..schemas.grazing_radius_type import GrazingRadiusType
from ..schemas.watered_type import WateredType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedWateredAreaLayer(DerivedFeatureLayer):

    STYLE = "watered_area"

    NEAR_WATERED_AREA = "NearWateredArea"
    FAR_WATERED_AREA = "FarWateredArea"

    QUERY = f"""
with
  {NEAR_WATERED_AREA} as
	(select
	 st_union(geometry) as geometry,
	 {PADDOCK},
	 {STATUS},
	 "{PADDOCK_STATUS}"
	 from "{{1}}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Near.name}'
	 group by {PADDOCK}, {STATUS})
, {FAR_WATERED_AREA} as
	(select
	 st_union(geometry) as geometry,
	 {PADDOCK},
	 {STATUS},
	 "{PADDOCK_STATUS}"
	 from "{{1}}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Far.name}'
	 group by {PADDOCK}, {STATUS})
select
	0 as {FID},
	st_multi(geometry) as geometry,
	'{WateredType.Near.name}' as {WATERED_TYPE},
	{NEAR_WATERED_AREA}.{STATUS},
	{NEAR_WATERED_AREA}.{PADDOCK},
	{NEAR_WATERED_AREA}."{PADDOCK_STATUS}"
from {NEAR_WATERED_AREA}
union
select
	0 as {FID},
	st_multi(st_difference({FAR_WATERED_AREA}.geometry, {NEAR_WATERED_AREA}.geometry)) as geometry,
	'{WateredType.Far.name}' as {WATERED_TYPE},
	{FAR_WATERED_AREA}.{STATUS},
	{FAR_WATERED_AREA}.{PADDOCK},
	{FAR_WATERED_AREA}."{PADDOCK_STATUS}"
from {FAR_WATERED_AREA}
inner join {NEAR_WATERED_AREA}
	on {FAR_WATERED_AREA}.{STATUS} = {NEAR_WATERED_AREA}.{STATUS}
	and {FAR_WATERED_AREA}.{PADDOCK} = {NEAR_WATERED_AREA}.{PADDOCK}
	and st_difference({FAR_WATERED_AREA}.geometry, {NEAR_WATERED_AREA}.geometry) is not null
	and st_area(st_difference({FAR_WATERED_AREA}.geometry, {NEAR_WATERED_AREA}.geometry)) >= {Calculator.MINIMUM_AREA_M2}
union
select
	0 as {FID},
	st_multi(st_difference({{0}}.geometry, {FAR_WATERED_AREA}.geometry)) as geometry,
	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	{FAR_WATERED_AREA}.{STATUS},
	{FAR_WATERED_AREA}.{PADDOCK},
	"{{0}}".{STATUS} as "{PADDOCK_STATUS}"
from "{{0}}"
inner join {FAR_WATERED_AREA}
	on "{{0}}".{FID} = {FAR_WATERED_AREA}.{PADDOCK}
	and st_difference({{0}}.geometry, {FAR_WATERED_AREA}.geometry) is not null
	and st_area(st_difference({{0}}.geometry, {FAR_WATERED_AREA}.geometry)) >= {Calculator.MINIMUM_AREA_M2}
"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WateredArea

    def __init__(self, layerName, paddockLayer, waterpointBufferLayer):
        super().__init__(
            layerName,
            DerivedWateredAreaLayer.QUERY,
            DerivedWateredAreaLayer.STYLE,
            paddockLayer,
            waterpointBufferLayer)
