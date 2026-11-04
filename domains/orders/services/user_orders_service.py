import uuid

from domains.inventory.repositories.inventory_repository import InventoryRepository
from domains.orders.models.orders_model import OrdersModel
from domains.orders.orders_enums import OrderStatus
from domains.orders.orders_exceptions import OrderCannotBeCanceled, OrderNotFound
from domains.orders.repositories.orders_repository import OrdersRepository
from domains.payments.payments_enums import PaymentsStatus
from domains.payments.repositories.payments_repository import PaymentsRepository


class UserOrdersService:
    def __init__(
        self,
        repository: OrdersRepository,
        inventory_repository: InventoryRepository | None = None,
        payments_repository: PaymentsRepository | None = None,
    ):
        self.repository = repository
        self.inventory_repository = inventory_repository
        self.payments_repository = payments_repository

    async def list_orders(self, user_id: uuid.UUID) -> list[OrdersModel]:
        return await self.repository.list_by_user(user_id)

    async def get_order(self, order_id: uuid.UUID, user_id: uuid.UUID) -> OrdersModel:
        order = await self.repository.get_by_id(order_id)
        if order is None or order.user_id != user_id:
            raise OrderNotFound
        return order

    async def list_all(self) -> list[OrdersModel]:
        return await self.repository.list_all()

    async def cancel_order(self, order_id: uuid.UUID, user_id: uuid.UUID) -> OrdersModel:
        if self.inventory_repository is None or self.payments_repository is None:
            raise RuntimeError("Cancelamento sem dependencias de estoque e pagamento")
        order = await self.repository.get_by_id(order_id, lock=True)
        if order is None or order.user_id != user_id:
            raise OrderNotFound
        payment = await self.payments_repository.get_by_order_id(order_id, lock=True)
        if order.status != OrderStatus.PAYMENT_PENDING or (
            payment and payment.status not in {PaymentsStatus.PENDING, PaymentsStatus.REJECTED}
        ):
            raise OrderCannotBeCanceled
        for item in order.order_items:
            inventory = await self.inventory_repository.get_item_by_product_id(item.product_id)
            if inventory is not None:
                inventory.reserved_quantity = max(0, inventory.reserved_quantity - item.quantity)
        order.status = OrderStatus.CANCELED
        if payment is not None:
            payment.status = PaymentsStatus.CANCELLED
        await self.inventory_repository.db.commit()
        return order
