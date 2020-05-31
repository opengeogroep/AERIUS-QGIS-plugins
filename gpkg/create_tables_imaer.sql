DROP TABLE IF EXISTS receptors;
CREATE TABLE receptors (
    receptor_id TEXT,
    point GEOMETRY,
    representation GEOMETRY,
    dep_nh3 DOUBLE,
    dep_nox DOUBLE,
    dep_no2 DOUBLE
);

INSERT INTO gpkg_contents VALUES ('receptors', 0);
