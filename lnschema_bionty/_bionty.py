from typing import Iterable, List, Literal, Optional, Set, Union  # noqa

import bionty as bt
from django.core.exceptions import ObjectDoesNotExist
from lamin_logger import logger
from lnschema_core.models import BaseORM

from . import ids


def fields_from_knowledge(
    locals: dict,
    bionty_object: bt.Bionty,
) -> List:
    if len(locals) > 1:
        raise AssertionError("Only 1 kwarg can be passed when populating fields from bionty!")
    df = bionty_object._df

    k = next(iter(locals))
    v = locals[k]
    try:
        bionty_dicts = df.set_index(k).loc[[v]].reset_index().to_dict(orient="records")
    except KeyError:
        raise KeyError(f"No entry is found in bionty reference table with '{k}={v}'!\n Try passing a species other than {bionty_object.species}!")

    return bionty_dicts


def create_or_get_species_record(species: Union[str, BaseORM]) -> Optional[BaseORM]:
    if isinstance(species, BaseORM):
        species_record = species
    elif isinstance(species, str):
        from lnschema_bionty import Species

        try:
            species_record = Species.objects.get(name=species)
        except ObjectDoesNotExist:
            try:
                species_record = Species.from_bionty(name=species)
                species_record.bionty_source = get_bionty_source_record(bt.Species())
                species_record.save()
            except KeyError:
                species_record = None
    else:
        species_record = None

    return species_record


def get_bionty_source_record(bionty_object: bt.Bionty):
    kwargs = dict(
        entity=bionty_object.__class__.__name__,
        species=bionty_object.species,
        source=bionty_object.source,
        version=bionty_object.version,
    )
    from .models import BiontySource

    source_record = BiontySource.objects.filter(**kwargs).get()
    if not source_record.currently_used:
        raise AssertionError("Currently used resources are not correctly configured! Please reload your instance!")

    return source_record


def get_bionty_object(model: BaseORM, species: Optional[str] = None):
    if model.__module__.startswith("lnschema_bionty."):
        import bionty as bt

        bionty_object = getattr(bt, model.__name__)(species=species)

        return bionty_object


def _check_synonyms_field_exist(record: BaseORM):
    try:
        record.__getattribute__("synonyms")
    except AttributeError:
        raise NotImplementedError(f"No synonyms field found in table {record.__class__.__name__}!")


def _add_or_remove_synonyms(
    synonym: Union[str, Iterable],
    record: BaseORM,
    action: Literal["add", "remove"],
    force: bool = False,
):
    """Add or remove synonyms."""

    def check_synonyms_in_all_records(synonyms: Set[str], record: BaseORM):
        """Errors if the input synonyms are already associated with records in the DB."""
        import pandas as pd
        from IPython.display import display

        syns_all = record.__class__.objects.exclude(synonyms="").exclude(synonyms=None).all()
        df = pd.DataFrame(syns_all.values())
        df["synonyms"] = df["synonyms"].str.split("|")
        df = df.explode("synonyms")
        matches_df = df[df["synonyms"].isin(synonyms)]
        if matches_df.shape[0] > 0:
            records_df = pd.DataFrame(syns_all.filter(id__in=matches_df["id"]).values())
            logger.error(
                f"Input synonyms {matches_df['synonyms'].unique()} already associated"
                " with the following records:\n(Pass `force=True` to ignore this error)"
            )
            display(records_df)
            raise SystemExit(AssertionError)

    # passed synonyms
    if isinstance(synonym, str):
        syn_new_set = set([synonym])
    else:
        syn_new_set = set(synonym)
    # nothing happens when passing an empty string or list
    if len(syn_new_set) == 0:
        return
    # because we use | as the separator
    if any(["|" in i for i in syn_new_set]):
        raise AssertionError("A synonym can't contain '|'!")

    # existing synonyms
    syns_exist = record.synonyms
    if syns_exist is None or len(syns_exist) == 0:
        syns_exist_set = set()
    else:
        syns_exist_set = set(syns_exist.split("|"))

    if action == "add":
        if not force:
            check_synonyms_in_all_records(syn_new_set, record)
        syns_exist_set.update(syn_new_set)
    elif action == "remove":
        syns_exist_set = syns_exist_set.difference(syn_new_set)

    if len(syns_exist_set) == 0:
        syns_str = None
    else:
        syns_str = "|".join(syns_exist_set)

    record.synonyms = syns_str

    # if the record already exists in the DB, save it
    if not record._state.adding:
        record.save()


def bionty_decorator(django_class):
    @classmethod
    def bionty(cls, species: Optional[str] = None):
        """Bionty object of the entity."""
        return get_bionty_object(model=django_class, species=species)

    @classmethod
    def from_bionty(
        cls,
        lookup_result: Optional[tuple] = None,
        species: Union[str, BaseORM, None] = None,
        **kwargs,
    ):
        """Auto-complete additional fields based on bionty reference."""
        if species is not None:
            species = create_or_get_species_record(species)
        species_name = species.name if species is not None else None
        bionty_object = django_class.bionty(species=species_name)

        if lookup_result is not None:
            if isinstance(lookup_result, list):
                lookups = lookup_result
            else:
                lookups = [lookup_result]

            bionty_dicts = [_encode_id(i._asdict()) for i in lookups]  # type:ignore
        else:
            bionty_dicts = fields_from_knowledge(locals=kwargs, bionty_object=bionty_object)
            bionty_dicts = [_encode_id(bd) for bd in bionty_dicts]

        records = []
        for bionty_dict in bionty_dicts:
            if getattr(django_class, "species", False):
                if species is None:
                    raise AssertionError("Must specify a species!")
                else:
                    bionty_dict["species"] = species
            if getattr(django_class, "bionty_source", False):
                bionty_dict["bionty_source"] = get_bionty_source_record(bionty_object)

            # filter for model fields
            fields = [i.name for i in django_class._meta.fields]
            bionty_dict_fields = {k: v for k, v in bionty_dict.items() if k in fields}

            records.append(django_class(**bionty_dict_fields))

        return records if len(records) > 1 else records[0]

    def _encode_id(kwargs: dict):
        name = django_class.__name__.lower()
        ontology = False
        concat_str = ""
        if name == "gene":
            if kwargs.get("hgnc_id") is not None:
                concat_str = kwargs.get("hgnc_id", "")
            elif kwargs.get("mgi_id") is not None:
                concat_str = kwargs.get("mgi_id", "")
            else:
                concat_str = ""
            concat_str = f"{concat_str}{kwargs.get('ensembl_gene_id', '')}{kwargs.get('ncbi_gene_id', '')}{kwargs.get('symbol', '')}"  # noqa
        elif name == "protein":
            concat_str = kwargs.get("uniprotkb_id", "")
        elif name == "cellmarker":
            concat_str = kwargs.get("name", "")
        elif kwargs.get("id") is not None:
            # species
            concat_str = kwargs.get("id", "")
        elif kwargs.get("ontology_id") is not None:
            concat_str = f"{kwargs.get('name', '')}{kwargs.get('ontology_id', '')}"
            ontology = True
        if len(concat_str) > 0:
            if ontology:
                id_encoder = ids.ontology
            else:
                try:
                    id_encoder = getattr(ids, name)
                except Exception:
                    return kwargs
            kwargs["id"] = id_encoder(concat_str)
        return kwargs

    def add_synonym(self, synonym: Union[str, Iterable], force: bool = False):
        _check_synonyms_field_exist(self)
        _add_or_remove_synonyms(synonym=synonym, record=self, force=force, action="add")

    def remove_synonym(self, synonym: Union[str, Iterable]):
        _check_synonyms_field_exist(self)
        _add_or_remove_synonyms(synonym=synonym, record=self, action="remove")

    django_class.from_bionty = from_bionty
    django_class.bionty = bionty
    django_class.add_synonym = add_synonym
    django_class.remove_synonym = remove_synonym

    return django_class
