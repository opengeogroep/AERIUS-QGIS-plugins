from imaerread import ImaerRead

testfilename = '/home/raymond/git/AERIUS-QGIS-plugins/demodata/AERIUS_Calculator_4.gml'
testfilename = '/home/raymond/git/AERIUS-QGIS-plugins/demodata/AERIUS_Calculator_4e.gml'
testfilename = '/home/raymond/terglobo/data/aerius/AERIUS_gml_20200520100603/AERIUS_20200520100604_0_Situatie1.gml'

ir = ImaerRead(testfilename)

print(ir)

#print(ir.attributeFields)

ft = ir.nextFeature()
print(ft)


ft = True
while not ft == False:
    ft = ir.nextFeature(doHexagons=False)
    print(ft)

print(ir.numFeatures)
