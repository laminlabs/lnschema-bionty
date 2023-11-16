import bionty as bt
from lamin_utils import logger


def sync_bionty_source_to_latest():
    """Sync up the BiontySource registry with the latest available sources."""
    from ..models import BiontySource

    records = BiontySource.filter().all()
    df_sources = bt.display_available_sources().reset_index()
    for _, row in df_sources.iterrows():
        record = records.filter(
            source=row.source,
            version=row.version,
            entity=row.entity,
            organism=row.organism,
        ).all()
        if len(record) == 0:
            record = BiontySource(**row.to_dict())
            record.save()
            logger.success(f"added {record}")
        else:
            record.update(**row.to_dict())
            logger.success(f"updated {record.one()}")
    logger.info("setting currently_used to latest version...")
    set_currently_used_to_latest()
    logger.success("synced up BiontySource registry with the latest available sources")
    logger.warning("please reload your instance to reflect the updates!")


def set_currently_used_to_latest():
    """Set the currently_used column to True for the latest version of each source."""
    from ..models import BiontySource

    records = BiontySource.filter().all()
    df = records.df()
    for (entity, organism), df_group in df.groupby(["entity", "organism"]):
        latest_uid = df_group.sort_values("version", ascending=False).uid.iloc[0]
        records.filter(uid=latest_uid).update(currently_used=True)
        records.filter(entity=entity, organism=organism).exclude(uid=latest_uid).update(currently_used=False)
