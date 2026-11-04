import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from domains.orders.orders_enums import OrderStatus


class _FromModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OrderProduct(_FromModel):
    id: uuid.UUID
    product_name: str
    product_type: str
    product_price: Decimal
    product_description: str
    created_at: datetime
    updated_at: datetime


class OrderItem(_FromModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: Decimal
    product: OrderProduct


class Order(_FromModel):
    id: uuid.UUID
    user_id: uuid.UUID
    total: Decimal
    status: OrderStatus
    order_items: list[OrderItem]
    created_at: datetime
    updated_at: datetime


class OrderSummary(Order):
    payment_status: str | None = None


class CreateOrderItem(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(gt=0)


class CreateOrder(BaseModel):
    items: list[CreateOrderItem] = Field(min_length=1)
