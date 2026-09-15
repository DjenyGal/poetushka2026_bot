from database.models import async_session, Order


async def create_order(user_id: int) -> int:
    async with async_session() as session:
        order = Order(user_id=user_id)
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order.id


async def update_order(order_id: int, **kwargs):
    async with async_session() as session:
        order = await session.get(Order, order_id)
        for key, value in kwargs.items():
            setattr(order, key, value)
        await session.commit()


async def get_order(order_id: int) -> Order:
    async with async_session() as session:
        return await session.get(Order, order_id)