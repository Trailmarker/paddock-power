<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" version="3.22.13-Białowieża" maxScale="0" hasScaleBasedVisibilityFlag="0" labelsEnabled="0" styleCategories="AllStyleCategories" simplifyDrawingTol="1" simplifyLocal="1" symbologyReferenceScale="-1" minScale="0" simplifyDrawingHints="1" simplifyMaxScale="1" readOnly="1">
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
  <renderer-v2 graduatedMethod="GraduatedColor" attr="case&#xd;&#xa;when matchCurrentTimeframe(&quot;Timeframe&quot;) then &quot;AE/km²&quot;&#xd;&#xa;else 'Ignored'&#xd;&#xa;end&#xd;&#xa;" forceraster="0" referencescale="-1" enableorderby="0" type="graduatedSymbol" symbollevels="0">
    <ranges>
      <range lower="0.000000000000000" upper="0.000000000000000" label="Non-producing" render="true" symbol="0"/>
      <range lower="0.000000000000000" upper="5.000000000000000" label="0 – 5 AE/km²" render="true" symbol="1"/>
      <range lower="5.000000000000000" upper="10.000000000000000" label="5 – 10 AE/km²" render="true" symbol="2"/>
      <range lower="10.000000000000000" upper="15.000000000000000" label="10 – 15 AE/km²" render="true" symbol="3"/>
      <range lower="15.000000000000000" upper="20.000000000000000" label="15 – 20 AE/km²" render="true" symbol="4"/>
      <range lower="20.000000000000000" upper="100.000000000000000" label="Over 20 AE/km²" render="true" symbol="5"/>
    </ranges>
    <symbols>
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" type="fill" name="0">
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
            <Option value="255,103,0,255" type="QString" name="color"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="255,255,0,255" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0.66" type="QString" name="outline_width"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="solid" type="QString" name="style"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="255,103,0,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.66"/>
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
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" type="fill" name="1">
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
            <Option value="161,217,155,255" type="QString" name="color"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="255,255,0,255" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0.66" type="QString" name="outline_width"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="solid" type="QString" name="style"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="161,217,155,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.66"/>
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
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" type="fill" name="2">
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
            <Option value="116,196,118,255" type="QString" name="color"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="255,255,0,255" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0.66" type="QString" name="outline_width"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="solid" type="QString" name="style"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="116,196,118,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.66"/>
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
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" type="fill" name="3">
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
            <Option value="65,171,93,255" type="QString" name="color"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="255,255,0,255" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0.66" type="QString" name="outline_width"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="solid" type="QString" name="style"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="65,171,93,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.66"/>
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
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" type="fill" name="4">
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
            <Option value="35,139,69,255" type="QString" name="color"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="255,255,0,255" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0.66" type="QString" name="outline_width"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="solid" type="QString" name="style"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="35,139,69,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.66"/>
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
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" type="fill" name="5">
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
            <Option value="0,109,44,255" type="QString" name="color"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="255,255,0,255" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0.66" type="QString" name="outline_width"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="solid" type="QString" name="style"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="0,109,44,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.66"/>
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
    <source-symbol>
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" type="fill" name="0">
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
            <Option value="125,139,143,255" type="QString" name="color"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0.26" type="QString" name="outline_width"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="solid" type="QString" name="style"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="125,139,143,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
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
    </source-symbol>
    <colorramp type="preset" name="[source]">
      <Option type="Map">
        <Option value="161,217,155,255" type="QString" name="preset_color_0"/>
        <Option value="116,196,118,255" type="QString" name="preset_color_1"/>
        <Option value="65,171,93,255" type="QString" name="preset_color_2"/>
        <Option value="35,139,69,255" type="QString" name="preset_color_3"/>
        <Option value="0,109,44,255" type="QString" name="preset_color_4"/>
        <Option value="#a1d99b" type="QString" name="preset_color_name_0"/>
        <Option value="#74c476" type="QString" name="preset_color_name_1"/>
        <Option value="#41ab5d" type="QString" name="preset_color_name_2"/>
        <Option value="#238b45" type="QString" name="preset_color_name_3"/>
        <Option value="#006d2c" type="QString" name="preset_color_name_4"/>
        <Option value="preset" type="QString" name="rampType"/>
      </Option>
      <prop k="preset_color_0" v="161,217,155,255"/>
      <prop k="preset_color_1" v="116,196,118,255"/>
      <prop k="preset_color_2" v="65,171,93,255"/>
      <prop k="preset_color_3" v="35,139,69,255"/>
      <prop k="preset_color_4" v="0,109,44,255"/>
      <prop k="preset_color_name_0" v="#a1d99b"/>
      <prop k="preset_color_name_1" v="#74c476"/>
      <prop k="preset_color_name_2" v="#41ab5d"/>
      <prop k="preset_color_name_3" v="#238b45"/>
      <prop k="preset_color_name_4" v="#006d2c"/>
      <prop k="rampType" v="preset"/>
    </colorramp>
    <classificationMethod id="Quantile">
      <symmetricMode astride="0" enabled="0" symmetrypoint="0"/>
      <labelFormat format="%1 - %2" labelprecision="4" trimtrailingzeroes="1"/>
      <parameters>
        <Option/>
      </parameters>
      <extraInformation/>
    </classificationMethod>
    <rotation/>
    <sizescale/>
  </renderer-v2>
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
    <field name="Area (km²)" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AE/km²" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Potential AE/km²" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AE" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Potential AE" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Condition" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="A" type="QString" name="A"/>
              </Option>
              <Option type="Map">
                <Option value="B" type="QString" name="B"/>
              </Option>
              <Option type="Map">
                <Option value="C" type="QString" name="C"/>
              </Option>
              <Option type="Map">
                <Option value="D" type="QString" name="D"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="Paddock" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Paddock Name" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Timeframe" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="Historical" type="QString" name="Historical"/>
              </Option>
              <Option type="Map">
                <Option value="Current" type="QString" name="Current"/>
              </Option>
              <Option type="Map">
                <Option value="Future" type="QString" name="Future"/>
              </Option>
              <Option type="Map">
                <Option value="Drafted" type="QString" name="Drafted"/>
              </Option>
              <Option type="Map">
                <Option value="Undefined" type="QString" name="Undefined"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="Land Type" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Land Type Name" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Area (km²)" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded AE/km²" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Potential AE/km²" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded AE" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Potential AE" configurationFlags="None">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""/>
    <alias field="Area (km²)" index="1" name=""/>
    <alias field="AE/km²" index="2" name=""/>
    <alias field="Potential AE/km²" index="3" name=""/>
    <alias field="AE" index="4" name=""/>
    <alias field="Potential AE" index="5" name=""/>
    <alias field="Condition" index="6" name=""/>
    <alias field="Paddock" index="7" name=""/>
    <alias field="Paddock Name" index="8" name=""/>
    <alias field="Timeframe" index="9" name=""/>
    <alias field="Land Type" index="10" name=""/>
    <alias field="Land Type Name" index="11" name=""/>
    <alias field="Rounded Area (km²)" index="12" name="Area (km²)"/>
    <alias field="Rounded AE/km²" index="13" name="AE/km²"/>
    <alias field="Rounded Potential AE/km²" index="14" name="Potential AE/km²"/>
    <alias field="Rounded AE" index="15" name="AE"/>
    <alias field="Rounded Potential AE" index="16" name="Potential AE"/>
  </aliases>
  <defaults>
    <default field="fid" applyOnUpdate="0" expression=""/>
    <default field="Area (km²)" applyOnUpdate="0" expression=""/>
    <default field="AE/km²" applyOnUpdate="0" expression=""/>
    <default field="Potential AE/km²" applyOnUpdate="0" expression=""/>
    <default field="AE" applyOnUpdate="0" expression=""/>
    <default field="Potential AE" applyOnUpdate="0" expression=""/>
    <default field="Condition" applyOnUpdate="0" expression="'A'"/>
    <default field="Paddock" applyOnUpdate="0" expression=""/>
    <default field="Paddock Name" applyOnUpdate="0" expression=""/>
    <default field="Timeframe" applyOnUpdate="0" expression="'Undefined'"/>
    <default field="Land Type" applyOnUpdate="0" expression=""/>
    <default field="Land Type Name" applyOnUpdate="0" expression=""/>
    <default field="Rounded Area (km²)" applyOnUpdate="0" expression=""/>
    <default field="Rounded AE/km²" applyOnUpdate="0" expression=""/>
    <default field="Rounded Potential AE/km²" applyOnUpdate="0" expression=""/>
    <default field="Rounded AE" applyOnUpdate="0" expression=""/>
    <default field="Rounded Potential AE" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="fid" unique_strength="1" constraints="3" exp_strength="0" notnull_strength="1"/>
    <constraint field="Area (km²)" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="AE/km²" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Potential AE/km²" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="AE" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Potential AE" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Condition" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Paddock" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Paddock Name" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Timeframe" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Land Type" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Land Type Name" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Rounded Area (km²)" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Rounded AE/km²" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Rounded Potential AE/km²" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Rounded AE" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint field="Rounded Potential AE" unique_strength="0" constraints="0" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="Area (km²)" desc="" exp=""/>
    <constraint field="AE/km²" desc="" exp=""/>
    <constraint field="Potential AE/km²" desc="" exp=""/>
    <constraint field="AE" desc="" exp=""/>
    <constraint field="Potential AE" desc="" exp=""/>
    <constraint field="Condition" desc="" exp=""/>
    <constraint field="Paddock" desc="" exp=""/>
    <constraint field="Paddock Name" desc="" exp=""/>
    <constraint field="Timeframe" desc="" exp=""/>
    <constraint field="Land Type" desc="" exp=""/>
    <constraint field="Land Type Name" desc="" exp=""/>
    <constraint field="Rounded Area (km²)" desc="" exp=""/>
    <constraint field="Rounded AE/km²" desc="" exp=""/>
    <constraint field="Rounded Potential AE/km²" desc="" exp=""/>
    <constraint field="Rounded AE" desc="" exp=""/>
    <constraint field="Rounded Potential AE" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields>
    <field typeName="" length="0" expression="round(&quot;Area (km²)&quot;, 2)" precision="0" subType="0" comment="" name="Rounded Area (km²)" type="6"/>
    <field typeName="" length="0" expression="round(&quot;AE/km²&quot;, 1)" precision="0" subType="0" comment="" name="Rounded AE/km²" type="6"/>
    <field typeName="" length="0" expression="round(&quot;Potential AE/km²&quot;, 1)" precision="0" subType="0" comment="" name="Rounded Potential AE/km²" type="6"/>
    <field typeName="" length="0" expression="round(&quot;AE&quot;, 0)" precision="0" subType="0" comment="" name="Rounded AE" type="6"/>
    <field typeName="" length="0" expression="round(&quot;Potential AE&quot;, 0)" precision="0" subType="0" comment="" name="Rounded Potential AE" type="6"/>
  </expressionfields>
  <attributeactions/>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column hidden="0" type="field" name="Paddock" width="-1"/>
      <column hidden="0" type="field" name="Paddock Name" width="369"/>
      <column hidden="0" type="field" name="Land Type" width="296"/>
      <column hidden="0" type="field" name="Land Type Name" width="243"/>
      <column hidden="1" type="field" name="AE/km²" width="280"/>
      <column hidden="0" type="field" name="Condition" width="-1"/>
      <column hidden="0" type="field" name="fid" width="-1"/>
      <column hidden="1" type="field" name="Area (km²)" width="-1"/>
      <column hidden="1" type="field" name="AE" width="-1"/>
      <column hidden="1" type="field" name="Potential AE" width="-1"/>
      <column hidden="1" type="field" name="Potential AE/km²" width="262"/>
      <column hidden="0" type="field" name="Timeframe" width="-1"/>
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
    <field editable="1" name="Condition"/>
    <field editable="1" name="Grazing Radius Type"/>
    <field editable="1" name="Land Type"/>
    <field editable="1" name="Land Type Name"/>
    <field editable="1" name="Paddock"/>
    <field editable="1" name="Paddock Name"/>
    <field editable="1" name="Paddock Status"/>
    <field editable="1" name="Potential AE"/>
    <field editable="1" name="Potential AE/km²"/>
    <field editable="1" name="Timeframe"/>
    <field editable="1" name="Watered"/>
    <field editable="1" name="Watered Area Status"/>
    <field editable="1" name="fid"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="AE"/>
    <field labelOnTop="0" name="AE/km²"/>
    <field labelOnTop="0" name="Area (km²)"/>
    <field labelOnTop="0" name="Condition"/>
    <field labelOnTop="0" name="Grazing Radius Type"/>
    <field labelOnTop="0" name="Land Type"/>
    <field labelOnTop="0" name="Land Type Name"/>
    <field labelOnTop="0" name="Paddock"/>
    <field labelOnTop="0" name="Paddock Name"/>
    <field labelOnTop="0" name="Paddock Status"/>
    <field labelOnTop="0" name="Potential AE"/>
    <field labelOnTop="0" name="Potential AE/km²"/>
    <field labelOnTop="0" name="Timeframe"/>
    <field labelOnTop="0" name="Watered"/>
    <field labelOnTop="0" name="Watered Area Status"/>
    <field labelOnTop="0" name="fid"/>
  </labelOnTop>
  <reuseLastValue>
    <field reuseLastValue="0" name="AE"/>
    <field reuseLastValue="0" name="AE/km²"/>
    <field reuseLastValue="0" name="Area (km²)"/>
    <field reuseLastValue="0" name="Condition"/>
    <field reuseLastValue="0" name="Grazing Radius Type"/>
    <field reuseLastValue="0" name="Land Type"/>
    <field reuseLastValue="0" name="Land Type Name"/>
    <field reuseLastValue="0" name="Paddock"/>
    <field reuseLastValue="0" name="Paddock Name"/>
    <field reuseLastValue="0" name="Paddock Status"/>
    <field reuseLastValue="0" name="Potential AE"/>
    <field reuseLastValue="0" name="Potential AE/km²"/>
    <field reuseLastValue="0" name="Timeframe"/>
    <field reuseLastValue="0" name="Watered"/>
    <field reuseLastValue="0" name="Watered Area Status"/>
    <field reuseLastValue="0" name="fid"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"Paddock Name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
