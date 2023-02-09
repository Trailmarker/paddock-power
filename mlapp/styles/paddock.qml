<?xml version="1.1"?>
<qgis version="3.22.13-Białowieża" styleCategories="AllStyleCategories" readOnly="0" hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0" simplifyDrawingTol="1" labelsEnabled="1" simplifyDrawingHints="1" symbologyReferenceScale="-1" maxScale="0" simplifyLocal="1" minScale="0" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal accumulate="0" startField="" startExpression="" durationField="" endField="" durationUnit="min" limitMode="0" enabled="0" mode="0" fixedDuration="0" endExpression="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 symbollevels="0" forceraster="0" referencescale="-1" enableorderby="0" type="singleSymbol">
    <symbols>
      <symbol clip_to_extent="1" name="0" type="fill" force_rhr="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties" type="Map">
              <Option name="alpha" type="Map">
                <Option name="active" type="bool" value="true"/>
                <Option name="expression" type="QString" value="case&#xd;&#xa;when matchCurrentTimeframe(&quot;Timeframe&quot;) then 100.0&#xd;&#xa;else 0.0&#xd;&#xa;end"/>
                <Option name="type" type="int" value="3"/>
              </Option>
            </Option>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
          <Option type="Map">
            <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="color" type="QString" value="60,179,113,255"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="35,35,35,178"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0.4"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="style" type="QString" value="solid"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="60,179,113,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,178"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.4"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{68d24b63-2390-4d96-b72c-5a61d131756b}">
      <rule key="{5b3cf6fd-0ae2-4270-9982-4f97fc88d09e}" filter="&quot;Area (km²)&quot; > 5 and matchCurrentFeatureStatus(&quot;Status&quot;)">
        <settings calloutType="simple">
          <text-style fontWeight="75" capitalization="0" fontItalic="0" fontSize="12" useSubstitutions="0" textColor="0,0,0,255" isExpression="1" fontSizeUnit="Point" allowHtml="0" previewBkgrdColor="0,251,0,255" blendMode="0" fieldName=" title(  &quot;Name&quot; ||  '\n' || round(  &quot;Area (km²)&quot;  ,1) || 'km²')" fontUnderline="0" fontKerning="1" namedStyle="Bold" multilineHeight="1" fontFamily="Arial" legendString="Aa" fontStrikeout="0" fontWordSpacing="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" textOpacity="1" fontLetterSpacing="0" textOrientation="horizontal">
            <families/>
            <text-buffer bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferNoFill="1" bufferOpacity="1" bufferJoinStyle="128" bufferSize="0.29999999999999999" bufferDraw="1" bufferColor="255,255,255,255" bufferBlendMode="0"/>
            <text-mask maskedSymbolLayers="" maskType="0" maskSizeUnits="MM" maskJoinStyle="128" maskEnabled="0" maskSize="0" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskOpacity="1"/>
            <background shapeRotationType="0" shapeSizeX="0" shapeBorderWidth="0" shapeJoinStyle="64" shapeBlendMode="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiX="0" shapeSizeY="0" shapeRotation="0" shapeSizeType="0" shapeRadiiY="0" shapeSVGFile="" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeBorderColor="128,128,128,255" shapeBorderWidthUnit="MM" shapeRadiiUnit="MM" shapeOffsetX="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeDraw="0" shapeSizeUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeOffsetY="0" shapeFillColor="255,255,255,255">
              <symbol clip_to_extent="1" name="markerSymbol" type="marker" force_rhr="0" alpha="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" type="QString" value=""/>
                    <Option name="properties"/>
                    <Option name="type" type="QString" value="collection"/>
                  </Option>
                </data_defined_properties>
                <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
                  <Option type="Map">
                    <Option name="angle" type="QString" value="0"/>
                    <Option name="cap_style" type="QString" value="square"/>
                    <Option name="color" type="QString" value="125,139,143,255"/>
                    <Option name="horizontal_anchor_point" type="QString" value="1"/>
                    <Option name="joinstyle" type="QString" value="bevel"/>
                    <Option name="name" type="QString" value="circle"/>
                    <Option name="offset" type="QString" value="0,0"/>
                    <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
                    <Option name="offset_unit" type="QString" value="MM"/>
                    <Option name="outline_color" type="QString" value="35,35,35,255"/>
                    <Option name="outline_style" type="QString" value="solid"/>
                    <Option name="outline_width" type="QString" value="0"/>
                    <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
                    <Option name="outline_width_unit" type="QString" value="MM"/>
                    <Option name="scale_method" type="QString" value="diameter"/>
                    <Option name="size" type="QString" value="2"/>
                    <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
                    <Option name="size_unit" type="QString" value="MM"/>
                    <Option name="vertical_anchor_point" type="QString" value="1"/>
                  </Option>
                  <prop k="angle" v="0"/>
                  <prop k="cap_style" v="square"/>
                  <prop k="color" v="125,139,143,255"/>
                  <prop k="horizontal_anchor_point" v="1"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="name" v="circle"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="35,35,35,255"/>
                  <prop k="outline_style" v="solid"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="scale_method" v="diameter"/>
                  <prop k="size" v="2"/>
                  <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="size_unit" v="MM"/>
                  <prop k="vertical_anchor_point" v="1"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" type="QString" value=""/>
                      <Option name="properties"/>
                      <Option name="type" type="QString" value="collection"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
              <symbol clip_to_extent="1" name="fillSymbol" type="fill" force_rhr="0" alpha="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" type="QString" value=""/>
                    <Option name="properties"/>
                    <Option name="type" type="QString" value="collection"/>
                  </Option>
                </data_defined_properties>
                <layer locked="0" pass="0" enabled="1" class="SimpleFill">
                  <Option type="Map">
                    <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
                    <Option name="color" type="QString" value="255,255,255,255"/>
                    <Option name="joinstyle" type="QString" value="bevel"/>
                    <Option name="offset" type="QString" value="0,0"/>
                    <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
                    <Option name="offset_unit" type="QString" value="MM"/>
                    <Option name="outline_color" type="QString" value="128,128,128,255"/>
                    <Option name="outline_style" type="QString" value="no"/>
                    <Option name="outline_width" type="QString" value="0"/>
                    <Option name="outline_width_unit" type="QString" value="MM"/>
                    <Option name="style" type="QString" value="solid"/>
                  </Option>
                  <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="color" v="255,255,255,255"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="128,128,128,255"/>
                  <prop k="outline_style" v="no"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="style" v="solid"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" type="QString" value=""/>
                      <Option name="properties"/>
                      <Option name="type" type="QString" value="collection"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowUnder="0" shadowOpacity="0.69999999999999996" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowRadius="1.5" shadowDraw="0" shadowRadiusUnit="MM" shadowScale="100" shadowOffsetGlobal="1" shadowOffsetUnit="MM" shadowColor="0,0,0,255" shadowBlendMode="6" shadowRadiusAlphaOnly="0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format autoWrapLength="9" addDirectionSymbol="0" leftDirectionSymbol="&lt;" reverseDirectionSymbol="0" formatNumbers="0" wrapChar="" rightDirectionSymbol=">" decimals="3" plussign="0" multilineAlign="1" useMaxLineLengthForAutoWrap="1" placeDirectionSymbol="0"/>
          <placement polygonPlacementFlags="2" offsetUnits="MM" maxCurvedCharAngleOut="-25" distUnits="MM" lineAnchorPercent="0.5" lineAnchorType="0" repeatDistanceUnits="MM" geometryGeneratorType="PointGeometry" overrunDistanceUnit="MM" preserveRotation="1" geometryGenerator="" overrunDistance="0" centroidInside="0" repeatDistance="0" lineAnchorClipping="0" yOffset="0" rotationAngle="0" distMapUnitScale="3x:0,0,0,0,0,0" xOffset="0" geometryGeneratorEnabled="0" placementFlags="10" priority="5" dist="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" rotationUnit="AngleDegrees" quadOffset="4" maxCurvedCharAngleIn="25" offsetType="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" centroidWhole="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" placement="1" layerType="PolygonGeometry" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0"/>
          <rendering upsidedownLabels="0" scaleVisibility="0" limitNumLabels="0" zIndex="0" fontMinPixelSize="3" unplacedVisibility="0" obstacleFactor="1" scaleMin="0" mergeLines="0" obstacleType="0" obstacle="1" labelPerPart="0" fontMaxPixelSize="10000" displayAll="0" maxNumLabels="2000" drawLabels="1" minFeatureSize="0" scaleMax="0" fontLimitPixelSize="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" type="QString" value="pole_of_inaccessibility"/>
              <Option name="blendMode" type="int" value="0"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
              <Option name="drawToAllParts" type="bool" value="false"/>
              <Option name="enabled" type="QString" value="0"/>
              <Option name="labelAnchorPoint" type="QString" value="point_on_exterior"/>
              <Option name="lineSymbol" type="QString" value="&lt;symbol clip_to_extent=&quot;1&quot; name=&quot;symbol&quot; type=&quot;line&quot; force_rhr=&quot;0&quot; alpha=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer locked=&quot;0&quot; pass=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;align_dash_pattern&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;capstyle&quot; type=&quot;QString&quot; value=&quot;square&quot;/>&lt;Option name=&quot;customdash&quot; type=&quot;QString&quot; value=&quot;5;2&quot;/>&lt;Option name=&quot;customdash_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option name=&quot;customdash_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;dash_pattern_offset&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;dash_pattern_offset_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option name=&quot;dash_pattern_offset_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;draw_inside_polygon&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;joinstyle&quot; type=&quot;QString&quot; value=&quot;bevel&quot;/>&lt;Option name=&quot;line_color&quot; type=&quot;QString&quot; value=&quot;60,60,60,255&quot;/>&lt;Option name=&quot;line_style&quot; type=&quot;QString&quot; value=&quot;solid&quot;/>&lt;Option name=&quot;line_width&quot; type=&quot;QString&quot; value=&quot;0.3&quot;/>&lt;Option name=&quot;line_width_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;offset&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;offset_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option name=&quot;offset_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;ring_filter&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;trim_distance_end&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;trim_distance_end_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option name=&quot;trim_distance_end_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;trim_distance_start&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;trim_distance_start_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option name=&quot;trim_distance_start_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;tweak_dash_pattern_on_corners&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;use_custom_dash&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;width_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
              <Option name="minLength" type="double" value="0"/>
              <Option name="minLengthMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="minLengthUnit" type="QString" value="MM"/>
              <Option name="offsetFromAnchor" type="double" value="0"/>
              <Option name="offsetFromAnchorMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromAnchorUnit" type="QString" value="MM"/>
              <Option name="offsetFromLabel" type="double" value="0"/>
              <Option name="offsetFromLabelMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromLabelUnit" type="QString" value="MM"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <Option/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector" showLabelLegend="0"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="fid" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Name" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Status" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Drafted" type="QString" value="Drafted"/>
              </Option>
              <Option type="Map">
                <Option name="Planned" type="QString" value="Planned"/>
              </Option>
              <Option type="Map">
                <Option name="Built" type="QString" value="Built"/>
              </Option>
              <Option type="Map">
                <Option name="Superseded (was Planned)" type="QString" value="PlannedSuperseded"/>
              </Option>
              <Option type="Map">
                <Option name="Superseded (was Built)" type="QString" value="BuiltSuperseded"/>
              </Option>
              <Option type="Map">
                <Option name="Archived (was Planned)" type="QString" value="PlannedArchived"/>
              </Option>
              <Option type="Map">
                <Option name="Archived (was Built)" type="QString" value="BuiltArchived"/>
              </Option>
              <Option type="Map">
                <Option name="Undefined" type="QString" value="Undefined"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="Area (km²)" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Perimeter (km)" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Build Fence" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Area (km²)" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Perimeter (km)" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""/>
    <alias field="Name" index="1" name=""/>
    <alias field="Status" index="2" name=""/>
    <alias field="Area (km²)" index="3" name=""/>
    <alias field="Perimeter (km)" index="4" name=""/>
    <alias field="Build Fence" index="5" name=""/>
    <alias field="Rounded Area (km²)" index="6" name="Area (km²)"/>
    <alias field="Rounded Perimeter (km)" index="7" name="Perimeter (km)"/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="Name" applyOnUpdate="0"/>
    <default expression="Undefined" field="Status" applyOnUpdate="0"/>
    <default expression="" field="Area (km²)" applyOnUpdate="0"/>
    <default expression="" field="Perimeter (km)" applyOnUpdate="0"/>
    <default expression="" field="Build Fence" applyOnUpdate="0"/>
    <default expression="" field="Rounded Area (km²)" applyOnUpdate="0"/>
    <default expression="" field="Rounded Perimeter (km)" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" field="fid" unique_strength="1" exp_strength="0" constraints="3"/>
    <constraint notnull_strength="0" field="Name" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Status" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Area (km²)" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Perimeter (km)" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Build Fence" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Rounded Area (km²)" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Rounded Perimeter (km)" unique_strength="0" exp_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="fid" desc=""/>
    <constraint exp="" field="Name" desc=""/>
    <constraint exp="" field="Status" desc=""/>
    <constraint exp="" field="Area (km²)" desc=""/>
    <constraint exp="" field="Perimeter (km)" desc=""/>
    <constraint exp="" field="Build Fence" desc=""/>
    <constraint exp="" field="Rounded Area (km²)" desc=""/>
    <constraint exp="" field="Rounded Perimeter (km)" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field comment="" expression="round(&quot;Area (km²)&quot;, 2)" typeName="" name="Rounded Area (km²)" subType="0" precision="0" type="6" length="0"/>
    <field comment="" expression="round(&quot;Perimeter (km)&quot;, 2)" typeName="" name="Rounded Perimeter (km)" subType="0" precision="0" type="6" length="0"/>
  </expressionfields>
  <attributeactions/>
  <attributetableconfig sortExpression="&quot;fid&quot;" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="0" width="-1" name="fid" type="field"/>
      <column hidden="0" width="-1" name="Status" type="field"/>
      <column hidden="1" width="-1" name="Area (km²)" type="field"/>
      <column hidden="1" width="-1" name="Perimeter (km)" type="field"/>
      <column hidden="1" width="-1" name="AE/km²" type="field"/>
      <column hidden="0" width="-1" name="Build Fence" type="field"/>
      <column hidden="1" width="-1" name="AE" type="field"/>
      <column hidden="1" width="-1" name="Potential AE" type="field"/>
      <column hidden="0" width="-1" name="Name" type="field"/>
      <column hidden="0" width="-1" name="Paddock" type="field"/>
      <column hidden="1" width="-1" name="Potential AE/km²" type="field"/>
      <column hidden="1" width="-1" name="Watered Area (km²)" type="field"/>
      <column hidden="0" width="-1" name="Timeframe" type="field"/>
      <column hidden="0" width="-1" name="Rounded Area (km²)" type="field"/>
      <column hidden="0" width="-1" name="Rounded Perimeter (km)" type="field"/>
      <column hidden="0" width="-1" name="Rounded AE/km²" type="field"/>
      <column hidden="0" width="-1" name="Rounded AE" type="field"/>
      <column hidden="0" width="-1" name="Rounded Potential AE/km²" type="field"/>
      <column hidden="0" width="-1" name="Rounded Potential AE" type="field"/>
      <column hidden="0" width="-1" name="Rounded Watered Area (km²)" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
    geom = feature.geometry()
    control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="AE"/>
    <field editable="1" name="AE/km²"/>
    <field editable="1" name="Area (km²)"/>
    <field editable="1" name="Build Fence"/>
    <field editable="1" name="Complete"/>
    <field editable="1" name="Current"/>
    <field editable="1" name="Name"/>
    <field editable="1" name="Paddock"/>
    <field editable="1" name="Perimeter (km)"/>
    <field editable="1" name="Potential AE"/>
    <field editable="1" name="Potential AE/km²"/>
    <field editable="0" name="Rounded AE"/>
    <field editable="0" name="Rounded AE/km²"/>
    <field editable="0" name="Rounded Area (km²)"/>
    <field editable="0" name="Rounded Perimeter (km)"/>
    <field editable="0" name="Rounded Potential AE"/>
    <field editable="0" name="Rounded Potential AE/km²"/>
    <field editable="0" name="Rounded Watered Area (km²)"/>
    <field editable="1" name="Status"/>
    <field editable="1" name="Timeframe"/>
    <field editable="1" name="Watered Area (km²)"/>
    <field editable="1" name="fid"/>
  </editable>
  <labelOnTop>
    <field name="AE" labelOnTop="0"/>
    <field name="AE/km²" labelOnTop="0"/>
    <field name="Area (km²)" labelOnTop="0"/>
    <field name="Build Fence" labelOnTop="0"/>
    <field name="Complete" labelOnTop="0"/>
    <field name="Current" labelOnTop="0"/>
    <field name="Name" labelOnTop="1"/>
    <field name="Paddock" labelOnTop="0"/>
    <field name="Perimeter (km)" labelOnTop="0"/>
    <field name="Potential AE" labelOnTop="0"/>
    <field name="Potential AE/km²" labelOnTop="0"/>
    <field name="Rounded AE" labelOnTop="0"/>
    <field name="Rounded AE/km²" labelOnTop="0"/>
    <field name="Rounded Area (km²)" labelOnTop="0"/>
    <field name="Rounded Perimeter (km)" labelOnTop="0"/>
    <field name="Rounded Potential AE" labelOnTop="0"/>
    <field name="Rounded Potential AE/km²" labelOnTop="0"/>
    <field name="Rounded Watered Area (km²)" labelOnTop="0"/>
    <field name="Status" labelOnTop="1"/>
    <field name="Timeframe" labelOnTop="0"/>
    <field name="Watered Area (km²)" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field reuseLastValue="0" name="AE"/>
    <field reuseLastValue="0" name="AE/km²"/>
    <field reuseLastValue="0" name="Area (km²)"/>
    <field reuseLastValue="0" name="Build Fence"/>
    <field reuseLastValue="0" name="Complete"/>
    <field reuseLastValue="0" name="Condition"/>
    <field reuseLastValue="0" name="Current"/>
    <field reuseLastValue="0" name="Name"/>
    <field reuseLastValue="0" name="Paddock"/>
    <field reuseLastValue="0" name="Perimeter (km)"/>
    <field reuseLastValue="0" name="Potential AE"/>
    <field reuseLastValue="0" name="Potential AE/km²"/>
    <field reuseLastValue="0" name="Rounded AE"/>
    <field reuseLastValue="0" name="Rounded AE/km²"/>
    <field reuseLastValue="0" name="Rounded Area (km²)"/>
    <field reuseLastValue="0" name="Rounded Perimeter (km)"/>
    <field reuseLastValue="0" name="Rounded Potential AE"/>
    <field reuseLastValue="0" name="Rounded Potential AE/km²"/>
    <field reuseLastValue="0" name="Rounded Watered Area (km²)"/>
    <field reuseLastValue="0" name="Status"/>
    <field reuseLastValue="0" name="Timeframe"/>
    <field reuseLastValue="0" name="Watered Area (km²)"/>
    <field reuseLastValue="0" name="fid"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"Name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
