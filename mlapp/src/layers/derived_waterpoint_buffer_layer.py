# -*- coding: utf-8 -*-
from ..utils import qgsDebug
from .calculator import Calculator
from .features import WaterpointBuffer
from .fields import FAR_GRAZING_RADIUS, FID, GRAZING_RADIUS, GRAZING_RADIUS_TYPE, NEAR_GRAZING_RADIUS, PADDOCK, STATUS, TIMEFRAME, WATERPOINT, WATERPOINT_TYPE, GrazingRadiusType, Timeframe, WaterpointType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedWaterpointBufferLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Waterpoint Buffers"
    STYLE = "waterpoint_buffer"

    @classmethod
    def getFeatureType(cls):
        return WaterpointBuffer

    def getRederiveFeaturesRequest(self):
        """Define which features must be removed from a target layer to be re-derived."""
        if not self.changeset:
            return None
        
        [basePaddockLayer, waterpointLayer] = self.dependentLayers            
        return self.prepareRederiveFeaturesRequest(basePaddockLayer, PADDOCK, FID, waterpointLayer, WATERPOINT, FID)    

    def prepareQuery(self, query, dependentLayers):
        [basePaddockLayer, waterpointLayer] = dependentLayers
        [basePaddocks, waterpoints] = self.names(dependentLayers)

        # Set up clauses
        inPaddocksClause = self.andAllKeyClauses(
            self.changeset, basePaddockLayer, PADDOCK, FID, waterpointLayer, WATERPOINT, FID)
        renamedWaterpointsClause = self.andAllKeyClauses(self.changeset, waterpointLayer, FID, FID)

        _BUFFERS = "Buffers"
        _FAR_BUFFER = "FarBuffer"
        _NEAR_BUFFER = "NearBuffer"
        _IN_PADDOCKS = "InPaddocks"
        _RENAMED_WATERPOINTS = "RenamedWaterpoints"

        query = f"""
with {_IN_PADDOCKS} as
    (select
        "{basePaddocks}".geometry,
        "{basePaddocks}".{FID} as "{PADDOCK}",
        "{waterpoints}".{FID} as "{WATERPOINT}",
        '{Timeframe.Current.name}' as "{TIMEFRAME}"
	 from "{waterpoints}"
	 inner join "{basePaddocks}"
     on {Timeframe.Current.includesStatuses(f'"{waterpoints}"."{STATUS}"', f'"{basePaddocks}"."{STATUS}"')}
	 and st_contains("{basePaddocks}".geometry, "{waterpoints}".geometry)
     where {WaterpointType.givesWaterSql(f'"{waterpoints}"."{WATERPOINT_TYPE}"')}
     union
     select
        "{basePaddocks}".geometry,
        "{basePaddocks}".{FID} as "{PADDOCK}",
        "{waterpoints}".{FID} as "{WATERPOINT}",
        '{Timeframe.Future.name}' as "{TIMEFRAME}"
	 from "{waterpoints}"
	 inner join "{basePaddocks}"
     on {Timeframe.Future.includesStatuses(f'"{waterpoints}"."{STATUS}"', f'"{basePaddocks}"."{STATUS}"')}
	 and st_contains("{basePaddocks}".geometry, "{waterpoints}".geometry)
     where {WaterpointType.givesWaterSql(f'"{waterpoints}"."{WATERPOINT_TYPE}"')}
     {inPaddocksClause}),
{_RENAMED_WATERPOINTS} as
     (select
	     geometry,
         {FID},
		 {STATUS},
		 "{NEAR_GRAZING_RADIUS}" as {_NEAR_BUFFER},
		 "{FAR_GRAZING_RADIUS}" as {_FAR_BUFFER}
	  from "{waterpoints}"
      where {WaterpointType.givesWaterSql(f'"{waterpoints}"."{WATERPOINT_TYPE}"')}
      {renamedWaterpointsClause}),
    {_BUFFERS} as
    (select
		st_buffer(geometry, {_NEAR_BUFFER}) as geometry,
		{FID} as "{WATERPOINT}",
        '{GrazingRadiusType.Near.name}' as "{GRAZING_RADIUS_TYPE}",
        {_NEAR_BUFFER} as "{GRAZING_RADIUS}",
        {STATUS}
	 from {_RENAMED_WATERPOINTS}
	 union
     select
		st_buffer(geometry, {_FAR_BUFFER}) as geometry,
		{FID} as "{WATERPOINT}",
        '{GrazingRadiusType.Far.name}' as "{GRAZING_RADIUS_TYPE}",
        {_FAR_BUFFER} as "{GRAZING_RADIUS}",
        {STATUS}
	 from {_RENAMED_WATERPOINTS})
select
    st_multi(st_intersection({_BUFFERS}.geometry, {_IN_PADDOCKS}.geometry)) as geometry,
    0 as {FID},
    {_BUFFERS}."{WATERPOINT}",
    {_IN_PADDOCKS}."{PADDOCK}",
    {_BUFFERS}."{GRAZING_RADIUS_TYPE}",
    {_BUFFERS}."{GRAZING_RADIUS}",
    {_BUFFERS}.{STATUS},
    {_IN_PADDOCKS}.{TIMEFRAME}
from {_BUFFERS}
inner join {_IN_PADDOCKS}
on {_BUFFERS}."{WATERPOINT}" = {_IN_PADDOCKS}."{WATERPOINT}"
and st_area(st_intersection({_BUFFERS}.geometry, {_IN_PADDOCKS}.geometry)) >= {Calculator.MINIMUM_PLANAR_AREA_M2}
and {Timeframe.timeframesIncludeStatuses(f'{_IN_PADDOCKS}."{TIMEFRAME}"', f'{_BUFFERS}."{STATUS}"')}
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
