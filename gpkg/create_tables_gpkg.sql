DROP TABLE IF EXISTS gpkg_contents;
CREATE TABLE gpkg_contents (
    table_name TEXT,
    data_type TEXT,
    identifier TEXT,
    description TEXT,
    last_change DATETIME,
    min_x DOUBLE,
    min_y DOUBLE,
    max_x DOUBLE,
    max_y DOUBLE,
    srs_id INTEGER
);

DROP TABLE IF EXISTS gpkg_geometry_columns;
CREATE TABLE gpkg_geometry_columns (
    table_name TEXT,
    column_name TEXT,
    geometry_type_name TEXT,
    srs_id INTEGER,
    z TINYINT,
    m TINYINT
);

DROP TABLE IF EXISTS gpkg_ogr_contents;
CREATE TABLE gpkg_ogr_contents (
    table_name TEXT,
    feature_count INTEGER
);

DROP TABLE IF EXISTS gpkg_spatial_ref_sys;
CREATE TABLE gpkg_spatial_ref_sys (
    srs_name TEXT,
    srs_id INTEGER,
    organization TEXT,
    organization_coordsys_id INTEGER,
    definition TEXT,
    description TEXT
);
