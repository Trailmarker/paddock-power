# -*- coding: utf-8 -*-
from ..features.watered_area import WateredArea
from ..schemas.feature_status import FeatureStatus
from ..schemas.schemas import GRAZING_RADIUS, FAR_GRAZING_RADIUS, FID, NEAR_GRAZING_RADIUS, STATUS, WATERPOINT, GRAZING_RADIUS_TYPE
from ..schemas.grazing_radius_type import GrazingRadiusType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedWateredAreaLayer(DerivedFeatureLayer):

    STYLE = "watered_area"

    QUERY = f"""
with
  "{GrazingRadiusType.Near.name}" as
	(select
	 st_union(geometry) as "geometry",
	 "{STATUS}"
	 from "{{1}}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Near.name}'
	 group by "{STATUS}")
, "{GrazingRadiusType.Far.name}" as
	(select
	 st_union(geometry) as "geometry",
	 "{STATUS}"
	 from "{{1}}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Far.name}'
	 group by "{STATUS}")
, "Property" as
	(select st_union(geometry) as "geometry"
     from
	 (select geometry from "{{0}}"
	  union
	  select geometry from "{{1}}"))
select
	0 as "{FID}",
	st_collectionextract(geometry, 3),
	'{GrazingRadiusType.Near.name}' as "Watered",
	"{STATUS}"
from "{GrazingRadiusType.Near.name}"
union
select
	0 as "{FID}",
	st_collectionextract(st_difference("{GrazingRadiusType.Far.name}".geometry, "{GrazingRadiusType.Near.name}".geometry), 3),
	'{GrazingRadiusType.Far.name}' as "Watered",
	"{GrazingRadiusType.Far.name}"."{STATUS}"
from "{GrazingRadiusType.Far.name}"
inner join "{GrazingRadiusType.Near.name}"
on "{GrazingRadiusType.Far.name}"."{STATUS}" = "{GrazingRadiusType.Near.name}"."{STATUS}"
union
select
	0 as "{FID}",
	st_collectionextract(st_difference(st_difference("Property".geometry, "{GrazingRadiusType.Far.name}".geometry), "{GrazingRadiusType.Near.name}".geometry), 3),
	'Unwatered' as "Watered",
	"{GrazingRadiusType.Far.name}"."{STATUS}"
from "Property", "{GrazingRadiusType.Far.name}", "{GrazingRadiusType.Near.name}"
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
