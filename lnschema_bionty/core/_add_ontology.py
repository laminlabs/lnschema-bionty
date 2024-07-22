from typing import Iterable, List, Optional, Set, Union

import pandas as pd
from lnschema_core.models import Record

from lnschema_bionty.models import BioRecord, PublicSource


def get_all_ancestors(df: pd.DataFrame, ontology_ids: Iterable[str]) -> Set[str]:
    ancestors = set()

    def get_parents(onto_id: str) -> None:
        try:
            parents = df.at[onto_id, "parents"]
            for parent in parents:
                if parent not in ancestors:
                    ancestors.add(parent)
                    get_parents(parent)
        except KeyError:
            print(f"Warning: Ontology ID {onto_id} not found in DataFrame")

    for onto_id in ontology_ids:
        get_parents(onto_id)

    return ancestors


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.index.name != "ontology_id" and "ontology_id" in df.columns:
        return df.set_index("ontology_id")
    return df


def get_new_ontology_ids(
    registry, ontology_ids: Iterable[str], df_all: pd.DataFrame
) -> Set[str]:
    parents_ids = get_all_ancestors(df_all, ontology_ids)
    ontology_ids = set(ontology_ids) | parents_ids
    existing_ontology_ids = set(
        registry.filter(ontology_id__in=ontology_ids).values_list(
            "ontology_id", flat=True
        )
    )
    return ontology_ids - existing_ontology_ids


def create_records(registry, df: pd.DataFrame) -> List[Record]:
    import lamindb as ln

    df_records = (
        df.reset_index()
        .rename(columns={"definition": "description"})
        .drop(columns=["parents"])
        .to_dict(orient="records")
    )
    try:
        ln.settings.creation.search_names = False
        records = [registry(**record) for record in df_records]
    finally:
        ln.settings.creation.search_names = True

    return records


def create_link_records(
    registry, df: pd.DataFrame, records: List[Record]
) -> List[Record]:
    public_source = records[0].public_source
    linkorm = registry.parents.through
    link_records = []
    for child_id, parents_ids in df["parents"].items():
        if len(parents_ids) == 0:
            continue
        child_record = next(
            (
                r
                for r in records
                if r.ontology_id == child_id and r.public_source == public_source
            ),
            None,
        )
        if not child_record:
            continue
        for parent_id in parents_ids:
            parent_record = next(
                (
                    r
                    for r in records
                    if r.ontology_id == parent_id and r.public_source == public_source
                ),
                None,
            )
            if parent_record:
                link_records.append(
                    linkorm(
                        **{
                            f"from_{registry.__name__.lower()}": child_record,
                            f"to_{registry.__name__.lower()}": parent_record,
                        }
                    )
                )
    return link_records


def add_ontology_from_df(
    registry: BioRecord,
    ontology_ids: List[str] | None = None,
    organism: Union[str, Record, None] = None,
    public_source: Optional[PublicSource] = None,
):
    import lamindb as ln

    df_all = prepare_dataframe(
        registry.public(organism=organism, public_source=public_source).df()
    )

    if ontology_ids is None:
        df = df_all
    else:
        new_ontology_ids = get_new_ontology_ids(registry, ontology_ids, df_all)
        df = df_all[df_all.index.isin(new_ontology_ids)]

    records = create_records(registry, df)
    registry.objects.bulk_create(records)

    all_records = registry.filter().all()
    link_records = create_link_records(registry, df, all_records)
    ln.save(link_records)


def add_ontology(
    records: List[BioRecord],
    organism: Union[str, Record, None] = None,
    public_source: Optional[PublicSource] = None,
):
    registry = records[0]._meta.model
    public_source = public_source or records[0].public_source
    if hasattr(registry, "organism_id"):
        organism = organism or records[0].organism_id
    ontology_ids = [r.ontology_id for r in records]
    add_ontology_from_df(
        registry=registry,
        ontology_ids=ontology_ids,
        organism=organism,
        public_source=public_source,
    )
