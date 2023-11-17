import datetime
from enum import Enum
import os
from pathlib import Path
import shutil
import tarfile

from dotenv import load_dotenv
from loguru import logger
import typer
import weaviate

BASE = Path(__file__).resolve().parent.parent

load_dotenv(str(BASE / ".env"))


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:bz2") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


class BackupBackend(str, Enum):
    FILESYSTEM = "filesystem"


def main(
    backup_anno: str = "", backend: BackupBackend = BackupBackend.FILESYSTEM
) -> None:
    """
    Backup all data in Weaviate.
    Backups are saved to /mnt/md0/backups/weaviate (configured in weaviate.env using BACKUP_FILESYSTEM_PATH variable.)


    Backup names are automatically generated based on the current date and time.

    If --backup_anno is provided, it will be appended to the backup name.
    """
    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    backup_name = f"{current_date}_{backup_anno}" if backup_anno else current_date
    BASE_BACKUP_DIR = Path("/mnt/md0/backups/weaviate")

    client = weaviate.Client(
        url="http://localhost:8000",
        auth_client_secret=weaviate.AuthApiKey(
            api_key=os.environ["WEAVIATE_ADMIN_PASS"]
        ),
        timeout_config=(5, 99999),
    )
    result = client.backup.create(
        backup_id=backup_name,
        backend=backend,
        wait_for_completion=True,
        # include_classes=["TestContentItem"],
    )
    logger.info(result)

    logger.info("Creating tarfile...")
    make_tarfile(
        output_filename=str(BASE_BACKUP_DIR / f"{backup_name}.tar.bz2"),
        source_dir=str(BASE_BACKUP_DIR / backup_name),
    )

    # logger.info("Deleting unarchived backup...")
    # shutil.rmtree(Path(BASE_BACKUP_DIR / backup_name))

    logger.info("Done.")


if __name__ == "__main__":
    typer.run(main)
