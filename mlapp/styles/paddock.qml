<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" version="3.22.13-Białowieża" maxScale="0" hasScaleBasedVisibilityFlag="0" labelsEnabled="1" styleCategories="AllStyleCategories" simplifyDrawingTol="1" simplifyLocal="1" symbologyReferenceScale="-1" minScale="0" simplifyDrawingHints="1" simplifyMaxScale="1" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal durationUnit="min" startField="" fixedDuration="0" enabled="0" durationField="" mode="0" limitMode="0" startExpression="" endExpression="" accumulate="0" endField="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 forceraster="0" referencescale="-1" enableorderby="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" type="fill" name="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option type="Map" name="properties">
              <Option type="Map" name="alpha">
                <Option value="true" type="bool" name="active"/>
                <Option value="case&#xd;&#xa;when matchCurrentFeatureStatus(&quot;Status&quot;) then 100.0&#xd;&#xa;else 0.0&#xd;&#xa;end" type="QString" name="expression"/>
                <Option value="3" type="int" name="type"/>
              </Option>
            </Option>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" class="SimpleFill" enabled="1" pass="0">
          <Option type="Map">
            <Option value="3x:0,0,0,0,0,0" type="QString" name="border_width_map_unit_scale"/>
            <Option value="60,179,113,255" type="QString" name="color"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,178" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0.4" type="QString" name="outline_width"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="solid" type="QString" name="style"/>
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
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
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
      <rule key="{11e68d6d-61d9-4100-a265-56fc337e0dae}" filter="&quot;Area (km²)&quot; > 5 and matchCurrentFeatureStatus(&quot;Status&quot;)">
        <settings calloutType="simple">
          <text-style fieldName=" title(  &quot;Name&quot; ||  '\n' || round(  &quot;Area (km²)&quot;  ,1) || 'km²')" allowHtml="0" fontStrikeout="0" fontWeight="75" textColor="0,0,0,255" fontSizeUnit="Point" fontSize="12" fontSizeMapUnitScale="3x:0,0,0,0,0,0" legendString="Aa" fontWordSpacing="0" fontItalic="0" isExpression="1" useSubstitutions="0" blendMode="0" fontUnderline="0" previewBkgrdColor="0,251,0,255" textOpacity="1" fontFamily="Arial" namedStyle="Bold" fontLetterSpacing="0" textOrientation="horizontal" fontKerning="1" multilineHeight="1" capitalization="0">
            <families/>
            <text-buffer bufferSizeUnits="MM" bufferDraw="1" bufferOpacity="1" bufferJoinStyle="128" bufferNoFill="1" bufferBlendMode="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferColor="255,255,255,255" bufferSize="0.29999999999999999"/>
            <text-mask maskSizeUnits="MM" maskedSymbolLayers="" maskOpacity="1" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskEnabled="0" maskSize="0" maskType="0" maskJoinStyle="128"/>
            <background shapeRotationType="0" shapeBorderWidthUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0" shapeRadiiUnit="MM" shapeSizeX="0" shapeBlendMode="0" shapeRadiiY="0" shapeSizeUnit="MM" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeSizeY="0" shapeFillColor="255,255,255,255" shapeDraw="0" shapeOffsetY="0" shapeOffsetX="0" shapeRotation="0" shapeSizeType="0" shapeRadiiX="0" shapeOpacity="1" shapeBorderColor="128,128,128,255" shapeType="0" shapeSVGFile="" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM">
              <symbol alpha="1" clip_to_extent="1" force_rhr="0" type="marker" name="markerSymbol">
                <data_defined_properties>
                  <Option type="Map">
                    <Option value="" type="QString" name="name"/>
                    <Option name="properties"/>
                    <Option value="collection" type="QString" name="type"/>
                  </Option>
                </data_defined_properties>
                <layer locked="0" class="SimpleMarker" enabled="1" pass="0">
                  <Option type="Map">
                    <Option value="0" type="QString" name="angle"/>
                    <Option value="square" type="QString" name="cap_style"/>
                    <Option value="125,139,143,255" type="QString" name="color"/>
                    <Option value="1" type="QString" name="horizontal_anchor_point"/>
                    <Option value="bevel" type="QString" name="joinstyle"/>
                    <Option value="circle" type="QString" name="name"/>
                    <Option value="0,0" type="QString" name="offset"/>
                    <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
                    <Option value="MM" type="QString" name="offset_unit"/>
                    <Option value="35,35,35,255" type="QString" name="outline_color"/>
                    <Option value="solid" type="QString" name="outline_style"/>
                    <Option value="0" type="QString" name="outline_width"/>
                    <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
                    <Option value="MM" type="QString" name="outline_width_unit"/>
                    <Option value="diameter" type="QString" name="scale_method"/>
                    <Option value="2" type="QString" name="size"/>
                    <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
                    <Option value="MM" type="QString" name="size_unit"/>
                    <Option value="1" type="QString" name="vertical_anchor_point"/>
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
                      <Option value="" type="QString" name="name"/>
                      <Option name="properties"/>
                      <Option value="collection" type="QString" name="type"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
              <symbol alpha="1" clip_to_extent="1" force_rhr="0" type="fill" name="fillSymbol">
                <data_defined_properties>
                  <Option type="Map">
                    <Option value="" type="QString" name="name"/>
                    <Option name="properties"/>
                    <Option value="collection" type="QString" name="type"/>
                  </Option>
                </data_defined_properties>
                <layer locked="0" class="SimpleFill" enabled="1" pass="0">
                  <Option type="Map">
                    <Option value="3x:0,0,0,0,0,0" type="QString" name="border_width_map_unit_scale"/>
                    <Option value="255,255,255,255" type="QString" name="color"/>
                    <Option value="bevel" type="QString" name="joinstyle"/>
                    <Option value="0,0" type="QString" name="offset"/>
                    <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
                    <Option value="MM" type="QString" name="offset_unit"/>
                    <Option value="128,128,128,255" type="QString" name="outline_color"/>
                    <Option value="no" type="QString" name="outline_style"/>
                    <Option value="0" type="QString" name="outline_width"/>
                    <Option value="MM" type="QString" name="outline_width_unit"/>
                    <Option value="solid" type="QString" name="style"/>
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
                      <Option value="" type="QString" name="name"/>
                      <Option name="properties"/>
                      <Option value="collection" type="QString" name="type"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowUnder="0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowRadiusUnit="MM" shadowOpacity="0.69999999999999996" shadowRadiusAlphaOnly="0" shadowDraw="0" shadowOffsetGlobal="1" shadowColor="0,0,0,255" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadius="1.5" shadowScale="100" shadowOffsetUnit="MM" shadowBlendMode="6" shadowOffsetDist="1"/>
            <dd_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format rightDirectionSymbol=">" leftDirectionSymbol="&lt;" autoWrapLength="9" multilineAlign="1" addDirectionSymbol="0" placeDirectionSymbol="0" useMaxLineLengthForAutoWrap="1" reverseDirectionSymbol="0" wrapChar="" decimals="3" formatNumbers="0" plussign="0"/>
          <placement predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" preserveRotation="1" lineAnchorType="0" maxCurvedCharAngleOut="-25" rotationAngle="0" overrunDistanceUnit="MM" quadOffset="4" distUnits="MM" placementFlags="10" dist="0" centroidWhole="0" geometryGeneratorType="PointGeometry" centroidInside="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" rotationUnit="AngleDegrees" lineAnchorClipping="0" maxCurvedCharAngleIn="25" repeatDistance="0" lineAnchorPercent="0.5" distMapUnitScale="3x:0,0,0,0,0,0" placement="1" overrunDistance="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" layerType="PolygonGeometry" yOffset="0" priority="5" polygonPlacementFlags="2" repeatDistanceUnits="MM" geometryGeneratorEnabled="0" offsetType="0" geometryGenerator="" offsetUnits="MM" xOffset="0"/>
          <rendering labelPerPart="0" fontMinPixelSize="3" unplacedVisibility="0" obstacleFactor="1" drawLabels="1" scaleMax="0" displayAll="0" fontLimitPixelSize="0" maxNumLabels="2000" zIndex="0" limitNumLabels="0" upsidedownLabels="0" scaleVisibility="0" obstacleType="0" scaleMin="0" obstacle="1" minFeatureSize="0" mergeLines="0" fontMaxPixelSize="10000"/>
          <dd_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option value="pole_of_inaccessibility" type="QString" name="anchorPoint"/>
              <Option value="0" type="int" name="blendMode"/>
              <Option type="Map" name="ddProperties">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
              <Option value="false" type="bool" name="drawToAllParts"/>
              <Option value="0" type="QString" name="enabled"/>
              <Option value="point_on_exterior" type="QString" name="labelAnchorPoint"/>
              <Option value="&lt;symbol alpha=&quot;1&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; name=&quot;symbol&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer locked=&quot;0&quot; class=&quot;SimpleLine&quot; enabled=&quot;1&quot; pass=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;align_dash_pattern&quot;/>&lt;Option value=&quot;square&quot; type=&quot;QString&quot; name=&quot;capstyle&quot;/>&lt;Option value=&quot;5;2&quot; type=&quot;QString&quot; name=&quot;customdash&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;customdash_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;customdash_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;draw_inside_polygon&quot;/>&lt;Option value=&quot;bevel&quot; type=&quot;QString&quot; name=&quot;joinstyle&quot;/>&lt;Option value=&quot;60,60,60,255&quot; type=&quot;QString&quot; name=&quot;line_color&quot;/>&lt;Option value=&quot;solid&quot; type=&quot;QString&quot; name=&quot;line_style&quot;/>&lt;Option value=&quot;0.3&quot; type=&quot;QString&quot; name=&quot;line_width&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;line_width_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;offset&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;offset_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;offset_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;ring_filter&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;trim_distance_end&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;trim_distance_end_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;trim_distance_end_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;trim_distance_start&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;trim_distance_start_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;trim_distance_start_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;use_custom_dash&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;width_map_unit_scale&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString" name="lineSymbol"/>
              <Option value="0" type="double" name="minLength"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="minLengthMapUnitScale"/>
              <Option value="MM" type="QString" name="minLengthUnit"/>
              <Option value="0" type="double" name="offsetFromAnchor"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromAnchorMapUnitScale"/>
              <Option value="MM" type="QString" name="offsetFromAnchorUnit"/>
              <Option value="0" type="double" name="offsetFromLabel"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromLabelMapUnitScale"/>
              <Option value="MM" type="QString" name="offsetFromLabelUnit"/>
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
  <legend showLabelLegend="0" type="default-vector"/>
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
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="Drafted" type="QString" name="Drafted"/>
              </Option>
              <Option type="Map">
                <Option value="Planned" type="QString" name="Planned"/>
              </Option>
              <Option type="Map">
                <Option value="Built" type="QString" name="Built"/>
              </Option>
              <Option type="Map">
                <Option value="PlannedSuperseded" type="QString" name="Superseded (was Planned)"/>
              </Option>
              <Option type="Map">
                <Option value="BuiltSuperseded" type="QString" name="Superseded (was Built)"/>
              </Option>
              <Option type="Map">
                <Option value="Archived" type="QString" name="Archived"/>
              </Option>
              <Option type="Map">
                <Option value="Undefined" type="QString" name="Undefined"/>
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
    <alias field="fid" index="0" name=""/>
    <alias field="Name" index="1" name=""/>
    <alias field="Status" index="2" name=""/>
    <alias field="Area (km²)" index="3" name=""/>
    <alias field="Perimeter (km)" index="4" name=""/>
    <alias field="Build Fence" index="5" name=""/>
    <alias field="Rounded Area (km²)" index="6" name="Area (km²)"/>
    <alias field="Rounded Perimeter (km)" index="7" name="Perimeter (km)"/>
    <alias field="Rounded AE/km²" index="8" name="AE/km²"/>
    <alias field="Rounded AE" index="9" name="AE"/>
    <alias field="Rounded Potential AE/km²" index="10" name="Potential AE/km²"/>
    <alias field="Rounded Potential AE" index="11" name="Potential AE"/>
  </aliases>
  <defaults>
    <default field="fid" applyOnUpdate="0" expression=""/>
    <default field="Name" applyOnUpdate="0" expression=""/>
    <default field="Status" applyOnUpdate="0" expression="Undefined"/>
    <default field="Area (km²)" applyOnUpdate="0" expression=""/>
    <default field="Perimeter (km)" applyOnUpdate="0" expression=""/>
    <default field="Build Fence" applyOnUpdate="0" expression=""/>
    <default field="Rounded Area (km²)" applyOnUpdate="0" expression=""/>
    <default field="Rounded Perimeter (km)" applyOnUpdate="0" expression=""/>
    <default field="Rounded AE/km²" applyOnUpdate="0" expression=""/>
    <default field="Rounded AE" applyOnUpdate="0" expression=""/>
    <default field="Rounded Potential AE/km²" applyOnUpdate="0" expression=""/>
    <default field="Rounded Potential AE" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="fid" unique_strength="1" constraints="3" exp_strength="0" notnull_strength="1"/>
    <constraint field="Name" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Status" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Area (km²)" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Perimeter (km)" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Build Fence" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Rounded Area (km²)" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Rounded Perimeter (km)" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Rounded AE/km²" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Rounded AE" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Rounded Potential AE/km²" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Rounded Potential AE" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="Name" desc="" exp=""/>
    <constraint field="Status" desc="" exp=""/>
    <constraint field="Area (km²)" desc="" exp=""/>
    <constraint field="Perimeter (km)" desc="" exp=""/>
    <constraint field="Build Fence" desc="" exp=""/>
    <constraint field="Rounded Area (km²)" desc="" exp=""/>
    <constraint field="Rounded Perimeter (km)" desc="" exp=""/>
    <constraint field="Rounded AE/km²" desc="" exp=""/>
    <constraint field="Rounded AE" desc="" exp=""/>
    <constraint field="Rounded Potential AE/km²" desc="" exp=""/>
    <constraint field="Rounded Potential AE" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields>
    <field typeName="" length="0" expression="round(&quot;Area (km²)&quot;, 2)" precision="0" subType="0" comment="" name="Rounded Area (km²)" type="6"/>
    <field typeName="" length="0" expression="round(&quot;Perimeter (km)&quot;, 2)" precision="0" subType="0" comment="" name="Rounded Perimeter (km)" type="6"/>
    <field typeName="" length="0" expression="round(&quot;AE/km²&quot;, 1)" precision="0" subType="0" comment="" name="Rounded AE/km²" type="6"/>
    <field typeName="" length="0" expression="round(&quot;AE&quot;, 0)" precision="0" subType="0" comment="" name="Rounded AE" type="6"/>
    <field typeName="" length="0" expression="round(&quot;Potential AE/km²&quot;, 1)" precision="0" subType="0" comment="" name="Rounded Potential AE/km²" type="6"/>
    <field typeName="" length="0" expression="round(&quot;Potential AE&quot;, 0)" precision="0" subType="0" comment="" name="Rounded Potential AE" type="6"/>
    <field typeName="" length="0" expression="round(&quot;Area (km²)&quot;, 2)" precision="0" subType="0" comment="" name="Rounded Area (km²)" type="6"/>
    <field typeName="" length="0" expression="round(&quot;Perimeter (km)&quot;, 2)" precision="0" subType="0" comment="" name="Rounded Perimeter (km)" type="6"/>
  </expressionfields>
  <attributeactions/>
  <attributetableconfig sortExpression="&quot;fid&quot;" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column hidden="0" type="field" name="fid" width="-1"/>
      <column hidden="0" type="field" name="Status" width="-1"/>
      <column hidden="1" type="field" name="Area (km²)" width="-1"/>
      <column hidden="1" type="field" name="Perimeter (km)" width="-1"/>
      <column hidden="1" type="field" name="AE/km²" width="-1"/>
      <column hidden="0" type="field" name="Build Fence" width="-1"/>
      <column hidden="1" type="field" name="AE" width="-1"/>
      <column hidden="1" type="field" name="Potential AE" width="-1"/>
      <column hidden="0" type="field" name="Name" width="-1"/>
      <column hidden="0" type="field" name="Paddock" width="-1"/>
      <column hidden="1" type="field" name="Potential AE/km²" width="-1"/>
      <column hidden="0" type="field" name="Timeframe" width="-1"/>
      <column hidden="0" type="field" name="Rounded Area (km²)" width="-1"/>
      <column hidden="0" type="field" name="Rounded Perimeter (km)" width="-1"/>
      <column hidden="0" type="field" name="Rounded AE/km²" width="-1"/>
      <column hidden="0" type="field" name="Rounded AE" width="-1"/>
      <column hidden="0" type="field" name="Rounded Potential AE/km²" width="-1"/>
      <column hidden="0" type="field" name="Rounded Potential AE" width="-1"/>
      <column hidden="1" type="actions" width="-1"/>
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
    <field editable="1" name="Status"/>
    <field editable="1" name="Timeframe"/>
    <field editable="1" name="fid"/>
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
    <field labelOnTop="1" name="Status"/>
    <field labelOnTop="0" name="Timeframe"/>
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
    <field reuseLastValue="0" name="Status"/>
    <field reuseLastValue="0" name="Timeframe"/>
    <field reuseLastValue="0" name="fid"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"Name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
