<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<imaer:FeatureCollectionCalculator xmlns:imaer="http://imaer.aerius.nl/0.5" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" gml:id="NL.IMAER.Collection" xsi:schemaLocation="http://imaer.aerius.nl/0.5 http://imaer.aerius.nl/0.5/IMAER.xsd">
    <imaer:aeriusCalculatorMetaData>
        <imaer:year>2015</imaer:year>
        <imaer:version>BETA12_20150617_f926129777</imaer:version>
        <imaer:databaseVersion>BETA12_20150611_86d2118008</imaer:databaseVersion>
        <imaer:situationName>Situation 1</imaer:situationName>
    </imaer:aeriusCalculatorMetaData>
    <imaer:featureMembers>
        <imaer:EmissionSource sectorId="2100" gml:id="ES.1">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>ES.1</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:label>Source 1</imaer:label>
            <imaer:emissionSourceCharacteristics>
                <imaer:EmissionSourceCharacteristics>
                    <imaer:heatContent>0.22</imaer:heatContent>
                    <imaer:emissionHeight>40.0</imaer:emissionHeight>
                    <imaer:diurnalVariation>INDUSTRIAL_ACTIVITY</imaer:diurnalVariation>
                </imaer:EmissionSourceCharacteristics>
            </imaer:emissionSourceCharacteristics>
            <imaer:geometry>
                <imaer:EmissionSourceGeometry>
                    <imaer:GM_Point>
                        <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="ES.1.POINT">
                            <gml:pos>148094.44 411614.7</gml:pos>
                        </gml:Point>
                    </imaer:GM_Point>
                </imaer:EmissionSourceGeometry>
            </imaer:geometry>
            <imaer:emission>
                <imaer:Emission substance="NH3">
                    <imaer:value>300.0</imaer:value>
                </imaer:Emission>
            </imaer:emission>
            <imaer:emission>
                <imaer:Emission substance="NOX">
                    <imaer:value>1000.0</imaer:value>
                </imaer:Emission>
            </imaer:emission>
            <imaer:emission>
                <imaer:Emission substance="PM10">
                    <imaer:value>10000.0</imaer:value>
                </imaer:Emission>
            </imaer:emission>
            <imaer:emission>
                <imaer:Emission substance="NO2">
                    <imaer:value>0.0</imaer:value>
                </imaer:Emission>
            </imaer:emission>
        </imaer:EmissionSource>
        <imaer:ReceptorPoint receptorPointId="3204036" gml:id="CP.3204036">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.3204036</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.3204036.POINT">
                    <gml:pos>148871.0 409361.0</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.3204036">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>148902.0 409415.0 148933.0 409361.0 148902.0 409307.0 148840.0 409307.0 148809.0 409361.0 148840.0 409415.0 148902.0 409415.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:Result resultType="DEPOSITION" substance="NH3">
                    <imaer:value>0.0502</imaer:value>
                </imaer:Result>
            </imaer:result>
        </imaer:ReceptorPoint>
        <imaer:ReceptorPoint receptorPointId="3251421" gml:id="CP.3251421">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.3251421</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.3251421.POINT">
                    <gml:pos>146173.0 411027.0</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.3251421">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>146204.0 411081.0 146235.0 411027.0 146204.0 410973.0 146142.0 410973.0 146111.0 411027.0 146142.0 411081.0 146204.0 411081.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:Result resultType="DEPOSITION" substance="NH3">
                    <imaer:value>0.0942</imaer:value>
                </imaer:Result>
            </imaer:result>
        </imaer:ReceptorPoint>
        <imaer:ReceptorPoint receptorPointId="3217800" gml:id="CP.3217800">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.3217800</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.3217800.POINT">
                    <gml:pos>149337.0 409845.0</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.3217800">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>149368.0 409898.0 149399.0 409845.0 149368.0 409791.0 149306.0 409791.0 149275.0 409845.0 149306.0 409898.0 149368.0 409898.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:Result resultType="DEPOSITION" substance="NH3">
                    <imaer:value>3.128E-4</imaer:value>
                </imaer:Result>
            </imaer:result>
        </imaer:ReceptorPoint>
        <imaer:ReceptorPoint receptorPointId="3204040" gml:id="CP.3204040">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.3204040</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.3204040.POINT">
                    <gml:pos>149616.0 409361.0</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.3204040">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>149647.0 409415.0 149678.0 409361.0 149647.0 409307.0 149585.0 409307.0 149554.0 409361.0 149585.0 409415.0 149647.0 409415.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:Result resultType="DEPOSITION" substance="NH3">
                    <imaer:value>0.0503</imaer:value>
                </imaer:Result>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMembers>
</imaer:FeatureCollectionCalculator>
