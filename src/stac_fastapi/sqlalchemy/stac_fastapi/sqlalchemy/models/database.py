"""SQLAlchemy ORM models."""

from decimal import Decimal
import json
from typing import Optional

import geoalchemy2 as ga
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import func, select, cast
from sqlalchemy.orm import query_expression

from stac_fastapi.sqlalchemy.types.search import Queryables
from stac_fastapi.sqlalchemy.config import QueryableInfo

BaseModel = declarative_base()


class GeojsonGeometry(ga.Geometry):
    """Custom geoalchemy type which returns GeoJSON."""

    from_text = "ST_GeomFromGeoJSON"

    def result_processor(self, dialect: str, coltype):
        """Override default processer to return GeoJSON."""

        def process(value: Optional[bytes]):
            if value is not None:
                geom = ga.shape.to_shape(
                    ga.elements.WKBElement(
                        value, srid=self.srid, extended=self.extended
                    )
                )
                return json.loads(json.dumps(geom.__geo_interface__))

        return process


def default_title(context):
    return context.get_current_parameters()["id"]


class Collection(BaseModel):  # type:ignore
    """Collection orm model."""

    __tablename__ = "collections"
    __table_args__ = {"schema": "stac_api"}

    id = sa.Column(sa.VARCHAR(1024), nullable=False, primary_key=True)
    stac_version = sa.Column(sa.VARCHAR(300))
    stac_extensions = sa.Column(sa.ARRAY(sa.VARCHAR(300)), nullable=True)
    title = sa.Column(
        sa.VARCHAR(1024), default=default_title
    )  # Defaults to the ID of the collection if title is not set
    description = sa.Column(sa.VARCHAR(1024), nullable=False)
    keywords = sa.Column(sa.ARRAY(sa.VARCHAR(300)))
    version = sa.Column(sa.VARCHAR(300))
    license = sa.Column(sa.VARCHAR(300), nullable=False)
    providers = sa.Column(JSONB)
    summaries = sa.Column(JSONB, nullable=True)
    extent = sa.Column(JSONB)
    links = sa.Column(JSONB)
    # children = sa.orm.relationship("Item", lazy="dynamic")
    children = sa.orm.relationship("ImageView", lazy="dynamic")
    type = sa.Column(sa.VARCHAR(300), nullable=False)
    storage_crs = sa.Column(
        sa.VARCHAR(300),
        default="http://www.opengis.net/def/crs/OGC/1.3/CRS84",
        nullable=True,
    )


class ImageView(BaseModel):
    """Image orm model."""

    __tablename__ = "images_vw"
    __table_args__ = {"schema": "stac_api"}

    id = sa.Column(sa.TEXT, nullable=False, primary_key=True)
    collection_id = sa.Column(sa.TEXT, sa.ForeignKey(Collection.id), nullable=False)
    instrument_id = sa.Column(sa.Integer, nullable=False)
    datetime = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False)
    end_datetime = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False)
    footprint = query_expression(
        default_expr=sa.Column(
            GeojsonGeometry("POLYGON", srid=4326, spatial_index=True)
        )
    )
    bbox = query_expression(
        default_expr=sa.Column(sa.ARRAY(sa.NUMERIC), nullable=False)
    )
    easting = sa.Column(sa.Numeric(asdecimal=False))
    northing = sa.Column(sa.Numeric(asdecimal=False))
    height = sa.Column(sa.Numeric(asdecimal=False))
    vertical_crs = sa.Column(sa.Integer)
    horisontal_crs = sa.Column(sa.Integer)
    compound_crs = sa.Column(sa.Integer)
    omega = sa.Column(sa.Numeric(asdecimal=False))
    phi = sa.Column(sa.Numeric(asdecimal=False))
    kappa = sa.Column(sa.Numeric(asdecimal=False))
    rotmatrix = sa.Column(sa.ARRAY(sa.Float))
    direction = sa.Column(sa.TEXT)
    azimuth = sa.Column(sa.Numeric(asdecimal=False))
    offnadir = sa.Column(sa.Numeric(asdecimal=False))
    estacc = sa.Column(sa.Numeric(asdecimal=False))
    producer = sa.Column(sa.TEXT)
    gsd = sa.Column(sa.Numeric(asdecimal=False))
    data_path = sa.Column(sa.TEXT)
    properties = sa.Column(JSONB)

    # Camera properties
    camera_id = sa.Column(sa.TEXT)
    focal_length = sa.Column(sa.Numeric(asdecimal=False))
    principal_point_x = sa.Column(sa.Numeric(asdecimal=False))
    principal_point_y = sa.Column(sa.Numeric(asdecimal=False))
    sensor_pixel_size = sa.Column(sa.Numeric(asdecimal=False))
    sensor_physical_width = sa.Column(sa.Numeric(asdecimal=False))
    sensor_physical_height = sa.Column(sa.Numeric(asdecimal=False))
    sensor_columns = sa.Column(sa.Numeric(asdecimal=False))
    sensor_rows = sa.Column(sa.Numeric(asdecimal=False))
    calibration_date = sa.Column(sa.Date)
    owner = sa.Column(sa.TEXT)

    parent_collection = sa.orm.relationship("Collection", back_populates="children")

    @classmethod
    def get_field(cls, field_name):
        """Get a model field."""
        try:
            return getattr(cls, Queryables.get_queryable(field_name).name)
        except AttributeError:
            # Use a JSONB field
            return cls.properties[(field_name)].astext.cast(
                getattr(QueryableInfo, Queryables.get_queryable(field_name).name)[0]
            )
