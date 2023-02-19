<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" readOnly="0" version="3.22.14-Białowieża" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms|AttributeTable">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 enableorderby="0" type="categorizedSymbol" referencescale="-1" symbollevels="0" attr="ifCurrentFeatureStatus(&quot;Status&quot;, &quot;Waterpoint Type&quot;, 'Ignore')" forceraster="0">
    <categories>
      <category value="Bore" label="Bore" symbol="0" render="true"/>
      <category value="Dam" label="Dam" symbol="1" render="true"/>
      <category value="Trough" label="Trough" symbol="2" render="true"/>
      <category value="Turkey Nest" label="Turkey Nest" symbol="3" render="true"/>
      <category value="Water Tank" label="Water Tank" symbol="4" render="true"/>
      <category value="Waterhole" label="Waterhole" symbol="5" render="true"/>
    </categories>
    <symbols>
      <symbol name="0" type="marker" clip_to_extent="1" force_rhr="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="cap_style" type="QString" value="square"/>
            <Option name="color" type="QString" value="9,211,251,255"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="name" type="QString" value="circle"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="35,35,35,0"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="scale_method" type="QString" value="diameter"/>
            <Option name="size" type="QString" value="5"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="MM"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="square" k="cap_style"/>
          <prop v="9,211,251,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,0" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="5" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointColour(featureStatusToTimeframe(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="FontMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="chr" type="QString" value="B"/>
            <Option name="color" type="QString" value="0,0,0,255"/>
            <Option name="font" type="QString" value="Calibri"/>
            <Option name="font_style" type="QString" value="Bold"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,-1.59999999999999987"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="Point"/>
            <Option name="outline_color" type="QString" value="0,0,0,255"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="Point"/>
            <Option name="size" type="QString" value="8"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="Point"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="B" k="chr"/>
          <prop v="0,0,0,255" k="color"/>
          <prop v="Calibri" k="font"/>
          <prop v="Bold" k="font_style"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,-1.59999999999999987" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="Point" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="Point" k="outline_width_unit"/>
          <prop v="8" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="Point" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="char" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="waterpointInitials(&quot;Waterpoint Type&quot;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" type="marker" clip_to_extent="1" force_rhr="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="cap_style" type="QString" value="square"/>
            <Option name="color" type="QString" value="9,211,251,255"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="name" type="QString" value="circle"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="35,35,35,0"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="scale_method" type="QString" value="diameter"/>
            <Option name="size" type="QString" value="5"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="MM"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="square" k="cap_style"/>
          <prop v="9,211,251,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,0" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="5" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointColour(featureStatusToTimeframe(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="FontMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="chr" type="QString" value="D"/>
            <Option name="color" type="QString" value="0,0,0,255"/>
            <Option name="font" type="QString" value="Calibri"/>
            <Option name="font_style" type="QString" value="Bold"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,-1.59999999999999987"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="Point"/>
            <Option name="outline_color" type="QString" value="0,0,0,255"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="Point"/>
            <Option name="size" type="QString" value="8"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="Point"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="D" k="chr"/>
          <prop v="0,0,0,255" k="color"/>
          <prop v="Calibri" k="font"/>
          <prop v="Bold" k="font_style"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,-1.59999999999999987" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="Point" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="Point" k="outline_width_unit"/>
          <prop v="8" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="Point" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="char" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="waterpointInitials(&quot;Waterpoint Type&quot;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="2" type="marker" clip_to_extent="1" force_rhr="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="cap_style" type="QString" value="square"/>
            <Option name="color" type="QString" value="9,211,251,255"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="name" type="QString" value="circle"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="35,35,35,0"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="scale_method" type="QString" value="diameter"/>
            <Option name="size" type="QString" value="5"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="MM"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="square" k="cap_style"/>
          <prop v="9,211,251,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,0" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="5" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointColour(featureStatusToTimeframe(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="FontMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="chr" type="QString" value="T"/>
            <Option name="color" type="QString" value="0,0,0,255"/>
            <Option name="font" type="QString" value="Calibri"/>
            <Option name="font_style" type="QString" value="Bold"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,-1.59999999999999987"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="Point"/>
            <Option name="outline_color" type="QString" value="0,0,0,255"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="Point"/>
            <Option name="size" type="QString" value="8"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="Point"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="T" k="chr"/>
          <prop v="0,0,0,255" k="color"/>
          <prop v="Calibri" k="font"/>
          <prop v="Bold" k="font_style"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,-1.59999999999999987" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="Point" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="Point" k="outline_width_unit"/>
          <prop v="8" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="Point" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="char" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="waterpointInitials(&quot;Waterpoint Type&quot;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="3" type="marker" clip_to_extent="1" force_rhr="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="cap_style" type="QString" value="square"/>
            <Option name="color" type="QString" value="9,211,251,255"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="name" type="QString" value="circle"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="35,35,35,0"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="scale_method" type="QString" value="diameter"/>
            <Option name="size" type="QString" value="5"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="MM"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="square" k="cap_style"/>
          <prop v="9,211,251,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,0" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="5" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointColour(featureStatusToTimeframe(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="FontMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="chr" type="QString" value="TN"/>
            <Option name="color" type="QString" value="0,0,0,255"/>
            <Option name="font" type="QString" value="Calibri"/>
            <Option name="font_style" type="QString" value="Bold"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,-1.59999999999999987"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="Point"/>
            <Option name="outline_color" type="QString" value="0,0,0,255"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="Point"/>
            <Option name="size" type="QString" value="8"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="Point"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="TN" k="chr"/>
          <prop v="0,0,0,255" k="color"/>
          <prop v="Calibri" k="font"/>
          <prop v="Bold" k="font_style"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,-1.59999999999999987" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="Point" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="Point" k="outline_width_unit"/>
          <prop v="8" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="Point" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="char" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="waterpointInitials(&quot;Waterpoint Type&quot;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="4" type="marker" clip_to_extent="1" force_rhr="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="cap_style" type="QString" value="square"/>
            <Option name="color" type="QString" value="9,211,251,255"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="name" type="QString" value="circle"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="35,35,35,0"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="scale_method" type="QString" value="diameter"/>
            <Option name="size" type="QString" value="5"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="MM"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="square" k="cap_style"/>
          <prop v="9,211,251,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,0" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="5" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointColour(featureStatusToTimeframe(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="FontMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="chr" type="QString" value="WT"/>
            <Option name="color" type="QString" value="0,0,0,255"/>
            <Option name="font" type="QString" value="Calibri"/>
            <Option name="font_style" type="QString" value="Bold"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,-1.59999999999999987"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="Point"/>
            <Option name="outline_color" type="QString" value="0,0,0,255"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="Point"/>
            <Option name="size" type="QString" value="8"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="Point"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="WT" k="chr"/>
          <prop v="0,0,0,255" k="color"/>
          <prop v="Calibri" k="font"/>
          <prop v="Bold" k="font_style"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,-1.59999999999999987" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="Point" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="Point" k="outline_width_unit"/>
          <prop v="8" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="Point" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="char" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="waterpointInitials(&quot;Waterpoint Type&quot;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="5" type="marker" clip_to_extent="1" force_rhr="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="cap_style" type="QString" value="square"/>
            <Option name="color" type="QString" value="9,211,251,255"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="name" type="QString" value="circle"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="35,35,35,0"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="scale_method" type="QString" value="diameter"/>
            <Option name="size" type="QString" value="5"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="MM"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="square" k="cap_style"/>
          <prop v="9,211,251,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,0" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="5" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointColour(featureStatusToTimeframe(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="FontMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="chr" type="QString" value="WH"/>
            <Option name="color" type="QString" value="0,0,0,255"/>
            <Option name="font" type="QString" value="Calibri"/>
            <Option name="font_style" type="QString" value="Bold"/>
            <Option name="horizontal_anchor_point" type="QString" value="1"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,-1.59999999999999987"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="Point"/>
            <Option name="outline_color" type="QString" value="0,0,0,255"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="outline_width_unit" type="QString" value="Point"/>
            <Option name="size" type="QString" value="8"/>
            <Option name="size_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="size_unit" type="QString" value="Point"/>
            <Option name="vertical_anchor_point" type="QString" value="1"/>
          </Option>
          <prop v="0" k="angle"/>
          <prop v="WH" k="chr"/>
          <prop v="0,0,0,255" k="color"/>
          <prop v="Calibri" k="font"/>
          <prop v="Bold" k="font_style"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,-1.59999999999999987" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="Point" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="Point" k="outline_width_unit"/>
          <prop v="8" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="Point" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="char" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="waterpointInitials(&quot;Waterpoint Type&quot;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="fillColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="timeframeToWaterpointForegroundColour(featureStatusToTimeFrame(&quot;Status&quot;))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol name="0" type="marker" clip_to_extent="1" force_rhr="0" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" type="QString" value="0"/>
            <Option name="cap_style" type="QString" value="square"/>
            <Option name="color" type="QString" value="255,158,23,255"/>
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
          <prop v="255,158,23,255" k="color"/>
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
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
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
    <field name="Name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Waterpoint Type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Bore" type="QString" value="Bore"/>
              </Option>
              <Option type="Map">
                <Option name="Dam" type="QString" value="Dam"/>
              </Option>
              <Option type="Map">
                <Option name="Trough" type="QString" value="Trough"/>
              </Option>
              <Option type="Map">
                <Option name="Turkey Nest" type="QString" value="TurkeyNest"/>
              </Option>
              <Option type="Map">
                <Option name="Water Tank" type="QString" value="WaterTank"/>
              </Option>
              <Option type="Map">
                <Option name="Waterhole" type="QString" value="Waterhole"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="Near Grazing Radius (m)" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Far Grazing Radius (m)" configurationFlags="None">
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
    <field name="Longitude" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Latitude" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Elevation (m)" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Longitude" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Latitude" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Elevation (m)" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Near Grazing Radius (m)" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Far Grazing Radius (m)" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="fid" name=""/>
    <alias index="1" field="Name" name=""/>
    <alias index="2" field="Waterpoint Type" name=""/>
    <alias index="3" field="Near Grazing Radius (m)" name=""/>
    <alias index="4" field="Far Grazing Radius (m)" name=""/>
    <alias index="5" field="Status" name=""/>
    <alias index="6" field="Longitude" name=""/>
    <alias index="7" field="Latitude" name=""/>
    <alias index="8" field="Elevation (m)" name=""/>
    <alias index="9" field="Rounded Longitude" name="Longitude"/>
    <alias index="10" field="Rounded Latitude" name="Latitude"/>
    <alias index="11" field="Rounded Elevation (m)" name="Elevation (m)"/>
    <alias index="12" field="Rounded Near Grazing Radius (m)" name="Near Grazing Radius (m)"/>
    <alias index="13" field="Rounded Far Grazing Radius (m)" name="Far Grazing Radius (m)"/>
  </aliases>
  <defaults>
    <default field="fid" applyOnUpdate="0" expression=""/>
    <default field="Name" applyOnUpdate="0" expression=""/>
    <default field="Waterpoint Type" applyOnUpdate="0" expression="'Trough'"/>
    <default field="Near Grazing Radius (m)" applyOnUpdate="0" expression="3000.0"/>
    <default field="Far Grazing Radius (m)" applyOnUpdate="0" expression="5000.0"/>
    <default field="Status" applyOnUpdate="0" expression="Undefined"/>
    <default field="Longitude" applyOnUpdate="0" expression="nan"/>
    <default field="Latitude" applyOnUpdate="0" expression="nan"/>
    <default field="Elevation (m)" applyOnUpdate="0" expression="nan"/>
    <default field="Rounded Longitude" applyOnUpdate="0" expression=""/>
    <default field="Rounded Latitude" applyOnUpdate="0" expression=""/>
    <default field="Rounded Elevation (m)" applyOnUpdate="0" expression=""/>
    <default field="Rounded Near Grazing Radius (m)" applyOnUpdate="0" expression=""/>
    <default field="Rounded Far Grazing Radius (m)" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="fid" unique_strength="1" notnull_strength="1" constraints="3" exp_strength="0"/>
    <constraint field="Name" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Waterpoint Type" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Near Grazing Radius (m)" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Far Grazing Radius (m)" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Status" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Longitude" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Latitude" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Elevation (m)" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Rounded Longitude" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Rounded Latitude" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Rounded Elevation (m)" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Rounded Near Grazing Radius (m)" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Rounded Far Grazing Radius (m)" unique_strength="0" notnull_strength="0" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="fid" desc=""/>
    <constraint exp="" field="Name" desc=""/>
    <constraint exp="" field="Waterpoint Type" desc=""/>
    <constraint exp="" field="Near Grazing Radius (m)" desc=""/>
    <constraint exp="" field="Far Grazing Radius (m)" desc=""/>
    <constraint exp="" field="Status" desc=""/>
    <constraint exp="" field="Longitude" desc=""/>
    <constraint exp="" field="Latitude" desc=""/>
    <constraint exp="" field="Elevation (m)" desc=""/>
    <constraint exp="" field="Rounded Longitude" desc=""/>
    <constraint exp="" field="Rounded Latitude" desc=""/>
    <constraint exp="" field="Rounded Elevation (m)" desc=""/>
    <constraint exp="" field="Rounded Near Grazing Radius (m)" desc=""/>
    <constraint exp="" field="Rounded Far Grazing Radius (m)" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field name="Rounded Longitude" type="6" subType="0" typeName="" comment="" expression="round(&quot;Longitude&quot;, 2)" precision="0" length="0"/>
    <field name="Rounded Latitude" type="6" subType="0" typeName="" comment="" expression="round(&quot;Latitude&quot;, 2)" precision="0" length="0"/>
    <field name="Rounded Elevation (m)" type="6" subType="0" typeName="" comment="" expression="round(&quot;Elevation (m)&quot;, 1)" precision="0" length="0"/>
    <field name="Rounded Near Grazing Radius (m)" type="6" subType="0" typeName="" comment="" expression="round(&quot;Near Grazing Radius (m)&quot;, 0)" precision="0" length="0"/>
    <field name="Rounded Far Grazing Radius (m)" type="6" subType="0" typeName="" comment="" expression="round(&quot;Far Grazing Radius (m)&quot;, 0)" precision="0" length="0"/>
    <field name="Rounded Near Grazing Radius (m)" type="6" subType="0" typeName="" comment="" expression="round(&quot;Near Grazing Radius (m)&quot;, 0)" precision="0" length="0"/>
    <field name="Rounded Far Grazing Radius (m)" type="6" subType="0" typeName="" comment="" expression="round(&quot;Far Grazing Radius (m)&quot;, 0)" precision="0" length="0"/>
    <field name="Rounded Longitude" type="6" subType="0" typeName="" comment="" expression="round(&quot;Longitude&quot;, 5)" precision="0" length="0"/>
    <field name="Rounded Latitude" type="6" subType="0" typeName="" comment="" expression="round(&quot;Latitude&quot;, 5)" precision="0" length="0"/>
    <field name="Rounded Elevation (m)" type="6" subType="0" typeName="" comment="" expression="round(&quot;Elevation (m)&quot;, 1)" precision="0" length="0"/>
    <field name="Rounded Near Grazing Radius (m)" type="6" subType="0" typeName="" comment="" expression="round(&quot;Near Grazing Radius (m)&quot;, 0)" precision="0" length="0"/>
    <field name="Rounded Far Grazing Radius (m)" type="6" subType="0" typeName="" comment="" expression="round(&quot;Far Grazing Radius (m)&quot;, 0)" precision="0" length="0"/>
    <field name="Rounded Longitude" type="6" subType="0" typeName="" comment="" expression="round(&quot;Longitude&quot;, 5)" precision="0" length="0"/>
    <field name="Rounded Latitude" type="6" subType="0" typeName="" comment="" expression="round(&quot;Latitude&quot;, 5)" precision="0" length="0"/>
    <field name="Rounded Elevation (m)" type="6" subType="0" typeName="" comment="" expression="round(&quot;Elevation (m)&quot;, 1)" precision="0" length="0"/>
  </expressionfields>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="&quot;Rounded Longitude&quot;">
    <columns>
      <column name="fid" type="field" width="53" hidden="0"/>
      <column name="Name" type="field" width="197" hidden="0"/>
      <column name="Waterpoint Type" type="field" width="236" hidden="0"/>
      <column name="Status" type="field" width="97" hidden="0"/>
      <column name="Near Grazing Radius (m)" type="field" width="-1" hidden="1"/>
      <column name="Far Grazing Radius (m)" type="field" width="-1" hidden="1"/>
      <column name="Longitude" type="field" width="-1" hidden="1"/>
      <column name="Latitude" type="field" width="-1" hidden="1"/>
      <column name="Elevation (m)" type="field" width="-1" hidden="1"/>
      <column name="Rounded Near Grazing Radius (m)" type="field" width="269" hidden="0"/>
      <column name="Rounded Far Grazing Radius (m)" type="field" width="235" hidden="0"/>
      <column name="Rounded Longitude" type="field" width="116" hidden="0"/>
      <column name="Rounded Latitude" type="field" width="111" hidden="0"/>
      <column name="Rounded Elevation (m)" type="field" width="157" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
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
  <featformsuppress>2</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorField showLabel="1" index="0" name="fid"/>
    <attributeEditorField showLabel="1" index="1" name="Name"/>
    <attributeEditorField showLabel="1" index="5" name="Status"/>
    <attributeEditorField showLabel="1" index="2" name="Waterpoint Type"/>
    <attributeEditorField showLabel="1" index="6" name="Longitude"/>
    <attributeEditorField showLabel="1" index="7" name="Latitude"/>
    <attributeEditorField showLabel="1" index="8" name="Elevation (m)"/>
    <attributeEditorField showLabel="1" index="4" name="Far Grazing Radius (m)"/>
    <attributeEditorField showLabel="1" index="3" name="Near Grazing Radius (m)"/>
  </attributeEditorForm>
  <editable>
    <field name="Elevation (m)" editable="1"/>
    <field name="Far Grazing Radius (m)" editable="1"/>
    <field name="Latitude" editable="1"/>
    <field name="Longitude" editable="1"/>
    <field name="Name" editable="1"/>
    <field name="Near Grazing Radius (m)" editable="1"/>
    <field name="Rounded Elevation (m)" editable="0"/>
    <field name="Rounded Far Grazing Radius (m)" editable="0"/>
    <field name="Rounded Latitude" editable="0"/>
    <field name="Rounded Longitude" editable="0"/>
    <field name="Rounded Near Grazing Radius (m)" editable="0"/>
    <field name="Status" editable="1"/>
    <field name="Waterpoint Type" editable="1"/>
    <field name="fid" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="Elevation (m)" labelOnTop="0"/>
    <field name="Far Grazing Radius (m)" labelOnTop="0"/>
    <field name="Latitude" labelOnTop="0"/>
    <field name="Longitude" labelOnTop="0"/>
    <field name="Name" labelOnTop="0"/>
    <field name="Near Grazing Radius (m)" labelOnTop="0"/>
    <field name="Rounded Elevation (m)" labelOnTop="0"/>
    <field name="Rounded Far Grazing Radius (m)" labelOnTop="0"/>
    <field name="Rounded Latitude" labelOnTop="0"/>
    <field name="Rounded Longitude" labelOnTop="0"/>
    <field name="Rounded Near Grazing Radius (m)" labelOnTop="0"/>
    <field name="Status" labelOnTop="0"/>
    <field name="Waterpoint Type" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="Elevation (m)" reuseLastValue="0"/>
    <field name="Far Grazing Radius (m)" reuseLastValue="0"/>
    <field name="Latitude" reuseLastValue="0"/>
    <field name="Longitude" reuseLastValue="0"/>
    <field name="Name" reuseLastValue="0"/>
    <field name="Near Grazing Radius (m)" reuseLastValue="0"/>
    <field name="Rounded Elevation (m)" reuseLastValue="0"/>
    <field name="Rounded Far Grazing Radius (m)" reuseLastValue="0"/>
    <field name="Rounded Latitude" reuseLastValue="0"/>
    <field name="Rounded Longitude" reuseLastValue="0"/>
    <field name="Rounded Near Grazing Radius (m)" reuseLastValue="0"/>
    <field name="Status" reuseLastValue="0"/>
    <field name="Waterpoint Type" reuseLastValue="0"/>
    <field name="fid" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"WPT_TYPE"</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
