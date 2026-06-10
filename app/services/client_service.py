from sqlalchemy.exc import IntegrityError

from app.core.exceptions import AppBaseException, EmailUnavailableException, PhoneNumberUnavailableException
from app.models.client_model import Client
from app.repositories.client_db_repository import ClientDbRepository
from app.schemas.client_schema import ClientCreate

class ClientService:
  def __init__(self, db_repo: ClientDbRepository):
    self.db_repo = db_repo

  async def save_client(self, client_data: ClientCreate) -> Client:
    if await self.db_repo.get_by_email(client_data.email) is not None:
      raise EmailUnavailableException(f"Email '{client_data.email}' is already in use")
    
    if await self.db_repo.get_by_phone_number(client_data.phone_number) is not None:
      raise PhoneNumberUnavailableException(f"Phone number '{client_data.phone_number}' is already in use")
    
    client_obj = Client(
      first_name=client_data.first_name,
      last_name=client_data.last_name,
      email=client_data.email,
      phone_number=client_data.phone_number,
      notes=client_data.notes
    )

    try:
      await self.db_repo.save(client_obj)

      return client_obj
    
    except IntegrityError as exc:
      if "email" in str(exc.orig):
        raise EmailUnavailableException(f"Email '{client_data.email}' is already in use")
      
      if "phone_number" in str(exc.orig):
        raise PhoneNumberUnavailableException(f"Phone number '{client_data.phone_number}' is already in use")
      
    raise AppBaseException("failed to save client data")