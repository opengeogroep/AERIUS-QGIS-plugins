import os

from PyQt5.QtCore import QVariant

from qgis.core import (
    Qgis,
    QgsProviderRegistry,
    QgsCoordinateReferenceSystem,
    QgsFields,
    QgsField,
    QgsWkbTypes
)

class ImaerGpkg():

    def __init__(self, filename, version='99.99.99', plugin=None):
        self.conn = None
        self.md = QgsProviderRegistry.instance().providerMetadata('ogr')
        self.filename = filename
        self.version = version
        self.plugin = plugin

        self.connect()
    
    def __str__(self):
        return f'ImaerGpkg[{self.filename}]'

    def connect(self):
        '''Try to connect to existing db, or create a new one.'''
        if self.filename is None:
            return
        if os.path.isfile(self.filename):
            self.conn = self.md.createConnection(self.filename, {})
            self.version = self.get_metadata('db_version')  # TODO!!!
        else:
            self.create_new()
    
    def create_new(self):
        if Qgis.QGIS_VERSION_INT >= 32800:
            self.md.createDatabase(self.filename)
        self.conn = self.md.createConnection(self.filename, {})

        #self.create_layer_receptor_points()
        #self.create_layer_receptor_hexagons()
        #self.create_layer_sub_points()

    def create_layer(self, name, specific_fields, geometry_type, epsg_id):
        if self.conn is None:
            return

        fields = QgsFields()
        for field in specific_fields:
            fields.append(field)
        
        self.conn.createVectorTable(
            '',
            name,
            fields,
            geometry_type,
            QgsCoordinateReferenceSystem(epsg_id),
            True,
            {'layerOptions': 'FID=ogc_fid'}
        )

    def get_deposition_fields(self):
        result = []
        result.append(QgsField('deposition_nox_nh3_sum', QVariant.Double))
        result.append(QgsField('deposition_nox', QVariant.Double))
        result.append(QgsField('deposition_nh3', QVariant.Double))
        return result
        
    def get_concentration_fields(self):
        result = []
        result.append(QgsField('concentration_nox', QVariant.Double))
        result.append(QgsField('concentration_no2', QVariant.Double))
        result.append(QgsField('concentration_nh3', QVariant.Double))
        result.append(QgsField('concentration_pm10', QVariant.Double))
        result.append(QgsField('concentration_pm25', QVariant.Double))
        return result

    def get_exceedance_fields(self):
        result = []
        result.append(QgsField('exceedance_days_pm10', QVariant.LongLong))
        result.append(QgsField('exceedance_days_pm25', QVariant.LongLong))
        result.append(QgsField('exceedance_hours_pm10', QVariant.LongLong))
        result.append(QgsField('exceedance_hours_pm25', QVariant.LongLong))
        return result

    def create_layer_receptor_points(self, epsg_id):
        fields = QgsFields()
        fields.append(QgsField('receptor_id', QVariant.LongLong))
        for field in self.get_concentration_fields():
            fields.append(field)
        for field in self.get_exceedance_fields():
            fields.append(field)
        self.create_layer('receptor_points', fields, QgsWkbTypes.Point, epsg_id)
    
    def create_layer_receptor_hexagons(self, epsg_id):
        fields = QgsFields()
        fields.append(QgsField('receptor_id', QVariant.LongLong))
        fields.append(QgsField('edge_effect', QVariant.LongLong))
        for field in self.get_deposition_fields():
            fields.append(field)
        self.create_layer('receptor_hexagons', fields, QgsWkbTypes.Polygon, epsg_id)
    
    def create_layer_sub_points(self, epsg_id):
        fields = QgsFields()
        fields.append(QgsField('receptor_id', QVariant.LongLong))
        fields.append(QgsField('sub_point_id', QVariant.LongLong))
        fields.append(QgsField('level', QVariant.LongLong))
        for field in self.get_deposition_fields():
            fields.append(field)
        for field in self.get_concentration_fields():
            fields.append(field)
        for field in self.get_exceedance_fields():
            fields.append(field)
        self.create_layer('sub_points', fields, QgsWkbTypes.Point, epsg_id)
