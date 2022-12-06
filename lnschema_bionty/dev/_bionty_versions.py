from datetime import datetime as datetime
from typing import Optional

from lnschema_core._timestamps import CreatedAt, UpdatedAt
from lnschema_core._users import CreatedBy
from sqlmodel import Field, SQLModel


class bionty_versions(SQLModel, table=True):  # type: ignore
    """Versions of the knowledge tables."""

    id: Optional[int] = Field(default=None, primary_key=True)
    entity: str = Field(index=True)
    database: str = Field(index=True)
    database_v: str = Field(index=True)
    database_url: Optional[str] = None
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class bionty_version(SQLModel, table=True):  # type: ignore
    """In-use version of the knowledge tables."""

    id: int = Field(primary_key=True, foreign_key="bionty_versions.id")
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
