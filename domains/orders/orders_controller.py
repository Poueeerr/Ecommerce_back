import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from api.middlewares.auth_guard import auth_guard, require_admin
from domains.orders.dependencies import get_order_service, get_user_orders_service
from domains.orders.schemas.orders_schemas import CreateOrder, Order
from domains.orders.services.orders_service import OrdersService
from domains.orders.services.user_orders_service import UserOrdersService

router = APIRouter()


@router.get("/mine", response_model=list[Order])
async def list_my_orders(
    current_user: Annotated[dict, Depends(auth_guard)],
    service: UserOrdersService = Depends(get_user_orders_service),
) -> list[Order]:
    return await service.list_orders(uuid.UUID(current_user["sub"]))


@router.get("/all", response_model=list[Order])
async def list_all_orders(
    _admin: Annotated[dict, Depends(require_admin)],
    service: UserOrdersService = Depends(get_user_orders_service),
) -> list[Order]:
    return await service.list_all()


@router.get("/{order_id}", response_model=Order)
async def get_my_order(
    order_id: uuid.UUID,
    current_user: Annotated[dict, Depends(auth_guard)],
    service: UserOrdersService = Depends(get_user_orders_service),
) -> Order:
    return await service.get_order(order_id, uuid.UUID(current_user["sub"]))


@router.post("/{order_id}/cancel", response_model=Order)
async def cancel_my_order(
    order_id: uuid.UUID,
    current_user: Annotated[dict, Depends(auth_guard)],
    service: UserOrdersService = Depends(get_user_orders_service),
) -> Order:
    return await service.cancel_order(order_id, uuid.UUID(current_user["sub"]))


@router.get("/")
def route_check():
    return {"message": "Orders route"}


@router.post("/create-order", response_model=Order)
async def create_order(
    order_data: CreateOrder,
    current_user: Annotated[dict, Depends(auth_guard)],
    order_service: OrdersService = Depends(get_order_service),
) -> Order:
    return await order_service.create_order(order_data, current_user)
