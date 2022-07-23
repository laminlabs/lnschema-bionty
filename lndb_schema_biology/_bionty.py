from typing import Optional  # noqa

from sqlmodel import Field, SQLModel


class species(SQLModel, table=True):  # type: ignore
    """Species table that stores each species as a row."""

    id: Optional[int] = Field(default=None, primary_key=True)
    common_name: str = Field(default=None, index=True)
    taxon_id: str = Field(default=None, index=True)
    scientific_name: str = Field(default=None, index=True)
    short_name: str = Field(default=None)


class geneset_gene(SQLModel, table=True):  # type: ignore
    """Link table between geneset and gene."""

    geneset_id: Optional[int] = Field(
        default=None, foreign_key="geneset.id", primary_key=True
    )
    gene_id: Optional[int] = Field(
        default=None, foreign_key="gene.id", primary_key=True
    )


class geneset(SQLModel, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)


class gene(SQLModel, table=True):  # type: ignore
    """Gene table."""

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(default=None)
    species: str = Field(default=None, foreign_key="species.id")
    name: str = Field(default=None)
    hgnc_id: str = Field(default=None)
    entrez_gene_id: str = Field(default=None)
    ensembl_gene_id: str = Field(default=None)
    alias_symbol: str = Field(default=None)
    locus_group: str = Field(default=None)  # sqlmodel doeesn't work with Literal yet
    locus_type: str = Field(default=None)
    location: str = Field(default=None)
    vega_id: str = Field(default=None)
    ucsc_id: str = Field(default=None)
    rgd_id: str = Field(default=None)
    omim_id: str = Field(default=None)


class proteinset_protein(SQLModel, table=True):  # type: ignore
    """Link table between protein and protein."""

    proteinset_id: Optional[str] = Field(
        default=None, foreign_key="proteinset.id", primary_key=True
    )
    protein_id: Optional[str] = Field(
        default=None, foreign_key="protein.id", primary_key=True
    )


class proteinset(SQLModel, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)


class protein(SQLModel, table=True):  # type: ignore
    """Gene table."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    species: str = Field(default=None, foreign_key="species.id")
    uniprotkb_ac: str = Field(default=None)
    uniprotkb_id: str = Field(default=None)
    pdb_id: str = Field(default=None)
