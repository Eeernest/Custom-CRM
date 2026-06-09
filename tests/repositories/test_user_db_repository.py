import pytest

from tests.fixtures.user_fixture import db_repo, user_obj, saved_user_obj

@pytest.mark.anyio
async def test_save(db_repo, user_obj):
  result = await db_repo.save(user_obj)

  assert result.id is not None
  assert result.username == user_obj.username
  assert result.email == user_obj.email

@pytest.mark.anyio
async def test_get_by_username(db_repo, saved_user_obj):
  result = await db_repo.get_by_username(saved_user_obj.username)

  assert result.username == saved_user_obj.username

@pytest.mark.anyio
async def test_get_by_email(db_repo, saved_user_obj):
  result = await db_repo.get_by_email(saved_user_obj.email)

  assert result.email == saved_user_obj.email