from typing import Optional

from lamin_logger import logger


class Settings:
    """Settings.

    Directly use `lnschema_bionty.settings` rather than instantiating this class
    yourself.
    """

    def __init__(self):
        self._species = None

    @property
    def species(self) -> Optional[str]:
        """Default species.

        Default species to use when `species` argument is required.

        Example:
            >>> lb.settings.species = "mouse"
        """
        return self._species

    @species.setter
    def species(self, name: str):
        import lnschema_bionty as lb

        species = lb.Species.from_bionty(name=name)
        if species._state.adding:
            species.save()
        logger.success(f"Set species: {species}")
        self._species = species


settings = Settings()
settings.__doc__ = """Global :class:`~lnschema_bionty.dev.Settings`."""
