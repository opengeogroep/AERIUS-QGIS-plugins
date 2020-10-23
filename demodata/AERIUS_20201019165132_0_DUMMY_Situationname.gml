<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<imaer:FeatureCollectionCalculator xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:imaer="http://imaer.aerius.nl/3.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="NL.IMAER.Collection" xsi:schemaLocation="http://imaer.aerius.nl/3.1 http://imaer.aerius.nl/3.1/IMAER.xsd">
    <imaer:metadata>
        <imaer:AeriusCalculatorMetadata>
            <imaer:project>
                <imaer:ProjectMetadata>
                    <imaer:year>2020</imaer:year>
                    <imaer:name>DUMMY_name</imaer:name>
                    <imaer:corporation>DUMMY_corporation</imaer:corporation>
                    <imaer:facilityLocation>
                        <imaer:Address>
                            <imaer:streetAddress>DUMMY_streetAdress</imaer:streetAddress>
                            <imaer:postcode>DUMMY_postcode</imaer:postcode>
                            <imaer:city>DUMMY_city</imaer:city>
                        </imaer:Address>
                    </imaer:facilityLocation>
                    <imaer:description>DUMMY_description</imaer:description>
                </imaer:ProjectMetadata>
            </imaer:project>
            <imaer:situation>
                <imaer:SituationMetadata>
                    <imaer:name>DUMMY_Situation-name</imaer:name>
                    <imaer:reference>RoG2T9svYHRB</imaer:reference>
                </imaer:SituationMetadata>
            </imaer:situation>
            <imaer:calculation>
                <imaer:CalculationMetadata>
                    <imaer:type>PERMIT</imaer:type>
                    <imaer:substance>NOX</imaer:substance>
                    <imaer:substance>NO2</imaer:substance>
                    <imaer:substance>NH3</imaer:substance>
                    <imaer:resultType>DEPOSITION</imaer:resultType>
                </imaer:CalculationMetadata>
            </imaer:calculation>
            <imaer:version>
                <imaer:VersionMetadata>
                    <imaer:aeriusVersion>2020_20201013_1649cba239</imaer:aeriusVersion>
                    <imaer:databaseVersion>2020_20201013_1649cba239</imaer:databaseVersion>
                </imaer:VersionMetadata>
            </imaer:version>
        </imaer:AeriusCalculatorMetadata>
    </imaer:metadata>
    <imaer:featureMember>
        <imaer:EmissionSource sectorId="1800" gml:id="ES.1">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>ES.1</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:label>Bron 1</imaer:label>
            <imaer:emissionSourceCharacteristics>
                <imaer:EmissionSourceCharacteristics>
                    <imaer:heatContent>
                        <imaer:SpecifiedHeatContent>
                            <imaer:value>0.0</imaer:value>
                        </imaer:SpecifiedHeatContent>
                    </imaer:heatContent>
                    <imaer:emissionHeight>5.0</imaer:emissionHeight>
                    <imaer:diurnalVariation>INDUSTRIAL_ACTIVITY</imaer:diurnalVariation>
                </imaer:EmissionSourceCharacteristics>
            </imaer:emissionSourceCharacteristics>
            <imaer:geometry>
                <imaer:EmissionSourceGeometry>
                    <imaer:GM_Point>
                        <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="ES.1.POINT">
                            <gml:pos>230574.46 477195.6</gml:pos>
                        </gml:Point>
                    </imaer:GM_Point>
                </imaer:EmissionSourceGeometry>
            </imaer:geometry>
            <imaer:emission>
                <imaer:Emission substance="NH3">
                    <imaer:value>0.0</imaer:value>
                </imaer:Emission>
            </imaer:emission>
            <imaer:emission>
                <imaer:Emission substance="NOX">
                    <imaer:value>10.0</imaer:value>
                </imaer:Emission>
            </imaer:emission>
            <imaer:emission>
                <imaer:Emission substance="PM10">
                    <imaer:value>0.0</imaer:value>
                </imaer:Emission>
            </imaer:emission>
            <imaer:emission>
                <imaer:Emission substance="NO2">
                    <imaer:value>0.0</imaer:value>
                </imaer:Emission>
            </imaer:emission>
        </imaer:EmissionSource>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5129486" gml:id="CP.5129486">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5129486</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5129486.POINT">
                    <gml:pos>230485.46464909188 477005.37756680796</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5129486">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230516.0 477059.0 230548.0 477005.0 230516.0 476952.0 230454.0 476952.0 230423.0 477005.0 230454.0 477059.0 230516.0 477059.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.04672</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5129487" gml:id="CP.5129487">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5129487</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5129487.POINT">
                    <gml:pos>230671.58562091232 477005.37756680796</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5129487">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230703.0 477059.0 230734.0 477005.0 230703.0 476952.0 230641.0 476952.0 230610.0 477005.0 230641.0 477059.0 230703.0 477059.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.04821</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5129485" gml:id="CP.5129485">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5129485</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5129485.POINT">
                    <gml:pos>230299.34367727148 477005.37756680796</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5129485">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230330.0 477059.0 230361.0 477005.0 230330.0 476952.0 230268.0 476952.0 230237.0 477005.0 230268.0 477059.0 230330.0 477059.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.02351</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5131016" gml:id="CP.5131016">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5131016</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5131016.POINT">
                    <gml:pos>230764.64610682253 477059.1060633991</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5131016">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230796.0 477113.0 230827.0 477059.0 230796.0 477005.0 230734.0 477005.0 230703.0 477059.0 230734.0 477113.0 230796.0 477113.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.04858</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5117254" gml:id="CP.5117254">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5117254</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5117254.POINT">
                    <gml:pos>230485.46464909188 476575.54959407856</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5117254">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230516.0 476629.0 230548.0 476576.0 230516.0 476522.0 230454.0 476522.0 230423.0 476576.0 230454.0 476629.0 230516.0 476629.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.005324</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5131014" gml:id="CP.5131014">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5131014</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5131014.POINT">
                    <gml:pos>230392.4041631817 477059.1060633991</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5131014">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230423.0 477113.0 230454.0 477059.0 230423.0 477005.0 230361.0 477005.0 230330.0 477059.0 230361.0 477113.0 230423.0 477113.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.04636</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5146310" gml:id="CP.5146310">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5146310</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5146310.POINT">
                    <gml:pos>231509.1299941042 477596.3910293109</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5146310">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>231540.0 477650.0 231571.0 477596.0 231540.0 477543.0 231478.0 477543.0 231447.0 477596.0 231478.0 477650.0 231540.0 477650.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.005515</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5117255" gml:id="CP.5117255">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5117255</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5117255.POINT">
                    <gml:pos>230671.58562091232 476575.54959407856</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5117255">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230703.0 476629.0 230734.0 476576.0 230703.0 476522.0 230641.0 476522.0 230610.0 476576.0 230641.0 476629.0 230703.0 476629.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.005634</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5131015" gml:id="CP.5131015">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5131015</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5131015.POINT">
                    <gml:pos>230578.5251350021 477059.1060633991</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5131015">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230610.0 477113.0 230641.0 477059.0 230610.0 477005.0 230548.0 477005.0 230516.0 477059.0 230548.0 477113.0 230610.0 477113.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.09877</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5132544" gml:id="CP.5132544">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5132544</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5132544.POINT">
                    <gml:pos>230485.46464909188 477112.8345599903</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5132544">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230516.0 477167.0 230548.0 477113.0 230516.0 477059.0 230454.0 477059.0 230423.0 477113.0 230454.0 477167.0 230516.0 477167.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.1232</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5132545" gml:id="CP.5132545">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5132545</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5132545.POINT">
                    <gml:pos>230671.58562091232 477112.8345599903</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5132545">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230703.0 477167.0 230734.0 477113.0 230703.0 477059.0 230641.0 477059.0 230610.0 477113.0 230641.0 477167.0 230703.0 477167.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.1426</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5126428" gml:id="CP.5126428">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5126428</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5126428.POINT">
                    <gml:pos>230485.46464909188 476897.9205736256</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5126428">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230516.0 476952.0 230548.0 476898.0 230516.0 476844.0 230454.0 476844.0 230423.0 476898.0 230454.0 476952.0 230516.0 476952.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.01973</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5127956" gml:id="CP.5127956">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5127956</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5127956.POINT">
                    <gml:pos>230392.4041631817 476951.6490702168</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5127956">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230423.0 477005.0 230454.0 476952.0 230423.0 476898.0 230361.0 476898.0 230330.0 476952.0 230361.0 477005.0 230423.0 477005.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.02511</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5127957" gml:id="CP.5127957">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5127957</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5127957.POINT">
                    <gml:pos>230578.5251350021 476951.6490702168</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5127957">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230610.0 477005.0 230641.0 476952.0 230610.0 476898.0 230548.0 476898.0 230516.0 476952.0 230548.0 477005.0 230610.0 477005.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.03183</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5121838" gml:id="CP.5121838">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5121838</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5121838.POINT">
                    <gml:pos>230020.16221954086 476736.7350838521</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5121838">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230051.0 476790.0 230082.0 476737.0 230051.0 476683.0 229989.0 476683.0 229958.0 476737.0 229989.0 476790.0 230051.0 476790.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.005406</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5121839" gml:id="CP.5121839">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5121839</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5121839.POINT">
                    <gml:pos>230206.28319136126 476736.7350838521</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5121839">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230237.0 476790.0 230268.0 476737.0 230237.0 476683.0 230175.0 476683.0 230144.0 476737.0 230175.0 476790.0 230237.0 476790.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.006802</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5123370" gml:id="CP.5123370">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5123370</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5123370.POINT">
                    <gml:pos>230485.46464909188 476790.4635804433</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5123370">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230516.0 476844.0 230548.0 476790.0 230516.0 476737.0 230454.0 476737.0 230423.0 476790.0 230454.0 476844.0 230516.0 476844.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.01161</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5123368" gml:id="CP.5123368">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5123368</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5123368.POINT">
                    <gml:pos>230113.22270545104 476790.4635804433</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5123368">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230144.0 476844.0 230175.0 476790.0 230144.0 476737.0 230082.0 476737.0 230051.0 476790.0 230082.0 476844.0 230144.0 476844.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.006952</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5123369" gml:id="CP.5123369">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5123369</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5123369.POINT">
                    <gml:pos>230299.34367727148 476790.4635804433</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5123369">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230330.0 476844.0 230361.0 476790.0 230330.0 476737.0 230268.0 476737.0 230237.0 476790.0 230268.0 476844.0 230330.0 476844.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.009058</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5124898" gml:id="CP.5124898">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5124898</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5124898.POINT">
                    <gml:pos>230392.4041631817 476844.19207703444</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5124898">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230423.0 476898.0 230454.0 476844.0 230423.0 476790.0 230361.0 476790.0 230330.0 476844.0 230361.0 476898.0 230423.0 476898.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.01298</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5124899" gml:id="CP.5124899">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5124899</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5124899.POINT">
                    <gml:pos>230578.5251350021 476844.19207703444</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5124899">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230610.0 476898.0 230641.0 476844.0 230610.0 476790.0 230548.0 476790.0 230516.0 476844.0 230548.0 476898.0 230610.0 476898.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.01562</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5124897" gml:id="CP.5124897">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5124897</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5124897.POINT">
                    <gml:pos>230206.28319136126 476844.19207703444</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5124897">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230237.0 476898.0 230268.0 476844.0 230237.0 476790.0 230175.0 476790.0 230144.0 476844.0 230175.0 476898.0 230237.0 476898.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.009812</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5118782" gml:id="CP.5118782">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5118782</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5118782.POINT">
                    <gml:pos>230392.4041631817 476629.2780906697</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5118782">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230423.0 476683.0 230454.0 476629.0 230423.0 476576.0 230361.0 476576.0 230330.0 476629.0 230361.0 476683.0 230423.0 476683.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.005934</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5118783" gml:id="CP.5118783">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5118783</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5118783.POINT">
                    <gml:pos>230578.5251350021 476629.2780906697</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5118783">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230610.0 476683.0 230641.0 476629.0 230610.0 476576.0 230548.0 476576.0 230516.0 476629.0 230548.0 476683.0 230610.0 476683.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.006373</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5118781" gml:id="CP.5118781">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5118781</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5118781.POINT">
                    <gml:pos>230206.28319136126 476629.2780906697</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5118781">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230237.0 476683.0 230268.0 476629.0 230237.0 476576.0 230175.0 476576.0 230144.0 476629.0 230175.0 476683.0 230237.0 476683.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.005075</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5120312" gml:id="CP.5120312">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5120312</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5120312.POINT">
                    <gml:pos>230485.46464909188 476683.00658726087</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5120312">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230516.0 476737.0 230548.0 476683.0 230516.0 476629.0 230454.0 476629.0 230423.0 476683.0 230454.0 476737.0 230516.0 476737.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.007544</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5120310" gml:id="CP.5120310">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5120310</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5120310.POINT">
                    <gml:pos>230113.22270545104 476683.00658726087</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5120310">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230144.0 476737.0 230175.0 476683.0 230144.0 476629.0 230082.0 476629.0 230051.0 476683.0 230082.0 476737.0 230144.0 476737.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.005156</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5120311" gml:id="CP.5120311">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5120311</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5120311.POINT">
                    <gml:pos>230299.34367727148 476683.00658726087</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5120311">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230330.0 476737.0 230361.0 476683.0 230330.0 476629.0 230268.0 476629.0 230237.0 476683.0 230268.0 476737.0 230330.0 476737.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.006431</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="5121840" gml:id="CP.5121840">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.5121840</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.5121840.POINT">
                    <gml:pos>230392.4041631817 476736.7350838521</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.5121840">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>230423.0 476790.0 230454.0 476737.0 230423.0 476683.0 230361.0 476683.0 230330.0 476737.0 230361.0 476790.0 230423.0 476790.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>
            <imaer:result>
                <imaer:CalculationResult resultType="DEPOSITION" substance="NOX">
                    <imaer:value>0.0085</imaer:value>
                </imaer:CalculationResult>
            </imaer:result>
        </imaer:ReceptorPoint>
    </imaer:featureMember>
</imaer:FeatureCollectionCalculator>
