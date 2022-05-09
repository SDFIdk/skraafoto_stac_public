"""database session management."""
import logging
import os
from contextlib import contextmanager
from typing import Iterator, Optional

import attr
import psycopg2
import sqlalchemy as sa
from fastapi_utils.session import FastAPISessionMaker as _FastAPISessionMaker
from sqlalchemy.orm import Session as SqlSession

from stac_fastapi.sqlalchemy.config import SqlalchemySettings
from stac_fastapi.types import errors

logger = logging.getLogger(__name__)


class FastAPISessionMaker(_FastAPISessionMaker):
    """FastAPISessionMaker."""
    def __init__(self, database_uri: str, connect_args: dict):
        """
        `database_uri` should be any sqlalchemy-compatible database URI.

        In particular, `sqlalchemy.create_engine(database_uri)` should work to create an engine.

        Typically, this would look like:

            "<scheme>://<user>:<password>@<host>:<port>/<database>"

        A concrete example looks like "postgresql://db_user:password@db:5432/app"
        """
        self.database_uri = database_uri
        self.connect_args = connect_args

        self._cached_engine: Optional[sa.engine.Engine] = None
        self._cached_sessionmaker: Optional[sa.orm.sessionmaker] = None

    @contextmanager
    def context_session(self) -> Iterator[SqlSession]:
        """Override base method to include exception handling."""
        try:
            yield from self.get_db()
        except sa.exc.StatementError as e:
            if isinstance(e.orig, psycopg2.errors.UniqueViolation):
                raise errors.ConflictError("Resource already exists") from e
            elif isinstance(e.orig, psycopg2.errors.ForeignKeyViolation):
                raise errors.ForeignKeyError("Collection does not exist") from e
            elif isinstance(e.orig, psycopg2.errors.QueryCanceled):
                raise errors.TimeoutError("The request took longer than the allowed amount of time, and timed out.")
            logger.error(e, exc_info=True)
            raise errors.DatabaseError("Unhandled database error")
    
    def get_new_engine(self) -> sa.engine.Engine:
        """
        Returns a new sqlalchemy engine using the instance's database_uri.
        """
        return get_engine(self.database_uri,self.connect_args)

# Overridge get_engine, so we can send connection_args
def get_engine(uri: str, connect_args: dict) -> sa.engine.Engine:
    """
    Returns a sqlalchemy engine with pool_pre_ping enabled.

    This function may be updated over time to reflect recommended engine configuration for use with FastAPI.
    """
    return sa.create_engine(uri, pool_pre_ping=True, connect_args=connect_args)

@attr.s
class Session:
    """Database session management."""

    conn_string: str = attr.ib()
    connect_args: dict = attr.ib()
    
    @classmethod
    def create_from_env(cls):
        """Create from environment."""
        return cls(
            conn_string=os.environ.get("CONN_STRING"),
            connect_args=os.environ.get("CONNECT_ARGS")
        )

    @classmethod
    def create_from_settings(cls, settings: SqlalchemySettings) -> "Session":
        """Create a Session object from settings."""
        return cls(
            conn_string=settings.connection_string,
            connect_args=settings.connect_args
        )

    def __attrs_post_init__(self):
        """Post init handler."""
        self.session_maker: FastAPISessionMaker = FastAPISessionMaker(self.conn_string,self.connect_args)
