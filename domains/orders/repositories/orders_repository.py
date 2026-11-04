import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domains.orders.models.order_item_model import OrderItemsModel
from domains.orders.models.orders_model import OrdersModel
from domains.products.models.product_model import ProductModel


class OrdersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_order(self, order: OrdersModel) -> None:
        self.db.add(order)
        await self.db.flush()

    async def get_by_id(
        self,
        order_id: uuid.UUID,
        lock: bool = False,
    ) -> OrdersModel | None:
        stmt = select(OrdersModel).where(OrdersModel.id == order_id).options(
            selectinload(OrdersModel.order_items)
            .selectinload(OrderItemsModel.product)
            .selectinload(ProductModel.inventory),
            selectinload(OrdersModel.payments),
        )

        if lock:
            stmt = stmt.with_for_update()

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: uuid.UUID) -> list[OrdersModel]:
        result = await self.db.execute(
            select(OrdersModel)
            .where(OrdersModel.user_id == user_id)
            .options(
                selectinload(OrdersModel.order_items)
                .selectinload(OrderItemsModel.product)
                .selectinload(ProductModel.inventory),
                selectinload(OrdersModel.payments),
            )
            .order_by(OrdersModel.created_at.desc())
        )
        return list(result.scalars().unique().all())

    async def list_all(self) -> list[OrdersModel]:
        result = await self.db.execute(
            select(OrdersModel)
            .options(
                selectinload(OrdersModel.order_items)
                .selectinload(OrderItemsModel.product),
                selectinload(OrdersModel.payments),
            )
            .order_by(OrdersModel.created_at.desc())
        )
        return list(result.scalars().unique().all())

    async def save(
        self,
        order: OrdersModel,
    ) -> OrdersModel:
        self.db.add(order)
        await self.db.flush()
        return order
