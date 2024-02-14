import pytest
from app import utils
from app.tests.db.conftest import DB_NAME_TEST


@pytest.mark.asyncio
async def test_verify_test_db_used():  # noqa: F811
    session = await utils.get_session()
    url = str(session.get_bind().url)
    assert DB_NAME_TEST == url.split("/")[-1]
