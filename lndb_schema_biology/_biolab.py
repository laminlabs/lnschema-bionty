from typing import Optional  # noqa

from sqlmodel import Field, SQLModel

from ._bionty import featureset  # noqa


class dobject_biometa(SQLModel, table=True):  # type: ignore
    """Link between dobject and meta."""

    dobject_id: Optional[str] = Field(
        default=None, foreign_key="dobject.id", primary_key=True
    )
    biometa_id: Optional[int] = Field(
        default=None, foreign_key="biometa.id", primary_key=True
    )


class biometa(SQLModel, table=True):  # type: ignore
    """Metadata is a combination of biosample and experiment."""

    id: Optional[int] = Field(default=None, primary_key=True)
    biosample_id: int = Field(default=None, foreign_key="biosample.id")
    readout_type_id: int = Field(default=None, foreign_key="readout_type.id")
    featureset_id: int = Field(default=None, foreign_key="featureset.id")


class biosample(SQLModel, table=True):  # type: ignore
    """Biological samples that are registered in experiments."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    species_id: str = Field(default=None, foreign_key="species.id")


class readout_type(SQLModel, table=True):  # type: ignore
    """Readouts of experiments."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    platform: str = Field(default=None)
