from pathlib import Path
from subprocess import run

import pytest
from lamin_logger import logger


def pytest_sessionstart(session: pytest.Session):
    instance_dirs = [d for d in ["./docs/guide/lnbionty-test"] if Path(d).exists()]
    for instance_dir in instance_dirs:
        cmd = f"rm -r {instance_dir}"
        try:
            run(cmd)
            logger.info(cmd)
        except Exception:
            logger.info(f"Could not delete {instance_dir}")
    cmd = "lamin init --storage ./docs/guide/lnbionty-test --schema bionty"
    logger.info(cmd)
    run(cmd, shell=True)
