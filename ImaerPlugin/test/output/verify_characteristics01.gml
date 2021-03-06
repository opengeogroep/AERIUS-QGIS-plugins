<?xml version="1.0" ?>
<imaer:FeatureCollectionCalculator gml:id="NL.IMAER.Collection" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:imaer="http://imaer.aerius.nl/3.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://imaer.aerius.nl/3.1 http://imaer.aerius.nl/3.1/IMAER.xsd">
  <imaer:metadata/>
  <imaer:featureMember>
    <imaer:EmissionSource gml:id="ES.123" sectorId="9999">
      <imaer:identifier>
        <imaer:NEN3610ID>
          <imaer:namespace>NL.IMAER</imaer:namespace>
          <imaer:localId>ES.123</imaer:localId>
        </imaer:NEN3610ID>
      </imaer:identifier>
      <imaer:label>Bron 123</imaer:label>
      <imaer:emissionSourceCharacteristics>
        <imaer:EmissionSourceCharacteristics>
          <imaer:heatContent>
            <imaer:SpecifiedHeatContent>
              <imaer:value>12.5</imaer:value>
            </imaer:SpecifiedHeatContent>
          </imaer:heatContent>
          <imaer:emissionHeight>2.4</imaer:emissionHeight>
          <imaer:diurnalVariation>CONTINUOUS</imaer:diurnalVariation>
        </imaer:EmissionSourceCharacteristics>
      </imaer:emissionSourceCharacteristics>
      <imaer:geometry>
        <imaer:EmissionSourceGeometry>
          <imaer:GM_Curve>
            <gml:LineString gml:id="ES.123.CURVE" srsName="urn:ogc:def:crs:EPSG::28992">
              <gml:posList>1.0 0.0 2.0 1.0 3.0 0.0</gml:posList>
            </gml:LineString>
          </imaer:GM_Curve>
        </imaer:EmissionSourceGeometry>
      </imaer:geometry>
      <imaer:emission>
        <imaer:Emission substance="NH3">
          <imaer:value>1</imaer:value>
        </imaer:Emission>
      </imaer:emission>
      <imaer:emission>
        <imaer:Emission substance="NOX">
          <imaer:value>3.3</imaer:value>
        </imaer:Emission>
      </imaer:emission>
    </imaer:EmissionSource>
  </imaer:featureMember>
</imaer:FeatureCollectionCalculator>
<!--Created using QGIS ImaerPlugin by OpenGeoGroep-->
