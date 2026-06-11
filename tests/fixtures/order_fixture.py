import pytest

from app.models.client_model import Client
from app.models.order_model import Order
from app.repositories.client_db_repository import ClientDbRepository
from app.repositories.order_db_repository import OrderDbRepository
from tests.conftest import db_session

@pytest.fixture()
def db_repo(db_session):
  return OrderDbRepository(db_session)

@pytest.fixture()
async def client_obj(db_session):
  client_obj = Client(
    first_name="client",
    email="client@example.com",
    phone_number="111 111 111"
  )

  client_db_repo = ClientDbRepository(db_session)

  return await client_db_repo.save(client_obj)


@pytest.fixture()
def order_obj(client_obj):
  return Order(
    title="new_job",
    client_id=client_obj.id,
    delivery_address="address 123",
    deal_size=500.00,
    estimated_hours=120.00,
  )