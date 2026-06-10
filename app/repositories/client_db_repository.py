from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client_model import Client

class ClientDbRepository:
  def __init__(self, session: AsyncSession):
    self.session = session
  
  async def get_by_email(self, email: str) -> Client | None:
    result = await self.session.execute(select(Client).where(Client.email == email))

    return result.scalar_one_or_none()
  
  async def get_by_phone_number(self, phone_number: str) -> Client | None:
    result = await self.session.execute(select(Client).where(Client.phone_number == phone_number))

    return result.scalar_one_or_none()

  async def save(self, client_obj: Client) -> Client:
    try:
      self.session.add(client_obj)
      await self.session.commit()
      await self.session.refresh(client_obj)
    
      return client_obj

    except IntegrityError as exc:
      await self.session.rollback()
      raise exc