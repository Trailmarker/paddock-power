<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms|AttributeTable" labelsEnabled="1" version="3.22.14-Białowieża">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 enableorderby="0" symbollevels="0" referencescale="-1" type="singleSymbol" forceraster="0">
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" name="0" alpha="1" type="fill">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties" type="Map">
              <Option name="alpha" type="Map">
                <Option value="true" name="active" type="bool"/>
                <Option value="case&#xd;&#xa;when matchCurrentTimeframe(&quot;Timeframe&quot;) then 100.0&#xd;&#xa;else 0.0&#xd;&#xa;end" name="expression" type="QString"/>
                <Option value="3" name="type" type="int"/>
              </Option>
            </Option>
            <Option value="collection" name="type" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleFill" pass="0">
          <Option type="Map">
            <Option value="3x:0,0,0,0,0,0" name="border_width_map_unit_scale" type="QString"/>
            <Option value="60,179,113,255" name="color" type="QString"/>
            <Option value="bevel" name="joinstyle" type="QString"/>
            <Option value="0,0" name="offset" type="QString"/>
            <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
            <Option value="MM" name="offset_unit" type="QString"/>
            <Option value="35,35,35,178" name="outline_color" type="QString"/>
            <Option value="solid" name="outline_style" type="QString"/>
            <Option value="0.4" name="outline_width" type="QString"/>
            <Option value="MM" name="outline_width_unit" type="QString"/>
            <Option value="solid" name="style" type="QString"/>
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{a0101363-e0a9-4d70-a7ae-21810c8ec23b}">
      <rule filter="&quot;Area (km²)&quot; > 5 and matchCurrentFeatureStatus(&quot;Status&quot;)" key="{5c2616fd-369b-48ac-938e-43cfbdc6dcc2}">
        <settings calloutType="simple">
          <text-style fontSize="12" fontWeight="75" fontLetterSpacing="0" multilineHeight="1" fontStrikeout="0" fontFamily="Arial" blendMode="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontWordSpacing="0" allowHtml="0" namedStyle="Bold" fontUnderline="0" isExpression="1" textColor="0,0,0,255" previewBkgrdColor="0,251,0,255" textOrientation="horizontal" useSubstitutions="0" fontKerning="1" legendString="Aa" fontItalic="0" textOpacity="1" fieldName=" title(  &quot;Name&quot; ||  '\n' || round(  &quot;Area (km²)&quot;  ,1) || 'km²')" capitalization="0" fontSizeUnit="Point">
            <families/>
            <text-buffer bufferJoinStyle="128" bufferBlendMode="0" bufferNoFill="1" bufferDraw="1" bufferSize="0.29999999999999999" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferColor="255,255,255,255" bufferOpacity="1" bufferSizeUnits="MM"/>
            <text-mask maskType="0" maskSize="0" maskOpacity="1" maskedSymbolLayers="" maskEnabled="0" maskSizeUnits="MM" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskJoinStyle="128"/>
            <background shapeFillColor="255,255,255,255" shapeRotation="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeOffsetX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeBorderColor="128,128,128,255" shapeBorderWidth="0" shapeRadiiY="0" shapeSizeX="0" shapeType="0" shapeBorderWidthUnit="MM" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeSizeUnit="MM" shapeRadiiX="0" shapeJoinStyle="64" shapeSVGFile="" shapeOpacity="1" shapeRadiiUnit="MM" shapeRotationType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeOffsetY="0" shapeOffsetUnit="MM">
              <symbol clip_to_extent="1" force_rhr="0" name="markerSymbol" alpha="1" type="marker">
                <data_defined_properties>
                  <Option type="Map">
                    <Option value="" name="name" type="QString"/>
                    <Option name="properties"/>
                    <Option value="collection" name="type" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" locked="0" class="SimpleMarker" pass="0">
                  <Option type="Map">
                    <Option value="0" name="angle" type="QString"/>
                    <Option value="square" name="cap_style" type="QString"/>
                    <Option value="125,139,143,255" name="color" type="QString"/>
                    <Option value="1" name="horizontal_anchor_point" type="QString"/>
                    <Option value="bevel" name="joinstyle" type="QString"/>
                    <Option value="circle" name="name" type="QString"/>
                    <Option value="0,0" name="offset" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
                    <Option value="MM" name="offset_unit" type="QString"/>
                    <Option value="35,35,35,255" name="outline_color" type="QString"/>
                    <Option value="solid" name="outline_style" type="QString"/>
                    <Option value="0" name="outline_width" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="outline_width_map_unit_scale" type="QString"/>
                    <Option value="MM" name="outline_width_unit" type="QString"/>
                    <Option value="diameter" name="scale_method" type="QString"/>
                    <Option value="2" name="size" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="size_map_unit_scale" type="QString"/>
                    <Option value="MM" name="size_unit" type="QString"/>
                    <Option value="1" name="vertical_anchor_point" type="QString"/>
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
                      <Option value="" name="name" type="QString"/>
                      <Option name="properties"/>
                      <Option value="collection" name="type" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
              <symbol clip_to_extent="1" force_rhr="0" name="fillSymbol" alpha="1" type="fill">
                <data_defined_properties>
                  <Option type="Map">
                    <Option value="" name="name" type="QString"/>
                    <Option name="properties"/>
                    <Option value="collection" name="type" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" locked="0" class="SimpleFill" pass="0">
                  <Option type="Map">
                    <Option value="3x:0,0,0,0,0,0" name="border_width_map_unit_scale" type="QString"/>
                    <Option value="255,255,255,255" name="color" type="QString"/>
                    <Option value="bevel" name="joinstyle" type="QString"/>
                    <Option value="0,0" name="offset" type="QString"/>
                    <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
                    <Option value="MM" name="offset_unit" type="QString"/>
                    <Option value="128,128,128,255" name="outline_color" type="QString"/>
                    <Option value="no" name="outline_style" type="QString"/>
                    <Option value="0" name="outline_width" type="QString"/>
                    <Option value="MM" name="outline_width_unit" type="QString"/>
                    <Option value="solid" name="style" type="QString"/>
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
                      <Option value="" name="name" type="QString"/>
                      <Option name="properties"/>
                      <Option value="collection" name="type" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowOffsetDist="1" shadowScale="100" shadowOffsetAngle="135" shadowRadiusUnit="MM" shadowBlendMode="6" shadowUnder="0" shadowRadiusAlphaOnly="0" shadowDraw="0" shadowOffsetGlobal="1" shadowOpacity="0.69999999999999996" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadius="1.5"/>
            <dd_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format useMaxLineLengthForAutoWrap="1" autoWrapLength="9" decimals="3" plussign="0" leftDirectionSymbol="&lt;" rightDirectionSymbol=">" formatNumbers="0" multilineAlign="1" wrapChar="" placeDirectionSymbol="0" reverseDirectionSymbol="0" addDirectionSymbol="0"/>
          <placement distMapUnitScale="3x:0,0,0,0,0,0" lineAnchorClipping="0" placement="1" maxCurvedCharAngleOut="-25" quadOffset="4" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" yOffset="0" centroidWhole="0" priority="5" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" maxCurvedCharAngleIn="25" lineAnchorPercent="0.5" centroidInside="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="1" lineAnchorType="0" offsetType="0" dist="0" rotationAngle="0" distUnits="MM" repeatDistanceUnits="MM" polygonPlacementFlags="2" offsetUnits="MM" rotationUnit="AngleDegrees" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" placementFlags="10" xOffset="0" repeatDistance="0" layerType="PolygonGeometry" fitInPolygonOnly="0" geometryGeneratorEnabled="0" overrunDistanceUnit="MM" geometryGeneratorType="PointGeometry" overrunDistance="0"/>
          <rendering minFeatureSize="0" fontMaxPixelSize="10000" zIndex="0" displayAll="0" obstacleFactor="1" obstacle="1" scaleMin="0" fontMinPixelSize="3" labelPerPart="0" fontLimitPixelSize="0" scaleVisibility="0" unplacedVisibility="0" mergeLines="0" drawLabels="1" limitNumLabels="0" upsidedownLabels="0" scaleMax="0" maxNumLabels="2000" obstacleType="0"/>
          <dd_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option value="pole_of_inaccessibility" name="anchorPoint" type="QString"/>
              <Option value="0" name="blendMode" type="int"/>
              <Option name="ddProperties" type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
              <Option value="false" name="drawToAllParts" type="bool"/>
              <Option value="0" name="enabled" type="QString"/>
              <Option value="point_on_exterior" name="labelAnchorPoint" type="QString"/>
              <Option value="&lt;symbol clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; name=&quot;symbol&quot; alpha=&quot;1&quot; type=&quot;line&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer enabled=&quot;1&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;0&quot; name=&quot;align_dash_pattern&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;square&quot; name=&quot;capstyle&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;5;2&quot; name=&quot;customdash&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;customdash_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;customdash_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;dash_pattern_offset&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;dash_pattern_offset_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;dash_pattern_offset_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;draw_inside_polygon&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;bevel&quot; name=&quot;joinstyle&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;60,60,60,255&quot; name=&quot;line_color&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;solid&quot; name=&quot;line_style&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0.3&quot; name=&quot;line_width&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;line_width_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;offset&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;offset_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;offset_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;ring_filter&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;trim_distance_end&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_end_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_end_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;trim_distance_start&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_start_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_start_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;tweak_dash_pattern_on_corners&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;use_custom_dash&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;width_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol" type="QString"/>
              <Option value="0" name="minLength" type="double"/>
              <Option value="3x:0,0,0,0,0,0" name="minLengthMapUnitScale" type="QString"/>
              <Option value="MM" name="minLengthUnit" type="QString"/>
              <Option value="0" name="offsetFromAnchor" type="double"/>
              <Option value="3x:0,0,0,0,0,0" name="offsetFromAnchorMapUnitScale" type="QString"/>
              <Option value="MM" name="offsetFromAnchorUnit" type="QString"/>
              <Option value="0" name="offsetFromLabel" type="double"/>
              <Option value="3x:0,0,0,0,0,0" name="offsetFromLabelMapUnitScale" type="QString"/>
              <Option value="MM" name="offsetFromLabelUnit" type="QString"/>
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
                <Option value="Drafted" name="Drafted" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="Planned" name="Planned" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="Built" name="Built" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="PlannedSuperseded" name="Superseded (was Planned)" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="BuiltSuperseded" name="Superseded (was Built)" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="PlannedArchived" name="Archived (was Planned)" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="BuiltArchived" name="Archived (was Built)" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="Undefined" name="Undefined" type="QString"/>
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
                <Option value="Current" name="Current" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="Future" name="Future" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="Undefined" name="Undefined" type="QString"/>
              </Option>
            </Option>
          </Option>
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
    <field name="Perimeter (km)" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
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
    <field name="Watered Area (km²)" configurationFlags="None">
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
    <field name="Rounded Watered Area (km²)" configurationFlags="None">
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
    <alias index="0" name="" field="fid"/>
    <alias index="1" name="" field="Paddock"/>
    <alias index="2" name="" field="Name"/>
    <alias index="3" name="" field="Status"/>
    <alias index="4" name="" field="Timeframe"/>
    <alias index="5" name="" field="Build Fence"/>
    <alias index="6" name="" field="Perimeter (km)"/>
    <alias index="7" name="" field="Area (km²)"/>
    <alias index="8" name="" field="Watered Area (km²)"/>
    <alias index="9" name="" field="AE/km²"/>
    <alias index="10" name="" field="AE"/>
    <alias index="11" name="" field="Potential AE/km²"/>
    <alias index="12" name="" field="Potential AE"/>
    <alias index="13" name="Area (km²)" field="Rounded Area (km²)"/>
    <alias index="14" name="Perimeter (km)" field="Rounded Perimeter (km)"/>
    <alias index="15" name="Watered Area (km²)" field="Rounded Watered Area (km²)"/>
    <alias index="16" name="AE/km²" field="Rounded AE/km²"/>
    <alias index="17" name="AE" field="Rounded AE"/>
    <alias index="18" name="Potential AE/km²" field="Rounded Potential AE/km²"/>
    <alias index="19" name="Potential AE" field="Rounded Potential AE"/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="" applyOnUpdate="0" field="Paddock"/>
    <default expression="" applyOnUpdate="0" field="Name"/>
    <default expression="Undefined" applyOnUpdate="0" field="Status"/>
    <default expression="'Undefined'" applyOnUpdate="0" field="Timeframe"/>
    <default expression="" applyOnUpdate="0" field="Build Fence"/>
    <default expression="" applyOnUpdate="0" field="Perimeter (km)"/>
    <default expression="" applyOnUpdate="0" field="Area (km²)"/>
    <default expression="" applyOnUpdate="0" field="Watered Area (km²)"/>
    <default expression="" applyOnUpdate="0" field="AE/km²"/>
    <default expression="" applyOnUpdate="0" field="AE"/>
    <default expression="" applyOnUpdate="0" field="Potential AE/km²"/>
    <default expression="" applyOnUpdate="0" field="Potential AE"/>
    <default expression="" applyOnUpdate="0" field="Rounded Area (km²)"/>
    <default expression="" applyOnUpdate="0" field="Rounded Perimeter (km)"/>
    <default expression="" applyOnUpdate="0" field="Rounded Watered Area (km²)"/>
    <default expression="" applyOnUpdate="0" field="Rounded AE/km²"/>
    <default expression="" applyOnUpdate="0" field="Rounded AE"/>
    <default expression="" applyOnUpdate="0" field="Rounded Potential AE/km²"/>
    <default expression="" applyOnUpdate="0" field="Rounded Potential AE"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" constraints="3" notnull_strength="1" unique_strength="1" field="fid"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Paddock"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Name"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Status"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Timeframe"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Build Fence"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Perimeter (km)"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Area (km²)"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Watered Area (km²)"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="AE/km²"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="AE"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Potential AE/km²"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Potential AE"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Rounded Area (km²)"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Rounded Perimeter (km)"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Rounded Watered Area (km²)"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Rounded AE/km²"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Rounded AE"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Rounded Potential AE/km²"/>
    <constraint exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0" field="Rounded Potential AE"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="fid"/>
    <constraint desc="" exp="" field="Paddock"/>
    <constraint desc="" exp="" field="Name"/>
    <constraint desc="" exp="" field="Status"/>
    <constraint desc="" exp="" field="Timeframe"/>
    <constraint desc="" exp="" field="Build Fence"/>
    <constraint desc="" exp="" field="Perimeter (km)"/>
    <constraint desc="" exp="" field="Area (km²)"/>
    <constraint desc="" exp="" field="Watered Area (km²)"/>
    <constraint desc="" exp="" field="AE/km²"/>
    <constraint desc="" exp="" field="AE"/>
    <constraint desc="" exp="" field="Potential AE/km²"/>
    <constraint desc="" exp="" field="Potential AE"/>
    <constraint desc="" exp="" field="Rounded Area (km²)"/>
    <constraint desc="" exp="" field="Rounded Perimeter (km)"/>
    <constraint desc="" exp="" field="Rounded Watered Area (km²)"/>
    <constraint desc="" exp="" field="Rounded AE/km²"/>
    <constraint desc="" exp="" field="Rounded AE"/>
    <constraint desc="" exp="" field="Rounded Potential AE/km²"/>
    <constraint desc="" exp="" field="Rounded Potential AE"/>
  </constraintExpressions>
  <expressionfields>
    <field subType="0" precision="0" comment="" name="Rounded Area (km²)" typeName="" expression="round(&quot;Area (km²)&quot;, 2)" type="6" length="0"/>
    <field subType="0" precision="0" comment="" name="Rounded Perimeter (km)" typeName="" expression="round(&quot;Perimeter (km)&quot;, 2)" type="6" length="0"/>
    <field subType="0" precision="0" comment="" name="Rounded Perimeter (km)" typeName="" expression="round(&quot;Perimeter (km)&quot;, 2)" type="6" length="0"/>
    <field subType="0" precision="0" comment="" name="Rounded Area (km²)" typeName="" expression="round(&quot;Area (km²)&quot;, 2)" type="6" length="0"/>
    <field subType="0" precision="0" comment="" name="Rounded Watered Area (km²)" typeName="" expression="round(&quot;Watered Area (km²)&quot;, 2)" type="6" length="0"/>
    <field subType="0" precision="0" comment="" name="Rounded AE/km²" typeName="" expression="round(&quot;AE/km²&quot;, 1)" type="6" length="0"/>
    <field subType="0" precision="0" comment="" name="Rounded AE" typeName="" expression="round(&quot;AE&quot;, 0)" type="6" length="0"/>
    <field subType="0" precision="0" comment="" name="Rounded Potential AE/km²" typeName="" expression="round(&quot;Potential AE/km²&quot;, 1)" type="6" length="0"/>
    <field subType="0" precision="0" comment="" name="Rounded Potential AE" typeName="" expression="round(&quot;Potential AE&quot;, 0)" type="6" length="0"/>
  </expressionfields>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="&quot;fid&quot;" sortOrder="1">
    <columns>
      <column width="72" name="fid" hidden="0" type="field"/>
      <column width="107" name="Paddock" hidden="0" type="field"/>
      <column width="181" name="Name" hidden="0" type="field"/>
      <column width="-1" name="Build Fence" hidden="0" type="field"/>
      <column width="103" name="Status" hidden="0" type="field"/>
      <column width="-1" name="Timeframe" hidden="0" type="field"/>
      <column width="-1" name="Perimeter (km)" hidden="1" type="field"/>
      <column width="-1" name="Area (km²)" hidden="1" type="field"/>
      <column width="-1" name="Watered Area (km²)" hidden="1" type="field"/>
      <column width="-1" name="AE/km²" hidden="1" type="field"/>
      <column width="-1" name="Potential AE/km²" hidden="1" type="field"/>
      <column width="-1" name="AE" hidden="1" type="field"/>
      <column width="-1" name="Potential AE" hidden="1" type="field"/>
      <column width="161" name="Rounded Perimeter (km)" hidden="0" type="field"/>
      <column width="-1" name="Rounded Area (km²)" hidden="0" type="field"/>
      <column width="196" name="Rounded Watered Area (km²)" hidden="0" type="field"/>
      <column width="-1" name="Rounded AE/km²" hidden="0" type="field"/>
      <column width="191" name="Rounded Potential AE/km²" hidden="0" type="field"/>
      <column width="85" name="Rounded AE" hidden="0" type="field"/>
      <column width="-1" name="Rounded Potential AE" hidden="0" type="field"/>
      <column width="-1" hidden="1" type="actions"/>
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
    <field name="Rounded Watered Area (km²)" editable="0"/>
    <field name="Status" editable="1"/>
    <field name="Timeframe" editable="1"/>
    <field name="Watered Area (km²)" editable="1"/>
    <field name="fid" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="AE"/>
    <field labelOnTop="0" name="AE/km²"/>
    <field labelOnTop="0" name="Area (km²)"/>
    <field labelOnTop="0" name="Build Fence"/>
    <field labelOnTop="0" name="Complete"/>
    <field labelOnTop="0" name="Current"/>
    <field labelOnTop="1" name="Name"/>
    <field labelOnTop="0" name="Paddock"/>
    <field labelOnTop="0" name="Perimeter (km)"/>
    <field labelOnTop="0" name="Potential AE"/>
    <field labelOnTop="0" name="Potential AE/km²"/>
    <field labelOnTop="0" name="Rounded AE"/>
    <field labelOnTop="0" name="Rounded AE/km²"/>
    <field labelOnTop="0" name="Rounded Area (km²)"/>
    <field labelOnTop="0" name="Rounded Perimeter (km)"/>
    <field labelOnTop="0" name="Rounded Potential AE"/>
    <field labelOnTop="0" name="Rounded Potential AE/km²"/>
    <field labelOnTop="0" name="Rounded Watered Area (km²)"/>
    <field labelOnTop="1" name="Status"/>
    <field labelOnTop="0" name="Timeframe"/>
    <field labelOnTop="0" name="Watered Area (km²)"/>
    <field labelOnTop="0" name="fid"/>
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
  <layerGeometryType>2</layerGeometryType>
</qgis>
