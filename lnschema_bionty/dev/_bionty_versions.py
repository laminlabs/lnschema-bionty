from datetime import datetime as datetime
from typing import Optional

from lnschema_core._timestamps import CreatedAt, UpdatedAt
from lnschema_core._users import CreatedBy
from sqlmodel import Field, SQLModel


class bionty_versions(SQLModel, table=True):  # type: ignore
    """Versions of the knowledge tables."""

    id: int = Field(primary_key=True)
    table: str = Field(index=True)
    database: str = Field(index=True)
    database_v: str = Field(index=True)
    database_url: Optional[str] = None
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
