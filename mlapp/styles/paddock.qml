<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingHints="1" simplifyMaxScale="1" readOnly="0" minScale="100000000" simplifyLocal="1" hasScaleBasedVisibilityFlag="0" maxScale="0" labelsEnabled="1" simplifyDrawingTol="1" simplifyAlgorithm="0" version="3.22.8-Białowieża" symbologyReferenceScale="-1" styleCategories="AllStyleCategories">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal accumulate="0" durationUnit="min" startExpression="" enabled="0" mode="0" limitMode="0" endExpression="" fixedDuration="0" durationField="" startField="" endField="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 forceraster="0" type="singleSymbol" referencescale="-1" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol force_rhr="0" type="fill" clip_to_extent="1" alpha="1" name="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <Option type="Map">
            <Option value="0" type="QString" name="align_dash_pattern"/>
            <Option value="square" type="QString" name="capstyle"/>
            <Option value="5;2" type="QString" name="customdash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="customdash_map_unit_scale"/>
            <Option value="MM" type="QString" name="customdash_unit"/>
            <Option value="0" type="QString" name="dash_pattern_offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="dash_pattern_offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="dash_pattern_offset_unit"/>
            <Option value="0" type="QString" name="draw_inside_polygon"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="0,0,0,255" type="QString" name="line_color"/>
            <Option value="solid" type="QString" name="line_style"/>
            <Option value="0.96" type="QString" name="line_width"/>
            <Option value="MM" type="QString" name="line_width_unit"/>
            <Option value="0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="0" type="QString" name="ring_filter"/>
            <Option value="0" type="QString" name="trim_distance_end"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_end_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_end_unit"/>
            <Option value="0" type="QString" name="trim_distance_start"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_start_map_unit_scale"/>
            <Option value="MM" type="QString" name="trim_distance_start_unit"/>
            <Option value="0" type="QString" name="tweak_dash_pattern_on_corners"/>
            <Option value="0" type="QString" name="use_custom_dash"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="width_map_unit_scale"/>
          </Option>
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="0,0,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.96"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="trim_distance_end" v="0"/>
          <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_end_unit" v="MM"/>
          <prop k="trim_distance_start" v="0"/>
          <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_start_unit" v="MM"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
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
    <rules key="{ae00e2e1-e43a-4b40-9242-a06fc53238ae}">
      <rule filter="  &quot;Paddock Area (km²)&quot;  > 5" key="{e67b7858-b3e6-4fb7-9252-fb87730a1e72}">
        <settings calloutType="simple">
          <text-style capitalization="0" fontItalic="0" fontStrikeout="0" multilineHeight="1" fontLetterSpacing="0" textOpacity="1" textOrientation="horizontal" fontUnderline="0" isExpression="1" fontWeight="75" legendString="Aa" fontKerning="1" allowHtml="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontWordSpacing="0" fontSize="12" namedStyle="Bold" fontSizeUnit="Point" fontFamily="MS Shell Dlg 2" blendMode="0" fieldName=" title(  &quot;Name&quot;  || ' PDK' ||  '\n' || round(  &quot;Paddock Area (km²)&quot;  ,1) || 'km²')" previewBkgrdColor="0,0,0,255" textColor="0,0,0,255" useSubstitutions="0">
            <families/>
            <text-buffer bufferJoinStyle="128" bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferNoFill="1" bufferBlendMode="0" bufferColor="255,255,255,255" bufferSize="0.5" bufferDraw="1" bufferOpacity="1"/>
            <text-mask maskEnabled="0" maskOpacity="1" maskSizeUnits="MM" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskedSymbolLayers="" maskSize="0" maskType="0" maskJoinStyle="128"/>
            <background shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeRadiiY="0" shapeBorderColor="128,128,128,255" shapeOffsetUnit="MM" shapeBorderWidth="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeSizeX="0" shapeSizeType="0" shapeRadiiUnit="MM" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeSVGFile="" shapeFillColor="255,255,255,255" shapeRadiiX="0" shapeOffsetY="0" shapeJoinStyle="64" shapeDraw="0" shapeOpacity="1" shapeRotation="0" shapeSizeUnit="MM" shapeOffsetX="0" shapeType="0" shapeRotationType="0">
              <symbol force_rhr="0" type="marker" clip_to_extent="1" alpha="1" name="markerSymbol">
                <data_defined_properties>
                  <Option type="Map">
                    <Option value="" type="QString" name="name"/>
                    <Option name="properties"/>
                    <Option value="collection" type="QString" name="type"/>
                  </Option>
                </data_defined_properties>
                <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
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
              <symbol force_rhr="0" type="fill" clip_to_extent="1" alpha="1" name="fillSymbol">
                <data_defined_properties>
                  <Option type="Map">
                    <Option value="" type="QString" name="name"/>
                    <Option name="properties"/>
                    <Option value="collection" type="QString" name="type"/>
                  </Option>
                </data_defined_properties>
                <layer pass="0" enabled="1" class="SimpleFill" locked="0">
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
            <shadow shadowBlendMode="6" shadowDraw="0" shadowOffsetAngle="135" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.69999999999999996" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetGlobal="1" shadowUnder="0" shadowRadiusAlphaOnly="0" shadowRadiusUnit="MM" shadowColor="0,0,0,255" shadowScale="100" shadowOffsetDist="1" shadowOffsetUnit="MM" shadowRadius="1.5"/>
            <dd_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format formatNumbers="0" plussign="0" autoWrapLength="9" useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" decimals="3" placeDirectionSymbol="0" leftDirectionSymbol="&lt;" multilineAlign="1" rightDirectionSymbol=">" wrapChar="" reverseDirectionSymbol="0"/>
          <placement geometryGeneratorType="PointGeometry" rotationUnit="AngleDegrees" rotationAngle="0" xOffset="0" placement="1" distMapUnitScale="3x:0,0,0,0,0,0" offsetType="0" polygonPlacementFlags="2" placementFlags="10" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" distUnits="MM" lineAnchorType="0" repeatDistanceUnits="MM" centroidInside="0" priority="5" quadOffset="4" geometryGeneratorEnabled="0" dist="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" yOffset="0" offsetUnits="MM" layerType="PolygonGeometry" preserveRotation="1" repeatDistance="0" overrunDistanceUnit="MM" geometryGenerator="" maxCurvedCharAngleOut="-25" overrunDistance="0" maxCurvedCharAngleIn="25" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" centroidWhole="0" fitInPolygonOnly="0" lineAnchorClipping="0" lineAnchorPercent="0.5"/>
          <rendering displayAll="0" obstacleFactor="1" zIndex="0" fontMinPixelSize="3" upsidedownLabels="0" mergeLines="0" obstacleType="0" fontLimitPixelSize="0" scaleMin="0" obstacle="1" drawLabels="1" labelPerPart="0" fontMaxPixelSize="10000" minFeatureSize="0" unplacedVisibility="0" limitNumLabels="0" scaleMax="0" maxNumLabels="2000" scaleVisibility="0"/>
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
              <Option value="&lt;symbol force_rhr=&quot;0&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot; alpha=&quot;1&quot; name=&quot;symbol&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer pass=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;align_dash_pattern&quot;/>&lt;Option value=&quot;square&quot; type=&quot;QString&quot; name=&quot;capstyle&quot;/>&lt;Option value=&quot;5;2&quot; type=&quot;QString&quot; name=&quot;customdash&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;customdash_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;customdash_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;dash_pattern_offset_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;draw_inside_polygon&quot;/>&lt;Option value=&quot;bevel&quot; type=&quot;QString&quot; name=&quot;joinstyle&quot;/>&lt;Option value=&quot;60,60,60,255&quot; type=&quot;QString&quot; name=&quot;line_color&quot;/>&lt;Option value=&quot;solid&quot; type=&quot;QString&quot; name=&quot;line_style&quot;/>&lt;Option value=&quot;0.3&quot; type=&quot;QString&quot; name=&quot;line_width&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;line_width_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;offset&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;offset_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;offset_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;ring_filter&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;trim_distance_end&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;trim_distance_end_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;trim_distance_end_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;trim_distance_start&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;trim_distance_start_map_unit_scale&quot;/>&lt;Option value=&quot;MM&quot; type=&quot;QString&quot; name=&quot;trim_distance_start_unit&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;Option value=&quot;0&quot; type=&quot;QString&quot; name=&quot;use_custom_dash&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot; name=&quot;width_map_unit_scale&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString" name="lineSymbol"/>
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
    <Option type="Map">
      <Option type="List" name="dualview/previewExpressions">
        <Option value="NAME" type="QString"/>
      </Option>
      <Option value="0" type="QString" name="embeddedWidgets/count"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory width="15" lineSizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" sizeType="MM" direction="1" minimumSize="0" showAxis="0" enabled="0" spacing="0" scaleDependency="Area" penAlpha="255" opacity="1" spacingUnitScale="3x:0,0,0,0,0,0" sizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" penWidth="0" barWidth="5" diagramOrientation="Up" minScaleDenominator="0" spacingUnit="MM" scaleBasedVisibility="0" backgroundAlpha="255" backgroundColor="#ffffff" penColor="#000000" height="15" rotationOffset="270" maxScaleDenominator="1e+08">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
      <axisSymbol>
        <symbol force_rhr="0" type="line" clip_to_extent="1" alpha="1" name="">
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <layer pass="0" enabled="1" class="SimpleLine" locked="0">
            <Option type="Map">
              <Option value="0" type="QString" name="align_dash_pattern"/>
              <Option value="square" type="QString" name="capstyle"/>
              <Option value="5;2" type="QString" name="customdash"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="customdash_map_unit_scale"/>
              <Option value="MM" type="QString" name="customdash_unit"/>
              <Option value="0" type="QString" name="dash_pattern_offset"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="dash_pattern_offset_map_unit_scale"/>
              <Option value="MM" type="QString" name="dash_pattern_offset_unit"/>
              <Option value="0" type="QString" name="draw_inside_polygon"/>
              <Option value="bevel" type="QString" name="joinstyle"/>
              <Option value="35,35,35,255" type="QString" name="line_color"/>
              <Option value="solid" type="QString" name="line_style"/>
              <Option value="0.26" type="QString" name="line_width"/>
              <Option value="MM" type="QString" name="line_width_unit"/>
              <Option value="0" type="QString" name="offset"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
              <Option value="MM" type="QString" name="offset_unit"/>
              <Option value="0" type="QString" name="ring_filter"/>
              <Option value="0" type="QString" name="trim_distance_end"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_end_map_unit_scale"/>
              <Option value="MM" type="QString" name="trim_distance_end_unit"/>
              <Option value="0" type="QString" name="trim_distance_start"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="trim_distance_start_map_unit_scale"/>
              <Option value="MM" type="QString" name="trim_distance_start_unit"/>
              <Option value="0" type="QString" name="tweak_dash_pattern_on_corners"/>
              <Option value="0" type="QString" name="use_custom_dash"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="width_map_unit_scale"/>
            </Option>
            <prop k="align_dash_pattern" v="0"/>
            <prop k="capstyle" v="square"/>
            <prop k="customdash" v="5;2"/>
            <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="customdash_unit" v="MM"/>
            <prop k="dash_pattern_offset" v="0"/>
            <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="dash_pattern_offset_unit" v="MM"/>
            <prop k="draw_inside_polygon" v="0"/>
            <prop k="joinstyle" v="bevel"/>
            <prop k="line_color" v="35,35,35,255"/>
            <prop k="line_style" v="solid"/>
            <prop k="line_width" v="0.26"/>
            <prop k="line_width_unit" v="MM"/>
            <prop k="offset" v="0"/>
            <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="offset_unit" v="MM"/>
            <prop k="ring_filter" v="0"/>
            <prop k="trim_distance_end" v="0"/>
            <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="trim_distance_end_unit" v="MM"/>
            <prop k="trim_distance_start" v="0"/>
            <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="trim_distance_start_unit" v="MM"/>
            <prop k="tweak_dash_pattern_on_corners" v="0"/>
            <prop k="use_custom_dash" v="0"/>
            <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" obstacle="0" placement="1" priority="0" linePlacementFlags="18" dist="0" showAll="1">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option type="Map" name="QgsGeometryGapCheck">
        <Option value="0" type="double" name="allowedGapsBuffer"/>
        <Option value="false" type="bool" name="allowedGapsEnabled"/>
        <Option value="" type="QString" name="allowedGapsLayer"/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <legend type="default-vector" showLabelLegend="0"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field configurationFlags="None" name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="Name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="Status">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="Proposed" type="QString" name="Proposed"/>
              </Option>
              <Option type="Map">
                <Option value="Active" type="QString" name="Active"/>
              </Option>
              <Option type="Map">
                <Option value="Inactive" type="QString" name="Inactive"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="Area (km²)">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="Perimeter (km)">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <defaults>
    <default applyOnUpdate="0" expression="" field="fid"/>
    <default applyOnUpdate="0" expression="" field="Name"/>
    <default applyOnUpdate="0" expression="" field="Paddock Status"/>
    <default applyOnUpdate="1" expression="round($area * 0.000001, 2)" field="Paddock Area (km²)"/>
    <default applyOnUpdate="1" expression=" round($perimeter / 1000, 2)" field="Paddock Perimeter (km)"/>
    <default applyOnUpdate="0" expression="" field="Paddock Date Commisioned"/>
    <default applyOnUpdate="0" expression="" field="Paddock Date Decommisioned"/>
    <default applyOnUpdate="1" expression="to_date(now())" field="Date Edited"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" constraints="3" field="fid" unique_strength="1" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Name" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Paddock Status" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Paddock Area (km²)" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Paddock Perimeter (km)" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Paddock Date Commisioned" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Paddock Date Decommisioned" unique_strength="0" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" field="Date Edited" unique_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="fid" desc=""/>
    <constraint exp="" field="Name" desc=""/>
    <constraint exp="" field="Paddock Status" desc=""/>
    <constraint exp="" field="Paddock Area (km²)" desc=""/>
    <constraint exp="" field="Paddock Perimeter (km)" desc=""/>
    <constraint exp="" field="Paddock Date Commisioned" desc=""/>
    <constraint exp="" field="Paddock Date Decommisioned" desc=""/>
    <constraint exp="" field="Date Edited" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="&quot;fid&quot;">
    <columns>
      <column width="-1" type="actions" hidden="1"/>
      <column width="-1" type="field" hidden="0" name="fid"/>
      <column width="-1" type="field" hidden="0" name="Name"/>
      <column width="114" type="field" hidden="0" name="Paddock Area (km²)"/>
      <column width="140" type="field" hidden="0" name="Paddock Perimeter (km)"/>
      <column width="-1" type="field" hidden="0" name="Date Edited"/>
      <column width="-1" type="field" hidden="0" name="Paddock Status"/>
      <column width="-1" type="field" hidden="0" name="Paddock Date Commisioned"/>
      <column width="-1" type="field" hidden="0" name="Paddock Date Decommisioned"/>
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
  <attributeEditorForm>
    <attributeEditorField index="1" showLabel="1" name="Name"/>
    <attributeEditorField index="3" showLabel="1" name="Paddock Area (km²)"/>
    <attributeEditorField index="4" showLabel="1" name="Paddock Perimeter (km)"/>
    <attributeEditorField index="-1" showLabel="1" name="Date Commisioned"/>
    <attributeEditorField index="-1" showLabel="1" name="Date Decommisioned"/>
    <attributeEditorField index="-1" showLabel="1" name="Paddock Active?"/>
    <attributeEditorField index="-1" showLabel="1" name="Paddock Proposed?"/>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="2KM_WAREA"/>
    <field editable="1" name="3KM_WAREA"/>
    <field editable="1" name="5KM_WA"/>
    <field editable="1" name="8KM_WA"/>
    <field editable="0" name="Current 2km Watered Areas_CURR_WAREAKM2"/>
    <field editable="0" name="Current 2km Watered Areas_PDK_ACTIVE"/>
    <field editable="0" name="Current 2km Watered Areas_PDK_AREAKM"/>
    <field editable="0" name="Current 2km Watered Areas_PDK_COMMISIONED"/>
    <field editable="0" name="Current 2km Watered Areas_PDK_DECOMMISIONED"/>
    <field editable="0" name="Current 2km Watered Areas_PDK_PERMIM_KM"/>
    <field editable="0" name="Current 2km Watered Areas_PDK_PROPOSED"/>
    <field editable="0" name="Current 2km Watered Areas_WA_DISTKM"/>
    <field editable="0" name="Current 2km Watered Areas_fid"/>
    <field editable="0" name="Current Watered Areas_CURR_WAREAKM2"/>
    <field editable="0" name="Current Watered Areas_PDK_ACTIVE"/>
    <field editable="0" name="Current Watered Areas_PDK_AREAKM"/>
    <field editable="0" name="Current Watered Areas_PDK_COMMISIONED"/>
    <field editable="0" name="Current Watered Areas_PDK_DECOMMISIONED"/>
    <field editable="0" name="Current Watered Areas_PDK_PERMIM_KM"/>
    <field editable="0" name="Current Watered Areas_PDK_PROPOSED"/>
    <field editable="0" name="Current Watered Areas_WA_DISTKM"/>
    <field editable="0" name="Current Watered Areas_fid"/>
    <field editable="1" name="Date Commisioned"/>
    <field editable="1" name="Date Decommisioned"/>
    <field editable="1" name="Date Edited"/>
    <field editable="1" name="GM_LAYER"/>
    <field editable="1" name="GM_TYPE"/>
    <field editable="1" name="LAYER"/>
    <field editable="0" name="Mathison Current Watered Areas_CURR_WAREAKM2"/>
    <field editable="0" name="Mathison Current Watered Areas_PDK_ACTIVE"/>
    <field editable="0" name="Mathison Current Watered Areas_PDK_AREAKM"/>
    <field editable="0" name="Mathison Current Watered Areas_PDK_COMMISIONED"/>
    <field editable="0" name="Mathison Current Watered Areas_PDK_DECOMMISIONED"/>
    <field editable="0" name="Mathison Current Watered Areas_PDK_PERMIM_KM"/>
    <field editable="0" name="Mathison Current Watered Areas_PDK_PROPOSED"/>
    <field editable="0" name="Mathison Current Watered Areas_WA_DISTKM"/>
    <field editable="0" name="Mathison Current Watered Areas_fid"/>
    <field editable="1" name="NAME"/>
    <field editable="1" name="PDK_ACTIVE"/>
    <field editable="1" name="PDK_AREAKM"/>
    <field editable="1" name="PDK_COMMISIONED"/>
    <field editable="1" name="PDK_DECOMMISIONED"/>
    <field editable="1" name="PDK_NAME"/>
    <field editable="1" name="PDK_PERMIM_KM"/>
    <field editable="1" name="PDK_PROPOSED"/>
    <field editable="1" name="PROPERTY"/>
    <field editable="1" name="Paddock Active?"/>
    <field editable="1" name="Paddock Area (km²)"/>
    <field editable="1" name="Paddock Date Commisioned"/>
    <field editable="1" name="Paddock Date Decommisioned"/>
    <field editable="1" name="Name"/>
    <field editable="1" name="Paddock Perimeter (km)"/>
    <field editable="1" name="Paddock Proposed?"/>
    <field editable="1" name="Paddock Status"/>
    <field editable="1" name="Status"/>
    <field editable="1" name="areakm2"/>
    <field editable="1" name="fid"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="2KM_WAREA"/>
    <field labelOnTop="0" name="3KM_WAREA"/>
    <field labelOnTop="0" name="5KM_WA"/>
    <field labelOnTop="0" name="8KM_WA"/>
    <field labelOnTop="0" name="Current 2km Watered Areas_CURR_WAREAKM2"/>
    <field labelOnTop="0" name="Current 2km Watered Areas_PDK_ACTIVE"/>
    <field labelOnTop="0" name="Current 2km Watered Areas_PDK_AREAKM"/>
    <field labelOnTop="0" name="Current 2km Watered Areas_PDK_COMMISIONED"/>
    <field labelOnTop="0" name="Current 2km Watered Areas_PDK_DECOMMISIONED"/>
    <field labelOnTop="0" name="Current 2km Watered Areas_PDK_PERMIM_KM"/>
    <field labelOnTop="0" name="Current 2km Watered Areas_PDK_PROPOSED"/>
    <field labelOnTop="0" name="Current 2km Watered Areas_WA_DISTKM"/>
    <field labelOnTop="0" name="Current 2km Watered Areas_fid"/>
    <field labelOnTop="0" name="Current Watered Areas_CURR_WAREAKM2"/>
    <field labelOnTop="0" name="Current Watered Areas_PDK_ACTIVE"/>
    <field labelOnTop="0" name="Current Watered Areas_PDK_AREAKM"/>
    <field labelOnTop="0" name="Current Watered Areas_PDK_COMMISIONED"/>
    <field labelOnTop="0" name="Current Watered Areas_PDK_DECOMMISIONED"/>
    <field labelOnTop="0" name="Current Watered Areas_PDK_PERMIM_KM"/>
    <field labelOnTop="0" name="Current Watered Areas_PDK_PROPOSED"/>
    <field labelOnTop="0" name="Current Watered Areas_WA_DISTKM"/>
    <field labelOnTop="0" name="Current Watered Areas_fid"/>
    <field labelOnTop="1" name="Date Commisioned"/>
    <field labelOnTop="1" name="Date Decommisioned"/>
    <field labelOnTop="1" name="Date Edited"/>
    <field labelOnTop="0" name="GM_LAYER"/>
    <field labelOnTop="0" name="GM_TYPE"/>
    <field labelOnTop="0" name="LAYER"/>
    <field labelOnTop="0" name="Mathison Current Watered Areas_CURR_WAREAKM2"/>
    <field labelOnTop="0" name="Mathison Current Watered Areas_PDK_ACTIVE"/>
    <field labelOnTop="0" name="Mathison Current Watered Areas_PDK_AREAKM"/>
    <field labelOnTop="0" name="Mathison Current Watered Areas_PDK_COMMISIONED"/>
    <field labelOnTop="0" name="Mathison Current Watered Areas_PDK_DECOMMISIONED"/>
    <field labelOnTop="0" name="Mathison Current Watered Areas_PDK_PERMIM_KM"/>
    <field labelOnTop="0" name="Mathison Current Watered Areas_PDK_PROPOSED"/>
    <field labelOnTop="0" name="Mathison Current Watered Areas_WA_DISTKM"/>
    <field labelOnTop="0" name="Mathison Current Watered Areas_fid"/>
    <field labelOnTop="0" name="NAME"/>
    <field labelOnTop="0" name="PDK_ACTIVE"/>
    <field labelOnTop="0" name="PDK_AREAKM"/>
    <field labelOnTop="0" name="PDK_COMMISIONED"/>
    <field labelOnTop="0" name="PDK_DECOMMISIONED"/>
    <field labelOnTop="0" name="PDK_NAME"/>
    <field labelOnTop="0" name="PDK_PERMIM_KM"/>
    <field labelOnTop="0" name="PDK_PROPOSED"/>
    <field labelOnTop="0" name="PROPERTY"/>
    <field labelOnTop="1" name="Paddock Active?"/>
    <field labelOnTop="1" name="Paddock Area (km²)"/>
    <field labelOnTop="1" name="Paddock Date Commisioned"/>
    <field labelOnTop="1" name="Paddock Date Decommisioned"/>
    <field labelOnTop="1" name="Name"/>
    <field labelOnTop="1" name="Paddock Perimeter (km)"/>
    <field labelOnTop="1" name="Paddock Proposed?"/>
    <field labelOnTop="1" name="Paddock Status"/>
    <field labelOnTop="1" name="Status"/>
    <field labelOnTop="0" name="areakm2"/>
    <field labelOnTop="0" name="fid"/>
  </labelOnTop>
  <reuseLastValue/>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>NAME</previewExpression>
  <mapTip>&lt;center>[%  title("PDK_NAME") || ' Paddock' %]&lt;br>&#xd;
[%  round("PDK_AREAKM" ,2)%]km²&lt;/center></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
