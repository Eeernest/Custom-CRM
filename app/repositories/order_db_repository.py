from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_model import Order

class OrderDbRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  async def save(self, order_obj: Order) -> Order:
    self.session.add(order_obj)
    await self.session.commit()
    await self.session.refresh(order_obj)

    return order_obj