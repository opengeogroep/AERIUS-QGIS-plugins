import time


class ImaerGpkg():
    def __init__(self, gml_filename=None, gpkg_filename=None):

        self.gml_filename = gml_filename
        self.gpkg_filename = gpkg_filename



    def __str__(self):
        result = 'ImaerGpkg[{}]'.format({})


    def gmlToGpkg(self):
        if self.gml_filename is None:
            return
        if self.gpkg_filename is None:
            pass
            #return

        '''vl = QgsVectorLayer('NoGeometry', 'test', 'memory')
        pr = vl.dataProvider()
        pr.addAttributes([QgsField("id", QVariant.String)])
        pr.addAttributes([QgsField("test", QVariant.Int)])
        vl.updateFields()
        QgsProject.instance().addMapLayer(vl)'''

        gml_header = ''
        in_header = True
        gml_footer = ''
        in_feature_member = False
        receptor_cnt = 0

        with open(self.gml_filename) as gml_file:
            for line in gml_file:
                #print(line)
                #print(in_receptor, in_header)
                if '<imaer:ReceptorPoint ' in line:
                    #print('receptor!!!')
                    in_feature_member = True
                    in_header = False
                    receptor_cnt += 1
                if not in_feature_member:
                    if in_header:
                        gml_header += line
                    else:
                        gml_footer += line
                if '</imaer:ReceptorPoint>' in line:
                    in_feature_member = False
        if True:
            print(gml_header)
            print()
            print(receptor_cnt)
            print()
            print(gml_footer)



    def __checkSource(self, filename):
        if filename is None:
            return 0



t0 = time.time()

gml_filename = '/home/raymond/git/AERIUS-QGIS-plugins/demodata/AERIUS_20200623162435_0_Situatie1.gml'
# gml_filename = '/home/raymond/git/AERIUS-QGIS-plugins/demodata/AERIUS_Calculator_4.gml'

print(gml_filename)
ig = ImaerGpkg(gml_filename)
ig.gmlToGpkg()

print(time.time() - t0)
