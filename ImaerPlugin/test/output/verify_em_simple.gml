<?xml version="1.0" ?>
<imaer:FeatureCollectionCalculator gml:id="NL.IMAER.Collection" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:imaer="http://imaer.aerius.nl/3.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://imaer.aerius.nl/3.1 http://imaer.aerius.nl/3.1/IMAER.xsd">
  <imaer:metadata/>
  <imaer:featureMember>
    <imaer:EmissionSource gml:id="ES.123" sectorId="9000">
      <imaer:identifier>
        <imaer:NEN3610ID>
          <imaer:namespace>NL.IMAER</imaer:namespace>
          <imaer:localId>ES.123</imaer:localId>
        </imaer:NEN3610ID>
      </imaer:identifier>
      <imaer:label>Bron 123</imaer:label>
      <imaer:geometry>
        <imaer:EmissionSourceGeometry>
          <imaer:GM_Point>
            <gml:Point gml:id="ES.123.POINT" srsName="urn:ogc:def:crs:EPSG::28992">
              <gml:pos>148458.0 411641.0</gml:pos>
            </gml:Point>
          </imaer:GM_Point>
        </imaer:EmissionSourceGeometry>
      </imaer:geometry>
      <imaer:emission>
        <imaer:Emission substance="NH3">
          <imaer:value>1</imaer:value>
        </imaer:Emission>
      </imaer:emission>
    </imaer:EmissionSource>
  </imaer:featureMember>
</imaer:FeatureCollectionCalculator>
<!--Created using QGIS ImaerPlugin by OpenGeoGroep-->
