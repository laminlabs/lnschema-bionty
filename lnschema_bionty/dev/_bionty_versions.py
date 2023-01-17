from datetime import datetime as datetime
from typing import Optional

from lnschema_core._timestamps import CreatedAt, UpdatedAt
from lnschema_core._users import CreatedBy
from lnschema_core.dev.sqlmodel import schema_sqlmodel
from sqlmodel import Field

from .. import _name as schema_name

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


class BiontyVersions(SQLModel, table=True):  # type: ignore
    """Versions of the knowledge tables."""

    __tablename__ = f"{prefix}bionty_versions"

    id: Optional[int] = Field(default=None, primary_key=True)
    entity: str = Field(index=True)
    database: str = Field(index=True)
    database_v: str = Field(index=True)
    database_url: Optional[str] = None
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class CurrentBiontyVersions(SQLModel, table=True):  # type: ignore
    """In-use version of the knowledge tables."""

    __tablename__ = f"{prefix}current_bionty_versions"

    id: int = Field(primary_key=True, foreign_key="bionty.bionty_versions.id")
    entity: str = Field(index=True, unique=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
