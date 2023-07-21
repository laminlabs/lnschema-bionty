from typing import Optional, Union

from lamin_logger import logger

from ..models import Species


class Settings:
    """Settings.

    Directly use `lb.settings` rather than instantiating this class yourself.
    """

    def __init__(self):
        self._species = None

    @property
    def species(self) -> Optional[Species]:
        """Default species argument (default `None`).

        Default record to use when `species` argument is required in `lamindb`
        functionality.

        Only takes effect if explicitly set!

        Example:
            >>> lb.settings.species = "mouse"
        """
        return self._species

    @species.setter
    def species(self, name: Union[str, Species]):
        import lnschema_bionty as lb

        species = lb.Species.from_bionty(name=name)
        if species is None:
            raise ValueError(f"No species with name='{name}' is found, please create a species record!")
        if species._state.adding:  # type:ignore
            species.save()  # type:ignore
        logger.success(f"Set species: {species}")
        self._species = species


settings = Settings()
settings.__doc__ = """Global :class:`~lnschema_bionty.dev.Settings`."""
