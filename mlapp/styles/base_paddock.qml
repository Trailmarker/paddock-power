<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" version="3.22.14-Białowieża" labelsEnabled="1" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms|AttributeTable">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 referencescale="-1" forceraster="0" symbollevels="0" type="singleSymbol" enableorderby="0">
    <symbols>
      <symbol clip_to_extent="1" alpha="1" name="0" force_rhr="0" type="fill">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties" type="Map">
              <Option name="alpha" type="Map">
                <Option value="true" name="active" type="bool"/>
                <Option value="case&#xd;&#xa;when displayInCurrentTimeframeByFeatureStatus(&quot;Status&quot;) then 100.0&#xd;&#xa;else 0.0&#xd;&#xa;end" name="expression" type="QString"/>
                <Option value="3" name="type" type="int"/>
              </Option>
            </Option>
            <Option value="collection" name="type" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" pass="0" locked="0" class="SimpleFill">
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
    <rules key="{7f5ce27e-dedd-42a8-9736-4cba5de0ee6f}">
      <rule filter="&quot;Area (km²)&quot; > 1 and displayInCurrentTimeframeByFeatureStatus(&quot;Status&quot;)" key="{14aac2d3-b065-49f0-bf10-e8b98dc0c5c5}">
        <settings calloutType="simple">
          <text-style multilineHeight="1" fontFamily="Arial" textOpacity="1" allowHtml="0" fontLetterSpacing="0" fontSize="12" namedStyle="Bold" fontWordSpacing="0" blendMode="0" useSubstitutions="0" fontUnderline="0" textOrientation="horizontal" capitalization="0" textColor="0,0,0,255" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontWeight="75" previewBkgrdColor="0,251,0,255" legendString="Aa" fontItalic="0" fontKerning="1" isExpression="1" fontSizeUnit="Point" fieldName=" title(  &quot;Name&quot; ||  '\n' || round(  &quot;Area (km²)&quot;  ,1) || 'km²')" fontStrikeout="0">
            <families/>
            <text-buffer bufferJoinStyle="128" bufferBlendMode="0" bufferSize="0.29999999999999999" bufferSizeUnits="MM" bufferOpacity="1" bufferDraw="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferNoFill="1" bufferColor="255,255,255,255"/>
            <text-mask maskedSymbolLayers="" maskSizeUnits="MM" maskJoinStyle="128" maskOpacity="1" maskEnabled="0" maskType="0" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSize="0"/>
            <background shapeBlendMode="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiY="0" shapeRotation="0" shapeOpacity="1" shapeOffsetUnit="MM" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeOffsetX="0" shapeSizeUnit="MM" shapeSizeX="0" shapeBorderWidthUnit="MM" shapeSizeY="0" shapeRadiiX="0" shapeRadiiUnit="MM" shapeSizeType="0" shapeOffsetY="0" shapeJoinStyle="64" shapeRotationType="0" shapeBorderWidth="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderColor="128,128,128,255" shapeFillColor="255,255,255,255" shapeSVGFile="" shapeType="0">
              <symbol clip_to_extent="1" alpha="1" name="markerSymbol" force_rhr="0" type="marker">
                <data_defined_properties>
                  <Option type="Map">
                    <Option value="" name="name" type="QString"/>
                    <Option name="properties"/>
                    <Option value="collection" name="type" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" pass="0" locked="0" class="SimpleMarker">
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
              <symbol clip_to_extent="1" alpha="1" name="fillSymbol" force_rhr="0" type="fill">
                <data_defined_properties>
                  <Option type="Map">
                    <Option value="" name="name" type="QString"/>
                    <Option name="properties"/>
                    <Option value="collection" name="type" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" pass="0" locked="0" class="SimpleFill">
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
            <shadow shadowRadiusAlphaOnly="0" shadowScale="100" shadowOffsetDist="1" shadowOpacity="0.69999999999999996" shadowRadius="1.5" shadowUnder="0" shadowOffsetGlobal="1" shadowOffsetUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowRadiusUnit="MM" shadowColor="0,0,0,255" shadowBlendMode="6" shadowDraw="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0"/>
            <dd_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format decimals="3" plussign="0" placeDirectionSymbol="0" multilineAlign="1" reverseDirectionSymbol="0" leftDirectionSymbol="&lt;" autoWrapLength="9" addDirectionSymbol="0" formatNumbers="0" wrapChar="" useMaxLineLengthForAutoWrap="1" rightDirectionSymbol=">"/>
          <placement labelOffsetMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleOut="-25" geometryGenerator="" distUnits="MM" overrunDistance="0" distMapUnitScale="3x:0,0,0,0,0,0" priority="5" rotationAngle="0" preserveRotation="1" rotationUnit="AngleDegrees" lineAnchorPercent="0.5" lineAnchorClipping="0" layerType="PolygonGeometry" maxCurvedCharAngleIn="25" repeatDistance="0" offsetType="0" yOffset="0" geometryGeneratorType="PointGeometry" offsetUnits="MM" quadOffset="4" dist="0" centroidWhole="0" overrunDistanceUnit="MM" geometryGeneratorEnabled="0" fitInPolygonOnly="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" placement="1" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" xOffset="0" placementFlags="10" centroidInside="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" polygonPlacementFlags="2" repeatDistanceUnits="MM" lineAnchorType="0"/>
          <rendering fontLimitPixelSize="0" unplacedVisibility="0" maxNumLabels="2000" labelPerPart="0" scaleVisibility="0" drawLabels="1" obstacleType="0" fontMinPixelSize="3" minFeatureSize="0" scaleMax="0" mergeLines="0" fontMaxPixelSize="10000" scaleMin="0" obstacleFactor="1" upsidedownLabels="0" zIndex="0" limitNumLabels="0" displayAll="0" obstacle="1"/>
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
              <Option value="&lt;symbol clip_to_extent=&quot;1&quot; alpha=&quot;1&quot; name=&quot;symbol&quot; force_rhr=&quot;0&quot; type=&quot;line&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer enabled=&quot;1&quot; pass=&quot;0&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;0&quot; name=&quot;align_dash_pattern&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;square&quot; name=&quot;capstyle&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;5;2&quot; name=&quot;customdash&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;customdash_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;customdash_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;dash_pattern_offset&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;dash_pattern_offset_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;dash_pattern_offset_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;draw_inside_polygon&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;bevel&quot; name=&quot;joinstyle&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;60,60,60,255&quot; name=&quot;line_color&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;solid&quot; name=&quot;line_style&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0.3&quot; name=&quot;line_width&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;line_width_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;offset&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;offset_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;offset_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;ring_filter&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;trim_distance_end&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_end_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_end_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;trim_distance_start&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_start_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_start_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;tweak_dash_pattern_on_corners&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;use_custom_dash&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;width_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol" type="QString"/>
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
    <field configurationFlags="None" name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="Name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="Build Fence">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="Status">
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
    <field configurationFlags="None" name="Perimeter (km)">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="Area (km²)">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="Rounded Area (km²)">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="Rounded Perimeter (km)">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" name="" index="0"/>
    <alias field="Name" name="" index="1"/>
    <alias field="Build Fence" name="" index="2"/>
    <alias field="Status" name="" index="3"/>
    <alias field="Perimeter (km)" name="" index="4"/>
    <alias field="Area (km²)" name="" index="5"/>
    <alias field="Rounded Area (km²)" name="Area (km²)" index="6"/>
    <alias field="Rounded Perimeter (km)" name="Perimeter (km)" index="7"/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="Name" applyOnUpdate="0"/>
    <default expression="" field="Build Fence" applyOnUpdate="0"/>
    <default expression="Undefined" field="Status" applyOnUpdate="0"/>
    <default expression="" field="Perimeter (km)" applyOnUpdate="0"/>
    <default expression="" field="Area (km²)" applyOnUpdate="0"/>
    <default expression="" field="Rounded Area (km²)" applyOnUpdate="0"/>
    <default expression="" field="Rounded Perimeter (km)" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" constraints="0" field="fid" exp_strength="0" unique_strength="1"/>
    <constraint notnull_strength="0" constraints="0" field="Name" exp_strength="0" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Build Fence" exp_strength="0" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Status" exp_strength="0" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Perimeter (km)" exp_strength="0" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Area (km²)" exp_strength="0" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Rounded Area (km²)" exp_strength="0" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Rounded Perimeter (km)" exp_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="fid"/>
    <constraint desc="" exp="" field="Name"/>
    <constraint desc="" exp="" field="Build Fence"/>
    <constraint desc="" exp="" field="Status"/>
    <constraint desc="" exp="" field="Perimeter (km)"/>
    <constraint desc="" exp="" field="Area (km²)"/>
    <constraint desc="" exp="" field="Rounded Area (km²)"/>
    <constraint desc="" exp="" field="Rounded Perimeter (km)"/>
  </constraintExpressions>
  <expressionfields>
    <field expression="round(&quot;Area (km²)&quot;, 2)" precision="0" typeName="" subType="0" name="Rounded Area (km²)" length="0" type="6" comment=""/>
    <field expression="round(&quot;Perimeter (km)&quot;, 2)" precision="0" typeName="" subType="0" name="Rounded Perimeter (km)" length="0" type="6" comment=""/>
    <field expression="round(&quot;Perimeter (km)&quot;, 2)" precision="0" typeName="" subType="0" name="Rounded Perimeter (km)" length="0" type="6" comment=""/>
    <field expression="round(&quot;Area (km²)&quot;, 2)" precision="0" typeName="" subType="0" name="Rounded Area (km²)" length="0" type="6" comment=""/>
  </expressionfields>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="&quot;fid&quot;">
    <columns>
      <column hidden="0" name="fid" width="109" type="field"/>
      <column hidden="0" name="Name" width="232" type="field"/>
      <column hidden="0" name="Build Fence" width="144" type="field"/>
      <column hidden="0" name="Status" width="120" type="field"/>
      <column hidden="1" name="Perimeter (km)" width="-1" type="field"/>
      <column hidden="1" name="Area (km²)" width="-1" type="field"/>
      <column hidden="0" name="Rounded Perimeter (km)" width="187" type="field"/>
      <column hidden="0" name="Rounded Area (km²)" width="160" type="field"/>
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
    <field editable="0" name="Rounded Watered (km²)"/>
    <field editable="1" name="Status"/>
    <field editable="1" name="Timeframe"/>
    <field editable="1" name="Watered (km²)"/>
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
    <field name="Rounded Watered (km²)" labelOnTop="0"/>
    <field name="Status" labelOnTop="1"/>
    <field name="Timeframe" labelOnTop="0"/>
    <field name="Watered (km²)" labelOnTop="0"/>
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
    <field reuseLastValue="0" name="Rounded Watered (km²)"/>
    <field reuseLastValue="0" name="Status"/>
    <field reuseLastValue="0" name="Timeframe"/>
    <field reuseLastValue="0" name="Watered (km²)"/>
    <field reuseLastValue="0" name="fid"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"Name"</previewExpression>
  <layerGeometryType>2</layerGeometryType>
</qgis>
