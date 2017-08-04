<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="2.12.1-Lyon" minimumScale="0" maximumScale="1e+08" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
  <edittypes>
    <edittype widgetv2type="TextEdit" name="ste_cd">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="module">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="item_no">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="name">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="category">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="elevation">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="source_cd">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="source_mod">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="source_no">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="file">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="comment">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="cre_on">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="cre_by">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="mod_on">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="mod_by">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="0"/>
    </edittype>
  </edittypes>
  <renderer-v2 forceraster="0" symbollevels="0" type="RuleRenderer">
    <rules key="{e3bebbb7-d4af-48fc-b934-9aaafed669f5}">
      <rule filter="category = 'lvl'" key="{ff45a655-d362-4db0-bfe2-86b6c2215948}" symbol="0" label="Level"/>
      <rule filter="category = 'lvu'" key="{7a45dbfd-fb36-4102-9177-43efecc0e063}" symbol="1" label="Underside Level"/>
      <rule filter="category = 'spf'" key="{6323efd7-0c4d-40f0-81dc-cb6ab79d633e}" symbol="2" label="Special Find"/>
      <rule filter="category = 'sec'" key="{a850d464-6d92-44a4-a7f1-4794181abb7d}" symbol="3" label="Section Pin"/>
      <rule filter="category IS NULL or category NOT IN ('lvl', 'lvu', 'sec', 'spf')" key="{282b4f71-a81d-4ecf-b17e-d9829ab9c7cc}" symbol="4" label="UNKNOWN"/>
    </rules>
    <symbols>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="0">
        <layer pass="0" class="FontMarker" locked="0">
          <prop k="angle" v="90"/>
          <prop k="chr" v="&lt;"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="font" v="Dingbats"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="offset" v="1,-0.5"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="size" v="4"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
        <layer pass="1" class="SimpleMarker" locked="0">
          <prop k="angle" v="90"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="line"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="3.2"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="1">
        <layer pass="0" class="FontMarker" locked="0">
          <prop k="angle" v="270"/>
          <prop k="chr" v="&lt;"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="font" v="Dingbats"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="offset" v="1,-0.3"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="size" v="4"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
        <layer pass="1" class="SimpleMarker" locked="0">
          <prop k="angle" v="270"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="line"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="3.2"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="2">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,0,0,0"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="triangle"/>
          <prop k="offset" v="0,-0.5"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="3.2"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="0.5"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="3">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="202,117,178,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="cross2"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="4">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,0,222,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="3"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="rule-based">
    <rules>
      <rule description="Level" filter="category = 'lvl'">
        <settings>
          <text-style fontItalic="0" fontFamily="Gill Sans" fontLetterSpacing="0" fontUnderline="0" fontSizeMapUnitMaxScale="0" fontWeight="50" fontStrikeout="0" textTransp="0" previewBkgrdColor="#ffffff" fontCapitals="0" textColor="0,0,0,255" fontSizeMapUnitMinScale="0" fontSizeInMapUnits="0" isExpression="0" blendMode="0" fontSize="10" fieldName="elevation" namedStyle="Regular" fontWordSpacing="0"/>
          <text-format placeDirectionSymbol="0" multilineAlign="0" rightDirectionSymbol=">" multilineHeight="1" plussign="0" addDirectionSymbol="0" leftDirectionSymbol="&lt;" formatNumbers="1" decimals="2" wrapChar="" reverseDirectionSymbol="0"/>
          <text-buffer bufferSize="1" bufferSizeMapUnitMinScale="0" bufferColor="255,255,255,255" bufferDraw="0" bufferBlendMode="0" bufferTransp="0" bufferSizeInMapUnits="0" bufferSizeMapUnitMaxScale="0" bufferNoFill="0" bufferJoinStyle="64"/>
          <background shapeSizeUnits="1" shapeType="0" shapeOffsetMapUnitMinScale="0" shapeSizeMapUnitMinScale="0" shapeSVGFile="" shapeOffsetX="0" shapeOffsetY="0" shapeBlendMode="0" shapeBorderWidthMapUnitMaxScale="0" shapeFillColor="255,255,255,255" shapeTransparency="0" shapeSizeType="0" shapeJoinStyle="64" shapeDraw="0" shapeSizeMapUnitMaxScale="0" shapeBorderWidthUnits="1" shapeSizeX="0" shapeSizeY="0" shapeRadiiX="0" shapeOffsetMapUnitMaxScale="0" shapeOffsetUnits="1" shapeRadiiY="0" shapeRotation="0" shapeBorderWidth="0" shapeRadiiMapUnitMinScale="0" shapeRadiiMapUnitMaxScale="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeRadiiUnits="1" shapeBorderWidthMapUnitMinScale="0"/>
          <shadow shadowOffsetGlobal="1" shadowRadiusUnits="1" shadowRadiusMapUnitMinScale="0" shadowTransparency="30" shadowColor="0,0,0,255" shadowUnder="0" shadowScale="100" shadowOffsetDist="1" shadowOffsetMapUnitMinScale="0" shadowRadiusMapUnitMaxScale="0" shadowDraw="0" shadowOffsetAngle="135" shadowRadius="1.5" shadowBlendMode="6" shadowOffsetMapUnitMaxScale="0" shadowRadiusAlphaOnly="0" shadowOffsetUnits="1"/>
          <placement repeatDistanceUnit="1" placement="1" maxCurvedCharAngleIn="20" repeatDistance="0" distMapUnitMaxScale="0" labelOffsetMapUnitMaxScale="0" distInMapUnits="0" labelOffsetInMapUnits="1" xOffset="0" preserveRotation="1" centroidWhole="0" priority="5" repeatDistanceMapUnitMaxScale="0" yOffset="0" placementFlags="10" repeatDistanceMapUnitMinScale="0" centroidInside="0" dist="0" angleOffset="0" maxCurvedCharAngleOut="-20" fitInPolygonOnly="0" quadOffset="1" distMapUnitMinScale="0" labelOffsetMapUnitMinScale="0"/>
          <rendering fontMinPixelSize="3" scaleMax="10000000" fontMaxPixelSize="10000" scaleMin="1" upsidedownLabels="0" limitNumLabels="0" obstacle="1" obstacleFactor="1" scaleVisibility="0" fontLimitPixelSize="0" mergeLines="0" obstacleType="0" labelPerPart="0" maxNumLabels="2000" displayAll="0" minFeatureSize="0"/>
          <data-defined/>
        </settings>
      </rule>
      <rule description="Underside Level" filter="category = 'lvu'">
        <settings>
          <text-style fontItalic="0" fontFamily="Gill Sans" fontLetterSpacing="0" fontUnderline="0" fontSizeMapUnitMaxScale="0" fontWeight="50" fontStrikeout="0" textTransp="0" previewBkgrdColor="#ffffff" fontCapitals="0" textColor="0,0,0,255" fontSizeMapUnitMinScale="0" fontSizeInMapUnits="0" isExpression="0" blendMode="0" fontSize="10" fieldName="elevation" namedStyle="Regular" fontWordSpacing="0"/>
          <text-format placeDirectionSymbol="0" multilineAlign="0" rightDirectionSymbol=">" multilineHeight="1" plussign="0" addDirectionSymbol="0" leftDirectionSymbol="&lt;" formatNumbers="1" decimals="2" wrapChar="" reverseDirectionSymbol="0"/>
          <text-buffer bufferSize="1" bufferSizeMapUnitMinScale="0" bufferColor="255,255,255,255" bufferDraw="0" bufferBlendMode="0" bufferTransp="0" bufferSizeInMapUnits="0" bufferSizeMapUnitMaxScale="0" bufferNoFill="0" bufferJoinStyle="64"/>
          <background shapeSizeUnits="1" shapeType="0" shapeOffsetMapUnitMinScale="0" shapeSizeMapUnitMinScale="0" shapeSVGFile="" shapeOffsetX="0" shapeOffsetY="0" shapeBlendMode="0" shapeBorderWidthMapUnitMaxScale="0" shapeFillColor="255,255,255,255" shapeTransparency="0" shapeSizeType="0" shapeJoinStyle="64" shapeDraw="0" shapeSizeMapUnitMaxScale="0" shapeBorderWidthUnits="1" shapeSizeX="0" shapeSizeY="0" shapeRadiiX="0" shapeOffsetMapUnitMaxScale="0" shapeOffsetUnits="1" shapeRadiiY="0" shapeRotation="0" shapeBorderWidth="0" shapeRadiiMapUnitMinScale="0" shapeRadiiMapUnitMaxScale="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeRadiiUnits="1" shapeBorderWidthMapUnitMinScale="0"/>
          <shadow shadowOffsetGlobal="1" shadowRadiusUnits="1" shadowRadiusMapUnitMinScale="0" shadowTransparency="30" shadowColor="0,0,0,255" shadowUnder="0" shadowScale="100" shadowOffsetDist="1" shadowOffsetMapUnitMinScale="0" shadowRadiusMapUnitMaxScale="0" shadowDraw="0" shadowOffsetAngle="135" shadowRadius="1.5" shadowBlendMode="6" shadowOffsetMapUnitMaxScale="0" shadowRadiusAlphaOnly="0" shadowOffsetUnits="1"/>
          <placement repeatDistanceUnit="1" placement="1" maxCurvedCharAngleIn="20" repeatDistance="0" distMapUnitMaxScale="0" labelOffsetMapUnitMaxScale="0" distInMapUnits="0" labelOffsetInMapUnits="1" xOffset="0" preserveRotation="1" centroidWhole="0" priority="5" repeatDistanceMapUnitMaxScale="0" yOffset="0" placementFlags="10" repeatDistanceMapUnitMinScale="0" centroidInside="0" dist="0" angleOffset="0" maxCurvedCharAngleOut="-20" fitInPolygonOnly="0" quadOffset="7" distMapUnitMinScale="0" labelOffsetMapUnitMinScale="0"/>
          <rendering fontMinPixelSize="3" scaleMax="10000000" fontMaxPixelSize="10000" scaleMin="1" upsidedownLabels="0" limitNumLabels="0" obstacle="1" obstacleFactor="1" scaleVisibility="0" fontLimitPixelSize="0" mergeLines="0" obstacleType="0" labelPerPart="0" maxNumLabels="2000" displayAll="0" minFeatureSize="0"/>
          <data-defined/>
        </settings>
      </rule>
      <rule description="Section Pin" filter="category = 'sec'">
        <settings>
          <text-style fontItalic="0" fontFamily="Gill Sans" fontLetterSpacing="0" fontUnderline="0" fontSizeMapUnitMaxScale="0" fontWeight="50" fontStrikeout="0" textTransp="0" previewBkgrdColor="#ffffff" fontCapitals="0" textColor="0,0,0,255" fontSizeMapUnitMinScale="0" fontSizeInMapUnits="0" isExpression="0" blendMode="0" fontSize="10" fieldName="elevation" namedStyle="Regular" fontWordSpacing="0"/>
          <text-format placeDirectionSymbol="0" multilineAlign="0" rightDirectionSymbol=">" multilineHeight="1" plussign="0" addDirectionSymbol="0" leftDirectionSymbol="&lt;" formatNumbers="1" decimals="2" wrapChar="" reverseDirectionSymbol="0"/>
          <text-buffer bufferSize="1" bufferSizeMapUnitMinScale="0" bufferColor="255,255,255,255" bufferDraw="0" bufferBlendMode="0" bufferTransp="0" bufferSizeInMapUnits="0" bufferSizeMapUnitMaxScale="0" bufferNoFill="0" bufferJoinStyle="64"/>
          <background shapeSizeUnits="1" shapeType="0" shapeOffsetMapUnitMinScale="0" shapeSizeMapUnitMinScale="0" shapeSVGFile="" shapeOffsetX="0" shapeOffsetY="0" shapeBlendMode="0" shapeBorderWidthMapUnitMaxScale="0" shapeFillColor="255,255,255,255" shapeTransparency="0" shapeSizeType="0" shapeJoinStyle="64" shapeDraw="0" shapeSizeMapUnitMaxScale="0" shapeBorderWidthUnits="1" shapeSizeX="0" shapeSizeY="0" shapeRadiiX="0" shapeOffsetMapUnitMaxScale="0" shapeOffsetUnits="1" shapeRadiiY="0" shapeRotation="0" shapeBorderWidth="0" shapeRadiiMapUnitMinScale="0" shapeRadiiMapUnitMaxScale="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeRadiiUnits="1" shapeBorderWidthMapUnitMinScale="0"/>
          <shadow shadowOffsetGlobal="1" shadowRadiusUnits="1" shadowRadiusMapUnitMinScale="0" shadowTransparency="30" shadowColor="0,0,0,255" shadowUnder="0" shadowScale="100" shadowOffsetDist="1" shadowOffsetMapUnitMinScale="0" shadowRadiusMapUnitMaxScale="0" shadowDraw="0" shadowOffsetAngle="135" shadowRadius="1.5" shadowBlendMode="6" shadowOffsetMapUnitMaxScale="0" shadowRadiusAlphaOnly="0" shadowOffsetUnits="1"/>
          <placement repeatDistanceUnit="1" placement="1" maxCurvedCharAngleIn="20" repeatDistance="0" distMapUnitMaxScale="0" labelOffsetMapUnitMaxScale="0" distInMapUnits="0" labelOffsetInMapUnits="0" xOffset="0" preserveRotation="1" centroidWhole="0" priority="5" repeatDistanceMapUnitMaxScale="0" yOffset="-1" placementFlags="10" repeatDistanceMapUnitMinScale="0" centroidInside="0" dist="0" angleOffset="0" maxCurvedCharAngleOut="-20" fitInPolygonOnly="0" quadOffset="1" distMapUnitMinScale="0" labelOffsetMapUnitMinScale="0"/>
          <rendering fontMinPixelSize="3" scaleMax="10000000" fontMaxPixelSize="10000" scaleMin="1" upsidedownLabels="0" limitNumLabels="0" obstacle="1" obstacleFactor="1" scaleVisibility="0" fontLimitPixelSize="0" mergeLines="0" obstacleType="0" labelPerPart="0" maxNumLabels="2000" displayAll="0" minFeatureSize="0"/>
          <data-defined/>
        </settings>
      </rule>
      <rule description="Special Find" filter="category = 'spf'">
        <settings>
          <text-style fontItalic="0" fontFamily="Gill Sans" fontLetterSpacing="0" fontUnderline="0" fontSizeMapUnitMaxScale="0" fontWeight="50" fontStrikeout="0" textTransp="0" previewBkgrdColor="#ffffff" fontCapitals="0" textColor="0,0,0,255" fontSizeMapUnitMinScale="0" fontSizeInMapUnits="0" isExpression="0" blendMode="0" fontSize="10" fieldName="item_no" namedStyle="Regular" fontWordSpacing="0"/>
          <text-format placeDirectionSymbol="0" multilineAlign="0" rightDirectionSymbol=">" multilineHeight="1" plussign="0" addDirectionSymbol="0" leftDirectionSymbol="&lt;" formatNumbers="0" decimals="3" wrapChar="" reverseDirectionSymbol="0"/>
          <text-buffer bufferSize="1" bufferSizeMapUnitMinScale="0" bufferColor="255,255,255,255" bufferDraw="0" bufferBlendMode="0" bufferTransp="0" bufferSizeInMapUnits="0" bufferSizeMapUnitMaxScale="0" bufferNoFill="0" bufferJoinStyle="64"/>
          <background shapeSizeUnits="1" shapeType="0" shapeOffsetMapUnitMinScale="0" shapeSizeMapUnitMinScale="0" shapeSVGFile="" shapeOffsetX="0" shapeOffsetY="0" shapeBlendMode="0" shapeBorderWidthMapUnitMaxScale="0" shapeFillColor="255,255,255,255" shapeTransparency="0" shapeSizeType="0" shapeJoinStyle="64" shapeDraw="0" shapeSizeMapUnitMaxScale="0" shapeBorderWidthUnits="1" shapeSizeX="0" shapeSizeY="0" shapeRadiiX="0" shapeOffsetMapUnitMaxScale="0" shapeOffsetUnits="1" shapeRadiiY="0" shapeRotation="0" shapeBorderWidth="0" shapeRadiiMapUnitMinScale="0" shapeRadiiMapUnitMaxScale="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeRadiiUnits="1" shapeBorderWidthMapUnitMinScale="0"/>
          <shadow shadowOffsetGlobal="1" shadowRadiusUnits="1" shadowRadiusMapUnitMinScale="0" shadowTransparency="30" shadowColor="0,0,0,255" shadowUnder="0" shadowScale="100" shadowOffsetDist="1" shadowOffsetMapUnitMinScale="0" shadowRadiusMapUnitMaxScale="0" shadowDraw="0" shadowOffsetAngle="135" shadowRadius="1.5" shadowBlendMode="6" shadowOffsetMapUnitMaxScale="0" shadowRadiusAlphaOnly="0" shadowOffsetUnits="1"/>
          <placement repeatDistanceUnit="1" placement="1" maxCurvedCharAngleIn="20" repeatDistance="0" distMapUnitMaxScale="0" labelOffsetMapUnitMaxScale="0" distInMapUnits="0" labelOffsetInMapUnits="0" xOffset="0" preserveRotation="1" centroidWhole="0" priority="5" repeatDistanceMapUnitMaxScale="0" yOffset="-2" placementFlags="10" repeatDistanceMapUnitMinScale="0" centroidInside="0" dist="0" angleOffset="0" maxCurvedCharAngleOut="-20" fitInPolygonOnly="0" quadOffset="1" distMapUnitMinScale="0" labelOffsetMapUnitMinScale="0"/>
          <rendering fontMinPixelSize="3" scaleMax="10000000" fontMaxPixelSize="10000" scaleMin="1" upsidedownLabels="0" limitNumLabels="0" obstacle="1" obstacleFactor="1" scaleVisibility="0" fontLimitPixelSize="0" mergeLines="0" obstacleType="0" labelPerPart="0" maxNumLabels="2000" displayAll="0" minFeatureSize="0"/>
          <data-defined/>
        </settings>
      </rule>
      <rule description="Name" filter="name IS NOT NULL and (category IS NULL or category NOT IN ('lvl', 'lvu', 'sec', 'spf'))">
        <settings>
          <text-style fontItalic="0" fontFamily="Gill Sans" fontLetterSpacing="0" fontUnderline="0" fontSizeMapUnitMaxScale="0" fontWeight="50" fontStrikeout="0" textTransp="0" previewBkgrdColor="#ffffff" fontCapitals="0" textColor="0,0,0,255" fontSizeMapUnitMinScale="0" fontSizeInMapUnits="0" isExpression="0" blendMode="0" fontSize="10" fieldName="name" namedStyle="Regular" fontWordSpacing="0"/>
          <text-format placeDirectionSymbol="0" multilineAlign="0" rightDirectionSymbol=">" multilineHeight="1" plussign="0" addDirectionSymbol="0" leftDirectionSymbol="&lt;" formatNumbers="0" decimals="3" wrapChar="" reverseDirectionSymbol="0"/>
          <text-buffer bufferSize="1" bufferSizeMapUnitMinScale="0" bufferColor="255,255,255,255" bufferDraw="0" bufferBlendMode="0" bufferTransp="0" bufferSizeInMapUnits="0" bufferSizeMapUnitMaxScale="0" bufferNoFill="0" bufferJoinStyle="64"/>
          <background shapeSizeUnits="1" shapeType="0" shapeOffsetMapUnitMinScale="0" shapeSizeMapUnitMinScale="0" shapeSVGFile="" shapeOffsetX="0" shapeOffsetY="0" shapeBlendMode="0" shapeBorderWidthMapUnitMaxScale="0" shapeFillColor="255,255,255,255" shapeTransparency="0" shapeSizeType="0" shapeJoinStyle="64" shapeDraw="0" shapeSizeMapUnitMaxScale="0" shapeBorderWidthUnits="1" shapeSizeX="0" shapeSizeY="0" shapeRadiiX="0" shapeOffsetMapUnitMaxScale="0" shapeOffsetUnits="1" shapeRadiiY="0" shapeRotation="0" shapeBorderWidth="0" shapeRadiiMapUnitMinScale="0" shapeRadiiMapUnitMaxScale="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeRadiiUnits="1" shapeBorderWidthMapUnitMinScale="0"/>
          <shadow shadowOffsetGlobal="1" shadowRadiusUnits="1" shadowRadiusMapUnitMinScale="0" shadowTransparency="30" shadowColor="0,0,0,255" shadowUnder="0" shadowScale="100" shadowOffsetDist="1" shadowOffsetMapUnitMinScale="0" shadowRadiusMapUnitMaxScale="0" shadowDraw="0" shadowOffsetAngle="135" shadowRadius="1.5" shadowBlendMode="6" shadowOffsetMapUnitMaxScale="0" shadowRadiusAlphaOnly="0" shadowOffsetUnits="1"/>
          <placement repeatDistanceUnit="1" placement="1" maxCurvedCharAngleIn="20" repeatDistance="0" distMapUnitMaxScale="0" labelOffsetMapUnitMaxScale="0" distInMapUnits="0" labelOffsetInMapUnits="1" xOffset="0" preserveRotation="1" centroidWhole="0" priority="5" repeatDistanceMapUnitMaxScale="0" yOffset="0" placementFlags="10" repeatDistanceMapUnitMinScale="0" centroidInside="0" dist="0" angleOffset="0" maxCurvedCharAngleOut="-20" fitInPolygonOnly="0" quadOffset="1" distMapUnitMinScale="0" labelOffsetMapUnitMinScale="0"/>
          <rendering fontMinPixelSize="3" scaleMax="10000000" fontMaxPixelSize="10000" scaleMin="1" upsidedownLabels="0" limitNumLabels="0" obstacle="1" obstacleFactor="1" scaleVisibility="0" fontLimitPixelSize="0" mergeLines="0" obstacleType="0" labelPerPart="0" maxNumLabels="2000" displayAll="0" minFeatureSize="0"/>
          <data-defined/>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <property key="labeling/addDirectionSymbol" value="false"/>
    <property key="labeling/angleOffset" value="1"/>
    <property key="labeling/blendMode" value="0"/>
    <property key="labeling/bufferBlendMode" value="0"/>
    <property key="labeling/bufferColorA" value="255"/>
    <property key="labeling/bufferColorB" value="255"/>
    <property key="labeling/bufferColorG" value="255"/>
    <property key="labeling/bufferColorR" value="255"/>
    <property key="labeling/bufferDraw" value="false"/>
    <property key="labeling/bufferJoinStyle" value="64"/>
    <property key="labeling/bufferNoFill" value="false"/>
    <property key="labeling/bufferSize" value="1"/>
    <property key="labeling/bufferSizeInMapUnits" value="false"/>
    <property key="labeling/bufferSizeMapUnitMaxScale" value="0"/>
    <property key="labeling/bufferSizeMapUnitMinScale" value="0"/>
    <property key="labeling/bufferTransp" value="0"/>
    <property key="labeling/centroidInside" value="false"/>
    <property key="labeling/centroidWhole" value="false"/>
    <property key="labeling/decimals" value="2"/>
    <property key="labeling/displayAll" value="false"/>
    <property key="labeling/dist" value="0"/>
    <property key="labeling/distInMapUnits" value="false"/>
    <property key="labeling/distMapUnitMaxScale" value="0"/>
    <property key="labeling/distMapUnitMinScale" value="0"/>
    <property key="labeling/drawLabels" value="true"/>
    <property key="labeling/enabled" value="true"/>
    <property key="labeling/fieldName" value="CASE&#xa;    WHEN &quot;category&quot; = 'lvl' THEN format_number(&quot;elevation&quot;,2)&#xa;    WHEN &quot;category&quot; = 'llv' THEN format_number(&quot;elevation&quot;,2)&#xa;    WHEN &quot;category&quot; ='sec' THEN format_number(&quot;elevation&quot;,2)&#xa;    WHEN &quot;category&quot; ='spf' THEN  &quot;item_no&quot;&#xa;    WHEN &quot;name&quot; IS NOT NULL THEN &quot;name&quot;&#xa;&#x9;ELSE ' ' &#xa;END"/>
    <property key="labeling/fitInPolygonOnly" value="false"/>
    <property key="labeling/fontBold" value="false"/>
    <property key="labeling/fontCapitals" value="0"/>
    <property key="labeling/fontFamily" value="Gill Sans"/>
    <property key="labeling/fontItalic" value="false"/>
    <property key="labeling/fontLetterSpacing" value="0"/>
    <property key="labeling/fontLimitPixelSize" value="false"/>
    <property key="labeling/fontMaxPixelSize" value="10000"/>
    <property key="labeling/fontMinPixelSize" value="3"/>
    <property key="labeling/fontSize" value="10"/>
    <property key="labeling/fontSizeInMapUnits" value="false"/>
    <property key="labeling/fontSizeMapUnitMaxScale" value="0"/>
    <property key="labeling/fontSizeMapUnitMinScale" value="0"/>
    <property key="labeling/fontStrikeout" value="false"/>
    <property key="labeling/fontUnderline" value="false"/>
    <property key="labeling/fontWeight" value="50"/>
    <property key="labeling/fontWordSpacing" value="0"/>
    <property key="labeling/formatNumbers" value="false"/>
    <property key="labeling/isExpression" value="true"/>
    <property key="labeling/labelOffsetInMapUnits" value="false"/>
    <property key="labeling/labelOffsetMapUnitMaxScale" value="0"/>
    <property key="labeling/labelOffsetMapUnitMinScale" value="0"/>
    <property key="labeling/labelPerPart" value="false"/>
    <property key="labeling/leftDirectionSymbol" value="&lt;"/>
    <property key="labeling/limitNumLabels" value="false"/>
    <property key="labeling/maxCurvedCharAngleIn" value="20"/>
    <property key="labeling/maxCurvedCharAngleOut" value="-20"/>
    <property key="labeling/maxNumLabels" value="2000"/>
    <property key="labeling/mergeLines" value="false"/>
    <property key="labeling/minFeatureSize" value="0"/>
    <property key="labeling/multilineAlign" value="0"/>
    <property key="labeling/multilineHeight" value="1"/>
    <property key="labeling/namedStyle" value="Regular"/>
    <property key="labeling/obstacle" value="true"/>
    <property key="labeling/obstacleFactor" value="1"/>
    <property key="labeling/obstacleType" value="0"/>
    <property key="labeling/placeDirectionSymbol" value="0"/>
    <property key="labeling/placement" value="1"/>
    <property key="labeling/placementFlags" value="0"/>
    <property key="labeling/plussign" value="false"/>
    <property key="labeling/preserveRotation" value="true"/>
    <property key="labeling/previewBkgrdColor" value="#ffffff"/>
    <property key="labeling/priority" value="5"/>
    <property key="labeling/quadOffset" value="1"/>
    <property key="labeling/repeatDistance" value="0"/>
    <property key="labeling/repeatDistanceMapUnitMaxScale" value="0"/>
    <property key="labeling/repeatDistanceMapUnitMinScale" value="0"/>
    <property key="labeling/repeatDistanceUnit" value="1"/>
    <property key="labeling/reverseDirectionSymbol" value="false"/>
    <property key="labeling/rightDirectionSymbol" value=">"/>
    <property key="labeling/scaleMax" value="10000000"/>
    <property key="labeling/scaleMin" value="1"/>
    <property key="labeling/scaleVisibility" value="false"/>
    <property key="labeling/shadowBlendMode" value="6"/>
    <property key="labeling/shadowColorB" value="0"/>
    <property key="labeling/shadowColorG" value="0"/>
    <property key="labeling/shadowColorR" value="0"/>
    <property key="labeling/shadowDraw" value="false"/>
    <property key="labeling/shadowOffsetAngle" value="135"/>
    <property key="labeling/shadowOffsetDist" value="1"/>
    <property key="labeling/shadowOffsetGlobal" value="true"/>
    <property key="labeling/shadowOffsetMapUnitMaxScale" value="0"/>
    <property key="labeling/shadowOffsetMapUnitMinScale" value="0"/>
    <property key="labeling/shadowOffsetUnits" value="1"/>
    <property key="labeling/shadowRadius" value="1.5"/>
    <property key="labeling/shadowRadiusAlphaOnly" value="false"/>
    <property key="labeling/shadowRadiusMapUnitMaxScale" value="0"/>
    <property key="labeling/shadowRadiusMapUnitMinScale" value="0"/>
    <property key="labeling/shadowRadiusUnits" value="1"/>
    <property key="labeling/shadowScale" value="100"/>
    <property key="labeling/shadowTransparency" value="30"/>
    <property key="labeling/shadowUnder" value="0"/>
    <property key="labeling/shapeBlendMode" value="0"/>
    <property key="labeling/shapeBorderColorA" value="255"/>
    <property key="labeling/shapeBorderColorB" value="128"/>
    <property key="labeling/shapeBorderColorG" value="128"/>
    <property key="labeling/shapeBorderColorR" value="128"/>
    <property key="labeling/shapeBorderWidth" value="0"/>
    <property key="labeling/shapeBorderWidthMapUnitMaxScale" value="0"/>
    <property key="labeling/shapeBorderWidthMapUnitMinScale" value="0"/>
    <property key="labeling/shapeBorderWidthUnits" value="1"/>
    <property key="labeling/shapeDraw" value="false"/>
    <property key="labeling/shapeFillColorA" value="255"/>
    <property key="labeling/shapeFillColorB" value="255"/>
    <property key="labeling/shapeFillColorG" value="255"/>
    <property key="labeling/shapeFillColorR" value="255"/>
    <property key="labeling/shapeJoinStyle" value="64"/>
    <property key="labeling/shapeOffsetMapUnitMaxScale" value="0"/>
    <property key="labeling/shapeOffsetMapUnitMinScale" value="0"/>
    <property key="labeling/shapeOffsetUnits" value="1"/>
    <property key="labeling/shapeOffsetX" value="0"/>
    <property key="labeling/shapeOffsetY" value="0"/>
    <property key="labeling/shapeRadiiMapUnitMaxScale" value="0"/>
    <property key="labeling/shapeRadiiMapUnitMinScale" value="0"/>
    <property key="labeling/shapeRadiiUnits" value="1"/>
    <property key="labeling/shapeRadiiX" value="0"/>
    <property key="labeling/shapeRadiiY" value="0"/>
    <property key="labeling/shapeRotation" value="0"/>
    <property key="labeling/shapeRotationType" value="0"/>
    <property key="labeling/shapeSVGFile" value=""/>
    <property key="labeling/shapeSizeMapUnitMaxScale" value="0"/>
    <property key="labeling/shapeSizeMapUnitMinScale" value="0"/>
    <property key="labeling/shapeSizeType" value="0"/>
    <property key="labeling/shapeSizeUnits" value="1"/>
    <property key="labeling/shapeSizeX" value="0"/>
    <property key="labeling/shapeSizeY" value="0"/>
    <property key="labeling/shapeTransparency" value="0"/>
    <property key="labeling/shapeType" value="0"/>
    <property key="labeling/textColorA" value="255"/>
    <property key="labeling/textColorB" value="0"/>
    <property key="labeling/textColorG" value="0"/>
    <property key="labeling/textColorR" value="0"/>
    <property key="labeling/textTransp" value="0"/>
    <property key="labeling/upsidedownLabels" value="0"/>
    <property key="labeling/wrapChar" value=""/>
    <property key="labeling/xOffset" value="0"/>
    <property key="labeling/yOffset" value="0"/>
    <property key="variableNames" value="_fields_"/>
    <property key="variableValues" value=""/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerTransparency>0</layerTransparency>
  <displayfield>elev</displayfield>
  <label>0</label>
  <labelattributes>
    <label fieldname="" text="Label"/>
    <family fieldname="" name=".Lucida Grande UI"/>
    <size fieldname="" units="pt" value="12"/>
    <bold fieldname="" on="0"/>
    <italic fieldname="" on="0"/>
    <underline fieldname="" on="0"/>
    <strikeout fieldname="" on="0"/>
    <color fieldname="" red="0" blue="0" green="0"/>
    <x fieldname=""/>
    <y fieldname=""/>
    <offset x="0" y="0" units="pt" yfieldname="" xfieldname=""/>
    <angle fieldname="" value="0" auto="0"/>
    <alignment fieldname="" value="center"/>
    <buffercolor fieldname="" red="255" blue="255" green="255"/>
    <buffersize fieldname="" units="pt" value="1"/>
    <bufferenabled fieldname="" on=""/>
    <multilineenabled fieldname="" on=""/>
    <selectedonly on=""/>
  </labelattributes>
  <SingleCategoryDiagramRenderer diagramType="Pie">
    <DiagramCategory penColor="#000000" labelPlacementMethod="XHeight" penWidth="0" diagramOrientation="Up" minimumSize="0" barWidth="5" penAlpha="255" maxScaleDenominator="1e+08" backgroundColor="#ffffff" transparency="0" width="15" scaleDependency="Area" backgroundAlpha="255" angleOffset="1440" scaleBasedVisibility="0" enabled="0" height="15" sizeType="MM" minScaleDenominator="0">
      <fontProperties description=".Helvetica Neue DeskInterface,13,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings yPosColumn="-1" linePlacementFlags="10" placement="0" dist="0" xPosColumn="-1" priority="0" obstacle="0" showAll="1"/>
  <editform>.</editform>
  <editforminit/>
  <featformsuppress>0</featformsuppress>
  <annotationform>.</annotationform>
  <editorlayout>generatedlayout</editorlayout>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <attributeactions/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
</qgis>
