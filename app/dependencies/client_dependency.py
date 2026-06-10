from typing import Annotated

from fastapi import Depends

from app.db.database import SessionDep
from app.repositories.client_db_repository import ClientDbRepository
from app.services.client_service import ClientService

def get_client_service(session: SessionDep):
  db_repo = ClientDbRepository(session)

  return ClientService(db_repo)

ClientServiceDep = Annotated[ClientService, Depends(get_client_service)]