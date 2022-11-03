from datetime import datetime as datetime
from typing import Optional

from lnschema_core._timestamps import CreatedAt
from lnschema_core._users import CreatedBy
from sqlmodel import Field, SQLModel


class version_zdno(SQLModel, table=True):  # type: ignore
    """Schema versions."""

    v: str = Field(primary_key=True)
    migration: Optional[str] = None
    user_id: str = CreatedBy
    created_at: datetime = CreatedAt


class migration_zdno(SQLModel, table=True):  # type: ignore
    """Latest migration.

    This stores the reference to the latest migration script deployed.
    """

    version_num: Optional[str] = Field(primary_key=True)
