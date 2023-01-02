<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" labelsEnabled="1" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms|AttributeTable" version="3.22.13-Białowieża">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 referencescale="-1" type="singleSymbol" symbollevels="0" forceraster="0" enableorderby="0">
    <symbols>
      <symbol name="0" type="fill" force_rhr="0" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties" type="Map">
              <Option name="alpha" type="Map">
                <Option name="active" type="bool" value="true"/>
                <Option name="expression" type="QString" value="case&#xd;&#xa;when matchCurrentFeatureStatus(&quot;Status&quot;) then 100.0&#xd;&#xa;else 0.0&#xd;&#xa;end"/>
                <Option name="type" type="int" value="3"/>
              </Option>
            </Option>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleFill" pass="0">
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
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="60,179,113,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,178" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.4" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
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
    <rules key="{21fd22de-0e88-45c3-a395-76d6f4fe7f55}">
      <rule filter="&quot;Area (km²)&quot; > 5 and matchCurrentFeatureStatus(&quot;Status&quot;)" key="{11e68d6d-61d9-4100-a265-56fc337e0dae}">
        <settings calloutType="simple">
          <text-style fontSizeUnit="Point" blendMode="0" fieldName=" title(  &quot;Name&quot; ||  '\n' || round(  &quot;Area (km²)&quot;  ,1) || 'km²')" legendString="Aa" textOrientation="horizontal" fontItalic="0" multilineHeight="1" namedStyle="Bold" textColor="0,0,0,255" allowHtml="0" useSubstitutions="0" fontSize="12" textOpacity="1" fontStrikeout="0" fontLetterSpacing="0" fontFamily="Arial" fontUnderline="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" previewBkgrdColor="0,251,0,255" fontKerning="1" capitalization="0" fontWeight="75" fontWordSpacing="0" isExpression="1">
            <families/>
            <text-buffer bufferBlendMode="0" bufferOpacity="1" bufferSizeUnits="MM" bufferColor="255,255,255,255" bufferJoinStyle="128" bufferNoFill="1" bufferDraw="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSize="0.29999999999999999"/>
            <text-mask maskEnabled="0" maskType="0" maskOpacity="1" maskSizeUnits="MM" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskedSymbolLayers="" maskSize="0" maskJoinStyle="128"/>
            <background shapeRadiiX="0" shapeBorderWidth="0" shapeRotation="0" shapeOffsetX="0" shapeSizeUnit="MM" shapeOffsetUnit="MM" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeOffsetY="0" shapeFillColor="255,255,255,255" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeJoinStyle="64" shapeBlendMode="0" shapeRotationType="0" shapeRadiiY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeX="0" shapeSizeY="0" shapeBorderColor="128,128,128,255" shapeBorderWidthUnit="MM" shapeSizeType="0" shapeRadiiUnit="MM" shapeSVGFile="" shapeDraw="0">
              <symbol name="markerSymbol" type="marker" force_rhr="0" alpha="1" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" type="QString" value=""/>
                    <Option name="properties"/>
                    <Option name="type" type="QString" value="collection"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" locked="0" class="SimpleMarker" pass="0">
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
                  <prop v="0" k="angle"/>
                  <prop v="square" k="cap_style"/>
                  <prop v="125,139,143,255" k="color"/>
                  <prop v="1" k="horizontal_anchor_point"/>
                  <prop v="bevel" k="joinstyle"/>
                  <prop v="circle" k="name"/>
                  <prop v="0,0" k="offset"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
                  <prop v="MM" k="offset_unit"/>
                  <prop v="35,35,35,255" k="outline_color"/>
                  <prop v="solid" k="outline_style"/>
                  <prop v="0" k="outline_width"/>
                  <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
                  <prop v="MM" k="outline_width_unit"/>
                  <prop v="diameter" k="scale_method"/>
                  <prop v="2" k="size"/>
                  <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
                  <prop v="MM" k="size_unit"/>
                  <prop v="1" k="vertical_anchor_point"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" type="QString" value=""/>
                      <Option name="properties"/>
                      <Option name="type" type="QString" value="collection"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
              <symbol name="fillSymbol" type="fill" force_rhr="0" alpha="1" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" type="QString" value=""/>
                    <Option name="properties"/>
                    <Option name="type" type="QString" value="collection"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" locked="0" class="SimpleFill" pass="0">
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
                  <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
                  <prop v="255,255,255,255" k="color"/>
                  <prop v="bevel" k="joinstyle"/>
                  <prop v="0,0" k="offset"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
                  <prop v="MM" k="offset_unit"/>
                  <prop v="128,128,128,255" k="outline_color"/>
                  <prop v="no" k="outline_style"/>
                  <prop v="0" k="outline_width"/>
                  <prop v="MM" k="outline_width_unit"/>
                  <prop v="solid" k="style"/>
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
            <shadow shadowUnder="0" shadowRadius="1.5" shadowColor="0,0,0,255" shadowOffsetUnit="MM" shadowOpacity="0.69999999999999996" shadowOffsetAngle="135" shadowBlendMode="6" shadowOffsetDist="1" shadowDraw="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM" shadowRadiusAlphaOnly="0" shadowOffsetGlobal="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format reverseDirectionSymbol="0" decimals="3" placeDirectionSymbol="0" wrapChar="" rightDirectionSymbol=">" addDirectionSymbol="0" leftDirectionSymbol="&lt;" multilineAlign="1" autoWrapLength="9" plussign="0" useMaxLineLengthForAutoWrap="1" formatNumbers="0"/>
          <placement maxCurvedCharAngleOut="-25" centroidInside="0" xOffset="0" quadOffset="4" lineAnchorPercent="0.5" lineAnchorType="0" maxCurvedCharAngleIn="25" overrunDistance="0" layerType="PolygonGeometry" rotationAngle="0" placementFlags="10" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" offsetType="0" priority="5" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="1" geometryGenerator="" polygonPlacementFlags="2" lineAnchorClipping="0" geometryGeneratorType="PointGeometry" dist="0" repeatDistanceUnits="MM" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" repeatDistance="0" centroidWhole="0" distMapUnitScale="3x:0,0,0,0,0,0" placement="1" fitInPolygonOnly="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" geometryGeneratorEnabled="0" distUnits="MM" overrunDistanceUnit="MM" yOffset="0" rotationUnit="AngleDegrees"/>
          <rendering drawLabels="1" obstacleFactor="1" fontMaxPixelSize="10000" minFeatureSize="0" zIndex="0" scaleMin="0" limitNumLabels="0" fontMinPixelSize="3" obstacle="1" displayAll="0" upsidedownLabels="0" scaleVisibility="0" mergeLines="0" fontLimitPixelSize="0" maxNumLabels="2000" labelPerPart="0" unplacedVisibility="0" obstacleType="0" scaleMax="0"/>
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
              <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; type=&quot;line&quot; force_rhr=&quot;0&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer enabled=&quot;1&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;align_dash_pattern&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;capstyle&quot; type=&quot;QString&quot; value=&quot;square&quot;/>&lt;Option name=&quot;customdash&quot; type=&quot;QString&quot; value=&quot;5;2&quot;/>&lt;Option name=&quot;customdash_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option name=&quot;customdash_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;dash_pattern_offset&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;dash_pattern_offset_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option name=&quot;dash_pattern_offset_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;draw_inside_polygon&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;joinstyle&quot; type=&quot;QString&quot; value=&quot;bevel&quot;/>&lt;Option name=&quot;line_color&quot; type=&quot;QString&quot; value=&quot;60,60,60,255&quot;/>&lt;Option name=&quot;line_style&quot; type=&quot;QString&quot; value=&quot;solid&quot;/>&lt;Option name=&quot;line_width&quot; type=&quot;QString&quot; value=&quot;0.3&quot;/>&lt;Option name=&quot;line_width_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;offset&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;offset_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option name=&quot;offset_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;ring_filter&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;trim_distance_end&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;trim_distance_end_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option name=&quot;trim_distance_end_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;trim_distance_start&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;trim_distance_start_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option name=&quot;trim_distance_start_unit&quot; type=&quot;QString&quot; value=&quot;MM&quot;/>&lt;Option name=&quot;tweak_dash_pattern_on_corners&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;use_custom_dash&quot; type=&quot;QString&quot; value=&quot;0&quot;/>&lt;Option name=&quot;width_map_unit_scale&quot; type=&quot;QString&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;/Option>&lt;prop v=&quot;0&quot; k=&quot;align_dash_pattern&quot;/>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;dash_pattern_offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;dash_pattern_offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;trim_distance_end&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;trim_distance_end_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;trim_distance_end_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;trim_distance_start&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;trim_distance_start_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;trim_distance_start_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
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
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <fieldConfiguration>
    <field name="fid" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Paddock" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Name" configurationFlags="None">
      <editWidget type="TextEdit">
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
                <Option name="Archived" type="QString" value="Archived"/>
              </Option>
              <Option type="Map">
                <Option name="Undefined" type="QString" value="Undefined"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="Timeframe" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Historical" type="QString" value="Historical"/>
              </Option>
              <Option type="Map">
                <Option name="Current" type="QString" value="Current"/>
              </Option>
              <Option type="Map">
                <Option name="Future" type="QString" value="Future"/>
              </Option>
              <Option type="Map">
                <Option name="Drafted" type="QString" value="Drafted"/>
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
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Perimeter (km)" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Build Fence" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AE/km²" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AE" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Potential AE/km²" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Potential AE" configurationFlags="None">
      <editWidget type="TextEdit">
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
    <field name="Rounded AE/km²" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded AE" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Potential AE/km²" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Potential AE" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="fid" index="0"/>
    <alias name="" field="Paddock" index="1"/>
    <alias name="" field="Name" index="2"/>
    <alias name="" field="Status" index="3"/>
    <alias name="" field="Timeframe" index="4"/>
    <alias name="" field="Area (km²)" index="5"/>
    <alias name="" field="Perimeter (km)" index="6"/>
    <alias name="" field="Build Fence" index="7"/>
    <alias name="" field="AE/km²" index="8"/>
    <alias name="" field="AE" index="9"/>
    <alias name="" field="Potential AE/km²" index="10"/>
    <alias name="" field="Potential AE" index="11"/>
    <alias name="Area (km²)" field="Rounded Area (km²)" index="12"/>
    <alias name="Perimeter (km)" field="Rounded Perimeter (km)" index="13"/>
    <alias name="AE/km²" field="Rounded AE/km²" index="14"/>
    <alias name="AE" field="Rounded AE" index="15"/>
    <alias name="Potential AE/km²" field="Rounded Potential AE/km²" index="16"/>
    <alias name="Potential AE" field="Rounded Potential AE" index="17"/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="Paddock" expression="" applyOnUpdate="0"/>
    <default field="Name" expression="" applyOnUpdate="0"/>
    <default field="Status" expression="Undefined" applyOnUpdate="0"/>
    <default field="Timeframe" expression="'Undefined'" applyOnUpdate="0"/>
    <default field="Area (km²)" expression="" applyOnUpdate="0"/>
    <default field="Perimeter (km)" expression="" applyOnUpdate="0"/>
    <default field="Build Fence" expression="" applyOnUpdate="0"/>
    <default field="AE/km²" expression="" applyOnUpdate="0"/>
    <default field="AE" expression="" applyOnUpdate="0"/>
    <default field="Potential AE/km²" expression="" applyOnUpdate="0"/>
    <default field="Potential AE" expression="" applyOnUpdate="0"/>
    <default field="Rounded Area (km²)" expression="" applyOnUpdate="0"/>
    <default field="Rounded Perimeter (km)" expression="" applyOnUpdate="0"/>
    <default field="Rounded AE/km²" expression="" applyOnUpdate="0"/>
    <default field="Rounded AE" expression="" applyOnUpdate="0"/>
    <default field="Rounded Potential AE/km²" expression="" applyOnUpdate="0"/>
    <default field="Rounded Potential AE" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" exp_strength="0" unique_strength="1" constraints="3" notnull_strength="1"/>
    <constraint field="Paddock" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Name" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Status" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Timeframe" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Area (km²)" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Perimeter (km)" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Build Fence" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="AE/km²" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="AE" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Potential AE/km²" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Potential AE" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Rounded Area (km²)" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Rounded Perimeter (km)" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Rounded AE/km²" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Rounded AE" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Rounded Potential AE/km²" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="Rounded Potential AE" exp_strength="0" unique_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="fid"/>
    <constraint desc="" exp="" field="Paddock"/>
    <constraint desc="" exp="" field="Name"/>
    <constraint desc="" exp="" field="Status"/>
    <constraint desc="" exp="" field="Timeframe"/>
    <constraint desc="" exp="" field="Area (km²)"/>
    <constraint desc="" exp="" field="Perimeter (km)"/>
    <constraint desc="" exp="" field="Build Fence"/>
    <constraint desc="" exp="" field="AE/km²"/>
    <constraint desc="" exp="" field="AE"/>
    <constraint desc="" exp="" field="Potential AE/km²"/>
    <constraint desc="" exp="" field="Potential AE"/>
    <constraint desc="" exp="" field="Rounded Area (km²)"/>
    <constraint desc="" exp="" field="Rounded Perimeter (km)"/>
    <constraint desc="" exp="" field="Rounded AE/km²"/>
    <constraint desc="" exp="" field="Rounded AE"/>
    <constraint desc="" exp="" field="Rounded Potential AE/km²"/>
    <constraint desc="" exp="" field="Rounded Potential AE"/>
  </constraintExpressions>
  <expressionfields>
    <field typeName="" name="Rounded Area (km²)" subType="0" type="6" expression="round(&quot;Area (km²)&quot;, 2)" length="0" precision="0" comment=""/>
    <field typeName="" name="Rounded Perimeter (km)" subType="0" type="6" expression="round(&quot;Perimeter (km)&quot;, 2)" length="0" precision="0" comment=""/>
    <field typeName="" name="Rounded AE/km²" subType="0" type="6" expression="round(&quot;AE/km²&quot;, 1)" length="0" precision="0" comment=""/>
    <field typeName="" name="Rounded AE" subType="0" type="6" expression="round(&quot;AE&quot;, 0)" length="0" precision="0" comment=""/>
    <field typeName="" name="Rounded Potential AE/km²" subType="0" type="6" expression="round(&quot;Potential AE/km²&quot;, 1)" length="0" precision="0" comment=""/>
    <field typeName="" name="Rounded Potential AE" subType="0" type="6" expression="round(&quot;Potential AE&quot;, 0)" length="0" precision="0" comment=""/>
  </expressionfields>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="&quot;fid&quot;" sortOrder="0">
    <columns>
      <column name="fid" type="field" hidden="0" width="-1"/>
      <column name="Status" type="field" hidden="0" width="-1"/>
      <column name="Area (km²)" type="field" hidden="1" width="-1"/>
      <column name="Perimeter (km)" type="field" hidden="1" width="-1"/>
      <column name="AE/km²" type="field" hidden="1" width="-1"/>
      <column name="Build Fence" type="field" hidden="0" width="-1"/>
      <column name="AE" type="field" hidden="1" width="-1"/>
      <column name="Potential AE" type="field" hidden="1" width="-1"/>
      <column name="Name" type="field" hidden="0" width="-1"/>
      <column name="Paddock" type="field" hidden="0" width="-1"/>
      <column name="Potential AE/km²" type="field" hidden="1" width="-1"/>
      <column name="Timeframe" type="field" hidden="0" width="-1"/>
      <column name="Rounded Area (km²)" type="field" hidden="0" width="-1"/>
      <column name="Rounded Perimeter (km)" type="field" hidden="0" width="-1"/>
      <column name="Rounded AE/km²" type="field" hidden="0" width="-1"/>
      <column name="Rounded AE" type="field" hidden="0" width="-1"/>
      <column name="Rounded Potential AE/km²" type="field" hidden="0" width="-1"/>
      <column name="Rounded Potential AE" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
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
    <field name="AE" editable="1"/>
    <field name="AE/km²" editable="1"/>
    <field name="Area (km²)" editable="1"/>
    <field name="Build Fence" editable="1"/>
    <field name="Complete" editable="1"/>
    <field name="Current" editable="1"/>
    <field name="Name" editable="1"/>
    <field name="Paddock" editable="1"/>
    <field name="Perimeter (km)" editable="1"/>
    <field name="Potential AE" editable="1"/>
    <field name="Potential AE/km²" editable="1"/>
    <field name="Rounded AE" editable="0"/>
    <field name="Rounded AE/km²" editable="0"/>
    <field name="Rounded Area (km²)" editable="0"/>
    <field name="Rounded Perimeter (km)" editable="0"/>
    <field name="Rounded Potential AE" editable="0"/>
    <field name="Rounded Potential AE/km²" editable="0"/>
    <field name="Status" editable="1"/>
    <field name="Timeframe" editable="1"/>
    <field name="fid" editable="1"/>
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
    <field name="Status" labelOnTop="1"/>
    <field name="Timeframe" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="AE" reuseLastValue="0"/>
    <field name="AE/km²" reuseLastValue="0"/>
    <field name="Area (km²)" reuseLastValue="0"/>
    <field name="Build Fence" reuseLastValue="0"/>
    <field name="Complete" reuseLastValue="0"/>
    <field name="Condition" reuseLastValue="0"/>
    <field name="Current" reuseLastValue="0"/>
    <field name="Name" reuseLastValue="0"/>
    <field name="Paddock" reuseLastValue="0"/>
    <field name="Perimeter (km)" reuseLastValue="0"/>
    <field name="Potential AE" reuseLastValue="0"/>
    <field name="Potential AE/km²" reuseLastValue="0"/>
    <field name="Rounded AE" reuseLastValue="0"/>
    <field name="Rounded AE/km²" reuseLastValue="0"/>
    <field name="Rounded Area (km²)" reuseLastValue="0"/>
    <field name="Rounded Perimeter (km)" reuseLastValue="0"/>
    <field name="Rounded Potential AE" reuseLastValue="0"/>
    <field name="Rounded Potential AE/km²" reuseLastValue="0"/>
    <field name="Status" reuseLastValue="0"/>
    <field name="Timeframe" reuseLastValue="0"/>
    <field name="fid" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"Name"</previewExpression>
  <layerGeometryType>2</layerGeometryType>
</qgis>
