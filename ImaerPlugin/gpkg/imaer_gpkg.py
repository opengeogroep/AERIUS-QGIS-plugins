import os

from PyQt5.QtCore import QVariant

from qgis.core import (
    Qgis,
    QgsProviderRegistry,
    QgsCoordinateReferenceSystem,
    QgsFields,
    QgsField,
    QgsWkbTypes,
    #QgsFeature,
    #QgsGeometry,
    #QgsRectangle,
    #QgsVectorLayer
)

class ImaerGpkg():

    def __init__(self, filename, version='99.99.99', epsg_id=None, plugin=None):
        self.conn = None
        self.md = QgsProviderRegistry.instance().providerMetadata('ogr')
        self.filename = filename
        self.version = version
        self.epsg_id = epsg_id
        self.plugin = plugin

        self.connect()
    
    def __str__(self):
        return f'ImaerGpkg[{self.filename}]'

    def connect(self):
        print('connect()')
        '''Try to connect to existing db, or create a new one.'''
        if self.filename is None:
            print('no filename')
            return
        if os.path.isfile(self.filename):
            self.conn = self.md.createConnection(self.filename, {})
            self.version = self.get_metadata('db_version')
            self.epsg_id = self.get_epsg_id()
        else:
            if self.epsg_id is not None:
                self.create_new()
    
    def create_new(self):
        print('create_new()')
        if Qgis.QGIS_VERSION_INT >= 32800:
            self.md.createDatabase(self.filename)
        
        self.conn = self.md.createConnection(self.filename, {})

        self.create_layer_receptor_points()
        self.create_layer_receptor_hexagons()
        self.create_layer_sub_points()

        '''
        self.create_base_tables()
        self.create_voxels_view()
        self.create_indices()
        self.set_metadata('db_version', '1.0.0')

        self.upgrade_version(self.version)
        self.version = self.get_metadata('db_version')
        '''
    
    def create_layer(self, name, specific_fields, geometry_type):
        if self.conn is None:
            print('Non connection')
            return

        fields = QgsFields()

        #fields.append(QgsField('ogc_fid', QVariant.LongLong))

        for field in specific_fields:
            fields.append(field)
        
        print(fields)
        print(self.conn)

        self.conn.createVectorTable(
            '',
            name,
            fields,
            geometry_type,
            QgsCoordinateReferenceSystem(self.epsg_id),
            True,
            {'layerOptions': 'FID=ogc_fid'}
        )

    def get_deposition_fields(self):
        result = []
        result.append(QgsField('deposition_nh3', QVariant.Double))
        result.append(QgsField('deposition_nox', QVariant.Double))
        result.append(QgsField('deposition_sum_nh3_nox', QVariant.Double))
        return result
        
    def get_concentration_fields(self):
        result = []
        result.append(QgsField('concentration_nh3', QVariant.Double))
        result.append(QgsField('concentration_nox', QVariant.Double))
        result.append(QgsField('concentration_no2', QVariant.Double))
        return result

    def create_layer_receptor_points(self):
        fields = QgsFields()
        fields.append(QgsField('receptor_id', QVariant.LongLong))
        for field in self.get_concentration_fields():
            fields.append(field)
        self.create_layer('receptor_points', fields, QgsWkbTypes.Point)
    
    def create_layer_receptor_hexagons(self):
        fields = QgsFields()
        fields.append(QgsField('receptor_id', QVariant.LongLong))
        fields.append(QgsField('edge_effect', QVariant.LongLong))
        for field in self.get_deposition_fields():
            fields.append(field)
        self.create_layer('receptor_hexagons', fields, QgsWkbTypes.Polygon)
    
    def create_layer_sub_points(self):
        fields = QgsFields()
        fields.append(QgsField('receptor_id', QVariant.LongLong))
        fields.append(QgsField('sub_point_id', QVariant.LongLong))
        fields.append(QgsField('level', QVariant.LongLong))
        for field in self.get_deposition_fields():
            fields.append(field)
        for field in self.get_concentration_fields():
            fields.append(field)
        self.create_layer('sub_points', fields, QgsWkbTypes.Point)
