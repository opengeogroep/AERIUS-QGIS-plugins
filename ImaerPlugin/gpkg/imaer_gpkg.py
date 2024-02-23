import os

from PyQt5.QtCore import Qt, QVariant, QDateTime

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
            self.version = self.get_metadata('db_version')
        else:
            self.create_new()
    
    def create_new(self):
        if Qgis.QGIS_VERSION_INT >= 32800:
            self.md.createDatabase(self.filename)
        self.conn = self.md.createConnection(self.filename, {})

        self.create_metadata_table()

        if self.plugin is not None:
            self.set_metadata('qgis_plugin_version', self.plugin.version)
        self.set_metadata('gpkg_creation_time', QDateTime().currentDateTime().toString(Qt.ISODate))

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
            QgsCoordinateReferenceSystem(f'EPSG:{epsg_id}'),
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

    def create_metadata_table(self):
        q = '''
            CREATE TABLE imaer_metadata (
                metadata_id INTEGER PRIMARY KEY,
                key TEXT UNIQUE,
                value TEXT,
                data_type TEXT
            );
        '''
        self.conn.executeSql(q)

    def set_metadata(self, key, value):
        if value is None:
            q = f'DELETE FROM imaer_metadata WHERE key = \'{key}\';'
            self.conn.executeSql(q)
            return True

        if isinstance(value, str):
            data_type = 'str'
        elif isinstance(value, float):
            data_type = 'float'
        elif isinstance(value, int):
            data_type = 'int'
        else:
            return False
        str_value = str(value)

        q = f'SELECT * FROM imaer_metadata WHERE key = \'{key}\';'
        result = self.conn.executeSql(q)

        if len(result) == 0:
            q = f'INSERT INTO imaer_metadata (key, value, data_type) VALUES (\'{key}\', \'{str_value}\', \'{data_type}\');'
        else:
            q = f'UPDATE imaer_metadata SET (value, data_type) = (\'{str_value}\', \'{data_type}\') WHERE key = \'{key}\';'
        result = self.conn.executeSql(q)

        return True

    def get_metadata(self, key):
        q = f'SELECT key, value, data_type FROM imaer_metadata WHERE key = \'{key}\';'
        result = self.conn.executeSql(q)

        if len(result) == 0:
            return None

        data_type = result[0][2]
        str_value = result[0][1]
        if data_type == 'int':
            return int(str_value)
        elif data_type == 'float':
            return float(str_value)
        else:
            return str_value
    
    def get_all_metadata(self):
        q = 'SELECT key FROM imaer_metadata ORDER BY key;'
        qr = self.conn.executeSql(q)

        result = {}

        for rec in qr:
            key = rec[0]
            result[key] = self.get_metadata(key)
        
        return result