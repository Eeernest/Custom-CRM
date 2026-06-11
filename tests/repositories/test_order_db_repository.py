import pytest

from tests.fixtures.order_fixture import db_repo, client_obj, order_obj

@pytest.mark.anyio
async def test_save(db_repo, order_obj):
  result = await db_repo.save(order_obj)

  assert result.id is not None