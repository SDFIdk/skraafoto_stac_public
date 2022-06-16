"""Queryable data types for sqlalchemy backend."""

from dataclasses import dataclass

import sqlalchemy as sa


@dataclass
class QueryableTypes:
    """Defines a set of queryable fields.

    """

    orientation = sa.String
    gsd = sa.Float
    epsg = sa.Integer
    height = sa.Integer
    width = sa.Integer
    minzoom = sa.Integer
    maxzoom = sa.Integer
    dtype = sa.String
