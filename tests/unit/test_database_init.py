from unittest.mock import patch
from app import database_init


def test_init_db():
    with patch.object(
        database_init.Base.metadata, "create_all"
    ) as mock_create_all:
        database_init.init_db()

        mock_create_all.assert_called_once_with(
            bind=database_init.engine
        )

def test_init_db():
    with patch.object(
        database_init.Base.metadata, "create_all"
    ) as mock_create_all:
        database_init.init_db()

        mock_create_all.assert_called_once_with(
            bind=database_init.engine
        )