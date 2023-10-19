from typing import Optional, Union

from lamin_utils import logger

from ..models import Organism


class Settings:
    """Settings.

    Directly use `lb.settings` rather than instantiating this class yourself.
    """

    def __init__(self):
        self._organism = None
        self._auto_save_parents = True

    @property
    def auto_save_parents(self) -> bool:
        """Automatically save parents."""
        return self._auto_save_parents

    @auto_save_parents.setter
    def auto_save_parents(self, value: bool):
        self._auto_save_parents = value

    @property
    def organism(self) -> Optional[Organism]:
        """Default organism argument (default `None`).

        Default record to use when `organism` argument is required in `lamindb` functionality.

        Only takes effect if explicitly set!

        Examples:
            >>> lb.settings.organism = "mouse"
            ✅ set organism: Organism(id=vado, name=mouse, taxon_id=10090, scientific_name=mus_musculus, updated_at=2023-07-21 11:37:08, bionty_source_id=CXWj, created_by_id=DzTjkKse) # noqa
        """
        return self._organism

    @organism.setter
    def organism(self, name: Union[str, Organism]):
        if isinstance(name, Organism):
            self._organism = name
        else:
            import lamindb as ln

            # do not show the validated message for organism
            verbosity = ln.settings.verbosity
            ln.settings.verbosity = 1
            organism = Organism.from_bionty(name=name)
            ln.settings.verbosity = verbosity
            if organism is None:
                raise ValueError(f"No organism with name='{name}' is found, please create a organism record!")
            if organism._state.adding:  # type:ignore
                organism.save()  # type:ignore
            logger.debug(f"set organism: {organism}")
            self._organism = organism


settings = Settings()
settings.__doc__ = """Global :class:`~lnschema_bionty.dev.Settings`."""
