"""Init SDFE modelled db

Revision ID: e9808fb085f8
Revises: 
Create Date: 2022-02-01 10:06:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e9808fb085f89"
down_revision = None
branch_labels = None
depends_on = None

SCHEMA = "stac_api"


def upgrade():
    op.execute("create extension if not exists postgis;")
    op.execute(f"create schema {SCHEMA};")
    op.execute(f"comment on schema {SCHEMA} is 'Data used by the STAC API';")
    op.execute(
        f"""
        CREATE TABLE {SCHEMA}.collections (
            id varchar(1024) NOT NULL,
            stac_version varchar(300) NULL,
            title varchar(1024) NULL,
            stac_extensions _varchar NULL,
            description varchar(1024) NOT NULL,
            keywords _varchar NULL,
            "version" varchar(300) NULL,
            license varchar(300) NOT NULL,
            providers jsonb NULL,
            summaries jsonb NULL,
            extent jsonb NULL,
            links jsonb NULL,
            "type" varchar(300) NOT NULL,
            "storage_crs" varchar(300) NULL DEFAULT 'http://www.opengis.net/def/crs/OGC/1.3/CRS84'::character varying,
            CONSTRAINT collections_pkey PRIMARY KEY (id)
        );
    """
    )
    op.execute(
        f"""
            CREATE TABLE {SCHEMA}.instruments (
                id int4 NOT NULL,
                camera_id text,
                focal_length float8,
                principal_point_x float8,
                principal_point_y float8,
                sensor_pixel_size float8,
                sensor_physical_width float8,
                sensor_physical_height float8,
                sensor_columns int8,
                sensor_rows int8,
                calibration_date date,
                "owner" text,
                CONSTRAINT instruments_pkey PRIMARY KEY (id)
            );
    """
    )
    op.execute(
        f"""
        CREATE TABLE {SCHEMA}.images (
            id text NOT NULL,
            collection_id text NOT NULL,
            instrument_id integer NOT NULL,
            datetime timestamptz NOT NULL,
            end_datetime timestamptz NOT NULL,
            footprint geometry(polygon, 4326) NOT NULL,
            easting numeric,
            northing numeric,
            height numeric,
            vertical_crs int4,
            horisontal_crs int4,
            compound_crs int4,
            omega numeric,
            phi numeric,
            kappa numeric,
            rotmatrix float8[] CHECK (rotmatrix is null or array_length(rotmatrix, 1) = 9),
            direction text check (direction in (null, 'north', 'east', 'south', 'west', 'nadir')),
            azimuth numeric check (azimuth is null or azimuth between 0 and 360),
            offnadir numeric CHECK (offnadir is null or offnadir between 0 and 90),
            estacc numeric CHECK (estacc is null or estacc > 0),
            producer text,
            gsd numeric CHECK (gsd is null or gsd > 0),
            data_path text,
            properties jsonb NOT NULL, -- additional properties not foreseen at table creation time
            CONSTRAINT images_pkey PRIMARY KEY (id),
            CONSTRAINT images_collections_fk FOREIGN KEY (collection_id) REFERENCES {SCHEMA}.collections(id),
            CONSTRAINT images_instruments_fk FOREIGN KEY (instrument_id) REFERENCES {SCHEMA}.instruments(id)
        );
        CREATE UNIQUE INDEX images_datetime_id_desc_idx ON {SCHEMA}.images USING btree (datetime, id DESC);
        CREATE INDEX images_geometry_idx ON {SCHEMA}.images USING gist (footprint);
        CREATE INDEX images_collection_idx ON {SCHEMA}.images USING btree (collection_id);
        CREATE INDEX images_datetime_idx ON {SCHEMA}.images USING btree (datetime);  
    """
    )
    op.execute(
        f"""
        create view {SCHEMA}.images_vw as 
        select 
            i.id,
            i.collection_id,
            i.instrument_id,
            i.datetime,
            i.end_datetime,
            i.footprint,
            i.easting,
            i.northing,
            i.height,
            i.vertical_crs,
            i.horisontal_crs,
            i.compound_crs,
            i.omega,
            i.phi,
            i.kappa,
            i.rotmatrix,
            i.direction,
            i.azimuth,
            i.offnadir,
            i.estacc,
            i.producer,
            i.gsd,
            i.data_path,
            i.properties,
            c.camera_id,
            c.focal_length,
            c.principal_point_x,
            c.principal_point_y,
            c.sensor_pixel_size,
            c.sensor_physical_width,
            c.sensor_physical_height,
            c.sensor_columns,
            c.sensor_rows,
            c.calibration_date,
            c.owner
        from {SCHEMA}.images i left join {SCHEMA}.instruments c on (i.instrument_id = c.id);
        """
    )

    # # # # # # #
    # Test Data
    # # # # # # #
    # Collection
    op.execute(
        f"""INSERT INTO {SCHEMA}.collections (id, stac_version, title, stac_extensions, description, keywords, version, license, providers, summaries, extent, links, type, storage_crs) VALUES ('skraafotos2019', '1.0.0', 'Skråfotos 2019', '{{}}', 'Skråfotoflyvning i år 2019. Mere beskrivelse.....', '{{}}', NULL, 'various', '[{{"url": "https://www.sdfe.dk", "name": "SDFE", "roles": ["host", "licensor"]}}]', '{{}}', '{{"spatial": {{"bbox": [[8.003971195773962, 54.52440335178868, 15.25212221779363, 57.785177355171655]]}}, "temporal": {{"interval": [["2019-02-24 10:54:24Z", "2019-10-07 10:07:49Z"]]}}}}', '[{{"rel": "license", "href": "https://sdfe.dk/om-os/vilkaar-og-priser", "type": "text/html; charset=UTF-8", "title": "SDFE license terms"}}]', 'collection', 'http://www.opengis.net/def/crs/OGC/1.3/CRS84');
            INSERT INTO {SCHEMA}.collections (id, stac_version, title, stac_extensions, description, keywords, version, license, providers, summaries, extent, links, type, storage_crs) VALUES ('skraafotos2021', '1.0.0', 'Skråfotos 2021', '{{}}', 'Skråfotoflyvning i år 2021. Mere beskrivelse.....', '{{}}', NULL, 'various', '[{{"url": "https://www.sdfe.dk", "name": "SDFE", "roles": ["host", "licensor"]}}]', '{{}}', '{{"spatial": {{"bbox": [[8.015616423011219, 54.52455316904874, 15.254239006774482, 57.650387661241574]]}}, "temporal": {{"interval": [["2021-03-10 08:12:40Z", "2021-11-22 10:03:41Z"]]}}}}', '[{{"rel": "license", "href": "https://sdfe.dk/om-os/vilkaar-og-priser", "type": "text/html; charset=UTF-8", "title": "SDFE license terms"}}]', 'collection', 'http://www.opengis.net/def/crs/OGC/1.3/CRS84');
            INSERT INTO {SCHEMA}.collections (id, stac_version, title, stac_extensions, description, keywords, version, license, providers, summaries, extent, links, type, storage_crs) VALUES ('skraafotos2017', '1.0.0', 'Skråfotos 2017', '{{}}', 'Skråfotoflyvning i år 2017. Mere beskrivelse.....', '{{}}', NULL, 'various', '[{{"url": "https://www.sdfe.dk", "name": "SDFE", "roles": ["host", "licensor"]}}]', '{{}}', '{{"spatial": {{"bbox": [[7.996239440755403, 54.51938701852729, 15.276592787248427, 57.78491417688241]]}}, "temporal": {{"interval": [["2017-03-10 12:46:41Z", "2017-09-09 16:00:59Z"]]}}}}', '[{{"rel": "license", "href": "https://sdfe.dk/om-os/vilkaar-og-priser", "type": "text/html; charset=UTF-8", "title": "SDFE license terms"}}]', 'collection', 'http://www.opengis.net/def/crs/OGC/1.3/CRS84');
        """
    )
    # Instruments

    op.execute(
        f"""
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (23, 'UC-Xp-1-41410410-f100', 100.5, 0.12, 0.12, 0.00600000000000000000, 103.86, 67.86, 17310, 11310, '2018-02-04', 'TopGIS');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (2, 'UC-SXp-1-01613116', 100.5, -0.12, 0, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2014-04-18', 'COWI');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (10, 'UC-Eagle-1-50016095', 79.8, 0, 0, 0.00520000000000000000, 68.016, 104.052, 13080, 20010, '2012-02-23', 'FUGRO');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (11, 'UC-SXp-1-70113011', 100.5, 0, 0.12, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2011-08-04', 'Geophoto');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (12, 'UC-SXp-1-71717171', 100.5, 0.12, 0.18, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2009-02-03', NULL);
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (13, 'UXP-31217112', 100.5, 0, 0.12, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2014-03-19', 'COWI');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (14, 'UCE-1-30011051-f100', 100.5, 0, 0, 0.00520000000000000000, 68.016, 104.052, 13080, 20010, '2013-12-03', 'Weser');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (15, 'UCE-1-40317592-f100', 100.5, -0.104, 0, 0.00520000000000000000, 68.016, 104.052, 13080, 20010, '2015-01-15', 'AVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (17, 'UC-E-1-10418098-f80', 79.8, 0, 0, 0.00520000000000000000, 68.016, 104.052, 13080, 20010, '2016-02-04', 'TOPGIS');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (20, 'UC-SXp-1-90712467', 100.5, -0.12, 0, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2016-03-04', 'Finmap');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (21, 'UC-E-1-50111116-f100', 100.5, 0, -0.104, 0.00520000000000000000, 68.016, 104.052, 13080, 20010, '2016-02-04', 'AVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (25, 'UCXp-1-40719017', 100.5, -0.18, 0, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2016-03-14', 'Primis');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (27, 'DMCIII_27528', 92, 0, 0, 0.00390000000000000000, 56.9088, 100.3392, 14592, 25728, '2016-08-19', 'GEOREAL');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (29, 'UCO-M3p-423S01964X411181-f120_502', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (30, 'UCO-M3p-423S01964X411181-f120_503', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (31, 'UCO-M3p-423S01964X411181-f120_504', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (32, 'UCO-M3p-423S01964X411181-f120_505', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (33, 'UCO-M3p-423S01964X411181-f120_501', 82, 0, 0, 0.00520000000000000000, 70.044, 45.084, 13470, 8670, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (34, '423S91367X312008-f120_501', 82, 0, 0, 0.00520000000000000000, 70.044, 45.084, 13470, 8670, '2016-12-05', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (35, '423S91367X312008-f120_502', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2016-12-05', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (36, '423S91367X312008-f120_503', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2016-12-05', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (37, '423S91367X312008-f120_504', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2016-12-05', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (38, '423S91367X312008-f120_505', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2016-12-05', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (40, 'UCO-M3p-423S01968X612100-f120_502', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (41, 'UCO-M3p-423S01968X612100-f120_503', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (42, 'UCO-M3p-423S01968X612100-f120_504', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (50, 'RCD30_Oblique_Penta_35112_82569-50106', 53, 0, 0, 0.00520000000000000000, 53.748, 40.4976, 10336, 7788, '2017-01-01', 'COWI');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (44, 'UCO-M3p-423S01968X612100-f120_501', 82, 0, 0, 0.00520000000000000000, 70.044, 45.084, 13470, 8670, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (45, 'UCO-M3p-423S41871X111132-f120_502', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (46, 'UCO-M3p-423S41871X111132-f120_503', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (47, 'UCO-M3p-423S41871X111132-f120_504', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (51, 'RCD30_Oblique_Penta_35112_81559-80195', 83, 0, 0, 0.00520000000000000000, 53.748, 40.4976, 10336, 7788, '2017-01-01', 'COWI');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (49, 'UCO-M3p-423S41871X111132-f120_501', 82, 0, 0, 0.00520000000000000000, 70.044, 45.084, 13470, 8670, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (43, 'UCO-M3p-423S01968X612100-f120_505', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (48, 'UCO-M3p-423S41871X111132-f120_505', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2017-01-25', 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (52, 'RCD30_Oblique_Penta_35112_81554-80115', 83, 0, 0, 0.00520000000000000000, 53.748, 40.4976, 10336, 7788, '2017-01-01', 'COWI');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (53, 'RCD30_Oblique_Penta_35112_81570-80158', 83, 0, 0, 0.00520000000000000000, 53.748, 40.4976, 10336, 7788, '2017-01-01', 'COWI');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (39, 'UC_SXp_1_40719017_270', 100.5, -0.18, 0, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2016-03-14', 'Primis');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (88, 'UC-Ep-1-41317592-f100', 100.5, 0, 0, 0.00460000000000000000, 68.034, 105.846, 14790, 23010, '2016-05-06', 'Vexcel-Imaging');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (3, 'UC-SXp-1-31217112', 100.5, 0, 0.12, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2014-03-19', 'COWI');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (4, 'UC-SXp-1-00114453', 100.5, 0, 0, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2014-02-25', 'COWI');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (95, 'DMC-III-SN27548', 92, 0, 0, 0.00390000000000000000, 56.9088, 100.3392, 14592, 25728, '2019-05-03', 'HEXAGON');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (7, 'UC-SXp-1-10712003', 100.5, 0, 0, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2010-11-10', 'Terratec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (26, 'UCE-1-30011051-f100', 100.5, 0, 0, 0.00520000000000000000, 68.016, 104.052, 13080, 20010, '2015-10-15', 'Weser');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (22, 'UC-OpII-1-70918041-f120_AREODATA', 122.9962, -0.0503, 0.0732, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, NULL, 'Aerodata');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (62, 'Osprey-80316002-f120_Rev04.00_C100', 82, 0, 0, 0.00520000000000000000, 70.044, 45.084, 13470, 8670, '2016-05-03', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (63, 'Osprey-80316002-f120_Rev04.00_C104', 122.982, -0.015, 0.019, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2016-05-03', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (28, 'UC-E-1-70616210-f100', 100.5, 0, 0, 0.00520000000000000000, 68.016, 104.052, 13080, 20010, '2017-03-15', 'GEOREAL');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (56, '431S61885X911019', 100.5, 0, 0, 0.00400000000000000000, 68.016, 105.84, 17004, 26460, '2018-03-22', 'GEOREAL');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (57, 'UCXp-1-50312142', 100.5, 0, 0, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2018-03-22', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (58, 'UC-E-1-30011051-f100-O', 100.5, 0, 0, 0.00520000000000000000, 68.016, 104.052, 13080, 20010, '2017-12-14', 'Weser Org');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (59, 'UC-E-1-30011051-f100', 100.438, -0.005, -0.009, 0.00520000000000000000, 68.016, 104.052, 13080, 20010, '2018-04-01', 'Weser Beregn');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (54, 'RCD30_Oblique_Penta_35112_81572-80117', 83, 0, 0, 0.00520000000000000000, 53.748, 40.4976, 10336, 7788, '2017-01-01', 'COWI');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (68, 'UC-SXp-1-20118219', 100.5, -0.24, 0, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2019-08-06', 'Primis');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (69, 'UC-SXp-1-40719017', 100.5, -0.18, 0, 0.00600000000000000000, 67.86, 103.86, 1131, 17310, '2018-02-28', 'Primis');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (77, 'UC-SXp-1-50312142', 100.5, 0, 0, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2018-03-20', 'Vermessung AVT-ZT-GmbH');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (8, 'UC-SXp-1-30719036', 100.5, 0, 0, 0.00600000000000000000, 67.86, 103.86, 11310, 17310, '2011-02-18', 'Terratec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (9, 'UC-Eagle-1-70512096', 79.8, 0, 0, 0.00520000000000000000, 68.016, 104.052, 13080, 20010, '2012-03-06', 'Terratec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (71, 'PhaseOne-IXU-RS-1000_RS011017', 108.2837, 0, 0, 0.00460000000000000000, 52.79988, 39.4588, 11478, 8578, '2019-02-21', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (72, 'PhaseOne-IXU-RS-1000_RS011009', 108.2201, 0, 0, 0.00460000000000000000, 52.79988, 39.4588, 11478, 8578, '2019-02-21', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (73, 'PhaseOne-IXU-RS-1000_RS011081', 108.2468, 0, 0, 0.00460000000000000000, 52.79988, 39.4588, 11478, 8578, '2019-02-21', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (74, 'PhaseOne-IXU-RS-1000_RS011019', 108.3599, 0, 0, 0.00460000000000000000, 52.79988, 39.4588, 11478, 8578, '2019-02-21', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (67, 'UC-EM3-431S61680X916102', 100.5, 0, 0, 0.00400000000000000000, 68.016, 105.84, 17004, 26460, '2018-05-11', 'Primis');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (76, 'UC-Ep-1-41317592-f100', 100.5, 0, 0, 0.00460000000000000000, 68.034, 105.846, 14790, 23010, '2019-03-15', 'Vermessung AVT-ZT-GmbH');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (75, 'UC-Ep-1-31011051-f100', 100.5, 0, 0, 0.00460000000000000000, 68.034, 105.846, 14790, 23010, '2019-02-28', 'Vermessung AVT-ZT-GmbH');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (83, 'UC-OpII-1-70918041-f120_501', 82, 0, 0, 0.00520000000000000000, 70.044, 45.084, 13470, 8670, '2019-03-23', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (70, 'PhaseOne-IXU-RS-1000_12339911', 69.798, 0, 0, 0.00460000000000000000, 52.79988, 39.4588, 11478, 8578, '2019-02-21', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (84, 'UC-OpII-1-70918041-f120_502', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2019-03-23', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (66, 'Osprey-80316002-f120_Rev04.00_C107', 122.981, 0.011, -0.029, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2016-05-03', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (89, 'CT_RCD30_Oblique_Penta_35112_81554-80115', 83.0186854411896, -0.0004, -0.027, 0.00520000000000000000, 53.7472, 40.4976, 10336, 7788, '2016-01-01', 'Test');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (90, 'DMC_III_SN:27532', 92, 0, 0, 0.00390000000000000000, 56.9088, 100.3392, 14592, 25728, '2019-03-21', 'MGGPAERO');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (91, 'UC-Xp-1-41410410-f100', 100.5, 0.12, 0.12, 0.00600000000000000000, 103.86, 67.86, 17310, 11310, '2016-11-08', 'TopGIS');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (85, 'UC-OpII-1-70918041-f120_503', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2019-03-23', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (86, 'UC-OpII-1-70918041-f120_504', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2019-03-23', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (87, 'UC-OpII-1-70918041-f120_505', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2019-03-23', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (107, 'UC-EM3-431S92908X210339', 100, 0, -0.12, 0.00400000000000000000, 68.02, 104.050, 17005, 26013, '2020-08-18', 'Primis');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (78, 'UC-OM3p-423S81560X411059-f120_Nadir', 82, 0, 0, 0.00520000000000000000, 45.084, 70.044, 8670, 13470, '2019-03-01', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (93, 'DMC-III-SN27523', 92, 0, 0, 0.00390000000000000000, 56.9088, 100.3392, 14592, 25728, '2020-03-20', 'HEXAGON');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (118, '431S41187X510139', 100.5, 0, 0, 0.00400000000000000000, 68.016, 105.84, 17004, 26460, '2021-03-01', 'GEOREAL');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (94, 'DMC-III-SN27524', 92, 0, 0, 0.00390000000000000000, 56.9088, 100.3392, 14592, 25728, '2020-02-11', 'HEXAGON');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (79, 'UC-OM3p-423S81560X411059-f120_Bwd', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2019-03-01', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (80, 'UC-OM3p-423S81560X411059-f120_Left', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2019-03-01', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (81, 'UC-OM3p-423S81560X411059-f120_Fwd', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2019-03-01', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (64, 'Osprey-80316002-f120_Rev04.00_C105', 122.98, -6.77, -0.036, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2016-05-03', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (65, 'Osprey-80316002-f120_Rev04.00_C106', 122.982, 6.788, 0.028, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2016-05-03', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (108, 'PentaCam_IXU_MGGPAero_20210321_YC030073', 69.798, 0, 0, 0.00460000000000000000, 52.532, 39.4588, 11420, 8578, '2021-02-10', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (109, 'PentaCam_IXU_MGGPAero_20210321_YC030066', 108.1919, 0, 0, 0.00460000000000000000, 52.532, 39.4588, 11420, 8578, '2021-02-10', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (110, 'PentaCam_IXU_MGGPAero_20210321_YC030074', 108.1371, 0, 0, 0.00460000000000000000, 52.532, 39.4588, 11420, 8578, '2021-02-10', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (1, 'UC-Ep-1-41317592-f100', 100.5, 0, 0, 0.00460000000000000000, 68.034, 105.846, 14790, 23010, '2019-03-15', 'Vermessung AVT-ZT-GmbH');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (111, 'PentaCam_IXU_MGGPAero_20210321_YC030075', 108.2406, 0, 0, 0.00460000000000000000, 52.532, 39.4588, 11420, 8578, '2021-02-10', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (112, 'PentaCam_IXU_MGGPAero_20210321_YC030076', 108.3635, 0, 0, 0.00460000000000000000, 52.532, 39.4588, 11420, 8578, '2021-02-10', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (106, 'UC-EM3-431S61680X916102', 100.5, 0, 0, 0.00400000000000000000, 68.016, 105.84, 17004, 26460, '2020-11-19', 'Primis');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (82, 'UC-OM3p-423S81560X411059-f120_Right', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2019-03-01', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (115, 'CityMapper2_96601_S150008-146027', 146, 0, 0, 0.00376000000000000000, 53.36192, 40.00064, 14192, 10640, '2020-08-12', 'HEXAGON');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (116, 'CityMapper2_96601_L150002-146028', 146, 0, 0, 0.00376000000000000000, 53.36192, 40.00064, 14192, 10640, '2020-08-12', 'HEXAGON');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (117, 'CityMapper2_96601_L150001-146021', 146, 0, 0, 0.00376000000000000000, 53.36192, 40.00064, 14192, 10640, '2020-08-12', 'HEXAGON');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (124, 'CityMapper2_96616_S150022-112020', 112, 0, 0, 0.00376000000000000000, 53.36192, 40.00064, 14192, 10640, '2021-02-02', 'Opegieka');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (125, 'CityMapper2_96616_S150050-146056', 146, 0, 0, 0.00376000000000000000, 53.36192, 40.00064, 14192, 10640, '2021-02-02', 'Opegieka');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (126, 'CityMapper2_96616_S150051-146040', 146, 0, 0, 0.00376000000000000000, 53.36192, 40.00064, 14192, 10640, '2021-02-02', 'Opegieka');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (127, 'CityMapper2_96616_L150022-146032', 146, 0, 0, 0.00376000000000000000, 53.36192, 40.00064, 14192, 10640, '2021-02-02', 'Opegieka');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (128, 'CityMapper2_96616_L150023-146035', 146, 0, 0, 0.00376000000000000000, 53.36192, 40.00064, 14192, 10640, '2021-02-02', 'Opegieka');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (135, 'DMCIII_27533', 92, 0, 0, 0.00390000000000000000, 56.9088, 100.3392, 14592, 25728, '2021-03-30', 'Opegieka');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (129, '431S91898X119229-f100', 100.5, 0, -0.12, 0.00400000000000000000, 105.84, 68.016, 26460, 17004, '2019-10-30', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (130, 'PhaseOne-IXU-RS-1000_12339911', 69.7377, 0, 0, 0.00460000000000000000, 52.532, 39.4588, 11420, 8578, '2021-02-10', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (96, 'UCOM3p-423S81560X411059_Nadir', 82, 0, 0, 0.00520000000000000000, 70.044, 45.084, 13470, 8669, '2019-03-01', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (97, 'UCOM3p-423S81560X411059_UC-Op-BWD', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2019-03-01', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (98, 'UCOM3p-423S81560X411059_UC-Op-Left', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2019-03-01', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (99, 'UCOM3p-423S81560X411059_UC-Op-FWD', 123, 0, 0, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2019-03-01', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (100, 'UCOM3p-423S81560X411059_UC-Op-Right', 123, 0, 6.75, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2019-03-01', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (133, 'PhaseOne-IXU-RS-1000_RS0110081', 108.3635, 0, 0, 0.00460000000000000000, 52.532, 39.4588, 11420, 8578, '2021-02-18', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (113, 'CityMapper2_96601_S150007-112007', 112, 0, 0, 0.00376000000000000000, 53.36192, 40.00064, 14192, 10640, '2020-08-12', 'HEXAGON');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (105, 'UCOM4-434S42016X419232_UC-Op-Left', 123.38, 0, 6.68, 0.00376000000000000000, 39.7056, 53.18144, 10560, 14144, '2021-03-29', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (101, 'UCOM4-434S42016X419232_Nadir', 79.6, 0, 0, 0.00376000000000000000, 77.24544, 52.70016, 20544, 14016, '2021-03-29', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (103, 'UCOM4-434S42016X419232_UC-Op-BWD', 123.38, 0, 0, 0.00376000000000000000, 53.18144, 39.7056, 14144, 10560, '2021-03-29', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (104, 'UCOM4-434S42016X419232_UC-Op-FWD', 123.38, 0, 0, 0.00376000000000000000, 53.18144, 39.7056, 14144, 10560, '2021-03-29', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (102, 'UCOM4-434S42016X419232_UC-Op-Right', 123.38, 0, 6.68, 0.00376000000000000000, 39.7056, 53.18144, 10560, 14144, '2021-03-29', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (136, '431S41091X314298-f100', 100.5, 0, -0.12, 0.00400000000000000000, 105.84, 68.016, 26460, 17004, '2019-10-30', 'GeoFly');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (131, 'PhaseOne-IXU-RS-1000_RS0110018', 108.2406, 0, 0, 0.00460000000000000000, 52.532, 39.4588, 11420, 8578, '2021-02-10', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (132, 'PhaseOne-IXU-RS-1000_RS0110009', 108.1919, 0, 0, 0.00460000000000000000, 52.532, 39.4588, 11420, 8578, '2021-02-05', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (134, 'PhaseOne-IXU-RS-1000_RS0110019', 108.1371, 0, 0, 0.00460000000000000000, 52.532, 39.4588, 11420, 8578, '2021-02-10', 'MGGPAero');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (114, 'CityMapper2_96601_S150006-146018', 146, 0, 0, 0.00376000000000000000, 53.36192, 40.00064, 14192, 10640, '2020-08-12', 'HEXAGON');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (137, '434S22717X710284-f120_501', 79.6, 0, 0, 0.00376000000000000000, 77.24544, 52.70016, 20544, 14016, '2021-04-19', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (138, '434S22717X710284-f120_502', 123.38, 0, 6.68, 0.00376000000000000000, 39.7056, 53.18144, 10560, 14144, '2021-04-19', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (139, '434S22717X710284-f120_503', 123.38, 0, 6.68, 0.00376000000000000000, 39.7056, 53.18144, 10560, 14144, '2021-04-19', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (140, '434S22717X710284-f120_504', 123.38, 0, 0, 0.00376000000000000000, 53.18144, 39.7056, 14144, 10560, '2021-04-19', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (141, '434S22717X710284-f120_505', 123.38, 0, 0, 0.00376000000000000000, 53.18144, 39.7056, 14144, 10560, '2021-04-19', 'VermessungAVT');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (119, 'Osprey-80316002-f120_Rev07.00_C100', 81.966, 0.0045, -0.006, 0.00520000000000000000, 70.044, 45.084, 13470, 8670, '2021-03-04', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (120, 'Osprey-80316002-f120_Rev07.00_C104', 122.982, -0.015, 0.019, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2021-03-04', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (121, 'Osprey-80316002-f120_Rev07.00_C105', 122.98, -0.036, 6.77, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2021-03-04', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (122, 'Osprey-80316002-f120_Rev07.00_C106', 122.982, -0.028, 6.788, 0.00520000000000000000, 40.04, 53.56, 7700, 10300, '2021-03-04', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (123, 'Osprey-80316002-f120_Rev07.00_C107', 122.981, -0.011, 0.029, 0.00520000000000000000, 53.56, 40.04, 10300, 7700, '2021-03-04', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (142, 'Osprey-80316002-f120_Rev07.00_10cm_C100', 81.966, 0.005, -0.008, 0.0052, 70.0402, 45.0804, 13470, 8670, '2020-05-18', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (143, 'Osprey-80316002-f120_Rev07.00_10cm_C104', 122.982, -0.015, 0.019, 0.0052, 53.5598, 40.0398, 10300, 7700, '2020-05-18', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (146, 'Osprey-80316002-f120_Rev07.00_10cm_C107', 122.981, -0.011, 0.029, 0.0052, 53.5598, 40.0398, 10300, 7700, '2020-05-18', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (144, 'Osprey-80316002-f120_Rev07.00_10cm_C105', 122.98, -0.036, 6.77, 0.0052, 40.0398, 53.5598, 7700, 10300, '2020-05-18', 'TerraTec');
        INSERT INTO {SCHEMA}.instruments (id, camera_id, focal_length, principal_point_x, principal_point_y, sensor_pixel_size, sensor_physical_width, sensor_physical_height, sensor_columns, sensor_rows, calibration_date, owner) VALUES (145, 'Osprey-80316002-f120_Rev07.00_10cm_C106', 122.982, -0.028, 6.788, 0.0052, 40.0398, 53.5598, 7700, 10300, '2020-05-18', 'TerraTec');
    """
    )

    # Images
    op.execute(
        f"""
        INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_20_4_2031_00030536',
            'skraafotos2017',
            41,
            '2017-05-27 09:04:49+00',
            '2017-05-27 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
        INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_19_1_0039_00160059',
            'skraafotos2017',
            41,
            '2017-05-27 09:04:49+00',
            '2017-05-27 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
        INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_19_2_0039_00160059',
            'skraafotos2017',
            41,
            '2017-05-27 09:04:49+00',
            '2017-05-27 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
            INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_84_41_2_0005_00000519',
            'skraafotos2017',
            41,
            '2017-05-27 09:04:49+00',
            '2017-05-27 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
            INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_20_4_2031_00030540',
            'skraafotos2017',
            41,
            '2017-05-27 09:04:49+00',
            '2017-05-27 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
            INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_20_4_2031_00030541',
            'skraafotos2017',
            41,
            '2017-05-27 09:04:49+00',
            '2017-05-27 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
            INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_20_4_2031_00030542',
            'skraafotos2017',
            41,
            '2017-05-28 09:04:49+00',
            '2017-05-28 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
            INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_20_4_2031_00030543',
            'skraafotos2017',
            41,
            '2017-05-28 09:04:49+00',
            '2017-05-28 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
            INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_20_4_2031_00030544',
            'skraafotos2017',
            41,
            '2017-05-28 09:04:49+00',
            '2017-05-28 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
            INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_20_4_2031_00030545',
            'skraafotos2017',
            41,
            '2017-05-28 09:04:49+00',
            '2017-05-28 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
            INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_20_4_2031_00030546',
            'skraafotos2017',
            41,
            '2017-05-28 09:04:49+00',
            '2017-05-28 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
            INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_20_4_2031_00030547',
            'skraafotos2017',
            41,
            '2017-05-28 09:04:49+00',
            '2017-05-28 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
            INSERT INTO {SCHEMA}.images(id, collection_id, instrument_id, datetime, end_datetime, footprint, easting, northing, height, vertical_crs, horisontal_crs, compound_crs, omega, phi, kappa, rotmatrix, direction, azimuth, offnadir, estacc, producer, gsd, data_path, properties)
	    VALUES (
            '2017_82_20_4_2031_00030548',
            'skraafotos2017',
            41,
            '2017-05-28 09:04:49+00',
            '2017-05-28 09:04:49+00',
            ST_GeomFromText('POLYGON((8.91023817166338 55.91173821232403,8.889373667657244 55.91306900272112,8.889486828862083 55.9182804475438,8.91042791107266 55.91964521416398,8.91023817166338 55.91173821232403))',4326),
            492210.26663,
            6196700.824,
            1586.9,
            5799,
            25832,
            7416,
            0.63227,
            -44.9837,
            270.368,
            '{{0.004541131412415701,-0.9999685865230831,-0.006496467695804305,0.7072931998517609,-0.0013806082230656616,0.706918965203503,-0.7069057274976289,-0.007805119343217051,0.7072647117897838}}',
            'east',
            90,
            45,
            NULL,
            'Aerodata',
            0.096,
            'https://api.dataforsyningen.dk/skraafoto_server_test/2017_cog/2017_82_20_4_2031_00030536.jpg.cog.tif',
            '{{}}');
        """
    )


def downgrade():
    op.execute(f"DROP VIEW {SCHEMA}.images_vw;")
    op.execute(f"DROP TABLE {SCHEMA}.images;")
    op.execute(f"DROP TABLE {SCHEMA}.instruments;")
    op.execute(f"DROP TABLE {SCHEMA}.collections;")
    op.execute(f"DROP SCHEMA {SCHEMA};")
