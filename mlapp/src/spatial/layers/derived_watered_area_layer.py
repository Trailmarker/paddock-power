# -*- coding: utf-8 -*-
from ..calculator import Calculator
from ..features.watered_area import WateredArea
from ..fields.names import FID, PADDOCK, STATUS, GRAZING_RADIUS_TYPE, TIMEFRAME, WATERED_TYPE
from ..fields.timeframe import Timeframe
from ..fields.grazing_radius_type import GrazingRadiusType
from ..fields.watered_type import WateredType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedWateredAreaLayer(DerivedFeatureLayer):

    STYLE = "watered_area"

    def parameteriseQuery(self, PaddockLayer, WaterpointBufferLayer):
        NearWateredArea = "NearWateredArea"
        FarWateredArea = "FarWateredArea"

        return f"""
with
  {NearWateredArea} as
	(select
		st_union(geometry) as geometry,
		{PADDOCK},
		{TIMEFRAME}
	 from "{WaterpointBufferLayer}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Near.name}'
	 group by {PADDOCK}, {TIMEFRAME})
, {FarWateredArea} as
	(select
		st_union(geometry) as geometry,
		{PADDOCK},
		{TIMEFRAME}
	 from "{WaterpointBufferLayer}"
	 where "{GRAZING_RADIUS_TYPE}" = '{GrazingRadiusType.Far.name}'
	 group by {PADDOCK}, {TIMEFRAME})
select
	0 as {FID},
	st_multi(geometry) as geometry,
	'{WateredType.Near.name}' as {WATERED_TYPE},
	{NearWateredArea}.{TIMEFRAME},
	{NearWateredArea}.{PADDOCK}
from {NearWateredArea}
union
select
	0 as {FID},
	st_multi(st_difference({FarWateredArea}.geometry, {NearWateredArea}.geometry)) as geometry,
	'{WateredType.Far.name}' as {WATERED_TYPE},
	{FarWateredArea}.{TIMEFRAME},
	{FarWateredArea}.{PADDOCK}
from {FarWateredArea}
inner join {NearWateredArea}
	on {FarWateredArea}.{TIMEFRAME} = {NearWateredArea}.{TIMEFRAME}
	and {FarWateredArea}.{PADDOCK} = {NearWateredArea}.{PADDOCK}
	and st_difference({FarWateredArea}.geometry, {NearWateredArea}.geometry) is not null
	and st_area(st_difference({FarWateredArea}.geometry, {NearWateredArea}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
union
select
	0 as {FID},
	st_multi(st_difference({PaddockLayer}.geometry, {FarWateredArea}.geometry)) as geometry,
	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	{FarWateredArea}.{TIMEFRAME},
	{FarWateredArea}.{PADDOCK}
from "{PaddockLayer}"
inner join {FarWateredArea}
	on "{PaddockLayer}".{FID} = {FarWateredArea}.{PADDOCK}
	and st_difference({PaddockLayer}.geometry, {FarWateredArea}.geometry) is not null
	and st_area(st_difference({PaddockLayer}.geometry, {FarWateredArea}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
	and {Timeframe.timeframesIncludeStatuses(f'"{FarWateredArea}"."{TIMEFRAME}"', f'"{PaddockLayer}"."{STATUS}"')}
union
select
	0 as {FID},
	st_multi({PaddockLayer}.geometry) as geometry,
	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	'{Timeframe.Current.name}' as {TIMEFRAME},
	"{PaddockLayer}".{FID} as {PADDOCK}
from "{PaddockLayer}", "{WaterpointBufferLayer}"
where not exists (
	select 1
	from "{WaterpointBufferLayer}"
	where "{WaterpointBufferLayer}".{PADDOCK} = "{PaddockLayer}".{FID}
	and {Timeframe.Current.timeframeIncludesStatuses(f'"{WaterpointBufferLayer}".{TIMEFRAME}', f'"{PaddockLayer}".{STATUS}')})
union
select
	0 as {FID},
	st_multi({PaddockLayer}.geometry) as geometry,
	'{WateredType.Unwatered.name}' as {WATERED_TYPE},
	'{Timeframe.Future.name}' as {TIMEFRAME},
	"{PaddockLayer}".{FID} as {PADDOCK}
from "{PaddockLayer}", "{WaterpointBufferLayer}"
where not exists (
	select 1
	from "{WaterpointBufferLayer}"
	where "{WaterpointBufferLayer}".{PADDOCK} = "{PaddockLayer}".{FID}
	and {Timeframe.Future.timeframeIncludesStatuses(f'"{WaterpointBufferLayer}".{TIMEFRAME}', f'"{PaddockLayer}".{STATUS}')})

"""

    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WateredArea

    def wrapFeature(self, feature):
        # Burn in the FID that gets generated by QGIS for consistency
        feature.setAttribute(FID, feature.id())
        return super().wrapFeature(feature)

    def __init__(self, project, layerName, paddockLayer, waterpointBufferLayer):
        super().__init__(
            project,
            layerName,
            self.parameteriseQuery(paddockLayer.name(), waterpointBufferLayer.name()),
            DerivedWateredAreaLayer.STYLE,
            paddockLayer,
            waterpointBufferLayer)
