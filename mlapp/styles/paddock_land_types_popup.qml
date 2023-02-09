<?xml version="1.1"?>
<qgis version="3.22.13-Białowieża" styleCategories="AllStyleCategories" readOnly="1" hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0" simplifyDrawingTol="1" labelsEnabled="0" simplifyDrawingHints="1" symbologyReferenceScale="-1" maxScale="0" simplifyLocal="1" minScale="0" simplifyMaxScale="1">
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
  <renderer-v2 symbollevels="0" graduatedMethod="GraduatedColor" forceraster="0" referencescale="-1" enableorderby="0" type="graduatedSymbol" attr="case&#xd;&#xa;when matchCurrentTimeframe(&quot;Timeframe&quot;) then &quot;AE/km²&quot;&#xd;&#xa;else 'Ignored'&#xd;&#xa;end&#xd;&#xa;">
    <ranges>
      <range upper="0.000000000000000" label="Non-producing" render="true" lower="0.000000000000000" symbol="0"/>
      <range upper="5.000000000000000" label="0 – 5 AE/km²" render="true" lower="0.000000000000000" symbol="1"/>
      <range upper="10.000000000000000" label="5 – 10 AE/km²" render="true" lower="5.000000000000000" symbol="2"/>
      <range upper="15.000000000000000" label="10 – 15 AE/km²" render="true" lower="10.000000000000000" symbol="3"/>
      <range upper="20.000000000000000" label="15 – 20 AE/km²" render="true" lower="15.000000000000000" symbol="4"/>
      <range upper="100.000000000000000" label="Over 20 AE/km²" render="true" lower="20.000000000000000" symbol="5"/>
    </ranges>
    <symbols>
      <symbol clip_to_extent="1" name="0" type="fill" force_rhr="0" alpha="1">
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
            <Option name="color" type="QString" value="255,103,0,255"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="255,255,0,255"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0.66"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="style" type="QString" value="solid"/>
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="1" type="fill" force_rhr="0" alpha="1">
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
            <Option name="color" type="QString" value="161,217,155,255"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="255,255,0,255"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0.66"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="style" type="QString" value="solid"/>
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="2" type="fill" force_rhr="0" alpha="1">
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
            <Option name="color" type="QString" value="116,196,118,255"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="255,255,0,255"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0.66"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="style" type="QString" value="solid"/>
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="3" type="fill" force_rhr="0" alpha="1">
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
            <Option name="color" type="QString" value="65,171,93,255"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="255,255,0,255"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0.66"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="style" type="QString" value="solid"/>
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="4" type="fill" force_rhr="0" alpha="1">
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
            <Option name="color" type="QString" value="35,139,69,255"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="255,255,0,255"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0.66"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="style" type="QString" value="solid"/>
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="5" type="fill" force_rhr="0" alpha="1">
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
            <Option name="color" type="QString" value="0,109,44,255"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="255,255,0,255"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0.66"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="style" type="QString" value="solid"/>
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol clip_to_extent="1" name="0" type="fill" force_rhr="0" alpha="1">
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
            <Option name="color" type="QString" value="125,139,143,255"/>
            <Option name="joinstyle" type="QString" value="bevel"/>
            <Option name="offset" type="QString" value="0,0"/>
            <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="outline_color" type="QString" value="35,35,35,255"/>
            <Option name="outline_style" type="QString" value="solid"/>
            <Option name="outline_width" type="QString" value="0.26"/>
            <Option name="outline_width_unit" type="QString" value="MM"/>
            <Option name="style" type="QString" value="solid"/>
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <colorramp name="[source]" type="preset">
      <Option type="Map">
        <Option name="preset_color_0" type="QString" value="161,217,155,255"/>
        <Option name="preset_color_1" type="QString" value="116,196,118,255"/>
        <Option name="preset_color_2" type="QString" value="65,171,93,255"/>
        <Option name="preset_color_3" type="QString" value="35,139,69,255"/>
        <Option name="preset_color_4" type="QString" value="0,109,44,255"/>
        <Option name="preset_color_name_0" type="QString" value="#a1d99b"/>
        <Option name="preset_color_name_1" type="QString" value="#74c476"/>
        <Option name="preset_color_name_2" type="QString" value="#41ab5d"/>
        <Option name="preset_color_name_3" type="QString" value="#238b45"/>
        <Option name="preset_color_name_4" type="QString" value="#006d2c"/>
        <Option name="rampType" type="QString" value="preset"/>
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
      <symmetricMode symmetrypoint="0" astride="0" enabled="0"/>
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
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="A" type="QString" value="A"/>
              </Option>
              <Option type="Map">
                <Option name="B" type="QString" value="B"/>
              </Option>
              <Option type="Map">
                <Option name="C" type="QString" value="C"/>
              </Option>
              <Option type="Map">
                <Option name="D" type="QString" value="D"/>
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
    <field name="Watered Area (km²)" configurationFlags="None">
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
    <field name="Rounded Watered Area (km²)" configurationFlags="None">
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
    <alias field="Watered Area (km²)" index="12" name=""/>
    <alias field="Rounded Area (km²)" index="13" name="Area (km²)"/>
    <alias field="Rounded Watered Area (km²)" index="14" name="Watered Area (km²)"/>
    <alias field="Rounded AE/km²" index="15" name="AE/km²"/>
    <alias field="Rounded Potential AE/km²" index="16" name="Potential AE/km²"/>
    <alias field="Rounded AE" index="17" name="AE"/>
    <alias field="Rounded Potential AE" index="18" name="Potential AE"/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="Area (km²)" applyOnUpdate="0"/>
    <default expression="" field="AE/km²" applyOnUpdate="0"/>
    <default expression="" field="Potential AE/km²" applyOnUpdate="0"/>
    <default expression="" field="AE" applyOnUpdate="0"/>
    <default expression="" field="Potential AE" applyOnUpdate="0"/>
    <default expression="'A'" field="Condition" applyOnUpdate="0"/>
    <default expression="" field="Paddock" applyOnUpdate="0"/>
    <default expression="" field="Paddock Name" applyOnUpdate="0"/>
    <default expression="'Undefined'" field="Timeframe" applyOnUpdate="0"/>
    <default expression="" field="Land Type" applyOnUpdate="0"/>
    <default expression="" field="Land Type Name" applyOnUpdate="0"/>
    <default expression="" field="Watered Area (km²)" applyOnUpdate="0"/>
    <default expression="" field="Rounded Area (km²)" applyOnUpdate="0"/>
    <default expression="" field="Rounded Watered Area (km²)" applyOnUpdate="0"/>
    <default expression="" field="Rounded AE/km²" applyOnUpdate="0"/>
    <default expression="" field="Rounded Potential AE/km²" applyOnUpdate="0"/>
    <default expression="" field="Rounded AE" applyOnUpdate="0"/>
    <default expression="" field="Rounded Potential AE" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" field="fid" unique_strength="1" exp_strength="0" constraints="3"/>
    <constraint notnull_strength="0" field="Area (km²)" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="AE/km²" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Potential AE/km²" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="AE" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Potential AE" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Condition" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Paddock" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Paddock Name" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Timeframe" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Land Type" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Land Type Name" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Watered Area (km²)" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Rounded Area (km²)" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Rounded Watered Area (km²)" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Rounded AE/km²" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Rounded Potential AE/km²" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Rounded AE" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="Rounded Potential AE" unique_strength="0" exp_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="fid" desc=""/>
    <constraint exp="" field="Area (km²)" desc=""/>
    <constraint exp="" field="AE/km²" desc=""/>
    <constraint exp="" field="Potential AE/km²" desc=""/>
    <constraint exp="" field="AE" desc=""/>
    <constraint exp="" field="Potential AE" desc=""/>
    <constraint exp="" field="Condition" desc=""/>
    <constraint exp="" field="Paddock" desc=""/>
    <constraint exp="" field="Paddock Name" desc=""/>
    <constraint exp="" field="Timeframe" desc=""/>
    <constraint exp="" field="Land Type" desc=""/>
    <constraint exp="" field="Land Type Name" desc=""/>
    <constraint exp="" field="Watered Area (km²)" desc=""/>
    <constraint exp="" field="Rounded Area (km²)" desc=""/>
    <constraint exp="" field="Rounded Watered Area (km²)" desc=""/>
    <constraint exp="" field="Rounded AE/km²" desc=""/>
    <constraint exp="" field="Rounded Potential AE/km²" desc=""/>
    <constraint exp="" field="Rounded AE" desc=""/>
    <constraint exp="" field="Rounded Potential AE" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field comment="" expression="round(&quot;Area (km²)&quot;, 2)" typeName="" name="Rounded Area (km²)" subType="0" precision="0" type="6" length="0"/>
    <field comment="" expression="round(&quot;Watered Area (km²)&quot;, 2)" typeName="" name="Rounded Watered Area (km²)" subType="0" precision="0" type="6" length="0"/>
    <field comment="" expression="round(&quot;AE/km²&quot;, 1)" typeName="" name="Rounded AE/km²" subType="0" precision="0" type="6" length="0"/>
    <field comment="" expression="round(&quot;Potential AE/km²&quot;, 1)" typeName="" name="Rounded Potential AE/km²" subType="0" precision="0" type="6" length="0"/>
    <field comment="" expression="round(&quot;AE&quot;, 0)" typeName="" name="Rounded AE" subType="0" precision="0" type="6" length="0"/>
    <field comment="" expression="round(&quot;Potential AE&quot;, 0)" typeName="" name="Rounded Potential AE" subType="0" precision="0" type="6" length="0"/>
  </expressionfields>
  <attributeactions/>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="0" width="-1" name="Paddock" type="field"/>
      <column hidden="0" width="369" name="Paddock Name" type="field"/>
      <column hidden="0" width="296" name="Land Type" type="field"/>
      <column hidden="0" width="243" name="Land Type Name" type="field"/>
      <column hidden="1" width="280" name="AE/km²" type="field"/>
      <column hidden="0" width="-1" name="Condition" type="field"/>
      <column hidden="0" width="-1" name="fid" type="field"/>
      <column hidden="1" width="-1" name="Area (km²)" type="field"/>
      <column hidden="1" width="-1" name="AE" type="field"/>
      <column hidden="1" width="-1" name="Potential AE" type="field"/>
      <column hidden="1" width="-1" name="Potential AE/km²" type="field"/>
      <column hidden="1" width="-1" name="Watered Area (km²)" type="field"/>
      <column hidden="0" width="-1" name="Timeframe" type="field"/>
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
    <field name="AE" labelOnTop="0"/>
    <field name="AE/km²" labelOnTop="0"/>
    <field name="Area (km²)" labelOnTop="0"/>
    <field name="Condition" labelOnTop="0"/>
    <field name="Grazing Radius Type" labelOnTop="0"/>
    <field name="Land Type" labelOnTop="0"/>
    <field name="Land Type Name" labelOnTop="0"/>
    <field name="Paddock" labelOnTop="0"/>
    <field name="Paddock Name" labelOnTop="0"/>
    <field name="Paddock Status" labelOnTop="0"/>
    <field name="Potential AE" labelOnTop="0"/>
    <field name="Potential AE/km²" labelOnTop="0"/>
    <field name="Timeframe" labelOnTop="0"/>
    <field name="Watered" labelOnTop="0"/>
    <field name="Watered Area Status" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
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
