from fastapi import APIRouter

from app.dependencies.client_dependency import ClientServiceDep
from app.schemas.client_schema import ClientCreate, ClientRead

router = APIRouter()

@router.post("/save", response_model=ClientRead)
async def save_client(service: ClientServiceDep, client_data: ClientCreate):
  return await service.save_client(client_data)