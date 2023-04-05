<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" version="3.28.4-Firenze" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms|AttributeTable" readOnly="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <renderer-v2 type="singleSymbol" symbollevels="0" referencescale="-1" enableorderby="0" forceraster="0">
    <symbols>
      <symbol force_rhr="0" name="0" type="fill" frame_rate="10" clip_to_extent="1" alpha="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties" type="Map">
              <Option name="alpha" type="Map">
                <Option name="active" value="true" type="bool"/>
                <Option name="expression" value="case &#xd;&#xa;when matchCurrentTimeframe(&quot;Timeframe&quot;) then 100.0&#xd;&#xa;else 0.0&#xd;&#xa;end" type="QString"/>
                <Option name="type" value="3" type="int"/>
              </Option>
            </Option>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleLine" locked="0" enabled="1" pass="0">
          <Option type="Map">
            <Option name="align_dash_pattern" value="0" type="QString"/>
            <Option name="capstyle" value="square" type="QString"/>
            <Option name="customdash" value="5;2" type="QString"/>
            <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="customdash_unit" value="MM" type="QString"/>
            <Option name="dash_pattern_offset" value="0" type="QString"/>
            <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
            <Option name="draw_inside_polygon" value="0" type="QString"/>
            <Option name="joinstyle" value="bevel" type="QString"/>
            <Option name="line_color" value="77,175,74,255" type="QString"/>
            <Option name="line_style" value="solid" type="QString"/>
            <Option name="line_width" value="0.96" type="QString"/>
            <Option name="line_width_unit" value="MM" type="QString"/>
            <Option name="offset" value="0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="ring_filter" value="0" type="QString"/>
            <Option name="trim_distance_end" value="0" type="QString"/>
            <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_end_unit" value="MM" type="QString"/>
            <Option name="trim_distance_start" value="0" type="QString"/>
            <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="trim_distance_start_unit" value="MM" type="QString"/>
            <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
            <Option name="use_custom_dash" value="0" type="QString"/>
            <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
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
    <field name="Timeframe" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Current" value="Current" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="Future" value="Future" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="Undefined" value="Undefined" type="QString"/>
              </Option>
            </Option>
          </Option>
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
    <field name="Watered (km²)" configurationFlags="None">
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
    <field name="Potential AE/km²" configurationFlags="None">
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
    <field name="Potential AE" configurationFlags="None">
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
    <field name="Rounded Area (km²)" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Rounded Watered (km²)" configurationFlags="None">
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
    <field name="Rounded Potential AE/km²" configurationFlags="None">
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
    <field name="Rounded Potential AE" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" name="" index="0"/>
    <alias field="Timeframe" name="" index="1"/>
    <alias field="Perimeter (km)" name="" index="2"/>
    <alias field="Area (km²)" name="" index="3"/>
    <alias field="Watered (km²)" name="" index="4"/>
    <alias field="AE/km²" name="" index="5"/>
    <alias field="Potential AE/km²" name="" index="6"/>
    <alias field="AE" name="" index="7"/>
    <alias field="Potential AE" name="" index="8"/>
    <alias field="Rounded Perimeter (km)" name="Perimeter (km)" index="9"/>
    <alias field="Rounded Area (km²)" name="Area (km²)" index="10"/>
    <alias field="Rounded Watered (km²)" name="Watered (km²)" index="11"/>
    <alias field="Rounded AE/km²" name="AE/km²" index="12"/>
    <alias field="Rounded Potential AE/km²" name="Potential AE/km²" index="13"/>
    <alias field="Rounded AE" name="AE" index="14"/>
    <alias field="Rounded Potential AE" name="Potential AE" index="15"/>
  </aliases>
  <defaults>
    <default field="fid" applyOnUpdate="0" expression=""/>
    <default field="Timeframe" applyOnUpdate="0" expression="'Undefined'"/>
    <default field="Perimeter (km)" applyOnUpdate="0" expression=""/>
    <default field="Area (km²)" applyOnUpdate="0" expression=""/>
    <default field="Watered (km²)" applyOnUpdate="0" expression=""/>
    <default field="AE/km²" applyOnUpdate="0" expression=""/>
    <default field="Potential AE/km²" applyOnUpdate="0" expression=""/>
    <default field="AE" applyOnUpdate="0" expression=""/>
    <default field="Potential AE" applyOnUpdate="0" expression=""/>
    <default field="Rounded Perimeter (km)" applyOnUpdate="0" expression=""/>
    <default field="Rounded Area (km²)" applyOnUpdate="0" expression=""/>
    <default field="Rounded Watered (km²)" applyOnUpdate="0" expression=""/>
    <default field="Rounded AE/km²" applyOnUpdate="0" expression=""/>
    <default field="Rounded Potential AE/km²" applyOnUpdate="0" expression=""/>
    <default field="Rounded AE" applyOnUpdate="0" expression=""/>
    <default field="Rounded Potential AE" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="fid" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Timeframe" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Perimeter (km)" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Area (km²)" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Watered (km²)" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="AE/km²" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Potential AE/km²" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="AE" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Potential AE" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Rounded Perimeter (km)" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Rounded Area (km²)" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Rounded Watered (km²)" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Rounded AE/km²" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Rounded Potential AE/km²" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Rounded AE" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="Rounded Potential AE" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" exp="" desc=""/>
    <constraint field="Timeframe" exp="" desc=""/>
    <constraint field="Perimeter (km)" exp="" desc=""/>
    <constraint field="Area (km²)" exp="" desc=""/>
    <constraint field="Watered (km²)" exp="" desc=""/>
    <constraint field="AE/km²" exp="" desc=""/>
    <constraint field="Potential AE/km²" exp="" desc=""/>
    <constraint field="AE" exp="" desc=""/>
    <constraint field="Potential AE" exp="" desc=""/>
    <constraint field="Rounded Perimeter (km)" exp="" desc=""/>
    <constraint field="Rounded Area (km²)" exp="" desc=""/>
    <constraint field="Rounded Watered (km²)" exp="" desc=""/>
    <constraint field="Rounded AE/km²" exp="" desc=""/>
    <constraint field="Rounded Potential AE/km²" exp="" desc=""/>
    <constraint field="Rounded AE" exp="" desc=""/>
    <constraint field="Rounded Potential AE" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field typeName="" name="Rounded Perimeter (km)" precision="0" type="6" comment="" expression="round(&quot;Perimeter (km)&quot;, 2)" length="0" subType="0"/>
    <field typeName="" name="Rounded Area (km²)" precision="0" type="6" comment="" expression="round(&quot;Area (km²)&quot;, 2)" length="0" subType="0"/>
    <field typeName="" name="Rounded Watered (km²)" precision="0" type="6" comment="" expression="round(&quot;Watered (km²)&quot;, 2)" length="0" subType="0"/>
    <field typeName="" name="Rounded AE/km²" precision="0" type="6" comment="" expression="round(&quot;AE/km²&quot;, 1)" length="0" subType="0"/>
    <field typeName="" name="Rounded Potential AE/km²" precision="0" type="6" comment="" expression="round(&quot;Potential AE/km²&quot;, 1)" length="0" subType="0"/>
    <field typeName="" name="Rounded AE" precision="0" type="6" comment="" expression="round(&quot;AE&quot;, 0)" length="0" subType="0"/>
    <field typeName="" name="Rounded Potential AE" precision="0" type="6" comment="" expression="round(&quot;Potential AE&quot;, 0)" length="0" subType="0"/>
  </expressionfields>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column name="Timeframe" type="field" width="-1" hidden="0"/>
      <column name="fid" type="field" width="-1" hidden="0"/>
      <column name="Perimeter (km)" type="field" width="-1" hidden="1"/>
      <column name="Area (km²)" type="field" width="-1" hidden="1"/>
      <column name="Watered (km²)" type="field" width="-1" hidden="1"/>
      <column name="AE/km²" type="field" width="-1" hidden="1"/>
      <column name="Potential AE/km²" type="field" width="-1" hidden="1"/>
      <column name="AE" type="field" width="-1" hidden="1"/>
      <column name="Potential AE" type="field" width="-1" hidden="1"/>
      <column name="Rounded Perimeter (km)" type="field" width="-1" hidden="0"/>
      <column name="Rounded Area (km²)" type="field" width="-1" hidden="0"/>
      <column name="Rounded Watered (km²)" type="field" width="-1" hidden="0"/>
      <column name="Rounded AE/km²" type="field" width="243" hidden="0"/>
      <column name="Rounded Potential AE/km²" type="field" width="246" hidden="0"/>
      <column name="Rounded AE" type="field" width="-1" hidden="0"/>
      <column name="Rounded Potential AE" type="field" width="-1" hidden="0"/>
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
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="AE" editable="1"/>
    <field name="AE/km²" editable="1"/>
    <field name="Area (km²)" editable="1"/>
    <field name="Perimeter (km)" editable="1"/>
    <field name="Potential AE" editable="1"/>
    <field name="Potential AE/km²" editable="1"/>
    <field name="Rounded AE" editable="0"/>
    <field name="Rounded AE/km²" editable="0"/>
    <field name="Rounded Area (km²)" editable="0"/>
    <field name="Rounded Perimeter (km)" editable="0"/>
    <field name="Rounded Potential AE" editable="0"/>
    <field name="Rounded Potential AE/km²" editable="0"/>
    <field name="Rounded Watered (km²)" editable="0"/>
    <field name="Status" editable="1"/>
    <field name="Timeframe" editable="1"/>
    <field name="Watered (km²)" editable="1"/>
    <field name="fid" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="AE" labelOnTop="0"/>
    <field name="AE/km²" labelOnTop="0"/>
    <field name="Area (km²)" labelOnTop="0"/>
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
    <field name="Status" labelOnTop="0"/>
    <field name="Timeframe" labelOnTop="0"/>
    <field name="Watered (km²)" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="AE" reuseLastValue="0"/>
    <field name="AE/km²" reuseLastValue="0"/>
    <field name="Area (km²)" reuseLastValue="0"/>
    <field name="Perimeter (km)" reuseLastValue="0"/>
    <field name="Potential AE" reuseLastValue="0"/>
    <field name="Potential AE/km²" reuseLastValue="0"/>
    <field name="Rounded AE" reuseLastValue="0"/>
    <field name="Rounded AE/km²" reuseLastValue="0"/>
    <field name="Rounded Area (km²)" reuseLastValue="0"/>
    <field name="Rounded Perimeter (km)" reuseLastValue="0"/>
    <field name="Rounded Potential AE" reuseLastValue="0"/>
    <field name="Rounded Potential AE/km²" reuseLastValue="0"/>
    <field name="Rounded Watered (km²)" reuseLastValue="0"/>
    <field name="Status" reuseLastValue="0"/>
    <field name="Timeframe" reuseLastValue="0"/>
    <field name="Watered (km²)" reuseLastValue="0"/>
    <field name="fid" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"Status"</previewExpression>
  <layerGeometryType>2</layerGeometryType>
</qgis>
