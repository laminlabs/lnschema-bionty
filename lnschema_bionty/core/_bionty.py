import bionty_base
from lamin_utils import logger


def sync_all_public_sources_to_latest():
    """Sync up the PublicSource registry with the latest available sources.

    Examples:
        >>> from bionty.core import sync_all_public_sources_to_latest
        >>> sync_all_public_sources_to_latest()
    """
    from ..models import PublicSource

    records = PublicSource.filter().all()
    df_sources = bionty_base.display_available_sources().reset_index()
    for _, row in df_sources.iterrows():
        record = records.filter(
            source=row.source,
            version=row.version,
            entity=row.entity,
            organism=row.organism,
        ).one_or_none()
        if record is None:
            record = PublicSource(**row.to_dict())
            record.save()
            logger.success(f"added {record}")
        else:
            # update metadata fields
            record.update(**row.to_dict())
            logger.success(f"updated {record.one()}")
    logger.info("setting the latest version as currently_used...")
    set_latest_public_sources_as_currently_used()
    logger.success("synced up PublicSource registry with the latest available sources")
    logger.warning("please reload your instance to reflect the updates!")


def set_latest_public_sources_as_currently_used():
    """Set the currently_used column to True for the latest version of each source.

    Examples:
        >>> from bionty.core import set_latest_public_sources_as_currently_used
        >>> set_latest_public_sources_as_currently_used()
    """
    from ..models import PublicSource

    records = PublicSource.filter().all()
    df = records.df()
    for (entity, organism), df_group in df.groupby(["entity", "organism"]):
        latest_uid = df_group.sort_values("version", ascending=False).uid.iloc[0]
        records.filter(uid=latest_uid).update(currently_used=True)
        records.filter(entity=entity, organism=organism).exclude(uid=latest_uid).update(currently_used=False)
