from typing import Optional, Union

from lamin_utils import logger

from ..models import Species


class Settings:
    """Settings.

    Directly use `lb.settings` rather than instantiating this class yourself.
    """

    def __init__(self):
        self._species = None
        self._auto_save_parents = True

    @property
    def auto_save_parents(self) -> bool:
        """Automatically save parents."""
        return self._auto_save_parents

    @auto_save_parents.setter
    def auto_save_parents(self, value: bool):
        self._auto_save_parents = value

    @property
    def species(self) -> Optional[Species]:
        """Default species argument (default `None`).

        Default record to use when `species` argument is required in `lamindb` functionality.

        Only takes effect if explicitly set!

        Examples:
            >>> lb.settings.species = "mouse"
            ✅ set species: Species(id=vado, name=mouse, taxon_id=10090, scientific_name=mus_musculus, updated_at=2023-07-21 11:37:08, bionty_source_id=CXWj, created_by_id=DzTjkKse) # noqa
        """
        return self._species

    @species.setter
    def species(self, name: Union[str, Species]):
        import lamindb as ln

        import lnschema_bionty as lb

        # do not show the validated message for species
        verbosity = ln.settings.verbosity
        ln.settings.verbosity = 1
        species = lb.Species.from_bionty(name=name)
        ln.settings.verbosity = verbosity
        if species is None:
            raise ValueError(f"No species with name='{name}' is found, please create a species record!")
        if species._state.adding:  # type:ignore
            species.save()  # type:ignore
        logger.save(f"set species: {species}")
        self._species = species


settings = Settings()
settings.__doc__ = """Global :class:`~lnschema_bionty.dev.Settings`."""
