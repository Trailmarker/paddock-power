# -*- coding: utf-8 -*-
from ..utils import randomString
from .calculator import Calculator
from .features import WaterpointBuffer
from .fields import ACTIVE, AREA, FAR_GRAZING_RADIUS, FID, GRAZING_RADIUS, GRAZING_RADIUS_TYPE, NAME, NEAR_GRAZING_RADIUS, PADDOCK, PADDOCK_NAME, STATUS, TIMEFRAME, WATERPOINT, WATERPOINT_NAME, WATERPOINT_TYPE, GrazingRadiusType, Timeframe, WaterpointType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedWaterpointBufferLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Waterpoint Buffers"
    STYLE = "waterpoint_buffer"

    @classmethod
    def getFeatureType(cls):
        return WaterpointBuffer

    def getRederiveFeaturesRequest(self):
        """Define which features must be removed from a target layer to be re-derived."""
        if self.changeset.isEmpty:
            return None

        [analyticPaddockLayer, waterpointLayer] = self.dependentLayers
        return self.prepareRederiveFeaturesRequest(
            analyticPaddockLayer, PADDOCK, PADDOCK, waterpointLayer, WATERPOINT, FID)

    def prepareQuery(self, query, dependentLayers):
        [analyticPaddockLayer, waterpointLayer] = dependentLayers
        [analyticPaddocks, waterpoints] = self.names(dependentLayers)

        # Set up clauses
        inPaddocksClause = self.andAllKeyClauses(
            self.changeset, analyticPaddockLayer, PADDOCK, FID, waterpointLayer, WATERPOINT, FID)
        renamedWaterpointsClause = self.andAllKeyClauses(self.changeset, waterpointLayer, FID, FID)

        _BUFFERS = f"Buffers{randomString()}"
        _FAR_BUFFER = f"FarBuffer{randomString()}"
        _NEAR_BUFFER = f"NearBuffer{randomString()}"
        _IN_PADDOCKS = f"InPaddocks{randomString()}"
        _RENAMED_WATERPOINTS = f"RenamedWaterpoints{randomString()}"

        query = f"""
with {_IN_PADDOCKS} as
    (select
        "{analyticPaddocks}".geometry,
        "{analyticPaddocks}".{PADDOCK} as "{PADDOCK}",
        "{analyticPaddocks}"."{NAME}" as "{PADDOCK_NAME}",
        "{waterpoints}".{FID} as "{WATERPOINT}",
        "{waterpoints}"."{NAME}" as "{WATERPOINT_NAME}",
        '{Timeframe.Current.name}' as "{TIMEFRAME}"
	 from "{waterpoints}"
	 inner join "{analyticPaddocks}"
     on {Timeframe.Current.matchesStatuses(f'"{waterpoints}"."{STATUS}"', f'"{analyticPaddocks}"."{STATUS}"')}
	 and st_contains("{analyticPaddocks}".geometry, "{waterpoints}".geometry)
     where {WaterpointType.givesWaterSql(f'"{waterpoints}"."{WATERPOINT_TYPE}"')}
     union
     select
        "{analyticPaddocks}".geometry,
        "{analyticPaddocks}".{PADDOCK} as "{PADDOCK}",
        "{analyticPaddocks}"."{NAME}" as "{PADDOCK_NAME}",
        "{waterpoints}".{FID} as "{WATERPOINT}",
        "{waterpoints}"."{NAME}" as "{WATERPOINT_NAME}",
        '{Timeframe.Future.name}' as "{TIMEFRAME}"
	 from "{waterpoints}"
	 inner join "{analyticPaddocks}"
     on {Timeframe.Future.matchesStatuses(f'"{waterpoints}"."{STATUS}"', f'"{analyticPaddocks}"."{STATUS}"')}
	 and st_contains("{analyticPaddocks}".geometry, "{waterpoints}".geometry)
     where {WaterpointType.givesWaterSql(f'"{waterpoints}"."{WATERPOINT_TYPE}"')}
     {inPaddocksClause}),
{_RENAMED_WATERPOINTS} as
     (select
	     geometry,
         {FID},
         {NAME},
		 {STATUS},
		 "{NEAR_GRAZING_RADIUS}" as {_NEAR_BUFFER},
		 "{FAR_GRAZING_RADIUS}" as {_FAR_BUFFER}
	  from "{waterpoints}"
      where ({ACTIVE} or upper({ACTIVE})='TRUE')
      and {WaterpointType.givesWaterSql(f'"{waterpoints}"."{WATERPOINT_TYPE}"')}
      {renamedWaterpointsClause}),
    {_BUFFERS} as
    (select
		st_buffer(geometry, {_NEAR_BUFFER}) as geometry,
		{FID} as "{WATERPOINT}",
        {NAME} as "{WATERPOINT_NAME}",
        '{GrazingRadiusType.Near.name}' as "{GRAZING_RADIUS_TYPE}",
        {_NEAR_BUFFER} as "{GRAZING_RADIUS}",
        {STATUS}
	 from {_RENAMED_WATERPOINTS}
	 union
     select
		st_buffer(geometry, {_FAR_BUFFER}) as geometry,
		{FID} as "{WATERPOINT}",
        {NAME} as "{WATERPOINT_NAME}",
        '{GrazingRadiusType.Far.name}' as "{GRAZING_RADIUS_TYPE}",
        {_FAR_BUFFER} as "{GRAZING_RADIUS}",
        {STATUS}
	 from {_RENAMED_WATERPOINTS})
select
    st_multi(st_intersection({_BUFFERS}.geometry, {_IN_PADDOCKS}.geometry)) as geometry,
    0 as {FID},
    {_BUFFERS}."{WATERPOINT}",
    {_BUFFERS}."{WATERPOINT_NAME}",
    {_IN_PADDOCKS}."{PADDOCK}",
    {_IN_PADDOCKS}."{PADDOCK_NAME}",
    {_BUFFERS}."{GRAZING_RADIUS_TYPE}",
    {_BUFFERS}."{GRAZING_RADIUS}",
    {_BUFFERS}.{STATUS},
    {_IN_PADDOCKS}.{TIMEFRAME},
    st_area(st_intersection({_BUFFERS}.geometry, {_IN_PADDOCKS}.geometry)) / 1000000 as "{AREA}"
from {_BUFFERS}
inner join {_IN_PADDOCKS}
on {_BUFFERS}."{WATERPOINT}" = {_IN_PADDOCKS}."{WATERPOINT}"
and st_area(st_intersection({_BUFFERS}.geometry, {_IN_PADDOCKS}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
and {Timeframe.timeframesMatchStatuses(f'{_IN_PADDOCKS}."{TIMEFRAME}"', f'{_BUFFERS}."{STATUS}"')}
"""
        return super().prepareQuery(query, dependentLayers)

    def __init__(self,
                 dependentLayers,
                 changeset):

        super().__init__(
            DerivedWaterpointBufferLayer.defaultName(),
            DerivedWaterpointBufferLayer.defaultStyle(),
            dependentLayers,
            changeset)
