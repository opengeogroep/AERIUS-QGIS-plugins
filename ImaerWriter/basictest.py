import imaerwrite as imaer

### this script does a basic test of the imaerwrite module ###
### it provides an example of how to construct valid IMAER-gml ###
### ... except that it is not valid as the geometry is not valid EPSG:28992 ###
### for brevity and readability the coordinates are kept short                         ###

fList = []

e = imaer.EmissionSource(wktGeometry = 'POINT(1 2)', gmlId = 'ES.1')
e.addEmission(imaer.EmissionSource.Emission('NOX',3))
e.addEmission(imaer.EmissionSource.Emission('NH3',4))

fList.append(e)

e = imaer.EmissionSource(wktGeometry = 'LINESTRING(1 2,12.14 23.4664478)', label = 'test source LINE', gmlId = 'ES.2')
e.addEmission(imaer.EmissionSource.Emission('NOX',3.13))
e.addEmission(imaer.EmissionSource.Emission('NH3',4.2))

fList.append(e)

sc = imaer.EmissionSource.EmissionSourceCharacteristics(heatContent = 4, emissionHeight = 31)
e = imaer.EmissionSource(wktGeometry = 'POLYGON ((10 10, 110 10, 110 110, 10 110), (20 20, 20 30, 30 30, 30 20), (40 20, 40 30, 50 30, 50 20))', 
                         emissionSourceCharacteristics = sc, label = 'test source POLYGON', gmlId = 'ES.3')
e.addEmission(imaer.EmissionSource.Emission('NOX',3.3))
e.addEmission(imaer.EmissionSource.Emission('NH3',4.12))

fList.append(e)

i = imaer.ImaerWrite(features = fList)
i.save('test.gml')
print 'Done'
