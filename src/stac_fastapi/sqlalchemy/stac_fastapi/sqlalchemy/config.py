"""Postgres API configuration."""
from typing import Set

from stac_fastapi.types.config import ApiSettings
from enum import auto
from stac_pydantic.utils import AutoValueEnum
import sqlalchemy as sa


class SqlalchemySettings(ApiSettings):
    """API settings."""

    debug: bool = False
    postgres_user: str
    postgres_pass: str
    postgres_host: str
    postgres_port: str
    postgres_dbname: str
    postgres_application_name: str = "stac-fastapi"

    cogtiler_basepath: str

    # Fields which are defined by STAC but not included in the database model
    forbidden_fields: Set[str] = {"type"}

    # Fields which are item properties but indexed as distinct fields in the database model
    indexed_fields: Set[str] = {"datetime"}

    @property
    def connection_string(self):
        """Create psql connection string."""
        return f"postgresql://{self.postgres_user}:{self.postgres_pass}@{self.postgres_host}:{self.postgres_port}/{self.postgres_dbname}?application_name={self.postgres_application_name}"


class BaseQueryables(str, AutoValueEnum):
    """Queryable fields.

    Define an enum of queryable fields and their data type.  Queryable fields are explicitly defined for two reasons:
        1. So the caller knows which fields they can query by
        2. Because JSONB queries with sqlalchemy ORM require casting the type of the field at runtime
            (see ``QueryableInfo``)

    # TODO: Let the user define these in a config file
    """

    id = auto()
    collection_id = "collection"
    footprint = "geometry"
    bbox = auto()
    datetime = auto()
    # stac_version = auto()
    # stac_extensions = auto()


class SkraafotosProperties(str, AutoValueEnum):
    end_datetime = auto()
    easting = auto()
    northing = auto()
    height = auto()
    vertical_crs = "pers:vertical_crs"
    horisontal_crs = "pers:crs"
    omega = "pers:omega"
    phi = "pers:phi"
    kappa = "pers:kappa"
    # rotation_matrix = "pers:rotation_matrix"  # omitted for now
    direction = auto()
    azimuth = "view:azimuth"
    offnadir = "view:off_nadir"
    estacc = "estimated_accuracy"
    producer = auto()
    gsd = auto()
    # license = auto()
    camera_id = "instruments"
    # epsg = "proj:epsg"
    # shape = "pers:shape" # omitted for now
    # io_camera_id = "pers:interior_orientation.camera_id"
    focal_length = "pers:interior_orientation.focal_length"
    calibration_date = "pers:interior_orientation.calibration_date"


class QueryableInfo:
    id = (
        None,
        "string",
        "ID",
        "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json#/id",
    )
    collection_id = (
        None,
        "string",
        "Collection ID",
        "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json#/collection",
    )
    footprint = (
        None,
        "Geometry",
        "Geometry",
        "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json#/geometry",
    )
    bbox = (
        None,
        "Geometry",
        "BBOX",
        "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json#/bbox",
    )
    datetime = (
        None,
        "string",
        "Datetime",
        "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/datetime.json#/properties/datetime",
    )
    # stac_version = (
    #     None,
    #     "string",
    #     "Stac version",
    #     "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json#/stac_version",
    # )
    # stac_extensions = (
    #     None,
    #     "string",
    #     "Datetime",
    #     "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json#/stac_extensions",
    # )

    # properties types: Pygeofilter currently don't support array operations in their sqlalchemy backend, so Array queryables are not exposed
    end_datetime = (
        None,
        "string",
        "End datetime",
        None,
    )
    easting = (
        None,
        "number",
        "Easting",
        None,
    )
    northing = (
        None,
        "number",
        "Northing",
        None,
    )
    height = (
        None,
        "number",
        "Height",
        None,
    )
    vertical_crs = (
        None,
        "number",
        "Perspective vertical_crs",
        None,
    )
    horisontal_crs = (
        None,
        "number",
        "Perspective crs",
        None,
    )
    omega = (None, "number", "Perspective omega", None)
    phi = (None, "number", "Perspective phi", None)
    kappa = (None, "number", "Perspective kappa", None)
    # rotation_matrix = (sa.ARRAY(sa.Float), "array", "Perspective rotation_matrix", None)
    direction = (None, "string", "Direction", None)
    azimuth = (None, "number", "View azimuth", None)
    offnadir = (None, "number", "View off_nadir", None)
    estacc = (None, "number", "Estimated accuracy", None)
    producer = (
        None,
        "string",
        "Producer name",
        None,
    )
    gsd = (
        None,
        "number",
        "Ground Sample Distance",
        "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/instrument.json#/properties/gsd",
    )
    # license = (sa.String, "string", "License", None)
    camera_id = (
        None,
        "string",
        "Instruments",
        "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/instrument.json#/properties/platform",
    )
    # epsg = (sa.Integer, "integer", "Projection EPSG", None)
    # shape = (sa.ARRAY(sa.INTEGER), "array", "Projection shape", None)
    # io_camera_id = (
    #     sa.String,
    #     "string",
    #     "Perspective (Interior Orientation) Camera Id",
    #     None,
    # )
    focal_length = (
        None,
        "string",
        "Perspective (Interior Orientation) Focal Length",
        None,
    )
    calibration_date = (
        None,
        "string",
        "Perspective (Interior Orientation) Calibration Date",
        None,
    )
