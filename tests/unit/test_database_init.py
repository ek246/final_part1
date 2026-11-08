from unittest.mock import patch
from app import database, database_init
import runpy
from pathlib import Path


def test_database_init_as_script():
    script_path = Path(database.__file__).with_name(
        "database_init.py"
    )

    with patch.object(
        database.Base.metadata, "create_all"
    ) as mock_create_all:
        runpy.run_path(
            str(script_path),
            run_name="__main__",
        )

        mock_create_all.assert_called_once_with(
            bind=database.engine
        )